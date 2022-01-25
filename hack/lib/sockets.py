import json
import logging

import typing as t
from copy import deepcopy

from aiohttp import web, WSMessage
from pip._vendor.tenacity import wait_fixed
from trafaret import DataError, Trafaret
from tenacity import retry, stop_after_attempt

from hack.exceptions import ValidateActionDataException, SendMessageException
from hack.lib.action import Action
from hack.lib.message import (
    BaseMessage,
    JoinMessageData,
    LeaveMessageData,
    AddPeerMessageData,
    RemovePeerMessageData,
    RelaySDPMessageData,
    RelayIceMessageData,
    IceCandidateMessageData,
    SessionDescriptionMessageData,
    DeleteClientMessageData,
    ClientDeletedMessageData,
    ReconnectMessageData,
)
from hack.lib.room import get_room, log_room, remove_room
from hack.models import Client, Room
from hack.utils import to_snake_case
from hack.utils import transform_dict_keys
from hack.utils import to_camel_case
from hack.lib.thread_job import ThreadJob

log = logging.getLogger(__name__)


ACTION_MESSAGE_TRAFARETS_MAPPING: t.Dict[Action, Trafaret] = {
    Action.JOIN: JoinMessageData,
    Action.LEAVE: LeaveMessageData,
    Action.ADD_PEER: AddPeerMessageData,
    Action.REMOVE_PEER: RemovePeerMessageData,
    Action.RELAY_SDP: RelaySDPMessageData,
    Action.RELAY_ICE: RelayIceMessageData,
    Action.ICE_CANDIDATE: IceCandidateMessageData,
    Action.SESSION_DESCRIPTION: SessionDescriptionMessageData,
    Action.DELETE_CLIENT: DeleteClientMessageData,
    Action.CLIENT_DELETED: ClientDeletedMessageData,
    Action.RECONNECT: ReconnectMessageData,
}

STOP_RETRY_ATTEMPTS = stop_after_attempt(5)
WAIT_PERIOD = wait_fixed(0.4)


def validate_action_data(action: Action, data: t.Dict[str, t.Any]):
    trafaret_schema = ACTION_MESSAGE_TRAFARETS_MAPPING[action]
    if not trafaret_schema:
        return
    try:
        trafaret_schema.check(data)
    except DataError as e:
        raise ValidateActionDataException(
            f'Data for action: {action.value} not valid, data {data}, err {e}'
        )


@retry(stop=STOP_RETRY_ATTEMPTS, wait=WAIT_PERIOD, reraise=True)
async def send_msg_to_client_in_room(
    app: web.Application, room_id: str,
    client_peer_id: str, msg_data: t.Dict[str, t.Any]
) -> None:
    # in prd sockets are closing very often, so we make action RECONNECT and
    # here trying to get actual client data with not closed socket
    room = get_room(app, room_id)
    client = room.get_client_by_peer_id(client_peer_id)

    await send_msg(client.ws, msg_data)


async def send_msg(
    ws: web.WebSocketResponse, msg_data: t.Dict[str, t.Any]
) -> None:
    action_str = msg_data['action']
    try:
        action = Action(action_str)
    except ValueError:
        log.warning(f'Try to send unknown action: {action_str}')
        return

    try:
        validate_action_data(action, msg_data['data'])
    except ValidateActionDataException as e:
        log.warning(e)
        return

    msg_data_to_send = deepcopy(msg_data)
    msg_data_to_send['data'] = transform_dict_keys(
        msg_data_to_send['data'], to_camel_case
    )

    data_for_log = deepcopy(msg_data_to_send)
    if data_for_log['data'].get('sessionDescription'):
        data_for_log['data']['sessionDescription'] = {
            'sessionDescription': 'hidden'
        }
    log.debug(f'send_msg to ws: {id(ws)} data {data_for_log} ')

    try:
        await ws.send_json(msg_data_to_send)
    except Exception as e:
        err_msg = (
            f'Error while send_msg to ws: {id(ws)} {msg_data_to_send} {str(e)}'
        )
        log.error(err_msg)
        raise SendMessageException(err_msg)


async def reconnect_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Room not found {room_id}')
        return

    peer_id = data['peer_id']
    client_to_reconnect = room.get_client_by_peer_id(peer_id)
    if not client_to_reconnect:
        log.warning(f'Client {peer_id} not found in room {room_id}')
        return

    old_client_ws_id = id(client_to_reconnect.ws)
    room.set_socket_for_client(
        ws=ws, client_peer_id=client_to_reconnect.peer_id,
    )
    new_client_ws_id = id(client_to_reconnect.ws)

    log.info(
        f'Changed client {peer_id} ws from {old_client_ws_id} '
        f'to {new_client_ws_id}'
    )

    log_room(room)


async def join_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Room not found {room_id}')
        return

    curr_client = Client(
        peer_id=data['client']['peer_id'],
        name=data['client']['name'],
        email=data['client']['email'],
        ws=ws,
    )

    if room.check_is_joined(curr_client.peer_id):
        log.warning(
            f'Client {curr_client.peer_id} already joined to room {room_id}'
        )
        return

    if not room.has_organizer():
        room.set_organizer(curr_client)
        curr_client.is_organizer = True
    elif room.check_is_organizer(curr_client.email):
        curr_client.is_organizer = True

    for client in room.clients:
        log.critical(room.clients)
        msg_data = {
            'action': Action.ADD_PEER.value,
            'data': {
                'client': {
                    'peer_id': curr_client.peer_id,
                    'name': curr_client.name,
                    'email': curr_client.email,
                    'is_organizer': curr_client.is_organizer,
                },
                'create_offer': False
            }
        }
        await send_msg_to_client_in_room(
            app=app, room_id=room.id, client_peer_id=client.peer_id,
            msg_data=msg_data
        )

        msg_data = {
            'action': Action.ADD_PEER.value,
            'data': {
                'client': {
                    'peer_id': client.peer_id,
                    'name': client.name,
                    'email': client.email,
                    'is_organizer': client.is_organizer,
                },
                'create_offer': True
            }
        }
        await send_msg(curr_client.ws, msg_data)

    should_run_ping = not len(room.ws_list)

    room.add_client(curr_client)
    log.info(f'Client: {curr_client.peer_id} joined to room: {room.id}')
    log_room(room)

    if should_run_ping:
        start_pinging(app, room_id)


async def leave_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Room not found {room_id}')
        return

    curr_client = room.get_client_by_ws(ws)

    if not curr_client:
        log.error(f'Client not found in room {room_id}')
        return

    await remove_from_room(app, room, client_to_remove=curr_client)
    log.info(f'Client: {curr_client.peer_id} left room: {room.id}')
    log_room(room)
    if not len(room.ws_list):
        stop_pinging()


async def delete_client_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Room not found {room_id}')
        return

    curr_client = room.get_client_by_ws(ws)

    if not curr_client:
        log.error(f'Client not found in room {room_id}')
        return

    if not curr_client.is_organizer:
        log.error(
            f'Client {curr_client.peer_id} isnt organizer of room {room.id}'
        )
        return

    client_to_remove = room.get_client_by_peer_id(data['peer_id'])
    if not client_to_remove:
        log.error(f'Client {data["peer_id"]} isnt in room {room.id}')
        return

    await remove_from_room(app, room, client_to_remove=client_to_remove)
    log.info(
        f'Client: {client_to_remove.peer_id} was delete from room: {room.id} '
        f'by client {curr_client.peer_id}'
    )
    log_room(room)


async def remove_from_room(
    app: web.Application, room: Room, client_to_remove: Client
) -> None:
    other_clients = [
        client
        for client in room.clients
        if client.peer_id != client_to_remove.peer_id
    ]

    for client in other_clients:
        msg_data = {
            'action': Action.REMOVE_PEER.value,
            'data': {
                'peer_id': client_to_remove.peer_id,
            }
        }
        await send_msg_to_client_in_room(
            app=app, room_id=room.id, client_peer_id=client.peer_id,
            msg_data=msg_data
        )

        msg_data = {
            'action': Action.REMOVE_PEER.value,
            'data': {
                'peer_id': client.peer_id,
            }
        }
        await send_msg_to_client_in_room(
            app=app, room_id=room.id, client_peer_id=client_to_remove.peer_id,
            msg_data=msg_data
        )

    room.remove_client(client_to_remove.peer_id)

    msg_data = {
        'action': Action.CLIENT_DELETED.value,
        'data': {
            'room_id': room.id,
            'peer_id': client_to_remove.peer_id,
        }
    }
    await send_msg(client_to_remove.ws, msg_data)
    log.info(f'Client {client_to_remove.peer_id} removed from room {room.id}')


async def close_room(app: web.Application, room_id: str) -> None:
    room = get_room(app, room_id)
    if not room:
        return

    for client in room.clients:
        try:
            await remove_from_room(app, room, client)
        except Exception as e:
            log.warning(
                f'Error while remove_from_room {room_id}, '
                f'client: {client.peer_id}: {e}'
            )

    remove_room(app, room.id)
    log.info(f'Room {room_id} closed')


async def relay_sdp_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Room not found {room_id}')
        return

    curr_client = room.get_client_by_ws(ws)
    if not curr_client:
        log.error(f'Client not found in room {room_id}')
        return

    msg_data = {
        'action': Action.SESSION_DESCRIPTION.value,
        'data': {
            'peer_id': curr_client.peer_id,
            'session_description': data['session_description']
        }
    }
    target_client = room.get_client_by_peer_id(data['peer_id'])
    await send_msg_to_client_in_room(
        app=app, room_id=room.id, client_peer_id=target_client.peer_id,
        msg_data=msg_data
    )
    log_room(room)


async def relay_ice_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Room not found {room_id}')
        return

    curr_client = room.get_client_by_ws(ws)
    if not curr_client:
        log.error(f'Client not found in room {room_id}')
        return

    msg_data = {
        'action': Action.ICE_CANDIDATE.value,
        'data': {
            'peer_id': curr_client.peer_id,
            'ice_candidate': data['ice_candidate']
        }
    }
    target_client = room.get_client_by_peer_id(data['peer_id'])
    await send_msg_to_client_in_room(
        app=app, room_id=room.id, client_peer_id=target_client.peer_id,
        msg_data=msg_data
    )
    log_room(room)


ACTIONS_PROCESSORS_MAPPING: t.Dict[Action, t.Callable] = {
    Action.JOIN: join_processor,
    Action.LEAVE: leave_processor,
    Action.DELETE_CLIENT: delete_client_processor,
    Action.RELAY_SDP: relay_sdp_processor,
    Action.RELAY_ICE: relay_ice_processor,
    Action.RECONNECT: reconnect_processor,
}


async def process_msg(
    app: web.Application, ws: web.WebSocketResponse, msg: WSMessage
) -> None:
    msg_data: BaseMessage = json.loads(msg.data)

    action_str = msg_data.get('action')
    if not action_str:
        log.warning(f'Received msg without action: {msg}')
        return

    data = msg_data.get('data')
    if not data:
        log.warning(f'Received msg without data: {msg}')
        return

    try:
        action = Action(action_str)
    except ValueError:
        log.warning(f'Received unknown action: {action_str}')
        return

    data = transform_dict_keys(data, to_snake_case)

    try:
        validate_action_data(action, data)
    except ValidateActionDataException as e:
        log.warning(e)
        return

    processor = ACTIONS_PROCESSORS_MAPPING[action]
    try:
        await processor(app, ws, data)
    except Exception as e:
        log.warning(f'Error while run processor: {e}')


def start_pinging(app: web.Application, room_id: str) -> None:
    async def ping():
        room = get_room(app, room_id)
        if room:
            for ws in room.ws_list:
                log.info(f'Ping room_id: {room_id} | socket_id: {id(ws)}')
                if not ws.closed:
                    try:
                        await ws.ping()
                    except:
                        log.info(f'Socket {id(ws)} already closed')

    room = get_room(app, room_id)
    if not room:
        return
    room.periodic_task = ThreadJob(ping, 2)
    room.periodic_task.start()


def stop_pinging(app: web.Application, room_id: str) -> None:
    room = get_room(app, room_id)
    if not room:
        return
    room.periodic_task.remove()
    room.periodic_task = None

import json
import logging

import typing as t

from aiohttp import web, WSMessage
from trafaret import DataError, Trafaret

from hack.exceptions import ValidateActionDataException
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
)
from hack.lib.room import get_room, log_room
from hack.models import Client, Room
from hack.utils import to_snake_case
from hack.utils import transform_dict_keys
from hack.utils import to_camel_case

log = logging.getLogger(__name__)


ACTION_MESSAGE_TRAFARETS_MAPPING: [Action, Trafaret] = {
    Action.JOIN: JoinMessageData,
    Action.LEAVE: LeaveMessageData,
    Action.ADD_PEER: AddPeerMessageData,
    Action.REMOVE_PEER: RemovePeerMessageData,
    Action.RELAY_SDP: RelaySDPMessageData,
    Action.RELAY_ICE: RelayIceMessageData,
    Action.ICE_CANDIDATE: IceCandidateMessageData,
    Action.SESSION_DESCRIPTION: SessionDescriptionMessageData,
    Action.DELETE_CLIENT: DeleteClientMessageData,
}


def validate_action_data(action: Action, data: t.Dict[str, t.Any]):
    trafaret_schema = ACTION_MESSAGE_TRAFARETS_MAPPING[action]
    try:
        trafaret_schema.check(data)
    except DataError as e:
        raise ValidateActionDataException(
            f'Data for action: {action.value} not valid, data {data}, err {e}'
        )


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

    msg_data['data'] = transform_dict_keys(msg_data['data'], to_camel_case)
    log.debug(f'\n\n{"#" * 50}\n send_msg data {msg_data}\n{"#" * 50}\n')
    await ws.send_json(msg_data)


async def join_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    # TODO: make checking room existing as decorator
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
        await send_msg(client.ws, msg_data)

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

    room.add_client(curr_client)
    log.info(f'Client: {curr_client.peer_id} joined to room: {room.id}')
    log_room(room)


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

    await _remove_from_room(room, client_to_remove=curr_client)
    log.info(f'Client: {curr_client.peer_id} left room: {room.id}')
    log_room(room)


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

    await _remove_from_room(room, client_to_remove=client_to_remove)
    log.info(
        f'Client: {client_to_remove.peer_id} was delete from room: {room.id} '
        f'by client {curr_client.peer_id}'
    )
    log_room(room)


async def _remove_from_room(room: Room, client_to_remove: Client) -> None:
    for client in room.clients:
        msg_data = {
            'action': Action.REMOVE_PEER.value,
            'data': {
                'peer_id': client_to_remove.peer_id,
            }
        }
        await send_msg(client.ws, msg_data)

        msg_data = {
            'action': Action.REMOVE_PEER.value,
            'data': {
                'peer_id': client.peer_id,
            }
        }
        await send_msg(client_to_remove.ws, msg_data)

    room.remove_client(client_to_remove.peer_id)
    await client_to_remove.ws.close()


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
    await send_msg(target_client.ws, msg_data)
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
    await send_msg(target_client.ws, msg_data)
    log_room(room)


ACTIONS_PROCESSORS_MAPPING: t.Dict[Action, t.Callable] = {
    Action.JOIN: join_processor,
    Action.LEAVE: leave_processor,
    Action.DELETE_CLIENT: delete_client_processor,
    Action.RELAY_SDP: relay_sdp_processor,
    Action.RELAY_ICE: relay_ice_processor,
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
    await processor(app, ws, data)

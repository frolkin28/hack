import json
import logging

import typing as t

from aiohttp import web, WSMessage

from hack.lib.action import Action
from hack.lib.message import BaseMessage
from hack.lib.room import get_room, log_room
from hack.models import Client
from hack.utils import to_snake_case
from hack.utils import transform_dict_keys
from hack.utils import to_camel_case

log = logging.getLogger(__name__)


async def send_msg(
    ws: web.WebSocketResponse, msg_data: t.Dict[str, t.Any]
) -> None:
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
        log.warning(f'Try joining to non-existent room {room_id}')
        return

    curr_client = Client(
        peer_id=data['client']['id'],
        name=data['client']['name'],
        email=data['client']['email'],
        ws=ws,
    )

    if room.check_is_joined(curr_client.peer_id):
        log.warning(
            f'Client {curr_client.peer_id} already joined to room {room_id}'
        )
        return

    for client in room.clients:
        msg_data = {
            'action': Action.ADD_PEER.value,
            'data': {
                'peer_id': curr_client.peer_id,
                'create_offer': False
            }
        }
        await send_msg(client.ws, msg_data)

        msg_data = {
            'action': Action.ADD_PEER.value,
            'data': {
                'peer_id': client.peer_id,
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
        log.warning(f'Try joining to non-existent room {room_id}')
        return

    curr_client = room.get_client_by_ws(ws)

    if not curr_client:
        log.error(f'Client not found in room {room_id}')
        return

    for client in room.clients:
        msg_data = {
            'action': Action.REMOVE_PEER.value,
            'data': {
                'peer_id': curr_client.peer_id,
            }
        }
        await send_msg(client.ws, msg_data)

        msg_data = {
            'action': Action.REMOVE_PEER.value,
            'data': {
                'peer_id': client.peer_id,
            }
        }
        await send_msg(curr_client.ws, msg_data)

    room.remove_client(curr_client.peer_id)
    await curr_client.ws.close()
    log.info(f'Client: {curr_client.peer_id} left room: {room.id}')
    log_room(room)


async def relay_sdp_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Try joining to non-existent room {room_id}')
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
    target_client = room.get_client_by_id(data['peer_id'])
    await send_msg(target_client.ws, msg_data)


async def relay_ice_processor(
    app: web.Application, ws: web.WebSocketResponse, data: t.Dict[str, t.Any]
) -> None:
    room_id = data['room_id']
    room = get_room(app, room_id)
    if not room:
        log.warning(f'Try joining to non-existent room {room_id}')
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
    target_client = room.get_client_by_id(data['peer_id'])
    await send_msg(target_client.ws, msg_data)


ACTIONS_PROCESSORS_MAPPING: t.Dict[Action, t.Callable] = {
    Action.JOIN: join_processor,
    Action.LEAVE: leave_processor,
    Action.RELAY_SDP: relay_sdp_processor,
    Action.RELAY_ICE: relay_ice_processor,
}


async def process_msg(
    app: web.Application, ws: web.WebSocketResponse, msg: WSMessage
) -> None:
    msg_data: BaseMessage = json.loads(msg.data)

    action = Action(msg_data['action'])
    data = transform_dict_keys(
        msg_data['data'],
        to_snake_case
    )

    processor = ACTIONS_PROCESSORS_MAPPING[action]
    await processor(app, ws, data)

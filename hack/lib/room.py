import logging

import typing as t

from aiohttp import web

from hack.models import Room, Client

log = logging.getLogger(__name__)


def get_room(app: web.Application, room_id: str) -> t.Optional[Room]:
    return app.rooms.get(room_id)

# TODO: add get_rooms(), add_room(), remove_room()


def prepare_client_data(client: Client) -> t.Dict[str, t.Any]:
    return {
        'peerId': client.peer_id,
        'name': client.name,
        'email': client.email,
        'socketId': id(client.ws),
        'isOrganizer': client.is_organizer,
    }


def prepare_room_data(room: Room) -> t.Dict[str, t.Any]:
    return {
        'roomId': room.id,
        'clients': [
            prepare_client_data(client) for client in room.clients
        ]
    }


def log_room(room: Room) -> None:
    log.debug(
        f'\n\n{"#" * 50}\n '
        f'room status {prepare_room_data(room)}'
        f'\n{"#" * 50}\n'
    )

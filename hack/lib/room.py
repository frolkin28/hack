import logging

import typing as t

from aiohttp import web

from hack.models import Room, Client

log = logging.getLogger(__name__)


def get_all_rooms(app: web.Application) -> t.List[Room]:
    return app.rooms.values()


def get_all_rooms_ids(app: web.Application) -> t.List[str]:
    return list(app.rooms.keys())


def get_room(app: web.Application, room_id: str) -> t.Optional[Room]:
    return app.rooms.get(room_id)


def add_room(app: web.Application, room: Room) -> None:
    app.rooms[room.id] = room
    log.info(f'Room {room.id} added')


def remove_room(app: web.Application, room_id: str) -> None:
    app.rooms.pop(room_id)
    log.info(f'Room {room_id} removed')


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
        'organizerEmail': room.organizer_email,
        'clients': [
            prepare_client_data(client) for client in room.clients
        ]
    }


def log_room(room: Room) -> None:
    log.debug(f'room status {prepare_room_data(room)}')

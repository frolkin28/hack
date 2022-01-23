import typing as t

from aiohttp import web

from hack.models import Room


def get_room(app: web.Application, room_id: str) -> t.Optional[Room]:
    return app.rooms.get(room_id)

# TODO: add get_rooms(), add_room(), remove_room()

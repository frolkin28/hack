from aiohttp import web

from hack.handlers import (
    health_check,
    post_room,
    delete_room,
    delete_all_rooms,
    get_root,
    get_template,
    websocket_handler,
    get_room,
    get_rooms
)


def setup_routes(app: web.Application) -> None:

    # health check
    app.router.add_get('/health', health_check)

    # web sockets
    app.router.add_get('/api/ws', websocket_handler)

    # rooms
    app.router.add_post('/api/rooms', post_room)

    app.router.add_get('/api/rooms', get_rooms)
    app.router.add_get('/api/rooms/{room_id}', get_room)

    app.router.add_delete('/api/rooms', delete_all_rooms)
    app.router.add_delete('/api/rooms/{room_id}', delete_room)

    # views
    app.router.add_get('/', get_root)
    app.router.add_get('/{tail:(?!api/)(.+)}/', get_template)

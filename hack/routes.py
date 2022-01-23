from aiohttp import web

from hack.handlers import (
    health_check,
    post_room,
    delete_room,
    delete_all_rooms,
    get_root,
    get_template,
    websocket_handler
)


def setup_routes(app: web.Application) -> None:

    # health check
    app.router.add_get('/health', health_check)

    # web sockets
    app.router.add_get('/api/ws', websocket_handler)

    # rooms
    app.router.add_post('/api/rooms', post_room)
    app.router.add_delete('/api/rooms/{room_id}', delete_room)
    app.router.add_delete('/api/rooms/delete_all', delete_all_rooms)

    # views
    app.router.add_get('/', get_root)
    app.router.add_get('/{tail:(?!api/)(.+)}/', get_template)

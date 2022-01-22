from aiohttp import web

from hack.handlers import health_check, websocket_handler

from hack.views import get_root


def setup_routes(app: web.Application) -> None:

    # health check
    app.router.add_get('/health', health_check)

    # web sockets
    app.router.add_get('/ws', websocket_handler)

    app.router.add_get('/', get_root)

from aiohttp import web

from hack.handlers import health_check
from hack.handlers import get_root
from hack.handlers import get_template
from hack.handlers import websocket_handler


def setup_routes(app: web.Application) -> None:

    # health check
    app.router.add_get('/health', health_check)

    # web sockets
    app.router.add_get('/api/ws', websocket_handler)

    app.router.add_get('/', get_root)
    app.router.add_get('/{tail:(?!api/)(.+)}/', get_template)

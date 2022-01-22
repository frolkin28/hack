from aiohttp import web

from hack.handlers import health_check

from hack.views import get_root


def setup_routes(app: web.Application) -> None:

    # health check
    app.router.add_get('/health', health_check)

    app.router.add_get('/', get_root)

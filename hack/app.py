from asyncio import get_running_loop
from concurrent.futures.thread import ThreadPoolExecutor
from aiohttp.web_app import Application
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_autoreload import start
from hack.config import CONFIG, STATIC_PATH
from hack.middlewares import main_middleware

from hack.routes import setup_routes


async def make_app() -> Application:
    app = Application(
        middlewares=[normalize_path_middleware(), main_middleware],
        debug=CONFIG['is_debug']
    )

    setup_routes(app)

    get_running_loop().set_default_executor(ThreadPoolExecutor(max_workers=4))
    if CONFIG['is_debug']:
        app.router.add_static(CONFIG['static_root'], STATIC_PATH, name='build')
        start()

    return app

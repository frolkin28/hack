import logging

import aiohttp
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request

from hack.config import INDEX_PATH

log = logging.getLogger(__name__)


async def get_root(request: Request) -> FileResponse:  # noqa
    return FileResponse(INDEX_PATH)


async def get_template(request: Request) -> FileResponse:
    return FileResponse(INDEX_PATH)


async def health_check(request: web.Request) -> web.Response:
    return web.json_response({'status': 'ok'}, status=200)


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        log.info(f'\n\n\n\n{"#"*100}\n msg {msg}\n{"#"*100}\n\n')
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            log.error(
                f'ws connection closed with exception {ws.exception()}'
            )

    log.info('websocket connection closed')

    return ws

import logging
import json

from aiohttp import WSMsgType
from aiohttp.web_request import Request
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web import WebSocketResponse

from hack.config import INDEX_PATH

from hack.config import INDEX_PATH


log = logging.getLogger(__name__)


@routes.get('/')
async def get_root(request: Request) -> FileResponse:  # noqa
    return FileResponse(INDEX_PATH)


@routes.get('/{tail:(?!api/)(.+)}/')
async def get_template(request: Request) -> FileResponse:
    return FileResponse(INDEX_PATH)


@routes.get('/api/ws/{room_id}')
async def websocket_handler(request: Request) -> WebSocketResponse:

    ws = WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                message_payload = msg.data
                # message validation stuff here ->

                response = {
                    'peer_id': msg.data
                }
                await ws.send_json(response)
        elif msg.type == WSMsgType.ERROR:
            log.error('ws connection closed with exception %s' %
                      ws.exception())
        elif msg.type == WSMsgType.CLOSE:
            await ws.close()

    log.info('websocket connection closed')

    return ws

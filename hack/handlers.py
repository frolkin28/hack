import json
import logging

import aiohttp
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request

from hack.config import INDEX_PATH
from hack.lib.room import (
    prepare_room_data,
    get_all_rooms_ids,
    add_room,
    get_room as _get_room,
    get_all_rooms,
)
from hack.lib.sockets import process_msg, close_room
from hack.models import Room

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
        log.debug(f'\n\n{"#" * 50}\n receive msg {msg} \n{"#" * 50}\n')
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await process_msg(request.app, ws, msg)
                all_rooms_ids = get_all_rooms_ids(request.app)
                log.debug(
                    f'all current rooms {len(all_rooms_ids)}: {all_rooms_ids}'
                )
        elif msg.type == aiohttp.WSMsgType.ERROR:
            log.error(
                f'ws connection closed with exception {ws.exception()}'
            )

    log.info('websocket connection closed')

    return ws


async def get_room(request: web.Request) -> web.Response:
    room_id = request.match_info['room_id']

    room = _get_room(request.app, room_id)
    if not room:
        return web.Response(
            status=web.HTTPNotFound.status_code,
            text=f'Room {room_id} doesnt exist'
        )

    return web.Response(
        status=web.HTTPOk.status_code,
        body=json.dumps(prepare_room_data(room))
    )


async def get_rooms(request: web.Request) -> web.Response:

    return web.Response(
        status=web.HTTPOk.status_code,
        body=json.dumps(
            [prepare_room_data(room) for room in get_all_rooms(request.app)]
        )
    )


async def post_room(request: web.Request) -> web.Response:
    room = Room()
    add_room(request.app, room)

    return web.Response(
        status=web.HTTPOk.status_code,
        body=json.dumps({'room_id': room.id})
    )


async def delete_room(request: web.Request) -> web.Response:
    room_id = request.match_info['room_id']

    room = _get_room(request.app, room_id)
    if not room:
        return web.Response(
            status=web.HTTPNotFound.status_code,
            text=f'Room {room_id} doesnt exist'
        )

    await close_room(request.app, room.id)

    return web.Response(status=web.HTTPOk.status_code)


async def delete_all_rooms(request: web.Request) -> web.Response:
    rooms_ids = get_all_rooms_ids(request.app)
    for room_id in rooms_ids:
        await close_room(request.app, room_id)

    return web.Response(status=web.HTTPOk.status_code)

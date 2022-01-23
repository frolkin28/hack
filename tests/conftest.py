import pytest
import typing as t

from hack.app import make_app
from hack.lib.room import add_room
from hack.models import Room
from tests.const import TEST_ROOM_ID


@pytest.fixture
async def app_server(aiohttp_server: t.Any) -> t.Any:
    app = await make_app()
    return await aiohttp_server(app)


@pytest.fixture
async def app_server_with_room(aiohttp_server: t.Any) -> t.Any:
    app = await make_app()
    server = await aiohttp_server(app)
    server.rooms = {}
    room = Room()
    room.id = TEST_ROOM_ID
    add_room(server, room)

    return server


@pytest.fixture
async def client(aiohttp_client: t.Any, app_server: t.Any) -> t.Any:
    client = await aiohttp_client(app_server)
    return client

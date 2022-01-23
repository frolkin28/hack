import json

import pytest

from aiohttp import WSMessage, WSMsgType
from aiohttp.web_ws import WebSocketResponse

from hack.lib.action import Action
from tests.lib.const import JOIN_DATA


@pytest.fixture
def ws() -> WebSocketResponse:
    return WebSocketResponse()


@pytest.fixture
def msg() -> WSMessage:
    return WSMessage(
        type=WSMsgType.TEXT,
        data={},
        extra=''
    )


@pytest.fixture
def msg_with_empty_data() -> WSMessage:
    return WSMessage(
        type=WSMsgType.TEXT,
        data=json.dumps({}),
        extra=''
    )


@pytest.fixture
def msg_with_wrong_action() -> WSMessage:
    return WSMessage(
        type=WSMsgType.TEXT,
        data=json.dumps({
            'action': 'some_wrong',
            'data': {
                'aaa': 'bbb'
            }
        }),
        extra=''
    )


@pytest.fixture
def join_msg() -> WSMessage:
    return WSMessage(
        type=WSMsgType.TEXT,
        data=json.dumps({
            'action': Action.JOIN.value,
            'data': JOIN_DATA
        }),
        extra=''
    )

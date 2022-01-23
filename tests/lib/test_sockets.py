import pytest

from aiohttp import WSMessage, web
from pytest_mock.plugin import MockFixture

from hack.exceptions import ValidateActionDataException
from hack.lib.action import Action
from hack.lib.sockets import process_msg, validate_action_data
from tests.lib.const import (
    JOIN_DATA,
    ICE_CANDIDATE_DATA,
    SESSION_DESCRIPTION_DATA,
    REMOVE_PEER_DATA,
    ADD_PEER_DATA,
    RELAY_ICE_DATA,
    RELAY_SDP_DATA,
    DELETE_CLIENT_DATA,
    LEAVE_DATA,
)


async def test_process_msg_empty_msg_data(
    mocker: MockFixture, app_server, ws: web.WebSocketResponse,
    msg_with_empty_data: WSMessage
) -> None:
    transform_dict_keys_mock = mocker.patch(
        'hack.lib.sockets.transform_dict_keys'
    )

    await process_msg(app_server, ws, msg_with_empty_data)

    transform_dict_keys_mock.assert_not_called()


async def test_process_msg_wrong_action(
    mocker: MockFixture, app_server, ws: web.WebSocketResponse,
    msg_with_wrong_action: WSMessage
) -> None:
    transform_dict_keys_mock = mocker.patch(
        'hack.lib.sockets.transform_dict_keys'
    )

    await process_msg(app_server, ws, msg_with_wrong_action)

    transform_dict_keys_mock.assert_not_called()


async def test_process_msg_join_action(
    mocker: MockFixture, app_server_with_room, ws: web.WebSocketResponse,
    join_msg: WSMessage
) -> None:
    transform_dict_keys_mock = mocker.patch(
        'hack.lib.sockets.transform_dict_keys'
    )
    validate_action_data = mocker.patch(
        'hack.lib.sockets.validate_action_data'
    )

    await process_msg(app_server_with_room, ws, join_msg)

    transform_dict_keys_mock.assert_called_once()
    validate_action_data.assert_called_once()


def test_validate_action_data_invalid_data() -> None:
    data = {
        'aaa': 'bbb'
    }
    with pytest.raises(ValidateActionDataException):
        validate_action_data(action=Action.JOIN, data=data)

    with pytest.raises(ValidateActionDataException):
        validate_action_data(action=Action.ADD_PEER, data=data)

    with pytest.raises(ValidateActionDataException):
        validate_action_data(action=Action.SESSION_DESCRIPTION, data=data)


def test_validate_action_data_valid_data() -> None:
    try:
        validate_action_data(action=Action.JOIN, data=JOIN_DATA)
        validate_action_data(action=Action.LEAVE, data=LEAVE_DATA)
        validate_action_data(
            action=Action.DELETE_CLIENT, data=DELETE_CLIENT_DATA
        )
        validate_action_data(action=Action.RELAY_SDP, data=RELAY_SDP_DATA)
        validate_action_data(action=Action.RELAY_ICE, data=RELAY_ICE_DATA)
        validate_action_data(action=Action.ADD_PEER, data=ADD_PEER_DATA)
        validate_action_data(action=Action.REMOVE_PEER, data=REMOVE_PEER_DATA)
        validate_action_data(
            action=Action.SESSION_DESCRIPTION, data=SESSION_DESCRIPTION_DATA
        )
        validate_action_data(
            action=Action.ICE_CANDIDATE, data=ICE_CANDIDATE_DATA
        )
    except ValidateActionDataException:
        pytest.fail("Error")

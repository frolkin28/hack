import logging
import typing as t

from dataclasses import dataclass

from aiohttp.web_ws import WebSocketResponse

from hack.utils import gen_id

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Client:
    id: str
    name: str
    email: str
    ws: WebSocketResponse
    is_organizer: bool = False


class Room:
    def __init__(self):
        self.id = gen_id()
        self.clients = []

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def remove_client(self, client_id: str) -> None:
        self.clients = [
            client for client in self.clients if client.id != client_id
        ]

    async def close(self):
        # TODO: check how it works
        log.info(f'Closing room {self.id}')
        for ws in self.ws_list:
            await ws.close()

    def get_client_by_id(self, client_id: str) -> t.Optional[Client]:
        for _client in self.clients:
            if client_id == _client.id:
                return _client

        return None

    def get_client_by_ws(self, ws: WebSocketResponse) -> t.Optional[Client]:
        for _client in self.clients:
            if ws is _client.ws:
                return _client

        return None

    def check_is_joined(self, client_id: str) -> bool:
        return client_id in (client.id for client in self.clients)

    @property
    def ws_list(self) -> t.List[WebSocketResponse]:
        return [client.ws for client in self.clients]

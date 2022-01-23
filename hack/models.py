import logging
import typing as t

from dataclasses import dataclass

from aiohttp.web_ws import WebSocketResponse

from hack.utils import gen_id

log = logging.getLogger(__name__)


@dataclass
class Client:
    peer_id: str
    name: str
    email: str
    ws: WebSocketResponse
    is_organizer: bool = False


class Room:
    def __init__(self):
        self.id = gen_id()
        self.clients = []
        self.organizer_email = None

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def remove_client(self, client_peer_id: str) -> None:
        self.clients = [
            client
            for client in self.clients
            if client.peer_id != client_peer_id
        ]

    async def close(self):
        # TODO: check how it works
        log.info(f'Closing room {self.id}')
        for ws in self.ws_list:
            await ws.close()

    def get_client_by_peer_id(self, client_peer_id: str) -> t.Optional[Client]:
        for _client in self.clients:
            if client_peer_id == _client.peer_id:
                return _client

        return None

    def get_client_by_ws(self, ws: WebSocketResponse) -> t.Optional[Client]:
        for _client in self.clients:
            if ws is _client.ws:
                return _client

        return None

    def check_is_joined(self, client_peer_id: str) -> bool:
        return client_peer_id in (client.peer_id for client in self.clients)

    def set_organizer(self, client: Client) -> None:
        self.organizer_email = client.email

    def check_is_organizer(self, client_email: str) -> bool:
        return self.organizer_email == client_email

    def has_organizer(self) -> bool:
        return bool(self.organizer_email)

    @property
    def ws_list(self) -> t.List[WebSocketResponse]:
        return [client.ws for client in self.clients]

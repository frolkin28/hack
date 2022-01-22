import typing as t

from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    id: str
    # TODO: typing
    ws_list: t.List[t.Any]
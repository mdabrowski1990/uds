"""Implementation of records queues."""

__all__ = ["RecordsQueue"]

from typing import Union, Type, Tuple

from uds.message import UdsMessageRecord
from uds.packet import AbstractUdsPacket


class RecordsQueue:
    # TODO: docstring

    RecordsTypeAlias = Union[Type[UdsMessageRecord], Type[AbstractUdsPacket]]
    # TODO: docstring
    RecordAlias = Union[UdsMessageRecord, AbstractUdsPacket]

    def __init__(self, records_type: RecordsTypeAlias, history_size: int) -> None:
        ...

    @property
    def records_type(self) -> RecordsTypeAlias:
        ...

    @property
    def max_history_size(self) -> int:
        ...

    @property
    def records_history(self) -> Tuple[RecordAlias, ...]:
        ...

    def put(self, record: RecordAlias) -> None:
        ...

    async def get_next(self) -> RecordAlias:
        ...

    def clear(self) -> None:
        ...

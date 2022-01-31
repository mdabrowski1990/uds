# TODO: docstring

__all__ = ["TransmissionQueue"]

from typing import Union, Optional, Type

from uds.message import UdsMessage
from uds.packet import AbstractUdsPacket


class TransmissionQueue:
    # TODO: docstring

    PDUAlias = Union[UdsMessage, AbstractUdsPacket]
    # TODO: docstring
    PDUTypeAlias = Union[Type[UdsMessage], Type[AbstractUdsPacket]]
    # TODO: docstring

    def __init__(self, pdu_type: PDUTypeAlias) -> None:
        ...

    def __len__(self) -> int:
        ...

    @property
    def pdu_type(self) -> PDUTypeAlias:
        ...

    @property
    def is_empty(self) -> bool:
        ...

    def mark_task_done(self):
        ...

    def clear(self) -> None:
        ...

    async def get_pdu(self) -> PDUAlias:
        ...

    def put_pdu(self, pdu: PDUAlias, timestamp: Optional[float] = None) -> None:
        ...

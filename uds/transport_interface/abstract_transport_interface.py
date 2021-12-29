"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from typing import Optional, Tuple, Any
from abc import ABC, abstractmethod
from datetime import datetime

from uds.utilities import TimeMilliseconds
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.message import UdsMessage, UdsMessageRecord
from .packet_queues import TimestampedPacketsQueue, PacketsQueue


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface class.

    Transport Interface classes are meant to handle middle layers of UDs
    """

    def __init__(self,
                 bus_handler: Any,
                 max_packet_records_stored: int,  # TODO: define and add default value
                 max_message_records_stored: int  # TODO: define and add default value
                 ) -> None:
        ...

    @abstractmethod  # TODO: assess whether abstract
    def send_packet(self, packet: AbstractUdsPacket, delay: Optional[TimeMilliseconds] = None) -> None:
        ...

    @abstractmethod  # TODO: assess whether abstract
    def send_message(self, message: UdsMessage, delay: Optional[TimeMilliseconds] = None) -> None:
        ...

    @property
    @abstractmethod  # TODO: assess whether abstract
    def packet_records(self) -> Tuple[AbstractUdsPacketRecord, ...]:
        ...

    @property
    @abstractmethod  # TODO: assess whether abstract
    def message_records(self) -> Tuple[UdsMessageRecord, ...]:
        ...

    @abstractmethod  # TODO: assess whether abstract
    async def await_packet_received(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        ...

    @abstractmethod  # TODO: assess whether abstract
    async def await_packet_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        ...

    @abstractmethod  # TODO: assess whether abstract
    async def await_message_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        ...

    @abstractmethod  # TODO: assess whether abstract
    async def await_message_received(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        ...

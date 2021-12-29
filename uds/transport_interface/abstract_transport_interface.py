"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from typing import Optional, Tuple, Any
from abc import ABC, abstractmethod

from uds.utilities import TimeMilliseconds
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.message import UdsMessage, UdsMessageRecord


DEFAULT_PACKET_RECORDS_STORED: int = 100
"""Default size of container for UDS packet records in Transport Interface."""
DEFAULT_MESSAGE_RECORDS_STORED: int = 10
"""Default size of container for UDS message records in Transport Interface."""


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface class.

    Transport Interface classes are meant to handle middle layers of UDs
    """

    def __init__(self,
                 bus_handler: Any,
                 max_packet_records_stored: int = DEFAULT_PACKET_RECORDS_STORED,
                 max_message_records_stored: int = DEFAULT_MESSAGE_RECORDS_STORED) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_handler: An object that handles the bus (Physical and Data layers of OSI Model).
        :param max_packet_records_stored: Maximal number of UDS packet records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.packet_records`.
        :param max_message_records_stored: Maximal number of UDS message records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.message_records`.
        """
        raise NotImplementedError

    @property
    def bus_handler(self) -> Any:
        """An object which handles the bus (Physical and Data layers of OSI Model) for this Transport Interface."""
        raise NotImplementedError

    @property
    def packet_records(self) -> Tuple[AbstractUdsPacketRecord, ...]:
        """Container with records of UDS packets that was either received or transmitted on the bus."""
        raise NotImplementedError

    @property
    def message_records(self) -> Tuple[UdsMessageRecord, ...]:
        """Container with records of UDS Messages that was either received or transmitted on the bus."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_supported_bus_handler(bus_handler: Any) -> bool:
        """
        Check whether provided value is a bus handler that is supported by this Transport Interface.

        :param bus_handler: Value to check.

        :return: True if provided object can handle the bus for this Transport Interface, False otherwise.
        """

    async def await_packet_received(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        """
        Wait until the next UDS packet is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just received.
        """
        raise NotImplementedError

    async def await_packet_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        """
        Wait until the next UDS packet is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just transmitted.
        """
        raise NotImplementedError

    async def await_message_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        """
        Wait until the next UDS message is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just received.
        """
        raise NotImplementedError

    async def await_message_received(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        """
        Wait until the next UDS message is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just transmitted.
        """
        raise NotImplementedError

    @abstractmethod
    def send_packet(self, packet: AbstractUdsPacket, delay: Optional[TimeMilliseconds] = None) -> None:
        """
        Transmit UDS packet on the configured bus.

        :param packet: A packet to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """

    @abstractmethod
    def send_message(self, message: UdsMessage, delay: Optional[TimeMilliseconds] = None) -> None:
        """
        Transmit UDS message on the configured bus.

        :param message: A message to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """

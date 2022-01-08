"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from typing import Optional, Tuple, Any
from abc import ABC, abstractmethod

from uds.utilities import TimeMilliseconds
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.message import UdsMessage, UdsMessageRecord
from uds.segmentation import AbstractSegmenter
from .packet_queues import PacketsQueue, TimestampedPacketsQueue
from .consts import DEFAULT_PACKET_RECORDS_STORED, DEFAULT_MESSAGE_RECORDS_STORED


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface.

    Transport Interfaces are meant to handle middle layers (Transport and Network) of UDS OSI Model.
    """

    def __init__(self,
                 bus_manager: Any,
                 max_packet_records_stored: int = DEFAULT_PACKET_RECORDS_STORED,
                 max_message_records_stored: int = DEFAULT_MESSAGE_RECORDS_STORED) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).
        :param max_packet_records_stored: Maximal number of UDS packet records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.packet_records`.
        :param max_message_records_stored: Maximal number of UDS message records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.message_records`.

        :raise ValueError: Provided value of bus_manager is incompatible with this Transport Interface.
        """
        if not self.is_supported_bus_manager(bus_manager):
            raise ValueError("Provided value of bus_manager is incompatible with this Transport Interface.")
        self.__bus_manager = bus_manager

    @property
    def bus_manager(self) -> Any:
        """
        Value of the bus manager used by this Transport Interface.

        Bus manager handles Physical and Data layers (OSI Model) of the bus.
        """
        return self.__bus_manager

    @property
    @abstractmethod
    def segmenter(self) -> AbstractSegmenter:
        """Value of the segmenter used by this Transport Interface."""

    @property
    @abstractmethod
    def _input_packets_queue(self) -> PacketsQueue:
        """Queue with records of UDS Packets that were either received or transmitted."""

    @property
    @abstractmethod
    def _output_packet_queue(self) -> TimestampedPacketsQueue:
        """Queue with UDS Packets that are planned for the transmission."""

    @property  # noqa: F841
    def packet_records(self) -> Tuple[AbstractUdsPacketRecord, ...]:
        """Container with records of UDS packets that were either received or transmitted."""
        raise NotImplementedError

    @property  # noqa: F841
    def message_records(self) -> Tuple[UdsMessageRecord, ...]:
        """Container with records of UDS Messages that were either received or transmitted."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """

    @abstractmethod
    async def await_packet_received(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        """
        Wait until the next UDS packet is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just received.
        """

    @abstractmethod
    async def await_packet_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        """
        Wait until the next UDS packet is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just transmitted.
        """

    @abstractmethod
    async def await_message_received(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        """
        Wait until the next UDS message is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just received.
        """

    @abstractmethod
    async def await_message_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:
        """
        Wait until the next UDS message is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just transmitted.
        """

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

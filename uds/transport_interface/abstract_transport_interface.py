"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from typing import Optional, Any
from abc import ABC, abstractmethod

from uds.utilities import TimeMilliseconds
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.message import UdsMessage, UdsMessageRecord
from uds.segmentation import AbstractSegmenter
from .packet_queues import PacketsQueue


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface.

    Transport Interfaces are meant to handle middle layers (Transport and Network) of UDS OSI Model.
    """

    def __init__(self,
                 bus_manager: Any,
                 packet_records_number: int,
                 message_records_number: int) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).
        :param packet_records_number: Number of UDS packet records to store.
        :param message_records_number: Number of UDS Message records to store.

        :raise ValueError: Provided value of bus manager is not supported by this Transport Interface.
        """
        if not self.is_supported_bus_manager(bus_manager):
            raise ValueError("Unsupported bus manager was provided.")
        self.__bus_manager = bus_manager

    @property
    def bus_manager(self) -> Any:
        """
        Value of the bus manager used by this Transport Interface.

        Bus manager handles Physical and Data layers (OSI Model) of the bus.
        """
        return self.__bus_manager

    @property
    def packet_records_queue(self) -> PacketsQueue:
        """Queue with records of UDS packets that were either received or transmitted."""
        return self.__packet_records_queue

    @property
    def message_records_queue(self):  # TODO: annotation
        """Queue with records of UDS Messages that were either received or transmitted."""
        return self.__message_records_queue

    @property
    @abstractmethod
    def segmenter(self) -> AbstractSegmenter:
        """Value of the segmenter used by this Transport Interface."""

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

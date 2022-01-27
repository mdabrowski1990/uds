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
                 bus_manager: Any,  # noqa: F841
                 max_packet_records_stored: int,  # noqa: F841
                 max_message_records_stored: int) -> None:  # noqa: F841
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).
        :param max_packet_records_stored: Maximal number of UDS packet records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.packet_records`.
        :param max_message_records_stored: Maximal number of UDS message records to be stored in
            :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.message_records`.
        """
        raise NotImplementedError

    @property  # noqa: F841
    def bus_manager(self) -> Any:
        """
        Value of the bus manager used by this Transport Interface.

        Bus manager handles Physical and Data layers (OSI Model) of the bus.
        """
        raise NotImplementedError

    @property  # noqa: F841
    @abstractmethod
    def segmenter(self) -> AbstractSegmenter:
        """Value of the segmenter used by this Transport Interface."""

    @property  # noqa: F841
    def packet_records_queue(self) -> PacketsQueue:
        """Queue with records of UDS packets that were either received or transmitted."""
        raise NotImplementedError

    @property  # noqa: F841
    def message_records_queue(self):  # TODO: annotation
        """Queue with records of UDS Messages that were either received or transmitted."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:  # noqa: F841
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """

    @abstractmethod
    async def await_packet_received(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:  # noqa: F841
        """
        Wait until the next UDS packet is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just received.
        """

    @abstractmethod
    async def await_packet_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:  # noqa: F841
        """
        Wait until the next UDS packet is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a packet that was just transmitted.
        """

    @abstractmethod
    async def await_message_received(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:  # noqa: F841
        """
        Wait until the next UDS message is received.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just received.
        """

    @abstractmethod
    async def await_message_transmitted(self, timeout: Optional[TimeMilliseconds] = None) -> UdsMessageRecord:  # noqa: F841
        """
        Wait until the next UDS message is transmitted.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information of a message that was just transmitted.
        """

    @abstractmethod
    def send_packet(self, packet: AbstractUdsPacket, delay: Optional[TimeMilliseconds] = None) -> None:  # noqa: F841
        """
        Transmit UDS packet on the configured bus.

        :param packet: A packet to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """

    @abstractmethod
    def send_message(self, message: UdsMessage, delay: Optional[TimeMilliseconds] = None) -> None:  # noqa: F841
        """
        Transmit UDS message on the configured bus.

        :param message: A message to send.
        :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
            None if the transmission to be executed immediately.
        """

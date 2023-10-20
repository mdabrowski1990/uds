"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from typing import Optional, Any
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop

from uds.utilities import TimeMilliseconds
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.segmentation import AbstractSegmenter


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface.

    Transport Interfaces are meant to handle middle layers (Transport and Network) of UDS OSI Model.
    """

    def __init__(self, bus_manager: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).

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
    @abstractmethod
    def segmenter(self) -> AbstractSegmenter:
        """
        Value of the segmenter used by this Transport Interface.

        .. warning:: Do not change any segmenter attributes as it might cause malfunction of the entire
            Transport Interface.
        """

    @staticmethod
    @abstractmethod
    def is_supported_bus_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided bus object is compatible with this Transport Interface, False otherwise.
        """

    @abstractmethod
    def send_packet(self, packet: AbstractUdsPacket) -> AbstractUdsPacketRecord:
        """
        Transmit UDS packet.

        :param packet: A packet to send.

        :return: Record with historic information about transmitted UDS packet.
        """

    @abstractmethod
    def receive_packet(self, timeout: Optional[TimeMilliseconds] = None) -> AbstractUdsPacketRecord:
        """
        Receive UDS packet.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received UDS packet.
        """

    @abstractmethod
    async def async_send_packet(self,
                                packet: AbstractUdsPacket,
                                loop: Optional[AbstractEventLoop] = None) -> AbstractUdsPacketRecord:
        """
        Transmit UDS packet asynchronously.

        :param packet: A packet to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about transmitted UDS packet.
        """

    @abstractmethod
    async def async_receive_packet(self,
                                   timeout: Optional[TimeMilliseconds] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> AbstractUdsPacketRecord:
        """
        Receive UDS packet asynchronously.

        :param timeout: Maximal time (in milliseconds) to wait.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TimeoutError: Timeout was reached.
        :raise asyncio.TimeoutError: Timeout was reached.

        :return: Record with historic information about received UDS packet.
        """

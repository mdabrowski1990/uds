"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Any, Optional

from uds.addressing import AbstractAddressingInformation
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import AbstractPacket, AbstractPacketRecord
from uds.segmentation import AbstractSegmenter
from uds.utilities import ReassignmentError, TimeMillisecondsAlias


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface.

    Transport Interfaces are meant to handle middle layers (Transport and Network) of UDS OSI Model.
    """

    def __init__(self,
                 network_manager: Any) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param network_manager: An object that handles the network (Physical and Data layers of OSI Model).
        """
        self.network_manager = network_manager

    @property
    @abstractmethod
    def segmenter(self) -> AbstractSegmenter:
        """
        Value of the segmenter used by this Transport Interface.

        .. warning:: Do not change any segmenter attributes during the communication as it might introduce
            faults to Transport Interface.
        """

    @property
    def addressing_information(self) -> AbstractAddressingInformation:
        """Get Addressing Information of UDS Entity simulated by this Transport Interface."""
        return self.segmenter.addressing_information

    @addressing_information.setter
    def addressing_information(self, value: AbstractAddressingInformation) -> None:
        """
        Set Addressing Information of UDS Entity simulated by this Transport Interface.

        :param value: Addressing Information value to set.
        """
        self.segmenter.addressing_information = value

    @property
    def network_manager(self) -> Any:
        """
        Get network manager used by this Transport Interface.

        Network manager handles Physical and Data layers (OSI Model) of the bus/network.
        """
        return self.__network_manager

    @network_manager.setter
    def network_manager(self, value: Any) -> None:
        """
        Set value of network manager used by this Transport Interface.

        :param value: Value to set.

        :raise ValueError: Provided value is not a supported Network Manager.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not self.is_supported_network_manager(value):
            raise ValueError("Unsupported network manager was provided.")
        if hasattr(self, "_AbstractTransportInterface__network_manager"):
            raise ReassignmentError("Value of 'network_manager' attribute cannot be changed once assigned.")
        self.__network_manager = value

    @staticmethod
    @abstractmethod
    def is_supported_network_manager(bus_manager: Any) -> bool:
        """
        Check whether provided value is a bus/network manager that is supported by this Transport Interface.

        :param bus_manager: Value to check.

        :return: True if provided object is compatible with this Transport Interface, False otherwise.
        """

    @abstractmethod
    def send_packet(self, packet: AbstractPacket) -> AbstractPacketRecord:
        """
        Transmit packet.

        :param packet: A packet to send.

        :return: Record with historic information about transmitted packet.
        """

    @abstractmethod
    async def async_send_packet(self,
                                packet: AbstractPacket,
                                loop: Optional[AbstractEventLoop] = None) -> AbstractPacketRecord:
        """
        Transmit packet asynchronously.

        :param packet: A packet to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about transmitted packet.
        """

    @abstractmethod
    def receive_packet(self, timeout: Optional[TimeMillisecondsAlias] = None) -> AbstractPacketRecord:
        """
        Receive packet.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received packet.
        """

    @abstractmethod
    async def async_receive_packet(self,
                                   timeout: Optional[TimeMillisecondsAlias] = None,
                                   loop: Optional[AbstractEventLoop] = None) -> AbstractPacketRecord:
        """
        Receive packet asynchronously.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise TimeoutError: Timeout was reached.
        :raise asyncio.TimeoutError: Timeout was reached.

        :return: Record with historic information about received packet.
        """

    @abstractmethod
    def send_message(self, message: UdsMessage) -> UdsMessageRecord:
        """
        Transmit UDS message.

        :param message: A message to send.

        :return: Record with historic information about transmitted UDS message.
        """

    @abstractmethod
    async def async_send_message(self,
                                 message: UdsMessage,
                                 loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Transmit asynchronously UDS message.

        :param message: A message to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about transmitted UDS message.
        """

    @abstractmethod
    def receive_message(self, timeout: Optional[TimeMillisecondsAlias] = None) -> UdsMessageRecord:
        """
        Receive UDS message.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received UDS message.
        """

    @abstractmethod
    async def async_receive_message(self,
                                    timeout: Optional[TimeMillisecondsAlias] = None,
                                    loop: Optional[AbstractEventLoop] = None) -> UdsMessageRecord:
        """
        Receive asynchronously UDS message.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about received UDS message.
        """

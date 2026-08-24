"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Any
from warnings import warn

from uds.addressing import AbstractAddressingInformation
from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import AbstractPacket, AbstractPacketRecord
from uds.segmentation import AbstractSegmenter
from uds.utilities import ReassignmentError, TimeMillisecondsAlias, TimeSync


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
        self.__time_sync: TimeSync = TimeSync()

    @property
    def time_sync(self) -> TimeSync:
        """Get time and timestamp synchronizer."""
        return self.__time_sync

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
        raise ReassignmentError("Value of 'frame' attribute cannot be changed once set.")
        """
        if not self.is_supported_network_manager(value):
            raise ValueError("Unsupported network manager was provided.")
        if hasattr(self, "_AbstractTransportInterface__network_manager"):
            raise ReassignmentError("Value of 'network_manager' attribute cannot be changed once set.")
        self.__network_manager = value

    @property
    @abstractmethod
    def is_sync_active(self) -> bool:
        """Get flag indicating whether synchronous communication is active."""

    @property
    @abstractmethod
    def is_async_active(self) -> bool:
        """Get flag indicating whether asynchronous communication is active."""

    @abstractmethod
    def setup_sync(self) -> None:
        """
        Prepare this Transport Interface for synchronous communication.

        This method activates synchronous communication and deactivates asynchronous communication.
        """

    @abstractmethod
    def setup_async(self, loop: AbstractEventLoop) -> None:
        """
        Prepare this Transport Interface for asynchronous communication.

        This method activates asynchronous communication and deactivates synchronous communication.

        :param loop: An :mod:`asyncio` event loop to use.
        """

    @abstractmethod
    def teardown_sync(self, suppress_warning: bool = False) -> None:
        """
        Deactivate synchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        if self.is_sync_active and not suppress_warning:
            warn(message="Synchronous (send_packet, receive_packet, send_message and receive_message) and "
                         "Asynchronous (async_send_packet, async_receive_packet, async_send_message, "
                         "async_receive_message) communication cannot be used together.",
                 category=UserWarning)

    @abstractmethod
    def teardown_async(self, suppress_warning: bool = False) -> None:
        """
        Deactivate asynchronous communication.

        :param suppress_warning: Do not warn about mixing Synchronous and Asynchronous implementation.
        """
        if self.is_async_active and not suppress_warning:
            warn(message="Synchronous (send_packet, receive_packet, send_message and receive_message) and "
                         "Asynchronous (async_send_packet, async_receive_packet, async_send_message, "
                         "async_receive_message) communication cannot be used together.",
                 category=UserWarning)

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
                                loop: AbstractEventLoop | None = None) -> AbstractPacketRecord:
        """
        Transmit packet asynchronously.

        :param packet: A packet to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about transmitted packet.
        """

    @abstractmethod
    def receive_packet(self, timeout: TimeMillisecondsAlias | None = None) -> AbstractPacketRecord:
        """
        Receive packet.

        :param timeout: Maximal time (in milliseconds) to wait.
            Leave None to wait forever.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received packet.
        """

    @abstractmethod
    async def async_receive_packet(self,
                                   timeout: TimeMillisecondsAlias | None = None,
                                   loop: AbstractEventLoop | None = None) -> AbstractPacketRecord:
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
                                 loop: AbstractEventLoop | None = None) -> UdsMessageRecord:
        """
        Transmit asynchronously UDS message.

        :param message: A message to send.
        :param loop: An asyncio event loop to use for scheduling this task.

        :return: Record with historic information about transmitted UDS message.
        """

    @abstractmethod
    def receive_message(self,
                        start_timeout: TimeMillisecondsAlias | None = None,
                        end_timeout: TimeMillisecondsAlias | None = None) -> UdsMessageRecord:
        """
        Receive UDS message.

        .. warning:: Value of end_timeout must not be less than the value of start_timeout.

        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
            Leave None to wait forever.
        :param end_timeout: Maximal time (in milliseconds) to wait for a message transmission to finish.
            Leave None to wait forever.

        :raise MessageTransmissionNotStartedError: Timeout was exceeded before message reception started.
        :raise TimeoutError: Timeout was exceeded during message receiving (before all packets received).

        :return: Record with historic information about received UDS message.
        """

    @abstractmethod
    async def async_receive_message(self,
                                    start_timeout: TimeMillisecondsAlias | None = None,
                                    end_timeout: TimeMillisecondsAlias | None = None,
                                    loop: AbstractEventLoop | None = None) -> UdsMessageRecord:
        """
        Receive asynchronously UDS message.

        .. warning:: Value of end_timeout must not be less than the value of start_timeout.

        :param start_timeout: Maximal time (in milliseconds) to wait for the start of a message transmission.
            Leave None to wait forever.
        :param end_timeout: Maximal time (in milliseconds) to wait for a message transmission to finish.
            Leave None to wait forever.
        :param loop: An asyncio event loop to use for scheduling this task.

        :raise MessageTransmissionNotStartedError: Timeout was exceeded before message reception started.
        :raise TimeoutError: Timeout was exceeded during message receiving (before all packets received).

        :return: Record with historic information about received UDS message.
        """

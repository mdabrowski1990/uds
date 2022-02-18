"""Abstract definition of UDS Transport Interface."""

__all__ = ["AbstractTransportInterface"]

from typing import Optional, Any, Tuple
from abc import ABC, abstractmethod

from uds.utilities import TimeMilliseconds
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.message import UdsMessage, UdsMessageRecord
from uds.segmentation import AbstractSegmenter
from .records_queue import RecordsQueue
from .transmission_queue import TransmissionQueue


class AbstractTransportInterface(ABC):
    """
    Abstract definition of Transport Interface.

    Transport Interfaces are meant to handle middle layers (Transport and Network) of UDS OSI Model.
    """

    DEFAULT_PACKET_RECORDS_NUMBER: int = 100
    """Default number of UDS packet records stored."""
    DEFAULT_MESSAGE_RECORDS_NUMBER: int = 10
    """Default number of UDS message records stored."""

    def __init__(self,
                 bus_manager: Any,
                 message_records_number: int = DEFAULT_MESSAGE_RECORDS_NUMBER) -> None:
        """
        Create Transport Interface (an object for handling UDS Transport and Network layers).

        :param bus_manager: An object that handles the bus (Physical and Data layers of OSI Model).
        :param message_records_number: Number of UDS Message records to store.

        :raise ValueError: Provided value of bus manager is not supported by this Transport Interface.
        """
        if not self.is_supported_bus_manager(bus_manager):
            raise ValueError("Unsupported bus manager was provided.")
        self.__bus_manager = bus_manager
        self.__message_records_queue = RecordsQueue(records_type=UdsMessageRecord, history_size=message_records_number)
        self.__message_transmission_queue = TransmissionQueue(pdu_type=UdsMessage)

    @property
    @abstractmethod
    def _packet_records_queue(self) -> RecordsQueue:
        """Queue with UDS packet records that were either received or transmitted."""

    @property  # noqa: F841
    @abstractmethod
    def _packet_transmission_queue(self) -> TransmissionQueue:
        """Queue with UDS packets that are planned for the transmission."""

    @property
    def _message_records_queue(self) -> RecordsQueue:
        """Queue with UDS messages records that were either received or transmitted."""
        return self.__message_records_queue

    @property  # noqa: F841
    def _message_transmission_queue(self) -> TransmissionQueue:
        """Queue with UDS messages that are planned for the transmission."""
        return self.__message_transmission_queue

    @property
    def bus_manager(self) -> Any:
        """
        Value of the bus manager used by this Transport Interface.

        Bus manager handles Physical and Data layers (OSI Model) of the bus.
        """
        return self.__bus_manager

    @property  # noqa: F841
    def message_records_history(self) -> Tuple[UdsMessageRecord]:
        """Historic records of UDS messages that were either received or transmitted."""
        return self._message_records_queue.records_history  # type: ignore

    @property  # noqa: F841
    def packet_records_history(self) -> Tuple[AbstractUdsPacketRecord]:
        """Historic records of UDS packets that were either received or transmitted."""
        return self._packet_records_queue.records_history  # type: ignore

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

    # async def await_packet_received(self,
    #                                 timeout: Optional[TimeMilliseconds] = None,  # noqa: F841
    #                                 ignore_interruptions: bool = False) -> AbstractUdsPacketRecord:  # noqa: F841
    #     """
    #     Wait until the next UDS packet is received.
    #
    #     :param timeout: Maximal time (in milliseconds) to wait.
    #     :param ignore_interruptions: Flag informing whether to stop if meanwhile UDS packet was transmitted.
    #
    #         - True - ignore transmitted UDS packets and do not raise InterruptedError
    #         - False - raise InterruptedError if UDS packet is transmitted when awaiting
    #
    #     :raise TypeError: Timeout value is not int or float type.
    #     :raise ValueError: Timeout value is less or equal 0.
    #     :raise TimeoutError: Timeout was reached.
    #     :raise InterruptedError: UDS packet was transmitted during awaiting.
    #
    #     :return: Record with historic information of a packet that was just received.
    #     """
    #     raise NotImplementedError
    #
    # async def await_packet_transmitted(self,
    #                                    timeout: Optional[TimeMilliseconds] = None,  # noqa: F841
    #                                    ignore_interruptions: bool = False) -> AbstractUdsPacketRecord:  # noqa: F841
    #     """
    #     Wait until the next UDS packet is transmitted.
    #
    #     :param timeout: Maximal time (in milliseconds) to wait.
    #     :param ignore_interruptions: Flag informing whether to stop if meanwhile UDS packet was received.
    #
    #         - True - ignore received UDS packets and do not raise InterruptedError
    #         - False - raise InterruptedError if UDS packet is received when awaiting
    #
    #     :raise TypeError: Timeout value is not int or float type.
    #     :raise ValueError: Timeout value is less or equal 0.
    #     :raise TimeoutError: Timeout was reached.
    #     :raise InterruptedError: UDS packet was received during awaiting.
    #
    #     :return: Record with historic information of a packet that was just transmitted.
    #     """
    #     raise NotImplementedError
    #
    # async def await_message_received(self,
    #                                  timeout: Optional[TimeMilliseconds] = None,  # noqa: F841
    #                                  ignore_interruptions: bool = False) -> UdsMessageRecord:  # noqa: F841
    #     """
    #     Wait until the next UDS message is received.
    #
    #     :param timeout: Maximal time (in milliseconds) to wait.
    #     :param ignore_interruptions: Flag informing whether to stop if meanwhile UDS packet was transmitted.
    #
    #         - True - ignore transmitted UDS packets and do not raise InterruptedError
    #         - False - raise InterruptedError if UDS packet is transmitted when awaiting
    #
    #     :raise TypeError: Timeout value is not int or float type.
    #     :raise ValueError: Timeout value is less or equal 0.
    #     :raise TimeoutError: Timeout was reached.
    #     :raise InterruptedError: UDS packet was transmitted during awaiting.
    #
    #     :return: Record with historic information of a message that was just received.
    #     """
    #     raise NotImplementedError
    #
    # async def await_message_transmitted(self,
    #                                     timeout: Optional[TimeMilliseconds] = None,  # noqa: F841
    #                                     ignore_interruptions: bool = False) -> UdsMessageRecord:  # noqa: F841
    #     """
    #     Wait until the next UDS message is transmitted.
    #
    #     :param timeout: Maximal time (in milliseconds) to wait.
    #     :param ignore_interruptions: Flag informing whether to stop if meanwhile UDS packet was received.
    #
    #         - True - ignore received UDS packets and do not raise InterruptedError
    #         - False - raise InterruptedError if UDS packet is received when awaiting
    #
    #     :raise TypeError: Timeout value is not int or float type.
    #     :raise ValueError: Timeout value is less or equal 0.
    #     :raise TimeoutError: Timeout was reached.
    #     :raise InterruptedError: UDS packet was received during awaiting.
    #
    #     :return: Record with historic information of a message that was just transmitted.
    #     """
    #     raise NotImplementedError
    #
    # def schedule_packet(self, packet: AbstractUdsPacket, delay: Optional[TimeMilliseconds] = None) -> None:  # noqa: F841
    #     """
    #     Schedule UDS packet transmission.
    #
    #     :param packet: A packet to send.
    #     :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
    #         None if the transmission to be scheduled immediately.
    #
    #     :raise TypeError: Delay value is not int or float type.
    #     :raise ValueError: Delay value is less or equal 0.
    #     """
    #     raise NotImplementedError
    #
    # def schedule_message(self, message: UdsMessage, delay: Optional[TimeMilliseconds] = None) -> None:  # noqa: F841
    #     """
    #     Schedule UDS message transmissions.
    #
    #     :param message: A message to send.
    #     :param delay: Value of a delay (in milliseconds) if the transmission to be scheduled in the future.
    #         None if the transmission to be scheduled immediately.
    #
    #     :raise TypeError: Delay value is not int or float type.
    #     :raise ValueError: Delay value is less or equal 0.
    #     """
    #     raise NotImplementedError

    @abstractmethod
    def send_packet(self, packet: AbstractUdsPacket) -> AbstractUdsPacketRecord:
        """
        Transmit UDS packet.

        :param packet: A packet to send.

        :return: Record with historic information about transmitted UDS packet.
        """

    @abstractmethod
    def send_message(self, message: UdsMessage) -> UdsMessageRecord:
        """
        Transmit UDS message.

        :param message: A message to send.

        :return: Record with historic information about transmitted UDS message.
        """

    @abstractmethod
    def receive_packet(self, timeout: Optional[TimeMilliseconds]) -> AbstractUdsPacketRecord:
        """
        Receive UDS packet.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received UDS packet.
        """

    @abstractmethod
    def receive_message(self, timeout: Optional[TimeMilliseconds]) -> UdsMessageRecord:
        """
        Receive UDS message.

        :param timeout: Maximal time (in milliseconds) to wait.

        :raise TimeoutError: Timeout was reached.

        :return: Record with historic information about received UDS message.
        """

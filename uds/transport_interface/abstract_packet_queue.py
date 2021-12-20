"""Abstract definition of UDS Packet queue."""

__all__ = ["AbstractPacketsQueue"]

from typing import NoReturn, Type
from abc import ABC, abstractmethod
from asyncio import Queue

from uds.packet import AbstractUdsPacketContainer


class AbstractPacketsQueue(ABC):
    """Abstract definition of a queue with UDS packets."""

    @abstractmethod
    def __init__(self, packet_type: Type[AbstractUdsPacketContainer]) -> None:
        """
        Create a queue for UDS packets storing.

        :param packet_type: A class of which all UDS packets in the queue shall be objects.
            This parameter is meant to support type restriction for packets objects that are managed by this queue.
            Leave None to use no restriction.

        :raise ValueError: Provided packet_class argument is not a type (class).
        :raise TypeError: Provided packet_class argument is a class that defines UDS Packet type.
        """
        if not isinstance(packet_type, type):
            raise ValueError(f"Provided value is not a type (class). Actual value: {packet_type}")
        if not issubclass(packet_type, AbstractUdsPacketContainer):
            raise TypeError(f"Provided value is not a class that defines UDS Packet type. "
                            f"Actual type: {type(packet_type)}")
        self.__packet_type = packet_type

    def __del__(self) -> NoReturn:
        """Delete the queue safely (make sure there are no hanging tasks)."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Get the number of packets that are currently stored by the queue."""
        return self._async_queue.qsize()

    @property
    @abstractmethod
    def _async_queue(self) -> Queue:
        """Asynchronous queue object behind this abstraction layer."""

    @property
    def packet_type(self) -> Type[AbstractUdsPacketContainer]:
        """Type of UDS packets in the queue."""
        return self.__packet_type

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        :return: True if queue is empty (does not contain any packets), False otherwise.
        """
        return len(self) == 0

    def mark_task_done(self) -> None:
        """
        Inform that a task related to one queue's packet was completed.

        This method is used for monitoring tasks, so they can be completed safely and closed quietly.
        """
        self._async_queue.task_done()

    def block(self) -> None:
        """Block from putting new packets to the queue until all packets are gotten and processed."""
        raise NotImplementedError

    def clear(self) -> None:
        """Delete all packets stored by the queue."""
        raise NotImplementedError

    @abstractmethod
    async def get_packet(self) -> AbstractUdsPacketContainer:
        """
        Get the next packet from the queue.

        :return: The next packet in the queue.
        """

    @abstractmethod
    def put_packet(self, packet: AbstractUdsPacketContainer) -> None:
        """
        Add a packet to the queue.

        :param packet: A packet to add to the queue.
        """

"""Abstract definition of UDS Packet queue."""

__all__ = ["AbstractPacketsQueue"]

from typing import NoReturn, Optional
from abc import ABC, abstractmethod

from uds.packet import AbstractUdsPacketContainer


class AbstractPacketsQueue(ABC):
    """Abstract definition of a queue with UDS packets."""

    @abstractmethod
    def __init__(self, packet_class: Optional[type] = None) -> None:  # noqa: F841
        """
        Create a queue for UDS packets storing.

        :param packet_class: A class of which all UDS packets in the queue shall be objects.
            This parameter is meant to support type restriction for packets objects that are managed by this queue.
            Leave None to use no restriction.

        :raise TypeError: Provided packet_class argument is not None neither equal to a proper UDS Packet class.
        """

    def __del__(self) -> NoReturn:
        """Delete the queue safely (make sure there are no hanging tasks)."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Get the number of packets that are currently stored by the queue."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        :return: True if queue is empty (does not contain any packets), False otherwise.
        """
        raise NotImplementedError

    def mark_task_done(self) -> None:
        """
        Inform that a task related to one queue's packet was completed.

        This method is used for monitoring tasks, so they can be completed safely and closed quietly.
        """
        raise NotImplementedError

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
    async def put_packet(self, packet: AbstractUdsPacketContainer) -> None:
        """
        Add a packet to the queue.

        :param packet: A packet to add to the queue.
        """

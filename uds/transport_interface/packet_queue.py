"""Implementation of UDS Packets queues."""

__all__ = ["PacketsQueue", "TimestampedPacketsQueue"]

from typing import NoReturn, Optional
from abc import ABC, abstractmethod
from queue import Queue

from uds.utilities import TimeStamp
from uds.packet import PacketAlias


class AbstractPacketsQueue(ABC):
    """Abstract definition of a queue with UDS packets."""

    @abstractmethod
    def __init__(self, packet_class: type) -> None:  # noqa: F841
        """
        Create a queue for storing UDS packets.

        :param packet_class: A class that defines UDS packets type that is accepted by this queue.
            One can use this parameter to restrict packets managed by this queue.

        :raise TypeError: Provided packet_class argument is not a class that inherits after
            :class:"~uds.packet.abstract_packet.AbstractUdsPacket" or
            :class:"~uds.packet.abstract_packet.AbstractUdsPacketRecord".
        """
        raise NotImplementedError

    def __del__(self) -> NoReturn:
        """
        Delete the queue safely.

        To satisfy safe closure of tasks using the queue:
         - prevent new tasks creations
         - await (till timeout) for closure of already started tasks
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Get number of packets that are currently stored by the queue."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        :return: True if queue is empty (does not contain any packets), False otherwise.
        """
        raise NotImplementedError

    def one_task_done(self) -> None:
        """
        Inform that a task related to one packet was completed.

        This method is used for monitoring tasks so they can be completed safely and closed quietly.
        """
        raise NotImplementedError

    def block(self) -> None:
        """Block from putting new packets to the queue until all packets are gotten and processed."""
        raise NotImplementedError

    def clear(self) -> None:
        """Delete all packets stored by the queue."""
        raise NotImplementedError

    @abstractmethod
    async def get_packet(self) -> PacketAlias:
        """
        Get the next received packet from the queue.

        Note: If called, when there are no packets in the queue, then execution would await until another packet
            is received.

        :return: The next received packet.
        """

    @abstractmethod
    async def put_packet(self, packet: PacketAlias) -> None:
        """
        Add a packet (that was just received) to the end of the queue.

        :param packet: A packet that was just received.
        """

    @property  # noqa: F841
    @abstractmethod
    def _queue_object(self) -> Queue:
        """Primitive queue object that is wrapped."""


class TimestampedPacketsQueue:
    """Priority queue with UDS packets ordered by packet's timestamp."""

    def __init__(self, packet_class: type) -> None:  # noqa: F841
        """
        Create a queue for storing UDS packets ordered by time stamp assigned to each packet.

        :param packet_class: A class that defines UDS packets type that is accepted by this queue.
            One can use this parameter to restrict packets managed by this queue.
        """
        raise NotImplementedError

    async def get_packet(self) -> PacketAlias:
        """
        Get the next received packet from the queue.

        Note: If called, when there are no packets in the queue, then execution would await until another packet
            is received.

        :return: The next received packet.
        """
        raise NotImplementedError

    async def put_packet(self, packet: PacketAlias, timestamp: Optional[TimeStamp] = None) -> None:  # noqa: F841
        """
        Add a packet (that was just received) to the end of the queue.

        :param packet: A packet that was just received.
        :param timestamp:
        """
        raise NotImplementedError


class PacketsQueue:
    """FIFO queue for UDS packets."""

    def __init__(self, packet_class: type) -> None:  # noqa: F841
        """
        Create a queue for storing UDS packets in FIFO order.

        :param packet_class: A class that defines UDS packets type that is accepted by this queue.
            One can use this parameter to restrict packets managed by this queue.
        """
        raise NotImplementedError

    async def get_packet(self) -> PacketAlias:
        """
        Get the next received packet from the queue.

        Note: If called, when there are no packets in the queue, then execution would await until another packet
            is received.

        :return: The next received packet.
        """
        raise NotImplementedError

    async def put_packet(self, packet: PacketAlias) -> None:
        """
        Add a packet (that was just received) to the end of the queue.

        :param packet: A packet that was just received.
        """
        raise NotImplementedError

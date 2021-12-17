"""Implementation of UDS Packets queues."""

__all__ = ["PacketsQueue", "TimestampedPacketsQueue"]

from typing import Optional

from uds.utilities import TimeStamp
from uds.packet import PacketAlias
from .abstract_packet_queue import AbstractPacketsQueue


class TimestampedPacketsQueue(AbstractPacketsQueue):
    """Priority queue with UDS packets ordered by packet's timestamp."""

    def __init__(self, packet_class: type) -> None:  # noqa: F841
        """
        Create a queue for storing UDS packets ordered by timestamp.

        .. note:: Packets from the queue become available when the timestamp is achieved.

        :param packet_class: A class of which all UDS packets in the queue shall be objects.
            This parameter is meant to support type restriction for packets objects that are managed by this queue.
            Leave None to use no restriction.
        """
        raise NotImplementedError

    async def get_packet(self) -> PacketAlias:
        """
        Get the next packet from the queue.

        .. note:: If called when there are no packets available in the queue, then the method would await until
            the next packet is ready (timestamp is achieved).

        :return: The next packet in the queue.
        """
        raise NotImplementedError

    async def put_packet(self, packet: PacketAlias, timestamp: Optional[TimeStamp] = None) -> None:  # noqa: F841
        """
        Add a packet to the queue.

        :param packet: A packet to add to the queue.
        :param timestamp: A moment of time that the packet become available in the queue.
        """
        raise NotImplementedError


class PacketsQueue(AbstractPacketsQueue):
    """FIFO queue for UDS packets."""

    def __init__(self, packet_class: type) -> None:  # noqa: F841
        """
        Create a queue for storing UDS packets in FIFO order.

        :param packet_class: A class of which all UDS packets in the queue shall be objects.
            This parameter is meant to support type restriction for packets objects that are managed by this queue.
            Leave None to use no restriction.
        """
        raise NotImplementedError

    async def get_packet(self) -> PacketAlias:
        """
        Get the next packet from the queue.

        :return: The next packet in the queue.
        """
        raise NotImplementedError

    async def put_packet(self, packet: PacketAlias) -> None:
        """
        Add a packet at the end of the queue.

        :param packet: A packet to add to the queue.
        """
        raise NotImplementedError

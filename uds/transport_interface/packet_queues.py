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


class PacketsQueue(AbstractPacketsQueue):
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

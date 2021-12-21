"""Implementation of UDS Packets queues."""

__all__ = ["PacketsQueue", "TimestampedPacketsQueue"]

from typing import Optional, Type
from asyncio import Queue, PriorityQueue, Event, wait, FIRST_COMPLETED

from uds.utilities import TimeStamp
from uds.packet import AbstractUdsPacketContainer
from .abstract_packet_queue import AbstractPacketsQueue


class TimestampedPacketsQueue(AbstractPacketsQueue):
    """Priority queue with UDS packets ordered by packet's timestamp."""

    def __init__(self, packet_type: Type[AbstractUdsPacketContainer]) -> None:
        """
        Create a queue for storing UDS packets ordered by timestamp.

        .. note:: Packets from the queue become available when the timestamp is achieved.

        :param packet_type: A class of which all UDS packets in the queue shall be objects.
            This parameter is meant to support type restriction for packets objects that are managed by this queue.
            Leave None to use no restriction.
        """
        super().__init__(packet_type=packet_type)
        self.__async_queue = PriorityQueue()
        # TODO: add flag whether new packet added - Event

    @property
    def _async_queue(self) -> Queue:
        """Asynchronous queue object behind this abstraction layer."""
        return self.__async_queue

    async def get_packet(self) -> AbstractUdsPacketContainer:
        """
        Get the next packet from the queue.

        .. note:: If called when there are no packets available in the queue, then the method would await until
            the next packet is ready (timestamp is achieved).

        :return: The next packet in the queue.
        """
        # TODO: use asyncio.wait to wait for the FIRST_COMPLETED, either:
        #  - the lowest timestamp of a packet (in the queue) achieved (asyncio.sleep timestamp-datetime.now())
        #  - a new packet was added to the queue
        raise NotImplementedError

    def put_packet(self, packet: AbstractUdsPacketContainer, timestamp: Optional[TimeStamp] = None) -> None:  # TODO: resolve incompatibility
        """
        Add a packet to the queue.

        :param packet: A packet to add to the queue.
        :param timestamp: A moment of time that the packet become available in the queue.

        :raise TypeError: Provided packet has unsupported type (inconsistent with packet_type attribute).
        """
        raise NotImplementedError


class PacketsQueue(AbstractPacketsQueue):
    """FIFO queue for UDS packets."""

    def __init__(self, packet_type: Type[AbstractUdsPacketContainer]) -> None:
        """
        Create a queue for storing UDS packets in FIFO order.

        :param packet_type: A class of which all UDS packets in the queue shall be objects.
            This parameter is meant to support type restriction for packets objects that are managed by this queue.
            Leave None to use no restriction.
        """
        super().__init__(packet_type=packet_type)
        self.__async_queue = Queue()

    @property
    def _async_queue(self) -> Queue:
        """Asynchronous queue object behind this abstraction layer."""
        return self.__async_queue

    async def get_packet(self) -> AbstractUdsPacketContainer:
        """
        Get the next packet from the queue.

        :return: The next packet in the queue.
        """
        return await self._async_queue.get()

    def put_packet(self, packet: AbstractUdsPacketContainer) -> None:
        """
        Add a packet at the end of the queue.

        :param packet: A packet to add to the queue.

        :raise TypeError: Provided packet has unsupported type (inconsistent with packet_type attribute).
        """
        if not isinstance(packet, self.packet_type):
            raise TypeError(f"Provided packet value is not proper UDS Packet Type.  Expected type: {self.packet_type}. "
                            f"Actual type: {type(packet)}.")
        # TODO: check if blocked
        self._async_queue.put_nowait(packet)

"""Implementation of UDS Packets queues."""

__all__ = ["PacketsQueue", "TimestampedPacketsQueue"]

from typing import Optional, Type, Set
from asyncio import Queue, PriorityQueue, Event, wait, FIRST_COMPLETED
from time import perf_counter

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
        self.__async_queue: PriorityQueue = PriorityQueue()
        self.__event_packet_added: Event = Event()
        self.__event_timestamp_achieved: Event = Event()
        # TODO: add container for timestamps
        # TODO: add task / async method that waits for the timestamp and set the flag

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
        # TODO: __event_packet_added cleared
        # use asyncio.wait to wait for the FIRST_COMPLETED, either __event_packet_added or __event_timestamp_achieved
        # if __event_timestamp_achieved -> return packet
        # if __event_packet_added -> run
        raise NotImplementedError

    def put_packet(self, packet: AbstractUdsPacketContainer, timestamp: Optional[float] = None) -> None:
        """
        Add a packet to the queue.

        :param packet: A packet to add to the queue.
        :param timestamp: Timestamp value (from perf_counter) when make the packet available (gettable) in the queue.

        :raise TypeError: Provided timestamp value has unexpected type.
        """
        if timestamp is None:
            timestamp = perf_counter()
        elif not isinstance(timestamp, float):
            raise TypeError(f"Provided value of timestamp is not float (perf_counter) value. "
                            f"Actual type: {type(timestamp)}")
        super().put_packet(packet=packet)
        self._async_queue.put_nowait((timestamp, packet))
        # TODO: __event_packet_added set


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
        self.__async_queue: Queue = Queue()

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
        """
        super().put_packet(packet=packet)
        self._async_queue.put_nowait(packet)

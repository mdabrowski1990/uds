"""Implementation of UDS Packets queues."""

__all__ = ["PacketsQueue", "TimestampedPacketsQueue"]

from typing import Optional, Type, Set
from asyncio import Queue, PriorityQueue, Event, wait_for
from asyncio import TimeoutError as AsyncioTimeoutError
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
        self.__timestamps: Set[float] = set()

    @property
    def _async_queue(self) -> Queue:
        """Asynchronous queue object behind this abstraction layer."""
        return self.__async_queue

    async def __await_lowest_timestamp(self) -> float:
        """
        Await until the next packet's timestamp is achieved.

        :return: The lowest timestamp of a packet that was just awaited.
        """
        min_timestamp = min(self.__timestamps) if self.__timestamps else float("inf")
        current_time = perf_counter()
        while current_time < min_timestamp:
            self.__event_packet_added.clear()
            try:
                await wait_for(fut=self.__event_packet_added.wait(), timeout=min_timestamp - current_time)
            except AsyncioTimeoutError:
                return min_timestamp
            else:
                current_time = perf_counter()
                min_timestamp = min(self.__timestamps)
        return min_timestamp

    async def get_packet(self) -> AbstractUdsPacketContainer:
        """
        Get the next packet from the queue.

        .. note:: If called when there are no packets available in the queue, then the method would await until
            the next packet is ready (timestamp is achieved).

        :raise RuntimeError: Internal problem with TimestampedPacketsQueue implementation.

        :return: The next packet in the queue.
        """
        min_timestamp = await self.__await_lowest_timestamp()
        packet_timestamp, packet = self._async_queue.get_nowait()
        if min_timestamp != packet_timestamp:
            raise RuntimeError("Something went wrong - packet_timestamp does not match the lowest timestamp.")
        self.__timestamps.remove(packet_timestamp)
        return packet

    def put_packet(self, packet: AbstractUdsPacketContainer, timestamp: Optional[float] = None) -> None:  # noqa
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
        self.__timestamps.add(timestamp)
        self.__event_packet_added.set()


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

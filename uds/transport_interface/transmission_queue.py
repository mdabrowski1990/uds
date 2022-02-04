"""Implementation of a queue with PDUs to transmit."""

__all__ = ["TransmissionQueue"]

from typing import Union, Optional, Type, Set
from warnings import warn
from time import perf_counter
from asyncio import PriorityQueue, Event, QueueEmpty, wait_for
from asyncio import TimeoutError as AsyncioTimeoutError

from uds.message import UdsMessage
from uds.packet import AbstractUdsPacket


class TransmissionQueue:
    """Queue with PDUs to transmit."""

    PDUTypeAlias = Union[Type[UdsMessage], Type[AbstractUdsPacket]]
    """Alias of a PDU type that is accepted by this Queue."""
    PDUAlias = Union[UdsMessage, AbstractUdsPacket]
    """Alias of a PDU (either a message or a packet) stored by this Queue."""

    def __init__(self, pdu_type: PDUTypeAlias) -> None:
        """
        Create timestamped queue with PDUs to transmit.

        :param pdu_type: Type of PDUs to store.

        :raise TypeError: Provided value has unsupported type.
        """
        if not issubclass(pdu_type, (UdsMessage, AbstractUdsPacket)):
            raise TypeError("Provided 'pdu_type' value does not store supported UDS message or packet class.")
        self.__pdu_type = pdu_type
        self.__async_queue: PriorityQueue = PriorityQueue()
        self.__event_pdu_added: Event = Event()
        self.__timestamps: Set[float] = set()

    def __len__(self) -> int:
        """Get number of elements that are currently stored."""
        return self.__async_queue.qsize()

    async def __pdu_ready(self) -> float:
        """
        Await until the next PDU's timestamp is achieved.

        :return: The lowest timestamp of a PDU that is ready for transmission.
        """
        min_timestamp = min(self.__timestamps) if self.__timestamps else float("inf")
        current_time = perf_counter()
        while current_time < min_timestamp:
            self.__event_pdu_added.clear()
            try:
                await wait_for(fut=self.__event_pdu_added.wait(), timeout=min_timestamp - current_time)
            except AsyncioTimeoutError:
                return min_timestamp
            else:
                current_time = perf_counter()
                min_timestamp = min(self.__timestamps)
        return min_timestamp

    @property
    def pdu_type(self) -> PDUTypeAlias:
        """Type of PDUs stored by this queue."""
        return self.__pdu_type

    @property  # noqa: F841
    def is_empty(self) -> bool:
        """Flag whether the queue is empty (does not contain any PDUs)."""
        return self.__len__() == 0

    def mark_pdu_sent(self) -> None:
        """
        Inform that one PDU transmission was completed or aborted.

        This method is used for monitoring PDU transmission tasks, so they can be completed safely and closed quietly.
        """
        self.__async_queue.task_done()

    def clear(self) -> None:
        """Delete all PDUs stored by the queue."""
        for _ in range(self.__len__()):
            try:
                self.__async_queue.get_nowait()
            except QueueEmpty:
                warn(message=f"At least one packet was gotten from {self} queue during the clearing.",
                     category=RuntimeWarning)
                break
            else:
                self.mark_pdu_sent()

    async def get_pdu(self) -> PDUAlias:  # pylint: disable=undefined-variable
        """
        Get the next PDU from the queue.

        .. note:: If called when there are no packets available in the queue, then the method would await until
            the next packet is ready (timestamp is achieved).

        :raise RuntimeError: Internal implementation problem occurred.

        :return: The next PDU from the queue.
        """
        min_timestamp = await self.__pdu_ready()
        packet_timestamp, pdu = self.__async_queue.get_nowait()
        if min_timestamp != packet_timestamp:
            raise RuntimeError("Something went wrong - packet_timestamp does not match the lowest timestamp.")
        self.__timestamps.remove(packet_timestamp)
        return pdu

    def put_pdu(self, pdu: PDUAlias, timestamp: Optional[float] = None) -> None:
        """
        Add a PDU to the queue.

        :param pdu: A PDU to add to the queue.
        :param timestamp: Timestamp value (from perf_counter) when make the packet available (gettable) in the queue.

        :raise TypeError: Provided PDU or timestamp value has unexpected type.
        """
        if not isinstance(pdu, self.pdu_type):
            raise TypeError("Provided PDU value has unexpected type.")
        if timestamp is None:
            timestamp = perf_counter()
        elif not isinstance(timestamp, float):
            raise TypeError("Provided timestamp value is not float (perf_counter) value.")
        self.__async_queue.put_nowait((timestamp, pdu))
        self.__timestamps.add(timestamp)
        self.__event_pdu_added.set()

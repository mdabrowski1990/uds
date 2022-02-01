"""Implementation of a queue with PDUs to transmit."""

__all__ = ["TransmissionQueue"]

from typing import Union, Optional, Type

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
        Created timestamped queue with PDUs to transmit.

        :param pdu_type: Type of PDUs to store.
        """

    def __len__(self) -> int:
        """Number of elements currently contained."""

    @property
    def pdu_type(self) -> PDUTypeAlias:
        """Type of PDUs stored by this queue."""

    @property
    def is_empty(self) -> bool:
        """Flag whether the queue is empty (does not contain any PDUs)."""

    def mark_pdu_sent(self):
        """
        Inform that one PDU transmission was completed or aborted.

        This method is used for monitoring PDU transmission tasks, so they can be completed safely and closed quietly.
        """

    def clear(self) -> None:
        """Delete all PDUs stored by the queue."""

    async def get_pdu(self) -> PDUAlias:
        """
        Get the next PDU from the queue.

        .. note:: If called when there are no packets available in the queue, then the method would await until
            the next packet is ready (timestamp is achieved).

        :raise RuntimeError: Internal implementation problem occurred.

        :return: The next PDU from the queue.
        """

    def put_pdu(self, pdu: PDUAlias, timestamp: Optional[float] = None) -> None:
        """
        Add a PDU to the queue.

        :param pdu: A PDU to add to the queue.
        :param timestamp: Timestamp value (from perf_counter) when make the packet available (gettable) in the queue.

        :raise TypeError: Provided PDU or timestamp value has unexpected type.
        """
    
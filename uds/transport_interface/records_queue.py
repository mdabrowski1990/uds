"""Implementation of queues with historic records."""

__all__ = ["RecordsQueue"]

from typing import Union, Type, Tuple

from uds.message import UdsMessageRecord
from uds.packet import AbstractUdsPacket


class RecordsQueue:
    """Queue with historic records of UDS Packets or Messages."""

    RecordsTypeAlias = Union[Type[UdsMessageRecord], Type[AbstractUdsPacket]]
    """Alias of a record type that is accepted by this Queue."""
    RecordAlias = Union[UdsMessageRecord, AbstractUdsPacket]
    """Alias of a record stored by this Queue."""

    def __init__(self, records_type: RecordsTypeAlias, history_size: int) -> None:
        """
        Create FIFO queue with historic records of UDS Packets or Messages.

        :param records_type: Type of records to store.
        :param history_size: Number of records to store.
        """

    @property
    def records_type(self) -> RecordsTypeAlias:
        """Type of records stored by this queue."""

    @property
    def history_size(self) -> int:
        """
        Number of records stored by this queue.

        .. note:: If a record beyond this number is received, then the oldest one is pushed out of the queue.
        """

    @property
    def total_records_number(self) -> int:
        """Total number of records that went through the queue."""

    @property
    def records_history(self) -> Tuple[RecordAlias, ...]:
        """Historic records from the youngest to the oldest."""

    def put_record(self, record: RecordAlias) -> None:
        """
        Add a new record to the queue.

        :param record: A new record to add.

        :raise TypeError: Provided record value has unexpected type.
        """

    async def get_next_record(self) -> RecordAlias:
        """
        Get the next record to enter the queue.

        :return: The next record that was put to the queue.
        """

    def clear_records_history(self) -> None:
        """Clear all stored records."""

"""Implementation of queues with historic records."""

__all__ = ["RecordsQueue"]

from typing import Union, Type, Tuple
from asyncio import Event

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

        :raise TypeError: Provided value has unsupported type.
        :raise ValueError: Provided value is out of range.
        """
        if not issubclass(records_type, (UdsMessageRecord, AbstractUdsPacket)):
            raise TypeError("Provided 'records_type' value does not store supported record class.")
        if not isinstance(history_size, int):
            raise TypeError("Provided 'history_size' value is not int type.")
        if history_size < 0:
            raise ValueError("Provided value of 'history_size' is lower than 0.")
        self.__records_type = records_type
        self.__history_size: int = history_size
        self.__total_records_number: int = 0
        self.__records_history = []
        self.__event_new_record = Event()

    @property
    def records_type(self) -> RecordsTypeAlias:
        """Type of records stored by this queue."""
        return self.__records_type

    @property
    def history_size(self) -> int:
        """
        Number of records stored by this queue.

        .. note:: If a record beyond this number is received, then the oldest one is pushed out of the queue.
        """
        return self.__history_size

    @property
    def total_records_number(self) -> int:
        """Total number of records that went through the queue."""
        return self.__total_records_number

    @property
    def records_history(self) -> Tuple[RecordAlias, ...]:
        """Historic records from the youngest to the oldest."""
        return tuple(self.__records_history)

    def clear_records_history(self) -> None:
        """Clear all stored records."""
        self.__records_history = []
        self.__total_records_number = 0

    def put_record(self, record: RecordAlias) -> None:
        """
        Add a new record to the queue.

        :param record: A new record to add.

        :raise TypeError: Provided record value has unexpected type.
        """
        if not isinstance(record, self.records_type):
            raise TypeError("Provided value has unexpected type.")
        self.__records_history.insert(0, record)
        self.__records_history = self.__records_history[:self.history_size]
        self.__total_records_number += 1
        self.__event_new_record.set()

    async def get_next_record(self) -> RecordAlias:
        """
        Get the next record to enter the queue.

        :return: The next record that was put to the queue.
        """
        self.__event_new_record.clear()
        await self.__event_new_record.wait()
        return self.records_history[0]

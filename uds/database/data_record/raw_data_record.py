from typing import Optional, Tuple

from .abstract_data_record import AbstractDataRecord, DataRecordType


class RawDataRecord(AbstractDataRecord):
    """Common implementation and interface for Raw Data Record."""

    def __init__(self, name: str, length: int) -> None:
        """
        Initialization of Raw Data Record.

        :param name: Name to assign to this Data Record.
        :param length: Number of bits that this Raw Data Record is stored over.

        :raise TypeError: Provided name is not str type.
        :raise ValueError: Provided length is not a positive integer.
        """
        super().__init__(name)
        if not isinstance(length, int) or length <= 0:
            raise ValueError("Length must be a positive integer.")
        self.__length = length

    @property
    def data_record_type(self) -> DataRecordType:
        """Type of this Data Record."""
        return DataRecordType.RAW

    @property
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        return self.__length

    @property
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """
        return False

    @property
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.data_record.raw_data_record.RawDataRecord.is_reoccurring`
            equals True.
        """
        return 1

    @property
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.data_record.raw_data_record.RawDataRecord.is_reoccurring`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        return 1

    @property
    def contains(self) -> Tuple[AbstractDataRecord, ...]:
        """Get Data Records contained by this Data Record."""
        return ()

    def decode(self, raw_value: int) -> int:
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        return raw_value

    def encode(self, physical_value: int) -> int:
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        return physical_value
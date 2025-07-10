"""Definition of RawDataRecord."""

__all__ = ["RawDataRecord"]

from typing import Optional, Tuple

from .abstract_data_record import AbstractDataRecord, DataRecordPhysicalValueAlias, DecodedDataRecord


class RawDataRecord(AbstractDataRecord):
    """Implementation and interface for Raw Data Record."""

    def __init__(self, name: str, length: int) -> None:
        """
        Initialize Raw Data Record.

        :param name: Name to assign to this Data Record.
        :param length: Number of bits that this Raw Data Record is stored over.

        :raise TypeError: Provided name is not str type.
        :raise ValueError: Provided length is not a positive integer.
        """
        super().__init__(name)
        self.length = length

    @property
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        return self.__length

    @length.setter
    def length(self, value: int) -> None:
        """
        Set the length, ensuring it's an integer and within an acceptable range.

        :param value: Number of bits that this Data Record is stored over.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, int):
            raise TypeError("Length must be an integer.")
        if value <= 0:
            raise ValueError("Length must be a positive integer.")
        self.__length = value

    @property  # noqa
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """
        return False

    @property  # noqa
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.data_record.raw_data_record.RawDataRecord.is_reoccurring`
            equals True.
        """
        return 1

    @property  # noqa
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.data_record.raw_data_record.RawDataRecord.is_reoccurring`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        return 1

    @property  # noqa
    def contains(self) -> Tuple[AbstractDataRecord, ...]:
        """Get Data Records contained by this Data Record."""
        return ()

    def decode(self, raw_value: int) -> DecodedDataRecord:
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.

        :raises TypeError: Provided `raw_value` is not int type.
        :raises ValueError: Provided `raw_value` is out of range (0 <= raw_value <= max_raw_value).
        """
        if not isinstance(raw_value, int):
            raise TypeError(f"Expected raw_value to be an int type, got '{type(raw_value).__name__}' instead.")

        if not 0 <= raw_value <= self.max_raw_value:
            raise ValueError(
                "Provided value of raw_value is out of range: "
                f"must be between 0 and {self.max_raw_value}, got {raw_value}."
            )
        return DecodedDataRecord(name=self.name, raw_value=raw_value, physical_value=raw_value)

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        if not isinstance(physical_value, int):
            raise TypeError(
                f"Expected physical_value to be an int type, got '{type(physical_value).__name__}' instead."
            )

        if not 0 <= physical_value <= self.max_raw_value:
            raise ValueError(
                "Provided value of physical_value is out of range: "
                f"must be between 0 and {self.max_raw_value}, got {physical_value}."
            )
        return physical_value

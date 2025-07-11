"""Definition of RawDataRecord."""

__all__ = ["RawDataRecord"]

from typing import Optional, Sequence

from .abstract_data_record import AbstractDataRecord, PhysicalValueAlias


class RawDataRecord(AbstractDataRecord):
    """Implementation and interface for Raw Data Record."""

    def __init__(self,
                 name: str,
                 length: int,
                 children: Sequence[AbstractDataRecord] = tuple(),
                 min_occurrences: int=1) -> None:
        """
        Initialize Raw Data Record.

        :param name: Name to assign to this Data Record.
        :param length: Number of bits that this Raw Data Record is stored over.

        :raise TypeError: Provided name is not str type.
        :raise ValueError: Provided length is not a positive integer.
        """
        super().__init__(name=name, length=length, children=children)

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

    def get_physical_value(self, raw_value: int) -> PhysicalValueAlias:
        """
        Decode raw value and provide physical value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Decoded physical value for this occurrence. For
        """
        super().get_physical_value(raw_value)
        return raw_value

    def get_raw_value(self, physical_value: PhysicalValueAlias) -> int:
        """
        Encode physical value into raw value.

        :param physical_value: Physical (meaningful e.g. vehicle speed in km/h) value of this Data Record
            single occurrence.

        :return: Raw Value of this Data Record occurrence.
        """
        raw_value = physical_value
        self._validate_raw_value(raw_value)
        return raw_value

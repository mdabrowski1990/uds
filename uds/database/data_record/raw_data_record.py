"""Definition of RawDataRecord."""

__all__ = ["RawDataRecord"]

from typing import Optional, Sequence

from .abstract_data_record import AbstractDataRecord, PhysicalValueAlias


class RawDataRecord(AbstractDataRecord):
    """Raw Data Record for storing integers without any convertion to physical values."""

    def __init__(self,
                 name: str,
                 length: int,
                 children: Sequence[AbstractDataRecord] = tuple(),
                 min_occurrences: int=1,
                 max_occurrences: Optional[int]=1) -> None:
        """
        Initialize Raw Data Record.

        :param name: Name to assign to this Data Record.
        :param length: Number of bits that are used to store a single occurrence of Data Record.
        :param children: Data Records contained by this one with detailed information.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        """
        super().__init__(name=name,
                         length=length,
                         children=children,
                         min_occurrences=min_occurrences,
                         max_occurrences=max_occurrences)

    def get_physical_value(self, raw_value: int) -> PhysicalValueAlias:
        """
        Decode raw value and provide physical value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Decoded physical value for this occurrence.
            For Raw Data Record the raw and physical values are the same.
        """
        self._validate_raw_value(raw_value)
        return raw_value

    def get_raw_value(self, physical_value: PhysicalValueAlias) -> int:
        """
        Encode physical value into raw value.

        :param physical_value: Physical value of this Data Record single occurrence.

        :return: Raw Value of this Data Record occurrence.
            For Raw Data Record the raw and physical values are the same.
        """
        raw_value = physical_value
        self._validate_raw_value(raw_value)
        return raw_value

"""Raw Data Records implementation."""

__all__ = ["RawDataRecord"]

from collections.abc import Sequence
from copy import deepcopy
from typing import Any

from .abstract_data_record import AbstractDataRecord


class RawDataRecord(AbstractDataRecord):
    """
    Implementation for Raw Data Records.

    Raw Data Records are the most basic Data Records which do not contain translation between physical and raw values.

    Common Use Cases:
     - Fillers without any meaning (e.g. reserved values)
     - Entries with unknown meaning
     - Data containers (e.g. DID structures) with multiple children
    """

    def __init__(self,
                 name: str,
                 length: int,
                 children: Sequence[AbstractDataRecord] = tuple(),
                 min_occurrences: int = 1,
                 max_occurrences: int | None = 1,
                 unit: str | None = None,
                 enforce_reoccurring: bool = False) -> None:
        """
        Create Raw Data Record.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param children: Contained Data Records.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        :param unit: Unit in which a physical value is represented.
        :param enforce_reoccurring: Decide whether to enforce this DataRecord to be treated as re-occurring.
        """
        super().__init__(name=name,
                         length=length,
                         unit=unit,
                         children=children,
                         min_occurrences=min_occurrences,
                         max_occurrences=max_occurrences,
                         enforce_reoccurring=enforce_reoccurring)

    def __deepcopy__(self, memo: dict[int, Any]) -> "RawDataRecord":
        """Get deep copy of this Data Record."""
        cls = self.__class__
        self_copy = cls.__new__(cls)
        memo[id(self)] = self_copy
        RawDataRecord.__init__(self_copy,
                               name=self.name,
                               length=self.length,
                               children=deepcopy(self.children, memo=memo),
                               min_occurrences=self.min_occurrences,
                               max_occurrences=self.max_occurrences,
                               unit=self.unit,
                               enforce_reoccurring=self.enforce_reoccurring)
        memo[id(self)] = self_copy
        return self_copy

    def get_physical_value(self, raw_value: int) -> int:
        """
        Decode raw value and provide physical value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Decoded physical value for this occurrence.
            For Raw Data Record the raw and physical values are the same.
        """
        self._validate_raw_value(raw_value)
        return raw_value

    def get_raw_value(self, physical_value: int) -> int:  # type: ignore
        """
        Encode physical value into raw value.

        :param physical_value: Physical value of this Data Record single occurrence.

        :return: Raw Value for this occurrence.
            For Raw Data Record the raw and physical values are the same.
        """
        raw_value = physical_value
        self._validate_raw_value(raw_value)
        return raw_value

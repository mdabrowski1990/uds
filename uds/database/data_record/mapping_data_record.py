"""Mapping Data Record implementation."""

__all__ = ["MappingDataRecord"]

from types import MappingProxyType
from typing import Dict, Optional, Sequence
from warnings import warn

from uds.utilities import ValueWarning

from .abstract_data_record import AbstractDataRecord, SinglePhysicalValueAlias
from .raw_data_record import RawDataRecord


class MappingDataRecord(RawDataRecord):
    """
    Data Record with mapping between raw values and human-readable labels.

    MappingDataRecord provides translation between raw integer values and  meaningful labels, ideal for status fields,
    enumerations, and boolean flags. Inherits from RawDataRecord to provide fallback behavior when no mapping exists.

    Features:
     - Bidirectional mapping: raw <-> label translation
     - Fallback behavior: unmapped values return raw integers with warning
     - Container support: Can have children (e.g. for complex bit-field structures)
     - Occurrence constraints: Support for multiple occurrences (e.g. status for multiple sensors)

    Common Use Cases:
     - Status indicators (0="Inactive", 1="Active")
     - Boolean flags (0="No", 1="Yes")
     - Enumerated values (0="Low", 1="Medium", 2="High")
     - Complex bit-fields with individual bit meanings
    """

    def __init__(self,
                 name: str,
                 length: int,
                 values_mapping: Dict[int, str],
                 children: Sequence[AbstractDataRecord] = tuple(),
                 min_occurrences: int = 1,
                 max_occurrences: Optional[int] = 1) -> None:
        """
        Create Mapping Data Record.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param values_mapping: Mapping of raw values to labels with their meaning.
            Dict keys are raw_values. Dict values are corresponding labels.
        :param children: Contained Data Records.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        """
        super().__init__(name=name,
                         length=length,
                         children=children,
                         min_occurrences=min_occurrences,
                         max_occurrences=max_occurrences)
        self.values_mapping = values_mapping

    @property
    def values_mapping(self) -> MappingProxyType[int, str]:
        """Get raw values mapping to their corresponding labels."""
        return self.__values_mapping

    @values_mapping.setter
    def values_mapping(self, value: Dict[int, str]) -> None:
        """
        Set the mapping between raw values and their labels.

        :param value: Mapping to set.

        :raise TypeError: Provided value is not dict type.
        :raise ValueError: At least one key is out of raw values range.
        """
        if not isinstance(value, dict):
            raise TypeError("Provided value is not dict type.")
        if not all(isinstance(key, int) and self.min_raw_value <= key <= self.max_raw_value for key in value.keys()):
            raise ValueError("Provided dict contain values that are out of raw values range.")
        self.__values_mapping = MappingProxyType(value)
        self.__labels_mapping = MappingProxyType({v: k for k, v in self.__values_mapping.items()})

    @property
    def labels_mapping(self) -> MappingProxyType[str, int]:
        """Get labels mapping to raw values."""
        return self.__labels_mapping

    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Get physical value representing provided raw value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: A label value for this occurrence.
        """
        if raw_value in self.values_mapping:
            return self.values_mapping[raw_value]
        warn(message=f"No label defined for raw value {raw_value} in mapping",
             category=ValueWarning,
             stacklevel=2)
        return super().get_physical_value(raw_value)

    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        """
        Get raw value that represents provided physical value.

        :param physical_value: Physical value (a label) of this Data Record single occurrence.

        :return: Raw Value for this occurrence.
        """
        if physical_value in self.labels_mapping:
            return self.labels_mapping[physical_value]  # type: ignore
        return super().get_raw_value(physical_value)

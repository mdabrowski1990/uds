"""Mapping Data Record implementation."""

__all__ = ["MappingDataRecord", "MappingAndLinearFormulaDataRecord"]

from abc import ABC, abstractmethod
from collections.abc import Sequence
from copy import deepcopy
from types import MappingProxyType
from typing import Any, Mapping
from warnings import warn

from uds.utilities import ValueWarning

from .abstract_data_record import AbstractDataRecord
from .formula_data_record import LinearFormulaDataRecord
from .raw_data_record import RawDataRecord


class AbstractMappingDataRecord(ABC):
    """Mapping functionality for Data Records."""

    def __init__(self, values_mapping: Mapping[int, str]) -> None:
        """
        Define mapping to use by this Data Record.

        :param values_mapping: Mapping of raw values to labels with their meaning.
            Dict keys are raw_values. Dict values are corresponding labels.
        """
        self.values_mapping = values_mapping

    @property
    def values_mapping(self) -> MappingProxyType[int, str]:
        """Get raw values mapping to their corresponding labels."""
        return self.__values_mapping

    @values_mapping.setter
    def values_mapping(self, value: Mapping[int, str]) -> None:
        """
        Set the mapping between raw values and their labels.

        :param value: Mapping to set.

        :raise TypeError: Provided value is not dict type.
        :raise ValueError: If any mapping key is outside the range of valid raw values,
            or any mapping value is not str type.
        """
        if not isinstance(value, Mapping):
            raise TypeError(f"Provided value is not Mapping. Actual type: {type(value)}.")
        if not all(isinstance(key, int) and self.min_raw_value <= key <= self.max_raw_value for key in value.keys()):
            raise ValueError("Provided values mapping contains values that are out of raw values range. "
                             f"Expected: {self.min_raw_value} <= key <= {self.max_raw_value}. "
                             f"Actual keys: {list(value.keys())}.")
        if not all(isinstance(value, str) for value in value.values()):
            raise ValueError("Provided values mapping contains labels that are not str type. "
                             f"Actual values: {list(value.values())}.")
        self.__values_mapping = MappingProxyType(value)
        self.__labels_mapping = MappingProxyType({v: k for k, v in self.__values_mapping.items()})

    @property
    def labels_mapping(self) -> MappingProxyType[str, int]:
        """Get labels mapping to raw values."""
        return self.__labels_mapping

    @property
    @abstractmethod
    def min_raw_value(self) -> int:
        """Minimum raw (bit) value for this Data Record."""

    @property
    @abstractmethod
    def max_raw_value(self) -> int:
        """Maximum raw (bit) value for this Data Record."""


class MappingDataRecord(RawDataRecord, AbstractMappingDataRecord):
    """
    Data Record with mapping between raw values and human-readable labels.

    MappingDataRecord provides translation between raw integer values and  meaningful labels, ideal for status fields,
    enumerations, and boolean flags. Inherits from RawDataRecord to provide fallback behavior when no mapping exists.

    Features:
     - Bidirectional mapping: raw value <-> label translation
     - Fallback behavior: unmapped values return raw integers with warning
     - Container support: can have children (e.g. for complex bit-field structures)
     - Occurrence constraints: support for multiple occurrences (e.g. status for multiple sensors)

    Common Use Cases:
     - Status indicators (0="Inactive", 1="Active")
     - Boolean flags (0="No", 1="Yes")
     - Enumerated values (0="Low", 1="Medium", 2="High")
     - Complex bit-fields with individual bit meanings
    """

    def __init__(self,
                 name: str,
                 length: int,
                 values_mapping: Mapping[int, str],
                 children: Sequence[AbstractDataRecord] = tuple(),
                 min_occurrences: int = 1,
                 max_occurrences: None | int = 1,
                 unit: None | str = None,
                 enforce_reoccurring: bool = False) -> None:
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
        :param unit: Unit in which values without mapping are represented.
        :param enforce_reoccurring: Decide whether to enforce this DataRecord to be treated as re-occurring.
        """
        RawDataRecord.__init__(self,
                               name=name,
                               length=length,
                               children=children,
                               unit=unit,
                               min_occurrences=min_occurrences,
                               max_occurrences=max_occurrences,
                               enforce_reoccurring=enforce_reoccurring)
        AbstractMappingDataRecord.__init__(self,
                                           values_mapping=values_mapping)

    def __deepcopy__(self, memo: dict[int, Any]) -> MappingDataRecord:
        """Get deep copy of this Data Record."""
        cls = self.__class__
        self_copy = cls.__new__(cls)
        memo[id(self)] = self_copy
        MappingDataRecord.__init__(self_copy,
                                   name=self.name,
                                   length=self.length,
                                   values_mapping=self.values_mapping,
                                   children=deepcopy(self.children, memo=memo),
                                   min_occurrences=self.min_occurrences,
                                   max_occurrences=self.max_occurrences,
                                   unit=self.unit,
                                   enforce_reoccurring=self.enforce_reoccurring)
        return self_copy

    def get_physical_value(self, raw_value: int) -> str | int:  # type: ignore
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

    def get_raw_value(self, physical_value: str | int) -> int:  # type: ignore
        """
        Get raw value that represents provided physical value.

        :param physical_value: Physical value (a label) of this Data Record single occurrence.

        :return: Raw Value for this occurrence.
        """
        if physical_value in self.labels_mapping:
            return self.labels_mapping[physical_value]  # type: ignore
        return super().get_raw_value(physical_value)  # type: ignore


class MappingAndLinearFormulaDataRecord(LinearFormulaDataRecord, AbstractMappingDataRecord):
    """
    Data Record with both mapping (raw value <-> label) and linear transformation capabilities.

    MappingAndLinearFormulaDataRecord extends LinearFormulaDataRecord with a predefined mapping
    between raw integer values and human-readable labels. When a raw value is found in the mapping,
    the corresponding label is returned. Otherwise, the raw value is converted into a physical
    quantity using a linear transformation (factor * raw_value + offset).

    Features:
     - Dual interpretation:
       * Label mapping for discrete or enumerated values
       * Linear transformation for continuous or numeric values
     - Bidirectional conversion: raw <-> label or physical value
     - Unit support for transformed values
     - Occurrence constraints (minimum and maximum number of records)

    Common Use Cases:
     - Mixed parameter fields where some values represent discrete states (e.g. 0="Off", 1="On"),
       and others represent scaled measurements
     - Diagnostic fields that combine enumerations with numeric ranges
     - Complex protocol parameters that can be expressed both categorically and numerically
    """

    def __init__(self,
                 name: str,
                 length: int,
                 values_mapping: Mapping[int, str],
                 factor: float | int,
                 offset: float | int,
                 min_occurrences: int = 1,
                 max_occurrences: None | int = 1,
                 unit: None | str = None,
                 enforce_reoccurring: bool = False) -> None:
        """
        Create Mapping and Linear Formula Data Record.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param values_mapping: Mapping of raw values to labels with their meaning.
            Dict keys are raw_values. Dict values are corresponding labels.
        :param factor: Multiplication factor for the linear transformation.
        :param offset: Additive offset for the linear transformation.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        :param unit: Unit in which values without mapping are represented.
        :param enforce_reoccurring: Decide whether to enforce this DataRecord to be treated as re-occurring.
        """
        LinearFormulaDataRecord.__init__(self,
                                         name=name,
                                         length=length,
                                         factor=factor,
                                         offset=offset,
                                         unit=unit,
                                         min_occurrences=min_occurrences,
                                         max_occurrences=max_occurrences,
                                         enforce_reoccurring=enforce_reoccurring)
        AbstractMappingDataRecord.__init__(self,
                                           values_mapping=values_mapping)

    def __deepcopy__(self, memo: dict[int, Any]) -> MappingAndLinearFormulaDataRecord:
        """Get deep copy of this Data Record."""
        cls = self.__class__
        self_copy = cls.__new__(cls)
        memo[id(self)] = self_copy
        MappingAndLinearFormulaDataRecord.__init__(self_copy,
                                                   name=self.name,
                                                   length=self.length,
                                                   values_mapping=self.values_mapping,
                                                   factor=self.factor,
                                                   offset=self.offset,
                                                   min_occurrences=self.min_occurrences,
                                                   max_occurrences=self.max_occurrences,
                                                   unit=self.unit,
                                                   enforce_reoccurring=self.enforce_reoccurring)
        memo[id(self)] = self_copy
        return self_copy

    def get_physical_value(self, raw_value: int) -> str | int | float:  # type: ignore
        """
        Get physical value representing provided raw value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: A label (from mapping) or a physical (linear transformation) value for this occurrence.
        """
        if raw_value in self.values_mapping:
            return self.values_mapping[raw_value]
        return super().get_physical_value(raw_value)

    def get_raw_value(self, physical_value: str | int | float) -> int:
        """
        Get raw value that represents provided physical value.

        :param physical_value: Physical value (a label) of this Data Record single occurrence.

        :return: Raw Value for this occurrence.
        """
        if physical_value in self.labels_mapping:
            return self.labels_mapping[physical_value]  # type: ignore
        raw_value = super().get_raw_value(physical_value)  # type: ignore
        if raw_value in self.values_mapping:
            warn(message="Numeric physical value was provided for a value with a label: "
                         f"{raw_value} ({self.values_mapping[raw_value]}).",
                 category=UserWarning,
                 stacklevel=2)
        return raw_value

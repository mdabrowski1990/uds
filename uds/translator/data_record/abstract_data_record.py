"""Implementation of Data Records structure and API."""

__all__ = ["AbstractDataRecord",
           "SingleOccurrenceInfo", "MultipleOccurrencesInfo", "DataRecordInfoAlias",
           "SinglePhysicalValueAlias", "MultiplePhysicalValuesAlias", "PhysicalValueAlias",
           "ChildrenValuesAlias"]

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import List, Mapping, Optional, Sequence, Tuple, TypedDict, Union

from uds.utilities import InconsistencyError, ReassignmentError

SinglePhysicalValueAlias = Union[int, float, str]
"""
Physical value from a single Data Record occurrence.

Physical values represent the human-readable interpretation of raw integer values:

- int: Direct numeric values (e.g., 127 for temperature sensor)
- float: Scaled/calculated values (e.g., 25.5°C after scaling)
- str: Mapped labels (e.g., "Active", "Inactive", "Warning")
"""
MultiplePhysicalValuesAlias = Union[str, Tuple[SinglePhysicalValueAlias, ...]]
"""
Physical values from multiple Data Record occurrences.

When processing multiple occurrences, physical values are either:

- str: Concatenated string for all occurrences (e.g. serial number, part number) using predefined encoding
  (e.g. ASCII, UTF-8)
- tuple: Individual values per occurrence
"""
PhysicalValueAlias = Union[SinglePhysicalValueAlias, MultiplePhysicalValuesAlias]
"""Alias for all physical values."""
ChildrenValuesAlias = Mapping[str, Union[int, "ChildrenValuesAlias"]]
"""Alias for children values mapping."""


class SingleOccurrenceInfo(TypedDict, total=True):
    """
    Comprehensive information about a single Data Record occurrence.

    :arg name: Data Record name.
    :arg length: Number of bits used to store this Data Record.
    :arg raw_value: Raw values for this occurrence.
    :arg physical_value: Physical value for this occurrence.
    :arg children: Extracted child information for this occurrence.
    :arg unit: Unit in which physical value is represented.
    """

    name: str
    length: int
    raw_value: int
    physical_value: SinglePhysicalValueAlias
    children: Tuple["SingleOccurrenceInfo", ...]
    unit: Optional[str]


class MultipleOccurrencesInfo(TypedDict, total=True):
    """
    Comprehensive information about multiple Data Record occurrences.

    :arg name: Data Record name.
    :arg length: Number of bits used to store a single occurrence of this Data Record.
    :arg raw_value: List with raw values for each occurrence.
    :arg physical_value: Physical values for multiple occurrences.
    :arg children: List with one element for each occurrence.
        Each element contains information about children for this occurrence.
    :arg unit: Unit in which a single physical value is represented.
    """

    name: str
    length: int
    raw_value: Tuple[int, ...]
    physical_value: MultiplePhysicalValuesAlias
    children: Tuple[Tuple["SingleOccurrenceInfo", ...], ...]
    unit: Optional[str]


DataRecordInfoAlias = Union[SingleOccurrenceInfo, MultipleOccurrencesInfo]
"""Comprehensive information Data Record occurrence(s)."""


class AbstractDataRecord(ABC):
    """
    Abstract base class for all Data Records with container functionality.

    This class implements the container pattern where every Data Record can contain hierarchical children,
    enabling automatic bit-field extraction and complex diagnostic message structures.

    The container design eliminates the need for separate container classes while
    providing powerful features:

    - Automatic bit extraction from parent to children
    - Multiple occurrences support with min/max constraints
    - Immutable properties to prevent accidental modification
    - Comprehensive occurrence information with nested children
    """

    def __init__(self,
                 name: str,
                 length: int,
                 children: Sequence["AbstractDataRecord"],
                 min_occurrences: int,
                 max_occurrences: Optional[int],
                 unit: Optional[str] = None,
                 enforce_reoccurring: bool = False) -> None:
        """
        Initialize common part for all Data Records.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param children: Contained Data Records.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        :param unit: Unit in which a physical value is represented.
        :param enforce_reoccurring: Decide whether to enforce this DataRecord to be treated as re-occurring.
        """
        self.name = name
        self.length = length
        self.children = children
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences
        self.unit = unit
        self.enforce_reoccurring = enforce_reoccurring

    def _validate_raw_value(self, raw_value: int) -> None:
        """
        Validate provided raw value.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is out of range (min_raw_value, max_raw_value).
        """
        if not isinstance(raw_value, int):
            raise TypeError("Provided value is not int type.")
        if not self.min_raw_value <= raw_value <= self.max_raw_value:
            raise ValueError("Provided value is out of range.")

    @property
    def name(self) -> str:
        """Get name of this Data Record."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set name for this Data Record.

        :param value: A name to set.

        :raise TypeError: Provided value is not str type.
        :raise ValueError: Provided value empty.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not isinstance(value, str):
            raise TypeError("Provided name is not str type.")
        stripped_names = value.strip()
        if stripped_names == "":
            raise ValueError("Name must not be empty.")
        if hasattr(self, "_AbstractDataRecord__name"):
            raise ReassignmentError("Value of 'name' attribute cannot be changed once assigned.")
        self.__name = stripped_names

    @property
    def length(self) -> int:
        """Get number of bits that a single occurrence of this Data Record is stored over."""
        return self.__length

    @length.setter
    def length(self, value: int) -> None:
        """
        Set number of bits that a single occurrence of this Data Record is stored over.

        :param value: Number of bits to set.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is not positive integer.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not isinstance(value, int):
            raise TypeError("Length must be an integer.")
        if value <= 0:
            raise ValueError("Length must be a positive value.")
        if hasattr(self, "_AbstractDataRecord__length"):
            raise ReassignmentError("Value of 'length' attribute cannot be changed once assigned.")
        self.__length = value

    @property
    def children(self) -> Tuple["AbstractDataRecord", ...]:
        """Get Data Records contained by this Data Record."""
        return self.__children

    @children.setter
    def children(self, value: Sequence["AbstractDataRecord"]) -> None:
        """
        Set Data Records contained by this Data Record.

        :param value: Sequence with Data Records to be set as children.

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: At least one of the provided elements in the sequence is not a Data Record or is reoccurring.
        :raise InconsistencyError: Provided sequence of Data Records cannot be children for this Data Record.
        """
        if not isinstance(value, Sequence):
            raise TypeError("Provided value is not a sequence.")
        children_length = 0
        children_names = set()
        for child in value:
            if not isinstance(child, AbstractDataRecord):
                raise ValueError("At least one of the values in the sequence is not a Data Record.")
            if child.is_reoccurring:
                raise ValueError("Child Data Record cannot be reoccurring.")
            children_length += child.length
            children_names.add(child.name)
        if children_length not in {self.length, 0}:
            raise InconsistencyError("Total children length does not match the length of this Data Record.")
        if len(children_names) != len(value):
            raise InconsistencyError("Each child has to have unique name.")
        self.__children = tuple(value)

    @property
    def min_occurrences(self) -> int:
        """Minimal number of occurrences for this Data Record."""
        return self.__min_occurrences

    @min_occurrences.setter
    def min_occurrences(self, value: int) -> None:
        """
        Set minimal number of occurrences.

        :param value: Value to set.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is negative number.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not isinstance(value, int):
            raise TypeError("Minimal occurrence number must be an integer.")
        if value < 0:
            raise ValueError("Minimal occurrence number must be a non-negative value.")
        if hasattr(self, "_AbstractDataRecord__min_occurrences"):
            raise ReassignmentError("Value of 'min_occurrences' attribute cannot be changed once assigned.")
        self.__min_occurrences = value

    @property
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of occurrences for this Data Record.

        .. note:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        return self.__max_occurrences

    @max_occurrences.setter
    def max_occurrences(self, value: Optional[int]) -> None:
        """
        Set maximal number of occurrences.

        :param value: Value to set.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Maximal occurrences number must be greater or equal minimal occurrences number.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Maximal occurrence number must be an integer or None.")
            if value < max(self.min_occurrences, 1):
                raise ValueError("Maximal occurrence number must be greater or equal minimal occurrences number.")
        if hasattr(self, "_AbstractDataRecord__max_occurrences"):
            raise ReassignmentError("Value of 'max_occurrences' attribute cannot be changed once assigned.")
        self.__max_occurrences = value

    @property
    def unit(self) -> Optional[str]:
        """Get unit in which Physical Value is presented. None if unused."""
        return self.__unit

    @unit.setter
    def unit(self, value: Optional[str]) -> None:
        """
        Set unit in which Physical Value is presented.

        :param value: Unit value to set.
            Set None if no units are used.

        :raise TypeError: Unit must be provided as str or set to None.
        """
        if value is None:
            self.__unit = None
        elif isinstance(value, str):
            self.__unit = value
        else:
            raise TypeError("Unit value must be a str type or equal None.")

    @property
    def enforce_reoccurring(self) -> bool:
        """
        Get flag enforcing this Data Record is treated as reoccurring.

        Values meaning:

        - True - even if :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.max_occurrences`
            equals 1 enforce
            :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.is_reoccurring` = True.
        - False - let :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.is_reoccurring`
            be assessed based on
            :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.max_occurrences` value
        """
        return self.__enforce_reoccurring

    @enforce_reoccurring.setter
    def enforce_reoccurring(self, value: bool) -> None:
        """Decide whether to enforce this DataRecord to be treated as re-occurring."""
        self.__enforce_reoccurring = bool(value)

    @property
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:

        - True - number of occurrences might vary
        - False - there might be 0 or 1 occurrence of this Data Record
        """
        return True if self.enforce_reoccurring else self.max_occurrences is None or self.max_occurrences > 1

    @property
    def fixed_total_length(self) -> bool:
        """
        Whether this Data Record has fixed total length and number of occurrences.

        Values meaning:

        - True - the number of occurrences is always the same (fixed)
        - False - the number of occurrences might vary
        """
        return self.min_occurrences == self.max_occurrences

    @property
    def min_raw_value(self) -> int:
        """Minimum raw (bit) value for this Data Record."""
        return 0

    @property
    def max_raw_value(self) -> int:
        """Maximum raw (bit) value for this Data Record."""
        return (1 << self.length) - 1

    def get_children_values(self, raw_value: int) -> OrderedDict[str, int]:
        """
        Get raw values of children.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Children names and their values for this occurrence.
        """
        self._validate_raw_value(raw_value)
        children_values = OrderedDict()
        offset = self.length
        for child in self.children:
            offset -= child.length
            mask = (1 << child.length) - 1
            child_value = (raw_value >> offset) & mask
            children_values[child.name] = child_value
        return children_values

    def get_children_occurrence_info(self, raw_value: int) -> Tuple[SingleOccurrenceInfo, ...]:
        """
        Get occurrence information for all children.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Children occurrence information.
        """
        children_values = self.get_children_values(raw_value)
        children_occurrence_info: List[SingleOccurrenceInfo] \
            = [child.get_occurrence_info(children_values[child.name]) for child in self.children]  # type: ignore
        return tuple(children_occurrence_info)

    def get_occurrence_info(self, *raw_values: int) -> DataRecordInfoAlias:
        """
        Extract comprehensive occurrence information with automatic child extraction.

        :param raw_values: Raw value for each occurrence of this Data Record.

        :raise ValueError: Either no values were provided or multiple values for a single occurrence Data Record.

        :return: Data Record Information about a Single Occurrence or Multiple Occurrences.
        """
        if len(raw_values) == 0:
            raise ValueError("Raw value for at least one occurrence must be provided.")
        if self.is_reoccurring:
            children_values = []
            for raw_value in raw_values:
                children_values.append(self.get_children_occurrence_info(raw_value))
            return MultipleOccurrencesInfo(name=self.name,
                                           length=self.length,
                                           raw_value=tuple(raw_values),
                                           physical_value=self.get_physical_values(*raw_values),
                                           children=tuple(children_values),
                                           unit=self.unit)
        if len(raw_values) == 1:
            raw_value = raw_values[0]
            return SingleOccurrenceInfo(name=self.name,
                                        length=self.length,
                                        raw_value=raw_value,
                                        physical_value=self.get_physical_value(raw_value),
                                        children=self.get_children_occurrence_info(raw_value),
                                        unit=self.unit)
        raise ValueError("Cannot handle multiple occurrences values for non reoccurring Data Record.")

    def get_physical_values(self, *raw_values: int) -> MultiplePhysicalValuesAlias:
        """
        Get physical values representing provided raw values.

        :param raw_values: Raw (bit) values of this Data Record for multiple occurrences.

        :raise RuntimeError: A call was made on a Data Record that is not reoccurring.
        :raise ValueError: Incorrect number of occurrences was provided.

        :return: Physical values for provided occurrences.
        """
        if not self.is_reoccurring:
            raise RuntimeError("This method must be called for reoccurring Data Record only.")
        if not self.min_occurrences <= len(raw_values) <= (self.max_occurrences or float("inf")):
            raise ValueError(f"This Data Record requires from {self.min_occurrences} to "
                             f"{self.max_occurrences or 'Infinite'} number of occurrences. "
                             f"Provided {len(raw_values)} occurrences.")
        return tuple(self.get_physical_value(raw_value) for raw_value in raw_values)

    @abstractmethod
    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Get physical value representing provided raw value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Physical value for this occurrence.
        """

    @abstractmethod
    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        """
        Get raw value that represents provided physical value.

        :param physical_value: Physical value of this Data Record single occurrence.

        :return: Raw Value for this occurrence.
        """

    def get_raw_value_from_children(self, children_values: ChildrenValuesAlias) -> int:
        """
        Get raw value that represents provided children values.

        :param children_values: Mapping of children values.
            Mapping keys are children names.
            Mapping values are corresponding children raw values or similar mapping for its children.

        :raise RuntimeError: The call was made for a Data Record without any children.
        :raise TypeError: Provided value is not a mapping.
        :raise ValueError: Provided mapping is incorrect and cannot be handled.

        :return: Raw Value for this occurrence.
        """
        if not self.children:
            raise RuntimeError("This Data Record has no children.")
        if not isinstance(children_values, Mapping):
            raise TypeError("Provided value is not a mapping.")
        children_names = set(child.name for child in self.children)
        provided_names = set(children_values.keys())
        if provided_names != children_names:
            raise ValueError("Values for all and only children have to be provided. "
                             f"Names of all children: {children_names}. Provided names: {provided_names}.")
        offset = self.length
        raw_value = 0
        for child in self.children:
            offset -= child.length
            child_value = children_values[child.name]
            if isinstance(child_value, int):
                child_raw_value = child_value
            elif isinstance(child_value, Mapping):
                child_raw_value = child.get_raw_value_from_children(child_value)
            else:
                raise ValueError("Value for each child must be a raw value or a mapping with its children values.")
            raw_value += child_raw_value << offset
        return raw_value

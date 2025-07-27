"""Definition of Data Records structure and API."""

__all__ = ["AbstractDataRecord", "MultipleOccurrencesInfo", "MultiplePhysicalValues", "PhysicalValueAlias",
           "SingleOccurrenceInfo", "SinglePhysicalValueAlias"]

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import List, Optional, Sequence, Tuple, TypedDict, Union

from uds.utilities import InconsistentArgumentsError, ReassignmentError

SinglePhysicalValueAlias = Union[int, float, str]
"""Alias for a physical value decoded from a single occurrence."""
MultiplePhysicalValues = Union[str, Tuple[SinglePhysicalValueAlias, ...]]
"""Alias for a physical values decoded from multiple occurences."""
PhysicalValueAlias = Union[SinglePhysicalValueAlias, MultiplePhysicalValues]
"""Alias for all physical values."""


class SingleOccurrenceInfo(TypedDict, total=True):
    """
    Information about a single Data Record occurrence.

    :arg name: Data Record name.
    :arg raw_value: Raw values for this occurrence.
    :arg physical_value: Physical value for this occurrence.
    :arg children: Information about children for this occurrence.
    """

    name: str
    raw_value: int
    physical_value: SinglePhysicalValueAlias
    children: Tuple["SingleOccurrenceInfo", ...]


class MultipleOccurrencesInfo(TypedDict, total=True):
    """
    Information about multiple Data Record occurrences.

    :arg name: Data Record name.
    :arg raw_value: List with raw values for each occurrence.
    :arg physical_value: Physical values for multiple occurrences.
    :arg children: List with one element for each occurrence.
        Each element contains information about children for this occurrence.
    """

    name: str
    raw_value: List[int]
    physical_value: MultiplePhysicalValues
    children: List[Tuple["SingleOccurrenceInfo", ...]]


class AbstractDataRecord(ABC):
    """
    Common implementation and interface for all Data Records.

    Data Records are parts of diagnostic messages which could be interpreted in various ways.
    The objects would allow users to operate on meaningful data (e.g. vehicle speed in km/h,
    temperature in Celsius degrees) which we call physical values instead of raw (byte) values.
    Each subclass is meant to provide utilities for translation between physical and raw values.
    """

    def __init__(self,
                 name: str,
                 length: int,
                 children: Sequence["AbstractDataRecord"],
                 min_occurrences: int,
                 max_occurrences: Optional[int]) -> None:
        """
        Initialize common part for all Data Records.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param children: Contained Data Records.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        """
        self.name = name
        self.length = length
        self.children = children
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences

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
        try:
            getattr(self, "_AbstractDataRecord__name")
        except AttributeError:
            self.__name = stripped_names
        else:
            raise ReassignmentError("You cannot change Data Record name. Create a new Data Record instead.")

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
        try:
            getattr(self, "_AbstractDataRecord__length")
        except AttributeError:
            self.__length = value
        else:
            raise ReassignmentError("You cannot change Data Record length. Create a new Data Record instead.")

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
        :raise InconsistentArgumentsError: Provided sequence of Data Records cannot be children for this Data Record.
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
            raise InconsistentArgumentsError("Total children length does not much the length of this Data Record.")
        if len(children_names) != len(value):
            raise InconsistentArgumentsError("Each child has to have unique name.")
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
        try:
            getattr(self, "_AbstractDataRecord__min_occurrences")
        except AttributeError:
            self.__min_occurrences = value
        else:
            raise ReassignmentError("You cannot change minimal number of Data Record occurrences. "
                                    "Create a new Data Record instead.")

    @property
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of occurrences for this Data Record.

        .. info:: No maximal number (infinite number of occurrences) is represented by None value.
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
        try:
            getattr(self, "_AbstractDataRecord__max_occurrences")
        except AttributeError:
            self.__max_occurrences = value
        else:
            raise ReassignmentError("You cannot change maximal number of Data Record occurrences. "
                                    "Create a new Data Record instead.")

    @property
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - there might be 0 or 1 occurrence of this Data Record
        - True - number of occurrences might vary
        """
        return self.max_occurrences is None or self.max_occurrences > 1

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
        return tuple(child.get_occurrence_info(children_values[child.name]) for child in self.children)  # type: ignore

    def get_occurrence_info(self, *raw_values: int) -> Union[SingleOccurrenceInfo, MultipleOccurrencesInfo]:
        """
        Get occurrence information for this Data Record.

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
                                           raw_value=list(raw_values),
                                           physical_value=self.get_physical_values(*raw_values),
                                           children=children_values)
        if len(raw_values) == 1:
            raw_value = raw_values[0]
            return SingleOccurrenceInfo(name=self.name,
                                        raw_value=raw_value,
                                        physical_value=self.get_physical_value(raw_value),
                                        children=self.get_children_occurrence_info(raw_value))
        raise ValueError("Cannot handle multiple occurrences values for non reoccurring Data Record.")

    def get_physical_values(self, *raw_values: int) -> MultiplePhysicalValues:
        """
        Decode raw values and provide physical values.

        :param raw_values: Raw (bit) values of this Data Record for multiple occurrences.

        :raise RuntimeError: A called was made on a Data Record that is not reoccurring.
        :raise ValueError: No values were provided.

        :return: Decoded physical values for provided raw values.
        """
        if not self.is_reoccurring:
            raise RuntimeError("This method must be called for reoccurring Data Record only.")
        if len(raw_values) == 0:
            raise ValueError("Raw value for at least one occurrence must be provided.")
        return tuple(self.get_physical_value(raw_value) for raw_value in raw_values)

    @abstractmethod
    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Decode raw value and provide physical value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Decoded physical value for this occurrence.
        """

    @abstractmethod
    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        """
        Encode physical value into raw value.

        :param physical_value: Physical value of this Data Record single occurrence.

        :return: Raw Value for this occurrence.
        """

"""Definition of AbstractDataRecord which is a base class for all Data Records."""

__all__ = ["AbstractDataRecord", "PhysicalValueAlias"]

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, Sequence
from collections import OrderedDict

from uds.utilities import InconsistentArgumentsError, ReassignmentError


PhysicalValueAlias = Union[int, float, str]
"""Alias for physical values used by Data Records."""


class AbstractDataRecord(ABC):
    """Common implementation and interface for all Data Records."""

    def __init__(self, name: str, length: int, children: Sequence["AbstractDataRecord"] = tuple()) -> None:
        """
        Initialize common part for all Data Records.

        :param name: Name to assign to this Data Record.

        :raise TypeError: Provided value of name is not str type.
        """
        self.name = name
        self.length = length
        self.children = children

    def __validate_raw_value(self, raw_value: int) -> None:
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
        """Name of this Data Record."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set name for this Data Record

        :param value: Value to set.
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
            raise ReassignmentError("You cannot change Data Record name. Create a new one.")

    @property
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        return self.__length

    @length.setter
    def length(self, value: int) -> None:
        if not isinstance(length, int):
            raise TypeError("Length must be an integer.")
        if length <= 0:
            raise ValueError("Length must be a positive value.")

    @property
    def min_raw_value(self) -> int:
        """Minimum raw (bit) value for this Data Record."""
        return 0

    @property
    def max_raw_value(self) -> int:
        """Maximum raw (bit) value for this Data Record."""
        return (1 << self.length) - 1

    @property
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """
        return not (self.min_occurrences == self.max_occurrences == 1)

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
            children_names.add(value)
        if children_length != self.length:
            raise InconsistentArgumentsError("Total children length does not much the length of this Data Record.")
        if len(children_names) != len(value):
            raise InconsistentArgumentsError("Each child has to have unique name.")
        self.__children = tuple(value)

    @property
    @abstractmethod
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.is_reoccurring`
            equals True.
        """

    @property
    @abstractmethod
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.is_reoccurring`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """

    @abstractmethod
    def get_physical_value(self, raw_value: int) -> PhysicalValueAlias:
        """
        Decode raw value and provide physical value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Decoded physical (meaningful e.g. vehicle speed in km/h) value for this occurence.
        """
        self.__validate_raw_value(raw_value)


    @abstractmethod
    def get_raw_value(self, physical_value: PhysicalValueAlias) -> int:
        """
        Encode physical value into raw value.

        :param physical_value: Physical (meaningful e.g. vehicle speed in km/h) value of this Data Record
            single occurrence.

        :return: Raw Value of this Data Record occurrence.
        """

    def get_children_values(self, raw_value: int) -> OrderedDict[str, int]:
        """
        Get raw values of children.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Children names and their values for this occurrence.
        """
        self.__validate_raw_value(raw_value)
        children_values = OrderedDict()
        offset = self.length
        for child in self.children:
            offset += child.length
            mask = (1 >> child.length) - 1
            child_value = (raw_value << offset) & mask
            children_values[child.name] = child_value
        return children_values

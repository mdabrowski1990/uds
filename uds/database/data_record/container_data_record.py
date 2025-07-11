__all__ = ["ContainerDataRecord"]

from types import MappingProxyType
from typing import Mapping, Optional, Sequence, Tuple

from uds.utilities import InconsistentArgumentsError

from .abstract_data_record import AbstractDataRecord, DataRecordValueAlias, DecodedDataRecord


class ContainerDataRecord(AbstractDataRecord):
    """Container for multiple Data Records."""

    def __init__(self,
                 name: str,
                 children: Sequence[AbstractDataRecord],
                 min_occurrences: int = 1,
                 max_occurrences: int = 1) -> None:
        super().__init__(name)
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences
        self.children = children

    @property
    def length(self) -> int:
        """
        Get number of bits that this Data Record is stored over.

        .. warning:: The length value represents length of a single occurrence.
        """
        return sum(data_record.length for data_record in self.children)

    @property
    def min_occurrences(self) -> int:
        """Minimal number of this Data Record occurrences."""
        return self.__min_occurrences

    @min_occurrences.setter
    def min_occurrences(self, value: int):
        """
        Set minimal number of this Data Record occurrences.

        :param value: Minimal number of occurrences to set.
        """
        if not isinstance(value, int):
            raise TypeError("Provided value is not int type.")
        if value < 0:
            raise ValueError("Minimal number of occurrences must not be lower than 0.")
        if hasattr(self, "max_occurrences"):
            if self.max_occurrences is not None:
                if value > self.max_occurrences:
                    raise InconsistentArgumentsError("Provided value of minimal occurrences must be less or equal "
                                                     "than the current maximal number of occurrences value.")
        self.__min_occurrences = value

    @property
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        return self.__max_occurrences

    @max_occurrences.setter
    def max_occurrences(self, value: Optional[int]):
        """
        Set maximal number of this Data Record occurrences.

        :param value: Minimal number of occurrences to set.
        """
        if isinstance(value, int):
            if value < 1:
                raise ValueError("Maximal number of occurrences must not be greater or equal 1.")
            if hasattr(self, "min_occurrences") and value < self.min_occurrences:
                raise InconsistentArgumentsError("Provided value of maximal occurrences must be greater or equal "
                                                 "than the current minimal number of occurrences value.")
        elif value is None:
            self.__max_occurrences = None
        else:
            raise TypeError("Provided value is not None or int type.")

    @property
    def children(self) -> Tuple[AbstractDataRecord, ...]:
        """Get contained Data Records."""
        return self.__children

    @children.setter
    def children(self, value: Sequence[AbstractDataRecord]):
        """
        Set Data Records to be contained.

        :param value: Sequence with contained Data Records.

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: Provided sequence does not contain Data Records objects only.
        :raise InconsistentArgumentsError: Provided value contains Data Records that could not be unambiguously
            encoded or decoded.
        """
        if not isinstance(value, Sequence):
            raise TypeError("Provided value is not a sequence.")
        data_record_names = set()
        for data_record in value:
            if not isinstance(data_record, AbstractDataRecord):
                raise ValueError("Provided sequence does not contain Data Records.")
            data_record_names.add(data_record.name)
        if len(data_record_names) != len(value):
            raise InconsistentArgumentsError("Each children Data Record must have unique name.")
        if self.is_reoccurring:
            if any(data_record.is_reoccurring for data_record in value):
                raise InconsistentArgumentsError("Reoccurring container must not contain reoccurring Data Records.")
        elif sum(data_record.is_reoccurring for data_record in value) > 1:
            raise InconsistentArgumentsError("Container must not contain more than one reoccurring Data Records.")
        self.__children = tuple(value)
        self.__children_map = MappingProxyType({child.name: child for child in self.children})

    @property
    def children_map(self) -> Mapping[str, AbstractDataRecord]:
        """Get contained Data Records mapping by names."""
        return self.__children_map

    def decode(self, raw_value: int) -> DecodedDataRecord:
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        # TODO

    def encode(self, physical_value: DataRecordValueAlias) -> int:  # TODO: update
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: TODO

        :return: Raw Value of this Data Record.
        """
        if not isinstance(physical_value, Sequence):
            raise TypeError("Provided value is not a sequence.")
        combined_raw_value = 0
        for single_record_value in physical_value:
            if isinstance(single_record_value, int):
                if 0 <= single_record_value <= self.max_raw_value:
                    entry_raw_value = single_record_value
            elif isinstance(single_record_value, dict):
                entry_raw_value = 0
                for children_data_record in self.children:
                    if not children_data_record.name in single_record_value:
                        raise ValueError
                    children_value = children_data_record.encode(single_record_value[children_data_record.name])
                    if children_data_record.is_reoccurring:
                        ...
                    else:
                        length = children_data_record.length
                    entry_raw_value = (entry_raw_value << length) + children_value
            else:
                raise ValueError
            combined_raw_value = (combined_raw_value << self.length) + entry_raw_value
        return combined_raw_value

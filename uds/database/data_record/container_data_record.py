__all__ = ["ContainerDataRecord"]

from typing import Sequence, Optional, Tuple
from .abstract_data_record import AbstractDataRecord, DecodedDataRecord
from uds.utilities import InconsistentArgumentsError


class ContainerDataRecord(AbstractDataRecord):

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
        """Get Data Records contained by this Container."""
        return self.__children

    @children.setter
    def children(self, value: Sequence[AbstractDataRecord]):
        """
        Set Data Records to be contained.

        :param value: Sequence with contained Data Records.
        """
        if not isinstance(value, Sequence):
            raise TypeError
        if not all(isinstance(data_record, AbstractDataRecord) for data_record in value):
            raise ValueError
        if self.is_reoccurring and any(data_record.is_reoccurring for data_record in value):
            raise InconsistentArgumentsError
        self.__children = tuple(value)

    def decode(self, raw_value: int) -> DecodedDataRecord:
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        # TODO
__all__ = ["ContainerDataRecord"]

from typing import Sequence, Optional, Tuple
from .abstract_data_record import AbstractDataRecord, DecodedDataRecord


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

    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        # TODO

    @property
    def min_occurrences(self) -> int:
        """Minimal number of this Data Record occurrences."""
        return self.__min_occurrences

    @min_occurrences.setter
    def min_occurrences(self, value: int):
        if not isinstance(value, int):
            raise TypeError
        if value < 0:
            raise ValueError
        self.__min_occurrences = value

    @property
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        return self.__max_occurrences

    @max_occurrences.setter
    def max_occurrences(self, value: int):
        if isinstance(value, int):
            if value < 1:
                raise ValueError
        elif value is None:
            self.__max_occurrences = None
        else:
            raise TypeError

    @property
    def children(self) -> Tuple[AbstractDataRecord, ...]:
        return self.__children

    @children.setter
    def children(self, value: Sequence[AbstractDataRecord]):
        if not isinstance(value, Sequence):
            raise TypeError
        if not all(isinstance(_val, AbstractDataRecord) for _val in value):
            raise ValueError
        self.__children = tuple(value)

    def decode(self, raw_value: int) -> DecodedDataRecord:
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        # TODO
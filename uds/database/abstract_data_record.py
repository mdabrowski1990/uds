"""
Definition of all Data Records types.

Each Data Record contains mapping (translation) of raw data (sequence of bits in diagnostic message payload) to some
meaningful information (e.g. physical value, text).
"""

__all__ = ["DataRecordType", "AbstractDataRecord", "DecodedDataRecord"]

from abc import ABC, abstractmethod
from typing import Tuple, TypedDict, Union

from uds.utilities import ValidatedEnum

DataRecordPhysicalValueAlias = Union[int, float, str, Tuple["DecodedDataRecord", ...]]
"""Alias of Data Records' physical value."""


class DecodedDataRecord(TypedDict):
    """Structure of decoded Data Record."""

    name: str
    raw_value: int
    physical_value: DataRecordPhysicalValueAlias


class DataRecordType(ValidatedEnum):
    """All Data Record types."""

    # TODO: fill with following tasks:
    #  - https://github.com/mdabrowski1990/uds/issues/2
    #  - https://github.com/mdabrowski1990/uds/issues/6
    #  - https://github.com/mdabrowski1990/uds/issues/8
    #  - https://github.com/mdabrowski1990/uds/issues/9
    #  - https://github.com/mdabrowski1990/uds/issues/10


class AbstractDataRecord(ABC):
    """Common implementation and interface for all Data Records."""

    def __init__(self, name: str) -> None:
        """
        Common part of initialization for all Data Records.

        :param name: Name to assign to this Data Record.
        """
        self.__name = name

    @property
    def name(self) -> str:
        """Name of this Data Record."""
        return self.__name

    @property
    @abstractmethod
    def data_record_type(self) -> DataRecordType:
        """Type of this Data Record."""

    @property
    @abstractmethod
    def length(self) -> int:
        """Number of bits that this Data Record is carried over."""

    @property
    @abstractmethod
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """

    @property
    @abstractmethod
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.min_occurrences`
            equals True.
        """

    @property
    @abstractmethod
    def max_occurrences(self) -> int:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.min_occurrences`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by `0` value.
        """

    @property
    @abstractmethod
    def contains(self) -> Tuple["AbstractDataRecord", ...]:
        """Data Records contained by this Data Record."""

    @abstractmethod
    def decode(self, raw_value: int) -> DecodedDataRecord:
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """

    @abstractmethod
    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """

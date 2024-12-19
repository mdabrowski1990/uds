"""Definition of AbstractDataRecord which is a base class for all Data Records."""

__all__ = ["AbstractDataRecord", "DataRecordPhysicalValueAlias", "DecodedDataRecord", "DataRecordValueAlias"]

from abc import ABC, abstractmethod
from typing import Dict, Optional, Sequence, Tuple, TypedDict, Union

DataRecordValueAlias = Union[
    int,  # raw value
    float,  # physical value calculated through formula
    str,  # text (physical) value from either Text Table or Text encoding
    Dict[str, "DataRecordValueAlias"],  # value of container's children
    Sequence[Union[int, Dict[str, "DataRecordValueAlias"]]],  # values for reoccurring container
]
"""
Alias of Data Records' input value.

Each type represent other data:

- int type - raw value of a data record
- float type - physical value of a formula data record

    .. warning:: Providing physical value as float might sometime cause issues due
        `floating-point precision <https://docs.python.org/3/tutorial/floatingpoint.html>`_.
        The closest raw value would be evaluated and put into a payload.

        To avoid rounding, provide raw value (int type).

- str type - text (physical) value of either text table or text data record
- dict type - values for children of a container data records
- sequence type - values for following occurrences of a container data record
"""

DataRecordPhysicalValueAlias = Union[
    int,  # physical value is the same as raw value
    float,  # physical value calculated through formula
    str,  # decoded text value
    Tuple[Tuple["DecodedDataRecord", ...], ...]  # decoded container value, each element is another entry
]
"""
Alias of Data Records' physical value.

Each type represent other data:

- int type - physical value is the same as raw value
- float type - value received through formula calculation
- str type - text value received either through encoding (e.g. ASCII, UTF-8)
  or mapping (each value has specific meaning)
- tuple type - one element for each container occurrence; each element is a tuple with values for children data records
"""


class DecodedDataRecord(TypedDict):
    """Structure of decoded Data Record."""

    name: str
    raw_value: int
    physical_value: DataRecordPhysicalValueAlias  # noqa: F841


class AbstractDataRecord(ABC):
    """
    Common implementation and interface for all Data Records.

    Data Records are fragments of diagnostic messages.
    Each Data Record defines how to interpret a single element/signal.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize common part for all Data Records.

        :param name: Name to assign to this Data Record.

        :raise TypeError: Provided value of name is not str type.
        """
        if not isinstance(name, str):
            raise TypeError("Provided name is not str type.")
        self.__name = name.strip()

    @property
    def name(self) -> str:
        """Name of this Data Record."""
        return self.__name

    @property  # noqa: F841
    @abstractmethod
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""

    @property
    def max_raw_value(self):
        """
        Maximum raw (bit) value for this Data Record.

        :return: Maximum value that can be represented by `length` bits.
        """
        return (1 << self.length) - 1

    @abstractmethod
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
         - True - number of occurrences might vary
         - False - constant number of occurrences in every diagnostic message
        """
        return self.min_occurrences != self.max_occurrences

    @property  # noqa: F841
    @abstractmethod
    def min_occurrences(self) -> int:
        """Minimal number of this Data Record occurrences."""

    @property  # noqa: F841
    @abstractmethod
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """

    @property  # noqa: F841
    @abstractmethod
    def children(self) -> Tuple["AbstractDataRecord", ...]:
        """Get Data Records contained by this Data Record."""

    @abstractmethod
    def decode(self, raw_value: int) -> DecodedDataRecord:  # noqa: F841
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """

    @abstractmethod
    def encode(self, physical_value: DataRecordValueAlias) -> int:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """

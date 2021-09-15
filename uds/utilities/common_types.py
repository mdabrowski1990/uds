"""Module with all common types (and its aliases) used in the package and helper functions for these types."""

__all__ = ["RawByte", "RawBytes", "RawBytesTuple", "RawBytesSet", "validate_raw_bytes",
           "TimeMilliseconds", "TimeStamp"]

from typing import Union, Tuple, List, Set, Any
from datetime import datetime

RawByte = int
"""Typing alias of byte value - integer in range 0x00-0xFF - that is used by the package."""
RawBytesTuple = Tuple[RawByte, ...]
"""Typing alias of a tuple filled with byte values."""
RawBytesSet = Set[RawByte]
"""Typing alias of a set filled with byte values."""
RawBytes = Union[RawBytesTuple, List[RawByte]]
"""Typing alias of a sequence filled with byte values."""
TimeMilliseconds = Union[int, float]  # noqa: F841
"""Typing alias of an amount of time in milliseconds that is used by the package."""
TimeStamp = datetime
"""Typing alias of a `timestamp <https://en.wikipedia.org/wiki/Timestamp>`_ that is used by the package."""


def validate_raw_bytes(value: Any) -> None:
    """
    Validate whether provided value stores raw bytes.

    :param value: Value to validate.

    :raise TypeError: Value is not tuple or list type.
    :raise ValueError: Value does not contain raw bytes (int value between 0x00-0xFF) only.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Provided value is not list or tuple type. Actual type: {type(value)}.")
    if not value or not all(isinstance(raw_byte, int) and 0x00 <= raw_byte <= 0xFF for raw_byte in value):
        raise ValueError(f"Provided value does not contain raw bytes (int value between 0x00 and 0xFF) only. "
                         f"Actual value: {value}")

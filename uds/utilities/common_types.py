"""Module with all common types (and its aliases) used in the package and helper functions for these types."""

__all__ = ["Nibble", "RawByte", "RawBytes", "RawBytesTuple", "RawBytesList", "RawBytesSet",
           "validate_nibble", "validate_raw_byte", "validate_raw_bytes",
           "TimeMilliseconds", "TimeStamp"]

from typing import Union, Tuple, List, Set, Any
from datetime import datetime


Nibble = int
"""Alias of a `nibble <https://en.wikipedia.org/wiki/Nibble>`_ value (integer in range 0x0-0xF)."""
RawByte = int
"""Alias of a byte value (integer in range 0x00-0xFF)."""
RawBytesTuple = Tuple[RawByte, ...]
"""Alias of a tuple filled with byte values."""
RawBytesSet = Set[RawByte]
"""Alias of a set filled with byte values."""
RawBytesList = List[RawByte]
"""Alias of a list filled with byte values."""
RawBytes = Union[RawBytesTuple, RawBytesList]
"""Alias of a sequence filled with byte values."""
TimeMilliseconds = Union[int, float]
"""Alias of a time value in milliseconds."""
TimeStamp = datetime
"""Alias of a `timestamp <https://en.wikipedia.org/wiki/Timestamp>`_ value."""


def validate_nibble(value: Any) -> None:
    """
    Validate whether provided value stores a nibble value.

    :param value: Value to validate.

    :raise TypeError: Value is not int type.
    :raise ValueError: Value is out of byte range (0x0-0xF).
    """
    if not isinstance(value, int):
        raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
    if not 0x0 <= value <= 0xF:
        raise ValueError(f"Provided value is out of nibble values range (0x0-0xF). Actual value: {value}")


def validate_raw_byte(value: Any) -> None:
    """
    Validate whether provided value stores a raw byte value.

    :param value: Value to validate.

    :raise TypeError: Value is not int type.
    :raise ValueError: Value is out of byte range (0x00-0xFF).
    """
    if not isinstance(value, int):
        raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
    if not 0x00 <= value <= 0xFF:
        raise ValueError(f"Provided value is out of byte values range (0x00-0xFF). Actual value: {value}")


def validate_raw_bytes(value: Any) -> None:
    """
    Validate whether provided value stores raw bytes value.

    :param value: Value to validate.

    :raise TypeError: Value is not tuple or list type.
    :raise ValueError: Value does not contain raw bytes (int value between 0x00-0xFF) only.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Provided value is not list or tuple type. Actual type: {type(value)}")
    if not value or not all(isinstance(raw_byte, int) and 0x00 <= raw_byte <= 0xFF for raw_byte in value):
        raise ValueError(f"Provided value does not contain raw bytes (int value between 0x00 and 0xFF) only. "
                         f"Actual value: {value}")

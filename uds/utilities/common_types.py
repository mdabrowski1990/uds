"""Module with all common types (and its aliases) used in the package and helper functions for these types."""

__all__ = ["TimeMillisecondsAlias",
           "RawBytesAlias", "RawBytesTupleAlias", "RawBytesListAlias", "RawBytesSetAlias",
           "validate_nibble", "validate_raw_byte", "validate_raw_bytes"]

from typing import List, Set, Tuple, Union

TimeMillisecondsAlias = Union[int, float]
"""Alias of a time value in milliseconds."""
RawBytesTupleAlias = Tuple[int, ...]
"""Alias of a tuple filled with byte values."""
RawBytesSetAlias = Set[int]
"""Alias of a set filled with byte values."""
RawBytesListAlias = List[int]
"""Alias of a list filled with byte values."""
RawBytesAlias = Union[bytes, bytearray, RawBytesTupleAlias, RawBytesListAlias]
"""Alias of a sequence filled with byte values."""


def validate_nibble(value: int) -> None:
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


def validate_raw_byte(value: int) -> None:
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


def validate_raw_bytes(value: RawBytesAlias, allow_empty: bool = False) -> None:
    """
    Validate whether provided value stores raw bytes value.

    :param value: Value to validate.
    :param allow_empty: True if empty list is allowed, False otherwise.

    :raise TypeError: Provided value is not tuple, list, bytearray or bytes type.
    :raise ValueError: Provided value does not contain raw bytes (int values between 0x00-0xFF) only.
    """
    if not isinstance(value, (tuple, list, bytearray, bytes)):
        raise TypeError(f"Provided value is not tuple, list, bytearray or bytes type. Actual type: {type(value)}")
    if not allow_empty and not value:
        raise ValueError("Provided values is empty sequence.")
    if not all(isinstance(raw_byte, int) and 0x00 <= raw_byte <= 0xFF for raw_byte in value):
        raise ValueError("Provided value does not contain raw bytes (int value between 0x00 and 0xFF) only. "
                         f"Actual value: {value!r}")

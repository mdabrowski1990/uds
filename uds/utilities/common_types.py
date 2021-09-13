"""Container with all types (and its aliases) used by the module."""

__all__ = ["RawByte", "RawBytes", "RawBytesTuple", "RawBytesSet", "validate_raw_bytes",
           "TimeMilliseconds", "TimeStamp"]

from typing import Union, Tuple, List, Set, Any
from datetime import datetime

RawByte = int
RawBytesTuple = Tuple[RawByte, ...]
RawBytesSet = Set[RawByte]
RawBytes = Union[RawBytesTuple, List[RawByte]]
TimeMilliseconds = Union[int, float]  # noqa: F841
TimeStamp = datetime


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

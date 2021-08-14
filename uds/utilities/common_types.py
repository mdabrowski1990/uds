"""Container with all types (and its aliases) used by the module."""

__all__ = ["TimeMilliseconds", "RawByte", "RawBytes", "RawBytesTuple", "validate_raw_bytes"]

from typing import Union, Tuple, List

RawByte = int
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint for Python 3.9.
RawBytesTuple = Tuple[RawByte, ...]  # pylint: disable=unsubscriptable-object
RawBytes = Union[RawBytesTuple, List[RawByte]]  # pylint: disable=unsubscriptable-object
TimeMilliseconds = Union[int, float]  # pylint: disable=unsubscriptable-object


def validate_raw_bytes(value: RawBytes) -> None:
    """
    Validate whether provided value contains raw bytes.

    :param value: Value to validate.

    :raise TypeError: Value is not tuple or list type.
    :raise ValueError: Value does not contain raw bytes (int value between 0x00-0xFF) only.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Provided value is not list or tuple type. Actual type: {type(value)}.")
    if not value or not all([isinstance(raw_byte, int) and 0x00 <= raw_byte <= 0xFF for raw_byte in value]):
        raise ValueError(f"Provided value does not contain raw bytes (int value between 0x00 and 0xFF) only. "
                         f"Actual value: {value}")

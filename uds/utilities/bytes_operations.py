"""Module with bytes list operations implementation."""

__all__ = ["Endianness", "bytes_to_int", "int_to_bytes"]

from typing import Optional

from aenum import StrEnum

from .common_types import RawBytesAlias, validate_raw_bytes
from .custom_exceptions import InconsistentArgumentsError
from .enums import ValidatedEnum


class Endianness(ValidatedEnum, StrEnum):
    """
    Endianness values definitions.

    `Endianness <https://en.wikipedia.org/wiki/Endianness>`_ determines order of bytes in a bytes sequence.
    """

    LITTLE_ENDIAN: "Endianness" = "little"  # type: ignore  # noqa: F841
    """Little Endian stores the most significant byte at the largest memory address and the least significant byte
    at the smallest."""
    BIG_ENDIAN: "Endianness" = "big"  # type: ignore
    """Big Endian stores the most significant byte at the smallest memory address and the least significant byte
    at the largest."""


def bytes_to_int(bytes_list: RawBytesAlias, endianness: Endianness = Endianness.BIG_ENDIAN) -> int:
    """
    Convert a list of bytes to integer value.

    :param bytes_list: List of bytes to convert.
    :param endianness: Order of bytes to use.

    :return: The integer value represented by provided list of bytes.
    """
    validate_raw_bytes(bytes_list)
    return int.from_bytes(bytes=bytes_list, byteorder=Endianness.validate_member(endianness).value)


def int_to_bytes(int_value: int,
                 size: Optional[int] = None,
                 endianness: Endianness = Endianness.BIG_ENDIAN) -> bytes:
    """
    Convert integer value to a list of bytes.

    :param int_value: Integer value to convert.
    :param size: Number of bytes in the output. Use None to use the smallest possible number of bytes.
    :param endianness: Order of bytes to use.

    :raise TypeError: At least one provided value has invalid type.
    :raise ValueError: At least one provided value is out of range.
    :raise InconsistentArgumentsError: Provided value of `size` is too small to contain entire `int_value`.

    :return: The value of bytes list that represents the provided integer value.
    """
    if not isinstance(int_value, int):
        raise TypeError(f"Provided `int_value` is not int type. Actual type: {type(int_value)}")
    if int_value < 0:
        raise ValueError(f"Provided `int_value` is negative and it cannot be converted. Actual value: {int_value}")
    if size is not None:
        if not isinstance(size, int):
            raise TypeError(f"Provided `size` is not int type. Actual type: {type(size)}")
        if size <= 0:
            raise ValueError(f"Provided `size` is not greater than zero. Actual value: {size}")
    endianness = Endianness.validate_member(endianness)
    bytes_number = max(1, (int_value.bit_length() + 7) // 8)
    size = size or bytes_number
    if size < bytes_number:
        raise InconsistentArgumentsError(f"Provided value of `size` is too small to contain all bytes of int_value."
                                         f"Actual values: int_value={int_value}, size={size}")
    return int_value.to_bytes(length=size, byteorder=endianness.value)

"""Module with bytes list operations implementation."""

__all__ = ["Endianness", "EndiannessAlias", "bytes_list_to_int", "int_to_bytes_list"]

from typing import Union, Optional

from aenum import StrEnum

from .enums import ValidatedEnum
from .common_types import RawBytesList, RawBytes, validate_raw_bytes
from .custom_exceptions import InconsistentArgumentsError


class Endianness(StrEnum, ValidatedEnum):
    """
    Endianness values definitions.

    `Endianness <https://en.wikipedia.org/wiki/Endianness>`_ determines order of bytes in a bytes sequence.
    """

    LITTLE_ENDIAN = "little"
    """Little Endian stores the most significant byte at the largest memory address and the least significant byte
    at the smallest."""
    BIG_ENDIAN = "big"
    """Big Endian stores the most significant byte at the smallest memory address and the least significant byte
    at the largest."""


EndiannessAlias = Union[Endianness, str]
"""Alias that describes :class:`~uds.utilities.bytes_operations.Endianness` member type."""


def bytes_list_to_int(bytes_list: RawBytes, endianness: EndiannessAlias = Endianness.BIG_ENDIAN) -> int:
    """
    Convert a list of bytes to integer value.

    :param bytes_list: List of bytes to convert.
    :param endianness: Order of bytes to use.

    :return: The integer value represented by provided list of bytes.
    """
    validate_raw_bytes(bytes_list)
    Endianness.validate_member(endianness)
    return int.from_bytes(bytes=bytes_list, byteorder=endianness)


def int_to_bytes_list(int_value: int,
                      list_size: Optional[int] = None,
                      endianness: EndiannessAlias = Endianness.BIG_ENDIAN) -> RawBytesList:
    """
    Convert integer value to a list of bytes.

    :param int_value: Integer value to convert.
    :param list_size: Size of the output list. Use None to use the smallest possible list size.
    :param endianness: Order of bytes to use.

    :raise TypeError: At least one provided value has invalid type.
    :raise ValueError: At least one provided value is out of range.
    :raise InconsistentArgumentsError: Provided value of `list_size` is too small to contain entire `int_value`.
    :raise NotImplementedError: A valid endianness was provided, but the implementation for it is missing.
        Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
        whenever you see this error.

    :return: The value of bytes list that represents the provided integer value.
    """
    if not isinstance(int_value, int):
        raise TypeError(f"Provided `int_value` is not int type. Actual type: {type(int_value)}")
    if int_value < 0:
        raise ValueError(f"Provided `int_value` is negative and it cannot be converted. Actual value: {int_value}")
    if list_size is not None:
        if not isinstance(list_size, int):
            raise TypeError(f"Provided `list_size` is not int type. Actual type: {type(list_size)}")
        if list_size <= 0:
            raise ValueError(f"Provided `list_size` is not greater than zero. Actual value: {list_size}")
    Endianness.validate_member(endianness)
    bytes_number = max(1, (int_value.bit_length() + 7) // 8)
    list_size = list_size or bytes_number
    if list_size < bytes_number:
        raise InconsistentArgumentsError(f"Provided value of `list_size` is too small to contain all byte of int_value."
                                         f"Actual values: int_value={int_value}, list_size={list_size}")
    hex_value = "".join(["{", f":0{2 * bytes_number}X", "}"]).format(int_value)
    bytes_list = list(bytes.fromhex(hex_value))
    bytes_list = ([0] * (list_size - len(bytes_list))) + bytes_list
    if endianness == Endianness.BIG_ENDIAN:
        return bytes_list
    if endianness == Endianness.LITTLE_ENDIAN:
        return bytes_list[::-1]
    raise NotImplementedError(f"Implementation missing for: {endianness}.")

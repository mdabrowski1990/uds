"""Module with various conversion functions."""

__all__ = ["bytes_to_hex", "bytes_to_int", "int_to_bytes", ]

from typing import Optional

from .common_types import RawBytesAlias, validate_raw_bytes
from .custom_exceptions import InconsistencyError
from .enums import Endianness


def bytes_to_hex(bytes_list: RawBytesAlias) -> str:
    """
    Convert a sequence of raw bytes to a parenthesized, comma-separated hex string.
    
    The result formats each byte as an uppercase two-digit hex literal prefixed with `0x`
    and joined with `, `, e.g. "(0x01, 0xFF, 0x0A)".
    
    Parameters:
        bytes_list: A sequence of byte values (0–255). The input is validated and
            invalid values will cause the same errors raised by validate_raw_bytes.
    
    Returns:
        A string containing the formatted hex representation of the input bytes.
    """
    validate_raw_bytes(bytes_list)
    bytes_str = ", ".join(f"0x{byte_value:02X}" for byte_value in bytes_list)
    return f"({bytes_str})"


def bytes_to_int(bytes_list: RawBytesAlias, endianness: Endianness = Endianness.BIG_ENDIAN) -> int:
    """
    Convert a sequence of bytes to an integer using the specified endianness.
    
    Validates the input byte sequence and the provided endianness, then returns the integer
    value produced by int.from_bytes(bytes, byteorder). The endianness may be any member
    of the Endianness enum (defaults to Endianness.BIG_ENDIAN).
    
    Parameters:
        bytes_list (RawBytesAlias): Sequence of raw bytes to convert.
        endianness (Endianness): Byte order to use; will be normalized via Endianness.validate_member.
    
    Returns:
        int: Integer represented by the byte sequence.
    
    Raises:
        Any exception raised by validate_raw_bytes or Endianness.validate_member when the input
        bytes or endianness are invalid.
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
    :raise InconsistencyError: Provided value of `size` is too small to contain entire `int_value`.

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
        raise InconsistencyError("Provided value of `size` is too small to contain all bytes of int_value. "
                                 f"Actual values: int_value={int_value}, size={size}")
    return int_value.to_bytes(length=size, byteorder=endianness.value)

"""Module with various conversion functions."""

__all__ = [
    "int_to_obd_dtc", "obd_dtc_to_int",
    "bytes_to_hex", "bytes_to_int", "int_to_bytes",
]

import re
from typing import Optional

from .common_types import RawBytesAlias, validate_raw_bytes
from .constants import BITS_TO_DTC_CHARACTER_MAPPING, DTC_CHARACTERS_MAPPING, MAX_DTC_VALUE, MIN_DTC_VALUE
from .custom_exceptions import InconsistencyError
from .enums import Endianness


def bytes_to_hex(bytes_list: RawBytesAlias) -> str:
    """
    Convert a list of bytes to hex string.

    :param bytes_list: List of bytes to convert.

    :return: String with provided list of bytes presented as hexadecimal values.
    """
    validate_raw_bytes(bytes_list)
    bytes_str = ", ".join(f"0x{byte_value:02X}" for byte_value in bytes_list)
    return f"({bytes_str})"


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
        if size < 0:
            raise ValueError(f"Provided `size` is smaller than zero. Actual value: {size}")
    endianness = Endianness.validate_member(endianness)
    if size == 0 and int_value == 0:
        return bytes()
    bytes_number = max(1, (int_value.bit_length() + 7) // 8)
    size = bytes_number if size is None else size
    if size < bytes_number:
        raise InconsistencyError("Provided value of `size` is too small to contain all bytes of int_value. "
                                 f"Actual values: int_value={int_value}, size={size}")
    return int_value.to_bytes(length=size, byteorder=endianness.value)


def obd_dtc_to_int(obd_dtc: str) -> int:
    """
    Convert text with DTC in OBD format into integer value (DTC in UDS format).

    :param obd_dtc: Text with DTC in OBD format.

    :raise TypeError: Provided value is not str type.
    :raise ValueError: Provided value is not DTC in OBD format.

    :return: Integer value representation of this DTC in UDS format.
    """
    if not isinstance(obd_dtc, str):
        raise TypeError("Provided value is not str type.")
    match = re.compile(r"^([PCBU])([0-3])([0-9A-F]{3})-([0-9A-F]{2})$", re.IGNORECASE).fullmatch(obd_dtc.upper())
    if not match:
        raise ValueError(f"Provided value is not a DTC in OBD format. Example: 'U0F1E-2D'. Actual value: {obd_dtc!r}")
    group_char, specification_number, fault_specification, fault_symptom = match.groups()
    return ((DTC_CHARACTERS_MAPPING[group_char] << 22)
            + (int(specification_number, 16) << 20)
            + (int(fault_specification, 16) << 8)
            + int(fault_symptom, 16))


def int_to_obd_dtc(dtc: int) -> str:
    """
    Encode integer value (DTC in UDS format) into text with DTC in OBD format.

    :param dtc: Integer with DTC in UDS format.

    :raise TypeError: Provided value is not int type.
    :raise ValueError: Provided value is not DTC in OBD format.

    :return: Text value representation of this DTC in OBD format.
    """
    if not isinstance(dtc, int):
        raise TypeError("Provided value is not int type.")
    if not MIN_DTC_VALUE <= dtc <= MAX_DTC_VALUE:
        raise ValueError("Provided value is not a DTC in UDS format.")
    return f"{BITS_TO_DTC_CHARACTER_MAPPING[dtc >> 22]}{(dtc & 0x3FFF00) >> 8:04X}-{dtc & 0xFF:02X}"

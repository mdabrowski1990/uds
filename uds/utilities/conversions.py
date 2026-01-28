"""Module with various conversion functions."""

__all__ = [
    "int_to_obd_dtc", "obd_dtc_to_int",
    "bytes_to_hex", "bytes_to_int", "int_to_bytes",
    "get_signed_value_decoding_formula", "get_signed_value_encoding_formula",
    "TimeSync",
]

import re
from threading import Lock
from time import perf_counter, time
from typing import Any, Callable, Optional, Union

from .common_types import RawBytesAlias, validate_raw_bytes
from .constants import BITS_TO_DTC_CHARACTER_MAPPING, DTC_CHARACTERS_MAPPING, MAX_DTC_VALUE, MIN_DTC_VALUE
from .custom_exceptions import InconsistencyError
from .enums import Endianness

OBD_DTC_RE = re.compile(r"^([PCBU])([0-3])([0-9A-F]{3})-([0-9A-F]{2})$", re.IGNORECASE)
"""Regular expression for DTC in OBD format."""


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
    validate_raw_bytes(bytes_list, allow_empty=True)
    if len(bytes_list) == 0:
        return 0
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
    match = OBD_DTC_RE.fullmatch(obd_dtc.upper())
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


def get_signed_value_decoding_formula(bit_length: int) -> Callable[[int], int]:
    """
    Get formula for decoding signed integer value.

    :param bit_length: Number of bits used for signed integer value.

    :raise TypeError: Provided value is not int type.
    :raise ValueError: Provided value is out of range.

    :return: Formula for decoding singed integer value from unsigned integer value.
    """
    if not isinstance(bit_length, int):
        raise TypeError("Provided `bit_length` value is not int type.")
    if bit_length < 2:
        raise ValueError(f"Provided `bit_length` is too small for store signed integer value: {bit_length}.")

    def decode_signed_value(value: int) -> int:
        max_value = (1 << bit_length) - 1
        msb_value = 1 << (bit_length - 1)
        if not 0 <= value <= max_value:
            raise ValueError(f"Provided value is out of range (0 <= value <= {max_value}): {value}.")
        return (- (value & msb_value)) + (value & (max_value ^ msb_value))
    return decode_signed_value


def get_signed_value_encoding_formula(bit_length: int) -> Callable[[int], int]:
    """
    Get formula for encoding signed integer value.

    :param bit_length: Number of bits used for signed integer value.

    :raise TypeError: Provided value is not int type.
    :raise ValueError: Provided value is out of range.

    :return: Formula for encoding singed integer value into unsinged integer value.
    """
    if not isinstance(bit_length, int):
        raise TypeError("Provided `bit_length` value is not int type.")
    if bit_length < 2:
        raise ValueError(f"Provided `bit_length` is too small for store signed integer value: {bit_length}.")

    def encode_signed_value(value: int) -> int:
        msb_value = 1 << (bit_length - 1)
        min_value = - msb_value
        max_value = msb_value - 1
        if not min_value <= value <= max_value:
            raise ValueError(f"Provided value is out of range ({min_value} <= value <= {max_value}): {value}.")
        if value >= 0:
            return value
        return 2 * msb_value + value
    return encode_signed_value


class TimeSync:
    """Synchronization between wall clock (`time.time()`) and performance counter (`time.perf_counter()`) values."""

    _instance = None

    DEFAULT_SAMPLES_NUMBER = 20
    DEFAULT_SYNC_EXPIRATION = 10  # s

    def __init__(self,
                 samples_number: Optional[int] = None,
                 sync_expiration: Optional[Union[int, float]] = None) -> None:
        """
        Get time synchronization object.

        :param samples_number: Number of samples to use for synchronization.
        :param sync_expiration: Time in seconds after which synchronization is considered no longer up to date.

        .. warning:: Objects of this class are Singletons.
        """
        if not hasattr(self, "_TimeSync__samples_number"):
            self.samples_number = self.DEFAULT_SAMPLES_NUMBER
        if not hasattr(self, "_TimeSync__sync_expiration"):
            self.sync_expiration = self.DEFAULT_SYNC_EXPIRATION
        if not hasattr(self, "_TimeSync__last_sync_timestamp"):
            self.__last_sync_timestamp = None
        if not hasattr(self, "_TimeSync__offset"):
            self.__offset = None
        if samples_number is not None:
            self.samples_number = samples_number
        if sync_expiration is not None:
            self.sync_expiration = sync_expiration

    def __new__(cls, *args: Any, **kwargs: Any):
        """Return existing instance if one exists, otherwise create one."""
        with Lock():
            if cls._instance is None:
                cls._instance = super(TimeSync, cls).__new__(cls)
        return cls._instance

    @property
    def samples_number(self) -> int:
        """Get number of samples to take during synchronization."""
        return self.__samples_number

    @samples_number.setter
    def samples_number(self, value: int) -> None:
        """
        Set number of samples to take during synchronization.

        :param value: Value to set.

        :raise TypeError: Value is not int type.
        :raise ValueError: Value is not a positive number.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}")
        if value < 1:
            raise ValueError(f"Provided value is not a positive number. Actual value: {value}")
        self.__samples_number = value

    @property
    def sync_expiration(self) -> float:
        """Get time in seconds after which synchronization value is considered outdated."""
        return self.__sync_expiration

    @sync_expiration.setter
    def sync_expiration(self, value: Union[int, float]) -> None:
        """
        Set time in seconds after which synchronization value is considered outdated.

        :param value: Value to set.

        :raise TypeError: Value is not int type.
        :raise ValueError: Value is not a positive number.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided value is not int or float type. Actual type: {type(value)}")
        if value <= 0:
            raise ValueError(f"Provided value is not a positive number. Actual value: {value}")
        self.__sync_expiration = float(value)

    @property
    def last_sync_timestamp(self) -> Optional[float]:
        """Value of performance counter for the last synchronization point."""
        return self.__last_sync_timestamp

    @property
    def is_sync_outdated(self) -> bool:
        """Get flag whether the current sync value is outdated."""
        if self.last_sync_timestamp is None:
            return True
        return perf_counter() - self.last_sync_timestamp > self.sync_expiration

    @property
    def offset(self) -> Optional[float]:
        """Difference between wall clock and performance counter."""
        return self.__offset

    def sync(self) -> float:
        """Perform synchronization."""
        best_offset = None
        best_latency = float("inf")
        for _ in range(self.samples_number):
            perf_value_start = perf_counter()
            time_value = time()
            perf_value_end = perf_counter()
            latency = perf_value_end - perf_value_start
            if latency < best_latency:
                mid_perf = (perf_value_end + perf_value_start) / 2
                best_offset = time_value - mid_perf
        self.__offset = best_offset
        self.__last_sync_timestamp = perf_counter()
        return self.offset

    def time_to_perf_counter(self,
                             time_value: float,
                             min_value: Optional[float] = None,
                             max_value: Optional[float] = None) -> float:
        """
        Convert wall clock time to performance counter.

        :param time_value: Wall clock time value to convert.
        :param min_value: The lowest possible result (an earlier value of performance counter).
        :param max_value: The highest possible result (a later value of performance counter).

        :return: An approximation of performance counter for given wall clock time value.
        """
        if self.is_sync_outdated:
            self.sync()
        converted_value = time_value - self.offset
        if min_value is not None and min_value > converted_value:
            return min_value
        if max_value is not None and max_value < converted_value:
            return max_value
        return converted_value

    def perf_counter_to_time(self,
                             perf_counter_value: float,
                             min_value: Optional[float] = None,
                             max_value: Optional[float] = None) -> float:
        """
        Convert performance counter to wall clock time.

        :param perf_counter_value: Performance counter value to convert.
        :param min_value: The lowest possible result (an earlier value of wall clock time).
        :param max_value: The highest possible result (a later value of wall clock time).

        :return: An approximation of wall clock time for given performance counter value.
        """
        if self.is_sync_outdated:
            self.sync()
        converted_value = perf_counter_value + self.offset
        if min_value is not None and min_value > converted_value:
            return min_value
        if max_value is not None and max_value < converted_value:
            return max_value
        return converted_value

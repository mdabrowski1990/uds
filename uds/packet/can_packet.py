"""
CAN bus specific implementation of UDS packets.

:ref:`CAN packets <knowledge-base-uds-can-packet>`.
"""

__all__ = ["CanPacketType", "CanAddressingFormat", "CanFlowStatus", "CanPacket", "CanPacketRecord"]

from typing import Any
from warnings import warn

from aenum import StrEnum, unique

from uds.utilities import ValidatedEnum, NibbleEnum, RawByte, TimeMilliseconds, validate_raw_byte
from .abstract_packet import AbstractUdsPacketType, AbstractUdsPacket, AbstractUdsPacketRecord


class UnrecognizedSTminWarning(Warning):
    """
    Warning about :ref:`STmin <knowledge-base-can-st-min>` value is reserved and therefore not implemented.

    .. note:: If you have any documentation that defines meaning of a value for which this warning was raised, please
        create a request in `issues management system <https://github.com/mdabrowski1990/uds/issues/new/choose>`_ with
        details.
    """


@unique
class CanPacketType(AbstractUdsPacketType):
    """Definition of :ref:`CAN packet types <knowledge-base-can-n-pci>`."""

    SINGLE_FRAME = 0x0
    """:ref:`Single Frame (SF) <knowledge-base-can-single-frame>` on CAN bus."""
    FIRST_FRAME = 0x1
    """:ref:`First Frame (FF) <knowledge-base-can-first-frame>` on CAN bus."""
    CONSECUTIVE_FRAME = 0x2
    """:ref:`Consecutive Frame (CF) <knowledge-base-can-consecutive-frame>` on CAN bus."""
    FLOW_CONTROL = 0x3
    """:ref:`Flow Control (FC) <knowledge-base-can-flow-control>` on CAN bus."""

    @classmethod
    def is_initial_packet_type(cls, value: Any) -> bool:
        """
        Check whether given argument is a member or a value of packet type that initiates a diagnostic message.

        :param value: Value to check.

        :return: True if given argument is a packet type that initiates a diagnostic message, else False.
        """
        cls.validate_member(value)
        return cls(value) in (cls.SINGLE_FRAME, cls.FIRST_FRAME)


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """Definition of :ref:`CAN addressing formats <knowledge-base-can-addressing>`."""

    NORMAL_11BIT_ADDRESSING = "Normal 11-bit Addressing"
    """This value represents :ref:`normal addressing <knowledge-base-can-normal-addressing>` that uses
    11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING = "Normal Fixed Addressing"
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format. 
    It uses 29-bit CAN Identifiers only."""
    EXTENDED_11BIT_ADDRESSING = "Extended 11-bit Addressing"
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses 11-bit CAN Identifiers."""
    EXTENDED_29BIT_ADDRESSING = "Extended 29-bit Addressing"
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses 29-bit CAN Identifiers."""
    MIXED_11BIT_ADDRESSING = "Mixed 11-bit Addressing"
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>`.
    Subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 11-bit CAN Identifiers."""
    MIXED_29BIT_ADDRESSING = "Mixed 29-bit Addressing"
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>`.
    Subformat of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 29-bit CAN Identifiers."""


@unique
class CanFlowStatus(NibbleEnum, ValidatedEnum):
    """Definition of :ref:`Flow Status (FS) <knowledge-base-can-flow-status>` values."""

    ContinueToSend = 0x0
    """Informs a sending entity to resume Consecutive Frames transmission."""
    Wait = 0x1
    """Inform a sending entity to pause Consecutive Frames transmission."""
    Overflow = 0x2
    """Informs a sending entity to abort transmission of a diagnostic message."""


class CanSTmin:
    """Helper class for :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>` mapping."""

    MAX_STMIN_TIME: TimeMilliseconds = 127
    """Maximal time value of STmin."""

    MIN_VALUE_MS_RANGE: int = 0
    """Minimal value of STmin in milliseconds range (raw value and time value are equal)."""
    MAX_VALUE_MS_RANGE: int = 127
    """Maximal value of STmin in milliseconds range (raw value and time value are equal)."""

    MIN_RAW_BYTE_VALUE_100US_RANGE: RawByte = 0xF1
    """Minimal raw value of STmin in 100 microseconds range."""
    MAX_RAW_BYTE_VALUE_100US_RANGE: RawByte = 0xF9
    """Maximal raw value of STmin in 100 microseconds range."""
    MIN_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.1
    """Minimal time value of STmin in 100 microseconds range."""
    MAX_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.9
    """Maximal time value of STmin in 100 microseconds range."""

    _FLOATING_POINT_ACCURACY: int = 8
    """Accuracy of floating point values - when rounding is necessary due to float operation in python."""

    @classmethod
    def _is_ms_value(cls, value: TimeMilliseconds) -> bool:
        """
        Check if provided argument is STmin time value in milliseconds.

        :param value: Value to check.

        :return: True if provided valid value of STmin time in milliseconds, False otherwise.
        """
        if not cls.MIN_VALUE_MS_RANGE <= value <= cls.MAX_VALUE_MS_RANGE:
            return False
        return value % 1 == 0

    @classmethod
    def _is_100us_value(cls, value: TimeMilliseconds) -> bool:
        """
        Check if provided argument is STmin time value in 100 microseconds.

        :param value: Value to check.

        :return: True if provided valid value of STmin time in 100 microseconds, False otherwise.
        """
        if not cls.MIN_TIME_VALUE_100US_RANGE <= value <= cls.MAX_TIME_VALUE_100US_RANGE:
            return False
        return round(value % 0.1, cls._FLOATING_POINT_ACCURACY) in (0, 0.1)

    @classmethod
    def encode(cls, value: RawByte) -> TimeMilliseconds:
        """
        Map raw value of STmin into time value.

        :param value: Raw value of STmin.

        :return: STmin time in milliseconds.
        """
        validate_raw_byte(value)
        if cls.MIN_VALUE_MS_RANGE <= value <= cls.MAX_VALUE_MS_RANGE:
            return value
        if cls.MIN_RAW_BYTE_VALUE_100US_RANGE <= value <= cls.MAX_RAW_BYTE_VALUE_100US_RANGE:
            return (value - 0xF0) * 0.1
        warn(message=f"STmin 0x{value:X} is not recognized by this version of the package.",
             category=UnrecognizedSTminWarning)
        return cls.MAX_STMIN_TIME

    @classmethod
    def decode(cls, value: TimeMilliseconds) -> RawByte:
        """
        Map time value of STmin into raw value.

        :param value: STmin time in milliseconds.

        :raise TypeError: Provided value is not time in milliseconds.
        :raise ValueError: Value out of supported range.

        :return: Raw value of STmin.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Provided value is not int or float type. Actual type: {type(value)}.")
        if cls._is_ms_value(value):
            return int(value)
        if cls._is_100us_value(value):
            return int(round(value * 10, 0) + 0xF0)
        raise ValueError(f"Provided value is out of valid STmin ranges. Actual value: {value}.")


class CanPacket(AbstractUdsPacket):
    """TODO: knowledge base first"""


class CanPacketRecord(AbstractUdsPacketRecord):
    """TODO: knowledge base first"""

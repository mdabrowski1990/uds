"""
Implementation specific for Flow Control CAN packets.

This module contains implementation of :ref:`Flow Control <knowledge-base-can-flow-control>` packet attributes:
 - :ref:`Flow Status <knowledge-base-can-flow-status>`
 - :ref:`Block Size <knowledge-base-can-block-size>`
 - :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>`
"""

__all__ = ["CanFlowStatus", "CanFlowStatusAlias", "CanSTminTranslator", "UnrecognizedSTminWarning"]

from typing import Union, Any
from warnings import warn

from aenum import unique

from uds.utilities import NibbleEnum, ValidatedEnum, TimeMilliseconds, \
    RawByte, RawBytes, RawBytesList, validate_raw_byte
from .addressing_format import CanAddressingFormat


class UnrecognizedSTminWarning(Warning):
    """
    Warning about STmin value that is reserved and therefore not implemented.

    .. note:: If you have a documentation that defines a meaning of :ref:`STmin <knowledge-base-can-st-min>` value
        for which this warning was raised, please create a request in
        `issues management system <https://github.com/mdabrowski1990/uds/issues/new/choose>`_ and provide this
        documentation for us.
    """


@unique
class CanFlowStatus(NibbleEnum, ValidatedEnum):
    """
    Definition of Flow Status values.

    :ref:`Flow Status (FS) <knowledge-base-can-flow-status>` is a 4-bit value that enables controlling
    Consecutive Frames transmission.
    """

    ContinueToSend = 0x0
    """Asks to resume Consecutive Frames transmission."""
    Wait = 0x1
    """Asks to pause Consecutive Frames transmission."""
    Overflow = 0x2
    """Asks to abort transmission of a diagnostic message."""


CanFlowStatusAlias = Union[CanFlowStatus, RawByte]
"""Typing alias that describes :class:`~uds.can.flow_control.CanFlowStatus` member."""


class CanSTminTranslator:
    """
    Helper class that provides STmin values mapping.

    :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>` informs about minimum time gap between
    a transmission of two following Consecutive Frames.
    """

    MAX_STMIN_TIME: TimeMilliseconds = 127
    """Maximal time value of STmin."""

    MIN_VALUE_MS_RANGE: int = 0
    """Minimal value of STmin in milliseconds range (raw value and time value are equal)."""
    MAX_VALUE_MS_RANGE: int = 127
    """Maximal value of STmin in milliseconds range (raw value and time value are equal)."""

    MIN_RAW_VALUE_100US_RANGE: RawByte = 0xF1
    """Minimal raw value of STmin in 100 microseconds range."""
    MAX_RAW_VALUE_100US_RANGE: RawByte = 0xF9
    """Maximal raw value of STmin in 100 microseconds range."""
    MIN_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.1
    """Minimal time value of STmin in 100 microseconds range."""
    MAX_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.9
    """Maximal time value of STmin in 100 microseconds range."""

    _FLOATING_POINT_ACCURACY: int = 8
    """Accuracy of floating point values - when rounding is necessary due to float operation in python."""

    @classmethod
    def decode(cls, raw_value: RawByte) -> TimeMilliseconds:
        """
        Map raw value of STmin into time value.

        .. note:: According to ISO 15765-2, if a raw value of STmin that is not recognized by its recipient,
            then the longest STmin time value (0x7F = 127 ms) shall be used instead.

        :param raw_value: Raw value of STmin.

        :return: STmin time in milliseconds.
        """
        validate_raw_byte(raw_value)
        if cls.MIN_VALUE_MS_RANGE <= raw_value <= cls.MAX_VALUE_MS_RANGE:
            return raw_value
        if cls.MIN_RAW_VALUE_100US_RANGE <= raw_value <= cls.MAX_RAW_VALUE_100US_RANGE:
            return (raw_value - 0xF0) * 0.1
        warn(message=f"STmin 0x{raw_value:X} is not recognized by this version of the package.",
             category=UnrecognizedSTminWarning)
        return cls.MAX_STMIN_TIME

    @classmethod
    def encode(cls, time_value: TimeMilliseconds) -> RawByte:
        """
        Map time value of STmin into raw value.

        :param time_value: STmin time in milliseconds.

        :raise TypeError: Provided value is not time in milliseconds.
        :raise ValueError: Value out of supported range.

        :return: Raw value of STmin.
        """
        if not isinstance(time_value, (int, float)):
            raise TypeError(f"Provided value is not int or float type. Actual type: {type(time_value)}")
        if cls._is_ms_value(time_value):
            return int(time_value)
        if cls._is_100us_value(time_value):
            return int(round(time_value * 10, 0) + 0xF0)
        raise ValueError(f"Provided value is out of valid STmin ranges. Actual value: {time_value}")

    @classmethod
    def is_time_value(cls, value: Any) -> bool:
        """
        Check if provided value is a valid time value of STmin.

        :param value: Value to check.

        :return: True if provided value is a valid time value of STmin, False otherwise.
        """
        if not isinstance(value, (int, float)):
            return False
        return cls._is_ms_value(value) or cls._is_100us_value(value)

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


class FlowControlHandler:
    # TODO

    @classmethod
    def is_flow_control(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def validate_flow_control(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def generate_can_frame_data(cls) -> RawBytesList:
        ...

"""
Implementation specific for Flow Control CAN packets.

This module contains implementation of :ref:`Flow Control <knowledge-base-can-flow-control>` packet attributes:
 - :ref:`Flow Status <knowledge-base-can-flow-status>`
 - :ref:`Block Size <knowledge-base-can-block-size>`
 - :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>`
"""

__all__ = ["CanFlowStatus", "CanFlowStatusAlias", "CanSTminTranslator", "UnrecognizedSTminWarning"]

from typing import Union, Optional, Any
from warnings import warn

from aenum import unique

from uds.utilities import NibbleEnum, ValidatedEnum, TimeMilliseconds, \
    Nibble, RawByte, RawBytes, RawBytesList, validate_raw_byte, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler


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


CanFlowStatusAlias = Union[CanFlowStatus, Nibble]
"""Typing alias that describes :class:`~uds.can.flow_control.CanFlowStatus` member."""


class CanSTminTranslator:
    """
    Helper class that provides STmin values mapping.

    :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>` informs about minimum time gap between
    a transmission of two following Consecutive Frames.
    """

    MAX_STMIN_TIME: TimeMilliseconds = 127
    """Maximal time value (in milliseconds) of STmin."""

    MIN_VALUE_MS_RANGE: int = 0
    """Minimal value of STmin in milliseconds range (raw value and time value in milliseconds are equal)."""
    MAX_VALUE_MS_RANGE: int = 127
    """Maximal value of STmin in milliseconds range (raw value and time value in milliseconds are equal)."""

    MIN_RAW_VALUE_100US_RANGE: RawByte = 0xF1
    """Minimal raw value of STmin in 100 microseconds range."""
    MAX_RAW_VALUE_100US_RANGE: RawByte = 0xF9
    """Maximal raw value of STmin in 100 microseconds range."""
    MIN_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.1
    """Minimal time value (in milliseconds) of STmin in 100 microseconds range."""
    MAX_TIME_VALUE_100US_RANGE: TimeMilliseconds = 0.9
    """Maximal time value (in milliseconds) of STmin in 100 microseconds range."""

    _FLOATING_POINT_ACCURACY: int = 10
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


class CanFlowControlHandler:
    """Helper class that provides utilities for Flow Control CAN Packets."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormatAlias,
                                flow_status: CanFlowStatusAlias,
                                block_size: Optional[RawByte] = None,
                                st_min: Optional[RawByte] = None,
                                dlc: Optional[int] = None,
                                filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                                target_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Create a data field of a CAN frame that carries a valid Flow Control packet.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            Use :meth:`~uds.can.flow_control.FlowControlHandler.create_any_frame_data` to create data bytes
            for a Flow Control with any (also incompatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Flow Control.
        :param flow_status: Value of Flow Status parameter.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param block_size: Value of Block Size parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill the unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: DLC value is too small.

        :return: Raw bytes of CAN frame data for the provided Flow Control packet information.
        """

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormatAlias,
                              flow_status: CanFlowStatusAlias,
                              dlc: int,
                              block_size: Optional[RawByte] = None,
                              st_min: Optional[RawByte] = None,
                              filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                              target_address: Optional[RawByte] = None,
                              address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Create a data field of a CAN frame that carries a Flow Control packet.

        .. note:: You can use this method to create Flow Control data bytes with any (also inconsistent with ISO 15765)
            parameters values.
            It is recommended to use :meth:`~uds.can.flow_control.FlowControlHandler.create_valid_frame_data` to create
            data bytes for a Flow Control with valid (compatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Flow Control.
        :param flow_status: Value of Flow Status parameter.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param block_size: Value of Block Size parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: DLC value is too small.

        :return: Raw bytes of CAN frame data for the provided Flow Control packet information.
        """

    @classmethod
    def is_flow_control(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        """
        Check if provided data bytes encodes a Flow Control packet.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            Only, :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter is checked whether contain
            Flow Control N_PCI value.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries Flow Control, False otherwise.
        """

    @classmethod
    def decode_flow_status(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> CanFlowStatus:
        """
        Extract Flow Status value from Flow Control data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Flow Control CAN packet.

        :return: Flow Status value carried by a considered Flow Control.
        """

    @classmethod
    def decode_block_size(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawByte:
        """
        Extract Block Size value from Flow Control data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Flow Control CAN packet
            with Continue To Send Flow Status.

        :return: Block Size value carried by a considered Flow Control.
        """

    @classmethod
    def decode_st_min(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawByte:
        """
        Extract STmin value from Flow Control data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Flow Control CAN packet
            with Continue To Send Flow Status.

        :return: Separation Time minimum (STmin) value carried by a considered Flow Control.
        """

    @classmethod
    def get_min_dlc(cls, addressing_format: CanAddressingFormatAlias) -> int:
        """
        Get the minimum value of a CAN frame DLC to carry a Flow Control packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.

        :return: The lowest value of DLC that enables to fit in provided Flow Control packet data.
        """

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded Flow Control.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Flow Control CAN packet.
        :raise InconsistentArgumentsError: Provided frame data of a CAN frames does not carry a properly encoded
            Flow Control CAN packet.
        """

"""
Implementation specific for Flow Control CAN packets.

This module contains implementation of :ref:`Flow Control <knowledge-base-can-flow-control>` packet attributes:
 - :ref:`Flow Status <knowledge-base-can-flow-status>`
 - :ref:`Block Size <knowledge-base-can-block-size>`
 - :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>`
"""

__all__ = ["CanFlowStatus", "CanSTminTranslator", "CanFlowControlHandler", "UnrecognizedSTminWarning"]

from typing import Optional
from warnings import warn

from aenum import unique

from uds.utilities import InconsistentArgumentsError, NibbleEnum, ValidatedEnum, TimeMillisecondsAlias, \
    RawBytesAlias, RawBytesListAlias, validate_nibble, validate_raw_byte, validate_raw_bytes
from .addressing_format import CanAddressingFormat
from .addressing_information import CanAddressingInformation
from .frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler


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

    ContinueToSend: "CanFlowStatus" = 0x0  # type: ignore
    """Asks to resume Consecutive Frames transmission."""
    Wait: "CanFlowStatus" = 0x1  # type: ignore  # noqa: F841
    """Asks to pause Consecutive Frames transmission."""
    Overflow: "CanFlowStatus" = 0x2  # type: ignore  # noqa: F841
    """Asks to abort transmission of a diagnostic message."""


class CanSTminTranslator:
    """
    Helper class that provides STmin values mapping.

    :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>` informs about minimum time gap between
    a transmission of two following Consecutive Frames.
    """

    MAX_STMIN_TIME: TimeMillisecondsAlias = 127
    """Maximal time value (in milliseconds) of STmin."""

    MIN_VALUE_MS_RANGE: int = 0
    """Minimal value of STmin in milliseconds range (raw value and time value in milliseconds are equal)."""
    MAX_VALUE_MS_RANGE: int = 127
    """Maximal value of STmin in milliseconds range (raw value and time value in milliseconds are equal)."""

    MIN_RAW_VALUE_100US_RANGE: int = 0xF1
    """Minimal raw value of STmin in 100 microseconds range."""
    MAX_RAW_VALUE_100US_RANGE: int = 0xF9
    """Maximal raw value of STmin in 100 microseconds range."""
    MIN_TIME_VALUE_100US_RANGE: TimeMillisecondsAlias = 0.1
    """Minimal time value (in milliseconds) of STmin in 100 microseconds range."""
    MAX_TIME_VALUE_100US_RANGE: TimeMillisecondsAlias = 0.9
    """Maximal time value (in milliseconds) of STmin in 100 microseconds range."""

    __FLOATING_POINT_ACCURACY: int = 10
    """Accuracy used for floating point values (rounding is necessary due to float operation in python)."""

    @classmethod
    def decode(cls, raw_value: int) -> TimeMillisecondsAlias:
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
    def encode(cls, time_value: TimeMillisecondsAlias) -> int:
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
    def is_time_value(cls, value: TimeMillisecondsAlias) -> bool:
        """
        Check if provided value is a valid time value of STmin.

        :param value: Value to check.

        :return: True if provided value is a valid time value of STmin, False otherwise.
        """
        if not isinstance(value, (int, float)):
            return False
        return cls._is_ms_value(value) or cls._is_100us_value(value)

    @classmethod
    def _is_ms_value(cls, value: TimeMillisecondsAlias) -> bool:
        """
        Check if provided argument is STmin time value in milliseconds.

        :param value: Value to check.

        :return: True if provided valid value of STmin time in milliseconds, False otherwise.
        """
        if not cls.MIN_VALUE_MS_RANGE <= value <= cls.MAX_VALUE_MS_RANGE:
            return False
        return value % 1 == 0

    @classmethod
    def _is_100us_value(cls, value: TimeMillisecondsAlias) -> bool:
        """
        Check if provided argument is STmin time value in 100 microseconds.

        :param value: Value to check.

        :return: True if provided valid value of STmin time in 100 microseconds, False otherwise.
        """
        if not cls.MIN_TIME_VALUE_100US_RANGE <= value <= cls.MAX_TIME_VALUE_100US_RANGE:
            return False
        return round(value % 0.1, cls.__FLOATING_POINT_ACCURACY) in (0, 0.1)


class CanFlowControlHandler:
    """Helper class that provides utilities for Flow Control CAN Packets."""

    FLOW_CONTROL_N_PCI: int = 0x3
    """N_PCI value of Flow Control."""
    FS_BYTES_USED: int = 3
    """Number of CAN Frame data bytes used to carry CAN Packet Type, Flow Status, Block Size and STmin."""
    BS_BYTE_POSITION: int = 1
    """Position of a data byte with :ref:`Block Size <knowledge-base-can-block-size>` parameter."""
    STMIN_BYTE_POSITION: int = 2
    """Position of a data byte with  :ref:`STmin <knowledge-base-can-st-min>` parameter."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormat,
                                flow_status: CanFlowStatus,
                                block_size: Optional[int] = None,
                                st_min: Optional[int] = None,
                                dlc: Optional[int] = None,
                                filler_byte: int = DEFAULT_FILLER_BYTE,
                                target_address: Optional[int] = None,
                                address_extension: Optional[int] = None) -> RawBytesListAlias:
        """
        Create a data field of a CAN frame that carries a valid Flow Control packet.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            Use :meth:`~uds.can.flow_control.FlowControlHandler.create_any_frame_data` to create data bytes
            for a Flow Control with any (also incompatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Flow Control.
        :param flow_status: Value of Flow Status parameter.
        :param block_size: Value of Block Size parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.

            - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
            - int type value - DLC value to set. CAN Data Padding will be used to fill the unused data bytes.

        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Invalid DLC value was provided.

        :return: Raw bytes of CAN frame data for the provided Flow Control packet information.
        """
        validate_raw_byte(filler_byte)
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        frame_dlc = cls.get_min_dlc(addressing_format) if dlc is None else dlc
        frame_data_bytes_number = CanDlcHandler.decode_dlc(frame_dlc)
        fs_data_bytes = cls.__encode_valid_flow_status(flow_status=flow_status,
                                                       block_size=block_size,
                                                       st_min=st_min,
                                                       filler_byte=filler_byte)
        fc_bytes = ai_data_bytes + fs_data_bytes
        if len(fc_bytes) > frame_data_bytes_number:
            raise InconsistentArgumentsError("Provided value of `dlc` is too small.")
        data_bytes_to_pad = frame_data_bytes_number - len(fc_bytes)
        if data_bytes_to_pad > 0:
            if dlc is not None and dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
                raise InconsistentArgumentsError(f"CAN Frame Data Padding shall not be used for CAN frames with "
                                                 f"DLC < {CanDlcHandler.MIN_BASE_UDS_DLC}. Actual value: dlc={dlc}")
            return fc_bytes + data_bytes_to_pad * [filler_byte]
        return fc_bytes

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormat,
                              flow_status: CanFlowStatus,
                              dlc: int,
                              block_size: Optional[int] = None,
                              st_min: Optional[int] = None,
                              filler_byte: int = DEFAULT_FILLER_BYTE,
                              target_address: Optional[int] = None,
                              address_extension: Optional[int] = None) -> RawBytesListAlias:
        """
        Create a data field of a CAN frame that carries a Flow Control packet.

        .. note:: You can use this method to create Flow Control data bytes with any (also inconsistent with ISO 15765)
            parameters values.
            It is recommended to use :meth:`~uds.can.flow_control.FlowControlHandler.create_valid_frame_data` to create
            data bytes for a Flow Control with valid (compatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Flow Control.
        :param flow_status: Value of Flow Status parameter.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            Leave None to not insert this parameter in a Flow Control data bytes.
        :param block_size: Value of Block Size parameter.
            Leave None to not insert this parameter in a Flow Control data bytes.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: DLC value is too small.

        :return: Raw bytes of CAN frame data for the provided Flow Control packet information.
        """
        validate_raw_byte(filler_byte)
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        fs_data_bytes = cls.__encode_any_flow_status(flow_status=flow_status,
                                                     block_size=block_size,
                                                     st_min=st_min)
        fc_bytes = ai_data_bytes + fs_data_bytes
        if len(fc_bytes) > frame_data_bytes_number:
            raise InconsistentArgumentsError("Provided value of `dlc` is too small.")
        data_bytes_to_pad = frame_data_bytes_number - len(fc_bytes)
        if data_bytes_to_pad > 0:
            return fc_bytes + data_bytes_to_pad * [filler_byte]
        return fc_bytes

    @classmethod
    def is_flow_control(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
        """
        Check if provided data bytes encodes a Flow Control packet.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            Only, :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter is checked whether contain
            Flow Control N_PCI value.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries Flow Control, False otherwise.
        """
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return raw_frame_data[ai_bytes_number] >> 4 == cls.FLOW_CONTROL_N_PCI

    @classmethod
    def decode_flow_status(cls,
                           addressing_format: CanAddressingFormat,
                           raw_frame_data: RawBytesAlias) -> CanFlowStatus:
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
        if not cls.is_flow_control(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError(f"Provided `raw_frame_data` value does not carry a Flow Control packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data}")
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return CanFlowStatus(raw_frame_data[ai_bytes_number] & 0xF)

    @classmethod
    def decode_block_size(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
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
        flow_status = cls.decode_flow_status(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        if flow_status != CanFlowStatus.ContinueToSend:
            raise ValueError(f"Provided `raw_frame_data` value does not carry a Flow Control packet with "
                             f"ContinueToSend Flow Status. Actual values: addressing_format={addressing_format}, "
                             f"raw_frame_data={raw_frame_data}, flow_status={flow_status}")
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return raw_frame_data[ai_data_bytes_number + cls.BS_BYTE_POSITION]

    @classmethod
    def decode_st_min(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
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
        flow_status = cls.decode_flow_status(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        if flow_status != CanFlowStatus.ContinueToSend:
            raise ValueError(f"Provided `raw_frame_data` value does not carry a Flow Control packet with "
                             f"ContinueToSend Flow Status. Actual values: addressing_format={addressing_format}, "
                             f"raw_frame_data={raw_frame_data}, flow_status={flow_status}")
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return raw_frame_data[ai_data_bytes_number + cls.STMIN_BYTE_POSITION]

    @classmethod
    def get_min_dlc(cls, addressing_format: CanAddressingFormat) -> int:
        """
        Get the minimum value of a CAN frame DLC to carry a Flow Control packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.

        :return: The lowest value of DLC that enables to fit in provided Flow Control packet data.
        """
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return CanDlcHandler.get_min_dlc(ai_data_bytes_number + cls.FS_BYTES_USED)

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded Flow Control.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a properly encoded Flow Control
            CAN packet.
        """
        validate_raw_bytes(raw_frame_data)
        cls.decode_flow_status(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        min_dlc = cls.get_min_dlc(addressing_format=addressing_format)
        dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
        if min_dlc > dlc:
            raise ValueError("Provided `raw_frame_data` is too short.")
        if dlc < CanDlcHandler.MIN_BASE_UDS_DLC and dlc != min_dlc:
            raise ValueError("Provided `raw_frame_data` has improper length (incorrect Data Length Optimization).")

    @classmethod
    def __encode_valid_flow_status(cls,
                                   flow_status: CanFlowStatus,
                                   block_size: Optional[int] = None,
                                   st_min: Optional[int] = None,
                                   filler_byte: int = DEFAULT_FILLER_BYTE) -> RawBytesListAlias:
        """
        Create Flow Control data bytes with CAN Packet Type and Flow Status, Block Size and STmin parameters.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.

        :param flow_status: Value of Flow Status parameter.
        :param block_size: Value of Block Size parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            This parameter is only required with ContinueToSend Flow Status, leave None otherwise.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.

        :return: Flow Control data bytes with CAN Packet Type and Flow Status, Block Size and STmin parameters.
        """
        CanFlowStatus.validate_member(flow_status)
        if flow_status == CanFlowStatus.ContinueToSend:
            validate_raw_byte(block_size)  # type: ignore
            validate_raw_byte(st_min)  # type: ignore
        else:
            if block_size is not None:
                validate_raw_byte(block_size)
            if st_min is not None:
                validate_raw_byte(st_min)
        return [(cls.FLOW_CONTROL_N_PCI << 4) ^ flow_status,
                block_size if block_size is not None else filler_byte,
                st_min if st_min is not None else filler_byte]

    @classmethod
    def __encode_any_flow_status(cls,
                                 flow_status: int,
                                 block_size: Optional[int] = None,
                                 st_min: Optional[int] = None) -> RawBytesListAlias:
        """
        Create Flow Control data bytes with CAN Packet Type and Flow Status, Block Size and STmin parameters.

        .. note:: This method can be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

        :param flow_status: Value of Flow Status parameter.
        :param block_size: Value of Block Size parameter.
            Leave None to skip the Block Size byte in the output.
        :param st_min: Value of Separation Time minimum (STmin) parameter.
            Leave None to skip the STmin byte in the output.

        :return: Flow Control data bytes with CAN Packet Type and Flow Status, Block Size and STmin parameters.
            Some of the parameters might be missing if certain arguments were provided.
        """
        validate_nibble(flow_status)
        output = [(cls.FLOW_CONTROL_N_PCI << 4) ^ flow_status]
        if block_size is not None:
            validate_raw_byte(block_size)
            output.append(block_size)
        if st_min is not None:
            validate_raw_byte(st_min)
            output.append(st_min)
        return output

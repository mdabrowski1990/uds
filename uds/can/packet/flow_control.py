"""
Implementation specific for Flow Control CAN packets.

This module contains implementation of :ref:`Flow Control CAN packet <knowledge-base-can-flow-control>` attributes:
 - :ref:`Flow Status <knowledge-base-can-flow-status>`
 - :ref:`Block Size <knowledge-base-can-block-size>`
 - :ref:`Separation Time minimum (STmin) <knowledge-base-can-st-min>`
"""

__all__ = ["FLOW_CONTROL_N_PCI", "FS_BYTES_USED", "BS_BYTE_POSITION", "ST_MIN_BYTE_POSITION",
           "CanFlowStatus", "CanSTminTranslator", "UnrecognizedSTminWarning",
           "AbstractFlowControlParametersGenerator", "DefaultFlowControlParametersGenerator",
           "FlowControlParametersAlias",
           "is_flow_control", "validate_flow_control_data",
           "create_flow_control_data", "generate_flow_control_data",
           "extract_flow_status", "extract_block_size", "extract_st_min",
           "get_flow_control_min_dlc",
           "encode_flow_status", "generate_flow_status"]

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, Tuple
from warnings import warn

from aenum import unique

from uds.utilities import (
    InconsistencyError,
    NibbleEnum,
    RawBytesAlias,
    TimeMillisecondsAlias,
    ValidatedEnum,
    validate_nibble,
    validate_raw_byte,
    validate_raw_bytes,
)

from ..addressing import CanAddressingFormat, CanAddressingInformation
from ..frame import DEFAULT_FILLER_BYTE, CanDlcHandler

FLOW_CONTROL_N_PCI: int = 0x3
"""N_PCI value of Flow Control."""

FS_BYTES_USED: int = 3
"""Number of CAN Frame data bytes used to carry CAN Packet Type, Flow Status, Block Size and STmin."""
BS_BYTE_POSITION: int = 1
"""Position of a data byte with :ref:`Block Size <knowledge-base-can-block-size>` parameter."""
ST_MIN_BYTE_POSITION: int = 2
"""Position of a data byte with  :ref:`STmin <knowledge-base-can-st-min>` parameter."""


class UnrecognizedSTminWarning(Warning):
    """Warning about STmin value that is reserved for future definition in ISO 15765 and therefore not implemented."""


@unique
class CanFlowStatus(ValidatedEnum, NibbleEnum):
    """
    Definition of Flow Status values.

    :ref:`Flow Status (FS) <knowledge-base-can-flow-status>` is a 4-bit value that enables controlling
    Consecutive Frames transmission.
    """

    ContinueToSend: "CanFlowStatus" = 0x0  # type: ignore
    """Asks to resume Consecutive Frames transmission."""
    Wait: "CanFlowStatus" = 0x1  # type: ignore
    """Asks to pause Consecutive Frames transmission."""
    Overflow: "CanFlowStatus" = 0x2  # type: ignore
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

        :raise TypeError: Provided value is not int or float type.
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


def is_flow_control(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
    """
    Check if provided data bytes contain a Flow Control packet.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        It only checks :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter for Flow Control N_PCI value.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to check.

    :return: True if provided data bytes carries Flow Control, False otherwise.
    """
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return raw_frame_data[ai_data_bytes_number] >> 4 == FLOW_CONTROL_N_PCI


def validate_flow_control_data(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
    """
    Validate whether data field of a CAN Packet carries a properly encoded Flow Control.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to validate.

    :raise ValueError: The value of N_PCI in provided data is not Flow Control N_PCI.
    :raise InconsistencyError: Provided data does not carry all Flow Control parameters.
    """
    validate_raw_bytes(raw_frame_data, allow_empty=False)
    if not is_flow_control(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
        raise ValueError("Provided `raw_frame_data` value does not carry a Flow Control packet.")
    extract_flow_status(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
    min_dlc = get_flow_control_min_dlc(addressing_format=addressing_format)
    dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
    if min_dlc > dlc:
        raise InconsistencyError("Provided `raw_frame_data` is too short.")
    if dlc < CanDlcHandler.MIN_BASE_UDS_DLC and dlc != min_dlc:
        raise InconsistencyError("Data padding was used for CAN frame with "
                                 f"DLC lesser than {CanDlcHandler.MIN_BASE_UDS_DLC}. Actual value: DLC={dlc}.")


def create_flow_control_data(addressing_format: CanAddressingFormat,
                             flow_status: CanFlowStatus,
                             block_size: Optional[int] = None,
                             st_min: Optional[int] = None,
                             dlc: Optional[int] = None,
                             filler_byte: int = DEFAULT_FILLER_BYTE,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> bytearray:
    """
    Create a data field of a CAN frame that carries a valid Flow Control packet.

    .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
        Use :func:`~uds.can.packet.flow_control.generate_flow_control_data` to generate data bytes with any (also
        incompatible with ISO 15765) parameters values.

    :param addressing_format: CAN addressing format used.
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
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Target Address parameter.
    :param address_extension: Address Extension value carried by this CAN packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Address Extension parameter.

    :raise InconsistencyError: Invalid DLC value was provided.

    :return: Raw data bytes of a CAN frame.
    """
    validate_raw_byte(filler_byte)
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    frame_dlc = get_flow_control_min_dlc(addressing_format) if dlc is None else dlc
    frame_data_bytes_number = CanDlcHandler.decode_dlc(frame_dlc)
    fs_data_bytes = encode_flow_status(flow_status=flow_status)
    fc_bytes = ai_data_bytes + fs_data_bytes
    if flow_status == CanFlowStatus.ContinueToSend or block_size is not None:
        validate_raw_byte(block_size)  # type: ignore
        fc_bytes += bytearray([block_size])  # type: ignore
    else:
        fc_bytes += bytearray([filler_byte])
    if flow_status == CanFlowStatus.ContinueToSend or st_min is not None:
        validate_raw_byte(st_min)  # type: ignore
        fc_bytes += bytearray([st_min])  # type: ignore
    else:
        fc_bytes += bytearray([filler_byte])
    if len(fc_bytes) > frame_data_bytes_number:
        raise InconsistencyError("Provided value of `dlc` is too small.")
    data_bytes_to_pad = frame_data_bytes_number - len(fc_bytes)
    if data_bytes_to_pad > 0:
        if dlc is not None and dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise InconsistencyError("CAN Frame Data Padding shall not be used for CAN frames with "
                                     f"DLC < {CanDlcHandler.MIN_BASE_UDS_DLC}. Actual value: DLC={dlc}.")
    return fc_bytes + data_bytes_to_pad * bytearray([filler_byte])


def generate_flow_control_data(addressing_format: CanAddressingFormat,
                               flow_status: int,
                               dlc: int,
                               block_size: Optional[int] = None,
                               st_min: Optional[int] = None,
                               filler_byte: int = DEFAULT_FILLER_BYTE,
                               target_address: Optional[int] = None,
                               address_extension: Optional[int] = None) -> bytearray:
    """
    Generate CAN frame data field that carries any combination of Flow Control packet data parameters.

    .. note:: Crosscheck of provided values is not performed so you might use this function to create data fields
        that are not compatible with Diagnostic on CAN standard (ISO 15765).

    :param addressing_format: CAN addressing format used.
    :param flow_status: Value of Flow Status parameter.
    :param dlc: DLC value of a CAN frame.
    :param block_size: Value of Block Size parameter.
        Leave None to skip this parameter in a Flow Control data bytes.
    :param st_min: Value of Separation Time minimum (STmin) parameter.
        Leave None to skip this parameter in a Flow Control data bytes.
    :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
    :param target_address: Target Address value carried by this CAN Packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Target Address parameter.
    :param address_extension: Address Extension value carried by this CAN packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Address Extension parameter.

    :raise InconsistencyError: Provided DLC value is too small.

    :return: Raw data bytes of a CAN frame.
    """
    validate_raw_byte(filler_byte)
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
    fs_data_bytes = generate_flow_status(flow_status=flow_status)
    fc_bytes = ai_data_bytes + fs_data_bytes
    if block_size is not None:
        validate_raw_byte(block_size)
        fc_bytes += bytearray([block_size])
    if st_min is not None:
        validate_raw_byte(st_min)
        fc_bytes += bytearray([st_min])
    if len(fc_bytes) > frame_data_bytes_number:
        raise InconsistencyError("Provided value of `dlc` is too small to fit all parameters.")
    data_bytes_to_pad = frame_data_bytes_number - len(fc_bytes)
    return fc_bytes + data_bytes_to_pad * bytearray([filler_byte])


def extract_flow_status(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> CanFlowStatus:
    """
    Extract Flow Status value from Flow Control data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :return: Flow Status value carried by the provided Flow Control data.
    """
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return CanFlowStatus(raw_frame_data[ai_data_bytes_number] & 0xF)


def extract_block_size(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
    """
    Extract Block Size value from Flow Control data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :return: Block Size value carried by the provided Flow Control data.
    """
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return raw_frame_data[ai_data_bytes_number + BS_BYTE_POSITION]


def extract_st_min(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
    """
    Extract STmin value from Flow Control data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :return: Separation Time minimum (STmin) value carried by the provided Flow Control data.
    """
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return raw_frame_data[ai_data_bytes_number + ST_MIN_BYTE_POSITION]


def get_flow_control_min_dlc(addressing_format: CanAddressingFormat) -> int:
    """
    Get the minimum value of a CAN frame DLC to carry a Flow Control packet.

    :param addressing_format: CAN addressing format used.

    :return: The lowest value of DLC for a Flow Control.
    """
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return CanDlcHandler.get_min_dlc(ai_data_bytes_number + FS_BYTES_USED)


def encode_flow_status(flow_status: CanFlowStatus) -> bytearray:
    """
    Create valid Flow Control data bytes that contain Flow Status and N_PCI values.

    :param flow_status: Value of Flow Status parameter.

    :return: Flow Control data bytes containing CAN Packet Type and Flow Status parameters.
    """
    CanFlowStatus.validate_member(flow_status)
    return generate_flow_status(flow_status)


def generate_flow_status(flow_status: int) -> bytearray:
    """
    Create Flow Control bytes containing Flow Status and N_PCI values.

    .. note:: This method can be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

    :param flow_status: Value of Flow Status parameter.

    :return: Flow Control data bytes containing CAN Packet Type and Flow Status parameters.
    """
    validate_nibble(flow_status)
    return bytearray([(FLOW_CONTROL_N_PCI << 4) + flow_status])


FlowControlParametersAlias = Tuple[CanFlowStatus, Optional[int], Optional[int]]
"""Alias of :ref:`Flow Control <knowledge-base-can-flow-control>` parameters which contain:
- :ref:`Flow Status <knowledge-base-can-flow-status>`
- :ref:`Block Size <knowledge-base-can-block-size>`
- :ref:`Separation Time minimum <knowledge-base-can-st-min>`"""


class AbstractFlowControlParametersGenerator(ABC):
    """Definition of Flow Control parameters generator."""

    def __iter__(self) -> "AbstractFlowControlParametersGenerator":
        """Get iterator object - called on each First Frame reception."""
        return self

    @abstractmethod
    def __next__(self) -> FlowControlParametersAlias:
        """
        Generate next set of Flow Control parameters - called on each Flow Control message building.

        :return: Tuple with values of Flow Control parameters (Flow Status, Block Size, ST min).
        """


class DefaultFlowControlParametersGenerator(AbstractFlowControlParametersGenerator):
    """
    Default (recommended to use) Flow Control parameters generator.

    Every generated Flow Control parameters will contain the same (valid) values.
    """

    def __init__(self, block_size: int = 0, st_min: int = 0, wait_count: int = 0, repeat_wait: bool = False) -> None:
        """
        Set values of Block Size and Separation Time minimum parameters to use.

        :param block_size: Value of :ref:`Block Size <knowledge-base-can-block-size>` parameter to use.
        :param st_min: Value of :ref:`Separation Time minimum <knowledge-base-can-st-min>` parameter to use.
        :param wait_count: Number of Flow Control packets to send with
            :ref:`Flow Status <knowledge-base-can-flow-status>` equal 1 (wait).
        :param repeat_wait: How to send Flow Control packets with WAIT Flow Status:

            - True - send them before every Flow Control packet with Flow Status=0 (continue to send)
            - False - send them only once before the first Flow Control packet with Flow Status=0 (continue to send)
        """
        self.block_size = block_size
        self.st_min = st_min
        self.wait_count = wait_count
        self.repeat_wait = repeat_wait
        self._remaining_wait: Optional[int] = None

    def __iter__(self) -> "DefaultFlowControlParametersGenerator":
        """Get iterator object."""
        iterator = deepcopy(self)
        if iterator.wait_count > 0:
            iterator._remaining_wait = iterator.wait_count
        else:
            iterator._remaining_wait = None
        return iterator

    def __next__(self) -> FlowControlParametersAlias:
        """
        Generate next set of Flow Control parameters.

        :return: Tuple with values of Flow Control parameters:
            - :ref:`Flow Status <knowledge-base-can-flow-status>`
            - :ref:`Block Size <knowledge-base-can-block-size>`
            - :ref:`Separation Time minimum <knowledge-base-can-st-min>`
        """
        if self._remaining_wait is None:
            return CanFlowStatus.ContinueToSend, self.block_size, self.st_min
        if self._remaining_wait == 0:
            if self.repeat_wait:
                self._remaining_wait = self.wait_count
            return CanFlowStatus.ContinueToSend, self.block_size, self.st_min
        self._remaining_wait -= 1
        return CanFlowStatus.Wait, None, None

    @property
    def block_size(self) -> int:
        """Value of :ref:`Block Size <knowledge-base-can-block-size>` parameter."""
        return self.__block_size

    @block_size.setter
    def block_size(self, value: int) -> None:
        """
        Set value of :ref:`Block Size <knowledge-base-can-block-size>` parameter.

        :param value: Value to set.
        """
        validate_raw_byte(value)
        self.__block_size = value

    @property
    def st_min(self) -> int:
        """Value of :ref:`Separation Time minimum <knowledge-base-can-st-min>` parameter."""
        return self.__st_min

    @st_min.setter
    def st_min(self, value: int) -> None:
        """
        Set value of :ref:`Separation Time minimum <knowledge-base-can-st-min>` parameter.

        :param value: Value to set.
        """
        validate_raw_byte(value)
        self.__st_min = value

    @property
    def wait_count(self) -> int:
        """Get number of Flow Control packets to send with WAIT :ref:`Flow Status <knowledge-base-can-flow-status>`."""
        return self.__wait_count

    @wait_count.setter
    def wait_count(self, value: int) -> None:
        """
        Set number of Flow Control packets to send with WAIT :ref:`Flow Status <knowledge-base-can-flow-status>`.

        :param value: Value to set.
        """
        if not isinstance(value, int):
            raise TypeError(f"Provided value is not int type. Actual type: {type(value)}.")
        if value < 0:
            raise ValueError(f"Provided value is les than 0. Actual value: {value}")
        self.__wait_count = value

    @property
    def repeat_wait(self) -> bool:
        """
        Flag informing how to send Flow Control packets with WAIT Flow Status.

        - True - send them before every Flow Control packet with Flow Status=0 (continue to send)
        - False - send them only once before the first Flow Control packet with Flow Status=0 (continue to send)
        """
        return self.__repeat_wait

    @repeat_wait.setter
    def repeat_wait(self, value: bool) -> None:
        """
        Set flag informing how to send Flow Control packets with WAIT Flow Status.

        - True - send them before every Flow Control packet with Flow Status=0 (continue to send)
        - False - send them only once before the first Flow Control packet with Flow Status=0 (continue to send)
        """
        self.__repeat_wait = bool(value)

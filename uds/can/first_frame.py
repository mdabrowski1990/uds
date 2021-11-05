"""
Implementation specific for First Frame CAN packets.

This module contains implementation specific for :ref:`First Frame <knowledge-base-can-first-frame>` packets - that
includes :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` parameter.
"""

__all__ = ["CanFirstFrameHandler"]

from typing import Optional

from uds.utilities import Nibble, RawByte, RawBytes, RawBytesList, int_to_bytes_list, \
    validate_raw_bytes, validate_raw_byte, validate_nibble, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler
from .packet_type import CanPacketType
from .single_frame import CanSingleFrameHandler


class CanFirstFrameHandler:
    """Helper class that provides utilities for First Frame CAN Packets."""

    MAX_SHORT_FF_DL_VALUE: int = 0xFFF
    """Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` for which
    short format of FF_DL is used."""
    MAX_LONG_FF_DL_VALUE: int = 0xFFFFFFFF
    """Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>`."""
    SHORT_FF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` and 
    :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` values in 
    :ref:`First Frame <knowledge-base-can-first-frame>` when FF_DL <= 4095."""
    LONG_FF_DL_BYTES_USED: int = 6
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` and 
    :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` values in 
    :ref:`First Frame <knowledge-base-can-first-frame>` when FF_DL > 4095."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormatAlias,
                                payload: RawBytes,
                                dlc: int,
                                ff_dl: int,
                                target_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> RawBytesList:
        ...

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormatAlias,
                              payload: RawBytes,
                              dlc: int,
                              ff_dl: int,
                              long_ff_dl_format: bool = False,
                              target_address: Optional[RawByte] = None,
                              address_extension: Optional[RawByte] = None) -> RawBytesList:
        ...

    @classmethod
    def is_first_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        """
        Check if provided data bytes encodes a First Frame packet.

        .. warning:: The method does not validate the content (e.g. FF_DL parameter) of the packet.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries First Frame, False otherwise.
        """
        ff_dl_data_bytes = cls.__extract_ff_dl_data_bytes(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        return ff_dl_data_bytes[0] >> 4 == CanPacketType.FIRST_FRAME.value

    @classmethod
    def decode_payload(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawBytesList:
        ...

    @classmethod
    def decode_ff_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        ...

    @classmethod
    def get_payload_size(cls, addressing_format: CanAddressingFormatAlias, dlc: int) -> int:
        ...

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded First Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a First Frame CAN packet.
        """
        if not cls.is_first_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError(f"Provided `raw_frame_data` value does not carry a First Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data}")
        # TODO: check FF_DL

    @classmethod
    def validate_ff_dl(cls,
                       ff_dl: int,
                       long_ff_dl_format: Optional[bool] = None,
                       dlc: Optional[int] = None,
                       addressing_format: Optional[CanAddressingFormatAlias] = None) -> None:
        """
        Validate a value of First Frame Data Length.

        :param ff_dl: First Frame Data Length value to validate.
        :param long_ff_dl_format: Information whether long or short format of First Frame Data Length is used.
            Possible values:
             - None - do not perform compatibility check with the FF_DL format
             - True - perform compatibility check with long FF_DL format
             - False - perform compatibility check with short FF_DL format
        :param dlc: Value of DLC to use for First Frame Data Length value validation.
            Leave None if you do not want to validate whether First Frame shall be used in this case.
        :param addressing_format: Value of CAN Addressing Format to use for First Frame Data Length value validation.
            Leave None if you do not want to validate whether First Frame shall be used in this case.

        :raise TypeError: Provided value of First Frame Data Length is not integer.
        :raise ValueError: Provided value of First Frame Data Length is out of range.
        :raise InconsistentArgumentsError: Single Frame shall be used instead of First Frame to transmit provided
            number of payload bytes represented by FF_DL value.
        """
        if not isinstance(ff_dl, int):
            raise TypeError(f"Provided value of First Frame Data Length is not integer. Actual type: {type(ff_dl)}")
        if not 0 < ff_dl <= cls.MAX_LONG_FF_DL_VALUE:
            raise ValueError(f"Provided value of First Frame Data Length is out of range. "
                             f"Expected: 0 <= ff_dl <= {cls.MAX_LONG_FF_DL_VALUE}. Actual value: {ff_dl}")
        if dlc is not None and addressing_format is not None:
            max_sf_dl = CanSingleFrameHandler.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
            if ff_dl <= max_sf_dl:
                raise InconsistentArgumentsError(f"Single Frame shall be used instead of First Frame to carry payload "
                                                 f"consisting of {ff_dl} data bytes.")
        if long_ff_dl_format is not None:
            if (long_ff_dl_format and ff_dl <= cls.MAX_SHORT_FF_DL_VALUE) \
                    or (not long_ff_dl_format and ff_dl > cls.MAX_SHORT_FF_DL_VALUE):
                raise InconsistentArgumentsError(f"Provided value of First Frame Data Length is not compatible with "
                                                 f"the format used. Actual values: ff_dl={ff_dl}, "
                                                 f"long_ff_dl_format={long_ff_dl_format}")

    @classmethod
    def __extract_ff_dl_data_bytes(cls,
                                   addressing_format: CanAddressingFormat,
                                   raw_frame_data: RawBytes) -> RawBytesList:
        """
        Extract data bytes that carries CAN Packet Type and First Frame Data Length parameters.

        .. warning:: This method does not check whether provided `raw_frame_data` actually contains First Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Extracted data bytes with CAN Packet Type and First Frame Data Length parameters.
        """
        ai_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        ff_dl_short = list(raw_frame_data[ai_bytes_number:][:cls.SHORT_FF_DL_BYTES_USED])
        if ff_dl_short[0] & 0xF != 0 or ff_dl_short[1] != 0:
            return ff_dl_short
        ff_dl_long = list(raw_frame_data[ai_bytes_number:][:cls.LONG_FF_DL_BYTES_USED])
        return ff_dl_long

    @classmethod
    def __encode_valid_ff_dl(cls, ff_dl: int) -> RawBytesList:
        """
        Create First Frame data bytes with CAN Packet Type and First Frame Data Length parameters.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            First Frame Data Length value validation (whether it is too low according to ISO 15765) is not performed
            though.

        :param ff_dl: Value to put into a slot of First Frame Data Length.

        :return: First Frame data bytes containing CAN Packet Type and First Frame Data Length parameters.
        """
        return cls.__encode_any_ff_dl(ff_dl=ff_dl, long_ff_dl_format=ff_dl > cls.MAX_SHORT_FF_DL_VALUE)

    @classmethod
    def __encode_any_ff_dl(cls, ff_dl: int, long_ff_dl_format: bool = False) -> RawBytesList:
        """
        Create First Frame data bytes with CAN Packet Type and First Frame Data Length parameters.

        .. note:: This method can be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

        :param ff_dl: Value to put into a slot of First Frame Data Length.
        :param long_ff_dl_format: Information whether to use long or short format of First Frame Data Length.

        :raise ValueError: Provided First Frame Data Length value is out of the parameter values range.
        :raise InconsistentArgumentsError: Provided First Frame Data Length value cannot fit into the short format.

        :return: First Frame data bytes containing CAN Packet Type and First Frame Data Length parameters.
        """
        cls.validate_ff_dl(ff_dl=ff_dl)
        if long_ff_dl_format:
            ff_dl_bytes = int_to_bytes_list(int_value=ff_dl, list_size=cls.LONG_FF_DL_BYTES_USED)
            ff_dl_bytes[0] ^= (CanPacketType.FIRST_FRAME.value << 4)
            return ff_dl_bytes
        if ff_dl > cls.MAX_SHORT_FF_DL_VALUE:
            raise InconsistentArgumentsError(f"Provided value of First Frame Data Length is too big for the short "
                                             f"FF_DL format. Use lower FF_DL value or change to long format. "
                                             f"Actual value: {ff_dl}")
        ff_dl_bytes = int_to_bytes_list(int_value=ff_dl, list_size=cls.SHORT_FF_DL_BYTES_USED)
        ff_dl_bytes[0] ^= (CanPacketType.FIRST_FRAME.value << 4)
        return ff_dl_bytes

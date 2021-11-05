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
        return (ff_dl_data_bytes[0] >> 4) == CanPacketType.FIRST_FRAME.value

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
        ...

    @classmethod
    def validate_ff_dl(cls, ff_dl: int, dlc: int, addressing_format: CanAddressingFormatAlias) -> None:
        ...

    @classmethod
    def __extract_ff_dl_data_bytes(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawBytesList:
        ...

    @classmethod
    def __encode_valid_ff_dl(cls, ff_dl: int) -> RawBytesList:
        ...

    @classmethod
    def __encode_any_ff_dl(cls, ff_dl: int, long_ff_dl_format: bool = False) -> RawBytesList:
        """
        Create First Frame data bytes with CAN Packet Type and First Frame Data Length parameters.

        .. note:: You can use this method to create any (also invalid) value of First Frame Data Length data bytes.
            Use :meth:`~uds.can.first_frame.CanFirstFrameHandler.__encode_valid_ff_dl` to create a valid
            (compatible with ISO 15765 - Diagnostic on CAN) output.

        :param ff_dl: TODO
        :param long_ff_dl_format: TODO

        :return: TODO
        """
        if not 0 <= ff_dl <= cls.MAX_LONG_FF_DL_VALUE:
            raise ValueError(f"Provided value of First Frame Data Length is out of range. "
                             f"Expected: 0 <= ff_dl <= {cls.MAX_LONG_FF_DL_VALUE}. Actual value: {ff_dl}")
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

"""
Implementation specific for First Frame CAN packets.

This module contains implementation specific for :ref:`First Frame <knowledge-base-can-first-frame>` packets - that
includes :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` parameter.
"""

__all__ = ["CanFirstFrameHandler"]

from typing import Optional

from uds.utilities import Nibble, RawByte, RawBytes, RawBytesList, \
    validate_raw_bytes, validate_raw_byte, validate_nibble, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler
from .packet_type import CanPacketType


class CanFirstFrameHandler:
    """Helper class that provides utilities for First Frame CAN Packets."""

    @classmethod
    def create_frame_data(cls, *,
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
                              use_long_ff_dl_format: bool = False,
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
    def __encode_ff_dl(cls, ff_dl: int) -> RawBytesList:
        ...

    @staticmethod
    def __create_ff_dl_data_bytes(ff_dl: int, use_long_ff_dl_format: bool = False) -> RawBytesList:
        ...

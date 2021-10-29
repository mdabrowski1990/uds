"""
Implementation specific for Single Frame CAN packets.

This module contains implementation of :ref:`Single Frame <knowledge-base-can-single-frame>` packet attributes:
 - :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>`
"""

__all__ = ["SingleFrameHandler"]

from uds.utilities import RawBytes, RawBytesList
from .addressing_format import CanAddressingFormat


class SingleFrameDataLengthHandler:
    # TODO

    MAX_DLC_VALUE_SHORT_SF_DL: int = 8
    """Maximum value of DLC for which short
    :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>` format is used."""
    SHORT_SF_DL_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` values in 
    :ref:`Single Frame <knowledge-base-can-single-frame>` packets with DLC <= 8."""
    LONG_SF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` values in 
    :ref:`Single Frame <knowledge-base-can-single-frame>` packets with DLC > 8."""

    @classmethod
    def encode_sf_dl(cls, payload_bytes_number: int, dlc: int) -> RawBytesList:
        ...

    @classmethod
    def decode_sf_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        ...

    @classmethod
    def validate_sf_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        ...


class SingleFrameHandler:
    """
    Helper class that provides utilities for Single Frame.

    :ref:`Single Frame <knowledge-base-can-single-frame>` uses
    :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` to inform about payload bytes
    number of a carried diagnostic message.
    """

    @classmethod
    def is_single_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def validate_single_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def generate_can_frame_data(cls) -> RawBytesList:
        ...

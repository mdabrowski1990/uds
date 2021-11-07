"""
Implementation specific for Consecutive Frame CAN packets.

This module contains implementation specific for :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
packets - that includes :ref:`Sequence Number (SN) <knowledge-base-can-sequence-number>` parameter.
"""

__all__ = ["CanConsecutiveFrameHandler"]

from typing import Optional

from uds.utilities import Nibble, RawByte, RawBytes, RawBytesList, \
    validate_raw_bytes, validate_raw_byte, validate_nibble, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler
from .packet_type import CanPacketType


class CanConsecutiveFrameHandler:
    """Helper class that provides utilities for Consecutive Frame CAN Packets."""

    SN_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>`
    and :ref:`Sequence Number <knowledge-base-can-sequence-number>` values in
    :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormatAlias,
                                payload: RawBytes,
                                sequence_number: Nibble,
                                dlc: Optional[int] = None,
                                filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                                target_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Create a data field of a CAN frame that carries a valid Consecutive Frame packet.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            Use :meth:`~uds.can.consecutive_frame.CanConsecutiveFrameHandler.create_any_frame_data` to create data bytes
            for a Consecutive Frame with any (also incompatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Consecutive Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param sequence_number: Value of Sequence Number parameter.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill the unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        # :raise InconsistentArgumentsError: Provided `payload` contains too many bytes to fit it into a Consecutive Frame
        #     data field.

        :return: Raw bytes of CAN frame data for the provided Single Frame packet information.
        """

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormatAlias,
                              payload: RawBytes,
                              sequence_number: Nibble,
                              dlc: int,
                              filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                              target_address: Optional[RawByte] = None,
                              address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Create a data field of a CAN frame that carries a Consecutive Frame packet.

        .. note:: You can use this method to create Consecutive Frame data bytes with any (also inconsistent
            with ISO 15765) parameters values.
            It is recommended to use
            :meth:`~uds.can.consecutive_frame.CanConsecutiveFrameHandler.create_valid_frame_data` to create data bytes
            for a Consecutive Frame with valid (compatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Single Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param sequence_number: Value of Sequence Number parameter.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :return: Raw bytes of CAN frame data for the provided Single Frame packet information.
        """

    @classmethod
    def is_consecutive_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def decode_payload(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawBytesList:
        ...

    @classmethod
    def decode_sn(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        ...

    @classmethod
    def get_min_dlc(cls, addressing_format: CanAddressingFormatAlias, payload_length: int) -> int:
        ...

    @classmethod
    def get_max_payload_size(cls,
                             addressing_format: Optional[CanAddressingFormatAlias] = None,
                             dlc: Optional[int] = None) -> int:
        ...

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        ...

    @classmethod
    def __extract_sn_data_bytes(cls,
                                addressing_format: CanAddressingFormat,
                                raw_frame_data: RawBytes) -> RawBytesList:
        ...

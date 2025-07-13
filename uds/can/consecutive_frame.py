"""
Implementation specific for Consecutive Frame CAN packets.

This module contains implementation specific for :ref:`Consecutive Frame <knowledge-base-addressing-consecutive-frame>`
packets - that includes :ref:`Sequence Number (SN) <knowledge-base-addressing-sequence-number>` parameter.
"""

__all__ = ["CanConsecutiveFrameHandler"]

from typing import Optional

from uds.utilities import (
    InconsistentArgumentsError,
    RawBytesAlias,
    validate_nibble,
    validate_raw_byte,
    validate_raw_bytes,
)

from uds.can.addressing import CanAddressingFormat
from uds.can.addressing.addressing_information import CanAddressingInformation
from .frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler


class CanConsecutiveFrameHandler:
    """Helper class that provides utilities for Consecutive Frame CAN Packets."""

    CONSECUTIVE_FRAME_N_PCI: int = 0x2
    """Consecutive Frame N_PCI value."""
    SN_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry CAN Packet Type and Sequence Number in Consecutive Frame."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormat,
                                payload: RawBytesAlias,
                                sequence_number: int,
                                dlc: Optional[int] = None,
                                filler_byte: int = DEFAULT_FILLER_BYTE,
                                target_address: Optional[int] = None,
                                address_extension: Optional[int] = None) -> bytearray:
        """
        Create a data field of a CAN frame that carries a valid Consecutive Frame packet.

        .. note:: This method addressing only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            Use :meth:`~uds.addressing.consecutive_frame.CanConsecutiveFrameHandler.create_any_frame_data` to create data bytes
            for a Consecutive Frame with any (also incompatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Consecutive Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param sequence_number: Value of Sequence Number parameter.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.

            - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
            - int type value - DLC value to set. CAN Data Padding will be used to fill the unused data bytes.

        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Provided `payload` contains invalid number of bytes to fit it into
            a properly defined Consecutive Frame data field.

        :return: Raw bytes of CAN frame data for the provided Consecutive Frame packet information.
        """
        validate_raw_byte(filler_byte)
        validate_raw_bytes(payload, allow_empty=False)
        frame_dlc = cls.get_min_dlc(addressing_format=addressing_format, payload_length=len(payload)) \
            if dlc is None else dlc
        frame_data_bytes_number = CanDlcHandler.decode_dlc(frame_dlc)
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        sn_data_bytes = cls.__encode_sn(sequence_number=sequence_number)
        cf_bytes = ai_data_bytes + sn_data_bytes + bytearray(payload)
        if len(cf_bytes) > frame_data_bytes_number:
            raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes to fit in. "
                                             "Consider increasing DLC value.")
        data_bytes_to_pad = frame_data_bytes_number - len(cf_bytes)
        if data_bytes_to_pad > 0:
            if dlc is not None and dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
                raise InconsistentArgumentsError(f"CAN Frame Data Padding shall not be used for CAN frames with "
                                                 f"DLC < {CanDlcHandler.MIN_BASE_UDS_DLC}. Actual value: dlc={dlc}")
            return cf_bytes + data_bytes_to_pad * bytearray([filler_byte])
        return cf_bytes

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormat,
                              payload: RawBytesAlias,
                              sequence_number: int,
                              dlc: int,
                              filler_byte: int = DEFAULT_FILLER_BYTE,
                              target_address: Optional[int] = None,
                              address_extension: Optional[int] = None) -> bytearray:
        """
        Create a data field of a CAN frame that carries a Consecutive Frame packet.

        .. note:: You addressing use this method to create Consecutive Frame data bytes with any (also inconsistent
            with ISO 15765) parameters values.
            It is recommended to use
            :meth:`~uds.addressing.consecutive_frame.CanConsecutiveFrameHandler.create_valid_frame_data` to create data bytes
            for a Consecutive Frame with valid (compatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Consecutive Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param sequence_number: Value of Sequence Number parameter.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Provided `payload` contains too many bytes to fit it into a Consecutive Frame
            data field.

        :return: Raw bytes of CAN frame data for the provided Consecutive Frame packet information.
        """
        validate_raw_byte(filler_byte)
        validate_raw_bytes(payload, allow_empty=True)
        frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        sn_data_bytes = cls.__encode_sn(sequence_number=sequence_number)
        cf_bytes = ai_data_bytes + sn_data_bytes + bytearray(payload)
        if len(cf_bytes) > frame_data_bytes_number:
            raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes to fit in. "
                                             "Consider increasing DLC value.")
        data_padding = ((frame_data_bytes_number - len(cf_bytes)) * bytearray([filler_byte]))
        return cf_bytes + data_padding

    @classmethod
    def is_consecutive_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
        """
        Check if provided data bytes encodes a Consecutive Frame packet.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            Only, :ref:`CAN Packet Type (N_PCI) <knowledge-base-addressing-n-pci>` parameter is checked whether contain
            Consecutive Frame N_PCI value.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries Consecutive Frame, False otherwise.
        """
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return raw_frame_data[ai_bytes_number] >> 4 == cls.CONSECUTIVE_FRAME_N_PCI

    @classmethod
    def decode_payload(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bytearray:
        """
        Extract diagnostic message payload from Consecutive Frame data bytes.

        .. warning:: The output might contain additional filler bytes (they are not part of diagnostic message payload)
            that were added during :ref:`CAN Frame Data Padding <knowledge-base-addressing-frame-data-padding>`.
            The presence of filler bytes in :ref:`Consecutive Frame <knowledge-base-addressing-consecutive-frame>`
            cannot be determined basing solely on the information contained in a Consecutive Frame data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Consecutive Frame CAN packet.

        :return: Payload bytes (with potential Filler Bytes) of a diagnostic message carried by a considered
            Consecutive Frame.
        """
        if not cls.is_consecutive_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError("Provided `raw_frame_data` value does not carry a Consecutive Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data!r}")
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return bytearray(raw_frame_data[ai_bytes_number + cls.SN_BYTES_USED:])

    @classmethod
    def decode_sequence_number(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
        """
        Extract a value of Sequence Number from Consecutive Frame data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Consecutive Frame CAN packet.

        :return: Extracted value of Sequence Number.
        """
        if not cls.is_consecutive_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError("Provided `raw_frame_data` value does not carry a Consecutive Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data!r}")
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return raw_frame_data[ai_bytes_number] & 0xF

    @classmethod
    def get_min_dlc(cls, addressing_format: CanAddressingFormat, payload_length: int = 1) -> int:
        """
        Get the minimum value of a CAN frame DLC to carry a Consecutive Frame packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param payload_length: Number of payload bytes that considered CAN packet carries.

        :raise TypeError: Provided value of Payload Length is not int type.
        :raise ValueError: Provided value of Payload Length is out of range (1 <= value <= MAX Payload Length).
        :raise InconsistentArgumentsError: Provided Addressing Format and Payload Length values cannot be used together.

        :return: The lowest value of DLC that enables to fit in provided Consecutive Frame packet data.
        """
        if not isinstance(payload_length, int):
            raise TypeError(f"Provided `payload_length` value is not int type. Actual type: {type(payload_length)}")
        max_payload_length = CanDlcHandler.MAX_DATA_BYTES_NUMBER - cls.SN_BYTES_USED
        if not 1 <= payload_length <= max_payload_length:
            raise ValueError(f"Provided `payload_length` value is out of range. "
                             f"Expected: 1 <= payload_length <= {max_payload_length}. Actual value: {payload_length}")
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        if payload_length + ai_data_bytes_number > max_payload_length:
            raise InconsistentArgumentsError(f"Provided `payload_length` and `addressing_format` values cannot be used "
                                             f"together. As they require {payload_length + ai_data_bytes_number} "
                                             f"to accommodate while there are maximally {max_payload_length} to use.")
        return CanDlcHandler.get_min_dlc(ai_data_bytes_number + cls.SN_BYTES_USED + payload_length)

    @classmethod
    def get_max_payload_size(cls,
                             addressing_format: Optional[CanAddressingFormat] = None,
                             dlc: Optional[int] = None) -> int:
        """
        Get the maximum size of a payload that addressing fit into Consecutive Frame data bytes.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
            Leave None to get the result for CAN addressing format that does not use data bytes for carrying
            addressing information.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
            Leave None to get the result for the greatest possible DLC value.

        :raise InconsistentArgumentsError: Consecutive Frame packet cannot use provided attributes according to
            ISO 15765.

        :return: The maximum number of payload bytes that could fit into a considered Consecutive Frame.
        """
        if dlc is not None:
            frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        else:
            frame_data_bytes_number = CanDlcHandler.MAX_DATA_BYTES_NUMBER
        ai_data_bytes_number = 0 if addressing_format is None else \
            CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        output = frame_data_bytes_number - ai_data_bytes_number - cls.SN_BYTES_USED
        if output <= 0:
            raise InconsistentArgumentsError(f"Provided values cannot be used to transmit a valid Consecutive Frame "
                                             f"packet. Consider using greater DLC value or changing the CAN Addressing "
                                             f"Format. Actual values: dlc={dlc}, addressing_format={addressing_format}")
        return output

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded Consecutive Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Consecutive Frame CAN packet.
        :raise InconsistentArgumentsError: Provided frame data of a CAN frames does not carry a properly encoded
            Consecutive Frame CAN packet.
        """
        validate_raw_bytes(raw_frame_data)
        if not cls.is_consecutive_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError("Provided `raw_frame_data` value does not carry a Consecutive Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data!r}")
        min_dlc = cls.get_min_dlc(addressing_format=addressing_format)
        dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
        if min_dlc > dlc:
            raise InconsistentArgumentsError("Provided `raw_frame_data` does not contain any payload bytes.")

    @classmethod
    def __encode_sn(cls, sequence_number: int) -> bytearray:
        """
        Create Consecutive Frame data bytes with CAN Packet Type and Sequence Number parameters.

        :param sequence_number: Value of the sequence number parameter.

        :return: Consecutive Frame data bytes containing CAN Packet Type and Sequence Number parameters.
        """
        validate_nibble(sequence_number)
        return bytearray([(cls.CONSECUTIVE_FRAME_N_PCI << 4) ^ sequence_number])

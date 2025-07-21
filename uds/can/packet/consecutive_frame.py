"""Implementation of handlers for :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>` CAN packet."""

__all__ = ["CONSECUTIVE_FRAME_N_PCI", "SN_BYTES_USED",
           "is_consecutive_frame", "validate_consecutive_frame_data",
           "encode_consecutive_frame_data", "generate_consecutive_frame_data",
           "decode_consecutive_frame_payload",
           "get_consecutive_frame_min_dlc", "get_consecutive_frame_max_payload_size",
           "extract_sequence_number", "encode_sequence_number"]

from typing import Optional

from uds.utilities import (
    InconsistentArgumentsError,
    RawBytesAlias,
    validate_nibble,
    validate_raw_byte,
    validate_raw_bytes,
)

from ..addressing import CanAddressingFormat, CanAddressingInformation
from ..frame import DEFAULT_FILLER_BYTE, CanDlcHandler

CONSECUTIVE_FRAME_N_PCI: int = 0x2
""":ref:`N_PCI <knowledge-base-n-pci>` value of :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`."""

SN_BYTES_USED: int = 1
"""Number of CAN Frame data bytes used to carry CAN Packet Type and Sequence Number (SN) in a Consecutive Frame."""


def is_consecutive_frame(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
    """
    Check if provided data bytes contain a Consecutive Frame packet.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        It only checks :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter for
        Consecutive Frame N_PCI value.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to check.

    :return: True if provided data bytes carries Consecutive Frame, False otherwise.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return raw_frame_data[ai_bytes_number] >> 4 == CONSECUTIVE_FRAME_N_PCI


def validate_consecutive_frame_data(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
    """
    Validate whether data field of a CAN Packet carries a properly encoded Consecutive Frame.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to validate.

    :raise ValueError: The value of N_PCI in provided data is not Consecutive Frame N_PCI.
    :raise InconsistentArgumentsError: Provided data does not carry any payload.
    """
    validate_raw_bytes(raw_frame_data, allow_empty=False)
    if not is_consecutive_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
        raise ValueError("Provided `raw_frame_data` value does not carry a Consecutive Frame packet.")
    min_dlc = get_consecutive_frame_min_dlc(addressing_format)
    dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
    if min_dlc > dlc:
        raise InconsistentArgumentsError("Provided `raw_frame_data` does not contain any payload bytes.")


def encode_consecutive_frame_data(addressing_format: CanAddressingFormat,
                                  payload: RawBytesAlias,
                                  sequence_number: int,
                                  dlc: Optional[int] = None,
                                  filler_byte: int = DEFAULT_FILLER_BYTE,
                                  target_address: Optional[int] = None,
                                  address_extension: Optional[int] = None) -> bytearray:
    """
    Create a data field of a CAN frame that carries a valid Consecutive Frame packet.

    .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
        Use :func:`~uds.can.packet.first_frame.generate_consecutive_frame_data` to generate data bytes with any (also
        incompatible with ISO 15765) parameters values.

    :param addressing_format: CAN addressing format used.
    :param payload: Payload to carry.
    :param sequence_number: Sequence Number value to set.
    :param dlc: DLC value of a CAN frame.

        - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
        - int type value - DLC value to set. CAN Data Padding will be used to fill the unused data bytes.

    :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
    :param target_address: Target Address value carried by this CAN Packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Target Address parameter.
    :param address_extension: Address Extension value carried by this CAN packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Address Extension parameter.

    :raise InconsistentArgumentsError: Provided parameters cannot be used together to create a valid
        Consecutive Frame data.

    :return: Raw data bytes of a CAN frame.
    """
    validate_raw_byte(filler_byte)
    validate_raw_bytes(payload, allow_empty=False)
    if dlc is None:
        frame_dlc = get_consecutive_frame_min_dlc(addressing_format=addressing_format, payload_length=len(payload))
    else:
        frame_dlc = dlc
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    frame_data_bytes_number = CanDlcHandler.decode_dlc(frame_dlc)
    sn_data_bytes = encode_sequence_number(sequence_number=sequence_number)
    cf_bytes = ai_data_bytes + sn_data_bytes + bytearray(payload)
    if len(cf_bytes) > frame_data_bytes_number:
        raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes. "
                                         "Consider increasing DLC value or shortening the payload.")
    data_bytes_to_pad = frame_data_bytes_number - len(cf_bytes)
    if data_bytes_to_pad > 0:
        if dlc is not None and dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise InconsistentArgumentsError("CAN Frame Data Padding shall not be used for CAN frames with "
                                             f"DLC < {CanDlcHandler.MIN_BASE_UDS_DLC}.")
    return cf_bytes + data_bytes_to_pad * bytearray([filler_byte])


def generate_consecutive_frame_data(addressing_format: CanAddressingFormat,
                                    payload: RawBytesAlias,
                                    sequence_number: int,
                                    dlc: int,
                                    filler_byte: int = DEFAULT_FILLER_BYTE,
                                    target_address: Optional[int] = None,
                                    address_extension: Optional[int] = None) -> bytearray:
    """
    Generate CAN frame data field that carries any combination of Consecutive Frame packet data parameters.

    .. note:: Crosscheck of provided values is not performed so you might use this function to create data fields
        that are not compatible with Diagnostic on CAN standard (ISO 15765).

    :param addressing_format: CAN addressing format used.
    :param payload: Payload to carry.
    :param dlc: DLC value of a CAN frame.
    :param sequence_number: Sequence Number value to set.
    :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
    :param target_address: Target Address value carried by this CAN Packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Target Address parameter.
    :param address_extension: Address Extension value carried by this CAN packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Address Extension parameter.

    :raise InconsistentArgumentsError: Provided `payload` contains invalid number of bytes.

    :return: Raw data bytes of a CAN frame.
    """
    validate_raw_byte(filler_byte)
    validate_raw_bytes(payload, allow_empty=True)
    frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    sn_data_bytes = encode_sequence_number(sequence_number=sequence_number)
    cf_bytes = ai_data_bytes + sn_data_bytes + bytearray(payload)
    if len(cf_bytes) > frame_data_bytes_number:
        raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes. "
                                         "Consider increasing DLC value or shortening the payload.")
    data_padding = ((frame_data_bytes_number - len(cf_bytes)) * bytearray([filler_byte]))
    return cf_bytes + data_padding


def decode_consecutive_frame_payload(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bytearray:
    """
    Extract diagnostic message payload from Consecutive Frame data bytes.

    .. warning:: The output might contain filler bytes (they are not part of diagnostic message payload)
        that were added during :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
        The presence of filler bytes in :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
        cannot be determined basing solely on the information contained in a Consecutive Frame data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a considered CAN frame.

    :return: Payload bytes (with potential Filler Bytes) carried by the provided Consecutive Frame data.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return bytearray(raw_frame_data[ai_bytes_number + SN_BYTES_USED:])


def get_consecutive_frame_min_dlc(addressing_format: CanAddressingFormat, payload_length: int = 1) -> int:
    """
    Get the minimum value of a CAN frame DLC to carry a Consecutive Frame packet.

    :param addressing_format: CAN addressing format used.
    :param payload_length: Number of payload bytes to carry.

    :raise TypeError: Provided value of Payload Length is not int type.
    :raise ValueError: Provided value of Payload Length is out of range.

    :return: The lowest value of DLC for a Consecutive Frame that would carry provided payload size.
    """
    if not isinstance(payload_length, int):
        raise TypeError("Provided `payload_length` value is not int type.")
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    max_payload_length = CanDlcHandler.MAX_DATA_BYTES_NUMBER - SN_BYTES_USED - ai_data_bytes_number
    if not 1 <= payload_length <= max_payload_length:
        raise ValueError("Provided `payload_length` value is out of range. "
                         f"Expected: 1 <= payload_length <= {max_payload_length}.")
    return CanDlcHandler.get_min_dlc(ai_data_bytes_number + SN_BYTES_USED + payload_length)


def get_consecutive_frame_max_payload_size(addressing_format: CanAddressingFormat,
                                           dlc: Optional[int] = None) -> int:
    """
    Get the maximum payload size that could be carried by a Consecutive Frame.

    :param addressing_format: CAN addressing format used.
    :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        Leave None to get the result for the greatest possible DLC value.

    :raise InconsistentArgumentsError: Provided dlc cannot be used for Consecutive Frame with in the provided
        CAN Addressing Format.

    :return: The maximum number of payload bytes that could be carried in a Consecutive Frame.
    """
    if dlc is not None:
        frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
    else:
        frame_data_bytes_number = CanDlcHandler.MAX_DATA_BYTES_NUMBER
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    output = frame_data_bytes_number - ai_data_bytes_number - SN_BYTES_USED
    if output <= 0:
        raise InconsistentArgumentsError("Provided values cannot be used to transmit a valid Consecutive Frame "
                                         "packet. Consider using greater DLC value.")
    return output


def extract_sequence_number(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
    """
    Extract the value of Sequence Number from Consecutive Frame data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a considered CAN frame.

    :return: Extracted value of Sequence Number.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return raw_frame_data[ai_bytes_number] & 0xF


def encode_sequence_number(sequence_number: int) -> bytearray:
    """
    Create valid Consecutive Frame data bytes that contain Sequence Number and N_PCI values.

    :param sequence_number: Order value of a Consecutive Frame.

    :return: Consecutive Frame data bytes containing CAN Packet Type and Sequence Number parameters.
    """
    validate_nibble(sequence_number)
    return bytearray([(CONSECUTIVE_FRAME_N_PCI << 4) ^ sequence_number])

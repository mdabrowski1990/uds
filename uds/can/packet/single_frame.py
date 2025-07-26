"""Implementation of handlers for :ref:`Single Frame <knowledge-base-can-single-frame>` CAN packet."""

__all__ = ["SINGLE_FRAME_N_PCI", "MAX_DLC_VALUE_SHORT_SF_DL", "SHORT_SF_DL_BYTES_USED", "LONG_SF_DL_BYTES_USED",
           "is_single_frame", "validate_single_frame_data",
           "create_single_frame_data", "generate_single_frame_data", "extract_single_frame_payload", "extract_sf_dl",
           "get_max_sf_dl", "get_single_frame_min_dlc",
           "extract_sf_dl_data_bytes", "get_sf_dl_bytes_number", "encode_sf_dl", "generate_sf_dl_bytes",
           "validate_sf_dl"]

from typing import Optional
from warnings import warn

from uds.utilities import (
    InconsistentArgumentsError,
    RawBytesAlias,
    ValueWarning,
    validate_nibble,
    validate_raw_byte,
    validate_raw_bytes,
)

from ..addressing import CanAddressingFormat, CanAddressingInformation
from ..frame import DEFAULT_FILLER_BYTE, CanDlcHandler

SINGLE_FRAME_N_PCI: int = 0
""":ref:`N_PCI <knowledge-base-n-pci>` value of :ref:`Single Frame <knowledge-base-can-single-frame>`."""

MAX_DLC_VALUE_SHORT_SF_DL: int = 8
"""Maximum value of DLC for which short
:ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>` format shall be used."""
SHORT_SF_DL_BYTES_USED: int = 1
"""Number of CAN Frame data bytes used to carry CAN Packet Type and Single Frame Data Length (SF_DL).
This value is valid only for the short format (used when DLC <= 8)."""
LONG_SF_DL_BYTES_USED: int = 2
"""Number of CAN Frame data bytes used to carry CAN Packet Type and Single Frame Data Length (SF_DL).
This value is valid only for the long format (used when DLC > 8)."""


def is_single_frame(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
    """
    Check if provided data bytes contain a Single Frame packet.

    .. warning:: The method does not validate the content (e.g. SF_DL parameter) of the provided frame data bytes.
        It only checks :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter for
        Single Frame N_PCI value.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to check.

    :return: True if provided data bytes carries Single Frame, False otherwise.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return (raw_frame_data[ai_bytes_number] >> 4) == SINGLE_FRAME_N_PCI


def validate_single_frame_data(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
    """
    Validate whether data field of a CAN Packet carries a properly encoded Single Frame.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to validate.

    :raise ValueError: The value of N_PCI in provided data is not Single Frame N_PCI.
    :raise InconsistentArgumentsError: Provided frame data of a CAN frames does not carry a properly encoded
        Single Frame CAN packet.
    """
    validate_raw_bytes(raw_frame_data, allow_empty=False)
    if not is_single_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
        raise ValueError("Provided `raw_frame_data` value does not carry a Single Frame packet.")
    sf_dl_data_bytes = extract_sf_dl_data_bytes(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
    dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
    if dlc <= MAX_DLC_VALUE_SHORT_SF_DL:
        sf_dl = sf_dl_data_bytes[0] & 0xF
    else:
        sf_dl = sf_dl_data_bytes[1]
        if sf_dl_data_bytes[0] & 0xF != 0:
            raise InconsistentArgumentsError("Value of Single Frame Data Length must use 0x00 at the first byte when "
                                             "long SF_DL format (for DLC > {MAX_DLC_VALUE_SHORT_SF_DL})) is used.")
    min_dlc = get_single_frame_min_dlc(addressing_format=addressing_format, payload_length=sf_dl)
    if min_dlc > dlc:
        raise InconsistentArgumentsError("Value of Single Frame Data Length is greater than number of payload bytes.")
    if min_dlc < dlc:
        if dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise InconsistentArgumentsError("Data padding was used for CAN frame with "
                                             f"DLC lesser than {CanDlcHandler.MIN_BASE_UDS_DLC}.")
        if dlc > CanDlcHandler.MIN_BASE_UDS_DLC:
            warn(message=f"DLC greater than {CanDlcHandler.MIN_BASE_UDS_DLC} is used for CAN Packets "
                         f"without data padding which unnecessarily increases the bus load.",
                 category=ValueWarning)


def create_single_frame_data(addressing_format: CanAddressingFormat,
                             payload: RawBytesAlias,
                             dlc: Optional[int] = None,
                             filler_byte: int = DEFAULT_FILLER_BYTE,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> bytearray:
    """
    Create data field of a CAN frame that carries a valid Single Frame packet.

    .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
        Use :func:`~uds.can.packet.single_frame.generate_single_frame_data` to generate data bytes with any (also
        incompatible with ISO 15765) parameters values.

    :param addressing_format: CAN addressing format used.
    :param payload: Payload to carry.
    :param dlc: DLC value of a CAN frame.

        - None - use CAN Data Frame Optimization (CAN DLC value will be automatically determined)
        - int type value - DLC value to use. CAN Data Padding will be used to fill the unused data bytes.

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
    validate_raw_bytes(payload, allow_empty=False)
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    frame_dlc = get_single_frame_min_dlc(addressing_format=addressing_format, payload_length=len(payload)) \
        if dlc is None else dlc
    frame_data_bytes_number = CanDlcHandler.decode_dlc(frame_dlc)
    sf_dl_bytes = encode_sf_dl(sf_dl=len(payload),
                               dlc=frame_dlc,
                               addressing_format=addressing_format)
    sf_bytes = ai_data_bytes + sf_dl_bytes + bytearray(payload)
    if len(sf_bytes) > frame_data_bytes_number:
        raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes to fit in. "
                                         "Consider increasing DLC value.")
    data_bytes_to_pad = frame_data_bytes_number - len(sf_bytes)
    if data_bytes_to_pad > 0:
        if dlc is not None and dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise InconsistentArgumentsError("CAN Frame Data Padding shall not be used for CAN frames with "
                                             f"DLC < {CanDlcHandler.MIN_BASE_UDS_DLC}.")
    return sf_bytes + data_bytes_to_pad * bytearray([filler_byte])


def generate_single_frame_data(addressing_format: CanAddressingFormat,
                               payload: RawBytesAlias,
                               dlc: int,
                               sf_dl_short: int,
                               sf_dl_long: Optional[int] = None,
                               filler_byte: int = DEFAULT_FILLER_BYTE,
                               target_address: Optional[int] = None,
                               address_extension: Optional[int] = None) -> bytearray:
    """
    Generate CAN frame data field that carries any combination of Single Frame packet data parameters.

    .. note:: Crosscheck of provided values is not performed so you might use this function to create data fields
        that are not compatible with Diagnostic on CAN standard (ISO 15765).

    :param addressing_format: CAN addressing format used.
    :param payload: Payload to carry.
    :param dlc: DLC value of a CAN frame.
    :param sf_dl_short: Value to put into a slot of Single Frame Data Length in short format.
    :param sf_dl_long: Value to put into a slot of Single Frame Data Length in long format.
        Leave None to use short (1-byte-long) format of Single Frame Data Length.
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
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
    sf_dl_bytes = generate_sf_dl_bytes(sf_dl_short=sf_dl_short, sf_dl_long=sf_dl_long)
    sf_bytes = ai_data_bytes + sf_dl_bytes + bytearray(payload)
    if len(sf_bytes) > frame_data_bytes_number:
        raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes to fit in. "
                                         "Consider increasing DLC value.")
    data_padding = ((frame_data_bytes_number - len(sf_bytes)) * bytearray([filler_byte]))
    return sf_bytes + data_padding


def extract_single_frame_payload(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bytearray:
    """
    Extract payload from Single Frame data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :return: Payload bytes carried by the provided Single Frame data.
    """
    sf_dl = extract_sf_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
    sf_dl_bytes_number = get_sf_dl_bytes_number(dlc)
    return bytearray(raw_frame_data[ai_data_bytes_number + sf_dl_bytes_number:][:sf_dl])


def extract_sf_dl(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
    """
    Extract the value of Single Frame Data Length from Single Frame data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :raise NotImplementedError: There is missing implementation for the provided Single Frame Data Length format.

    :return: Extracted value of Single Frame Data Length.
    """
    sf_dl_data_bytes = extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                raw_frame_data=raw_frame_data)
    if len(sf_dl_data_bytes) == SHORT_SF_DL_BYTES_USED:
        return sf_dl_data_bytes[0] & 0xF
    if len(sf_dl_data_bytes) == LONG_SF_DL_BYTES_USED:
        return sf_dl_data_bytes[1]
    raise NotImplementedError("Unknown format of Single Frame Data Length was found.")


def get_max_sf_dl(addressing_format: CanAddressingFormat,
                  dlc: Optional[int] = None) -> int:
    """
    Get the maximum value Single Frame Data Length.

    .. note:: The maximal value of SF_DL reflects maximal number of payload bytes that would fit into a Single Frame.

    :param addressing_format: CAN addressing format used.
    :param dlc: DLC value to use.
        Leave None to get the result for the greatest possible DLC value.

    :raise InconsistentArgumentsError: Single Frame packet cannot use provided attributes.

    :return: The maximum number value of SF_DL for the provided DLC and CAN Addressing Format.
    """
    if dlc is not None:
        frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        sf_dl_bytes_number = get_sf_dl_bytes_number(dlc)
    else:
        frame_data_bytes_number = CanDlcHandler.MAX_DATA_BYTES_NUMBER
        sf_dl_bytes_number = LONG_SF_DL_BYTES_USED
    ai_data_bytes_number = 0 if addressing_format is None else \
        CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    output = frame_data_bytes_number - ai_data_bytes_number - sf_dl_bytes_number
    if output <= 0:
        raise InconsistentArgumentsError("Provided values cannot be used to transmit a valid Single Frame packet. "
                                         "Consider using greater DLC value or changing the CAN Addressing Format.")
    return output


def get_single_frame_min_dlc(addressing_format: CanAddressingFormat, payload_length: int) -> int:
    """
    Get the minimum value of a CAN frame DLC to carry a Single Frame packet.

    :param addressing_format: CAN addressing format used.
    :param payload_length: Number of payload bytes to carry.

    :return: The lowest value of DLC for a Single Frame that would carry provided payload size.
    """
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    data_bytes_short_sf_dl = ai_data_bytes_number + SHORT_SF_DL_BYTES_USED + payload_length
    dlc_with_short_sf_dl = CanDlcHandler.get_min_dlc(data_bytes_short_sf_dl)
    if dlc_with_short_sf_dl <= MAX_DLC_VALUE_SHORT_SF_DL:
        return dlc_with_short_sf_dl
    data_bytes_long_sf_dl = ai_data_bytes_number + LONG_SF_DL_BYTES_USED + payload_length
    return CanDlcHandler.get_min_dlc(data_bytes_long_sf_dl)


def extract_sf_dl_data_bytes(addressing_format: CanAddressingFormat,
                             raw_frame_data: RawBytesAlias) -> bytearray:
    """
    Extract data bytes that carry CAN Packet Type and Single Frame Data Length parameters.

    .. warning:: This method does not check whether provided `raw_frame_data` actually contains Single Frame.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :return: Extracted data bytes with CAN Packet Type and Single Frame Data Length parameters.
    """
    dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return bytearray(raw_frame_data[ai_bytes_number:])[:get_sf_dl_bytes_number(dlc)]


def get_sf_dl_bytes_number(dlc: int) -> int:
    """
    Get number of data bytes used for carrying CAN Packet Type and Single Frame Data Length parameters.

    :param dlc: DLC value of a CAN frame.

    :return: The number of bytes used for CAN Packet Type and Single Frame Data Length parameters.
    """
    CanDlcHandler.validate_dlc(dlc)
    return SHORT_SF_DL_BYTES_USED if dlc <= MAX_DLC_VALUE_SHORT_SF_DL else LONG_SF_DL_BYTES_USED


def encode_sf_dl(addressing_format: CanAddressingFormat,
                 dlc: int,
                 sf_dl: int) -> bytearray:
    """
    Create valid Single Frame data bytes that contain Single Frame Data Length and N_PCI values.

    .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.

    :param addressing_format: CAN Addressing Format used.
    :param dlc: DLC value of a CAN Frame to carry this information.
    :param sf_dl: Number of payload bytes carried by a Single Frame.

    :return: Single Frame data bytes containing CAN Packet Type and Single Frame Data Length parameters.
    """
    validate_sf_dl(dlc=dlc, addressing_format=addressing_format, sf_dl=sf_dl)
    if dlc <= MAX_DLC_VALUE_SHORT_SF_DL:
        return generate_sf_dl_bytes(sf_dl_short=sf_dl)
    return generate_sf_dl_bytes(sf_dl_long=sf_dl)


def generate_sf_dl_bytes(sf_dl_short: int = 0, sf_dl_long: Optional[int] = None) -> bytearray:
    """
    Create Single Frame bytes containing Single Frame Data Length and N_PCI values.

    .. note:: This method can be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

    :param sf_dl_short: Value to put into a slot of Single Frame Data Length in short format.
    :param sf_dl_long: Value to put into a slot of Single Frame Data Length in long format.
        Leave None to use short (1-byte-long) format of Single Frame Data Length./

    :return: CAN frame data bytes containing CAN Packet Type and Single Frame Data Length parameters.
    """
    validate_nibble(sf_dl_short)
    sf_dl_byte_0 = sf_dl_short ^ (SINGLE_FRAME_N_PCI << 4)
    if sf_dl_long is None:
        return bytearray([sf_dl_byte_0])
    validate_raw_byte(sf_dl_long)
    return bytearray([sf_dl_byte_0, sf_dl_long])


def validate_sf_dl(addressing_format: CanAddressingFormat,
                   dlc: int,
                   sf_dl: int) -> None:
    """
    Validate a value of Single Frame Data Length.

    :param addressing_format: CAN Addressing Format used.
    :param dlc: DLC value used.
    :param sf_dl: Single Frame Data Length value to validate.

    :raise TypeError: Provided value of Single Frame Data Length is not int type.
    :raise ValueError: Provided value of Single Frame Data Length is too small.
    :raise InconsistentArgumentsError: It is impossible for a Single Frame with provided DLC to contain as many
        payload bytes as the provided value of Single Frame Data Length.
    """
    if not isinstance(sf_dl, int):
        raise TypeError(f"Provided value of Single Frame Data Length is not int type. Actual type: {type(sf_dl)}")
    if sf_dl <= 0:
        raise ValueError(f"Provided value of Single Frame Data Length is too small (<1). Actual value: {sf_dl}")
    max_sf = get_max_sf_dl(addressing_format=addressing_format, dlc=dlc)
    if sf_dl > max_sf:
        raise InconsistentArgumentsError("Provided value of `sf_dl` is greater than maximum valid value of "
                                         "Single Frame Data Length for provided DLC and Addressing Format.")

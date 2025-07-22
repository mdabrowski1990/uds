"""Implementation of handlers for :ref:`First Frame <knowledge-base-can-first-frame>` CAN packet."""

__all__ = ["FIRST_FRAME_N_PCI", "MAX_SHORT_FF_DL_VALUE", "MAX_LONG_FF_DL_VALUE", "SHORT_FF_DL_BYTES_USED",
           "SHORT_FF_DL_BYTES_USED", "LONG_FF_DL_BYTES_USED",
           "is_first_frame", "validate_first_frame_data",
           "create_first_frame_data", "generate_first_frame_data",
           "extract_first_frame_payload", "extract_ff_dl", "get_first_frame_payload_size",
           "extract_ff_dl_data_bytes", "encode_ff_dl", "generate_ff_dl_bytes", "validate_ff_dl"]

from typing import Optional

from uds.can.frame import CanDlcHandler
from uds.utilities import InconsistentArgumentsError, RawBytesAlias, bytes_to_int, int_to_bytes, validate_raw_bytes

from ..addressing import CanAddressingFormat, CanAddressingInformation
from .single_frame import get_max_sf_dl

FIRST_FRAME_N_PCI: int = 0x1
""":ref:`N_PCI <knowledge-base-n-pci>` value of :ref:`First Frame <knowledge-base-can-first-frame>`."""

MAX_SHORT_FF_DL_VALUE: int = 0xFFF
"""Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` 
for which short can be used."""
MAX_LONG_FF_DL_VALUE: int = 0xFFFFFFFF
"""Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>`."""
SHORT_FF_DL_BYTES_USED: int = 2
"""Number of CAN Frame data bytes used to carry CAN Packet Type and First Frame Data Length (FF_DL).
This value is valid only for the short format with FF_DL <= 4095."""
LONG_FF_DL_BYTES_USED: int = 6
"""Number of CAN Frame data bytes used to carry CAN Packet Type and First Frame Data Length (FF_DL).
This value is valid only for the long format with FF_DL > 4095."""


def is_first_frame(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
    """
    Check if provided data bytes contain a First Frame packet.

    .. warning:: The method does not validate the content (e.g. FF_DL parameter) of the provided frame data bytes.
        It only checks :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter for
        First Frame N_PCI value.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to check.

    :return: True if provided data bytes carries First Frame, False otherwise.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    return raw_frame_data[ai_bytes_number] >> 4 == FIRST_FRAME_N_PCI


def validate_first_frame_data(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
    """
    Validate whether data field of a CAN Packet carries a properly encoded First Frame.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: The value of N_PCI in provided data is not Single Frame N_PCI.
    """
    validate_raw_bytes(raw_frame_data, allow_empty=False)
    if not is_first_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
        raise ValueError("Provided `raw_frame_data` value does not carry a First Frame packet.")
    ff_dl = extract_ff_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
    ff_dl_data_bytes = extract_ff_dl_data_bytes(addressing_format=addressing_format,
                                                raw_frame_data=raw_frame_data)
    dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
    validate_ff_dl(addressing_format=addressing_format,
                   dlc=dlc,
                   ff_dl=ff_dl,
                   ff_dl_bytes_number=len(ff_dl_data_bytes))


def create_first_frame_data(addressing_format: CanAddressingFormat,
                            payload: RawBytesAlias,
                            dlc: int,
                            ff_dl: int,
                            target_address: Optional[int] = None,
                            address_extension: Optional[int] = None) -> bytearray:
    """
    Create a data field of a CAN frame that carries a valid First Frame packet.

    .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
        Use :func:`~uds.can.packet.first_frame.generate_first_frame_data` to generate data bytes with any (also
        incompatible with ISO 15765) parameters values.

    :param addressing_format: CAN addressing format used.
    :param payload: Payload to carry.
    :param dlc: DLC value of a CAN frame.
    :param ff_dl: Total payload bytes number of a diagnostic message.
    :param target_address: Target Address value carried by this CAN Packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Target Address parameter.
    :param address_extension: Address Extension value carried by this CAN packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Address Extension parameter.

    :raise InconsistentArgumentsError: Provided `payload` contains incorrect number of bytes to fit them into
        a First Frame data field using provided parameters.

    :return: Raw bytes of CAN frame data for the provided First Frame packet information.
    """
    validate_raw_bytes(payload, allow_empty=False)
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    ff_dl_data_bytes = encode_ff_dl(addressing_format=addressing_format, dlc=dlc, ff_dl=ff_dl)
    ff_data_bytes = ai_data_bytes + ff_dl_data_bytes + bytearray(payload)
    frame_length = CanDlcHandler.decode_dlc(dlc)
    if len(ff_data_bytes) != frame_length:
        raise InconsistentArgumentsError("Provided value of `payload` contains incorrect number of bytes for "
                                         "a First Frame with provided DLC.")
    return ff_data_bytes


def generate_first_frame_data(addressing_format: CanAddressingFormat,
                              payload: RawBytesAlias,
                              dlc: int,
                              ff_dl: int,
                              long_ff_dl_format: bool = False,
                              target_address: Optional[int] = None,
                              address_extension: Optional[int] = None) -> bytearray:
    """
    Generate CAN frame data field that carries any combination of First Frame packet data parameters.

    .. note:: Crosscheck of provided values is not performed so you might use this function to create data fields
        that are not compatible with Diagnostic on CAN standard (ISO 15765).

    :param addressing_format: CAN addressing format used.
    :param payload: Payload to carry.
    :param dlc: DLC value of a CAN frame.
    :param ff_dl: Total payload bytes number of a diagnostic message.
    :param long_ff_dl_format: Information whether long or short format of First Frame Data Length is used.
    :param target_address: Target Address value carried by this CAN Packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Target Address parameter.
    :param address_extension: Address Extension value carried by this CAN packet.
        The value must only be provided if `addressing_format` requires CAN frame data field to contain
        Address Extension parameter.

    :raise InconsistentArgumentsError: Provided `payload` contains incorrect number of bytes to fit them into
        a First Frame data field using provided parameters.

    :return: Raw bytes of CAN frame data for the provided First Frame packet information.
    """
    validate_raw_bytes(payload, allow_empty=True)
    ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                  target_address=target_address,
                                                                  address_extension=address_extension)
    ff_dl_data_bytes = generate_ff_dl_bytes(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)
    ff_data_bytes = ai_data_bytes + ff_dl_data_bytes + bytearray(payload)
    frame_length = CanDlcHandler.decode_dlc(dlc)
    if len(ff_data_bytes) != frame_length:
        raise InconsistentArgumentsError("Provided value of `payload` contains incorrect number of bytes for "
                                         "a First Frame with provided DLC.")
    return ff_data_bytes


def extract_first_frame_payload(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bytearray:
    """
    Extract payload from First Frame data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a considered CAN frame.

    :return: Payload bytes carried by the provided Single Frame data.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    ff_dl_data_bytes = extract_ff_dl_data_bytes(addressing_format=addressing_format,
                                                raw_frame_data=raw_frame_data)
    return bytearray(raw_frame_data[ai_bytes_number + len(ff_dl_data_bytes):])


def extract_ff_dl(addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
    """
    Extract the value of First Frame Data Length from First Frame data bytes.

    .. warning:: The method does not validate the content of the provided frame data bytes.
        There is no guarantee of the proper output when frame data in invalid format (incompatible with ISO 15765)
        is provided.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a considered CAN frame.

    :raise NotImplementedError: There is missing implementation for the provided First Frame Data Length format.

    :return: Extracted value of First Frame Data Length.
    """
    ff_dl_bytes = extract_ff_dl_data_bytes(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
    if len(ff_dl_bytes) == SHORT_FF_DL_BYTES_USED:
        return ((ff_dl_bytes[0] & 0xF) << 8) + ff_dl_bytes[1]
    if len(ff_dl_bytes) == LONG_FF_DL_BYTES_USED:
        return bytes_to_int(ff_dl_bytes[SHORT_FF_DL_BYTES_USED:])
    raise NotImplementedError("Unknown format of First Frame Data Length was found.")


def get_first_frame_payload_size(addressing_format: CanAddressingFormat,
                                 dlc: int,
                                 long_ff_dl_format: bool) -> int:
    """
    Get the number of payload bytes that could be carried by First Frame.

    :param addressing_format: CAN addressing format used.
    :param dlc: DLC value used.
    :param long_ff_dl_format: Information whether long or short format of First Frame Data Length is used.

    :raise ValueError: Invalid DLC value.

    :return: The number of payload bytes that shall be carried in a First Frame.
    """
    if dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
        raise ValueError(f"First Frame must use DLC >= {CanDlcHandler.MIN_BASE_UDS_DLC}.")
    data_bytes_number = CanDlcHandler.decode_dlc(dlc)
    ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    ff_dl_data_bytes_number = LONG_FF_DL_BYTES_USED if long_ff_dl_format else SHORT_FF_DL_BYTES_USED
    return data_bytes_number - ai_data_bytes_number - ff_dl_data_bytes_number


def extract_ff_dl_data_bytes(addressing_format: CanAddressingFormat,
                             raw_frame_data: RawBytesAlias) -> bytearray:
    """
    Extract data bytes that carry CAN Packet Type and First Frame Data Length parameters.

    .. warning:: This method does not check whether provided `raw_frame_data` actually contains First Frame.

    :param addressing_format: CAN Addressing Format used.
    :param raw_frame_data: Raw data bytes of a CAN frame.

    :return: Extracted data bytes with CAN Packet Type and First Frame Data Length parameters.
    """
    ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
    ff_dl_short_data_bytes = bytearray(raw_frame_data[ai_bytes_number:][:SHORT_FF_DL_BYTES_USED])
    if ff_dl_short_data_bytes[0] & 0xF != 0 or ff_dl_short_data_bytes[1] != 0x00:
        return ff_dl_short_data_bytes
    return bytearray(raw_frame_data[ai_bytes_number:][:LONG_FF_DL_BYTES_USED])


def encode_ff_dl(addressing_format: CanAddressingFormat,
                 dlc: int,
                 ff_dl: int) -> bytearray:
    """
    Create valid First Frame data bytes that contain First Frame Data Length and N_PCI values.

    .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.

    :param ff_dl: Value to put into a slot of First Frame Data Length.
    :param dlc: Value of DLC to use for First Frame Data Length value validation.
    :param addressing_format: Value of CAN Addressing Format to use for First Frame Data Length value validation.

    :return: First Frame data bytes containing CAN Packet Type and First Frame Data Length parameters.
    """
    validate_ff_dl(addressing_format=addressing_format, dlc=dlc, ff_dl=ff_dl)
    return generate_ff_dl_bytes(ff_dl=ff_dl, long_ff_dl_format=ff_dl > MAX_SHORT_FF_DL_VALUE)


def generate_ff_dl_bytes(ff_dl: int, long_ff_dl_format: bool) -> bytearray:
    """
    Create First Frame data bytes with CAN Packet Type and First Frame Data Length parameters.

    .. note:: This method addressing be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

    :param ff_dl: Value to put into a slot of First Frame Data Length.
    :param long_ff_dl_format: Information whether to use long or short format of First Frame Data Length.

    :raise ValueError: Provided First Frame Data Length value is out of the parameter values range.

    :return: First Frame data bytes containing CAN Packet Type and First Frame Data Length parameters.
    """
    if long_ff_dl_format and ff_dl > MAX_LONG_FF_DL_VALUE:
        raise ValueError(f"Value of First Frame Data Length must be not be greater than {MAX_LONG_FF_DL_VALUE} "
                         "to fit into long FF_DL format.")
    if not long_ff_dl_format and ff_dl > MAX_SHORT_FF_DL_VALUE:
        raise ValueError(f"Value of First Frame Data Length must be not be greater than {MAX_SHORT_FF_DL_VALUE} "
                         "to fit into short FF_DL format.")
    ff_dl_bytes_number = LONG_FF_DL_BYTES_USED if long_ff_dl_format else SHORT_FF_DL_BYTES_USED
    ff_dl_bytes = bytearray(int_to_bytes(int_value=ff_dl, size=ff_dl_bytes_number))
    ff_dl_bytes[0] ^= (FIRST_FRAME_N_PCI << 4)
    return ff_dl_bytes


def validate_ff_dl(ff_dl: int,
                   ff_dl_bytes_number: Optional[int] = None,
                   dlc: Optional[int] = None,
                   addressing_format: Optional[CanAddressingFormat] = None) -> None:
    """
    Validate a value of First Frame Data Length.

    :param ff_dl: First Frame Data Length value to validate.
    :param ff_dl_bytes_number: Information how many bytes are used to carry FF_DL.

        - None - do not perform compatibility check with the FF_DL format
        - LONG_FF_DL_BYTES_USED - perform compatibility check with long FF_DL format
        - SHORT_FF_DL_BYTES_USED - perform compatibility check with short FF_DL format
        - any other value will lead to raising an exception

    :param dlc: Value of DLC to use for First Frame Data Length value validation.
        Leave None if you do not want to validate whether First Frame shall be used in this case.
    :param addressing_format: Value of CAN Addressing Format to use for First Frame Data Length value validation.
        Leave None if you do not want to validate whether First Frame shall be used in this case.

    :raise TypeError: Provided value of First Frame Data Length is not int type.
    :raise ValueError: Provided value of First Frame Data Length is out of range (0 <= value <= MAX FF_DL).
    :raise InconsistentArgumentsError: Single Frame shall be used instead of First Frame to transmit provided
        number of payload bytes represented by FF_DL value.
    """
    if not isinstance(ff_dl, int):
        raise TypeError("Provided value of First Frame Data Length is not int type.")
    if not 0 <= ff_dl <= MAX_LONG_FF_DL_VALUE:
        raise ValueError("Provided value of First Frame Data Length is out of range. "
                         f"Expected: 0 <= ff_dl <= {MAX_LONG_FF_DL_VALUE}.")
    if dlc is not None and addressing_format is not None:
        if dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise ValueError("Provided value of DLC cannot be used with First Frame. "
                             f"Expected: dlc >= {CanDlcHandler.MIN_BASE_UDS_DLC}.")
        max_sf_dl = get_max_sf_dl(addressing_format=addressing_format, dlc=dlc)
        if ff_dl <= max_sf_dl:
            raise InconsistentArgumentsError("Single Frame shall be used instead of First Frame to carry this.")
    if ff_dl_bytes_number == LONG_FF_DL_BYTES_USED:
        if ff_dl <= MAX_SHORT_FF_DL_VALUE:
            raise InconsistentArgumentsError("Short format of First Frame Data Length shall be used.")
    elif ff_dl_bytes_number == SHORT_FF_DL_BYTES_USED:
        if ff_dl > MAX_SHORT_FF_DL_VALUE:
            raise InconsistentArgumentsError("Long format of First Frame Data Length shall be used.")
    elif ff_dl_bytes_number is not None:
        raise ValueError("Incorrect value of ff_dl_bytes was provided. It should be equal to either "
                         f"{SHORT_FF_DL_BYTES_USED} or {LONG_FF_DL_BYTES_USED}.")

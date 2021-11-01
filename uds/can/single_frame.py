"""
Implementation specific for Single Frame CAN packets.

This module contains implementation of :ref:`Single Frame <knowledge-base-can-single-frame>` packet attributes:
 - :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>`
"""

__all__ = ["CanSingleFrameDataLengthHandler", "CanSingleFrameHandler"]

from typing import Optional

from uds.utilities import RawByte, RawBytes, RawBytesList, int_to_bytes_list, bytes_list_to_int, \
    validate_raw_bytes, validate_raw_byte, validate_nibble, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler
from .packet_type import CanPacketType


class CanSingleFrameDataLengthHandler:
    """
    Helper class that provides utilities for Single Frame Data Length.

    :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` determines number of payload
    bytes of a diagnostic message that are carried by a Single Frame CAN Packet.
    """

    MAX_DLC_VALUE_SHORT_SF_DL: int = 8
    """Maximum value of DLC for which short
    :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>` format shall be used."""
    SHORT_SF_DL_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` parameters in 
    :ref:`Single Frame <knowledge-base-can-single-frame>` packets when short SF_DL format is used."""
    LONG_SF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` parameters in 
    :ref:`Single Frame <knowledge-base-can-single-frame>` packets when long SF_DL format is used."""

    @classmethod
    def encode_sf_dl(cls,
                     sf_dl: int,
                     dlc: int,
                     valid_sf_dl: bool = True,
                     addressing_format: Optional[CanAddressingFormatAlias] = None) -> RawBytesList:
        """
        Generate Single Frame data bytes with CAN Packet Type and Single Frame Data Length parameters.

        .. note:: This method can be used to encode any Single Frame Data Length value (also these invalid according
            to ISO 15765) as long as it can be converted to a list of CAN frame data bytes.

        :param sf_dl: Number of payload bytes carried by a considered Single Frame.
        :param dlc: DLC value of a CAN Frame to contain these data.
        :param valid_sf_dl: Flag informing whether only valid (compatible with ISO 15765) value shall be accepted.
        :param addressing_format: Value of CAN Addressing Format to use for Single Frame Data Length value validation.
            It is only used when `valid_sf_dl` is set to True.

        :return: Single Frame data bytes containing CAN Packet Type and Single Frame Data Length parameters.
        """
        cls.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, valid_sf_dl=valid_sf_dl, addressing_format=addressing_format)
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            sf_dl_data_bytes = int_to_bytes_list(int_value=sf_dl, list_size=cls.SHORT_SF_DL_BYTES_USED)
        else:
            sf_dl_data_bytes = int_to_bytes_list(int_value=sf_dl, list_size=cls.LONG_SF_DL_BYTES_USED)
        sf_dl_data_bytes[0] ^= (CanPacketType.SINGLE_FRAME.value << 4)
        return sf_dl_data_bytes

    @classmethod
    def decode_sf_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        """
        Decode value of Single Frame Data Length out of data of a CAN frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Extracted value of Single Frame Data Length.
        """
        CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data)
        sf_dl_data_bytes = cls.extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        sf_dl_data_bytes[0] ^= (CanPacketType.SINGLE_FRAME.value << 4)
        return bytes_list_to_int(bytes_list=sf_dl_data_bytes)

    @classmethod
    def extract_sf_dl_data_bytes(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawBytesList:
        """
        Extract data bytes that carries CAN Packet Type and Single Frame Data Length parameters.

        .. warning:: This method does not check whether provided `raw_frame_data` actually contains Single Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Extracted data bytes with CAN Packet Type and Single Frame Data Length parameters.
        """
        ai_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        validate_raw_bytes(raw_frame_data)
        dlc = CanDlcHandler.encode(len(raw_frame_data))
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            return list(raw_frame_data[ai_bytes_number:ai_bytes_number + cls.SHORT_SF_DL_BYTES_USED])
        else:
            return list(raw_frame_data[ai_bytes_number:ai_bytes_number + cls.LONG_SF_DL_BYTES_USED])

    @classmethod
    def validate_sf_dl(cls,
                       sf_dl: int,
                       dlc: int,
                       valid_sf_dl: bool = True,
                       addressing_format: Optional[CanAddressingFormatAlias] = None) -> None:
        """
        Validate a value of Single Frame Data Length.

        :param sf_dl: Single Frame Data Length value to validate.
        :param dlc: DLC value to validate.
        :param valid_sf_dl: Flag informing whether only valid (compatible with ISO 15765) value shall be accepted.
        :param addressing_format: Value of CAN Addressing Format to use for Single Frame Data Length value validation.
            It is only used when `valid_sf_dl` is set to True.

        :raise InconsistentArgumentsError: Provided Single Frame Data Length value is not consistent with other provided
            values.
        """
        if valid_sf_dl:
            frame_data_bytes = CanDlcHandler.decode(dlc)
            if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
                validate_nibble(sf_dl)
                sf_dl_data_bytes = cls.SHORT_SF_DL_BYTES_USED
            else:
                validate_raw_byte(sf_dl)
                sf_dl_data_bytes = cls.LONG_SF_DL_BYTES_USED
            ai_data_bytes = 0 if addressing_format is None else \
                CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
            max_sf_dl_value = frame_data_bytes - ai_data_bytes - sf_dl_data_bytes
            if sf_dl > max_sf_dl_value:
                raise InconsistentArgumentsError(f"Provided value of `sf_dl` is greater than maximum valid value of "
                                                 f"Single Frame Data Length for provided DLC and Addressing Format."
                                                 f"Actual values: sf_dl={sf_dl}, dlc={dlc}, "
                                                 f"addressing_format={addressing_format}. "
                                                 f"Expected: sf_dl<={max_sf_dl_value}")
        else:
            CanDlcHandler.validate_dlc(dlc)
            validate_nibble(sf_dl) if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL else validate_raw_byte(sf_dl)

    @classmethod
    def validate_sf_dl_data_bytes(cls,
                                  sf_dl_bytes: RawBytes,
                                  dlc: int,
                                  addressing_format: Optional[CanAddressingFormatAlias] = None) -> None:
        """
        Validate data bytes with CAN Packet Type and Single Frame Data Length parameters.

        :param sf_dl_bytes: Data bytes with CAN Packet Type and Single Frame Data Length to validate.
        :param dlc: DLC value used by a CAN Frame.
        :param addressing_format: Value of CAN Addressing Format to use for Single Frame Data Length value validation.

        :raise InconsistentArgumentsError:
        :raise ValueError: Provided Single Frame Data Length value is not correct or inconsistent with other arguments.
        """
        validate_raw_bytes(sf_dl_bytes)
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            if len(sf_dl_bytes) != cls.SHORT_SF_DL_BYTES_USED:
                raise InconsistentArgumentsError(f"Invalid length of `sf_dl_bytes` argument for provided DLC. "
                                                 f"Expected length: {cls.SHORT_SF_DL_BYTES_USED}. "
                                                 f"Actual values: dlc={dlc}, sf_dl_bytes={sf_dl_bytes}")
            sf_dl = sf_dl_bytes[0] ^ (CanPacketType.SINGLE_FRAME.value << 4)
        else:
            if len(sf_dl_bytes) != cls.LONG_SF_DL_BYTES_USED:
                raise InconsistentArgumentsError(f"Invalid length of `sf_dl_bytes` argument for provided DLC. "
                                                 f"Expected length: {cls.LONG_SF_DL_BYTES_USED}. "
                                                 f"Actual values: dlc={dlc}, sf_dl_bytes={sf_dl_bytes}")
            _short_sf_dl = sf_dl_bytes[0] ^ (CanPacketType.SINGLE_FRAME.value << 4) != 0
            if _short_sf_dl != 0:
                raise ValueError(f"Invalid value of `sf_dl_bytes`. Expected first byte is empty when long format is "
                                 f"used. Actual value: {sf_dl_bytes}")
            sf_dl = sf_dl_bytes[1]
        cls.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)


class CanSingleFrameHandler:
    """
    Helper class that provides utilities for Single Frame.

    :ref:`Single Frame <knowledge-base-can-single-frame>` uses
    :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` to inform about payload bytes
    number of a carried diagnostic message.
    """

    @classmethod
    def generate_can_frame_data(cls,
                                addressing_format: CanAddressingFormatAlias,
                                payload: RawBytes,
                                dlc: Optional[int] = None,
                                filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE,
                                target_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Generate data field of a CAN frame that carries a Single Frame packet.

        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param payload: Payload of a diagnostic message that is carried by considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :return: Raw bytes of CAN frame data for the provided Single Frame packet information.
        """
        validate_raw_byte(filler_byte)
        validate_raw_bytes(payload, allow_empty=True)
        ai_data_bytes = CanAddressingInformationHandler.generate_ai_data_bytes(addressing_format=addressing_format,
                                                                               target_address=target_address,
                                                                               address_extension=address_extension)
        frame_dlc = dlc or cls.get_dlc(addressing_format=addressing_format,
                                       payload_length=len(payload))
        data_bytes_number = CanDlcHandler.decode(frame_dlc)
        sf_dl_bytes = CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=len(payload),
                                                                   dlc=frame_dlc,
                                                                   addressing_format=addressing_format)
        sf_data_bytes = ai_data_bytes + sf_dl_bytes + list(payload)
        data_padding = ((data_bytes_number - len(sf_data_bytes)) * [filler_byte])
        return sf_data_bytes + data_padding

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded Single Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Single Frame CAN packet.
        """
        if not cls.is_single_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError(f"Provided `raw_frame_data` value does not carry Single Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data}")
        dlc = CanDlcHandler.encode(len(raw_frame_data))
        sf_dl_bytes = CanSingleFrameDataLengthHandler.extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                                               raw_frame_data=raw_frame_data)
        CanSingleFrameDataLengthHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                                  dlc=dlc,
                                                                  addressing_format=addressing_format)

    @classmethod
    def is_single_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        """
        Check if provided data bytes encodes a Single Frame packet.

        .. note:: The method does not validate the content (e.g. SF_DL parameter) of the packet.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries Single Frame, False otherwise.
        """
        validate_raw_bytes(raw_frame_data)
        ai_data_bytes = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        if len(raw_frame_data) <= ai_data_bytes:
            return False
        return raw_frame_data[ai_data_bytes] >> 4 == CanPacketType.SINGLE_FRAME.value

    @classmethod
    def get_dlc(cls, addressing_format: CanAddressingFormatAlias, payload_length: int) -> int:
        """
        Get the value of a CAN frame DLC that carries a Single Frame packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param payload_length: Number of payload bytes that considered CAN packet carries.

        :return: The lowest value of DLC that enables to fit in provided Single Frame packet data.
        """
        ai_data_bytes = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        cls.__validate_payload_length(payload_length=payload_length, ai_data_bytes_number=ai_data_bytes)
        data_bytes_short_sf_dl = ai_data_bytes + CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED + payload_length
        dlc_with_short_sf_dl = CanDlcHandler.get_min_dlc(data_bytes_short_sf_dl)
        if dlc_with_short_sf_dl <= CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            return dlc_with_short_sf_dl
        data_bytes_long_sf_dl = ai_data_bytes + CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED + payload_length
        return CanDlcHandler.get_min_dlc(data_bytes_long_sf_dl)

    # TODO: consider adding `get_max_payload_length` method to get the maximal number of payload bytes that could be
    #  carried by a Single Frame

    @staticmethod
    def __validate_payload_length(payload_length: int, ai_data_bytes_number: int) -> None:
        """
        Validate value of payload length.

        :param payload_length: Value to validate.
        :param ai_data_bytes_number: Number of data byte that carry Addressing Information.

        :raise TypeError: Provided value is not int type.
        :raise ValueError:
        :raise InconsistentArgumentsError: Provided value is out of range.
        """
        if not isinstance(payload_length, int):
            raise TypeError(f"Provided payload_length value is not int type. Actual type: {type(payload_length)}")
        if payload_length < 0:
            raise ValueError(f"Provided payload_length value is a negative number. Actual value: {payload_length}")
        max_payload_length = CanDlcHandler.MAX_DATA_BYTES_NUMBER - ai_data_bytes_number - \
            CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED
        if payload_length > max_payload_length:
            raise InconsistentArgumentsError(f"Provided payload_length value is too big and it would not be able"
                                             f"to fit into a CAN Frame with currently considered CAN Addressing Format."
                                             f"Expected: payload_length <= {max_payload_length}."
                                             f"Actual value: {payload_length}")

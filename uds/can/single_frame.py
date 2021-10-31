"""
Implementation specific for Single Frame CAN packets.

This module contains implementation of :ref:`Single Frame <knowledge-base-can-single-frame>` packet attributes:
 - :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>`
"""

__all__ = ["CanSingleFrameDataLengthHandler", "CanSingleFrameHandler"]

from typing import Optional

from uds.utilities import RawBytes, RawBytesList, int_to_bytes_list, bytes_list_to_int, \
    validate_raw_byte, validate_nibble, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import CanDlcHandler
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
        CanSingleFrameHandler.validate_single_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        ai_data_bytes = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        dlc = CanDlcHandler.encode(len(raw_frame_data))
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            sf_dl_data_bytes = list(raw_frame_data[ai_data_bytes: ai_data_bytes+cls.SHORT_SF_DL_BYTES_USED])
        else:
            sf_dl_data_bytes = list(raw_frame_data[ai_data_bytes: ai_data_bytes+cls.LONG_SF_DL_BYTES_USED])
        sf_dl_data_bytes[0] ^= (CanPacketType.SINGLE_FRAME.value << 4)
        return bytes_list_to_int(bytes_list=sf_dl_data_bytes)

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

    # TODO: consider adding `validate_sf_dl_data_bytes` method to check whether proper SF_DL format is used.


class CanSingleFrameHandler:
    """
    Helper class that provides utilities for Single Frame.

    :ref:`Single Frame <knowledge-base-can-single-frame>` uses
    :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` to inform about payload bytes
    number of a carried diagnostic message.
    """

    @classmethod
    def is_single_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        """
        Check if
        :param addressing_format:
        :param raw_frame_data:
        :return:
        """

    @classmethod
    def validate_single_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def generate_can_frame_data(cls) -> RawBytesList:
        ...

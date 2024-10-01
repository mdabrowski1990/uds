"""
Implementation specific for First Frame CAN packets.

This module contains implementation specific for :ref:`First Frame <knowledge-base-can-first-frame>` packets - that
includes :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` parameter.
"""

__all__ = ["CanFirstFrameHandler"]

from typing import Optional

from uds.utilities import (
    InconsistentArgumentsError,
    RawBytesAlias,
    RawBytesListAlias,
    bytes_list_to_int,
    int_to_bytes_list,
    validate_raw_bytes,
)

from .addressing_format import CanAddressingFormat
from .addressing_information import CanAddressingInformation
from .frame_fields import CanDlcHandler
from .single_frame import CanSingleFrameHandler


class CanFirstFrameHandler:
    """Helper class that provides utilities for First Frame CAN Packets."""

    FIRST_FRAME_N_PCI: int = 0x1
    """First Frame N_PCI value."""
    MAX_SHORT_FF_DL_VALUE: int = 0xFFF
    """Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` for which
    short format of FF_DL is used."""
    MAX_LONG_FF_DL_VALUE: int = 0xFFFFFFFF
    """Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>`."""
    SHORT_FF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry CAN Packet Type and First Frame Data Length (FF_DL).
    This value is valid only for the short format using FF_DL <= 4095."""
    LONG_FF_DL_BYTES_USED: int = 6
    """Number of CAN Frame data bytes used to carry CAN Packet Type and First Frame Data Length (FF_DL).
    This value is valid only for the long format using FF_DL > 4095."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormat,
                                payload: RawBytesAlias,
                                dlc: int,
                                ff_dl: int,
                                target_address: Optional[int] = None,
                                address_extension: Optional[int] = None) -> RawBytesListAlias:
        """
        Create a data field of a CAN frame that carries a valid First Frame packet.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            Use :meth:`~uds.can.first_frame.CanFirstFrameHandler.create_any_frame_data` to create data bytes
            for a First Frame with any (also incompatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered First Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param ff_dl: Value of First Frame Data Length parameter that is carried by a considered CAN packet.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Provided `payload` contains incorrect number of bytes to fit them into
            a First Frame data field using provided parameters.

        :return: Raw bytes of CAN frame data for the provided First Frame packet information.
        """
        validate_raw_bytes(payload)
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        ff_dl_data_bytes = cls.__encode_valid_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
        ff_data_bytes = list(ai_data_bytes) + list(ff_dl_data_bytes) + list(payload)
        frame_length = CanDlcHandler.decode_dlc(dlc)
        if len(ff_data_bytes) != frame_length:
            raise InconsistentArgumentsError("Provided value of `payload` contains incorrect number of bytes to fit "
                                             f"them into a valid CAN Frame. You can Use {cls.get_payload_size} to get "
                                             f"the expected value.")
        return ff_data_bytes

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormat,
                              payload: RawBytesAlias,
                              dlc: int,
                              ff_dl: int,
                              long_ff_dl_format: bool = False,
                              target_address: Optional[int] = None,
                              address_extension: Optional[int] = None) -> RawBytesListAlias:
        """
        Create a data field of a CAN frame that carries a First Frame packet.

        .. note:: You can use this method to create First Frame data bytes with any (also inconsistent with ISO 15765)
            parameters values.
            It is recommended to use :meth:`~uds.can.first_frame.CanFirstFrameHandler.create_valid_frame_data` to
            create data bytes for a First Frame with valid (compatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered First Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param ff_dl: Value of First Frame Data Length parameter that is carried by a considered CAN packet.
        :param long_ff_dl_format: Information whether to use long or short format of First Frame Data Length.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Provided `payload` contains incorrect number of bytes to fit them into
            a First Frame data field using provided parameters.

        :return: Raw bytes of CAN frame data for the provided First Frame packet information.
        """
        validate_raw_bytes(payload)
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        ff_dl_data_bytes = cls.__encode_any_ff_dl(ff_dl=ff_dl, long_ff_dl_format=long_ff_dl_format)
        ff_data_bytes = list(ai_data_bytes) + list(ff_dl_data_bytes) + list(payload)
        frame_length = CanDlcHandler.decode_dlc(dlc)
        if len(ff_data_bytes) != frame_length:
            raise InconsistentArgumentsError("Provided value of `payload` contains incorrect number of bytes to fit "
                                             f"them into a valid CAN Frame. You can Use {cls.get_payload_size} to get "
                                             f"the expected value.")
        return ff_data_bytes

    @classmethod
    def is_first_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> bool:
        """
        Check if provided data bytes encodes a First Frame packet.

        .. warning:: The method does not validate the content (e.g. FF_DL parameter) of the packet.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries First Frame, False otherwise.
        """
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        return raw_frame_data[ai_bytes_number] >> 4 == cls.FIRST_FRAME_N_PCI

    @classmethod
    def decode_payload(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> RawBytesListAlias:
        """
        Extract a value of payload from First Frame data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Payload bytes of a diagnostic message carried by a considered First Frame.
        """
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        ff_dl_data_bytes = cls.__extract_ff_dl_data_bytes(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        return list(raw_frame_data[ai_bytes_number + len(ff_dl_data_bytes):])

    @classmethod
    def decode_ff_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> int:
        """
        Extract a value of First Frame Data Length from First Frame data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise NotImplementedError: There is missing implementation for the provided First Frame Data Length format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Extracted value of First Frame Data Length.
        """
        ff_dl_bytes = cls.__extract_ff_dl_data_bytes(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        if len(ff_dl_bytes) == cls.SHORT_FF_DL_BYTES_USED:
            ff_dl_bytes[0] = ff_dl_bytes[0] & 0xF
            return bytes_list_to_int(ff_dl_bytes[-4:])
        if len(ff_dl_bytes) == cls.LONG_FF_DL_BYTES_USED:
            return bytes_list_to_int(ff_dl_bytes[-4:])
        raise NotImplementedError("Unknown format of First Frame Data Length was found.")

    @classmethod
    def get_payload_size(cls,
                         addressing_format: CanAddressingFormat,
                         dlc: int,
                         long_ff_dl_format: bool = False) -> int:
        """
        Get the size of a payload that can fit into First Frame data bytes.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param long_ff_dl_format: Information whether to use long or short format of First Frame Data Length.

        :raise ValueError: First Frame packet cannot use provided attributes according to ISO 15765.

        :return: The maximum number of payload bytes that could fit into a considered First Frame.
        """
        if dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
            raise ValueError(f"First Frame must use DLC >= {CanDlcHandler.MIN_BASE_UDS_DLC}. "
                             f"Actual value: dlc={dlc}")
        data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        ai_data_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        ff_dl_data_bytes_number = cls.LONG_FF_DL_BYTES_USED if long_ff_dl_format else cls.SHORT_FF_DL_BYTES_USED
        return data_bytes_number - ai_data_bytes_number - ff_dl_data_bytes_number

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytesAlias) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded First Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a First Frame CAN packet.
        """
        validate_raw_bytes(raw_frame_data)
        if not cls.is_first_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError(f"Provided `raw_frame_data` value does not carry a First Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data}")
        ff_dl = cls.decode_ff_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        ff_dl_data_bytes = cls.__extract_ff_dl_data_bytes(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        is_long_ff_dl_used = len(ff_dl_data_bytes) == cls.LONG_FF_DL_BYTES_USED
        dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
        cls.validate_ff_dl(ff_dl=ff_dl,
                           long_ff_dl_format=is_long_ff_dl_used,
                           dlc=dlc,
                           addressing_format=addressing_format)

    @classmethod
    def validate_ff_dl(cls,
                       ff_dl: int,
                       long_ff_dl_format: Optional[bool] = None,
                       dlc: Optional[int] = None,
                       addressing_format: Optional[CanAddressingFormat] = None) -> None:
        """
        Validate a value of First Frame Data Length.

        :param ff_dl: First Frame Data Length value to validate.
        :param long_ff_dl_format: Information whether long or short format of First Frame Data Length is used.

            - None - do not perform compatibility check with the FF_DL format
            - True - perform compatibility check with long FF_DL format
            - False - perform compatibility check with short FF_DL format

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
            raise TypeError(f"Provided value of First Frame Data Length is not integer. Actual type: {type(ff_dl)}")
        if not 0 <= ff_dl <= cls.MAX_LONG_FF_DL_VALUE:
            raise ValueError(f"Provided value of First Frame Data Length is out of range. "
                             f"Expected: 0 <= ff_dl <= {cls.MAX_LONG_FF_DL_VALUE}. Actual value: {ff_dl}")
        if dlc is not None and addressing_format is not None:
            if dlc < CanDlcHandler.MIN_BASE_UDS_DLC:
                raise ValueError(f"Provided value of DLC cannot be used with First Frame. "
                                 f"Expected: dlc >= {CanDlcHandler.MIN_BASE_UDS_DLC}. "
                                 f"Actual value: {dlc}")
            max_sf_dl = CanSingleFrameHandler.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
            if ff_dl <= max_sf_dl:
                raise InconsistentArgumentsError(f"Single Frame shall be used instead of First Frame to carry payload "
                                                 f"consisting of {ff_dl} data bytes.")
        if long_ff_dl_format is not None:
            if (long_ff_dl_format and ff_dl <= cls.MAX_SHORT_FF_DL_VALUE) \
                    or (not long_ff_dl_format and ff_dl > cls.MAX_SHORT_FF_DL_VALUE):
                raise InconsistentArgumentsError(f"Provided value of First Frame Data Length is not compatible with "
                                                 f"the format used. Actual values: ff_dl={ff_dl}, "
                                                 f"long_ff_dl_format={long_ff_dl_format}")

    @classmethod
    def __extract_ff_dl_data_bytes(cls,
                                   addressing_format: CanAddressingFormat,
                                   raw_frame_data: RawBytesAlias) -> RawBytesListAlias:
        """
        Extract data bytes that carries CAN Packet Type and First Frame Data Length parameters.

        .. warning:: This method does not check whether provided `raw_frame_data` actually contains First Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Extracted data bytes with CAN Packet Type and First Frame Data Length parameters.
        """
        ai_bytes_number = CanAddressingInformation.get_ai_data_bytes_number(addressing_format)
        ff_dl_short = list(raw_frame_data[ai_bytes_number:][:cls.SHORT_FF_DL_BYTES_USED])
        if ff_dl_short[0] & 0xF != 0 or ff_dl_short[1] != 0x00:
            return ff_dl_short
        ff_dl_long = list(raw_frame_data[ai_bytes_number:][:cls.LONG_FF_DL_BYTES_USED])
        return ff_dl_long

    @classmethod
    def __encode_valid_ff_dl(cls,
                             ff_dl: int,
                             dlc: int,
                             addressing_format: CanAddressingFormat) -> RawBytesListAlias:
        """
        Create First Frame data bytes with CAN Packet Type and First Frame Data Length parameters.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            First Frame Data Length value validation (whether it is too low according to ISO 15765) is not performed
            though.

        :param ff_dl: Value to put into a slot of First Frame Data Length.
        :param dlc: Value of DLC to use for First Frame Data Length value validation.
        :param addressing_format: Value of CAN Addressing Format to use for First Frame Data Length value validation.

        :return: First Frame data bytes containing CAN Packet Type and First Frame Data Length parameters.
        """
        cls.validate_ff_dl(ff_dl=ff_dl, dlc=dlc, addressing_format=addressing_format)
        return cls.__encode_any_ff_dl(ff_dl=ff_dl, long_ff_dl_format=ff_dl > cls.MAX_SHORT_FF_DL_VALUE)

    @classmethod
    def __encode_any_ff_dl(cls, ff_dl: int, long_ff_dl_format: bool = False) -> RawBytesListAlias:
        """
        Create First Frame data bytes with CAN Packet Type and First Frame Data Length parameters.

        .. note:: This method can be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

        :param ff_dl: Value to put into a slot of First Frame Data Length.
        :param long_ff_dl_format: Information whether to use long or short format of First Frame Data Length.

        :raise ValueError: Provided First Frame Data Length value is out of the parameter values range.
        :raise InconsistentArgumentsError: Provided First Frame Data Length value cannot fit into the short format.

        :return: First Frame data bytes containing CAN Packet Type and First Frame Data Length parameters.
        """
        cls.validate_ff_dl(ff_dl=ff_dl)
        if long_ff_dl_format:
            ff_dl_bytes = int_to_bytes_list(int_value=ff_dl, list_size=cls.LONG_FF_DL_BYTES_USED)
            ff_dl_bytes[0] ^= (cls.FIRST_FRAME_N_PCI << 4)
            return ff_dl_bytes
        if ff_dl > cls.MAX_SHORT_FF_DL_VALUE:
            raise InconsistentArgumentsError(f"Provided value of First Frame Data Length is too big for the short "
                                             f"FF_DL format. Use lower FF_DL value or change to long format. "
                                             f"Actual value: {ff_dl}")
        ff_dl_bytes = int_to_bytes_list(int_value=ff_dl, list_size=cls.SHORT_FF_DL_BYTES_USED)
        ff_dl_bytes[0] ^= (cls.FIRST_FRAME_N_PCI << 4)
        return ff_dl_bytes

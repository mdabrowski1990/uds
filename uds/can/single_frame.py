"""
Implementation specific for Single Frame CAN packets.

This module contains implementation specific for :ref:`Single Frame <knowledge-base-can-single-frame>` packets - that
includes :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` parameter.
"""

__all__ = ["CanSingleFrameHandler"]

from typing import Optional

from uds.utilities import Nibble, RawByte, RawBytes, RawBytesList, \
    validate_raw_bytes, validate_raw_byte, validate_nibble, InconsistentArgumentsError
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .can_frame_fields import DEFAULT_FILLER_BYTE, CanDlcHandler


class CanSingleFrameHandler:
    """Helper class that provides utilities for Single Frame CAN Packets."""

    SINGLE_FRAME_N_PCI: Nibble = 0
    """N_PCI value of Single Frame."""
    MAX_DLC_VALUE_SHORT_SF_DL: int = 8
    """Maximum value of DLC for which short
    :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>` format shall be used."""
    SHORT_SF_DL_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry CAN Packet Type and Single Frame Data Length (SF_DL).
    This value is valid only for the short format using DLC <= 8."""
    LONG_SF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry CAN Packet Type and Single Frame Data Length (SF_DL).
    This value is valid only for the long format using DLC > 8."""

    @classmethod
    def create_valid_frame_data(cls, *,
                                addressing_format: CanAddressingFormatAlias,
                                payload: RawBytes,
                                dlc: Optional[int] = None,
                                filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                                target_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Create a data field of a CAN frame that carries a valid Single Frame packet.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.
            Use :meth:`~uds.can.single_frame.CanSingleFrameHandler.create_any_frame_data` to create data bytes
            for a Single Frame with any (also incompatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Single Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill the unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Provided `payload` contains invalid number of bytes to fit it into
            a properly defined Single Frame data field.

        :return: Raw bytes of CAN frame data for the provided Single Frame packet information.
        """
        validate_raw_byte(filler_byte)
        validate_raw_bytes(payload, allow_empty=False)
        ai_data_bytes = CanAddressingInformationHandler.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                             target_address=target_address,
                                                                             address_extension=address_extension)
        frame_dlc = cls.get_min_dlc(addressing_format=addressing_format, payload_length=len(payload)) \
            if dlc is None else dlc
        frame_data_bytes_number = CanDlcHandler.decode_dlc(frame_dlc)
        sf_dl_bytes = cls.__encode_valid_sf_dl(sf_dl=len(payload),
                                               dlc=frame_dlc,
                                               addressing_format=addressing_format)
        sf_bytes = ai_data_bytes + sf_dl_bytes + list(payload)
        if len(sf_bytes) > frame_data_bytes_number:
            raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes to fit in. "
                                             "Consider increasing DLC value.")
        data_bytes_to_pad = frame_data_bytes_number - len(sf_bytes)
        if data_bytes_to_pad > 0:
            if dlc is not None and dlc < CanDlcHandler.MIN_DLC_DATA_PADDING:
                raise InconsistentArgumentsError(f"CAN Frame Data Padding shall not be used for CAN frames with "
                                                 f"DLC < {CanDlcHandler.MIN_DLC_DATA_PADDING}. Actual value: dlc={dlc}")
            return sf_bytes + data_bytes_to_pad * [filler_byte]
        return sf_bytes

    @classmethod
    def create_any_frame_data(cls, *,
                              addressing_format: CanAddressingFormatAlias,
                              payload: RawBytes,
                              dlc: int,
                              sf_dl_short: Nibble,
                              sf_dl_long: Optional[RawByte] = None,
                              filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                              target_address: Optional[RawByte] = None,
                              address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Create a data field of a CAN frame that carries a Single Frame packet.

        .. note:: You can use this method to create Single Frame data bytes with any (also inconsistent with ISO 15765)
            parameters values.
            It is recommended to use :meth:`~uds.can.single_frame.CanSingleFrameHandler.create_valid_frame_data` to
            create data bytes for a Single Frame with valid (compatible with ISO 15765) parameters values.

        :param addressing_format: CAN addressing format used by a considered Single Frame.
        :param payload: Payload of a diagnostic message that is carried by a considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
        :param sf_dl_short: Value to put into a slot of Single Frame Data Length in short format.
        :param sf_dl_long: Value to put into a slot of Single Frame Data Length in long format.
            Leave None to use short (1-byte-long) format of Single Frame Data Length.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise InconsistentArgumentsError: Provided `payload` contains too many bytes to fit it into a Single Frame
            data field.

        :return: Raw bytes of CAN frame data for the provided Single Frame packet information.
        """
        validate_raw_byte(filler_byte)
        validate_raw_bytes(payload, allow_empty=True)
        ai_data_bytes = CanAddressingInformationHandler.encode_ai_data_bytes(addressing_format=addressing_format,
                                                                             target_address=target_address,
                                                                             address_extension=address_extension)
        frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
        sf_dl_bytes = cls.__encode_any_sf_dl(sf_dl_short=sf_dl_short,
                                             sf_dl_long=sf_dl_long)
        sf_bytes = ai_data_bytes + sf_dl_bytes + list(payload)
        if len(sf_bytes) > frame_data_bytes_number:
            raise InconsistentArgumentsError("Provided value of `payload` contains of too many bytes to fit in. "
                                             "Consider increasing DLC value.")
        data_padding = ((frame_data_bytes_number - len(sf_bytes)) * [filler_byte])
        return sf_bytes + data_padding

    @classmethod
    def is_single_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        """
        Check if provided data bytes encodes a Single Frame packet.

        .. warning:: The method does not validate the content (e.g. SF_DL parameter) of the provided frame data bytes.
            Only, :ref:`CAN Packet Type (N_PCI) <knowledge-base-can-n-pci>` parameter is checked whether contain
            Single Frame N_PCI value.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to check.

        :return: True if provided data bytes carries Single Frame, False otherwise.
        """
        ai_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        return (raw_frame_data[ai_bytes_number] >> 4) == cls.SINGLE_FRAME_N_PCI

    @classmethod
    def decode_payload(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> RawBytesList:
        """
        Extract diagnostic message payload from Single Frame data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Payload bytes of a diagnostic message carried by a considered Single Frame.
        """
        sf_dl = cls.decode_sf_dl(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        ai_data_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
        sf_dl_bytes_number = cls.get_sf_dl_bytes_number(dlc)
        return list(raw_frame_data[ai_data_bytes_number + sf_dl_bytes_number:][:sf_dl])

    @classmethod
    def decode_sf_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        """
        Extract a value of Single Frame Data Length from Single Frame data bytes.

        .. warning:: The method does not validate the content of the provided frame data bytes.
            There is no guarantee of the proper output when frame data in invalid format (incompatible with
            ISO 15765) is provided.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :raise NotImplementedError: The provided data of Single Frame packet are valid, but the format of Single Frame
            Data Length is missing the implementation.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: Extracted value of Single Frame Data Length.
        """
        sf_dl_data_bytes = cls.__extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        if len(sf_dl_data_bytes) == cls.SHORT_SF_DL_BYTES_USED:
            return sf_dl_data_bytes[0] & 0xF
        if len(sf_dl_data_bytes) == cls.LONG_SF_DL_BYTES_USED:
            return sf_dl_data_bytes[1]
        raise NotImplementedError("Unknown format of Single Frame Data Length was found.")

    @classmethod
    def get_min_dlc(cls, addressing_format: CanAddressingFormatAlias, payload_length: int) -> int:
        """
        Get the minimum value of a CAN frame DLC to carry a Single Frame packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param payload_length: Number of payload bytes that considered CAN packet carries.

        :return: The lowest value of DLC that enables to fit in provided Single Frame packet data.
        """
        ai_data_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        cls.__validate_payload_length(payload_length=payload_length, ai_data_bytes_number=ai_data_bytes_number)
        data_bytes_short_sf_dl = ai_data_bytes_number + cls.SHORT_SF_DL_BYTES_USED + payload_length
        dlc_with_short_sf_dl = CanDlcHandler.get_min_dlc(data_bytes_short_sf_dl)
        if dlc_with_short_sf_dl <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            return dlc_with_short_sf_dl
        data_bytes_long_sf_dl = ai_data_bytes_number + cls.LONG_SF_DL_BYTES_USED + payload_length
        return CanDlcHandler.get_min_dlc(data_bytes_long_sf_dl)

    @classmethod
    def get_max_payload_size(cls,
                             addressing_format: Optional[CanAddressingFormatAlias] = None,
                             dlc: Optional[int] = None) -> int:
        """
        Get the maximum size of a payload that can fit into Single Frame data bytes.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
            Leave None to get the result for CAN addressing format that does not use data bytes for carrying
            addressing information.
        :param dlc: DLC value of a CAN frame that carries a considered CAN Packet.
            Leave None to get the result for the greatest possible DLC value.

        :raise InconsistentArgumentsError: Single Frame packet cannot use provided attributes according to ISO 15765.

        :return: The maximum number of payload bytes that could fit into a considered Single Frame.
        """
        if dlc is not None:
            frame_data_bytes_number = CanDlcHandler.decode_dlc(dlc)
            sf_dl_bytes_number = cls.get_sf_dl_bytes_number(dlc)
        else:
            frame_data_bytes_number = CanDlcHandler.MAX_DATA_BYTES_NUMBER
            sf_dl_bytes_number = cls.LONG_SF_DL_BYTES_USED
        ai_data_bytes_number = 0 if addressing_format is None else \
            CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        output = frame_data_bytes_number - ai_data_bytes_number - sf_dl_bytes_number
        if output <= 0:
            raise InconsistentArgumentsError(f"Provided values cannot be used to transmit a valid Single Frame packet. "
                                             f"Consider using greater DLC value or changing the CAN Addressing Format. "
                                             f"Actual values: dlc={dlc}, addressing_format={addressing_format}")
        return output

    @classmethod
    def get_sf_dl_bytes_number(cls, dlc: int) -> int:
        """
        Get number of data bytes used for carrying CAN Packet Type and Single Frame Data Length parameters.

        :param dlc: DLC value of a considered CAN frame.

        :return: The number of bytes used for carrying CAN Packet Type and Single Frame Data Length parameters.
        """
        CanDlcHandler.validate_dlc(dlc)
        return cls.SHORT_SF_DL_BYTES_USED if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL else cls.LONG_SF_DL_BYTES_USED

    @classmethod
    def validate_frame_data(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        """
        Validate whether data field of a CAN Packet carries a properly encoded Single Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a CAN frame to validate.

        :raise ValueError: Provided frame data of a CAN frames does not carry a Single Frame CAN packet.
        :raise InconsistentArgumentsError: Provided frame data of a CAN frames does not carry a properly encoded
            Single Frame CAN packet.
        """
        validate_raw_bytes(raw_frame_data)
        if not cls.is_single_frame(addressing_format=addressing_format, raw_frame_data=raw_frame_data):
            raise ValueError(f"Provided `raw_frame_data` value does not carry a Single Frame packet. "
                             f"Actual values: addressing_format={addressing_format}, raw_frame_data={raw_frame_data}")
        ai_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        sf_dl_data_bytes = cls.__extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        data_bytes_number = len(raw_frame_data)
        dlc = CanDlcHandler.encode_dlc(data_bytes_number)
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            sf_dl = sf_dl_data_bytes[0] & 0xF
            if ai_bytes_number + cls.SHORT_SF_DL_BYTES_USED + sf_dl != data_bytes_number:
                raise InconsistentArgumentsError("Value of Single Frame Data Length does not match the number of "
                                                 "payload bytes carried by the Single Frame packet.")
        else:
            if sf_dl_data_bytes[0] & 0xF != 0:
                raise InconsistentArgumentsError(f"Value of Single Frame Data Length must use 0x00 at the first byte  "
                                                 f"when long SF_DL format is used. Actual value: {sf_dl_data_bytes[0]}")
            sf_dl = sf_dl_data_bytes[1]
            if ai_bytes_number + cls.LONG_SF_DL_BYTES_USED + sf_dl > data_bytes_number:
                raise InconsistentArgumentsError("Value of Single Frame Data Length is greater than number of "
                                                 "payload bytes carried by the Single Frame packet.")

    @classmethod
    def validate_sf_dl(cls,
                       sf_dl: int,
                       dlc: int,
                       addressing_format: Optional[CanAddressingFormatAlias] = None) -> None:
        """
        Validate a value of Single Frame Data Length.

        :param sf_dl: Single Frame Data Length value to validate.
        :param dlc: DLC value to validate.
        :param addressing_format: Value of CAN Addressing Format to use for Single Frame Data Length value validation.
            Leave None if you do not want to validate whether payload can fit into a CAN Frame with considered DLC.

        :raise TypeError: Provided value of Single Frame Data Length is not integer.
        :raise ValueError: Provided value of Single Frame Data Length is too small.
        :raise InconsistentArgumentsError: It is impossible for a Single Frame with provided DLC to contain as many
            payload bytes as the provided value of Single Frame Data Length.
        """
        if not isinstance(sf_dl, int):
            raise TypeError(f"Provided value of Single Frame Data Length is not int type. Actual type: {type(sf_dl)}")
        if sf_dl <= 0:
            raise ValueError(f"Provided value of Single Frame Data Length is too small (<1). Actual value: {sf_dl}")
        max_sf_dlc = cls.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        if sf_dl > max_sf_dlc:
            raise InconsistentArgumentsError(f"Provided value of `sf_dl` is greater than maximum valid value of "
                                             f"Single Frame Data Length for provided DLC and Addressing Format."
                                             f"Actual values: sf_dl={sf_dl}, dlc={dlc}, "
                                             f"addressing_format={addressing_format}. "
                                             f"Expected: sf_dl<={max_sf_dlc}")

    @classmethod
    def __validate_payload_length(cls, payload_length: int, ai_data_bytes_number: int) -> None:
        """
        Validate value of payload length.

        :param payload_length: Value to validate.
        :param ai_data_bytes_number: Number of data byte that carry Addressing Information.

        :raise TypeError: Provided value of payload length is not integer.
        :raise ValueError: Provided value of payload length is less or equal to 0.
        :raise InconsistentArgumentsError: Provided value of payload length is greater than maximum value.
        """
        if not isinstance(payload_length, int):
            raise TypeError(f"Provided `payload_length` value is not int type. Actual type: {type(payload_length)}")
        if payload_length <= 0:
            raise ValueError(f"Provided `payload_length` value is not a positive value. Actual value: {payload_length}")
        max_payload_length = CanDlcHandler.MAX_DATA_BYTES_NUMBER - ai_data_bytes_number - cls.LONG_SF_DL_BYTES_USED
        if payload_length > max_payload_length:
            raise InconsistentArgumentsError(f"Provided payload_length value is too big and it would not be able"
                                             f"to fit into a CAN Frame with currently considered CAN Addressing Format."
                                             f"Expected: payload_length <= {max_payload_length}."
                                             f"Actual value: {payload_length}")

    @classmethod
    def __extract_sf_dl_data_bytes(cls,
                                   addressing_format: CanAddressingFormat,
                                   raw_frame_data: RawBytes) -> RawBytesList:
        """
        Extract data bytes that carries CAN Packet Type and Single Frame Data Length parameters.

        .. warning:: This method does not check whether provided `raw_frame_data` actually contains Single Frame.

        :param addressing_format: CAN Addressing Format used.
        :param raw_frame_data: Raw data bytes of a considered CAN frame.

        :return: Extracted data bytes with CAN Packet Type and Single Frame Data Length parameters.
        """
        dlc = CanDlcHandler.encode_dlc(len(raw_frame_data))
        ai_bytes_number = CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format)
        return list(raw_frame_data[ai_bytes_number:])[:cls.get_sf_dl_bytes_number(dlc)]

    @classmethod
    def __encode_valid_sf_dl(cls,
                             sf_dl: int,
                             dlc: int,
                             addressing_format: CanAddressingFormatAlias) -> RawBytesList:
        """
        Create Single Frame data bytes with CAN Packet Type and Single Frame Data Length parameters.

        .. note:: This method can only be used to create a valid (compatible with ISO 15765 - Diagnostic on CAN) output.

        :param sf_dl: Number of payload bytes carried by a considered Single Frame.
        :param dlc: DLC value of a CAN Frame to carry this information.
        :param addressing_format: Value of CAN Addressing Format to use for Single Frame Data Length value validation.

        :return: Single Frame data bytes containing CAN Packet Type and Single Frame Data Length parameters.
        """
        cls.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            return cls.__encode_any_sf_dl(sf_dl_short=sf_dl)
        return cls.__encode_any_sf_dl(sf_dl_long=sf_dl)

    @classmethod
    def __encode_any_sf_dl(cls, sf_dl_short: Nibble = 0, sf_dl_long: Optional[RawByte] = None) -> RawBytesList:
        """
        Create Single Frame data bytes with CAN Packet Type and Single Frame Data Length parameters.

        .. note:: This method can be used to create any (also incompatible with ISO 15765 - Diagnostic on CAN) output.

        :param sf_dl_short: Value to put into a slot of Single Frame Data Length in short format.
        :param sf_dl_long: Value to put into a slot of Single Frame Data Length in long format.
            Leave None to use short (1-byte-long) format of Single Frame Data Length.

        :return: Single Frame data bytes containing CAN Packet Type and Single Frame Data Length parameters.
        """
        validate_nibble(sf_dl_short)
        sf_dl_byte_0 = sf_dl_short ^ (cls.SINGLE_FRAME_N_PCI << 4)
        if sf_dl_long is None:
            return [sf_dl_byte_0]
        validate_raw_byte(sf_dl_long)
        return [sf_dl_byte_0, sf_dl_long]

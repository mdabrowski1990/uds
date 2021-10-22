"""
CAN bus specific implementation of UDS packets.

This module contains implementation of :ref:`CAN packets <knowledge-base-uds-can-packet>`:
 - :ref:`Single Frame <knowledge-base-can-single-frame>`
 - :ref:`First Frame <knowledge-base-can-first-frame>`
 - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
 - :ref:`Flow Control <knowledge-base-can-flow-control>`
"""

__all__ = ["CanPacket", "CanPacketRecord"]

from typing import Optional, Any
from warnings import warn

from uds.transmission_attributes import AddressingType, AddressingTypeMemberTyping
from uds.utilities import RawByte, RawBytes, RawBytesTuple, validate_raw_byte, validate_raw_bytes, \
    InconsistentArgumentsError, AmbiguityError, UnusedArgumentError, UnusedArgumentWarning

from .abstract_packet import AbstractUdsPacket, AbstractUdsPacketRecord
from .can_packet_attributes import DEFAULT_FILLER_BYTE, CanAddressingFormat, CanAddressingFormatTyping, \
    CanPacketType, CanPacketTypeMemberTyping, CanIdHandler, CanDlcHandler
from .can_flow_control import CanFlowStatus, CanFlowStatusTyping, CanSTminTranslator


class CanPacket(AbstractUdsPacket):
    """
    Definition of a CAN packet.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`CAN packet <knowledge-base-uds-can-packet>`.
    """

    MAX_DLC_VALUE_SHORT_SF_DL: int = 8
    """Maximum value of DLC for which short
    :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>` format is used."""
    MIN_DLC_VALUE_FF: int = 8
    """Minimum value of DLC for :ref:`First Frame <knowledge-base-can-first-frame>` Packet Type."""

    MAX_SHORT_FF_DL_VALUE: int = 0xFFF
    """Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` for which
    short format of FF_DL is used."""
    MAX_LONG_FF_DL_VALUE: int = 0xFFFFFFFF
    """Maximum value of :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>`."""
    MIN_SEQUENCE_NUMBER: int = 0x0
    """Minimum value of :ref:`Sequence Number <knowledge-base-can-sequence-number>`."""
    MAX_SEQUENCE_NUMBER: int = 0xF
    """Maximum value of :ref:`Sequence Number <knowledge-base-can-sequence-number>`."""

    SHORT_SF_DL_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` values in 
    :ref:`Single Frame <knowledge-base-can-single-frame>` packets with DLC <= 8."""
    LONG_SF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Single Frame Data Length (SF_DL) <knowledge-base-can-single-frame-data-length>` values in 
    :ref:`Single Frame <knowledge-base-can-single-frame>` packets with DLC > 8."""
    SHORT_FF_DL_BYTES_USED: int = 2
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` and 
    :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` values in 
    :ref:`First Frame <knowledge-base-can-first-frame>` when FF_DL <= 4095."""
    LONG_FF_DL_BYTES_USED: int = 6
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` and 
    :ref:`First Frame Data Length (FF_DL) <knowledge-base-can-first-frame-data-length>` values in 
    :ref:`First Frame <knowledge-base-can-first-frame>` when FF_DL > 4095."""
    SN_BYTES_USED: int = 1
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>` 
    and :ref:`Sequence Number <knowledge-base-can-sequence-number>` values in
    :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`."""
    FS_BYTES_USED: int = 3
    """Number of CAN Frame data bytes used to carry :ref:`CAN Packet Type <knowledge-base-can-n-pci>`,
    :ref:`Flow Status <knowledge-base-can-flow-status>`, :ref:`Block Size <knowledge-base-can-block-size>` and
    :ref:`Separation Time minimum <knowledge-base-can-st-min>` in :ref:`Flow Control <knowledge-base-can-flow-control>`
    packets."""

    def __init__(self, *,
                 packet_type: CanPacketTypeMemberTyping,
                 addressing_format: CanAddressingFormatTyping,
                 addressing: AddressingTypeMemberTyping,
                 can_id: Optional[int] = None,
                 target_address: Optional[RawByte] = None,
                 source_address: Optional[RawByte] = None,
                 address_extension: Optional[RawByte] = None,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Create a storage for a single CAN packet.

        :param packet_type: Type of this CAN packet.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            Leave None if other arguments unambiguously determine CAN ID value.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter
            or the value of Target Address was provided in `can_id` parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Source Address parameter
            or the value of Source Address was provided in `can_id` parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Address Extension parameter.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
            You have to provide DLC value for packets of First Frame type.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by this CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes of a diagnostic message initiated by this First Frame packet.
             - :parameter sequence_number: (required for: CF)
                 Sequence number value of this Consecutive Frame.
             - :parameter flow_status: (required for: FC)
                 Flow status information carried by this Flow Control frame.
             - :parameter block_size: (optional for: FC)
                 Block size information carried by this Flow Control frame.
             - :parameter stmin: (optional for: FC)
                 Separation Time minimum information carried by this Flow Control frame.
        """
        self.__raw_frame_data: RawBytesTuple = None  # type: ignore
        self.__addressing: AddressingType = None  # type: ignore
        self.__addressing_format: CanAddressingFormat = None  # type: ignore
        self.__packet_type: CanPacketType = None  # type: ignore
        self.__can_id: int = None  # type: ignore
        self.__dlc: int = None  # type: ignore
        self.__target_address: Optional[RawByte] = None
        self.__address_extension: Optional[RawByte] = None
        self.set_address_information(addressing=addressing,
                                     addressing_format=addressing_format,
                                     can_id=can_id,
                                     target_address=target_address,
                                     source_address=source_address,
                                     address_extension=address_extension)
        self.set_packet_data(packet_type=packet_type,
                             dlc=dlc,
                             filler_byte=filler_byte,
                             **packet_type_specific_kwargs)

    @classmethod
    def get_can_frame_dlc(cls,
                          packet_type: CanPacketType,
                          addressing_format: CanAddressingFormatTyping,
                          payload_length: Optional[int] = None,
                          data_length: Optional[int] = None) -> int:
        """
        Get value of a CAN frame DLC that carries a CAN packet.

        :param packet_type: Type of considered CAN packet.
        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param payload_length: Number of payload bytes that considered CAN packet carries.
            This parameter is only used with Single Frame, First Frame and Consecutive Frame packet type,
            otherwise ignored.
        :param data_length: Number of payload bytes of a diagnostic message initiated by considered First Frame.
            This parameter is only used with First Frame packet type, otherwise ignored.

        :raise NotImplementedError: A valid packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: The value of DLC that enables to fit in provided packet data.
            If multiple DLC values are valid, then the lowest is provided.
        """
        CanPacketType.validate_member(packet_type)
        packet_type_instance = CanPacketType(packet_type)
        if packet_type_instance == CanPacketType.SINGLE_FRAME:
            return cls.get_can_frame_dlc_single_frame(addressing_format=addressing_format,
                                                      payload_length=payload_length)
        elif packet_type_instance == CanPacketType.FIRST_FRAME:
            return cls.get_can_frame_dlc_first_frame(addressing_format=addressing_format,
                                                     payload_length=payload_length,
                                                     data_length=data_length)
        elif packet_type_instance == CanPacketType.CONSECUTIVE_FRAME:
            return cls.get_can_frame_dlc_consecutive_frame(addressing_format=addressing_format,
                                                           payload_length=payload_length)
        elif packet_type_instance == CanPacketType.FLOW_CONTROL:
            return cls.get_can_frame_dlc_flow_control(addressing_format=addressing_format)
        raise NotImplementedError(f"Missing implementation for: {packet_type_instance}")

    @classmethod
    def create_can_frame_data(cls, *,
                              packet_type: CanPacketTypeMemberTyping,
                              addressing_format: CanAddressingFormatTyping,
                              dlc: Optional[int] = None,
                              filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE,
                              target_address: Optional[RawByte] = None,
                              address_extension: Optional[RawByte] = None,
                              **packet_type_specific_kwargs: Any) -> RawBytesTuple:
        """
        Create data field of a CAN frame that carries a CAN packet.

        :param packet_type: Type of considered CAN packet.
        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
            You have to provide DLC value for packets of First Frame type.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by considered CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes of a diagnostic message initiated by considered First Frame packet.
             - :parameter sequence_number: (required for: CF)
                 Sequence number value of considered Consecutive Frame.
             - :parameter flow_status: (required for: FC)
                 Flow status information carried by considered Flow Control frame.
             - :parameter block_size: (optional for: FC)
                 Block size information carried by considered Flow Control frame.
             - :parameter stmin: (optional for: FC)
                 Separation Time minimum information carried by considered Flow Control frame.

        :raise NotImplementedError: A valid packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: Raw bytes of CAN frame data for the provided CAN packet information.
        """
        CanPacketType.validate_member(packet_type)
        packet_type_instance = CanPacketType(packet_type)
        if packet_type_instance == CanPacketType.SINGLE_FRAME:
            return cls.create_can_frame_data_single_frame(addressing_format=addressing_format,
                                                          dlc=dlc,
                                                          filler_byte=filler_byte,
                                                          target_address=target_address,
                                                          address_extension=address_extension,
                                                          **packet_type_specific_kwargs)
        if packet_type_instance == CanPacketType.FIRST_FRAME:
            return cls.create_can_frame_data_first_frame(addressing_format=addressing_format,
                                                         dlc=dlc,
                                                         target_address=target_address,
                                                         address_extension=address_extension,
                                                         **packet_type_specific_kwargs)
        if packet_type_instance == CanPacketType.CONSECUTIVE_FRAME:
            return cls.create_can_frame_data_consecutive_frame(addressing_format=addressing_format,
                                                               dlc=dlc,
                                                               filler_byte=filler_byte,
                                                               target_address=target_address,
                                                               address_extension=address_extension,
                                                               **packet_type_specific_kwargs)
        if packet_type_instance == CanPacketType.FLOW_CONTROL:
            return cls.create_can_frame_data_flow_control(addressing_format=addressing_format,
                                                          dlc=dlc,
                                                          filler_byte=filler_byte,
                                                          target_address=target_address,
                                                          address_extension=address_extension,
                                                          **packet_type_specific_kwargs)
        raise NotImplementedError(f"Missing implementation for: {packet_type_instance}")

    @classmethod
    def validate_address_information(cls,
                                     addressing_format: CanAddressingFormatTyping,
                                     addressing: AddressingTypeMemberTyping,
                                     can_id: Optional[int] = None,
                                     target_address: Optional[RawByte] = None,
                                     source_address: Optional[RawByte] = None,
                                     address_extension: Optional[RawByte] = None) -> None:
        """
        Validate addressing information arguments.

        This methods performs comprehensive check of :ref:`Network Addressing Information (N_AI) <knowledge-base-n-ai>`
        for :ref:`CAN Packet <knowledge-base-uds-can-packet>` to make sure that every required argument is provided
        and their values are consistent with provided :ref:`CAN Addressing Format <knowledge-base-can-addressing>`.

        :param addressing_format: CAN addressing format value to validate.
        :param addressing: Addressing type value to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise NotImplementedError: A valid packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        CanAddressingFormat.validate_member(addressing_format)
        addressing_format_instance = CanAddressingFormat(addressing_format)
        if addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            cls.__validate_ai_normal_11bit(addressing=addressing,
                                           can_id=can_id,
                                           target_address=target_address,
                                           source_address=source_address,
                                           address_extension=address_extension)
        elif addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            cls.__validate_ai_normal_fixed(addressing=addressing,
                                           can_id=can_id,
                                           target_address=target_address,
                                           source_address=source_address,
                                           address_extension=address_extension)
        elif addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            cls.__validate_ai_extended(addressing=addressing,
                                       can_id=can_id,
                                       target_address=target_address,
                                       source_address=source_address,
                                       address_extension=address_extension)
        elif addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            cls.__validate_ai_mixed_11bit(addressing=addressing,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        elif addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            cls.__validate_ai_mixed_29bit(addressing=addressing,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        else:
            raise NotImplementedError(f"Missing implementation for: {addressing_format_instance}")

    @classmethod
    def get_can_frame_dlc_single_frame(cls, addressing_format: CanAddressingFormatTyping, payload_length: int) -> int:
        """
        Get the value of a CAN frame DLC that carries a Single Frame packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param payload_length: Number of payload bytes that considered CAN packet carries.

        :raise InconsistentArgumentsError: Provided values of `payload_length` and `addressing_format` represent data
            that cannot fit into a Single Frame.

        :return: The lowest value of DLC that enables to fit in provided Single Frame packet data.
        """
        CanAddressingFormat.validate_member(addressing_format)
        cls.__validate_payload_length(payload_length)
        ai_data_bytes = CanAddressingFormat.get_number_of_data_bytes_used(addressing_format)
        data_bytes_number_short_dlc = ai_data_bytes + payload_length + cls.SHORT_SF_DL_BYTES_USED
        if data_bytes_number_short_dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            return CanDlcHandler.get_min_dlc(data_bytes_number_short_dlc)
        data_bytes_number_long_dlc = ai_data_bytes + payload_length + cls.LONG_SF_DL_BYTES_USED
        if data_bytes_number_long_dlc <= CanDlcHandler.MAX_DATA_BYTES_NUMBER:
            return CanDlcHandler.get_min_dlc(data_bytes_number_long_dlc)
        raise InconsistentArgumentsError(f"Provided payload_length cannot fit into a Single Frame when "
                                         f"{addressing_format} is used. Actual payload_length value: {payload_length}")

    @classmethod
    def get_can_frame_dlc_first_frame(cls,
                                      addressing_format: CanAddressingFormatTyping,
                                      data_length: int,
                                      payload_length: int) -> int:
        """
        Get the value of a CAN frame DLC that carries a First Frame packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param data_length: Number of payload bytes of a diagnostic message initiated by considered First Frame.
        :param payload_length: Number of payload bytes that considered CAN packet carries.

        :raise InconsistentArgumentsError: Provided values of `payload_length` and `addressing_format` requires using
            CAN Frame Data Padding or DLC value that is invalid for the First Frame packet type.

        :return: The exact value of DLC that enables to fit in provided First Frame packet data.
        """
        CanAddressingFormat.validate_member(addressing_format)
        cls.__validate_payload_length(payload_length)
        cls.__validate_ff_dl(data_length)
        ai_data_bytes = CanAddressingFormat.get_number_of_data_bytes_used(addressing_format)
        ff_dl_bytes = cls.SHORT_FF_DL_BYTES_USED if data_length <= cls.MAX_SHORT_FF_DL_VALUE \
            else cls.LONG_FF_DL_BYTES_USED
        dlc = CanDlcHandler.encode(data_bytes_number=ai_data_bytes + ff_dl_bytes + payload_length)
        if dlc < cls.MIN_DLC_VALUE_FF:
            raise InconsistentArgumentsError(f"Provided payload_length requires DLC value that is invalid for "
                                             f"First Frame packet. Actual values: payload_length={payload_length},"
                                             f"calculated DLC value={dlc}, minimum DLC value={cls.MIN_DLC_VALUE_FF}")
        return dlc

    @classmethod
    def get_can_frame_dlc_consecutive_frame(cls,
                                            addressing_format: CanAddressingFormatTyping,
                                            payload_length: int) -> int:
        """
        Get value of a CAN frame DLC that carries a Consecutive Frame packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.
        :param payload_length: Number of payload bytes that considered CAN packet carries.

        :return: The lowest value of DLC that enables to fit in provided Consecutive Frame packet data.
        """
        CanAddressingFormat.validate_member(addressing_format)
        cls.__validate_payload_length(payload_length)
        ai_data_bytes = CanAddressingFormat.get_number_of_data_bytes_used(addressing_format)
        return CanDlcHandler.get_min_dlc(ai_data_bytes + cls.SN_BYTES_USED + payload_length)

    @classmethod
    def get_can_frame_dlc_flow_control(cls, addressing_format: CanAddressingFormatTyping) -> int:
        """
        Get the value of a CAN frame DLC that carries a Flow Control packet.

        :param addressing_format: CAN addressing format that considered CAN packet uses.

        :return: The lowest value of DLC that enables to fit in Flow Control packet data.
        """
        CanAddressingFormat.validate_member(addressing_format)
        ai_data_bytes = CanAddressingFormat.get_number_of_data_bytes_used(addressing_format)
        return CanDlcHandler.get_min_dlc(ai_data_bytes + cls.FS_BYTES_USED)

    @classmethod
    def create_can_frame_data_single_frame(cls,
                                           addressing_format: CanAddressingFormatTyping,
                                           payload: RawBytes,
                                           dlc: Optional[int] = None,
                                           filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE,
                                           target_address: Optional[RawByte] = None,
                                           address_extension: Optional[RawByte] = None) -> RawBytesTuple:
        """
        Create data field of a CAN frame that carries a Single Frame packet.

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
        cls.__validate_data_single_frame(addressing_format=addressing_format,
                                         dlc=dlc,
                                         payload=payload,
                                         filler_byte=filler_byte)
        ai_data_bytes = cls.__get_can_frame_data_beginning(addressing_format=addressing_format,
                                                           target_address=target_address,
                                                           address_extension=address_extension)
        frame_dlc = dlc or cls.get_can_frame_dlc_single_frame(addressing_format=addressing_format,
                                                              payload_length=len(payload))
        data_bytes_number = CanDlcHandler.decode(frame_dlc)
        if dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL:
            ...  # TODO: put single frame N_PCI and short SF_DL
        else:
            ...  # TODO: put single frame N_PCI and long SF_DL
        frame_data_bytes = list(ai_data_bytes) + list(payload)
        frame_data_bytes += (data_bytes_number - len(frame_data_bytes)) * [filler_byte]
        return tuple(frame_data_bytes)

    @classmethod
    def create_can_frame_data_first_frame(cls,
                                          addressing_format: CanAddressingFormatTyping,
                                          payload: RawBytes,
                                          dlc: int,
                                          data_length: int,
                                          target_address: Optional[RawByte] = None,
                                          address_extension: Optional[RawByte] = None) -> RawBytesTuple:
        """
        Create data field of a CAN frame that carries a First Frame packet.

        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param payload: Payload of a diagnostic message that is carried by considered CAN packet.
        :param dlc: DLC value of a CAN frame that carries considered CAN Packet.
        :param data_length: Number of payload bytes of a diagnostic message initiated by considered First Frame packet.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :return: Raw bytes of CAN frame data for the provided First Frame packet information.
        """
        cls.__validate_data_first_frame(addressing_format=addressing_format,
                                        payload=payload,
                                        dlc=dlc,
                                        data_length=data_length)
        # TODO: tests and implementation

    @classmethod
    def create_can_frame_data_consecutive_frame(cls,
                                                addressing_format: CanAddressingFormatTyping,
                                                payload: RawBytes,
                                                sequence_number: int,
                                                dlc: Optional[int] = None,
                                                filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE,
                                                target_address: Optional[RawByte] = None,
                                                address_extension: Optional[RawByte] = None) -> RawBytesTuple:
        """
        Create data field of a CAN frame that carries a Consecutive Frame packet.

        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param payload: Payload of a diagnostic message that is carried by considered CAN packet.
        :param sequence_number: Sequence number value of considered Consecutive Frame.
        :param dlc: DLC value of a CAN frame that carries considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :return: Raw bytes of CAN frame data for the provided Consecutive Frame packet information.
        """
        # TODO: tests and implementation

    @classmethod
    def create_can_frame_data_flow_control(cls,
                                           addressing_format: CanAddressingFormatTyping,
                                           flow_status: CanFlowStatusTyping,
                                           block_size: Optional[RawByte] = None,
                                           stmin: Optional[RawByte] = None,
                                           dlc: Optional[int] = None,
                                           filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE,
                                           target_address: Optional[RawByte] = None,
                                           address_extension: Optional[RawByte] = None) -> RawBytesTuple:
        """
        Create data field of a CAN frame that carries a Flow Control packet.

        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param flow_status: Flow status information carried by considered Flow Control frame.
        :param block_size: Block size information carried by considered Flow Control frame.
        :param stmin: Separation Time minimum information carried by considered Flow Control frame.
        :param dlc: DLC value of a CAN frame that carries considered CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :return: Raw bytes of CAN frame data for the provided Flow Control packet information.
        """
        # TODO: tests and implementation

    def set_address_information(self, *,
                                addressing: AddressingTypeMemberTyping,
                                addressing_format: CanAddressingFormatTyping,
                                can_id: Optional[int] = None,
                                target_address: Optional[RawByte] = None,
                                source_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> None:
        """
        Change addressing information for this CAN packet.

        This function enables to change an entire :ref:`Network Address Information <knowledge-base-n-ai>`
        for a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param can_id: CAN Identifier value that is used by this packet.
            Leave None if other arguments unambiguously determine CAN ID value.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter
            or the value of Target Address was provided in `can_id` parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Source Address parameter
            or the value of Source Address was provided in `can_id` parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Address Extension parameter.

        :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        can_addressing_format_instance = CanAddressingFormat(addressing_format)
        if can_addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            self.set_address_information_normal_11bit(addressing=addressing,
                                                      can_id=can_id)  # type: ignore
            if (target_address, source_address, address_extension) != (None, None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: target_address={target_address}, source_address={source_address}, "
                             f"address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            self.set_address_information_normal_fixed(addressing=addressing,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address)
            if address_extension is not None:
                warn(message=f"Unused argument was provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual value: address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            self.set_address_information_extended(addressing=addressing,
                                                  can_id=can_id,  # type: ignore
                                                  target_address=target_address)  # type: ignore
            if (source_address, address_extension) != (None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: source_address={source_address}, address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            self.set_address_information_mixed_11bit(addressing=addressing,
                                                     can_id=can_id,  # type: ignore
                                                     address_extension=address_extension)  # type: ignore
            if (target_address, source_address) != (None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: target_address={target_address}, source_address={source_address}, ",
                     category=UnusedArgumentWarning)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            self.set_address_information_mixed_29bit(addressing=addressing,
                                                     can_id=can_id,
                                                     target_address=target_address,
                                                     source_address=source_address,
                                                     address_extension=address_extension)  # type: ignore
        else:
            raise NotImplementedError(f"Missing implementation for: {can_addressing_format_instance}")

    def set_packet_data(self, *,
                        packet_type: CanPacketTypeMemberTyping,
                        dlc: Optional[int] = None,
                        filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                        **packet_type_specific_kwargs: Any) -> None:
        """
        Change packet type and data field for this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param packet_type: Type of this CAN packet.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
            You have to provide DLC value for packets of First Frame type.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by this CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes of a diagnostic message initiated by this First Frame packet.
             - :parameter sequence_number: (required for: CF)
                 Sequence number value of this Consecutive Frame.
             - :parameter flow_status: (required for: FC)
                 Flow status information carried by this Flow Control frame.
             - :parameter block_size: (optional for: FC)
                 Block size information carried by this Flow Control frame.
             - :parameter stmin: (optional for: FC)
                 Separation Time minimum information carried by this Flow Control frame.

        :raise NotImplementedError: A valid packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        CanPacketType.validate_member(packet_type)
        packet_type_instance = CanPacketType(packet_type)
        if packet_type_instance == CanPacketType.SINGLE_FRAME:
            self.set_single_frame_data(dlc=dlc,
                                       filler_byte=filler_byte,
                                       **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.FIRST_FRAME:
            self.set_first_frame_data(dlc=dlc,
                                      **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.CONSECUTIVE_FRAME:
            self.set_consecutive_frame_data(dlc=dlc,
                                            filler_byte=filler_byte,
                                            **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.FLOW_CONTROL:
            self.set_flow_control_data(dlc=dlc,
                                       filler_byte=filler_byte,
                                       **packet_type_specific_kwargs)
        else:
            raise NotImplementedError(f"Missing implementation for: {packet_type_instance}")

    def set_single_frame_data(self,
                              payload: RawBytes,
                              dlc: Optional[int] = None,
                              filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Single Frame) and data field for this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Single Frame <knowledge-base-can-single-frame>`.

        :param payload: Payload of a diagnostic message that is carried by this CAN packet.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        """
        self.__validate_data_single_frame(dlc=dlc,
                                          payload=payload,
                                          filler_byte=filler_byte)  # TODO: refine
        self.__raw_frame_data = self.create_can_frame_data_single_frame(addressing_format=self.addressing_format,
                                                                        target_address=self.target_address,
                                                                        address_extension=self.address_extension,
                                                                        dlc=dlc,
                                                                        payload=payload,
                                                                        filler_byte=filler_byte)
        self.__dlc = dlc or self.get_can_frame_dlc_single_frame(addressing_format=self.addressing_format,
                                                                payload_length=len(payload))
        self.__packet_type = CanPacketType.SINGLE_FRAME

    def set_first_frame_data(self,
                             dlc: int,
                             payload: RawBytes,
                             data_length: int) -> None:
        """
        Change packet type (to First Frame) and data field for this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`First Frame <knowledge-base-can-first-frame>`.

        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
        :param payload: Payload of a diagnostic message that is carried by this CAN packet.
        :param data_length: Number of payload bytes of a diagnostic message initiated by this First Frame packet.
        """
        self.__validate_data_first_frame(dlc=dlc,
                                         payload=payload,
                                         data_length=data_length)
        self.__raw_frame_data = self.create_can_frame_data_first_frame(addressing_format=self.addressing_format,
                                                                       dlc=dlc,
                                                                       payload=payload,
                                                                       data_length=data_length)
        self.__dlc = dlc
        self.__packet_type = CanPacketType.FIRST_FRAME

    def set_consecutive_frame_data(self,
                                   payload: RawBytes,
                                   sequence_number: int,
                                   dlc: Optional[int] = None,
                                   filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Consecutive Frame) and data field for this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Consecutive Frame <knowledge-base-can-first-frame>`.

        :param payload: Payload of a diagnostic message that is carried by this CAN packet.
        :param sequence_number: Sequence number value of this Consecutive Frame.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        """
        self.__validate_data_consecutive_frame(payload=payload,
                                               sequence_number=sequence_number,
                                               dlc=dlc,
                                               filler_byte=filler_byte)
        # TODO: tests and further implementation

    def set_flow_control_data(self,
                              flow_status: CanFlowStatusTyping,
                              block_size: Optional[RawByte] = None,
                              stmin: Optional[RawByte] = None,
                              dlc: Optional[int] = None,
                              filler_byte: Optional[RawByte] = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Flow Control) and data field for this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Flow Control <knowledge-base-can-flow-control>`.

        :param flow_status: Flow status information carried by this Flow Control frame.
        :param block_size: Block size information carried by this Flow Control frame.
        :param stmin: Separation Time minimum information carried by this Flow Control frame.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        """
        # TODO: tests and further implementation

    def set_address_information_normal_11bit(self, addressing: AddressingType, can_id: int) -> None:
        """
        Change addressing information for this CAN packet to use Normal 11-bit Addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        """
        # TODO: rework - full validation
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_11BIT_ADDRESSING)  # type: ignore
        self.__addressing_format = CanAddressingFormat.NORMAL_11BIT_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__can_id = can_id
        self.__target_address = None
        self.__address_extension = None

    def set_address_information_normal_fixed(self,
                                             addressing: AddressingType,
                                             can_id: Optional[int] = None,
                                             target_address: Optional[RawByte] = None,
                                             source_address: Optional[RawByte] = None) -> None:
        """
        Change addressing information for this CAN packet to use Normal Fixed Addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            Leave None if the values of `target_address` and `source_address` parameters are provided.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if the value of `can_id` parameter is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if the value of `can_id` parameter is provided.
        """
        # TODO: rework - full validation
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_FIXED_ADDRESSING)  # type: ignore
        if can_id is None:
            self.__can_id = CanIdHandler.get_normal_fixed_addressed_can_id(addressing_type=addressing,
                                                                           target_address=target_address,  # noqa
                                                                           source_address=source_address)  # noqa
            self.__target_address = target_address
        else:
            self.__can_id = can_id
            self.__target_address = CanIdHandler.decode_normal_fixed_addressed_can_id(can_id)[1]
        self.__addressing_format = CanAddressingFormat.NORMAL_FIXED_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__address_extension = None

    def set_address_information_extended(self,
                                         addressing: AddressingType,
                                         can_id: int,
                                         target_address: RawByte) -> None:
        """
        Change addressing information for this CAN packet to use Extended Addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        :param target_address: Target Address value carried by this CAN Packet.
        """
        # TODO: rework - full validation
        self.__validate_unambiguous_ai_change(CanAddressingFormat.EXTENDED_ADDRESSING)  # type: ignore
        self.__addressing_format = CanAddressingFormat.EXTENDED_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__can_id = can_id
        self.__target_address = target_address
        self.__address_extension = None

    def set_address_information_mixed_11bit(self,
                                            addressing: AddressingType,
                                            can_id: int,
                                            address_extension: RawByte) -> None:
        """
        Change addressing information for this CAN packet to use Mixed 11-bit Addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        # TODO: rework - full validation
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_11BIT_ADDRESSING)  # type: ignore
        self.__addressing_format = CanAddressingFormat.MIXED_11BIT_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__can_id = can_id
        self.__target_address = None
        self.__address_extension = address_extension

    def set_address_information_mixed_29bit(self,
                                            addressing: AddressingType,
                                            address_extension: RawByte,
                                            can_id: Optional[int] = None,
                                            target_address: Optional[RawByte] = None,
                                            source_address: Optional[RawByte] = None) -> None:
        """
        Change addressing information for this CAN packet to use Mixed 29-bit Addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            Leave None if the values of `target_address` and `source_address` parameters are provided.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if the value of `can_id` parameter is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if the value of `can_id` parameter is provided.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        # TODO: rework - full validation
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_29BIT_ADDRESSING)  # type: ignore
        if can_id is None:
            self.__can_id = CanIdHandler.get_mixed_addressed_29bit_can_id(addressing_type=addressing,
                                                                          target_address=target_address,  # type: ignore
                                                                          source_address=source_address)  # type: ignore
            self.__target_address = target_address
        else:
            self.__can_id = can_id
            self.__target_address = CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id)[1]
        self.__addressing_format = CanAddressingFormat.MIXED_29BIT_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__address_extension = address_extension

    @property
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a CAN frame that carries this CAN packet."""
        return self.__raw_frame_data

    @property
    def addressing(self) -> AddressingType:
        """Addressing type for which this CAN packet is relevant."""
        return self.__addressing

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN addressing format used by this CAN packet."""
        return self.__addressing_format

    @property
    def packet_type(self) -> CanPacketType:
        """Type of this CAN packet."""
        return self.__packet_type

    @property
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""
        return self.__can_id

    @property
    def dlc(self) -> int:
        """Value of Data Length Code (DLC) of a CAN Frame that carries this CAN packet."""
        return self.__dlc

    @property
    def address_extension(self) -> Optional[RawByte]:
        """
        Address Extension (AE) value of this CAN Packet.

        Address Extension is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Mixed Addressing <knowledge-base-can-mixed-addressing>` - either:
           - :ref:`Mixed 11-bit Addressing <knowledge-base-can-mixed-11-bit-addressing>`
           - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__address_extension

    @property
    def target_address(self) -> Optional[RawByte]:
        """
        Target Address (TA) value of this CAN Packet.

        Target Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Extended Addressing <knowledge-base-can-extended-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__target_address

    @property
    def source_address(self) -> Optional[RawByte]:
        """
        Source Address (SA) value of this CAN Packet.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`

        None in other cases.
        """
        if self.addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            return CanIdHandler.decode_normal_fixed_addressed_can_id(self.can_id)[2]
        if self.addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            return CanIdHandler.decode_mixed_addressed_29bit_can_id(self.can_id)[2]
        return None

    @property
    def payload(self) -> Optional[RawBytesTuple]:
        """
        Diagnostic message payload carried by this CAN packet.

        Payload is only provided by packets of following types:
         - :ref:`Single Frame <knowledge-base-can-single-frame>`
         - :ref:`First Frame <knowledge-base-can-first-frame>`
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.

        .. warning:: For :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` this value might contain
            additional filler bytes (they are not part of diagnostic message payload) that were added during
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            The presence of filler bytes in :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
            cannot be determined basing solely on the information contained in this packet object.
        """
        # TODO: implementation and tests

    @property
    def data_length(self) -> Optional[int]:
        """
        Payload bytes number of a diagnostic message that is carried by this CAN packet.

        Data length is only provided by packets of following types:
         - :ref:`Single Frame <knowledge-base-can-single-frame>` -
           :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>`
         - :ref:`First Frame <knowledge-base-can-first-frame>` -
           :ref:`First Frame Data Length <knowledge-base-can-first-frame-data-length>`

        None in other cases.
        """
        # TODO: implementation and tests

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Sequence Number carried by this CAN packet.

        :ref:`Sequence Number <knowledge-base-can-sequence-number>` is only provided by packets of following types:
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.
        """
        # TODO: implementation and tests

    @property
    def flow_status(self) -> Optional[CanFlowStatus]:
        """
        Flow Status carried by this CAN packet.

        :ref:`Flow Status <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-flow-control>`

        None in other cases.
        """
        # TODO: implementation and tests

    @property
    def block_size(self) -> Optional[RawByte]:
        """
        Block Size value carried by this CAN packet.

        :ref:`Block Size <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        # TODO: implementation and tests

    @property
    def stmin(self) -> Optional[RawByte]:
        """
        Separation Time minimum (STmin) value carried by this CAN packet.

        :ref:`STmin <knowledge-base-can-st-min>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        # TODO: implementation and tests

    @staticmethod
    def __get_can_frame_data_beginning(addressing_format: CanAddressingFormatTyping,
                                       target_address: Optional[RawByte] = None,
                                       address_extension: Optional[RawByte] = None) -> RawBytes:
        """
        Get the beginning of CAN frame data field.

        :param addressing_format: CAN addressing format used by considered CAN packet.
        :param target_address: Target Address value carried by this CAN Packet.
            The value must only be provided if `addressing_format` uses Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            The value must only be provided if `addressing_format` uses Address Extension parameter.

        :raise NotImplementedError: Valid arguments were provided, but the implementation is missing.

        :return: The first bytes of CAN frame data field that are occupied by Addressing Information.
        """
        CanAddressingFormat.validate_member(addressing_format)
        addressing_format_instance = CanAddressingFormat(addressing_format)
        ai_data_bytes = CanAddressingFormat.get_number_of_data_bytes_used(addressing_format_instance)
        if ai_data_bytes == 0:
            return []
        if ai_data_bytes == 1:
            if addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
                validate_raw_byte(target_address)
                return [target_address]
            if addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING \
                    or addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
                validate_raw_byte(address_extension)
                return [address_extension]
        raise NotImplementedError("Missing implementation")

    # TODO: review whether the rest is needed












    # @classmethod
    # def get_payload_length(cls,
    #                        addressing_format: CanAddressingFormatTyping,
    #                        packet_type: CanPacketType,
    #                        dlc: Optional[int] = None) -> int:
    #     # TODO
    #     ...
    #
    # @classmethod
    # def get_max_payload_length_single_frame(cls,  # TODO: get rid of it or transform to private
    #                                         addressing_format: CanAddressingFormatTyping,
    #                                         dlc: Optional[int] = None) -> int:
    #     """
    #     Get maximal value of Single Frame Data Length (SF_DL) for a CAN packet.
    #
    #     :param addressing_format: CAN addressing format to use in considered CAN Packet.
    #     :param dlc: Value of DLC value in a CAN frame.
    #         Leave None to use maximal value.
    #
    #     :return: Maximal value of SF_DL that UDS Packet with provided Addressing Format and DLC can fit in.
    #         If negative, then a greater value of DLC must be used.
    #     """
    #     frame_data_bytes_number = CanDlcHandler.MAX_DATA_BYTES_NUMBER if dlc is None else CanDlcHandler.decode(dlc)
    #     data_bytes_used_for_ai = CanAddressingFormat.get_number_of_data_bytes_used(addressing_format)
    #     data_bytes_used_for_sfdl_and_npci = cls.DATA_BYTES_SHORT_SF_DL \
    #         if dlc is not None and dlc <= cls.MAX_DLC_VALUE_SHORT_SF_DL else cls.DATA_BYTES_LONG_SF_DL
    #     return frame_data_bytes_number - data_bytes_used_for_ai - data_bytes_used_for_sfdl_and_npci
    #
    # @classmethod
    # def get_payload_length_first_frame(cls,  # TODO: get rid of it or transform to private
    #                                    addressing_format: CanAddressingFormatTyping,
    #                                    data_length: int,
    #                                    dlc: int) -> int:
    #     ...  # TODO
    #
    # @classmethod
    # def get_max_payload_length_consecutive_frame(cls,  # TODO: get rid of it or transform to private
    #                                              addressing_format: CanAddressingFormatTyping,
    #                                              dlc: Optional[int] = None) -> int:
    #     ...  # TODO





    @classmethod
    def __validate_ai_consistency(cls,
                                  addressing: AddressingTypeMemberTyping,
                                  addressing_format: CanAddressingFormatTyping,
                                  can_id: Optional[int],
                                  target_address: Optional[RawByte],
                                  source_address: Optional[RawByte],
                                  address_extension: Optional[RawByte]) -> None:
        """
        Validate consistency of Address Information arguments.

        :param addressing: Addressing type value to validate.
        :param addressing_format: CAN addressing format value to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        can_addressing_format_instance = CanAddressingFormat(addressing_format)
        if can_addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            cls.__validate_ai_normal_11bit(can_id=can_id,
                                           target_address=target_address,
                                           source_address=source_address,
                                           address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            cls.__validate_ai_normal_fixed(addressing=addressing,
                                           can_id=can_id,
                                           target_address=target_address,
                                           source_address=source_address,
                                           address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            cls.__validate_ai_extended(can_id=can_id,
                                       target_address=target_address,
                                       source_address=source_address,
                                       address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            cls.__validate_ai_mixed_11bit(can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            cls.__validate_ai_mixed_29bit(addressing=addressing,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        else:
            raise NotImplementedError(f"Unknown CAN Addressing Format value was provided: "
                                      f"{can_addressing_format_instance}")

    @staticmethod
    def __validate_ai_normal_11bit(addressing: AddressingTypeMemberTyping,
                                   can_id: Optional[int],
                                   target_address: Optional[RawByte],
                                   source_address: Optional[RawByte],
                                   address_extension: Optional[RawByte]) -> None:
        # TODO: update docstring (same for siblings)
        """
        Validate consistency of Address Information arguments when Normal 11-bit Addressing Format is used.

        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: Value for at least one unused argument (not relevant for this can addressing format)
            was provided.
        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        # TODO: refactor the code and test it (same for siblings)
        if (target_address, source_address, address_extension) != (None, None, None):
            raise UnusedArgumentError(f"Either target_address, source_address or address_extension argument was "
                                      f"provided for Normal 11-bit Addressing Format. Actual values: "
                                      f"target_address={target_address}, source_address={source_address}, "
                                      f"address_extension={address_extension}")
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_normal_11bit_addressed_can_id(can_id):  # type: ignore
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Normal 11-bit Addressing Format. Actual value: {can_id}")

    @staticmethod
    def __validate_ai_normal_fixed(addressing: AddressingTypeMemberTyping,
                                   can_id: Optional[int],
                                   target_address: Optional[RawByte],
                                   source_address: Optional[RawByte],
                                   address_extension: Optional[RawByte]) -> None:
        """
        Validate consistency of Address Information arguments when Normal Fixed Addressing Format is used.

        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: Value for at least one unused argument (not relevant for this can addressing format)
            was provided.
        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        if address_extension is not None:
            raise UnusedArgumentError(f"Value for address_extension argument was provided for Normal Fixed "
                                      f"Addressing Format. Actual value: {address_extension}")
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Normal Fixed Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
            if (target_address, source_address) != (None, None):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be equal None,"
                                                 f"if can_id value is provided for Normal Fixed Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            CanIdHandler.validate_can_id(can_id)
            if not CanIdHandler.is_normal_fixed_addressed_can_id(can_id=can_id, addressing=addressing):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                                 f"Normal Fixed Addressing Format. Actual value: {can_id}")

    @staticmethod
    def __validate_ai_extended(addressing: AddressingTypeMemberTyping,
                               can_id: Optional[int],
                               target_address: Optional[RawByte],
                               source_address: Optional[RawByte],
                               address_extension: Optional[RawByte]) -> None:
        """
        Validate consistency of Address Information arguments when Extended Addressing Format is used.

        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: Value for at least one unused argument (not relevant for this can addressing format)
            was provided.
        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        if (source_address, address_extension) != (None, None):
            raise UnusedArgumentError(f"Either source_address or address_extension argument was "
                                      f"provided for Extended Addressing Format. Actual values: "
                                      f"source_address={source_address}, address_extension={address_extension}")
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_extended_addressed_can_id(can_id):  # type: ignore
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Extended Addressing Format. Actual value: {can_id}")
        validate_raw_byte(target_address)

    @staticmethod
    def __validate_ai_mixed_11bit(addressing: AddressingTypeMemberTyping,
                                  can_id: Optional[int],
                                  target_address: Optional[RawByte],
                                  source_address: Optional[RawByte],
                                  address_extension: Optional[RawByte]) -> None:
        """
        Validate consistency of Address Information arguments when Mixed 11-bit Addressing Format is used.

        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: Value for at least one unused argument (not relevant for this can addressing format)
            was provided.
        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        if (target_address, source_address) != (None, None):
            raise UnusedArgumentError(f"Either target_address or source_address argument was "
                                      f"provided for Mixed 11-bit Addressing Format. Actual values: "
                                      f"target_address={target_address}, address_extension={source_address}")
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_mixed_11bit_addressed_can_id(can_id):  # type: ignore
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Mixed 11-bit Addressing Format. Actual value: {can_id}")
        validate_raw_byte(address_extension)

    @staticmethod
    def __validate_ai_mixed_29bit(addressing: AddressingTypeMemberTyping,
                                  can_id: Optional[int],
                                  target_address: Optional[RawByte],
                                  source_address: Optional[RawByte],
                                  address_extension: Optional[RawByte]) -> None:
        """
        Validate consistency of Address Information arguments when Mixed 29-bit Addressing Format is used.

        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        validate_raw_byte(address_extension)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Mixed 29-bit Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
            if (target_address, source_address) != (None, None):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be equal None,"
                                                 f"if can_id value is provided for Mixed 29-bit Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            CanIdHandler.validate_can_id(can_id)
            if not CanIdHandler.is_mixed_29bit_addressed_can_id(can_id=can_id, addressing=addressing):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                                 f"Mixed 29-bit Addressing Format. Actual value: {can_id}")

    def __validate_unambiguous_ai_change(self, addressing_format: CanAddressingFormat) -> None:
        """
        Validate whether CAN Addressing Format change to provided value is ambiguous.

        :param addressing_format: Desired value of CAN Addressing Format.

        :raise AmbiguityError: Cannot change value because the operation is ambiguous.
        """
        if self.addressing_format is not None \
                and CanAddressingFormat.get_number_of_data_bytes_used(addressing_format) \
                != CanAddressingFormat.get_number_of_data_bytes_used(self.addressing_format):
            raise AmbiguityError(f"Cannot change CAN Addressing Format from {self.addressing_format} to "
                                 f"{addressing_format} as such operation provides ambiguity. "
                                 f"Create a new CAN Packet object instead.")

    @staticmethod
    def __validate_payload_length(payload_length: int) -> None:
        """
        Validate value of payload length.

        :param payload_length: Value to validate.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is not a positive value.
            NOTE: Maximum value is not verified as there are multiple factors that affects it.
        """
        if not isinstance(payload_length, int):
            raise TypeError(f"Provided payload_length value is not int type. Actual type: {type(payload_length)}")
        if payload_length <= 0:
            raise ValueError(f"Provided payload_length value not a positive number. Expected: payload_length>0."
                             f"Actual value: {payload_length}")

    @classmethod
    def __validate_ff_dl(cls, ff_dl: int) -> None:
        """
        Validate value of First Frame Data Length.

        :param ff_dl: Value to validate.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(ff_dl, int):
            raise TypeError(f"Provided ff_dl value is not int type. Actual type: {type(ff_dl)}")
        if not 0 < ff_dl <= cls.MAX_LONG_FF_DL_VALUE:
            raise ValueError(f"Provided ff_dl value is out of range. Expected: 0 < ff_dl < {cls.MAX_LONG_FF_DL_VALUE}."
                             f"Actual value: {ff_dl}")

    def __validate_data(self,
                        packet_type: CanPacketTypeMemberTyping,
                        dlc: Optional[int],
                        filler_byte: RawByte,
                        **packet_type_specific_kwargs: Any) -> None:
        """
        Validate arguments related to CAN Packet data.

        This methods performs comprehensive check of :ref:`Network Data Field (N_Data) <knowledge-base-n-data>`
        and :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        :ref:`CAN Packet <knowledge-base-uds-can-packet>` to make sure that every required argument is provided
        and their values are consistent with provided :ref:`CAN Packet Type <knowledge-base-can-n-pci>`.

        :param packet_type: Packet type to validate.
        :param dlc: DLC value to validate.
        :param filler_byte: Filler Byte value to validate.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
        """
        CanPacketType.validate_member(packet_type)
        validate_raw_byte(filler_byte)
        if dlc is not None:
            CanDlcHandler.validate_dlc(dlc)
        self.__validate_data_consistency(packet_type=packet_type,
                                         dlc=dlc,
                                         **packet_type_specific_kwargs)

    def __validate_data_consistency(self,
                                    packet_type: CanPacketTypeMemberTyping,
                                    dlc: Optional[int],
                                    **packet_type_specific_kwargs: Any) -> None:
        """
        Validate consistency of arguments related to CAN Packet data.

        :param packet_type: Packet type to validate.
        :param dlc: DLC value to validate.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.

        :raise NotImplementedError: A valid CAN packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        packet_type_instance = CanPacketType(packet_type)
        if packet_type_instance == CanPacketType.SINGLE_FRAME:
            self.__validate_data_single_frame(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.FIRST_FRAME:
            self.__validate_data_first_frame(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.CONSECUTIVE_FRAME:
            self.__validate_data_consecutive_frame(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.FLOW_CONTROL:
            self.__validate_data_flow_control(dlc=dlc, **packet_type_specific_kwargs)
        raise NotImplementedError(f"Unknown CAN Packet Type value was provided: {packet_type_instance}")

    @classmethod
    def __validate_data_single_frame(cls, addressing_format: CanAddressingFormatTyping, dlc: Optional[int], payload: RawBytes, filler_byte: RawByte) -> None:
        # TODO: update docstring and code
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param payload: Payload value to validate.

        :raise InconsistentArgumentsError: Value of payload is not compatible with values of other parameters.
        """
        validate_raw_bytes(payload)
        required_dlc = cls.get_can_frame_dlc_single_frame(addressing_format=addressing_format, payload_length=len(payload))
        current_dlc = dlc or CanDlcHandler.MAX_DLC_VALUE
        if current_dlc < required_dlc:
            raise InconsistentArgumentsError(f"Provided value of payload is not compatible with dlc and "
                                             f"addressing_format values. Addressing format: {addressing_format}. "
                                             f"DLC value: {current_dlc}. Actual payload length: {len(payload)}.")

    @classmethod
    def __validate_data_first_frame(cls, addressing_format: CanAddressingFormatTyping, dlc: int, data_length: int, payload: RawBytes) -> None:
        # TODO: update docstring and code
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param payload: Payload value to validate.

        :raise InconsistentArgumentsError: Value of payload is not compatible with values of other parameters.
        """
        validate_raw_bytes(payload)
        required_dlc = cls.get_can_frame_dlc_first_frame(addressing_format=addressing_format,
                                                          data_length=data_length,
                                                          payload_length=len(payload))
        if dlc != required_dlc:
            raise InconsistentArgumentsError(f"Provided value of dlc is not compatible with payload, data_length and "
                                             f"addressing_format values. Expected dlc value: {required_dlc}. "
                                             f"Actual dlc: {dlc}")

    @classmethod
    def __validate_data_consecutive_frame(cls, addressing_format: CanAddressingFormatTyping, dlc: Optional[int], sequence_number: int, payload: RawBytes) -> None:
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param sequence_number: Sequence Number value to validate.
        :param payload: Payload value to validate.

        :raise InconsistentArgumentsError: Value of payload is not compatible with values of other parameters.
        """
        # TODO: update docstring and code
        validate_raw_bytes(payload)
        if not isinstance(sequence_number, int):
            raise TypeError(f"Provided sequence_number value is not int type. Actual type: {type(sequence_number)}")
        if not cls.MIN_SEQUENCE_NUMBER <= sequence_number <= cls.MAX_SEQUENCE_NUMBER:
            raise ValueError(f"Provided sequence_number sequence_number is out of range. "
                             f"Actual value: {sequence_number}")
        required_dlc = cls.get_can_frame_dlc_consecutive_frame(addressing_format=addressing_format,
                                                                payload_length=len(payload))
        if dlc < required_dlc:
            raise InconsistentArgumentsError(f"Provided value of dlc is not compatible with payload, and "
                                             f"addressing_format values. Expected dlc value: {required_dlc}. "
                                             f"Actual dlc: {dlc}")

    @classmethod
    def __validate_data_flow_control(cls,
                                     addressing_format: CanAddressingFormatTyping,
                                     dlc: Optional[int],
                                     flow_status: CanFlowStatusTyping,
                                     block_size: Optional[RawByte] = None,
                                     stmin: Optional[RawByte] = None) -> None:
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param flow_status: Flow Status value to validate.
        :param block_size: Block Size value to validate.
        :param stmin: STmin value to validate.
        """
        # TODO: update docstring and code
        CanFlowStatus.validate_member(flow_status)
        flow_status_instance = CanFlowStatus(flow_status)
        if flow_status_instance == CanFlowStatus.ContinueToSend:
            validate_raw_byte(block_size)
            validate_raw_byte(stmin)
        elif (block_size, stmin) != (None, None):
            raise InconsistentArgumentsError(f"Values of block_size and stmin must not be equal None,"
                                             f"if ContinueToSend flow_status was provided. "
                                             f"Actual values: block_size={block_size}, stmin={stmin}")
        if dlc is not None:
            CanDlcHandler.validate_dlc(dlc)
            minimum_dlc = cls.get_can_frame_dlc_flow_control(addressing_format=addressing_format)
            if dlc < minimum_dlc:
                raise InconsistentArgumentsError(f"Provided value of dlc is not compatible with flow status and "
                                                 f"addressing_format values. Minimum dlc value: {minimum_dlc}. "
                                                 f"Actual payload length: {dlc}")




class CanPacketRecord(AbstractUdsPacketRecord):
    ...

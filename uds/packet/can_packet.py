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

from uds.transmission_attributes import AddressingType, AddressingTypeMemberTyping
from uds.utilities import RawByte, RawBytes, RawBytesTuple, validate_raw_byte, \
    InconsistentArgumentsError, UnusedArgumentError, AmbiguityError

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

    def __init__(self, *,
                 addressing: AddressingTypeMemberTyping,
                 addressing_format: CanAddressingFormatTyping,
                 packet_type: CanPacketTypeMemberTyping,
                 can_id: Optional[int] = None,
                 target_address: Optional[RawByte] = None,
                 source_address: Optional[RawByte] = None,
                 address_extension: Optional[RawByte] = None,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Create a storage for a single CAN packet.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param packet_type: Type of this CAN packet.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then other arguments must unambiguously determine CAN ID value.
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
             - int type value - DLC value to set, CAN Data Padding will be used to fill unused data bytes
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by this CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes that carried diagnostic message has.
             - :parameter sequence_number: (required for: CF)
                 Sequence number of this Consecutive Frame.
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
        self.set_data(packet_type=packet_type,
                      dlc=dlc,
                      filler_byte=filler_byte,
                      **packet_type_specific_kwargs)

    def set_address_information(self, *,
                                addressing: AddressingTypeMemberTyping,
                                addressing_format: CanAddressingFormatTyping,
                                can_id: Optional[int] = None,
                                target_address: Optional[RawByte] = None,
                                source_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information for this CAN packet.

        This function enables to set an entire :ref:`Network Address Information <knowledge-base-n-ai>`
        for a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then other arguments must unambiguously determine CAN ID value.
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
        self.validate_address_information(addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        can_addressing_format_instance = CanAddressingFormat(addressing_format)
        can_addressing_type_instance = AddressingType(addressing)
        if can_addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            self.__set_address_information_normal_11bit(addressing=can_addressing_type_instance,
                                                        can_id=can_id)  # type: ignore
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            self.__set_address_information_normal_fixed(addressing=can_addressing_type_instance,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address)
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            self.__set_address_information_extended(addressing=can_addressing_type_instance,
                                                    can_id=can_id,  # type: ignore
                                                    target_address=target_address)  # type: ignore
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            self.__set_address_information_mixed_11bit(addressing=can_addressing_type_instance,
                                                       can_id=can_id,  # type: ignore
                                                       address_extension=address_extension)  # type: ignore
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            self.__set_address_information_mixed_29bit(addressing=can_addressing_type_instance,
                                                       can_id=can_id,
                                                       target_address=target_address,
                                                       source_address=source_address,
                                                       address_extension=address_extension)  # type: ignore
        else:
            raise NotImplementedError(f"Missing implementation for: {can_addressing_format_instance}")

    def set_data(self, *,
                 packet_type: CanPacketTypeMemberTyping,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Set or change packet type and data field for this CAN packet.

        This function enables to set an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param packet_type: Type of this CAN packet.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set, CAN Data Padding will be used to fill unused data bytes
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by this CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes that carried diagnostic message has.
             - :parameter sequence_number: (required for: CF)
                 Sequence number of this Consecutive Frame.
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

    @classmethod
    def validate_address_information(cls,
                                     addressing: AddressingTypeMemberTyping,
                                     addressing_format: CanAddressingFormatTyping,
                                     can_id: Optional[int],
                                     target_address: Optional[RawByte],
                                     source_address: Optional[RawByte],
                                     address_extension: Optional[RawByte]) -> None:
        """
        Validate addressing information arguments.

        This methods performs comprehensive check of :ref:`Network Addressing Information (N_AI) <knowledge-base-n-ai>`
        for :ref:`CAN Packet <knowledge-base-uds-can-packet>` to make sure that every required argument is provided
        and their values are consistent with provided :ref:`CAN Addressing Format <knowledge-base-can-addressing>`.

        :param addressing: Addressing type value to validate.
        :param addressing_format: CAN addressing format value to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.
        """
        AddressingType.validate_member(addressing)
        CanAddressingFormat.validate_member(addressing_format)
        cls.__validate_ai_consistency(addressing=addressing,
                                      addressing_format=addressing_format,
                                      can_id=can_id,
                                      target_address=target_address,
                                      source_address=source_address,
                                      address_extension=address_extension)

    @classmethod
    def validate_data(cls,
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
        cls.__validate_data_consistency(packet_type=packet_type,
                                        dlc=dlc,
                                        **packet_type_specific_kwargs)

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
        """CAN addressing format of this CAN packet."""
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

        .. warning:: For :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` this field might contain
            additional filler bytes (they are not part of diagnostic message payload) that were added during
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            The presence of filler bytes in :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
            cannot be determined solely on the information contained in this packet.
        """

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

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Sequence Number carried by this CAN packet.

        :ref:`Sequence Number <knowledge-base-can-sequence-number>` is only provided by packets of following types:
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.
        """

    @property
    def flow_status(self) -> Optional[CanFlowStatus]:
        """
        Flow Status carried by this CAN packet.

        :ref:`Flow Status <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-flow-control>`

        None in other cases.
        """

    @property
    def block_size(self) -> Optional[RawByte]:
        """
        Block Size value carried by this CAN packet.

        :ref:`Block Size <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """

    @property
    def stmin(self) -> Optional[RawByte]:
        """
        Separation Time minimum (STmin) value carried by this CAN packet.

        :ref:`STmin <knowledge-base-can-st-min>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """

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
            cls.__validate_ai_consistency_normal_11bit(can_id=can_id,
                                                       target_address=target_address,
                                                       source_address=source_address,
                                                       address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            cls.__validate_ai_consistency_normal_fixed(addressing=addressing,
                                                       can_id=can_id,
                                                       target_address=target_address,
                                                       source_address=source_address,
                                                       address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            cls.__validate_ai_consistency_extended(can_id=can_id,
                                                   target_address=target_address,
                                                   source_address=source_address,
                                                   address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            cls.__validate_ai_consistency_mixed_11bit(can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            cls.__validate_ai_consistency_mixed_29bit(addressing=addressing,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address,
                                                      address_extension=address_extension)
        else:
            raise NotImplementedError(f"Unknown CAN Addressing Format value was provided: "
                                      f"{can_addressing_format_instance}")

    @staticmethod
    def __validate_ai_consistency_normal_11bit(can_id: Optional[int],
                                               target_address: Optional[RawByte],
                                               source_address: Optional[RawByte],
                                               address_extension: Optional[RawByte]) -> None:
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
    def __validate_ai_consistency_normal_fixed(addressing: AddressingTypeMemberTyping,
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
    def __validate_ai_consistency_extended(can_id: Optional[int],
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
    def __validate_ai_consistency_mixed_11bit(can_id: Optional[int],
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
    def __validate_ai_consistency_mixed_29bit(addressing: AddressingTypeMemberTyping,
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

    @classmethod
    def __validate_data_consistency(cls,
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
            cls.__validate_data_single_frame(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.FIRST_FRAME:
            cls.__validate_data_first_frame(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.CONSECUTIVE_FRAME:
            cls.__validate_data_consecutive_frame(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type_instance == CanPacketType.FLOW_CONTROL:
            cls.__validate_data_flow_control(dlc=dlc, **packet_type_specific_kwargs)
        raise NotImplementedError(f"Unknown CAN Packet Type value was provided: {packet_type_instance}")

    @classmethod
    def __validate_data_single_frame(cls, dlc: Optional[int], payload: RawBytes) -> None:
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param payload: Payload value to validate.
        """

    @classmethod
    def __validate_data_first_frame(cls, dlc: Optional[int], data_length: int, payload: RawBytes) -> None:
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param payload: Payload value to validate.
        """

    @classmethod
    def __validate_data_consecutive_frame(cls, dlc: Optional[int], sequence_number: int, payload: RawBytes) -> None:
        """
        Validate data parameters of single frame packet.

        :param dlc: DLC value to validate.
        :param sequence_number: Sequence Number value to validate.
        :param payload: Payload value to validate.
        """

    @classmethod
    def __validate_data_flow_control(cls,
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

    def __set_address_information_normal_11bit(self, addressing: AddressingType, can_id: int) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using normal 11-bit addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then other arguments must unambiguously determine CAN ID value.
        """
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_11BIT_ADDRESSING)  # type: ignore
        self.__addressing_format = CanAddressingFormat.NORMAL_11BIT_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__can_id = can_id
        self.__target_address = None
        self.__address_extension = None

    def __set_address_information_normal_fixed(self,
                                               addressing: AddressingType,
                                               can_id: Optional[int] = None,
                                               target_address: Optional[RawByte] = None,
                                               source_address: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using normal fixed addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then other arguments must unambiguously determine CAN ID value.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if the value of Target Address was provided in `can_id` parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if the value of Source Address was provided in `can_id` parameter.
        """
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

    def __set_address_information_extended(self,
                                           addressing: AddressingType,
                                           can_id: int,
                                           target_address: RawByte) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using extended addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
        :param target_address: Target Address value carried by this CAN Packet.
        """
        self.__validate_unambiguous_ai_change(CanAddressingFormat.EXTENDED_ADDRESSING)  # type: ignore
        self.__addressing_format = CanAddressingFormat.EXTENDED_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__can_id = can_id
        self.__target_address = target_address
        self.__address_extension = None

    def __set_address_information_mixed_11bit(self,
                                              addressing: AddressingType,
                                              can_id: int,
                                              address_extension: RawByte) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using mixed 11-bit addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_11BIT_ADDRESSING)  # type: ignore
        self.__addressing_format = CanAddressingFormat.MIXED_11BIT_ADDRESSING  # type: ignore
        self.__addressing = addressing
        self.__can_id = can_id
        self.__target_address = None
        self.__address_extension = address_extension

    def __set_address_information_mixed_29bit(self,
                                              addressing: AddressingType,
                                              address_extension: RawByte,
                                              can_id: Optional[int] = None,
                                              target_address: Optional[RawByte] = None,
                                              source_address: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using mixed 29-bit addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then other arguments must unambiguously determine CAN ID value.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if the value of Target Address was provided in `can_id` parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if the value of Source Address was provided in `can_id` parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Address Extension parameter.
        """
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


class CanPacketRecord(AbstractUdsPacketRecord):
    ...

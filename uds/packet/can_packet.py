"""
CAN bus specific implementation of UDS packets.

This module contains implementation of :ref:`CAN packets <knowledge-base-uds-can-packet>`:
 - :ref:`Single Frame <knowledge-base-can-single-frame>`
 - :ref:`First Frame <knowledge-base-can-first-frame>`
 - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
 - :ref:`Flow Control <knowledge-base-can-flow-control>`
"""

__all__ = ["CanPacket", "CanPacketRecord"]

from typing import Optional, Any, Dict

from uds.transmission_attributes import AddressingType, AddressingTypeMemberTyping
from uds.utilities import RawByte, RawBytesTuple, validate_raw_byte, \
    InconsistentArgumentsError, UnusedArgumentError

from .abstract_packet import AbstractUdsPacket, AbstractUdsPacketRecord
from .can_packet_attributes import DEFAULT_FILLER_BYTE, CanAddressingFormat, CanAddressingFormatTyping, \
    CanPacketType, CanPacketTypeMemberTyping, CanIdHandler, CanDlcHandler
from .can_flow_control import CanFlowStatus


class CanPacket(AbstractUdsPacket):
    """
    Definition of a CAN packet.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`CAN packet <knowledge-base-uds-can-packet>`.
    """

    __DATA_USAGE_BY_ADDRESSING_FORMAT: Dict[CanAddressingFormat, int] = {
        CanAddressingFormat.NORMAL_11BIT_ADDRESSING: 0,
        CanAddressingFormat.NORMAL_FIXED_ADDRESSING: 0,
        CanAddressingFormat.EXTENDED_ADDRESSING: 1,
        CanAddressingFormat.MIXED_11BIT_ADDRESSING: 1,
        CanAddressingFormat.MIXED_29BIT_ADDRESSING: 1,
    }

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
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Source Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Address Extension parameter.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            - None - use CAN Data Frame Optimization (CAN ID value would be automatically determined)
            - int type value - DLC value to set, CAN Data Padding will be used
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            - payload (required for: SF, FF and CF): Diagnostic message data that are carried by this CAN packet.
            - data_length (required for: FF): Number of bytes that a diagnostic message carried by this CAN packet has.
            - sequence_number (required for: CF): Sequence number of a Consecutive Frame.
            - flow_status (required for: FC): Flow status information carried by a Flow Control frame.
            - block_size (optional for: FC): Block size information carried by a Flow Control frame.
            - stmin (optional for: FC): Separation Time minimum information carried by a Flow Control frame.
        """
        self.__raw_frame_data = None
        self.__addressing = None
        self.__addressing_format = None
        self.__packet_type = None
        self.__can_id = None
        self.__dlc = None
        self.__target_address = None
        self.__address_extension = None
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
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Source Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Address Extension parameter.

        :raise NotImplementedError: A valid addressing format was provided, but the implementation is missing.
        """
        self.validate_address_information(addressing=addressing,
                                          addressing_format=addressing_format,
                                          can_id=can_id,
                                          target_address=target_address,
                                          source_address=source_address,
                                          address_extension=address_extension)
        can_addressing_format_instance = CanAddressingFormat(addressing_format)
        if can_addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            self.__set_address_information_normal_11bit(addressing=addressing,
                                                        can_id=can_id)
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            self.__set_address_information_normal_fixed(addressing=addressing,
                                                        can_id=can_id,
                                                        target_address=target_address,
                                                        source_address=source_address)
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            self.__set_address_information_extended(addressing=addressing,
                                                    can_id=can_id,
                                                    target_address=target_address)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            self.__set_address_information_mixed_11bit(addressing=addressing,
                                                       can_id=can_id,
                                                       address_extension=address_extension)
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            self.__set_address_information_mixed_29bit(addressing=addressing,
                                                       can_id=can_id,
                                                       target_address=target_address,
                                                       source_address=source_address,
                                                       address_extension=address_extension)
        else:
            raise NotImplementedError(f"Unknown CAN Addressing Format value was provided: "
                                      f"{can_addressing_format_instance}")

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
            Leave None if `use_data_optimization` argument is set to True.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            - payload (required for: SF, FF and CF): Diagnostic message data that are carried by this CAN packet.
            - data_length (required for: FF): Number of bytes that a diagnostic message carried by this CAN packet has.
            - sequence_number (required for: CF): Sequence number of a Consecutive Frame.
            - flow_status (required for: FC): Flow status information carried by a Flow Control frame.
            - block_size (optional for: FC): Block size information carried by a Flow Control frame.
            - stmin (optional for: FC): Separation Time minimum information carried by a Flow Control frame.

        :raise NotImplementedError: A valid packet type was provided, but there is no implementation for it.
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
        and arguments are consistent with provided :ref:`CAN Addressing Format <knowledge-base-can-addressing>`.

        :param addressing: Addressing type to validate.
        :param addressing_format: CAN addressing format to validate.
        :param can_id: CAN Identifier that is used to transmit this packet. TODO
        :param target_address: Target Address value carried by this CAN Packet.
        :param source_address: Source Address value carried by this CAN packet.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        AddressingType.validate_member(addressing)
        CanAddressingFormat.validate_member(addressing_format)
        cls.__validate_ai_consistency(addressing=addressing,
                                      addressing_format=addressing_format,
                                      can_id=can_id,
                                      target_address=target_address,
                                      source_address=source_address,
                                      address_extension=address_extension)

    @property
    def raw_frame_data(self) -> RawBytesTuple:
        """
        Raw data bytes of a CAN frame that carries this CAN packet.

        Data field of a :ref:`CAN frame <knowledge-base-can-frame>` that is determined by CAN packet information.
        """
        return self.__raw_frame_data

    @property
    def addressing(self) -> AddressingType:
        """
        Addressing type for which this CAN packet is relevant.

        :ref:`Addressing type <_knowledge-base-addressing>` value in CAN packet is determined by CAN ID value.
        """
        return self.__addressing

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """
        CAN addressing format of this CAN packet.

        Each :ref:`CAN addressing format <knowledge-base-can-addressing>` describes a different way of providing
        :ref:`Network Address Information <_knowledge-base-n-ai>` to all recipients of CAN packets."""
        return self.__addressing_format

    @property
    def packet_type(self) -> CanPacketType:
        """
        Type of this CAN packet.

        :ref:`CAN packet type <knowledge-base-can-n-pci>` provides CAN specific
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>`.
        """
        return self.__packet_type

    @property
    def can_id(self) -> int:
        """
        CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet.

        CAN ID value informs every receiving CAN node about a sender and a content of
        :ref:`CAN Frames <knowledge-base-can-frame>`.
        """
        return self.__can_id

    @property
    def dlc(self) -> int:
        """
        Data Length Code (DLC) of a CAN Frame that carries this CAN packet.

        DLC value determines number of bytes that :ref:`CAN Frame <knowledge-base-can-frame>` contains.
        """
        return self.__dlc

    @property
    def address_extension(self) -> Optional[RawByte]:
        """
        Address Extension (AE) value of this CAN Packet.

        AE and CAN ID values specifies sending and receiving entity during UDS communication over CAN.

        Address Extension is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Mixed Addressing <knowledge-base-can-mixed-addressing>` - either:
           - :ref:`Mixed 11-bit Addressing <knowledge-base-can-mixed-11-bit-addressing>`
           - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`
        """
        return self.__address_extension

    @property
    def target_address(self) -> Optional[RawByte]:
        """
        Target Address (TA) value of this CAN Packet.

        TA specifies receiving entity during UDS communication over CAN.

        Target Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Extended Addressing <knowledge-base-can-extended-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`
        """
        return self.__target_address

    @property
    def source_address(self) -> Optional[RawByte]:
        """
        Source Address (SA) value of this CAN Packet.

        SA specifies sending entity during UDS communication over CAN.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-can-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-can-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-can-mixed-29-bit-addressing>`
        """

    @property
    def payload(self) -> Optional[RawBytesTuple]:
        """
        Diagnostic message payload carried by this CAN packet.

        .. note:: This value is only present for packets of following types:

            - :ref:`Single Frame <knowledge-base-can-single-frame>`
            - :ref:`First Frame <knowledge-base-can-first-frame>`
            - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        .. warning:: For :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` this field might contain
            additional filler bytes (they are not part of diagnostic message payload) that were added during
            :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`.
            The presence of filler bytes in :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
            cannot be determined solely on the information contained in this packet.
        """

    @property
    def data_length(self) -> Optional[int]:
        ...

    @property
    def sequence_number(self) -> Optional[int]:
        ...

    @property
    def flow_status(self) -> Optional[CanFlowStatus]:
        ...

    @property
    def block_size(self) -> Optional[RawByte]:
        ...

    @property
    def stmin(self) -> Optional[RawByte]:
        ...

    @classmethod
    def __validate_ai_consistency(cls,
                                  addressing: AddressingTypeMemberTyping,
                                  addressing_format: CanAddressingFormatTyping,
                                  can_id: Optional[int],
                                  target_address: Optional[RawByte],
                                  source_address: Optional[RawByte],
                                  address_extension: Optional[RawByte]) -> None:
        # TODO: docstring
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
        # TODO: docstring
        if (target_address, source_address, address_extension) != (None, None, None):
            raise UnusedArgumentError  # TODO: text
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_normal_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError  # TODO: text

    @staticmethod
    def __validate_ai_consistency_normal_fixed(addressing: AddressingTypeMemberTyping,
                                               can_id: Optional[int],
                                               target_address: Optional[RawByte],
                                               source_address: Optional[RawByte],
                                               address_extension: Optional[RawByte]) -> None:
        # TODO: docstring
        if address_extension is not None:
            raise UnusedArgumentError  # TODO: text
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError  # TODO: text
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
            if (target_address, source_address) != (None, None):
                raise InconsistentArgumentsError  # TODO: text
            CanIdHandler.validate_can_id(can_id)
            if not CanIdHandler.is_normal_fixed_addressed_can_id(can_id=can_id, addressing=addressing):
                raise InconsistentArgumentsError  # TODO: text

    @staticmethod
    def __validate_ai_consistency_extended(can_id: Optional[int],
                                           target_address: Optional[RawByte],
                                           source_address: Optional[RawByte],
                                           address_extension: Optional[RawByte]) -> None:
        # TODO: docstring
        if (source_address, address_extension) != (None, None):
            raise UnusedArgumentError  # TODO: text
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_extended_addressed_can_id(can_id):
            raise InconsistentArgumentsError  # TODO: text
        validate_raw_byte(target_address)

    @staticmethod
    def __validate_ai_consistency_mixed_11bit(can_id: Optional[int],
                                              target_address: Optional[RawByte],
                                              source_address: Optional[RawByte],
                                              address_extension: Optional[RawByte]) -> None:
        if (target_address, source_address) != (None, None):
            raise UnusedArgumentError  # TODO: text
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_mixed_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError  # TODO: text
        validate_raw_byte(address_extension)

    @staticmethod
    def __validate_ai_consistency_mixed_29bit(addressing: AddressingTypeMemberTyping,
                                              can_id: Optional[int],
                                              target_address: Optional[RawByte],
                                              source_address: Optional[RawByte],
                                              address_extension: Optional[RawByte]) -> None:
        validate_raw_byte(address_extension)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError  # TODO: text
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
            if (target_address, source_address) != (None, None):
                raise InconsistentArgumentsError  # TODO: text
            CanIdHandler.validate_can_id(can_id)
            if not CanIdHandler.is_mixed_29bit_addressed_can_id(can_id=can_id, addressing=addressing):
                raise InconsistentArgumentsError  # TODO: text

    def __set_address_information_normal_11bit(self, addressing: AddressingType, can_id: int) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using normal 11-bit addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed due to incompatibility
            with previously used addressing format.
        :raise ValueError: Provided value of CAN ID is not compatible with this addressing format.
        """

    def __set_address_information_normal_fixed(self,
                                               addressing: AddressingType,
                                               can_id: Optional[int] = None,
                                               target_address: Optional[RawByte] = None,
                                               source_address: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using normal fixed addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then CAN ID value would be assessed basing on addressing, target_address and source_address values.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if can_id value is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if can_id value is provided.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed due to incompatibility
            with previously used addressing format.
        :raise InconsistentArgumentsError: Provided values of addressing, can_id, target_address and source_address
            are not compatible.
        """

    def __set_address_information_extended(self,
                                           addressing: AddressingType,
                                           can_id: int,
                                           target_address: RawByte) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using extended addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
        :param target_address: Target Address value carried by this CAN packet.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed due to incompatibility
            with previously used addressing format.
        """

    def __set_address_information_mixed_11bit(self,
                                              addressing: AddressingType,
                                              can_id: int,
                                              address_extension: RawByte) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using mixed 11-bit addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
        :param address_extension: Address Extension value carried by this CAN packet.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed due to incompatibility
            with previously used addressing format.
        :raise ValueError: Provided value of CAN ID is not compatible with this addressing format.
        """

    def __set_address_information_mixed_29bit(self,
                                              addressing: AddressingType,
                                              address_extension: RawByte,
                                              can_id: Optional[int] = None,
                                              target_address: Optional[RawByte] = None,
                                              source_address: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information for this CAN Packet to a value using mixed 29-bit addressing format.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param address_extension: Address Extension value carried by this CAN packet.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then CAN ID value would be assessed basing on addressing, target_address and source_address values.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if can_id value is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if can_id value is provided.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed due to incompatibility
            with previously used addressing format.
        :raise InconsistentArgumentsError: Provided values of addressing, can_id, target_address and source_address
            are not compatible.
        """


class CanPacketRecord(AbstractUdsPacketRecord):
    ...

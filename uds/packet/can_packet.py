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
from uds.utilities import RawByte, RawBytesTuple

from .abstract_packet import AbstractUdsPacket, AbstractUdsPacketRecord
from .can_packet_attributes import DEFAULT_FILLER_BYTE, CanAddressingFormat, CanAddressingFormatTyping, \
    CanPacketType, CanPacketTypeMemberTyping
from .can_flow_control import CanFlowStatus


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
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = None
        self.__dlc = None
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
            If None, then an attempt would be made to assess the CAN ID value basing on other provided arguments.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.

        :raise NotImplementedError: A valid addressing format was provided, but there is no implementation for it.
        """

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
        return self.__source_address

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
    def dlc(self) -> int:
        """
        Data Length Code (DLC) of a CAN Frame that carries this CAN packet.

        DLC value determines number of bytes that :ref:`CAN Frame <knowledge-base-can-frame>` contains.
        """
        return self.__dlc

    @property
    def payload(self) -> Optional[RawBytesTuple]:
        ...

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


class CanPacketRecord(AbstractUdsPacketRecord):
    ...

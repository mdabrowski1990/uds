"""
CAN bus specific implementation of UDS packets.

:ref:`CAN packets <knowledge-base-uds-can-packet>`.
"""

__all__ = ["CanAddressingFormat", "CanPacket", "CanPacketRecord", "IncompatibleCanAddressingFormatError"]

from typing import Any, Union, Optional
from warnings import warn

from aenum import StrEnum, unique

from uds.transmission_attributes import AddressingTypeMemberTyping, AddressingType
from uds.utilities import RawByte, RawBytes, RawBytesTuple, validate_raw_byte, \
    ValidatedEnum, NibbleEnum, TimeMilliseconds, InconsistentArgumentsError

from .abstract_packet import AbstractUdsPacket, AbstractUdsPacketRecord
from .can_packet_attributes import *
from .can_flow_control import *


class IncompatibleCanAddressingFormatError(Exception):
    """
    Addressing information cannot be changed for a CAN packet.

    This error informs about an attempt to change :ref:`Network Address Information <knowledge-base-n-ai>`
    to a value that is not compatible with previously used format.

    .. note:: As a user, you can create a new CAN packet object instead of changing existing one.
    """


class CanPacket(AbstractUdsPacket):
    """
    Definition of a CAN packet.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`CAN packet <knowledge-base-uds-can-packet>`.
    """

    def __init__(self,
                 addressing: AddressingTypeMemberTyping,
                 addressing_format: CanAddressingFormatTyping,
                 packet_type: CanPacketTypeMemberTyping,
                 can_id: Optional[int] = None,
                 target_address: Optional[RawByte] = None,
                 source_address: Optional[RawByte] = None,
                 address_extension: Optional[RawByte] = None,
                 use_data_optimization: bool = True,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Create a storage for a single CAN packet.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param packet_type: Type of this CAN packet.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then an attempt would be made to assess the CAN ID value basing on other provided arguments.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
        :param use_data_optimization: Flag whether to use CAN Data Frame Optimization during CAN Packet creation.
            - False - CAN Frame Data Padding is used in all cases (`dlc` value must be provided).
            - True - CAN Frame Data Optimization is used whenever possible, CAN Frame Data Padding is used when
              sole CAN Frame Data Optimization is not enough.
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
        """
        self.__addressing = None
        self.__raw_frame_data = None
        self.__packet_type = None
        self.__addressing_format = None
        self.__can_id = None
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = None
        self.__dlc = None
        self.__use_data_optimization = None
        self.__filler_byte = None
        self.set_address_information(addressing=addressing,
                                     addressing_format=addressing_format,
                                     can_id=can_id,
                                     target_address=target_address,
                                     source_address=source_address,
                                     address_extension=address_extension)
        self.set_data(packet_type=packet_type,
                      use_data_optimization=use_data_optimization,
                      dlc=dlc,
                      filler_byte=filler_byte,
                      **packet_type_specific_kwargs)

    def set_address_information(self,
                                addressing: AddressingTypeMemberTyping,
                                addressing_format: CanAddressingFormatTyping,
                                *,
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
        """
        self.__validate_address_information(addressing=addressing, addressing_format=addressing_format, can_id=can_id,
                                            target_address=target_address, source_address=source_address,
                                            address_extension=address_extension)

        # convert arguments
        addressing_type_instance = AddressingType(addressing)
        can_addressing_format_instance = CanAddressingFormat(addressing_format)
        # set values
        if can_addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            ...
        elif can_addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            ...
        else:
            raise NotImplementedError

    def __set_address_information_normal_11bit(self, addressing: AddressingType, can_id: int) -> None:
        """
        Set or change addressing information to normal 11-bit addressing for this CAN Packet.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed to Normal 11-bit Addressing
            format as previously used format is not compatible with it.
        :raise ValueError: Provided value of CAN ID is not using Normal 11-bit Addressing format.
        """
        if self.addressing_format not in (None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                          CanAddressingFormat.NORMAL_FIXED_ADDRESSING):
            raise IncompatibleCanAddressingFormatError(f"Cannot switch to CAN Normal 11-bit Addressing from "
                                                       f"{self.addressing_format}")
        if not CanIdHandler.is_normal_11bit_addressed_can_id(can_id):
            raise ValueError(f"Provided can_id value is not using Normal 11-bit Addressing format. "
                             f"Actual value: {can_id}")
        self.__addressing = addressing
        self.__addressing_format = CanAddressingFormat.NORMAL_11BIT_ADDRESSING
        self.__can_id = can_id
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = None

    def __set_address_information_normal_fixed(self,
                                               addressing: AddressingType,
                                               can_id: Optional[int] = None,
                                               target_address: Optional[RawByte] = None,
                                               source_address: Optional[RawByte] = None) -> None:
        """
        Set or change addressing information to normal fixed addressing for this CAN Packet.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier that is used to transmit this packet.
            If None, then CAN ID value would be assessed basing on addressing, target_address and source_address values.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if can_id value is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if can_id value is provided.

        :raise IncompatibleCanAddressingFormatError: Addressing format cannot be changed to Normal Fixed Addressing
            format as previously used format is not compatible with it.
        :raise InconsistentArgumentsError: Provided values of addressing, can_id, target_address and source_address
            are not compatible.
        """
        if self.addressing_format not in (None, CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                          CanAddressingFormat.NORMAL_FIXED_ADDRESSING):
            raise IncompatibleCanAddressingFormatError(f"Cannot switch to CAN Normal Fixed Addressing from "
                                                       f"{self.addressing_format}")
        if can_id is None:
            if target_address is None or source_address is None:
                raise InconsistentArgumentsError("Either can_id or target_address and source_address values must be"
                                                 "provided.")
            self.__can_id = CanIdHandler.get_normal_fixed_addressed_can_id(addressing_type=addressing,
                                                                           target_address=target_address,
                                                                           source_address=source_address)
            self.__target_address = target_address
            self.__source_address = source_address
        else:
            decoded_addressing, decoded_target_address, decoded_source_address = \
                CanIdHandler.decode_normal_fixed_addressed_can_id(can_id=can_id)
            if decoded_addressing != addressing:
                raise InconsistentArgumentsError("Provided values of addressing and can_id does not match. "
                                                 f"Actual values: addressing={addressing}, can_id={can_id}")
            if target_address not in (None, decoded_target_address):
                raise InconsistentArgumentsError("Provided values of target_address and can_id does not match. "
                                                 f"Actual values: target_address={target_address}, can_id={can_id}")
            if source_address not in (None, decoded_source_address):
                raise InconsistentArgumentsError("Provided values of source_address and can_id does not match. "
                                                 f"Actual values: source_address={source_address}, can_id={can_id}")
            self.__can_id = can_id
            self.__target_address = decoded_target_address
            self.__source_address = decoded_source_address
        self.__addressing = addressing
        self.__addressing_format = CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        self.__address_extension = None

    def set_data(self,
                 packet_type: CanPacketTypeMemberTyping,
                 *,
                 use_data_optimization: bool = True,
                 dlc: Optional[int] = None,
                 filler_byte: RawByte = DEFAULT_FILLER_BYTE,
                 **packet_type_specific_kwargs: Any) -> None:
        """

        :param packet_type:
        :param use_data_optimization:
        :param dlc:
        :param filler_byte:
        :param packet_type_specific_kwargs:

        :raise TypeError:
        :raise ValueError:
        """

    @staticmethod
    def __validate_address_information(addressing: AddressingTypeMemberTyping,
                                       addressing_format: CanAddressingFormatTyping,
                                       can_id: Optional[int],
                                       target_address: Optional[RawByte],
                                       source_address: Optional[RawByte],
                                       address_extension: Optional[RawByte]) -> None:
        """
        Validate addressing information arguments has proper types and values in range.

        Only sanity check is performed (whether types and values are in range). Values cross compatibility is
        not checked.

        :param addressing: Addressing type for which this CAN packet is relevant.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param can_id: CAN Identifier that is used to transmit this packet.
        :param target_address: Target Address value carried by this CAN Packet.
        :param source_address: Source Address value carried by this CAN packet.
        :param address_extension: Address Extension value carried by this CAN packet.

        :raise TypeError: At least one argument has invalid type (incompatible with annotation).
        :raise ValueError: At least one argument has invalid value.
        """
        AddressingType.validate_member(addressing)
        CanAddressingFormat.validate_member(addressing_format)
        if can_id is not None:
            CanIdHandler.validate_can_id(can_id)
        if target_address is not None:
            validate_raw_byte(target_address)
        if source_address is not None:
            validate_raw_byte(source_address)
        if address_extension is not None:
            validate_raw_byte(address_extension)

    def __set_single_frame_data(self, payload: RawBytes) -> None:
        """

        :param payload:

        :raise TypeError:
        :raise ValueError:
        """

    def __set_first_frame_data(self, data_length: int, payload: RawBytes) -> None:
        """

        :param data_length:
        :param payload:

        :raise TypeError:
        :raise ValueError:
        """

    def __set_consecutive_frame_data(self, sequence_number: int, payload: RawBytes) -> None:
        """

        :param sequence_number:
        :param payload:

        :raise TypeError:
        :raise ValueError:
        """

    def __set_flow_control_data(self,
                                flow_status: CanFlowStatusTyping,
                                block_size: Optional[RawByte] = None,
                                stmin: Optional[RawByte] = None) -> None:
        """

        :param flow_status:
        :param block_size:
        :param stmin:

        :raise TypeError:
        :raise ValueError:
        """

    @property
    def addressing(self) -> AddressingType:
        """
        Addressing type for which this CAN packet is relevant.

        :ref:`Addressing type <_knowledge-base-addressing>` value in CAN packet is determined by CAN ID value.
        """
        return self.__addressing

    @property
    def raw_frame_data(self) -> RawBytesTuple:
        """
        Raw data bytes of a CAN frame that carries this CAN packet.

        Data field of a :ref:`CAN frame <knowledge-base-can-frame>` that is determined by CAN packet information.
        """
        return self.__raw_frame_data

    @property
    def packet_type(self) -> CanPacketType:
        """
        Type of this CAN packet.

        :ref:`CAN packet type <knowledge-base-can-n-pci>` provides CAN specific
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>`.
        """
        return self.__packet_type

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """
        CAN addressing format of this CAN packet.

        Each :ref:`CAN addressing format <knowledge-base-can-addressing>` describes a different way of providing
        :ref:`Network Address Information <_knowledge-base-n-ai>` to all recipients of CAN packets."""
        return self.__addressing_format

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
    def use_data_optimization(self) -> bool:
        """
        Information whether this UDS packet uses CAN Frame Data Optimization.

        Values mapping:
         - False - :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` is used in all cases
         - True - :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is used whenever possible
           with :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` being used in special cases that
           sole :ref:`CAN Frame Data Optimization <knowledge-base-can-data-optimization>` is not enough
        """
        return self.__use_data_optimization

    @property
    def filler_byte(self) -> RawByte:
        """
        Value of Filler Byte that is used for CAN Frame Data Padding.

        Frequency of Filler Byte use depends on :attr:`~uds.packet.can_packet.CanPacket.use_data_optimization` value as
        it determines in which cases :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>` is used.
        """
        return self.__filler_byte


class CanPacketRecord(AbstractUdsPacketRecord):
    ...

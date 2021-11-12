"""CAN bus specific implementation of UDS packets."""

__all__ = ["CanPacket"]

from typing import Optional, Any
from warnings import warn

from uds.utilities import RawByte, RawBytes, RawBytesTuple, AmbiguityError, UnusedArgumentWarning
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from uds.packet import AbstractUdsPacket
from .can_frame_fields import CanIdHandler, CanDlcHandler, DEFAULT_FILLER_BYTE
from .packet_type import CanPacketType, CanPacketTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .single_frame import CanSingleFrameHandler
from .first_frame import CanFirstFrameHandler
from .consecutive_frame import CanConsecutiveFrameHandler
from .flow_control import CanFlowControlHandler, CanFlowStatus, CanFlowStatusAlias


class CanPacket(AbstractUdsPacket):
    """
    Definition of a CAN packet.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`CAN packet <knowledge-base-uds-can-packet>`.
    """

    def __init__(self, *,
                 packet_type: CanPacketTypeAlias,
                 addressing_format: CanAddressingFormatAlias,
                 addressing_type: AddressingTypeAlias,
                 can_id: Optional[int] = None,
                 target_address: Optional[RawByte] = None,
                 source_address: Optional[RawByte] = None,
                 address_extension: Optional[RawByte] = None,
                 dlc: Optional[int] = None,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Create a storage for a single CAN packet.

        :param packet_type: Type of this CAN packet.
        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param addressing_type: Addressing type for which this CAN packet is relevant.
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
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter filler_byte: (optional for: SF, CF and FC)
                 Filler Byte value to use for CAN Frame Data Padding.
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by this CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes of a diagnostic message initiated by this First Frame packet.
             - :parameter sequence_number: (required for: CF)
                 Sequence number value of this Consecutive Frame.
             - :parameter flow_status: (required for: FC)
                 Flow status information carried by this Flow Control frame.
             - :parameter block_size: (required for: FC ContinueToSend Flow Status)
                 Block size information carried by this Flow Control frame.
             - :parameter st_min: (required for: FC ContinueToSend Flow Status)
                 Separation Time minimum information carried by this Flow Control frame.
        """
        # initialize the variables
        self.__raw_frame_data: RawBytesTuple = None  # type: ignore
        self.__addressing_type: AddressingType = None  # type: ignore
        self.__addressing_format: CanAddressingFormat = None  # type: ignore
        self.__packet_type: CanPacketType = None  # type: ignore
        self.__can_id: int = None  # type: ignore
        self.__dlc: int = None  # type: ignore
        self.__target_address: Optional[RawByte] = None
        self.__source_address: Optional[RawByte] = None
        self.__address_extension: Optional[RawByte] = None
        # set the proper attribute values after arguments validation
        self.set_address_information(addressing_type=addressing_type,
                                     addressing_format=addressing_format,
                                     can_id=can_id,
                                     target_address=target_address,
                                     source_address=source_address,
                                     address_extension=address_extension)
        self.set_packet_data(packet_type=packet_type,
                             dlc=dlc,
                             **packet_type_specific_kwargs)

    def set_address_information(self, *,
                                addressing_format: CanAddressingFormatAlias,
                                addressing_type: AddressingTypeAlias,
                                can_id: Optional[int] = None,
                                target_address: Optional[RawByte] = None,
                                source_address: Optional[RawByte] = None,
                                address_extension: Optional[RawByte] = None) -> None:
        """
        Change addressing information for this CAN packet.

        This function enables to change an entire :ref:`Network Address Information <knowledge-base-n-ai>`
        for a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param addressing_format: CAN addressing format that this CAN packet uses.
        :param addressing_type: Addressing type for which this CAN packet is relevant.
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
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            self.set_address_information_normal_11bit(addressing_type=addressing_type,
                                                      can_id=can_id)
            if (target_address, source_address, address_extension) != (None, None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: target_address={target_address}, source_address={source_address}, "
                             f"address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            self.set_address_information_normal_fixed(addressing_type=addressing_type,
                                                      can_id=can_id,
                                                      target_address=target_address,
                                                      source_address=source_address)
            if address_extension is not None:
                warn(message=f"Unused argument was provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual value: address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            self.set_address_information_extended(addressing_type=addressing_type,
                                                  can_id=can_id,
                                                  target_address=target_address)
            if (source_address, address_extension) != (None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: source_address={source_address}, address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            self.set_address_information_mixed_11bit(addressing_type=addressing_type,
                                                     can_id=can_id,
                                                     address_extension=address_extension)
            if (target_address, source_address) != (None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: target_address={target_address}, source_address={source_address}, ",
                     category=UnusedArgumentWarning)
        elif addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            self.set_address_information_mixed_29bit(addressing_type=addressing_type,
                                                     can_id=can_id,
                                                     target_address=target_address,
                                                     source_address=source_address,
                                                     address_extension=address_extension)
        else:
            raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    def set_address_information_normal_11bit(self, addressing_type: AddressingTypeAlias, can_id: int) -> None:
        """
        Change addressing information for this CAN packet to use Normal 11-bit Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        """
        CanAddressingInformationHandler.validate_ai_normal_11bit(addressing_type=addressing_type, can_id=can_id)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_11BIT_ADDRESSING)
        self.__addressing_format = CanAddressingFormat.NORMAL_11BIT_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__can_id = can_id
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = None

    def set_address_information_normal_fixed(self,
                                             addressing_type: AddressingTypeAlias,
                                             can_id: Optional[int] = None,
                                             target_address: Optional[RawByte] = None,
                                             source_address: Optional[RawByte] = None) -> None:
        """
        Change addressing information for this CAN packet to use Normal Fixed Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            Leave None if the values of `target_address` and `source_address` parameters are provided.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if the value of `can_id` parameter is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if the value of `can_id` parameter is provided.
        """
        CanAddressingInformationHandler.validate_ai_normal_fixed(addressing_type=addressing_type,
                                                                 can_id=can_id,
                                                                 target_address=target_address,
                                                                 source_address=source_address)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        if can_id is None:
            self.__can_id = CanIdHandler.encode_normal_fixed_addressed_can_id(addressing_type=addressing_type,
                                                                              target_address=target_address,
                                                                              source_address=source_address)
            self.__source_address = source_address
            self.__target_address = target_address
        else:
            self.__can_id = can_id
            ai_info = CanIdHandler.decode_normal_fixed_addressed_can_id(can_id)
            self.__source_address = ai_info[CanIdHandler.SOURCE_ADDRESS_NAME]
            self.__target_address = ai_info[CanIdHandler.TARGET_ADDRESS_NAME]
        self.__addressing_format = CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__address_extension = None

    def set_address_information_extended(self,
                                         addressing_type: AddressingTypeAlias,
                                         can_id: int,
                                         target_address: RawByte) -> None:
        """
        Change addressing information for this CAN packet to use Extended Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        :param target_address: Target Address value carried by this CAN Packet.
        """
        CanAddressingInformationHandler.validate_ai_extended(addressing_type=addressing_type,
                                                             can_id=can_id,
                                                             target_address=target_address)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.EXTENDED_ADDRESSING)
        self.__addressing_format = CanAddressingFormat.EXTENDED_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__can_id = can_id
        self.__target_address = target_address
        self.__source_address = None
        self.__address_extension = None

    def set_address_information_mixed_11bit(self,
                                            addressing_type: AddressingTypeAlias,
                                            can_id: int,
                                            address_extension: RawByte) -> None:
        """
        Change addressing information for this CAN packet to use Mixed 11-bit Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        CanAddressingInformationHandler.validate_ai_mixed_11bit(addressing_type=addressing_type,
                                                                can_id=can_id,
                                                                address_extension=address_extension)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_11BIT_ADDRESSING)
        self.__addressing_format = CanAddressingFormat.MIXED_11BIT_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__can_id = can_id
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = address_extension

    def set_address_information_mixed_29bit(self,
                                            addressing_type: AddressingTypeAlias,
                                            address_extension: RawByte,
                                            can_id: Optional[int] = None,
                                            target_address: Optional[RawByte] = None,
                                            source_address: Optional[RawByte] = None) -> None:
        """
        Change addressing information for this CAN packet to use Mixed 29-bit Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            Leave None if the values of `target_address` and `source_address` parameters are provided.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if the value of `can_id` parameter is provided.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if the value of `can_id` parameter is provided.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        CanAddressingInformationHandler.validate_ai_mixed_29bit(addressing_type=addressing_type,
                                                                can_id=can_id,
                                                                target_address=target_address,
                                                                source_address=source_address,
                                                                address_extension=address_extension)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_29BIT_ADDRESSING)
        if can_id is None:
            self.__can_id = CanIdHandler.encode_mixed_addressed_29bit_can_id(addressing_type=addressing_type,
                                                                             target_address=target_address,
                                                                             source_address=source_address)
            self.__source_address = source_address
            self.__target_address = target_address
        else:
            self.__can_id = can_id
            ai_info = CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id)
            self.__source_address = ai_info[CanIdHandler.SOURCE_ADDRESS_NAME]
            self.__target_address = ai_info[CanIdHandler.TARGET_ADDRESS_NAME]
        self.__addressing_format = CanAddressingFormat.MIXED_29BIT_ADDRESSING  # type: ignore
        self.__addressing_type = AddressingType(addressing_type)
        self.__address_extension = address_extension

    def set_packet_data(self, *,
                        packet_type: CanPacketTypeAlias,
                        dlc: Optional[int] = None,
                        **packet_type_specific_kwargs: Any) -> None:
        """
        Change packet type and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`CAN packet <knowledge-base-uds-can-packet>`.

        :param packet_type: Type of this CAN packet.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
            You have to provide DLC value for packets of First Frame type.
        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.
            Possible parameters:
             - :parameter filler_byte: (optional for: SF, CF and FC)
                 Filler Byte value to use for CAN Frame Data Padding.
             - :parameter payload: (required for: SF, FF and CF)
                 Payload of a diagnostic message that is carried by this CAN packet.
             - :parameter data_length: (required for: FF)
                 Number of payload bytes of a diagnostic message initiated by this First Frame packet.
             - :parameter sequence_number: (required for: CF)
                 Sequence number value of this Consecutive Frame.
             - :parameter flow_status: (required for: FC)
                 Flow status information carried by this Flow Control frame.
             - :parameter block_size: (required for: FC ContinueToSend Flow Status)
                 Block size information carried by this Flow Control frame.
             - :parameter st_min: (required for: FC ContinueToSend Flow Status)
                 Separation Time minimum information carried by this Flow Control frame.

        :raise NotImplementedError: A valid packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        CanPacketType.validate_member(packet_type)
        if packet_type == CanPacketType.SINGLE_FRAME:
            self.set_single_frame_data(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type == CanPacketType.FIRST_FRAME:
            self.set_first_frame_data(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type == CanPacketType.CONSECUTIVE_FRAME:
            self.set_consecutive_frame_data(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type == CanPacketType.FLOW_CONTROL:
            self.set_flow_control_data(dlc=dlc, **packet_type_specific_kwargs)
        else:
            raise NotImplementedError(f"Missing implementation for: {packet_type}")

    def set_single_frame_data(self,
                              payload: RawBytes,
                              dlc: Optional[int] = None,
                              filler_byte: RawByte = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Single Frame) and data field of this CAN packet.

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
        raw_frame_data = CanSingleFrameHandler.create_valid_frame_data(addressing_format=self.addressing_format,
                                                                       target_address=self.target_address,
                                                                       address_extension=self.address_extension,
                                                                       dlc=dlc,
                                                                       payload=payload,
                                                                       filler_byte=filler_byte)
        self.__raw_frame_data = tuple(raw_frame_data)
        self.__dlc = dlc or CanDlcHandler.encode_dlc(len(raw_frame_data))
        self.__packet_type = CanPacketType.SINGLE_FRAME  # type: ignore

    def set_first_frame_data(self,
                             dlc: int,
                             payload: RawBytes,
                             data_length: int) -> None:
        """
        Change packet type (to First Frame) and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`First Frame <knowledge-base-can-first-frame>`.

        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
        :param payload: Payload of a diagnostic message that is carried by this CAN packet.
        :param data_length: Number of payload bytes of a diagnostic message initiated by this First Frame packet.
        """
        raw_frame_data = CanFirstFrameHandler.create_valid_frame_data(addressing_format=self.addressing_format,
                                                                      target_address=self.target_address,
                                                                      address_extension=self.address_extension,
                                                                      dlc=dlc,
                                                                      payload=payload,
                                                                      ff_dl=data_length)
        self.__raw_frame_data = tuple(raw_frame_data)
        self.__dlc = dlc
        self.__packet_type = CanPacketType.FIRST_FRAME  # type: ignore

    def set_consecutive_frame_data(self,
                                   payload: RawBytes,
                                   sequence_number: int,
                                   dlc: Optional[int] = None,
                                   filler_byte: RawByte = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Consecutive Frame) and data field of this CAN packet.

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
        raw_frame_data = CanConsecutiveFrameHandler.create_valid_frame_data(addressing_format=self.addressing_format,
                                                                            target_address=self.target_address,
                                                                            address_extension=self.address_extension,
                                                                            dlc=dlc,
                                                                            payload=payload,
                                                                            sequence_number=sequence_number,
                                                                            filler_byte=filler_byte)
        self.__raw_frame_data = tuple(raw_frame_data)
        self.__dlc = dlc or CanDlcHandler.encode_dlc(len(raw_frame_data))
        self.__packet_type = CanPacketType.CONSECUTIVE_FRAME  # type: ignore

    def set_flow_control_data(self,
                              flow_status: CanFlowStatusAlias,
                              block_size: Optional[RawByte] = None,
                              st_min: Optional[RawByte] = None,
                              dlc: Optional[int] = None,
                              filler_byte: RawByte = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Flow Control) and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Flow Control <knowledge-base-can-flow-control>`.

        :param flow_status: Flow status information carried by this Flow Control frame.
        :param block_size: Block size information carried by this Flow Control frame.
        :param st_min: Separation Time minimum information carried by this Flow Control frame.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.
            Possible values:
             - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
             - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.
        :param filler_byte: Filler Byte value to use for CAN Frame Data Padding.
        """
        raw_frame_data = CanFlowControlHandler.create_valid_frame_data(addressing_format=self.addressing_format,
                                                                       target_address=self.target_address,
                                                                       address_extension=self.address_extension,
                                                                       dlc=dlc,
                                                                       flow_status=flow_status,
                                                                       block_size=block_size,
                                                                       st_min=st_min,
                                                                       filler_byte=filler_byte)
        self.__raw_frame_data = tuple(raw_frame_data)
        self.__dlc = dlc or CanDlcHandler.encode_dlc(len(raw_frame_data))
        self.__packet_type = CanPacketType.FLOW_CONTROL  # type: ignore

    @property
    def raw_frame_data(self) -> RawBytesTuple:
        """Raw data bytes of a CAN frame that carries this CAN packet."""
        return self.__raw_frame_data

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type for which this CAN packet is relevant."""
        return self.__addressing_type

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN addressing format used by this CAN packet."""
        return self.__addressing_format

    @property
    def packet_type(self) -> CanPacketType:
        """Type (N_PCI value) of this CAN packet."""
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
        return self.__source_address

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
        if self.packet_type == CanPacketType.SINGLE_FRAME:
            return tuple(CanSingleFrameHandler.decode_payload(addressing_format=self.addressing_format,
                                                              raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.FIRST_FRAME:
            return tuple(CanFirstFrameHandler.decode_payload(addressing_format=self.addressing_format,
                                                             raw_frame_data=self.raw_frame_data))
        if self.packet_type == CanPacketType.CONSECUTIVE_FRAME:
            return tuple(CanConsecutiveFrameHandler.decode_payload(addressing_format=self.addressing_format,
                                                                   raw_frame_data=self.raw_frame_data))
        return None

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
        if self.packet_type == CanPacketType.SINGLE_FRAME:
            return CanSingleFrameHandler.decode_sf_dl(addressing_format=self.addressing_format,
                                                      raw_frame_data=self.raw_frame_data)
        if self.packet_type == CanPacketType.FIRST_FRAME:
            return CanFirstFrameHandler.decode_ff_dl(addressing_format=self.addressing_format,
                                                     raw_frame_data=self.raw_frame_data)
        return None

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Sequence Number carried by this CAN packet.

        :ref:`Sequence Number <knowledge-base-can-sequence-number>` is only provided by packets of following types:
         - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.CONSECUTIVE_FRAME:
            return CanConsecutiveFrameHandler.decode_sequence_number(addressing_format=self.addressing_format,
                                                                     raw_frame_data=self.raw_frame_data)
        return None

    @property
    def flow_status(self) -> Optional[CanFlowStatus]:
        """
        Flow Status carried by this CAN packet.

        :ref:`Flow Status <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-flow-control>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return CanFlowControlHandler.decode_flow_status(addressing_format=self.addressing_format,
                                                            raw_frame_data=self.raw_frame_data)
        return None

    @property
    def block_size(self) -> Optional[RawByte]:
        """
        Block Size value carried by this CAN packet.

        :ref:`Block Size <knowledge-base-can-flow-status>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return CanFlowControlHandler.decode_block_size(addressing_format=self.addressing_format,
                                                           raw_frame_data=self.raw_frame_data)
        return None

    @property
    def st_min(self) -> Optional[RawByte]:
        """
        Separation Time minimum (STmin) value carried by this CAN packet.

        :ref:`STmin <knowledge-base-can-st-min>` is only provided by packets of following types:
         - :ref:`Flow Control <knowledge-base-can-block-size>`

        None in other cases.
        """
        if self.packet_type == CanPacketType.FLOW_CONTROL:
            return CanFlowControlHandler.decode_st_min(addressing_format=self.addressing_format,
                                                       raw_frame_data=self.raw_frame_data)
        return None

    def __validate_unambiguous_ai_change(self, addressing_format: CanAddressingFormatAlias) -> None:
        """
        Validate whether CAN Addressing Format change to provided value is ambiguous.

        :param addressing_format: Desired value of CAN Addressing Format.

        :raise AmbiguityError: Cannot change value because the operation is ambiguous.
        """
        if self.addressing_format is not None \
                and CanAddressingInformationHandler.get_ai_data_bytes_number(addressing_format) \
                != CanAddressingInformationHandler.get_ai_data_bytes_number(self.addressing_format):
            raise AmbiguityError(f"Cannot change CAN Addressing Format from {self.addressing_format} to "
                                 f"{addressing_format} as such operation provides ambiguity. "
                                 f"Create a new CAN Packet object instead.")

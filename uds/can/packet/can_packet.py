"""CAN bus specific implementation for packets."""

__all__ = ["CanPacket"]

from typing import Any, Optional
from warnings import warn

from uds.can import (
    DEFAULT_FILLER_BYTE,
    CanConsecutiveFrameHandler,
    CanDlcHandler,
    CanFirstFrameHandler,
    CanFlowControlHandler,
    CanFlowStatus,
    CanSingleFrameHandler,

)
from uds.addressing import AddressingType, AbstractCanAddressingInformation, CanAddressingFormat, CanAddressingInformation,    ExtendedCanAddressingInformation,    Mixed11BitCanAddressingInformation,    Mixed29BitCanAddressingInformation,    NormalCanAddressingInformation,    NormalFixedCanAddressingInformation
from uds.utilities import AmbiguityError, RawBytesAlias, UnusedArgumentWarning

from uds.packet.abstract_packet import AbstractPacket
from .abstract_can_container import AbstractCanPacketContainer
from .can_packet_type import CanPacketType


class CanPacket(AbstractCanPacketContainer, AbstractPacket):
    """
    Definition of a CAN packet.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`CAN packet <knowledge-base-uds-addressing-packet>`.
    """

    def __init__(self, *,
                 packet_type: CanPacketType,
                 addressing_format: CanAddressingFormat,
                 addressing_type: AddressingType,
                 can_id: Optional[int] = None,
                 target_address: Optional[int] = None,
                 source_address: Optional[int] = None,
                 address_extension: Optional[int] = None,
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

            - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
            - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.

            .. warning:: You have to provide DLC value for packets of First Frame type.

        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.

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
            - :parameter block_size: (required for: FC with ContinueToSend Flow Status)
                Block size information carried by this Flow Control frame.
            - :parameter st_min: (required for: FC with ContinueToSend Flow Status)
                Separation Time minimum information carried by this Flow Control frame.
        """
        # initialize the variables
        self.__raw_frame_data: bytes = None  # type: ignore
        self.__addressing_type: AddressingType = None  # type: ignore
        self.__addressing_format: CanAddressingFormat = None  # type: ignore
        self.__packet_type: CanPacketType = None  # type: ignore
        self.__can_id: int = None  # type: ignore
        self.__dlc: int = None  # type: ignore
        self.__target_address: Optional[int] = None
        self.__source_address: Optional[int] = None
        self.__address_extension: Optional[int] = None
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

    def __str__(self) -> str:
        """Present object in string format."""
        payload_str = "None" if self.payload is None else f"[{', '.join(f'0x{byte:02X}' for byte in self.payload)}]"
        return (f"{self.__class__.__name__}("
                f"payload={payload_str},"
                f"addressing_type={self.addressing_type}, "
                f"addressing_format={self.addressing_format}, "
                f"packet_type={self.packet_type}, "
                f"raw_frame_data=[{', '.join(f'0x{byte:02X}' for byte in self.raw_frame_data)}], "
                f"can_id={self.can_id})")

    def set_address_information(self, *,
                                addressing_format: CanAddressingFormat,
                                addressing_type: AddressingType,
                                can_id: Optional[int] = None,
                                target_address: Optional[int] = None,
                                source_address: Optional[int] = None,
                                address_extension: Optional[int] = None) -> None:
        """
        Change addressing information for this CAN packet.

        This function enables to change an entire :ref:`Network Address Information <knowledge-base-n-ai>`
        for a :ref:`CAN packet <knowledge-base-uds-addressing-packet>`.

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

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.
        """
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format == CanAddressingFormat.NORMAL_ADDRESSING:
            self.set_address_information_normal(addressing_type=addressing_type,
                                                can_id=can_id)  # type: ignore
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
                                                  can_id=can_id,  # type: ignore
                                                  target_address=target_address)  # type: ignore
            if (source_address, address_extension) != (None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: source_address={source_address}, address_extension={address_extension}",
                     category=UnusedArgumentWarning)
        elif addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            self.set_address_information_mixed_11bit(addressing_type=addressing_type,
                                                     can_id=can_id,  # type: ignore
                                                     address_extension=address_extension)  # type: ignore
            if (target_address, source_address) != (None, None):
                warn(message=f"Unused arguments were provided to {CanPacket.set_address_information}. Expected: None."
                             f"Actual values: target_address={target_address}, source_address={source_address}, ",
                     category=UnusedArgumentWarning)
        elif addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            self.set_address_information_mixed_29bit(addressing_type=addressing_type,
                                                     can_id=can_id,
                                                     target_address=target_address,
                                                     source_address=source_address,
                                                     address_extension=address_extension)  # type: ignore
        else:
            raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    def set_address_information_normal(self, addressing_type: AddressingType, can_id: int) -> None:
        """
        Change addressing information for this CAN packet to use Normal Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        """
        NormalCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type, can_id=can_id)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_ADDRESSING)
        self.__addressing_format = CanAddressingFormat.NORMAL_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__can_id = can_id
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = None
        self.__update_ai_data_byte()

    def set_address_information_normal_fixed(self,
                                             addressing_type: AddressingType,
                                             can_id: Optional[int] = None,
                                             target_address: Optional[int] = None,
                                             source_address: Optional[int] = None) -> None:
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
        ai_params = NormalFixedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                           can_id=can_id,
                                                                           target_address=target_address,
                                                                           source_address=source_address)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.NORMAL_FIXED_ADDRESSING)
        self.__can_id = ai_params[AbstractCanAddressingInformation.CAN_ID_NAME]  # type: ignore
        self.__source_address = ai_params[AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME]  # type: ignore
        self.__target_address = ai_params[AbstractCanAddressingInformation.TARGET_ADDRESS_NAME]  # type: ignore
        self.__addressing_format = CanAddressingFormat.NORMAL_FIXED_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__address_extension = None
        self.__update_ai_data_byte()

    def set_address_information_extended(self,
                                         addressing_type: AddressingType,
                                         can_id: int,
                                         target_address: int) -> None:
        """
        Change addressing information for this CAN packet to use Extended Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        :param target_address: Target Address value carried by this CAN Packet.
        """
        ExtendedCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                            can_id=can_id,
                                                            target_address=target_address)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.EXTENDED_ADDRESSING)
        self.__addressing_format = CanAddressingFormat.EXTENDED_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__can_id = can_id
        self.__target_address = target_address
        self.__source_address = None
        self.__address_extension = None
        self.__update_ai_data_byte()

    def set_address_information_mixed_11bit(self,
                                            addressing_type: AddressingType,
                                            can_id: int,
                                            address_extension: int) -> None:
        """
        Change addressing information for this CAN packet to use Mixed 11-bit Addressing format.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
        :param address_extension: Address Extension value carried by this CAN packet.
        """
        Mixed11BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                              can_id=can_id,
                                                              address_extension=address_extension)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_11BIT_ADDRESSING)
        self.__addressing_format = CanAddressingFormat.MIXED_11BIT_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__can_id = can_id
        self.__target_address = None
        self.__source_address = None
        self.__address_extension = address_extension
        self.__update_ai_data_byte()

    def set_address_information_mixed_29bit(self,
                                            addressing_type: AddressingType,
                                            address_extension: int,
                                            can_id: Optional[int] = None,
                                            target_address: Optional[int] = None,
                                            source_address: Optional[int] = None) -> None:
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
        ai_params = Mixed29BitCanAddressingInformation.validate_packet_ai(addressing_type=addressing_type,
                                                                          can_id=can_id,
                                                                          target_address=target_address,
                                                                          source_address=source_address,
                                                                          address_extension=address_extension)
        self.__validate_unambiguous_ai_change(CanAddressingFormat.MIXED_29BIT_ADDRESSING)
        self.__can_id = ai_params[AbstractCanAddressingInformation.CAN_ID_NAME]  # type: ignore
        self.__source_address = ai_params[AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME]  # type: ignore
        self.__target_address = ai_params[AbstractCanAddressingInformation.TARGET_ADDRESS_NAME]  # type: ignore
        self.__addressing_format = CanAddressingFormat.MIXED_29BIT_ADDRESSING
        self.__addressing_type = AddressingType(addressing_type)
        self.__address_extension = address_extension
        self.__update_ai_data_byte()

    def set_packet_data(self, *,
                        packet_type: CanPacketType,
                        dlc: Optional[int] = None,
                        **packet_type_specific_kwargs: Any) -> None:
        """
        Change packet type and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`CAN packet <knowledge-base-uds-addressing-packet>`.

        :param packet_type: Type of this CAN packet.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.

            - None - use CAN Data Frame Optimization (CAN ID value will be automatically determined)
            - int type value - DLC value to set. CAN Data Padding will be used to fill unused data bytes.

            .. warning:: You have to provide DLC value for packets of First Frame type.

        :param packet_type_specific_kwargs: Arguments that are specific for provided CAN Packet Type.

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
            - :parameter block_size: (required for: FC with ContinueToSend Flow Status)
                Block size information carried by this Flow Control frame.
            - :parameter st_min: (required for: FC with ContinueToSend Flow Status)
                Separation Time minimum information carried by this Flow Control frame.

        :raise NotImplementedError: There is missing implementation for the provided CAN Packet Type.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.
        """
        CanPacketType.validate_member(packet_type)
        if packet_type == CanPacketType.SINGLE_FRAME:
            self.set_single_frame_data(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type == CanPacketType.FIRST_FRAME:
            self.set_first_frame_data(dlc=dlc, **packet_type_specific_kwargs)  # type: ignore
        elif packet_type == CanPacketType.CONSECUTIVE_FRAME:
            self.set_consecutive_frame_data(dlc=dlc, **packet_type_specific_kwargs)
        elif packet_type == CanPacketType.FLOW_CONTROL:
            self.set_flow_control_data(dlc=dlc, **packet_type_specific_kwargs)
        else:
            raise NotImplementedError(f"Missing implementation for: {packet_type}")

    def set_single_frame_data(self,
                              payload: RawBytesAlias,
                              dlc: Optional[int] = None,
                              filler_byte: int = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Single Frame) and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Single Frame <knowledge-base-addressing-single-frame>`.

        :param payload: Payload of a diagnostic message that is carried by this CAN packet.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.

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
        self.__raw_frame_data = bytes(raw_frame_data)
        self.__dlc = dlc or CanDlcHandler.encode_dlc(len(raw_frame_data))
        self.__packet_type = CanPacketType.SINGLE_FRAME

    def set_first_frame_data(self,
                             dlc: int,
                             payload: RawBytesAlias,
                             data_length: int) -> None:
        """
        Change packet type (to First Frame) and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`First Frame <knowledge-base-addressing-first-frame>`.

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
        self.__raw_frame_data = bytes(raw_frame_data)
        self.__dlc = dlc
        self.__packet_type = CanPacketType.FIRST_FRAME

    def set_consecutive_frame_data(self,
                                   payload: RawBytesAlias,
                                   sequence_number: int,
                                   dlc: Optional[int] = None,
                                   filler_byte: int = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Consecutive Frame) and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Consecutive Frame <knowledge-base-addressing-first-frame>`.

        :param payload: Payload of a diagnostic message that is carried by this CAN packet.
        :param sequence_number: Sequence number value of this Consecutive Frame.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.

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
        self.__raw_frame_data = bytes(raw_frame_data)
        self.__dlc = dlc or CanDlcHandler.encode_dlc(len(raw_frame_data))
        self.__packet_type = CanPacketType.CONSECUTIVE_FRAME

    def set_flow_control_data(self,
                              flow_status: CanFlowStatus,
                              block_size: Optional[int] = None,
                              st_min: Optional[int] = None,
                              dlc: Optional[int] = None,
                              filler_byte: int = DEFAULT_FILLER_BYTE) -> None:
        """
        Change packet type (to Flow Control) and data field of this CAN packet.

        This function enables to change an entire :ref:`Network Data Field <knowledge-base-n-data>` and
        :ref:`Network Protocol Control Information <knowledge-base-n-pci>` for
        a :ref:`Flow Control <knowledge-base-addressing-flow-control>`.

        :param flow_status: Flow status information carried by this Flow Control frame.
        :param block_size: Block size information carried by this Flow Control frame.
        :param st_min: Separation Time minimum information carried by this Flow Control frame.
        :param dlc: DLC value of a CAN frame that carries this CAN Packet.

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
        self.__raw_frame_data = bytes(raw_frame_data)
        self.__dlc = dlc or CanDlcHandler.encode_dlc(len(raw_frame_data))
        self.__packet_type = CanPacketType.FLOW_CONTROL

    @property
    def raw_frame_data(self) -> bytes:
        """Raw data bytes of a CAN frame that carries this CAN packet."""
        return self.__raw_frame_data

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type for which this CAN packet is relevant."""
        return self.__addressing_type

    @property
    def packet_type(self) -> CanPacketType:
        """Type (N_PCI value) of this CAN packet."""
        return self.__packet_type

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN addressing format used by this CAN packet."""
        return self.__addressing_format

    @property
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""
        return self.__can_id

    @property
    def dlc(self) -> int:
        """Value of Data Length Code (DLC) of a CAN Frame that carries this CAN packet."""
        return self.__dlc

    @property
    def target_address(self) -> Optional[int]:
        """
        Target Address (TA) value of this CAN Packet.

        Target Address value is used with following :ref:`addressing formats <knowledge-base-addressing-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-addressing-normal-fixed-addressing>`
         - :ref:`Extended Addressing <knowledge-base-addressing-extended-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-addressing-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__target_address

    @property
    def source_address(self) -> Optional[int]:
        """
        Source Address (SA) value of this CAN Packet.

        Source Address value is used with following :ref:`addressing formats <knowledge-base-addressing-addressing>`:
         - :ref:`Normal Fixed Addressing <knowledge-base-addressing-normal-fixed-addressing>`
         - :ref:`Mixed 29-bit Addressing <knowledge-base-addressing-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__source_address

    @property
    def address_extension(self) -> Optional[int]:
        """
        Address Extension (AE) value of this CAN Packet.

        Address Extension is used with following :ref:`addressing formats <knowledge-base-addressing-addressing>`:
         - :ref:`Mixed Addressing <knowledge-base-addressing-mixed-addressing>` - either:
           - :ref:`Mixed 11-bit Addressing <knowledge-base-addressing-mixed-11-bit-addressing>`
           - :ref:`Mixed 29-bit Addressing <knowledge-base-addressing-mixed-29-bit-addressing>`

        None in other cases.
        """
        return self.__address_extension

    def __validate_unambiguous_ai_change(self, addressing_format: CanAddressingFormat) -> None:
        """
        Validate whether CAN Addressing Format change to provided value is ambiguous.

        :param addressing_format: Desired value of CAN Addressing Format.

        :raise AmbiguityError: Cannot change value because the operation is ambiguous.
        """
        if self.addressing_format is not None \
                and CanAddressingInformation.get_ai_data_bytes_number(addressing_format) \
                != CanAddressingInformation.get_ai_data_bytes_number(self.addressing_format):
            raise AmbiguityError(f"Cannot change CAN Addressing Format from {self.addressing_format} to "
                                 f"{addressing_format} as such operation provides ambiguity. "
                                 f"Create a new CAN Packet object instead.")

    def __update_ai_data_byte(self) -> None:
        """Update the value of `raw_frame_data` attribute after Addressing Information change."""
        if self.__raw_frame_data is not None:
            ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=self.addressing_format,
                                                                          target_address=self.target_address,
                                                                          address_extension=self.address_extension)
            self.__raw_frame_data = bytes(ai_data_bytes) + bytes(self.__raw_frame_data[len(ai_data_bytes):])

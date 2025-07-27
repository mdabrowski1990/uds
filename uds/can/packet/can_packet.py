"""Implementation of CAN Packet."""

__all__ = ["CanPacket"]

from typing import Any, Optional

from uds.addressing import AddressingType
from uds.packet import AbstractPacket
from uds.utilities import ReassignmentError

from ..addressing import CanAddressingFormat, CanAddressingInformation
from .abstract_container import AbstractCanPacketContainer
from .can_packet_type import CanPacketType
from .consecutive_frame import create_consecutive_frame_data
from .first_frame import create_first_frame_data
from .flow_control import create_flow_control_data
from .single_frame import create_single_frame_data


class CanPacket(AbstractCanPacketContainer, AbstractPacket):
    """
    Definition of a CAN Packet.

    Objects of this class act as a storage for all relevant attributes of a
    :ref:`CAN packet <knowledge-base-uds-addressing-packet>`.
    Later on, such object might be transmitted.
    Once a packet is transmitted, its historic data would be stored in
    :class:`~uds.can.packet.can_packet_record.CanPacketRecord`.
    """

    def __init__(self, *,
                 addressing_format: CanAddressingFormat,
                 packet_type: CanPacketType,
                 addressing_type: AddressingType,
                 can_id: Optional[int] = None,
                 target_address: Optional[int] = None,
                 source_address: Optional[int] = None,
                 address_extension: Optional[int] = None,
                 dlc: Optional[int] = None,
                 **packet_type_specific_kwargs: Any) -> None:
        """
        Create a storage for a single CAN packet.

        :param addressing_format: CAN Addressing Format used.
        :param packet_type: Type of this CAN packet.
        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            You do not have to provide it if other arguments unambiguously determine CAN ID value.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
            You do not have to provide it if `can_id` parameter unambiguously determine TARGET ADDRESS value.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Source Address parameter.
            You do not have to provide it if `can_id` parameter unambiguously determine SOURCE ADDRESS value.
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
        self.__raw_frame_data: bytes = b""  # Initialize empty value as it might be used by
        # set_addressing_information method. Teh final value will be set by set_packet_data.
        self.addressing_format = addressing_format
        self.set_addressing_information(addressing_type=addressing_type,
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

    @property
    def can_id(self) -> int:
        """CAN Identifier (CAN ID) of a CAN Frame that carries this CAN packet."""
        return self.__can_id

    @property
    def raw_frame_data(self) -> bytes:
        """Raw data bytes of a CAN frame that carries this CAN packet."""
        return self.__raw_frame_data

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing Format used by this CAN packet."""
        return self.__addressing_format

    @addressing_format.setter
    def addressing_format(self, value: CanAddressingFormat) -> None:
        """
        Set CAN Addressing Format used by this CAN packet.

        :param value: Value of CAN Addressing Format.

        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        try:
            getattr(self, "_CanPacket__addressing_format")
        except AttributeError:
            self.__addressing_format = CanAddressingFormat.validate_member(value)
        else:
            raise ReassignmentError("You cannot change value of 'addressing_format' attribute once it is assigned. "
                                    "Create a new object instead.")

    @property
    def addressing_type(self) -> AddressingType:
        """Addressing type for which this CAN packet is relevant."""
        return self.__addressing_type

    def set_addressing_information(self, *,
                                   addressing_type: AddressingType,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> None:
        """
        Change addressing information for this CAN packet.

        This function enables to change an entire :ref:`Network Address Information <knowledge-base-n-ai>`.

        :param addressing_type: Addressing type for which this CAN packet is relevant.
        :param can_id: CAN Identifier value that is used by this packet.
            You do not have to provide it if other arguments unambiguously determine CAN ID value.
        :param target_address: Target Address value carried by this CAN Packet.
            Leave None if provided `addressing_format` does not use Target Address parameter.
            You do not have to provide it if `can_id` parameter unambiguously determine TARGET ADDRESS value.
        :param source_address: Source Address value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Source Address parameter.
            You do not have to provide it if `can_id` parameter unambiguously determine SOURCE ADDRESS value.
        :param address_extension: Address Extension value carried by this CAN packet.
            Leave None if provided `addressing_format` does not use Address Extension parameter.
        """
        ai_params = CanAddressingInformation.validate_addressing_params(addressing_format=self.addressing_format,
                                                                        addressing_type=addressing_type,
                                                                        can_id=can_id,
                                                                        target_address=target_address,
                                                                        source_address=source_address,
                                                                        address_extension=address_extension)
        self.__can_id = ai_params["can_id"]
        self.__addressing_type = ai_params["addressing_type"]
        ai_data_bytes = CanAddressingInformation.encode_ai_data_bytes(addressing_format=self.addressing_format,
                                                                      target_address=ai_params["target_address"],
                                                                      address_extension=ai_params["address_extension"])
        self.__raw_frame_data = bytes(ai_data_bytes) + self.__raw_frame_data[len(ai_data_bytes):]

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

        :raise NotImplementedError: There is missing implementation for current CAN Packet Type.
        """
        CanPacketType.validate_member(packet_type)
        if packet_type == CanPacketType.SINGLE_FRAME:
            self.__raw_frame_data = bytes(create_single_frame_data(addressing_format=self.addressing_format,
                                                                   target_address=self.target_address,
                                                                   address_extension=self.address_extension,
                                                                   dlc=dlc,
                                                                   **packet_type_specific_kwargs))
        elif packet_type == CanPacketType.FIRST_FRAME:
            self.__raw_frame_data = bytes(create_first_frame_data(addressing_format=self.addressing_format,
                                                                  target_address=self.target_address,
                                                                  address_extension=self.address_extension,
                                                                  dlc=dlc,  # type: ignore
                                                                  **packet_type_specific_kwargs))
        elif packet_type == CanPacketType.CONSECUTIVE_FRAME:
            self.__raw_frame_data = bytes(create_consecutive_frame_data(addressing_format=self.addressing_format,
                                                                        target_address=self.target_address,
                                                                        address_extension=self.address_extension,
                                                                        dlc=dlc,
                                                                        **packet_type_specific_kwargs))
        elif packet_type == CanPacketType.FLOW_CONTROL:
            self.__raw_frame_data = bytes(create_flow_control_data(addressing_format=self.addressing_format,
                                                                   target_address=self.target_address,
                                                                   address_extension=self.address_extension,
                                                                   dlc=dlc,
                                                                   **packet_type_specific_kwargs))
        else:
            raise NotImplementedError("No handling for given CAN Packet Packet Type.")

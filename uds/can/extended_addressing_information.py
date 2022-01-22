"""Implementation of Extended Addressing Information handler."""

__all__ = ["ExtendedAddressingInformation"]

from copy import deepcopy

from uds.utilities import InconsistentArgumentsError, RawByte, validate_raw_byte
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .frame_fields import CanIdHandler
from .abstract_addressing_information import AbstractAddressingInformation


class ExtendedAddressingInformation(AbstractAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Extended Addressing format."""

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.EXTENDED_ADDRESSING

    @property
    def ai_data_bytes_number(self) -> int:
        """Get number of CAN Frame data bytes that are used to carry Addressing Information."""
        return 1

    @property
    def rx_packets_physical_ai(self) -> AbstractAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of incoming physically addressed CAN packets."""
        return deepcopy(self.__rx_packets_physical_ai)

    @rx_packets_physical_ai.setter
    def rx_packets_physical_ai(self, value: AbstractAddressingInformation.InputAIParamsAlias):
        """
        Set Addressing Information parameters of incoming physically addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL}, **value)  # type: ignore
        self.__rx_packets_physical_ai: AbstractAddressingInformation.PacketAIParamsAlias = {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,  # type: ignore
            self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            **value
        }

    @property
    def tx_packets_physical_ai(self) -> AbstractAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of outgoing physically addressed CAN packets."""
        return deepcopy(self.__tx_packets_physical_ai)

    @tx_packets_physical_ai.setter
    def tx_packets_physical_ai(self, value: AbstractAddressingInformation.InputAIParamsAlias):
        """
        Set Addressing Information parameters of outgoing physically addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL}, **value)  # type: ignore
        self.__tx_packets_physical_ai: AbstractAddressingInformation.PacketAIParamsAlias = {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,  # type: ignore
            self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            **value
        }

    @property
    def rx_packets_functional_ai(self) -> AbstractAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of incoming functionally addressed CAN packets."""
        return deepcopy(self.__rx_packets_functional_ai)

    @rx_packets_functional_ai.setter
    def rx_packets_functional_ai(self, value: AbstractAddressingInformation.InputAIParamsAlias):
        """
        Set Addressing Information parameters of incoming functionally addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL}, **value)  # type: ignore
        self.__rx_packets_functional_ai: AbstractAddressingInformation.PacketAIParamsAlias = {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,  # type: ignore
            self.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
            **value
        }

    @property
    def tx_packets_functional_ai(self) -> AbstractAddressingInformation.PacketAIParamsAlias:
        """Addressing Information parameters of outgoing functionally addressed CAN packets."""
        return deepcopy(self.__tx_packets_functional_ai)

    @tx_packets_functional_ai.setter
    def tx_packets_functional_ai(self, value: AbstractAddressingInformation.InputAIParamsAlias):
        """
        Set Addressing Information parameters of outgoing functionally addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL}, **value)  # type: ignore
        self.__tx_packets_functional_ai: AbstractAddressingInformation.PacketAIParamsAlias = {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,  # type: ignore
            self.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL,
            **value
        }

    @staticmethod
    def validate_packet_ai(addressing_type: AddressingTypeAlias, can_id: int, target_address: RawByte) -> None:
        """
        Validate Addressing Information parameters of a CAN packet that uses Extended CAN Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Extended Addressing format.
        """
        AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)
        validate_raw_byte(target_address)
        if not CanIdHandler.is_extended_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Extended Addressing Format. Actual value: {can_id}")

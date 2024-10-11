"""Implementation of Extended Addressing Information handler."""

__all__ = ["ExtendedCanAddressingInformation"]

from typing import Optional

from uds.transmission_attributes import AddressingType
from uds.utilities import InconsistentArgumentsError, UnusedArgumentError, validate_raw_byte

from .abstract_addressing_information import AbstractCanAddressingInformation, PacketAIParamsAlias
from .addressing_format import CanAddressingFormat
from .frame_fields import CanIdHandler


class ExtendedCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Extended Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 1
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""
        return CanAddressingFormat.EXTENDED_ADDRESSING

    @classmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingType,
                           can_id: Optional[int] = None,
                           target_address: Optional[int] = None,
                           source_address: Optional[int] = None,
                           address_extension: Optional[int] = None) -> PacketAIParamsAlias:
        """
        Validate Addressing Information parameters of a CAN packet that uses Extended Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided CAN ID value is incompatible with Extended Addressing format.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if (source_address, address_extension) != (None, None):
            raise UnusedArgumentError("Values of Source Address and Address Extension are not supported by "
                                      "Extended Addressing format and all must be None.")
        addressing_type = AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)  # type: ignore
        validate_raw_byte(target_address)  # type: ignore
        if not CanIdHandler.is_extended_addressed_can_id(can_id):  # type: ignore
            raise InconsistentArgumentsError("Provided value of CAN ID is not compatible with "
                                             "Extended Addressing Format.")
        return PacketAIParamsAlias(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                   addressing_type=addressing_type,
                                   can_id=can_id,  # type: ignore
                                   target_address=target_address,
                                   source_address=source_address,
                                   address_extension=address_extension)

    @staticmethod
    def _validate_node_ai(rx_packets_physical_ai: PacketAIParamsAlias,
                          tx_packets_physical_ai: PacketAIParamsAlias,
                          rx_packets_functional_ai: PacketAIParamsAlias,
                          tx_packets_functional_ai: PacketAIParamsAlias) -> None:
        """
        Validate Node Addressing Information parameters.

        :param rx_packets_physical_ai: Addressing Information parameters of incoming physically addressed
            CAN packets to validate.
        :param tx_packets_physical_ai: Addressing Information parameters of outgoing physically addressed
            CAN packets to validate.
        :param rx_packets_functional_ai: Addressing Information parameters of incoming functionally addressed
            CAN packets to validate.
        :param tx_packets_functional_ai: Addressing Information parameters of outgoing functionally addressed
            CAN packets to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other.
        """
        if len({(rx_packets_physical_ai["can_id"], rx_packets_physical_ai["target_address"]),
                (tx_packets_physical_ai["can_id"], tx_packets_physical_ai["target_address"]),
                (rx_packets_functional_ai["can_id"], rx_packets_functional_ai["target_address"]),
                (tx_packets_functional_ai["can_id"], tx_packets_functional_ai["target_address"])}) != 4:
            raise InconsistentArgumentsError("Combination of CAN ID and Target Address for incoming and outgoing "
                                             "CAN packets must be unique")

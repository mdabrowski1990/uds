"""Implementation of Extended Addressing Information handler."""

__all__ = ["ExtendedCanAddressingInformation"]

from typing import Optional

from uds.addressing import AddressingType
from uds.utilities import InconsistentArgumentsError, UnusedArgumentError, validate_raw_byte

from uds.can.addressing.abstract_addressing_information import AbstractCanAddressingInformation, CANAddressingParams
from uds.can.addressing.addressing_format import CanAddressingFormat
from uds.can.frame import CanIdHandler


class ExtendedCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Extended Addressing format."""

    ai_data_bytes_number: int = 1
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
                           address_extension: Optional[int] = None) -> CANAddressingParams:
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
        AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)  # type: ignore
        validate_raw_byte(target_address)  # type: ignore
        if not CanIdHandler.is_extended_addressed_can_id(can_id):  # type: ignore
            raise InconsistentArgumentsError("Provided value of CAN ID is incompatible with "
                                             "Extended Addressing Format.")
        return CANAddressingParams(addressing_format=CanAddressingFormat.EXTENDED_ADDRESSING,
                                   addressing_type=addressing_type,
                                   can_id=can_id,  # type: ignore
                                   target_address=target_address,
                                   source_address=source_address,
                                   address_extension=address_extension)

    @staticmethod
    def _validate_node_ai(rx_packets_physical_ai: CANAddressingParams,
                          tx_packets_physical_ai: CANAddressingParams,
                          rx_packets_functional_ai: CANAddressingParams,
                          tx_packets_functional_ai: CANAddressingParams) -> None:
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
        rx_ai_params = {
            (rx_packets_physical_ai["can_id"], rx_packets_physical_ai["target_address"]),
            (rx_packets_functional_ai["can_id"], rx_packets_functional_ai["target_address"])
        }
        tx_ai_params = {
            (tx_packets_physical_ai["can_id"], tx_packets_physical_ai["target_address"]),
            (tx_packets_functional_ai["can_id"], tx_packets_functional_ai["target_address"])
        }
        if ((rx_packets_physical_ai["can_id"], rx_packets_physical_ai["target_address"]) in tx_ai_params
                or (rx_packets_functional_ai["can_id"], rx_packets_functional_ai["target_address"]) in tx_ai_params
                or (tx_packets_physical_ai["can_id"], tx_packets_physical_ai["target_address"]) in rx_ai_params
                or (tx_packets_functional_ai["can_id"], tx_packets_functional_ai["target_address"]) in rx_ai_params):
            raise InconsistentArgumentsError("The same combination of CAN ID and Target Address cannot be used for "
                                             "incoming and outgoing communication.")

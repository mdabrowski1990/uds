"""Implementation of Extended Addressing Information handler."""

__all__ = ["ExtendedCanAddressingInformation"]

from typing import Optional

from uds.utilities import InconsistentArgumentsError, UnusedArgumentError, RawByte, validate_raw_byte
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .frame_fields import CanIdHandler
from .abstract_addressing_information import AbstractCanAddressingInformation


class ExtendedCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Extended Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 1
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.EXTENDED_ADDRESSING

    @classmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingTypeAlias,
                           can_id: Optional[int] = None,
                           target_address: Optional[RawByte] = None,
                           source_address: Optional[RawByte] = None,
                           address_extension: Optional[RawByte] = None
                           ) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
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
        CanIdHandler.validate_can_id(can_id)
        validate_raw_byte(target_address)
        if not CanIdHandler.is_extended_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Extended Addressing Format. Actual value: {can_id}")
        return {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.EXTENDED_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: addressing_type,
            AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: target_address,
        }

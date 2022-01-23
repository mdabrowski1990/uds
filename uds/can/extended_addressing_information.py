"""Implementation of Extended Addressing Information handler."""

__all__ = ["ExtendedAddressingInformation"]

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

    @staticmethod
    def validate_packet_ai(addressing_type: AddressingTypeAlias,  # noqa
                           can_id: int,
                           target_address: RawByte) -> None:
        """
        Validate Addressing Information parameters of a CAN packet that uses Extended Addressing format.

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

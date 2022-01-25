"""Implementation of Mixed Addressing Information handlers."""

__all__ = ["Mixed11BitCanAddressingInformation", "Mixed29BitCanAddressingInformation"]

from typing import Optional

from uds.utilities import InconsistentArgumentsError, RawByte, validate_raw_byte
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .frame_fields import CanIdHandler
from .abstract_addressing_information import AbstractCanAddressingInformation


class Mixed11BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Mixed 11-bit Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 1
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.MIXED_11BIT_ADDRESSING

    @staticmethod
    def validate_packet_ai(addressing_type: AddressingTypeAlias,  # TODO: rework
                           can_id: int,
                           address_extension: RawByte) -> None:
        """
        Validate Addressing Information parameters of a CAN packet that uses Mixed 11-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Mixed 11-bit Addressing format.
        """
        AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)
        validate_raw_byte(address_extension)
        if not CanIdHandler.is_mixed_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Mixed 11-bit Addressing Format. Actual value: {can_id}")


class Mixed29BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Mixed 29-bit Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 1
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.MIXED_29BIT_ADDRESSING

    @staticmethod
    def validate_packet_ai(addressing_type: AddressingTypeAlias,  # TODO: rework
                           address_extension: RawByte,
                           can_id: Optional[int] = None,
                           target_address: Optional[RawByte] = None,
                           source_address: Optional[RawByte] = None) -> None:
        """
        Validate Addressing Information parameters of a CAN packet that uses Mixed 29-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param address_extension: Address Extension value to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Mixed 29-bit Addressing format.
        """
        AddressingType.validate_member(addressing_type)
        validate_raw_byte(address_extension)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Mixed 29-bit Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
            decoded_info = CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id)
            if addressing_type != decoded_info[CanIdHandler.ADDRESSING_TYPE_NAME]:  # type: ignore
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                                 f"Actual values: can_id={can_id}, addressing={addressing_type}")
            if target_address not in (decoded_info[CanIdHandler.TARGET_ADDRESS_NAME], None):  # type: ignore
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                                 f"Actual values: can_id={can_id}, target_address={target_address}")
            if source_address not in (decoded_info[CanIdHandler.SOURCE_ADDRESS_NAME], None):  # type: ignore
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                                 f"Actual values: can_id={can_id}, source_address={source_address}")

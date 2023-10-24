"""Implementation of Mixed Addressing Information handlers."""

__all__ = ["Mixed11BitCanAddressingInformation", "Mixed29BitCanAddressingInformation"]

from typing import Optional

from uds.utilities import InconsistentArgumentsError, UnusedArgumentError, validate_raw_byte
from uds.transmission_attributes import AddressingType
from .addressing_format import CanAddressingFormat
from .frame_fields import CanIdHandler
from .abstract_addressing_information import AbstractCanAddressingInformation, PacketAIParamsAlias


class Mixed11BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Mixed 11-bit Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 1
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""
        return CanAddressingFormat.MIXED_11BIT_ADDRESSING

    @classmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingType,
                           can_id: Optional[int] = None,
                           target_address: Optional[int] = None,
                           source_address: Optional[int] = None,
                           address_extension: Optional[int] = None) -> PacketAIParamsAlias:
        """
        Validate Addressing Information parameters of a CAN packet that uses Mixed 11-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided CAN ID value is incompatible with Mixed 11-bit Addressing format.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if (target_address, source_address) != (None, None):
            raise UnusedArgumentError("Values of Target Address and Source Address are not supported by "
                                      "Mixed 11-bit Addressing format and all must be None.")
        AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)  # type: ignore
        validate_raw_byte(address_extension)  # type: ignore
        if not CanIdHandler.is_mixed_11bit_addressed_can_id(can_id):  # type: ignore
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Mixed 11-bit Addressing Format. Actual value: {can_id}")
        return PacketAIParamsAlias(addressing_format=CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                   addressing_type=addressing_type,
                                   can_id=can_id,  # type: ignore
                                   target_address=target_address,
                                   source_address=source_address,
                                   address_extension=address_extension)


class Mixed29BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Mixed 29-bit Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 1
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""
        return CanAddressingFormat.MIXED_29BIT_ADDRESSING

    @classmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingType,
                           can_id: Optional[int] = None,
                           target_address: Optional[int] = None,
                           source_address: Optional[int] = None,
                           address_extension: Optional[int] = None) -> PacketAIParamsAlias:
        """
        Validate Addressing Information parameters of a CAN packet that uses Mixed 29-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided Target Address, Source Address or CAN ID values are incompatible
            with each other or Mixed 29-bit Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        addressing_type = AddressingType.validate_member(addressing_type)
        validate_raw_byte(address_extension)  # type: ignore
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Mixed 29-bit Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)  # type: ignore
            validate_raw_byte(source_address)  # type: ignore
            encoded_can_id = CanIdHandler.encode_mixed_addressed_29bit_can_id(
                addressing_type=addressing_type,
                target_address=target_address,  # type: ignore
                source_address=source_address)  # type: ignore
            return PacketAIParamsAlias(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                       addressing_type=addressing_type,
                                       can_id=encoded_can_id,
                                       target_address=target_address,
                                       source_address=source_address,
                                       address_extension=address_extension)
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
        return PacketAIParamsAlias(addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                   addressing_type=addressing_type,
                                   can_id=can_id,
                                   target_address=decoded_info[CanIdHandler.TARGET_ADDRESS_NAME],  # type: ignore
                                   source_address=decoded_info[CanIdHandler.SOURCE_ADDRESS_NAME],  # type: ignore
                                   address_extension=address_extension)

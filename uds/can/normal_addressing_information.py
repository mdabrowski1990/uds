"""Implementation of Normal Addressing Information handlers."""

__all__ = ["Normal11BitCanAddressingInformation", "NormalFixedCanAddressingInformation"]

from typing import Optional

from uds.utilities import InconsistentArgumentsError, UnusedArgumentError, RawByte, validate_raw_byte
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .frame_fields import CanIdHandler
from .abstract_addressing_information import AbstractCanAddressingInformation


class Normal11BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Normal 11-bit Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 0
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.NORMAL_11BIT_ADDRESSING

    @classmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingTypeAlias,
                           can_id: Optional[int] = None,
                           target_address: Optional[RawByte] = None,
                           source_address: Optional[RawByte] = None,
                           address_extension: Optional[RawByte] = None
                           ) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
        """
        Validate Addressing Information parameters of a CAN packet that uses Normal 11-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided CAN ID value is incompatible with Normal 11-bit Addressing format.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if (target_address, source_address, address_extension) != (None, None, None):
            raise UnusedArgumentError("Values of Target Address, Source Address and Address Extension are "
                                      "not supported by Normal 11-bit Addressing format and all must be None.")
        AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_normal_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Normal 11-bit Addressing Format. Actual value: {can_id}")
        return {
            cls.ADDRESSING_FORMAT_NAME: CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
            cls.ADDRESSING_TYPE_NAME: addressing_type,
            cls.CAN_ID_NAME: can_id
        }


class NormalFixedCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Normal Fixed Addressing format."""

    AI_DATA_BYTES_NUMBER: int = 0
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.NORMAL_FIXED_ADDRESSING

    @classmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingTypeAlias,
                           can_id: Optional[int] = None,
                           target_address: Optional[RawByte] = None,
                           source_address: Optional[RawByte] = None,
                           address_extension: Optional[RawByte] = None
                           ) -> AbstractCanAddressingInformation.PacketAIParamsAlias:
        """
        Validate Addressing Information parameters of a CAN packet that uses Normal Fixed Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided Target Address, Source Address or CAN ID values are incompatible
            with each other or Normal Fixed Addressing format.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if address_extension is not None:
            raise UnusedArgumentError("Values of TAddress Extension is not supported by Normal Fixed Addressing format "
                                      "and all must be None.")
        AddressingType.validate_member(addressing_type)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Normal Fixed Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
            encoded_can_id = CanIdHandler.encode_normal_fixed_addressed_can_id(addressing_type=addressing_type,
                                                                               target_address=target_address,
                                                                               source_address=source_address)
            return {
                AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: addressing_type,
                AbstractCanAddressingInformation.CAN_ID_NAME: encoded_can_id,
                AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: target_address,
                AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: source_address,
            }
        decoded_info = CanIdHandler.decode_normal_fixed_addressed_can_id(can_id)
        if addressing_type != decoded_info[CanIdHandler.ADDRESSING_TYPE_NAME]:
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                             f"Actual values: can_id={can_id}, addressing={addressing_type}")
        if target_address not in (decoded_info[CanIdHandler.TARGET_ADDRESS_NAME], None):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                             f"Actual values: can_id={can_id}, target_address={target_address}")
        if source_address not in (decoded_info[CanIdHandler.SOURCE_ADDRESS_NAME], None):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                             f"Actual values: can_id={can_id}, source_address={source_address}")
        return {
            AbstractCanAddressingInformation.ADDRESSING_FORMAT_NAME: CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
            AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME: addressing_type,
            AbstractCanAddressingInformation.CAN_ID_NAME: can_id,
            AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: decoded_info[CanIdHandler.TARGET_ADDRESS_NAME],
            AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME: decoded_info[CanIdHandler.SOURCE_ADDRESS_NAME],
        }

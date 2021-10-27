"""CAN Addressing Formats definitions."""

__all__ = ["CanAddressingFormat", "CanAddressingFormatAlias"]

from typing import Union, Optional

from aenum import StrEnum, unique

from uds.transmission_attributes import AddressingType, AddressingTypeMemberAlias
from uds.utilities import validate_raw_byte, RawByte, ValidatedEnum, UnusedArgumentError, InconsistentArgumentsError
from .can_frame_fields import CanIdHandler


@unique
class CanAddressingFormat(StrEnum, ValidatedEnum):
    """
    Definition of CAN addressing formats.

    :ref:`CAN addressing formats <knowledge-base-can-addressing>` determines how
    :ref:`Network Address Information (N_AI) <knowledge-base-n-ai>` is provided in a CAN packet.
    """

    NORMAL_11BIT_ADDRESSING = "Normal 11-bit Addressing"
    """:ref:`Normal addressing <knowledge-base-can-normal-addressing>` that uses 11-bit CAN Identifiers."""
    NORMAL_FIXED_ADDRESSING = "Normal Fixed Addressing"
    """:ref:`Normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` format.
    It uses 29-bit CAN Identifiers only."""
    EXTENDED_ADDRESSING = "Extended Addressing"
    """:ref:`Extended addressing <knowledge-base-can-extended-addressing>` format that uses either 11-bit or 29-bit
    CAN Identifiers."""
    MIXED_11BIT_ADDRESSING = "Mixed 11-bit Addressing"
    """:ref:`Mixed addressing with 11-bit CAN ID <knowledge-base-can-mixed-11-bit-addressing>`. It is a subformat
    of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 11-bit CAN Identifiers."""
    MIXED_29BIT_ADDRESSING = "Mixed 29-bit Addressing"
    """:ref:`Mixed addressing with 29-bit CAN ID <knowledge-base-can-mixed-29-bit-addressing>`. It is a subformat
    of :ref:`mixed addressing <knowledge-base-can-mixed-addressing>` that uses 29-bit CAN Identifiers."""

    @classmethod
    def get_number_of_data_bytes_used(cls, addressing_format: "CanAddressingFormatAlias") -> int:
        """
        Get number of data bytes that are used by CAN Addressing Format.

        :param addressing_format: CAN Addressing Format for which value to be provided.

        :return: Number of data bytes in a CAN Packet that are used to carry Addressing Information for provided
            CAN Addressing Format.
        """
        cls.validate_member(addressing_format)
        return {cls.NORMAL_11BIT_ADDRESSING: 0,
                cls.NORMAL_FIXED_ADDRESSING: 0,
                cls.EXTENDED_ADDRESSING: 1,
                cls.MIXED_11BIT_ADDRESSING: 1,
                cls.MIXED_29BIT_ADDRESSING: 1}[cls(addressing_format)]

    @classmethod
    def validate_ai(cls,
                    addressing_format: "CanAddressingFormatAlias",
                    addressing: AddressingTypeMemberAlias,
                    can_id: Optional[int] = None,
                    target_address: Optional[RawByte] = None,
                    source_address: Optional[RawByte] = None,
                    address_extension: Optional[RawByte] = None) -> None:
        """
        Validate Addressing Information.

        This methods performs comprehensive check of :ref:`Network Addressing Information (N_AI) <knowledge-base-n-ai>`
        to make sure that every required argument is provided and their values are consistent with
        :ref:`CAN Addressing Format <knowledge-base-can-addressing>`.

        :param addressing_format: CAN addressing format value to validate.
        :param addressing: Addressing type value to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: Value for at least one unused argument (not relevant for this can addressing format)
            was provided.
        :raise NotImplementedError: A valid packet type was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.
        """
        CanAddressingFormat.validate_member(addressing_format)
        addressing_format_instance = CanAddressingFormat.__call__(addressing_format)
        if addressing_format_instance == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            if (target_address, source_address, address_extension) != (None, None, None):
                raise UnusedArgumentError(f"Values of Target Address, Source Address and Address Extension must not be "
                                          f"provided for {addressing_format_instance}. Actual values: "
                                          f"target_address={target_address}, source_address={source_address}, "
                                          f"address_extension={address_extension}")
            cls.validate_ai_normal_11bit(addressing=addressing,
                                         can_id=can_id)
        elif addressing_format_instance == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            if address_extension is not None:
                raise UnusedArgumentError(f"Value of Address Extension must not be provided for "
                                          f"{addressing_format_instance}. Actual value: "
                                          f"address_extension={address_extension}")
            cls.validate_ai_normal_fixed(addressing=addressing,
                                         can_id=can_id,
                                         target_address=target_address,
                                         source_address=source_address)
        elif addressing_format_instance == CanAddressingFormat.EXTENDED_ADDRESSING:
            if (source_address, address_extension) != (None, None):
                raise UnusedArgumentError(f"Values of Source Address and Address Extension must not be provided for "
                                          f"{addressing_format_instance}. Actual values: "
                                          f"source_address={source_address}, address_extension={address_extension}")
            cls.validate_ai_extended(addressing=addressing,
                                     can_id=can_id,
                                     target_address=target_address)
        elif addressing_format_instance == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            if (target_address, source_address) != (None, None):
                raise UnusedArgumentError(f"Values of Target Address and Source Address must not be provided for "
                                          f"{addressing_format_instance}. Actual values: "
                                          f"target_address={target_address}, source_address={source_address}")
            cls.validate_ai_mixed_11bit(addressing=addressing,
                                        can_id=can_id,
                                        address_extension=address_extension)
        elif addressing_format_instance == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            cls.validate_ai_mixed_29bit(addressing=addressing,
                                        can_id=can_id,
                                        target_address=target_address,
                                        source_address=source_address,
                                        address_extension=address_extension)
        else:
            raise NotImplementedError(f"Missing implementation for: {addressing_format_instance}")

    @staticmethod
    def validate_ai_normal_11bit(addressing: AddressingTypeMemberAlias,
                                 can_id: int) -> None:
        """
        Validate Addressing Information in Normal 11-bit Addressing format.

        :param addressing: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        AddressingType.validate_member(addressing)
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_normal_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Normal 11-bit Addressing Format. Actual value: {can_id}")

    @staticmethod
    def validate_ai_normal_fixed(addressing: AddressingTypeMemberAlias,
                                 can_id: Optional[int] = None,
                                 target_address: Optional[RawByte] = None,
                                 source_address: Optional[RawByte] = None) -> None:
        """
        Validate consistency of Address Information arguments when Normal Fixed Addressing Format is used.

        :param addressing: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        AddressingType.validate_member(addressing)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Normal Fixed Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
            decoded_addressing, decoded_target_address, decoded_source_address = \
                CanIdHandler.decode_normal_fixed_addressed_can_id(can_id)
            if AddressingType(addressing) != decoded_addressing:
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                                 f"Actual values: can_id={can_id}, addressing={addressing}")
            if target_address not in (decoded_target_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                                 f"Actual values: can_id={can_id}, target_address={target_address}")
            if source_address not in (decoded_source_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                                 f"Actual values: can_id={can_id}, source_address={source_address}")

    @staticmethod
    def validate_ai_extended(addressing: AddressingTypeMemberAlias,
                             can_id: int,
                             target_address: RawByte) -> None:
        """
        Validate consistency of Address Information arguments when Extended Addressing Format is used.

        :param addressing: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        AddressingType.validate_member(addressing)
        CanIdHandler.validate_can_id(can_id)
        validate_raw_byte(target_address)
        if not CanIdHandler.is_extended_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Extended Addressing Format. Actual value: {can_id}")

    @staticmethod
    def validate_ai_mixed_11bit(addressing: AddressingTypeMemberAlias,
                                can_id: int,
                                address_extension: RawByte) -> None:
        """
        Validate consistency of Address Information arguments when Mixed 11-bit Addressing Format is used.

        :param addressing: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        AddressingType.validate_member(addressing)
        CanIdHandler.validate_can_id(can_id)
        validate_raw_byte(address_extension)
        if not CanIdHandler.is_mixed_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Mixed 11-bit Addressing Format. Actual value: {can_id}")

    @staticmethod
    def validate_ai_mixed_29bit(addressing: AddressingTypeMemberAlias,
                                can_id: Optional[int],
                                target_address: Optional[RawByte],
                                source_address: Optional[RawByte],
                                address_extension: RawByte) -> None:
        """
        Validate consistency of Address Information arguments when Mixed 29-bit Addressing Format is used.

        :param addressing: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together).
        """
        AddressingType.validate_member(addressing)
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
            decoded_addressing, decoded_target_address, decoded_source_address = \
                CanIdHandler.decode_mixed_addressed_29bit_can_id(can_id)
            if AddressingType(addressing) != decoded_addressing:
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                                 f"Actual values: can_id={can_id}, addressing={addressing}")
            if target_address not in (decoded_target_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                                 f"Actual values: can_id={can_id}, target_address={target_address}")
            if source_address not in (decoded_source_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                                 f"Actual values: can_id={can_id}, source_address={source_address}")


CanAddressingFormatAlias = Union[CanAddressingFormat, str]
"""Alias that describes :class:`~uds.can.addressing_format.CanAddressingFormat` member."""


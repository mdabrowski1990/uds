"""
Implementation of CAN Addressing Information.

This module contains helper class and methods for managing CAN :ref:`Addressing Information <knowledge-base-n-ai>`.
"""

__all__ = ["CanAddressingInformationHandler"]

from typing import Optional

from uds.utilities import RawByte, validate_raw_byte, InconsistentArgumentsError, UnusedArgumentError
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .can_frame_fields import CanIdHandler
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias


class CanAddressingInformationHandler:
    """
    Helper class that provides utilities for CAN Addressing Information.

    CAN :ref:`Addressing Information <knowledge-base-n-ai>` depends on
    """

    @classmethod
    def get_data_bytes_used_for_ai(cls, addressing_format: CanAddressingFormatAlias) -> int:
        """
        Get number of data bytes that are used to carry Addressing Information.

        Depending on addressing

        :param addressing_format: CAN Addressing Format for which value to be provided.

        :return: Number of data bytes in a CAN Packet that are used to carry Addressing Information for provided
            CAN Addressing Format.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return {CanAddressingFormat.NORMAL_11BIT_ADDRESSING: 0,
                CanAddressingFormat.NORMAL_FIXED_ADDRESSING: 0,
                CanAddressingFormat.EXTENDED_ADDRESSING: 1,
                CanAddressingFormat.MIXED_11BIT_ADDRESSING: 1,
                CanAddressingFormat.MIXED_29BIT_ADDRESSING: 1}[addressing_format]

    @classmethod
    def validate_ai(cls,
                    addressing_format: CanAddressingFormatAlias,
                    addressing: AddressingTypeAlias,
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
        if addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            if (target_address, source_address, address_extension) != (None, None, None):
                raise UnusedArgumentError(f"Values of Target Address, Source Address and Address Extension must not be "
                                          f"provided for {addressing_format}. Actual values: "
                                          f"target_address={target_address}, source_address={source_address}, "
                                          f"address_extension={address_extension}")
            cls.validate_ai_normal_11bit(addressing=addressing,
                                         can_id=can_id)
        elif addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            if address_extension is not None:
                raise UnusedArgumentError(f"Value of Address Extension must not be provided for "
                                          f"{addressing_format}. Actual value: "
                                          f"address_extension={address_extension}")
            cls.validate_ai_normal_fixed(addressing=addressing,
                                         can_id=can_id,
                                         target_address=target_address,
                                         source_address=source_address)
        elif addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            if (source_address, address_extension) != (None, None):
                raise UnusedArgumentError(f"Values of Source Address and Address Extension must not be provided for "
                                          f"{addressing_format}. Actual values: "
                                          f"source_address={source_address}, address_extension={address_extension}")
            cls.validate_ai_extended(addressing=addressing,
                                     can_id=can_id,
                                     target_address=target_address)
        elif addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            if (target_address, source_address) != (None, None):
                raise UnusedArgumentError(f"Values of Target Address and Source Address must not be provided for "
                                          f"{addressing_format}. Actual values: "
                                          f"target_address={target_address}, source_address={source_address}")
            cls.validate_ai_mixed_11bit(addressing=addressing,
                                        can_id=can_id,
                                        address_extension=address_extension)
        elif addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            cls.validate_ai_mixed_29bit(addressing=addressing,
                                        can_id=can_id,
                                        target_address=target_address,
                                        source_address=source_address,
                                        address_extension=address_extension)
        else:
            raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @staticmethod
    def validate_ai_normal_11bit(addressing: AddressingTypeAlias,
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
    def validate_ai_normal_fixed(addressing: AddressingTypeAlias,
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
            if addressing != decoded_addressing:
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                                 f"Actual values: can_id={can_id}, addressing={addressing}")
            if target_address not in (decoded_target_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                                 f"Actual values: can_id={can_id}, target_address={target_address}")
            if source_address not in (decoded_source_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                                 f"Actual values: can_id={can_id}, source_address={source_address}")

    @staticmethod
    def validate_ai_extended(addressing: AddressingTypeAlias,
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
    def validate_ai_mixed_11bit(addressing: AddressingTypeAlias,
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
    def validate_ai_mixed_29bit(addressing: AddressingTypeAlias,
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
            if addressing != decoded_addressing:
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                                 f"Actual values: can_id={can_id}, addressing={addressing}")
            if target_address not in (decoded_target_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                                 f"Actual values: can_id={can_id}, target_address={target_address}")
            if source_address not in (decoded_source_address, None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                                 f"Actual values: can_id={can_id}, source_address={source_address}")

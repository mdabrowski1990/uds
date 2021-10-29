"""
Implementation of CAN Addressing Information.

This module contains helper class and methods for managing CAN :ref:`Addressing Information <knowledge-base-n-ai>`.
"""

__all__ = ["CanAddressingInformationHandler"]

from typing import Optional, Union, Dict

from uds.utilities import RawByte, RawBytes, RawBytesList, validate_raw_byte, validate_raw_bytes, \
    InconsistentArgumentsError, UnusedArgumentError
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .can_frame_fields import CanIdHandler
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias

AIDataBytesInfoAlias = Dict[str, Optional[RawByte]]
"""Typing alias of Addressing Information carried by Data bytes."""
AIInfoAlias = Dict[str, Optional[Union[RawByte, AddressingType]]]
"""Typing alias of Addressing Information carried by Data bytes."""


class CanAddressingInformationHandler:
    """
    Helper class that provides utilities for CAN Addressing Information.

    CAN :ref:`Addressing Information <knowledge-base-n-ai>` depends on
    """

    ADDRESSING_TYPE_NAME = "addressing"
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` key that is used as in dictionary with 
    decoded Addressing Information."""
    TARGET_ADDRESS_NAME = "target_address"
    """Name of Target Address key that is used as in dictionary with decoded Addressing Information."""
    SOURCE_ADDRESS_NAME = "source_address"
    """Name of Source Address key that is used as in dictionary with decoded Addressing Information."""
    ADDRESS_EXTENSION_NAME = "address_extension"
    """Name of Address Extension key that is used as in dictionary with decoded Addressing Information."""

    @classmethod
    def decode_ai(cls,
                  addressing_format: CanAddressingFormatAlias,
                  can_id: int,
                  ai_data_bytes: RawBytes) -> AIInfoAlias:
        """
        Decode Addressing Information from CAN ID and data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param can_id: Value of CAN Identifier.
        :param ai_data_bytes: Data bytes containing Addressing Information.

        :return: Dictionary with Addressing Information decoded out of CAN ID and Addressing Information data bytes.
        """
        from_data_bytes = cls.decode_ai_data_bytes(addressing_format=addressing_format, ai_data_bytes=ai_data_bytes)
        from_can_id = CanIdHandler.decode_can_id(addressing_format=addressing_format, can_id=can_id)
        names = (cls.ADDRESSING_TYPE_NAME, cls.TARGET_ADDRESS_NAME, cls.SOURCE_ADDRESS_NAME, cls.ADDRESS_EXTENSION_NAME)
        return {name: from_data_bytes.get(name, None) or from_can_id.get(name, None) for name in names}

    @classmethod
    def get_ai_data_bytes_number(cls, addressing_format: CanAddressingFormatAlias) -> int:
        """
        Get number of data bytes that are used to carry Addressing Information.

        Depending on addressing

        :param addressing_format: CAN Addressing Format for which the value to be provided.

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
    def generate_ai_data_bytes(cls,
                               addressing_format: CanAddressingFormatAlias,
                               target_address: Optional[RawByte] = None,
                               address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Generate a list of data bytes that carry Addressing Information.

        .. note:: The number of bytes and their values depends on
            :ref:`CAN Addressing Format <knowledge-base-can-addressing>` used.

        :param addressing_format: CAN Addressing Format for which the value to be generated.
        :param target_address: Target Address value used.
        :param address_extension: Source Address value used.

        :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: List of data bytes that carry Addressing Information in CAN frame Data field.
        """
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format in (CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                 CanAddressingFormat.NORMAL_FIXED_ADDRESSING):
            return []
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            validate_raw_byte(target_address)
            return [target_address]
        if addressing_format in (CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 CanAddressingFormat.MIXED_29BIT_ADDRESSING):
            validate_raw_byte(address_extension)
            return [address_extension]
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @classmethod
    def decode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormatAlias,
                             ai_data_bytes: RawBytes) -> AIDataBytesInfoAlias:
        """
        Decode Addressing Information from data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes containing Addressing Information.

        :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
            Please raise an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            whenever you see this error.

        :return: Dictionary with Target Address and Address Extension values decoded out of Addressing Information
            data bytes.
        """
        cls.validate_ai_data_bytes(addressing_format=addressing_format,
                                   ai_data_bytes=ai_data_bytes)
        if addressing_format in {CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                 CanAddressingFormat.NORMAL_FIXED_ADDRESSING}:
            return {cls.TARGET_ADDRESS_NAME: None,
                    cls.ADDRESS_EXTENSION_NAME: None}
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            return {cls.TARGET_ADDRESS_NAME: ai_data_bytes[0],
                    cls.ADDRESS_EXTENSION_NAME: None}
        if addressing_format in {CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 CanAddressingFormat.MIXED_29BIT_ADDRESSING}:
            return {cls.TARGET_ADDRESS_NAME: None,
                    cls.ADDRESS_EXTENSION_NAME:  ai_data_bytes[0]}
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

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
        :raise NotImplementedError: A valid addressing format was provided, but the implementation for it is missing.
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

    @classmethod
    def validate_ai_data_bytes(cls, addressing_format: CanAddressingFormatAlias, ai_data_bytes: RawBytes) -> None:
        """
        Validate Addressing Information data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes containing Addressing Information.

        :raise InconsistentArgumentsError: Provided number of Addressing Information data bytes does not match
            Addressing Format used.
        """
        CanAddressingFormat.validate_member(addressing_format)
        validate_raw_bytes(ai_data_bytes, allow_empty=True)
        expected_ai_bytes_number = cls.get_ai_data_bytes_number(addressing_format)
        if expected_ai_bytes_number != len(ai_data_bytes):
            raise InconsistentArgumentsError(f"Number of Addressing Information data bytes does not match provided "
                                             f"Addressing Format. Expected number of AI data bytes: "
                                             f"{expected_ai_bytes_number}. Actual value: {ai_data_bytes}")

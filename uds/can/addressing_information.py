"""
Implementation of CAN Addressing Information.

This module contains helper class for managing :ref:`Addressing Information <knowledge-base-n-ai>` on CAN bus.
"""

__all__ = ["CanAddressingInformationHandler", "AIDataBytesAlias", "AIAlias"]

from typing import Optional, Union, Dict

from uds.utilities import RawByte, RawBytes, RawBytesList, validate_raw_byte, validate_raw_bytes, \
    InconsistentArgumentsError, UnusedArgumentError
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .frame_fields import CanIdHandler
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias


AIDataBytesAlias = Dict[str, Optional[RawByte]]
"""Alias of :ref:`Addressing Information <knowledge-base-n-ai>` that is carried in data bytes."""
AIAlias = Dict[str, Optional[Union[RawByte, AddressingTypeAlias]]]
"""Alias of :ref:`Addressing Information <knowledge-base-n-ai>`."""


class CanAddressingInformationHandler:
    """
    Helper class that provides utilities for CAN Addressing Information.

    .. note:: CAN :ref:`Addressing Information <knowledge-base-n-ai>` and its providing depends on
        :ref:`CAN addressing formats <knowledge-base-can-addressing>` used.

    .. warning:: This class contains only implementation that is consistent with ISO 15765 and
        **it does not take into account system specific requirements.**
    """

    ADDRESSING_TYPE_NAME = CanIdHandler.ADDRESSING_TYPE_NAME
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` parameter in Addressing Information."""
    TARGET_ADDRESS_NAME = CanIdHandler.TARGET_ADDRESS_NAME
    """Name of Target Address parameter in Addressing Information."""
    SOURCE_ADDRESS_NAME = CanIdHandler.SOURCE_ADDRESS_NAME
    """Name of Source Address parameter in Addressing Information."""
    ADDRESS_EXTENSION_NAME = "address_extension"
    """Name of Address Extension parameter in Addressing Information."""

    @classmethod
    def decode_ai(cls,
                  addressing_format: CanAddressingFormatAlias,
                  can_id: int,
                  ai_data_bytes: RawBytes) -> AIAlias:
        """
        Decode Addressing Information from CAN ID and data bytes.

        .. warning:: This methods might not extract full Addressing Information from the provided data as some of these
            information are system specific.

            For example, Addressing Type will not be decoded when either Normal 11bit, Extended or Mixed 11bit
            addressing format is used as the Addressing Type (in such case) depends on system specific behaviour.

        :param addressing_format: CAN Addressing Format used.
        :param can_id: Value of CAN Identifier.
        :param ai_data_bytes: Data bytes containing Addressing Information.
            This shall be either 0 or 1 byte located at the beginning of a CAN frame data field.
            Number and content of these bytes depends on :ref:`CAN Addressing Format <knowledge-base-can-addressing>`
            used.

        :return: Dictionary with Addressing Information decoded out of the provided CAN ID and Addressing Information
            data bytes.
        """
        from_data_bytes = cls.decode_ai_data_bytes(addressing_format=addressing_format, ai_data_bytes=ai_data_bytes)
        from_can_id = CanIdHandler.decode_can_id(addressing_format=addressing_format, can_id=can_id)
        names = (cls.ADDRESSING_TYPE_NAME, cls.TARGET_ADDRESS_NAME, cls.SOURCE_ADDRESS_NAME, cls.ADDRESS_EXTENSION_NAME)
        return {name: from_data_bytes.get(name, None) or from_can_id.get(name, None) for name in names}

    @classmethod
    def decode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormatAlias,
                             ai_data_bytes: RawBytes) -> AIDataBytesAlias:
        """
        Decode Addressing Information from CAN data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes containing Addressing Information.
            This shall be either 0 or 1 byte located at the beginning of a CAN frame data field.
            Number and content of these bytes depends on :ref:`CAN Addressing Format <knowledge-base-can-addressing>`
            used.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

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
    def encode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormatAlias,
                             target_address: Optional[RawByte] = None,
                             address_extension: Optional[RawByte] = None) -> RawBytesList:
        """
        Generate a list of data bytes that carry Addressing Information.

        :param addressing_format: CAN Addressing Format used.
        :param target_address: Target Address value used.
        :param address_extension: Source Address value used.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: List of data bytes that carry Addressing Information in CAN frame Data field.
        """
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format in (CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                 CanAddressingFormat.NORMAL_FIXED_ADDRESSING):
            return []
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            validate_raw_byte(target_address)
            return [target_address]  # type: ignore
        if addressing_format in (CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 CanAddressingFormat.MIXED_29BIT_ADDRESSING):
            validate_raw_byte(address_extension)
            return [address_extension]  # type: ignore
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @classmethod
    def get_ai_data_bytes_number(cls, addressing_format: CanAddressingFormatAlias) -> int:
        """
        Get number of data bytes that are used to carry Addressing Information.

        :param addressing_format: CAN Addressing Format used.

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
                    addressing_type: AddressingTypeAlias,
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
        :param addressing_type: Addressing type value to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise UnusedArgumentError: Value for at least one unused argument (not relevant for this can addressing format)
            was provided.
        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.
        """
        CanAddressingFormat.validate_member(addressing_format)
        if addressing_format == CanAddressingFormat.NORMAL_11BIT_ADDRESSING:
            if (target_address, source_address, address_extension) != (None, None, None):
                raise UnusedArgumentError(f"Values of Target Address, Source Address and Address Extension must not be "
                                          f"provided for {addressing_format}. Actual values: "
                                          f"target_address={target_address}, source_address={source_address}, "
                                          f"address_extension={address_extension}")
            cls.validate_ai_normal_11bit(addressing_type=addressing_type, can_id=can_id)  # type: ignore
        elif addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            if address_extension is not None:
                raise UnusedArgumentError(f"Value of Address Extension must not be provided for "
                                          f"{addressing_format}. Actual value: "
                                          f"address_extension={address_extension}")
            cls.validate_ai_normal_fixed(addressing_type=addressing_type,
                                         can_id=can_id,
                                         target_address=target_address,
                                         source_address=source_address)
        elif addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            if (source_address, address_extension) != (None, None):
                raise UnusedArgumentError(f"Values of Source Address and Address Extension must not be provided for "
                                          f"{addressing_format}. Actual values: "
                                          f"source_address={source_address}, address_extension={address_extension}")
            cls.validate_ai_extended(addressing_type=addressing_type,
                                     can_id=can_id,  # type: ignore
                                     target_address=target_address)  # type: ignore
        elif addressing_format == CanAddressingFormat.MIXED_11BIT_ADDRESSING:
            if (target_address, source_address) != (None, None):
                raise UnusedArgumentError(f"Values of Target Address and Source Address must not be provided for "
                                          f"{addressing_format}. Actual values: "
                                          f"target_address={target_address}, source_address={source_address}")
            cls.validate_ai_mixed_11bit(addressing_type=addressing_type,
                                        can_id=can_id,  # type: ignore
                                        address_extension=address_extension)  # type: ignore
        elif addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            cls.validate_ai_mixed_29bit(addressing_type=addressing_type,
                                        can_id=can_id,
                                        target_address=target_address,
                                        source_address=source_address,
                                        address_extension=address_extension)  # type: ignore
        else:
            raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @staticmethod
    def validate_ai_normal_11bit(addressing_type: AddressingTypeAlias, can_id: int) -> None:
        """
        Validate Addressing Information parameters for Normal 11-bit CAN Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Normal 11-bit Addressing format.
        """
        AddressingType.validate_member(addressing_type)
        CanIdHandler.validate_can_id(can_id)
        if not CanIdHandler.is_normal_11bit_addressed_can_id(can_id):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with "
                                             f"Normal 11-bit Addressing Format. Actual value: {can_id}")

    @staticmethod
    def validate_ai_normal_fixed(addressing_type: AddressingTypeAlias,
                                 can_id: Optional[int] = None,
                                 target_address: Optional[RawByte] = None,
                                 source_address: Optional[RawByte] = None) -> None:
        """
        Validate Addressing Information parameters for Normal Fixed CAN Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Normal Fixed Addressing format.
        """
        AddressingType.validate_member(addressing_type)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError(f"Values of target_address and source_address must be provided,"
                                                 f"if can_id value is None for Normal Fixed Addressing Format. "
                                                 f"Actual values: "
                                                 f"target_address={target_address}, source_address={source_address}")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
        else:
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

    @staticmethod
    def validate_ai_extended(addressing_type: AddressingTypeAlias, can_id: int, target_address: RawByte) -> None:
        """
        Validate Addressing Information parameters for Extended CAN Addressing format.

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

    @staticmethod
    def validate_ai_mixed_11bit(addressing_type: AddressingTypeAlias, can_id: int, address_extension: RawByte) -> None:
        """
        Validate Addressing Information parameters for Mixed 11-bit CAN Addressing format.

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

    @staticmethod
    def validate_ai_mixed_29bit(addressing_type: AddressingTypeAlias,
                                address_extension: RawByte,
                                can_id: Optional[int] = None,
                                target_address: Optional[RawByte] = None,
                                source_address: Optional[RawByte] = None) -> None:
        """
        Validate Addressing Information parameters for Mixed 29-bit CAN Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

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
            if addressing_type != decoded_info[CanIdHandler.ADDRESSING_TYPE_NAME]:
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Addressing Type."
                                                 f"Actual values: can_id={can_id}, addressing={addressing_type}")
            if target_address not in (decoded_info[CanIdHandler.TARGET_ADDRESS_NAME], None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Target Address."
                                                 f"Actual values: can_id={can_id}, target_address={target_address}")
            if source_address not in (decoded_info[CanIdHandler.SOURCE_ADDRESS_NAME], None):
                raise InconsistentArgumentsError(f"Provided value of CAN ID is not compatible with Source Address."
                                                 f"Actual values: can_id={can_id}, source_address={source_address}")

    @classmethod
    def validate_ai_data_bytes(cls, addressing_format: CanAddressingFormatAlias, ai_data_bytes: RawBytes) -> None:
        """
        Validate Addressing Information stored in CAN data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes to validate.

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

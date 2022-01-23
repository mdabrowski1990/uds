"""
Implementation of CAN Addressing Information.

This module contains helper class for managing :ref:`Addressing Information <knowledge-base-n-ai>` on CAN bus.
"""

__all__ = ["CanAddressingInformation"]

from typing import Optional, Dict, TypedDict, Type

from uds.utilities import RawByte, RawBytes, RawBytesList
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .abstract_addressing_information import AbstractCanAddressingInformation
from .normal_addressing_information import Normal11BitCanAddressingInformation, NormalFixedCanAddressingInformation
from .extended_addressing_information import ExtendedCanAddressingInformation
from .mixed_addressing_information import Mixed11BitCanAddressingInformation, Mixed29BitCanAddressingInformation


class CanAddressingInformation:
    """CAN Entity (either server or client) Addressing Information."""

    ADDRESSING_INFORMATION_MAPPING: Dict[CanAddressingFormatAlias, Type[AbstractCanAddressingInformation]] = {
        CanAddressingFormat.NORMAL_11BIT_ADDRESSING: Normal11BitCanAddressingInformation,
        CanAddressingFormat.NORMAL_FIXED_ADDRESSING: NormalFixedCanAddressingInformation,
        CanAddressingFormat.EXTENDED_ADDRESSING: ExtendedCanAddressingInformation,
        CanAddressingFormat.MIXED_11BIT_ADDRESSING: Mixed11BitCanAddressingInformation,
        CanAddressingFormat.MIXED_29BIT_ADDRESSING: Mixed29BitCanAddressingInformation,
    }
    """Dictionary with CAN Addressing format mapping to Addressing Information handler classes."""

    class DataBatesAIParamsAlias(TypedDict, total=True):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in data field."""

        target_address: Optional[RawByte]
        address_extension: Optional[RawByte]

    class DecodedAIParamsAlias(TypedDict, total=True):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in CAN ID and data field."""

        addressing_type: Optional[AddressingTypeAlias]
        target_address: Optional[RawByte]
        source_address: Optional[RawByte]
        address_extension: Optional[RawByte]

    def __new__(cls,
                addressing_format: CanAddressingFormatAlias,
                rx_physical: AbstractCanAddressingInformation.InputAIParamsAlias,
                tx_physical: AbstractCanAddressingInformation.InputAIParamsAlias,
                rx_functional: AbstractCanAddressingInformation.InputAIParamsAlias,
                tx_functional: AbstractCanAddressingInformation.InputAIParamsAlias) -> AbstractCanAddressingInformation:
        """
        Create object of CAN Entity (either server or client) Addressing Information.

        :param addressing_format: CAN Addressing format used by CAN Entity.
        :param rx_physical: Addressing Information parameters used for incoming physically addressed communication.
        :param tx_physical: Addressing Information parameters used for outgoing physically addressed communication.
        :param rx_functional: Addressing Information parameters used for incoming functionally addressed communication.
        :param tx_functional: Addressing Information parameters used for outgoing functionally addressed communication.
        """
        # TODO

    @staticmethod
    def validate_packet_ai(addressing_format: CanAddressingFormatAlias,
                           addressing_type: AddressingTypeAlias,
                           can_id: Optional[int],
                           target_address: Optional[RawByte],
                           source_address: Optional[RawByte],
                           address_extension: Optional[RawByte]) -> None:
        """
        Validate Addressing Information parameters of a CAN packet.

        :param addressing_format: CAN addressing format value to validate.
        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Addressing format used.
        """
        # TODO

    @classmethod
    def validate_ai_data_bytes(cls, addressing_format: CanAddressingFormatAlias, ai_data_bytes: RawBytes) -> None:
        """
        Validate Addressing Information stored in CAN data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes to validate.

        :raise InconsistentArgumentsError: Provided number of Addressing Information data bytes does not match
            Addressing Format used.
        """
        # TODO

    @classmethod
    def decode_ai(cls,
                  addressing_format: CanAddressingFormatAlias,
                  can_id: int,
                  ai_data_bytes: RawBytes) -> DecodedAIParamsAlias:
        """
        Decode Addressing Information parameters from CAN ID and data bytes.

        .. warning:: This methods might not extract full Addressing Information from the provided data as some of them
            are system specific.

            For example, Addressing Type will not be decoded when either Normal 11bit, Extended or Mixed 11bit
            addressing format is used as the Addressing Type (in such case) depends on system specific behaviour.

        :param addressing_format: CAN Addressing Format used.
        :param can_id: Value of CAN Identifier.
        :param ai_data_bytes: Data bytes containing Addressing Information.
            This parameter shall contain either 0 or 1 byte that is located at the beginning of a CAN frame data field.
            Number of these bytes depends on :ref:`CAN Addressing Format <knowledge-base-can-addressing>` used.

        :return: Dictionary with Addressing Information decoded out of the provided CAN ID and data bytes.
        """
        # TODO

    @classmethod
    def decode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormatAlias,
                             ai_data_bytes: RawBytes) -> DataBatesAIParamsAlias:
        """
        Decode Addressing Information from CAN data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes containing Addressing Information.
            This parameter shall contain either 0 or 1 byte that is located at the beginning of a CAN frame data field.
            Number of these bytes depends on :ref:`CAN Addressing Format <knowledge-base-can-addressing>` used.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Dictionary with Addressing Information decoded out of the provided data bytes.
        """
        # TODO

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
        # TODO

    @staticmethod
    def get_ai_data_bytes_number(addressing_format: CanAddressingFormatAlias) -> int:
        """
        Get number of data bytes that are used to carry Addressing Information.

        :param addressing_format: CAN Addressing Format used.

        :return: Number of data bytes in a CAN Packet that are used to carry Addressing Information for provided
            CAN Addressing Format.
        """
        # TODO










from typing import Optional, Union, Literal, Dict

from uds.utilities import RawByte, RawBytes, RawBytesList, validate_raw_byte, validate_raw_bytes, \
    InconsistentArgumentsError, UnusedArgumentError
from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from .frame_fields import CanIdHandler
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias


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

    AIDataBytesAlias = Dict[Literal[TARGET_ADDRESS_NAME, ADDRESS_EXTENSION_NAME], Optional[RawByte]]
    """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` that is carried in data bytes."""
    AIAlias = Dict[Literal[ADDRESSING_TYPE_NAME, TARGET_ADDRESS_NAME, SOURCE_ADDRESS_NAME, ADDRESS_EXTENSION_NAME],
                   Optional[Union[RawByte, AddressingTypeAlias]]]
    """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in CAN ID and data field."""

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
    def validate_ai(cls,  # TODO: move code
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

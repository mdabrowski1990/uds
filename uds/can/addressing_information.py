"""
Implementation of CAN Addressing Information.

This module contains helper class for managing :ref:`Addressing Information <knowledge-base-n-ai>` on CAN bus.
"""

__all__ = ["CanAddressingInformation"]

from typing import Optional, Dict, TypedDict, Type

from uds.utilities import InconsistentArgumentsError, \
    RawBytesAlias, RawBytesListAlias, validate_raw_byte, validate_raw_bytes
from uds.transmission_attributes import AddressingType
from .addressing_format import CanAddressingFormat
from .frame_fields import CanIdHandler
from .abstract_addressing_information import AbstractCanAddressingInformation, PacketAIParamsAlias
from .normal_addressing_information import Normal11BitCanAddressingInformation, NormalFixedCanAddressingInformation
from .extended_addressing_information import ExtendedCanAddressingInformation
from .mixed_addressing_information import Mixed11BitCanAddressingInformation, Mixed29BitCanAddressingInformation


class CanAddressingInformation:
    """CAN Entity (either server or client) Addressing Information."""

    ADDRESSING_INFORMATION_MAPPING: Dict[CanAddressingFormat, Type[AbstractCanAddressingInformation]] = {
        CanAddressingFormat.NORMAL_11BIT_ADDRESSING: Normal11BitCanAddressingInformation,
        CanAddressingFormat.NORMAL_FIXED_ADDRESSING: NormalFixedCanAddressingInformation,
        CanAddressingFormat.EXTENDED_ADDRESSING: ExtendedCanAddressingInformation,
        CanAddressingFormat.MIXED_11BIT_ADDRESSING: Mixed11BitCanAddressingInformation,
        CanAddressingFormat.MIXED_29BIT_ADDRESSING: Mixed29BitCanAddressingInformation,
    }
    """Dictionary with CAN Addressing format mapping to Addressing Information handler classes."""

    class DataBytesAIParamsAlias(TypedDict, total=False):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in data field."""

        target_address: int
        address_extension: int

    class DecodedAIParamsAlias(TypedDict, total=True):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters encoded in CAN ID and data field."""

        addressing_type: Optional[AddressingType]
        target_address: Optional[int]
        source_address: Optional[int]
        address_extension: Optional[int]

    def __new__(cls,  # type: ignore
                addressing_format: CanAddressingFormat,
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
        ai_class = cls.ADDRESSING_INFORMATION_MAPPING[addressing_format]
        return ai_class(rx_physical=rx_physical,
                        tx_physical=tx_physical,
                        rx_functional=rx_functional,
                        tx_functional=tx_functional)

    @classmethod
    def validate_packet_ai(cls,
                           addressing_format: CanAddressingFormat,
                           addressing_type: AddressingType,
                           can_id: Optional[int] = None,
                           target_address: Optional[int] = None,
                           source_address: Optional[int] = None,
                           address_extension: Optional[int] = None) -> PacketAIParamsAlias:
        """
        Validate Addressing Information parameters of a CAN packet.

        :param addressing_format: CAN addressing format value to validate.
        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].validate_packet_ai(
            addressing_type=addressing_type,
            can_id=can_id,
            target_address=target_address,
            source_address=source_address,
            address_extension=address_extension)

    @classmethod
    def validate_ai_data_bytes(cls, addressing_format: CanAddressingFormat, ai_data_bytes: RawBytesAlias) -> None:
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

    @classmethod
    def decode_packet_ai(cls,
                         addressing_format: CanAddressingFormat,
                         can_id: int,
                         ai_data_bytes: RawBytesAlias) -> DecodedAIParamsAlias:
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
        from_data_bytes = cls.decode_ai_data_bytes(addressing_format=addressing_format, ai_data_bytes=ai_data_bytes)
        from_can_id = CanIdHandler.decode_can_id(addressing_format=addressing_format, can_id=can_id)
        items_names = (AbstractCanAddressingInformation.ADDRESSING_TYPE_NAME,
                       AbstractCanAddressingInformation.TARGET_ADDRESS_NAME,
                       AbstractCanAddressingInformation.SOURCE_ADDRESS_NAME,
                       AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME)
        return {name: from_data_bytes.get(name, None) or from_can_id.get(name, None)
                for name in items_names}  # type: ignore

    @classmethod
    def decode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormat,
                             ai_data_bytes: RawBytesAlias) -> DataBytesAIParamsAlias:
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
        cls.validate_ai_data_bytes(addressing_format=addressing_format,
                                   ai_data_bytes=ai_data_bytes)
        if addressing_format in {CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                 CanAddressingFormat.NORMAL_FIXED_ADDRESSING}:
            return {}
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            return {AbstractCanAddressingInformation.TARGET_ADDRESS_NAME: ai_data_bytes[0]}  # type: ignore
        if addressing_format in {CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 CanAddressingFormat.MIXED_29BIT_ADDRESSING}:
            return {AbstractCanAddressingInformation.ADDRESS_EXTENSION_NAME:  ai_data_bytes[0]}  # type: ignore
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @classmethod
    def encode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormat,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> RawBytesListAlias:
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
    def get_ai_data_bytes_number(cls, addressing_format: CanAddressingFormat) -> int:
        """
        Get number of data bytes that are used to carry Addressing Information.

        :param addressing_format: CAN Addressing Format used.

        :return: Number of data bytes in a CAN Packet that are used to carry Addressing Information for provided
            CAN Addressing Format.
        """
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].AI_DATA_BYTES_NUMBER

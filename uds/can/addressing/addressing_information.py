"""
Implementation of Addressing Information for CAN bus.

This module contains helper class for managing :ref:`Addressing Information <knowledge-base-n-ai>` on CAN bus.
"""

__all__ = ["CanAddressingInformation"]

from typing import Dict, Optional, Type, TypedDict

from uds.addressing import AddressingType
from uds.utilities import InconsistentArgumentsError, RawBytesAlias, validate_raw_byte, validate_raw_bytes

from ..frame import CanIdHandler
from .abstract_addressing_information import AbstractCanAddressingInformation, CANAddressingParams
from .addressing_format import CanAddressingFormat
from .extended_addressing import ExtendedCanAddressingInformation
from .mixed_addressing import Mixed11BitCanAddressingInformation, Mixed29BitCanAddressingInformation
from .normal_addressing import NormalCanAddressingInformation, NormalFixedCanAddressingInformation


class CanAddressingInformation:
    """CAN Entity (either server or client) Addressing Information."""

    ADDRESSING_INFORMATION_MAPPING: Dict[CanAddressingFormat, Type[AbstractCanAddressingInformation]] = {
        CanAddressingFormat.NORMAL_ADDRESSING: NormalCanAddressingInformation,
        CanAddressingFormat.NORMAL_FIXED_ADDRESSING: NormalFixedCanAddressingInformation,
        CanAddressingFormat.EXTENDED_ADDRESSING: ExtendedCanAddressingInformation,
        CanAddressingFormat.MIXED_11BIT_ADDRESSING: Mixed11BitCanAddressingInformation,
        CanAddressingFormat.MIXED_29BIT_ADDRESSING: Mixed29BitCanAddressingInformation,
    }
    """Dictionary with CAN Addressing Formats mapped to Addressing Information handler classes."""

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

    def __new__(cls,
                addressing_format: CanAddressingFormat,
                rx_physical_params: AbstractCanAddressingInformation.InputAIParams,
                tx_physical_params: AbstractCanAddressingInformation.InputAIParams,
                rx_functional_params: AbstractCanAddressingInformation.InputAIParams,
                tx_functional_params: AbstractCanAddressingInformation.InputAIParams) -> AbstractCanAddressingInformation:
        """
        Create UDS Addressing Information for a CAN node.

        :param addressing_format: CAN Addressing format used by CAN node.
        :param rx_physical_params: Addressing Information parameters used for incoming physically addressed communication.
        :param tx_physical_params: Addressing Information parameters used for outgoing physically addressed communication.
        :param rx_functional_params: Addressing Information parameters used for incoming functionally addressed communication.
        :param tx_functional_params: Addressing Information parameters used for outgoing functionally addressed communication.
        """
        ai_class = cls.ADDRESSING_INFORMATION_MAPPING[addressing_format]
        return ai_class(rx_physical_params=rx_physical_params,
                        tx_physical_params=tx_physical_params,
                        rx_functional_params=rx_functional_params,
                        tx_functional_params=tx_functional_params)

    @classmethod
    def get_ai_data_bytes_number(cls, addressing_format: CanAddressingFormat) -> int:
        """
        Get number of data bytes that are used to carry Addressing Information.

        :param addressing_format: CAN Addressing Format used.

        :return: Number of data bytes in a CAN Packet that are used to carry Addressing Information for provided
            CAN Addressing Format.
        """
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].AI_DATA_BYTES_NUMBER

    @classmethod
    def is_compatible_can_id(cls,
                             addressing_format: CanAddressingFormat,
                             can_id: int,
                             addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check whether provided CAN ID is consistent the provided CAN Addressing Format.

        :param addressing_format: Addressing format used.
        :param can_id: CAN ID value to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].is_compatible_can_id(
            can_id=can_id, addressing_type=addressing_type)

    @classmethod
    def decode_can_id(cls,
                      addressing_format: CanAddressingFormat,
                      can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """
        Extract Addressing Information parameters out of CAN ID.

        .. warning:: This methods might not extract any Addressing Information parameters from the provided CAN ID
            as some of the information are system specific.

            For example, Addressing Type (even though it always depends on CAN ID value) will not be decoded when
            either Normal, Extended or Mixed 11bit addressing format is used as the Addressing Type (in such case)
            depends on system specific behaviour.

        :param addressing_format: Addressing format used.
        :param can_id: CAN ID from which Addressing Information to be extracted.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Format.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Dictionary with Addressing Information decoded out of the provided CAN ID.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].decode_can_id(can_id=can_id)

    @classmethod
    def encode_can_id(cls,
                      addressing_format: CanAddressingFormat,
                      addressing_type: AddressingType,
                      target_address: int,
                      source_address: int,
                      priority: int = CanIdHandler.DEFAULT_PRIORITY_VALUE) -> int:
        """
        Generate CAN ID value for Normal Fixed CAN Addressing format.

        :param addressing_format: Addressing format used.
        :param addressing_type: Addressing type used.
        :param target_address: Target Address value to use.
        :param source_address: Source Address value to use.
        :param priority: Priority parameter value to use.

        :raise ValueError: CAN ID cannot be encoded for provided CAN Addressing Format.

        :return: Value of CAN ID that is compatible with provided CAN Addressing Format and was generated out of
            the provided values.
        """
        if addressing_format == CanAddressingFormat.NORMAL_FIXED_ADDRESSING:
            return NormalFixedCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                                     target_address=target_address,
                                                                     source_address=source_address,
                                                                     priority=priority)
        if addressing_format == CanAddressingFormat.MIXED_29BIT_ADDRESSING:
            return Mixed29BitCanAddressingInformation.encode_can_id(addressing_type=addressing_type,
                                                                    target_address=target_address,
                                                                    source_address=source_address,
                                                                    priority=priority)
        raise ValueError("Provided CAN Addressing Format does not offer utility of CAN ID encoding.")

    @classmethod
    def validate_addressing_params(cls,
                                   addressing_format: CanAddressingFormat,
                                   addressing_type: AddressingType,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> CANAddressingParams:
        """
        Validate Addressing Information parameters of a CAN packet.

        :param addressing_format: CAN addressing format used.
        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].validate_addressing_params(
            addressing_format=addressing_format,
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
            CAN Addressing Format used.
        """
        CanAddressingFormat.validate_member(addressing_format)
        validate_raw_bytes(ai_data_bytes, allow_empty=True)
        expected_ai_bytes_number = cls.get_ai_data_bytes_number(addressing_format)
        if expected_ai_bytes_number != len(ai_data_bytes):
            raise InconsistentArgumentsError("Number of Addressing Information data bytes does not match provided "
                                             "CAN Addressing Format.")

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
        from_can_id = cls.decode_can_id(addressing_format=addressing_format, can_id=can_id)
        return cls.DecodedAIParamsAlias(
            addressing_type=from_can_id.get("addressing_type", None),
            target_address=from_data_bytes.get("target_address", None) or from_can_id.get("target_address", None),
            source_address=from_can_id.get("source_address", None),
            address_extension=from_data_bytes.get("address_extension", None))

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
        if addressing_format in {CanAddressingFormat.NORMAL_ADDRESSING,
                                 CanAddressingFormat.NORMAL_FIXED_ADDRESSING}:
            return cls.DataBytesAIParamsAlias()
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            return cls.DataBytesAIParamsAlias(target_address=ai_data_bytes[0])
        if addressing_format in {CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 CanAddressingFormat.MIXED_29BIT_ADDRESSING}:
            return cls.DataBytesAIParamsAlias(address_extension=ai_data_bytes[0])
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

    @classmethod
    def encode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormat,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> bytearray:
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
        if addressing_format in (CanAddressingFormat.NORMAL_ADDRESSING,
                                 CanAddressingFormat.NORMAL_FIXED_ADDRESSING):
            return bytearray()
        if addressing_format == CanAddressingFormat.EXTENDED_ADDRESSING:
            validate_raw_byte(target_address)
            return bytearray([target_address])
        if addressing_format in (CanAddressingFormat.MIXED_11BIT_ADDRESSING,
                                 CanAddressingFormat.MIXED_29BIT_ADDRESSING):
            validate_raw_byte(address_extension)
            return bytearray([address_extension])
        raise NotImplementedError(f"Missing implementation for: {addressing_format}")

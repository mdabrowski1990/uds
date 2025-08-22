"""
Implementation of Addressing Information for CAN bus.

This module contains helper class for managing :ref:`Addressing Information <knowledge-base-n-ai>` on CAN bus.
"""

__all__ = ["CanAddressingInformation"]

from typing import Dict, Optional, Type

from uds.addressing import AddressingType
from uds.utilities import InconsistencyError, RawBytesAlias, validate_raw_bytes

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

    def __new__(cls,  # type: ignore
                addressing_format: CanAddressingFormat,
                rx_physical_params: AbstractCanAddressingInformation.InputAIParams,
                tx_physical_params: AbstractCanAddressingInformation.InputAIParams,
                rx_functional_params: AbstractCanAddressingInformation.InputAIParams,
                tx_functional_params: AbstractCanAddressingInformation.InputAIParams
                ) -> AbstractCanAddressingInformation:
        """
        Create UDS Addressing Information for a CAN node.

        :param addressing_format: CAN Addressing format used by CAN node.
        :param rx_physical_params: Addressing Information parameters used for incoming physically
            addressed communication.
        :param tx_physical_params: Addressing Information parameters used for outgoing physically
            addressed communication.
        :param rx_functional_params: Addressing Information parameters used for incoming functionally
            addressed communication.
        :param tx_functional_params: Addressing Information parameters used for outgoing functionally
            addressed communication.
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
    def validate_ai_data_bytes(cls, addressing_format: CanAddressingFormat, ai_data_bytes: RawBytesAlias) -> None:
        """
        Validate Addressing Information stored in CAN data bytes.

        :param addressing_format: CAN Addressing Format used.
        :param ai_data_bytes: Data bytes to validate.

        :raise InconsistencyError: Provided number of Addressing Information data bytes does not match
            CAN Addressing Format used.
        """
        CanAddressingFormat.validate_member(addressing_format)
        validate_raw_bytes(ai_data_bytes, allow_empty=True)
        expected_ai_bytes_number = cls.get_ai_data_bytes_number(addressing_format)
        if expected_ai_bytes_number != len(ai_data_bytes):
            raise InconsistencyError("Number of Addressing Information data bytes does not match provided "
                                     f"CAN Addressing Format. CAN Addressing Format: {addressing_format}. "
                                     f"Provided AI Data Bytes number: {len(ai_data_bytes)}. "
                                     f"Expected AI Data Bytes number: {expected_ai_bytes_number}.")

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
    def decode_can_id_ai_params(cls,
                                addressing_format: CanAddressingFormat,
                                can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """
        Decode Addressing Information parameters from CAN Identifier.

        :param addressing_format: Addressing format used.
        :param can_id: Value of a CAN Identifier.

        :return: Decoded Addressing Information parameters.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].decode_can_id_ai_params(can_id)

    @classmethod
    def decode_data_bytes_ai_params(cls,
                                    addressing_format: CanAddressingFormat,
                                    ai_data_bytes: RawBytesAlias
                                    ) -> AbstractCanAddressingInformation.DataBytesAIParamsAlias:
        """
        Decode Addressing Information parameters from CAN data bytes.

        :param addressing_format: Addressing format used.
        :param ai_data_bytes: Data bytes containing Addressing Information.

        :return: Decoded Addressing Information parameters.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].decode_data_bytes_ai_params(ai_data_bytes)

    @classmethod
    def decode_frame_ai_params(cls,
                               addressing_format: CanAddressingFormat,
                               can_id: int,
                               raw_frame_data: RawBytesAlias) -> AbstractCanAddressingInformation.DecodedAIParamsAlias:
        """
        Decode Addressing Information parameters from a CAN Frame.

        :param addressing_format: Addressing format used.
        :param can_id: CAN Identifier value of a CAN frame.
        :param raw_frame_data: Raw data bytes of a CAN frame

        :return: Decoded Addressing Information parameters.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].decode_frame_ai_params(
            can_id=can_id, raw_frame_data=raw_frame_data)

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
    def encode_ai_data_bytes(cls,
                             addressing_format: CanAddressingFormat,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> bytearray:
        """
        Generate data bytes that carry Addressing Information.

        :param addressing_format: CAN Addressing Format used.
        :param target_address: Target Address value used.
        :param address_extension: Source Address value used.

        :return: Data bytes that carry Addressing Information in a CAN frame Data field.
        """
        CanAddressingFormat.validate_member(addressing_format)
        return cls.ADDRESSING_INFORMATION_MAPPING[addressing_format].encode_ai_data_bytes(
            target_address=target_address, address_extension=address_extension)

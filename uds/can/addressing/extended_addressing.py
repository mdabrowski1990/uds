"""Implementation of Extended CAN Addressing format."""

__all__ = ["ExtendedCanAddressingInformation"]

from typing import Optional

from uds.addressing import AddressingType
from uds.can.addressing.abstract_addressing_information import AbstractCanAddressingInformation, CANAddressingParams
from uds.can.addressing.addressing_format import CanAddressingFormat
from uds.can.frame import CanIdHandler
from uds.utilities import InconsistencyError, RawBytesAlias, UnusedArgumentError, validate_raw_byte, validate_raw_bytes


class ExtendedCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Extended Addressing format."""

    ADDRESSING_FORMAT = CanAddressingFormat.EXTENDED_ADDRESSING
    """CAN Addressing Format used."""

    AI_DATA_BYTES_NUMBER = 1
    """Number of CAN frame data bytes that are used to carry Addressing Information."""

    def _validate_addressing_information(self) -> None:
        """
        Validate Addressing Information parameters.

        :raise InconsistencyError: Provided values are not consistent with each other.
        """
        rx_can_ids = {self.rx_physical_params["can_id"], self.rx_functional_params["can_id"]}
        tx_can_ids = {self.tx_physical_params["can_id"], self.tx_functional_params["can_id"]}
        if (self.rx_physical_params["can_id"] in tx_can_ids
                or self.tx_physical_params["can_id"] in rx_can_ids
                or self.rx_functional_params["can_id"] in tx_can_ids
                or self.tx_functional_params["can_id"] in rx_can_ids):
            raise InconsistencyError("CAN ID used for transmission cannot be used for receiving too.")

    @classmethod
    def validate_addressing_params(cls,  # type: ignore
                                   addressing_type: AddressingType,
                                   addressing_format: CanAddressingFormat = ADDRESSING_FORMAT,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> CANAddressingParams:
        """
        Validate Addressing Information parameters of a CAN packet that uses Extended Addressing format.

        :param addressing_type: Addressing type to validate.
        :param addressing_format: CAN Addressing Format to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise ValueError: Provided Addressing format cannot be handled by this class.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.
        :raise InconsistencyError: Provided CAN ID value is incompatible with Extended Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if addressing_format != cls.ADDRESSING_FORMAT:
            raise ValueError(f"This class handles only one CAN Addressing format: {cls.ADDRESSING_FORMAT}")
        if (source_address, address_extension) != (None, None):
            raise UnusedArgumentError("Values of Source Address and Address Extension are not supported by "
                                      "Extended Addressing format and must be equal None.")
        addressing_type = AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)  # type: ignore
        if not cls.is_compatible_can_id(can_id=can_id, addressing_type=addressing_type):  # type: ignore
            raise InconsistencyError("Provided value of CAN ID is incompatible with Extended Addressing format.")
        return CANAddressingParams(addressing_format=cls.ADDRESSING_FORMAT,
                                   addressing_type=addressing_type,
                                   can_id=can_id,  # type: ignore
                                   target_address=target_address,
                                   source_address=source_address,
                                   address_extension=address_extension)

    @staticmethod
    def is_compatible_can_id(can_id: int,
                             addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check whether provided CAN ID is consistent with Extended Addressing format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """
        return CanIdHandler.is_can_id(can_id)

    @staticmethod
    def decode_can_id_ai_params(can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """Decode Addressing Information parameters from CAN Identifier."""
        return AbstractCanAddressingInformation.CanIdAIParams(addressing_type=None,
                                                              target_address=None,
                                                              source_address=None,
                                                              priority=None)

    @staticmethod
    def decode_data_bytes_ai_params(
            ai_data_bytes: RawBytesAlias) -> AbstractCanAddressingInformation.DataBytesAIParamsAlias:
        """
        Decode Addressing Information parameters from CAN data bytes.

        :param ai_data_bytes: Data bytes containing Addressing Information.

        :return: Decoded Addressing Information parameters.
        """
        validate_raw_bytes(ai_data_bytes, allow_empty=False)
        return AbstractCanAddressingInformation.DataBytesAIParamsAlias(target_address=ai_data_bytes[0])

    @classmethod
    def encode_ai_data_bytes(cls,
                             target_address: Optional[int] = None,
                             address_extension: Optional[int] = None) -> bytearray:
        """
        Generate data bytes that carry Addressing Information.

        :param target_address: Target Address value used.
        :param address_extension: Source Address value used.

        :return: Data bytes that carry Addressing Information in a CAN frame Data field.
        """
        validate_raw_byte(target_address)  # type: ignore
        return bytearray([target_address])  # type: ignore

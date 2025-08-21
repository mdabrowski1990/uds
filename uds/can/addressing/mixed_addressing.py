"""Implementation of Mixed CAN Addressing formats."""

__all__ = ["Mixed11BitCanAddressingInformation", "Mixed29BitCanAddressingInformation"]

from typing import Optional

from uds.addressing import AddressingType
from uds.can.addressing.abstract_addressing_information import AbstractCanAddressingInformation, CANAddressingParams
from uds.can.addressing.addressing_format import CanAddressingFormat
from uds.can.frame import CanIdHandler
from uds.utilities import InconsistencyError, RawBytesAlias, UnusedArgumentError, validate_raw_byte, validate_raw_bytes


class Mixed11BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Mixed 11-bit Addressing format."""

    ADDRESSING_FORMAT = CanAddressingFormat.MIXED_11BIT_ADDRESSING
    """CAN Addressing format used."""

    AI_DATA_BYTES_NUMBER = 1
    """Number of CAN frame data bytes that are used to carry Addressing Information."""

    def _validate_addressing_information(self) -> None:
        """
        Validate Addressing Information parameters.

        :raise InconsistencyError: Provided values are not consistent with each other.
        """
        if self.rx_physical_params["address_extension"] != self.tx_physical_params["address_extension"]:
            raise InconsistencyError("Addressing Extension parameter must be the same for incoming and "
                                             "outgoing physically addressed CAN packets.")
        if self.rx_functional_params["address_extension"] != self.tx_functional_params["address_extension"]:
            raise InconsistencyError("Addressing Extension parameter must be the same for incoming and "
                                             "outgoing functionally addressed CAN packets.")
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
        Validate Addressing Information parameters in Mixed 11-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param addressing_format: CAN Addressing Format to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise ValueError: Provided Addressing format cannot be handled by this class.
        :raise UnusedArgumentError: At least one provided parameter is not supported by this Addressing format.
        :raise InconsistencyError: Provided CAN ID value is incompatible with Mixed 11-bit Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if addressing_format != cls.ADDRESSING_FORMAT:
            raise ValueError(f"This class handles only one CAN Addressing format: {cls.ADDRESSING_FORMAT}")
        if (target_address, source_address) != (None, None):
            raise UnusedArgumentError("Values of Target Address and Source Address are not supported "
                                      "by Mixed 11-bit Addressing format and must be equal None.")
        addressing_type = AddressingType.validate_member(addressing_type)
        validate_raw_byte(address_extension)  # type: ignore
        if not cls.is_compatible_can_id(can_id=can_id, addressing_type=addressing_type):  # type: ignore
            raise InconsistencyError("Provided value of CAN ID is incompatible with "
                                             "Mixed 11-bit Addressing format.")
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
        Check whether provided CAN ID is consistent with Normal Addressing Format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """
        return CanIdHandler.is_standard_can_id(can_id)

    @staticmethod
    def decode_can_id_ai_params(can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """
        Decode Addressing Information parameters from CAN Identifier.

        :param can_id: Value of a CAN Identifier.

        :return: Decoded Addressing Information parameters.
        """
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
        return AbstractCanAddressingInformation.DataBytesAIParamsAlias(address_extension=ai_data_bytes[0])

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
        validate_raw_byte(address_extension)  # type: ignore
        return bytearray([address_extension])  # type: ignore


class Mixed29BitCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Mixed 29-bit Addressing format."""

    ADDRESSING_FORMAT = CanAddressingFormat.MIXED_29BIT_ADDRESSING
    """CAN Addressing format used."""

    AI_DATA_BYTES_NUMBER = 1
    """Number of CAN frame data bytes that are used to carry Addressing Information."""

    def _validate_addressing_information(self) -> None:
        """
        Validate Addressing Information parameters.

        :raise InconsistencyError: Provided values are not consistent with each other.
        """
        if self.rx_physical_params["address_extension"] != self.tx_physical_params["address_extension"]:
            raise InconsistencyError("Addressing Extension parameter must be the same for incoming and "
                                             "outgoing physically addressed CAN packets.")
        if self.rx_functional_params["address_extension"] != self.tx_functional_params["address_extension"]:
            raise InconsistencyError("Addressing Extension parameter must be the same for incoming and "
                                             "outgoing functionally addressed CAN packets.")
        if (self.rx_physical_params["target_address"] != self.tx_physical_params["source_address"]
                or self.rx_physical_params["source_address"] != self.tx_physical_params["target_address"]):
            raise InconsistencyError("Target Address and Source Address for incoming physically addressed "
                                             "CAN packets must equal Source Address and Target Address for outgoing "
                                             "physically addressed CAN packets.")
        if self.rx_functional_params["can_id"] == self.tx_functional_params["can_id"]:
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
        Validate Addressing Information parameters of a CAN packet that uses Mixed 29-bit Addressing format.

        :param addressing_type: Addressing type to validate.
        :param addressing_format: CAN Addressing Format to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise ValueError: Provided Addressing format cannot be handled by this class.
        :raise InconsistencyError: Provided Target Address, Source Address or CAN ID values are incompatible
            with each other or Mixed 29-bit Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if addressing_format != cls.ADDRESSING_FORMAT:
            raise ValueError(f"This class handles only one CAN Addressing format: {cls.ADDRESSING_FORMAT}")
        addressing_type = AddressingType.validate_member(addressing_type)
        validate_raw_byte(address_extension)  # type: ignore
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistencyError("Values of target_address and source_address must be provided for Mixed 29-bit Addressing Format if can_id value is None.")
            validate_raw_byte(target_address)  # type: ignore
            validate_raw_byte(source_address)  # type: ignore
            encoded_can_id = cls.encode_can_id(addressing_type=addressing_type,
                                               target_address=target_address,  # type: ignore
                                               source_address=source_address)  # type: ignore
            return CANAddressingParams(addressing_format=cls.ADDRESSING_FORMAT,
                                       addressing_type=addressing_type,
                                       can_id=encoded_can_id,
                                       target_address=target_address,
                                       source_address=source_address,
                                       address_extension=address_extension)
        decoded_info = cls.decode_can_id_ai_params(can_id)
        if addressing_type != decoded_info["addressing_type"]:
            raise InconsistencyError("Provided value of CAN ID is incompatible with Addressing Type.")
        if target_address not in {decoded_info["target_address"], None}:
            raise InconsistencyError("Provided value of CAN ID is incompatible with Target Address.")
        if source_address not in {decoded_info["source_address"], None}:
            raise InconsistencyError("Provided value of CAN ID is incompatible with Source Address.")
        return CANAddressingParams(addressing_format=cls.ADDRESSING_FORMAT,
                                   addressing_type=addressing_type,
                                   can_id=can_id,
                                   target_address=decoded_info["target_address"],
                                   source_address=decoded_info["source_address"],
                                   address_extension=address_extension)

    @staticmethod
    def is_compatible_can_id(can_id: int,
                             addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check whether provided CAN ID is consistent with Mixed 29-bit Addressing format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """
        if addressing_type is not None:
            addressing_type = AddressingType.validate_member(addressing_type)
        masked_can_id = can_id & CanIdHandler.ADDRESSING_MASK
        if (masked_can_id == CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
                and addressing_type in {None, AddressingType.PHYSICAL}):
            return True
        if (masked_can_id == CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
                and addressing_type in {None, AddressingType.FUNCTIONAL}):
            return True
        return False

    @classmethod
    def decode_can_id_ai_params(cls, can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """Decode Addressing Information parameters from CAN Identifier."""
        CanIdHandler.validate_can_id(can_id)
        if not cls.is_compatible_can_id(can_id):
            raise ValueError("Provided CAN ID value is out of range.")
        target_address = (can_id >> CanIdHandler.TARGET_ADDRESS_BIT_OFFSET) & 0xFF
        source_address = (can_id >> CanIdHandler.SOURCE_ADDRESS_BIT_OFFSET) & 0xFF
        can_id_masked_value = can_id & CanIdHandler.ADDRESSING_MASK
        priority = can_id >> CanIdHandler.PRIORITY_BIT_OFFSET
        if can_id_masked_value == CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE:
            return AbstractCanAddressingInformation.CanIdAIParams(addressing_type=AddressingType.PHYSICAL,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  priority=priority)
        if can_id_masked_value == CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE:
            return AbstractCanAddressingInformation.CanIdAIParams(addressing_type=AddressingType.FUNCTIONAL,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  priority=priority)
        raise NotImplementedError("CAN ID in Mixed 29-bit Addressing format was provided, but it was not handled.")

    @staticmethod
    def decode_data_bytes_ai_params(
            ai_data_bytes: RawBytesAlias) -> AbstractCanAddressingInformation.DataBytesAIParamsAlias:
        """
        Decode Addressing Information parameters from CAN data bytes.

        :param ai_data_bytes: Data bytes containing Addressing Information.

        :return: Decoded Addressing Information parameters.
        """
        validate_raw_bytes(ai_data_bytes, allow_empty=False)
        return AbstractCanAddressingInformation.DataBytesAIParamsAlias(address_extension=ai_data_bytes[0])

    @classmethod
    def encode_can_id(cls,
                      addressing_type: AddressingType,
                      target_address: int,
                      source_address: int,
                      priority: int = CanIdHandler.DEFAULT_PRIORITY_VALUE) -> int:
        """
        Generate CAN ID value for Mixed 29-bit CAN Addressing format.

        :param addressing_type: Addressing type used.
        :param target_address: Target Address value to use.
        :param source_address: Source Address value to use.
        :param priority: Priority parameter value to use.

        :return: Value of CAN ID (compatible with Mixed 29-bit Addressing format) that was generated from
            the provided values.
        """
        addressing_type = AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)
        validate_raw_byte(source_address)
        CanIdHandler.validate_priority(priority)
        priority_value = priority << CanIdHandler.PRIORITY_BIT_OFFSET
        target_address_value = target_address << CanIdHandler.TARGET_ADDRESS_BIT_OFFSET
        source_address_value = source_address << CanIdHandler.SOURCE_ADDRESS_BIT_OFFSET
        if addressing_type == AddressingType.PHYSICAL:
            return (priority_value
                    + CanIdHandler.MIXED_29BIT_PHYSICAL_ADDRESSING_MASKED_VALUE
                    + target_address_value
                    + source_address_value)
        if addressing_type == AddressingType.FUNCTIONAL:
            return (priority_value
                    + CanIdHandler.MIXED_29BIT_FUNCTIONAL_ADDRESSING_MASKED_VALUE
                    + target_address_value
                    + source_address_value)
        raise NotImplementedError("Provided Addressing Type is not handled.")

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
        validate_raw_byte(address_extension)  # type: ignore
        return bytearray([address_extension])  # type: ignore

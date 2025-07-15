"""Implementation of Normal Addressing Information handlers."""

__all__ = ["NormalCanAddressingInformation", "NormalFixedCanAddressingInformation"]

from typing import Optional

from uds.addressing import AddressingType
from uds.utilities import InconsistentArgumentsError, UnusedArgumentError, validate_raw_byte

from .abstract_addressing_information import AbstractCanAddressingInformation, CANAddressingParams
from uds.can.addressing.addressing_format import CanAddressingFormat
from uds.can.frame import CanIdHandler


class NormalCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Normal Addressing format."""

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""
        return CanAddressingFormat.NORMAL_ADDRESSING

    @property
    def ai_data_bytes_number(self) -> int:
        """Number of CAN frame data bytes that are used to carry Addressing Information."""
        return 0

    @staticmethod
    def is_compatible_can_id(can_id: int,
                             addressing_type: Optional[AddressingType]=None) -> bool:
        """
        Check whether provided CAN ID is consistent with Normal Addressing Format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """
        return CanIdHandler.is_can_id(can_id)

    @staticmethod
    def decode_can_id(can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """Decode Addressing Information parameters from CAN Identifier."""
        return AbstractCanAddressingInformation.CanIdAIParams(addressing_type=None,
                                                              target_address=None,
                                                              source_address=None,
                                                              priority=None)

    @classmethod
    def validate_addressing_params(cls,
                                   addressing_type: AddressingType,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> CANAddressingParams:
        """
        Validate Addressing Information parameters in Normal Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided CAN ID value is incompatible with Normal 11-bit Addressing format.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if (target_address, source_address, address_extension) != (None, None, None):
            raise UnusedArgumentError("Values of Target Address, Source Address and Address Extension are "
                                      "not supported by Normal Addressing format and all must be None.")
        addressing_type = AddressingType.validate_member(addressing_type)
        if not cls.is_compatible_can_id(can_id=can_id, addressing_type=addressing_type):
            raise InconsistentArgumentsError("Provided value of CAN ID is incompatible with "
                                             "Normal Addressing Format.")
        return CANAddressingParams(addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
                                   addressing_type=addressing_type,
                                   can_id=can_id,
                                   target_address=target_address,
                                   source_address=source_address,
                                   address_extension=address_extension)

    def _validate_addressing_information(self) -> None:
        """
        Validate Addressing Information parameters.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other.
        """
        rx_can_ids = {self.rx_physical_params["can_id"], self.rx_functional_params["can_id"]}
        tx_can_ids = {self.tx_physical_params["can_id"], self.tx_functional_params["can_id"]}
        if (self.rx_physical_params["can_id"] in tx_can_ids
                or self.tx_physical_params["can_id"] in rx_can_ids
                or self.rx_functional_params["can_id"] in tx_can_ids
                or self.tx_functional_params["can_id"] in rx_can_ids):
            raise InconsistentArgumentsError("CAN ID used for transmission cannot be used for reception.")


class NormalFixedCanAddressingInformation(AbstractCanAddressingInformation):
    """Addressing Information of CAN Entity (either server or client) that uses Normal Fixed Addressing format."""

    @property
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""
        return CanAddressingFormat.NORMAL_FIXED_ADDRESSING

    @property
    def ai_data_bytes_number(self) -> int:
        """Number of CAN frame data bytes that are used to carry Addressing Information."""
        return 0

    @staticmethod
    def is_compatible_can_id(can_id: int,
                             addressing_type: Optional[AddressingType] = None) -> bool:
        """
        Check whether provided CAN ID is consistent with Normal Fixed Addressing Format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """
        if addressing_type is not None:
            addressing_type = AddressingType.validate_member(addressing_type)
        masked_can_id = can_id & CanIdHandler.ADDRESSING_MASK
        if (masked_can_id == CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
                and addressing_type in {None, AddressingType.PHYSICAL}):
            return True
        if (masked_can_id == CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE
                and addressing_type in {None, AddressingType.FUNCTIONAL}):
            return True
        return False

    @classmethod
    def decode_can_id(cls, can_id: int) -> AbstractCanAddressingInformation.CanIdAIParams:
        """
        Extract Addressing Information parameters from CAN Identifier for Normal Fixed CAN Addressing format.

        :param can_id: CAN Identifier to extract parameters from.

        :return: Dictionary with extracted addressing parameters.
        """
        CanIdHandler.validate_can_id(can_id)
        if not cls.is_compatible_can_id(can_id):
            raise ValueError("Provided CAN ID value is out of range.")
        target_address = (can_id >> CanIdHandler.TARGET_ADDRESS_BIT_OFFSET) & 0xFF
        source_address = (can_id >> CanIdHandler.SOURCE_ADDRESS_BIT_OFFSET) & 0xFF
        can_id_masked_value = can_id & CanIdHandler.ADDRESSING_MASK
        priority = can_id >> CanIdHandler.PRIORITY_BIT_OFFSET
        if can_id_masked_value == CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE:
            return AbstractCanAddressingInformation.CanIdAIParams(addressing_type=AddressingType.PHYSICAL,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  priority=priority)
        if can_id_masked_value == CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE:
            return AbstractCanAddressingInformation.CanIdAIParams(addressing_type=AddressingType.FUNCTIONAL,
                                                                  target_address=target_address,
                                                                  source_address=source_address,
                                                                  priority=priority)
        raise NotImplementedError("CAN ID in Normal Fixed Addressing format was provided, but cannot be handled.")

    @classmethod
    def encode_can_id(cls,
                      addressing_type: AddressingType,
                      target_address: int,
                      source_address: int,
                      priority: int = CanIdHandler.DEFAULT_PRIORITY_VALUE) -> int:
        """
        Generate CAN ID value for Normal Fixed CAN Addressing format.

        :param addressing_type: Addressing type used.
        :param target_address: Target Address value to use.
        :param source_address: Source Address value to use.
        :param priority: Priority parameter value to use.

        :raise NotImplementedError: There is missing implementation for the provided Addressing Type.
            Please create an issue in our `Issues Tracking System <https://github.com/mdabrowski1990/uds/issues>`_
            with detailed description if you face this error.

        :return: Value of CAN ID (compatible with Normal Fixed Addressing Format) that was generated from
            the provided values.
        """
        AddressingType.validate_member(addressing_type)
        validate_raw_byte(target_address)
        validate_raw_byte(source_address)
        CanIdHandler.validate_priority(priority)
        priority_value = priority << CanIdHandler.PRIORITY_BIT_OFFSET
        target_address_value = target_address << CanIdHandler.TARGET_ADDRESS_BIT_OFFSET
        source_address_value = source_address << CanIdHandler.SOURCE_ADDRESS_BIT_OFFSET
        if addressing_type == AddressingType.PHYSICAL:
            return (priority_value
                    + CanIdHandler.NORMAL_FIXED_PHYSICAL_ADDRESSING_MASKED_VALUE
                    + target_address_value
                    + source_address_value)
        if addressing_type == AddressingType.FUNCTIONAL:
            return (priority_value
                    + CanIdHandler.NORMAL_FIXED_FUNCTIONAL_ADDRESSING_MASKED_VALUE
                    + target_address_value
                    + source_address_value)
        raise NotImplementedError("Unhandled addressing type value was provided.")

    @classmethod
    def validate_addressing_params(cls,
                                   addressing_type: AddressingType,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> CANAddressingParams:
        """
        Validate Addressing Information parameters of a CAN packet that uses Normal Fixed Addressing format.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided Target Address, Source Address or CAN ID values are incompatible
            with each other or Normal Fixed Addressing format.
        :raise UnusedArgumentError: Provided parameter is not supported by this Addressing format.

        :return: Normalized dictionary with the provided Addressing Information.
        """
        if address_extension is not None:
            raise UnusedArgumentError("Value of Address Extension is not supported by Normal Fixed Addressing format "
                                      "and must be None.")
        addressing_type = AddressingType.validate_member(addressing_type)
        if can_id is None:
            if None in (target_address, source_address):
                raise InconsistentArgumentsError("Values of target_address and source_address must be provided, "
                                                 "for Normal Fixed Addressing Format if can_id value is None.")
            validate_raw_byte(target_address)
            validate_raw_byte(source_address)
            encoded_can_id = cls.encode_can_id(addressing_type=addressing_type,
                                               target_address=target_address,
                                               source_address=source_address)
            return CANAddressingParams(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                       addressing_type=addressing_type,
                                       can_id=encoded_can_id,
                                       target_address=target_address,
                                       source_address=source_address,
                                       address_extension=address_extension)
        decoded_info = cls.decode_can_id(can_id)
        if addressing_type != decoded_info["addressing_type"]:
            raise InconsistentArgumentsError(f"Provided value of CAN ID is incompatible with Addressing Type.")
        if target_address not in (decoded_info["target_address"], None):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is incompatible with Target Address.")
        if source_address not in (decoded_info["source_address"], None):
            raise InconsistentArgumentsError(f"Provided value of CAN ID is incompatible with Source Address.")
        return CANAddressingParams(addressing_format=CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                   addressing_type=addressing_type,
                                   can_id=can_id,
                                   target_address=decoded_info["target_address"],
                                   source_address=decoded_info["source_address"],
                                   address_extension=address_extension)

    def _validate_addressing_information(self) -> None:
        """
        Validate Addressing Information parameters.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other.
        """
        if (self.rx_physical_params["target_address"] != self.tx_physical_params["source_address"]
                or self.rx_physical_params["source_address"] != self.tx_physical_params["target_address"]):
            raise InconsistentArgumentsError("Target Address and Source Address for incoming physically addressed "
                                             "CAN packets must equal Source Address and Target Address for outgoing "
                                             "physically addressed CAN packets.")
        if (self.rx_functional_params["target_address"] != self.tx_functional_params["source_address"]
                or self.rx_functional_params["source_address"] != self.tx_functional_params["target_address"]):
            raise InconsistentArgumentsError("Target Address and Source Address for incoming functionally addressed "
                                             "CAN packets must equal Source Address and Target Address for outgoing "
                                             "functionally addressed CAN packets.")

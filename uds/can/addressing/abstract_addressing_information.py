"""Abstract definition of Addressing Information handler."""

__all__ = ["AbstractCanAddressingInformation", "CANAddressingParams"]

from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from uds.addressing import AddressingType

from uds.can.addressing.addressing_format import CanAddressingFormat
from uds.addressing.abstract_addressing_information import AbstractAddressingInformation


class CANAddressingParams(TypedDict):
    """:ref:`Addressing Information <knowledge-base-n-ai>` parameters collection for a single CAN Packet."""

    addressing_format: CanAddressingFormat
    addressing_type: AddressingType
    can_id: int
    target_address: Optional[int]
    source_address: Optional[int]
    address_extension: Optional[int]


class AbstractCanAddressingInformation(AbstractAddressingInformation, ABC):
    """Abstract definition of storage for addressing related parameters for UDS entity operating on CAN bus."""

    # ADDRESSING_FORMAT_NAME: str = "addressing_format"
    # """Name of :ref:`CAN Addressing Format <knowledge-base-can-addressing>` parameter."""
    # CAN_ID_NAME: str = "can_id"
    # """Name of CAN Identifier parameter."""
    # TARGET_ADDRESS_NAME: str = "target_address"
    # """Name of Target Address parameter."""
    # SOURCE_ADDRESS_NAME: str = "source_address"
    # """Name of Source Address parameter."""
    # ADDRESS_EXTENSION_NAME: str = "address_extension"
    # """Name of Address Extension parameter."""

    class InputAIParams(TypedDict, total=False):
        """:ref:`Addressing Information <knowledge-base-n-ai>` configuration parameters."""

        can_id: int
        target_address: Optional[int]
        source_address: Optional[int]
        address_extension: Optional[int]

    class CanIdAIParams(TypedDict, total=False):
        """ref:`Addressing Information <knowledge-base-n-ai>` parameters that are carried by CAN Identifier."""

        addressing_type: Optional[AddressingType]
        target_address: Optional[int]
        source_address: Optional[int]
        priority: Optional[int]

    def __init__(self,
                 rx_physical_params: InputAIParams,
                 tx_physical_params: InputAIParams,
                 rx_functional_params: InputAIParams,
                 tx_functional_params: InputAIParams) -> None:
        """
        Configure Addresses of UDS Entity (either a server or a client) for UDS over CAN communication.

        :param rx_physical_params: Addressing parameters for incoming physically addressed communication.
        :param tx_physical_params: Addressing parameters for outgoing physically addressed communication.
        :param rx_functional_params: Addressing parameters for incoming functionally addressed communication.
        :param tx_functional_params: Addressing parameters for outgoing functionally addressed communication.
        """
        super().__init__(rx_physical_params=rx_physical_params,
                         tx_physical_params=tx_physical_params,
                         rx_functional_params=rx_functional_params,
                         tx_functional_params=tx_functional_params)

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""

    @property
    @abstractmethod
    def ai_data_bytes_number(self) -> int:
        """Number of CAN Frame data bytes that are used to carry UDS Addressing Information."""

    @staticmethod
    @abstractmethod
    def is_valid_can_id(can_id: int,
                        addressing_type: Optional[AddressingType]) -> bool:
        """
        Check whether provided CAN ID is consistent with this CAN Addressing Format.

        :param can_id: Value of CAN ID to check.
        :param addressing_type: Addressing type for which consistency to be performed.
            Leave None to skip crosscheck between CAN Identifier and Addressing Type.

        :return: True if CAN ID value is compatible with this CAN Addressing Format, False otherwise.
        """

    @classmethod
    @abstractmethod
    def decode_can_id(cls, can_id: int) -> CanIdAIParams:
        """Decode Addressing Information parameters from CAN Identifier."""

    @classmethod
    @abstractmethod
    def validate_addressing_params(cls,
                                   addressing_type: AddressingType,
                                   can_id: Optional[int] = None,
                                   target_address: Optional[int] = None,
                                   source_address: Optional[int] = None,
                                   address_extension: Optional[int] = None) -> CANAddressingParams:
        """
        Validate Addressing Information parameters of a CAN packet.

        :param addressing_type: Addressing type to validate.
        :param can_id: CAN Identifier value to validate.
        :param target_address: Target Address value to validate.
        :param source_address: Source Address value to validate.
        :param address_extension: Address Extension value to validate.

        :raise InconsistentArgumentsError: Provided values are not consistent with each other (cannot be used together)
            or with the Addressing format used.
        :raise UnusedArgumentError: Provided parameter is not supported by Addressing format used.

        :return: Normalized dictionary with the provided information.
        """

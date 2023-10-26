"""Abstract definition of Addressing Information handler."""

__all__ = ["AbstractCanAddressingInformation", "PacketAIParamsAlias"]

from typing import Optional, TypedDict
from abc import ABC, abstractmethod
from copy import deepcopy

from uds.transmission_attributes import AddressingType
from .addressing_format import CanAddressingFormat
from .frame_fields import CanIdHandler


class PacketAIParamsAlias(TypedDict):
    """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters of CAN packets stream."""

    addressing_format: CanAddressingFormat
    addressing_type: AddressingType
    can_id: int
    target_address: Optional[int]
    source_address: Optional[int]
    address_extension: Optional[int]


class AbstractCanAddressingInformation(ABC):  # TODO: consider defining abstract class for all buses
    """Abstract definition of CAN Entity (either server or client) Addressing Information."""

    ADDRESSING_FORMAT_NAME: str = "addressing_format"
    """Name of :ref:`CAN Addressing Format <knowledge-base-can-addressing>` parameter in Addressing Information."""
    ADDRESSING_TYPE_NAME: str = CanIdHandler.ADDRESSING_TYPE_NAME
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` parameter in Addressing Information."""
    CAN_ID_NAME: str = "can_id"
    """Name of CAN Identifier parameter in Addressing Information."""
    TARGET_ADDRESS_NAME: str = CanIdHandler.TARGET_ADDRESS_NAME
    """Name of Target Address parameter in Addressing Information."""
    SOURCE_ADDRESS_NAME: str = CanIdHandler.SOURCE_ADDRESS_NAME
    """Name of Source Address parameter in Addressing Information."""
    ADDRESS_EXTENSION_NAME: str = "address_extension"
    """Name of Address Extension parameter in Addressing Information."""

    AI_DATA_BYTES_NUMBER: int
    """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    class InputAIParamsAlias(TypedDict, total=False):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` configuration parameters."""

        can_id: int
        target_address: int
        source_address: int
        address_extension: int

    def __init__(self,
                 rx_physical: InputAIParamsAlias,
                 tx_physical: InputAIParamsAlias,
                 rx_functional: InputAIParamsAlias,
                 tx_functional: InputAIParamsAlias) -> None:
        """
        Configure Addressing Information of a CAN Entity.

        :param rx_physical: Addressing Information parameters used for incoming physically addressed communication.
        :param tx_physical: Addressing Information parameters used for outgoing physically addressed communication.
        :param rx_functional: Addressing Information parameters used for incoming functionally addressed communication.
        :param tx_functional: Addressing Information parameters used for outgoing functionally addressed communication.
        """
        self.rx_packets_physical_ai = rx_physical  # type: ignore
        self.tx_packets_physical_ai = tx_physical  # type: ignore
        self.rx_packets_functional_ai = rx_functional  # type: ignore
        self.tx_packets_functional_ai = tx_functional  # type: ignore

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormat:
        """CAN Addressing format used."""

    @property
    def rx_packets_physical_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of incoming physically addressed CAN packets."""
        return deepcopy(self.__rx_packets_physical_ai)

    @rx_packets_physical_ai.setter
    def rx_packets_physical_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of incoming physically addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.__rx_packets_physical_ai: PacketAIParamsAlias \
            = self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL}, **value)

    @property
    def tx_packets_physical_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of outgoing physically addressed CAN packets."""
        return deepcopy(self.__tx_packets_physical_ai)

    @tx_packets_physical_ai.setter
    def tx_packets_physical_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of outgoing physically addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.__tx_packets_physical_ai: PacketAIParamsAlias \
            = self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL}, **value)

    @property
    def rx_packets_functional_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of incoming functionally addressed CAN packets."""
        return deepcopy(self.__rx_packets_functional_ai)

    @rx_packets_functional_ai.setter
    def rx_packets_functional_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of incoming functionally addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.__rx_packets_functional_ai: PacketAIParamsAlias \
            = self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL}, **value)

    @property
    def tx_packets_functional_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of outgoing functionally addressed CAN packets."""
        return deepcopy(self.__tx_packets_functional_ai)

    @tx_packets_functional_ai.setter
    def tx_packets_functional_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of outgoing functionally addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """
        self.__tx_packets_functional_ai: PacketAIParamsAlias \
            = self.validate_packet_ai(**{self.ADDRESSING_TYPE_NAME: AddressingType.FUNCTIONAL}, **value)

    @classmethod
    @abstractmethod
    def validate_packet_ai(cls,
                           addressing_type: AddressingType,
                           can_id: Optional[int] = None,
                           target_address: Optional[int] = None,
                           source_address: Optional[int] = None,
                           address_extension: Optional[int] = None) -> PacketAIParamsAlias:
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

"""Abstract definition of Addressing Information handler."""

__all__ = ["AbstractAddressingInformation"]

from typing import TypedDict
from abc import ABC, abstractmethod

from uds.utilities import RawByte
from uds.transmission_attributes import AddressingTypeAlias
from .addressing_format import CanAddressingFormatAlias
from .frame_fields import CanIdHandler


class AbstractAddressingInformation(ABC):
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

    class InputAIParamsAlias(TypedDict, total=False):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` configuration parameters."""

        can_id: int
        target_address: RawByte
        source_address: RawByte
        address_extension: RawByte

    class _OptionalPacketAIParamsAlias(TypedDict, total=False):
        """Alias of optional :ref:`Addressing Information <knowledge-base-n-ai>` parameters of CAN packets stream."""

        target_address: RawByte
        source_address: RawByte
        address_extension: RawByte

    class PacketAIParamsAlias(_OptionalPacketAIParamsAlias, total=True):
        """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters of CAN packets stream."""

        addressing_format: CanAddressingFormatAlias
        addressing_type: AddressingTypeAlias
        can_id: int

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
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""

    @property
    @abstractmethod
    def ai_data_bytes_number(self) -> int:
        """Get number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    @abstractmethod
    def rx_packets_physical_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of incoming physically addressed CAN packets."""

    @rx_packets_physical_ai.setter
    def rx_packets_physical_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of incoming physically addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """

    @property
    @abstractmethod
    def tx_packets_physical_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of outgoing physically addressed CAN packets."""

    @tx_packets_physical_ai.setter
    def tx_packets_physical_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of outgoing physically addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """

    @property
    @abstractmethod
    def rx_packets_functional_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of incoming functionally addressed CAN packets."""

    @rx_packets_functional_ai.setter
    def rx_packets_functional_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of incoming functionally addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """

    @property
    @abstractmethod
    def tx_packets_functional_ai(self) -> PacketAIParamsAlias:
        """Addressing Information parameters of outgoing functionally addressed CAN packets."""

    @tx_packets_functional_ai.setter
    def tx_packets_functional_ai(self, value: InputAIParamsAlias):
        """
        Set Addressing Information parameters of outgoing functionally addressed CAN packets.

        :param value: Addressing Information parameters to set.
        """

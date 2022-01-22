"""Abstract definition of Addressing Information handler."""

__all__ = ["AbstractAddressingInformation"]

from typing import Optional, Union, Literal, Dict
from abc import ABC, abstractmethod

from uds.transmission_attributes import AddressingTypeAlias
from .addressing_format import CanAddressingFormatAlias
from .frame_fields import CanIdHandler


class AbstractAddressingInformation(ABC):
    """Abstract definition of CAN Entity (either server or client) Addressing Information."""

    ADDRESSING_FORMAT_NAME = "addressing_format"
    """Name of :ref:`CAN Addressing Format <knowledge-base-can-addressing>` parameter in Addressing Information."""
    ADDRESSING_TYPE_NAME = CanIdHandler.ADDRESSING_TYPE_NAME
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` parameter in Addressing Information."""
    CAN_ID_NAME = "can_id"
    """Name of CAN Identifier parameter in Addressing Information."""
    TARGET_ADDRESS_NAME = CanIdHandler.TARGET_ADDRESS_NAME
    """Name of Target Address parameter in Addressing Information."""
    SOURCE_ADDRESS_NAME = CanIdHandler.SOURCE_ADDRESS_NAME
    """Name of Source Address parameter in Addressing Information."""
    ADDRESS_EXTENSION_NAME = "address_extension"
    """Name of Address Extension parameter in Addressing Information."""

    AIParamsAlias = Dict[Literal[ADDRESSING_FORMAT_NAME, ADDRESSING_TYPE_NAME, CAN_ID_NAME,
                                 TARGET_ADDRESS_NAME, SOURCE_ADDRESS_NAME, ADDRESS_EXTENSION_NAME],
                         Optional[Union[AddressingTypeAlias, CanAddressingFormatAlias, int]]]
    """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters."""

    def __init__(self, rx_physical: dict, tx_physical: dict, rx_functional: dict, tx_functional: dict) -> None:
        """
        Configure Addressing Information of a CAN Entity.

        :param rx_physical: Addressing Information parameters used for incoming physically addressed communication.
        :param tx_physical: Addressing Information parameters used for outgoing physically addressed communication.
        :param rx_functional: Addressing Information parameters used for incoming functionally addressed communication.
        :param tx_functional: Addressing Information parameters used for outgoing functionally addressed communication.
        """
        self.rx_packets_physical_ai = rx_physical
        self.tx_packets_physical_ai = tx_physical
        self.rx_packets_functional_ai = rx_functional
        self.tx_packets_functional_ai = tx_functional

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""

    @property
    @abstractmethod
    def ai_data_bytes_number(self) -> int:
        """Number of CAN Frame data bytes that are used to carry Addressing Information."""

    @property
    @abstractmethod
    def rx_packets_physical_ai(self) -> AIParamsAlias:
        """Addressing Information parameters of incoming physically addressed CAN packets."""

    @property
    @abstractmethod
    def tx_packets_physical_ai(self) -> AIParamsAlias:
        """Addressing Information parameters of outgoing physically addressed CAN packets."""

    @property
    @abstractmethod
    def rx_packets_functional_ai(self) -> AIParamsAlias:
        """Addressing Information parameters of incoming functionally addressed CAN packets."""

    @property
    @abstractmethod
    def tx_packets_functional_ai(self) -> AIParamsAlias:
        """Addressing Information parameters of outgoing functionally addressed CAN packets."""

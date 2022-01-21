"""Implementation of containers for Addressing Information."""

__all__ = ["AbstractCanEntityAI",  "CanEntityNormal11bitAI", "CanEntityNormalFixedAI", "CanEntityExtendedAI",
           "CanEntityMixed11bitAI", "CanEntityMixed29bitAI", "get_can_entity_ai"]

from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, Literal, Any

from uds.transmission_attributes import AddressingType, AddressingTypeAlias
from uds.packet import AbstractCanPacketContainer
from .addressing_format import CanAddressingFormat, CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler
from .frame_fields import CanIdHandler


class AbstractCanEntityAI(ABC):
    """Abstract definition of CAN Entity (either server or client) Addressing Information"""

    ADDRESSING_FORMAT_NAME = "addressing_format"
    """Name of :ref:`CAN Addressing Format <knowledge-base-can-addressing>` parameter in Addressing Information."""
    ADDRESSING_TYPE_NAME = CanAddressingInformationHandler.ADDRESSING_TYPE_NAME
    """Name of :ref:`Addressing Type <knowledge-base-can-addressing>` parameter in Addressing Information."""
    CAN_ID_NAME = "can_id"
    """Name of CAN Identifier parameter in Addressing Information."""
    TARGET_ADDRESS_NAME = CanAddressingInformationHandler.TARGET_ADDRESS_NAME
    """Name of Target Address parameter in Addressing Information."""
    SOURCE_ADDRESS_NAME = CanAddressingInformationHandler.SOURCE_ADDRESS_NAME
    """Name of Source Address parameter in Addressing Information."""
    ADDRESS_EXTENSION_NAME = CanAddressingInformationHandler.ADDRESS_EXTENSION_NAME
    """Name of Address Extension parameter in Addressing Information."""

    AIParamsAlias = Dict[Literal[ADDRESSING_FORMAT_NAME, ADDRESSING_TYPE_NAME, CAN_ID_NAME,
                                 TARGET_ADDRESS_NAME, SOURCE_ADDRESS_NAME, ADDRESS_EXTENSION_NAME],
                         Optional[Union[AddressingTypeAlias, CanAddressingFormatAlias, int]]]
    """Alias of :ref:`Addressing Information <knowledge-base-n-ai>` parameters."""

    def __init__(self, physical_ai: Dict[str, Any], functional_ai: Dict[str, Any]) -> None:
        """
        Configure Addressing Information of UDS CAN Entity.

        :param physical_ai: Addressing Information parameters used for physically addressed communication.
        :param functional_ai: Addressing Information parameters used ot functionally addressed communication.
        """
        self.set_physical_ai(**physical_ai)
        self.set_functional_ai(**functional_ai)

    @abstractmethod
    def set_physical_ai(self, **kwargs: Any) -> None:
        """
        Set Addressing Information parameters for physically addressed communication.

        :param kwargs: Values of Addressing Information parameters.
        """

    @abstractmethod
    def set_functional_ai(self, **kwargs: Any) -> None:
        """
        Set Addressing Information parameters for functionally addressed communication.

        :param kwargs: Values of Addressing Information parameters.
        """

    def is_packet_targeting_entity(self, can_packet: AbstractCanPacketContainer) -> bool:
        """
        Check if provided CAN packet targets this CAN entity.

        :param can_packet: CAN packet to check.

        :raise TypeError: Provided value is not CAN Packet.
        :raise NotImplementedError: CAN Packet using unknown addressing was provided.

        :return: True if provided CAN Packet targets this CAN entity, False otherwise.
        """
        if not isinstance(can_packet, AbstractCanPacketContainer):
            raise TypeError(f"Provided value does not carry CAN Packet. Actual type: {type(can_packet)}")
        if can_packet.addressing_type == AddressingType.PHYSICAL:
            receiving_ai_params = self.receiving_physical_ai
        elif can_packet.addressing_type == AddressingType.FUNCTIONAL:
            receiving_ai_params = self.receiving_functional_ai
        else:
            raise NotImplementedError(f"CAN Packet using unknown addressing type value was provided: "
                                      f"{can_packet.addressing_type}")
        return all(getattr(can_packet, ai_param_name) == ai_param_value
                   for ai_param_name, ai_param_value in receiving_ai_params.items())

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""

    @property
    @abstractmethod
    def receiving_physical_ai(self) -> AIParamsAlias:  # TODO: rename
        """
        Addressing Information parameters of incoming physically addressed communication.

        Physically addressed CAN packets that target this entity must use these parameters.
        """

    @property
    @abstractmethod
    def transmitting_physical_ai(self) -> AIParamsAlias:  # TODO: rename
        """
        Addressing Information parameters of outgoing physically addressed communication.

        Physically addressed CAN packets that are transmitted by this entity must use these parameters.
        """

    @property
    @abstractmethod
    def receiving_functional_ai(self) -> AIParamsAlias:  # TODO: rename
        """
        Addressing Information parameters of incoming functionally addressed communication.

        Functionally addressed CAN packets that target this entity must use these parameters.
        """

    @property
    @abstractmethod
    def transmitting_functional_ai(self) -> AIParamsAlias:
        """
        Addressing Information parameters of outgoing functionally addressed communication.

        Functionally addressed CAN packets that are transmitted by this entity must use these parameters.
        """


class CanEntityNormal11bitAI(AbstractCanEntityAI):
    """Addressing Information of CAN Entity which uses Normal 11-bit Addressing format."""

    AIArgsAlias = Dict[Literal["rx_can_id", "tx_can_id"], int]

    def __init__(self, physical_ai: AIArgsAlias, functional_ai: AIArgsAlias) -> None:
        """
        Configure Addressing Information of UDS CAN Entity.

        :param physical_ai: Addressing Information parameters used for physically addressed communication.
        :param functional_ai: Addressing Information parameters used ot functionally addressed communication.
        """
        # set initial values
        self.__physical_rx_can_id: int = None  # type: ignore
        self.__physical_tx_can_id: int = None  # type: ignore
        self.__functional_rx_can_id: int = None  # type: ignore
        self.__functional_tx_can_id: int = None  # type: ignore
        # call proper init
        super().__init__(physical_ai=physical_ai, functional_ai=functional_ai)

    def set_physical_ai(self, rx_can_id: int, tx_can_id: int) -> None:
        """
        Set Addressing Information parameters for physically addressed communication.

        :param rx_can_id: CAN Identifier of incoming physically addressed CAN packets.
        :param tx_can_id: CAN Identifier of outgoing physically addressed CAN packets.

        :raise ValueError: Invalid CAN ID values were provided.
        """
        if not CanIdHandler.is_normal_11bit_addressed_can_id(rx_can_id):
            raise ValueError(f"Provided `rx_can_id` is not 11-bit CAN ID. Actual value: {rx_can_id}")
        if not CanIdHandler.is_normal_11bit_addressed_can_id(tx_can_id):
            raise ValueError(f"Provided `tx_can_id` is not 11-bit CAN ID. Actual value: {tx_can_id}")
        if rx_can_id in {tx_can_id, self.__functional_rx_can_id, self.__functional_tx_can_id}:
            raise ValueError(f"Provided `rx_can_id` is used more than once.")
        if tx_can_id in {rx_can_id, self.__functional_rx_can_id, self.__functional_tx_can_id}:
            raise ValueError(f"Provided `tx_can_id` is used more than once.")
        self.__physical_rx_can_id = rx_can_id
        self.__physical_tx_can_id = tx_can_id

    def set_functional_ai(self, rx_can_id: int, tx_can_id: int) -> None:
        """
        Set Addressing Information parameters for functionally addressed communication.

        :param rx_can_id: CAN Identifier of incoming functionally addressed CAN packets.
        :param tx_can_id: CAN Identifier of outgoing functionally addressed CAN packets.

        :raise ValueError: Invalid CAN ID values were provided.
        """
        if not CanIdHandler.is_normal_11bit_addressed_can_id(rx_can_id):
            raise ValueError(f"Provided `rx_can_id` is not 11-bit CAN ID. Actual value: {rx_can_id}")
        if not CanIdHandler.is_normal_11bit_addressed_can_id(tx_can_id):
            raise ValueError(f"Provided `tx_can_id` is not 11-bit CAN ID. Actual value: {tx_can_id}")
        if rx_can_id in {tx_can_id, self.__physical_rx_can_id, self.__physical_tx_can_id}:
            raise ValueError(f"Provided `rx_can_id` is used more than once.")
        if tx_can_id in {rx_can_id, self.__physical_rx_can_id, self.__physical_tx_can_id}:
            raise ValueError(f"Provided `tx_can_id` is used more than once.")
        self.__functional_rx_can_id = rx_can_id
        self.__functional_tx_can_id = tx_can_id

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""
        return CanAddressingFormat.NORMAL_11BIT_ADDRESSING

    @property
    def receiving_physical_ai(self) -> AbstractCanEntityAI.AIParamsAlias:
        """
        Addressing Information parameters of incoming physically addressed communication.

        Physically addressed CAN packets that target this entity must use these parameters.
        """
        return {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,
            self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            self.CAN_ID_NAME: self.__physical_rx_can_id,
            self.TARGET_ADDRESS_NAME: None,
            self.SOURCE_ADDRESS_NAME: None,
            self.ADDRESS_EXTENSION_NAME: None,
        }

    @property
    def transmitting_physical_ai(self) -> AbstractCanEntityAI.AIParamsAlias:
        """
        Addressing Information parameters of outgoing physically addressed communication.

        Physically addressed CAN packets that are transmitted by this entity must use these parameters.
        """
        return {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,
            self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            self.CAN_ID_NAME: self.__physical_tx_can_id,
            self.TARGET_ADDRESS_NAME: None,
            self.SOURCE_ADDRESS_NAME: None,
            self.ADDRESS_EXTENSION_NAME: None,
        }

    @property
    def receiving_functional_ai(self) -> AbstractCanEntityAI.AIParamsAlias:
        """
        Addressing Information parameters of incoming functionally addressed communication.

        Functionally addressed CAN packets that target this entity must use these parameters.
        """
        return {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,
            self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            self.CAN_ID_NAME: self.__functional_rx_can_id,
            self.TARGET_ADDRESS_NAME: None,
            self.SOURCE_ADDRESS_NAME: None,
            self.ADDRESS_EXTENSION_NAME: None,
        }

    @property
    def transmitting_functional_ai(self) -> AbstractCanEntityAI.AIParamsAlias:
        """
        Addressing Information parameters of outgoing functionally addressed communication.

        Functionally addressed CAN packets that are transmitted by this entity must use these parameters.
        """
        return {
            self.ADDRESSING_FORMAT_NAME: self.addressing_format,
            self.ADDRESSING_TYPE_NAME: AddressingType.PHYSICAL,
            self.CAN_ID_NAME: self.__functional_tx_can_id,
            self.TARGET_ADDRESS_NAME: None,
            self.SOURCE_ADDRESS_NAME: None,
            self.ADDRESS_EXTENSION_NAME: None,
        }


class CanEntityNormalFixedAI(AbstractCanEntityAI):
    """Addressing Information of CAN Entity which uses Normal Fixed Addressing format."""


class CanEntityExtendedAI(AbstractCanEntityAI):
    """Addressing Information of CAN Entity which uses Extended Addressing format."""


class CanEntityMixed11bitAI(AbstractCanEntityAI):
    """Addressing Information of CAN Entity which uses Mixed 11-bit Addressing format."""


class CanEntityMixed29bitAI(AbstractCanEntityAI):
    """Addressing Information of CAN Entity which uses Mixed 29-bit Addressing format."""


def get_can_entity_ai(addressing_format: CanAddressingFormatAlias,
                      physical_ai: Dict[str, Any],
                      functional_ai: Dict[str, Any]) -> AbstractCanEntityAI:
    # TODO
    ...

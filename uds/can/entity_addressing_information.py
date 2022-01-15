from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, Literal, Tuple, Any

from uds.transmission_attributes import AddressingTypeAlias
from uds.packet import AbstractCanPacketContainer
from .addressing_format import CanAddressingFormatAlias
from .addressing_information import CanAddressingInformationHandler


class AbstractCanEntityAI(ABC):
    """Abstract definition of CAN Entity (either server or client) Addressing Information"""

    def __init__(self, physical_ai: Dict[str, Any], functional_ai: Dict[str, Any]) -> None:
        """
        Configure Addressing Information of UDS CAN Entity.

        :param physical_ai: Addressing Information parameters used for physically addressed communication.
        :param functional_ai: Addressing Information parameters used ot functionally addressed communication.
        """
        # TODO

    def set_physical_ai(self, **kwargs: Any) -> None:
        """
        Set Addressing Information parameters for physically addressed communication.

        :param kwargs: Values of Addressing Information parameters.
        """
        # TODO

    def set_functional_ai(self, **kwargs: Any) -> None:
        """
        Set Addressing Information parameters for functionally addressed communication.

        :param kwargs: Values of Addressing Information parameters.
        """
        # TODO

    def check_packet_targets_entity(self, can_packet: AbstractCanPacketContainer) -> Optional[AddressingTypeAlias]:
        """
        Check if provided CAN packet targets this CAN entity.

        :param can_packet: CAN packet to check.

        :return: Either Addressing Type that was used to target the entity or None if the packet targets another entity.
        """
        # TODO

    @property
    @abstractmethod
    def addressing_format(self) -> CanAddressingFormatAlias:
        """CAN Addressing format used."""

    @property
    def receiving_physical_ai(self) -> :
        """
        Addressing Information parameters of incoming physically addressed communication.

        Physically addressed CAN packets that target this entity must use these parameters.
        """
        # TODO

    @property
    def transmitting_physical_ai(self):
        """
        Addressing Information parameters of outgoing physically addressed communication.

        Physically addressed CAN packets that are transmitted by this entity must use these parameters.
        """
        # TODO

    @property
    def receiving_functional_ai(self):
        """
        Addressing Information parameters of incoming functionally addressed communication.

        Functionally addressed CAN packets that target this entity must use these parameters.
        """
        # TODO

    @property
    def transmitting_functional_ai(self):
        """
        Addressing Information parameters of outgoing functionally addressed communication.

        Functionally addressed CAN packets that are transmitted by this entity must use these parameters.
        """
        # TODO


class CanEntityNormal11bitAI(AbstractCanEntityAI):

    def set_physical_ai(self, rx_can_id: int, tx_can_id: int) -> None:
        """
        Set Addressing Information parameters for physically addressed communication.

        :param rx_can_id: CAN Identifier of incoming physically addressed CAN packets.
        :param tx_can_id: CAN Identifier of outgoing physically addressed CAN packets.
        """

    def set_functional_ai(self, rx_can_id: int, tx_can_id: int) -> None:
        """
        Set Addressing Information parameters for physically addressed communication.

        :param rx_can_id: CAN Identifier of incoming CAN packets.
        :param tx_can_id: CAN Identifier of outgoing CAN packets.
        """

    @property
    def addressing_format(self) -> CanAddressingFormatAlias:
        # TODO
        ...


class CanEntityNormalFixedAI(AbstractCanEntityAI):
    ...


class CanEntityExtendedAI(AbstractCanEntityAI):
    ...


class CanEntityMixed11bitAI(AbstractCanEntityAI):
    ...


class CanEntityMixed29bitAI(AbstractCanEntityAI):
    ...


def get_can_entity_ai(addressing_format: CanAddressingFormatAlias,
                      physical_ai: dict,
                      functional_ai: dict) -> AbstractCanEntityAI:
    ...

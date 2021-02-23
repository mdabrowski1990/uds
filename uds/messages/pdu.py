"""Common implementation of UDS PDU (Protocol Data Unit) for all bus types."""

__all__ = ["AbstractPDU"]

from typing import Optional
from abc import ABC, abstractmethod

from .addressing import AddressingType


class AbstractPDU(ABC):
    """Abstract definition of Protocol Data Unit."""

    @abstractmethod
    def __init__(self, pdu_type, **kwargs) -> None:  # noqa TODO: add params and remove noqa
        """Create storage related to a single PDU."""

    @property
    @abstractmethod
    def addressing(self) -> Optional[AddressingType]:
        """
        Get addressing type over which this PDU was transmitted/received.

        :return: Addressing over which the PDU was transmitted/received. None if PDU was not transmitted/received.
        """

    @property
    @abstractmethod  # noqa  TODO: update and remove noqa
    def pdu_type(self):
        """Getter of this PDU type."""

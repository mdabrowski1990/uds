"""Common implementation of UDS PDU (Protocol Data Unit) for all bus types."""

__all__ = ["AbstractPDU"]

from typing import Optional
from abc import ABC, abstractmethod
from enum import Enum

from .addressing import AddressingType


class AbstractPDU(ABC):
    """Abstract definition of Protocol Data Unit."""

    @property
    @abstractmethod
    def addressing(self) -> Optional[AddressingType]:
        """
        Get addressing type over which this PDU was transmitted/received.

        :return: Addressing over which the PDU was transmitted/received. None if PDU was not transmitted/received.
        """

    @property  # noqa
    @abstractmethod
    def pdu_type(self) -> Enum:
        """Getter of this PDU type."""

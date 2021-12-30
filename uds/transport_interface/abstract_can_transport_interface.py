"""Abstract definition of UDS Transport Interface for CAN bus."""

from typing import Optional, Tuple, Any
from abc import abstractmethod

from .abstract_transport_interface import AbstractTransportInterface


class AbstractCanTransportInterface(AbstractTransportInterface):
    """
    Abstract definition of Transport Interface for CAN bus.

    CAN Transport Interfaces are meant to handle middle layers (Transport and Network) for CAN bus.
    """

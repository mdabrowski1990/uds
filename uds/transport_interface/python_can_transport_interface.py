"""Implementation of Transport Interfaces for CAN bus handled by python-can."""

__all__ = ["PyCanTransportInterface"]


from can import BusABC

from .abstract_transport_interface import AbstractTransportInterface


class PyCanTransportInterface(AbstractTransportInterface):
    """
    Transport Interface for CAN that is compatible with python-can.

    Documentation for python-can: https://python-can.readthedocs.io/
    """

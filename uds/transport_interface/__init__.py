"""
Abstract definition for Transport Interfaces.

Transport Interfaces are meant to handle following UDS protocol layers (according to OSI model):
 - Transport (4th)
 - Network (3rd)
 - Data (2nd)
 - Physical (1st)

Each bus (e.g. CAN, LIN, Ethernet) that support UDS requires implementation of:
 - TransportInterfaceClient
 - TransportInterfaceServer
"""

from .common import UdsSegmentationError
from .client import TransportInterfaceClient, UdsSequenceError
from .server import TransportInterfaceServer

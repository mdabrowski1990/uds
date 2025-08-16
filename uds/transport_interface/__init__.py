"""
A sub-package with definition of UDS middle layers (Transport and Network).

It provides tools and base for configurable Transport Interfaces. Transport Interfaces features:
 - transmitting and receiving packets
 - transmitting and receiving UDS messages
 - storing historic information about transmitted and received packets
 - storing historic information about transmitted and received UDS messages
 - managing Transport and Network layer errors
"""

from .abstract_transport_interface import AbstractTransportInterface

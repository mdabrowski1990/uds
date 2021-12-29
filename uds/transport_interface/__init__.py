"""
A subpackage with implementation for UDS middle layers (Transport and Network).

It provides configurable Transport Interfaces for:
 - transmitting and receiving UDS packets
 - transmitting and receiving UDS messages
 - storing historic information about transmitted and received UDS packets
 - storing historic information about transmitted and received UDS messages
 - managing Transport and Network layer errors
"""

from .abstract_transport_interface import AbstractTransportInterface

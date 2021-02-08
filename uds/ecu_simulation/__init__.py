"""
Module that contains implementation of classes that are able to simulate UDS communication of all UDS node types.

Client enables to simulate UDS client's communication (sends request, received responses).
UDS client is usually diagnostic tester, but it might also be gateway node (e.g. LIN master that received request on
a backbone bus).

Server enables to simulate UDS server's communication (receives requests, sends responses).
UDS server is always vehicle's on-board ECU (an electronic control unit
"""


__all__ = ["Client", "Server", "ResponseManager"]


from .client import Client
from .server import Server, ResponseManager

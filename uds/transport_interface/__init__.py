"""
Package with abstraction layer for Transport Interface.

Transport Interface is meant to handle UDS layer 4 (Transport) and all below it.
There are many buses that supports UDS and each of them has special implementation, therefore there are many
ISO standards that describes desired behavior such as:
- ISO 15765-2 (DoCAN)
- ISO 13400-2 and 13400-3 (DoIP)
"""

from .client_side import AbstractTIClient
from .server_side import AbstractTIServer

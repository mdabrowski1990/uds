"""
Package with abstraction layer for Transport Protocol Interface definition.

Transport Protocol Interface is meant to handle UDS protocol 4 (Transport Protocol) and other below it
(directly or indirectly).
There are many buses that supports UDS and each of them has special implementation for these layers, e.g.
- DoCAN (ISO 15765-2)
- DoLIN
- DoIP (ISO 13400-2 and 13400-3)
"""

__all__ = ["AbstractTPInterface"]

from .abstract import AbstractTPInterface

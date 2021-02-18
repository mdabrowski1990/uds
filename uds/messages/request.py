"""Module with UDS request messages implementation."""

__all__ = ["UdsRequest"]

from .base_message import UdsMessage


class UdsRequest(UdsMessage):
    """
    Storage for diagnostic requests information.

    UDS request is always sent by client and received by server.
    """

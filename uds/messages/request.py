"""Module with UDS request messages implementation."""

__all__ = ["UdsRequest"]

from .uds_message import UdsMessage


class UdsRequest(UdsMessage):
    """
    Storage for a single diagnostic request message.

    UDS request is always sent by a client and received by a server.
    """

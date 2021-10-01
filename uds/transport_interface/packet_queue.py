"""Module with common implementation of UDS Packets queues."""

__all__ = ["ReceivedPacketsQueue"]

from typing import Optional
from abc import ABC, abstractmethod
from asyncio import Queue

from uds.utilities import TimeMilliseconds
from uds.messages import AbstractUdsPacket, AbstractUdsPacketRecord


class ReceivedPacketsQueue:
    """Queue for storing received packets."""

    def __init__(self, packet_class: type = AbstractUdsPacketRecord) -> None:
        """
        Create a queue as a storage for received packets.

        :param packet_class: A class that defines UDS packets type that is accepted by this queue.
            One can use this parameter to restrict packets managed by this queue.

        :raise TypeError: Provided packet_class is not a class that inherits after
            :class:"uds.messages.uds_packet.AbstractUdsPacketRecord".
        """
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    async def get_packet(self) -> AbstractUdsPacketRecord:
        raise NotImplementedError

    def packet_handled(self) -> None:
        raise NotImplementedError

    async def put_packet(self, packet: AbstractUdsPacketRecord) -> None:
        raise NotImplementedError


"""Abstract definition of UDS Packet queue."""

__all__ = ["AbstractPacketsQueue"]

from typing import NoReturn
from abc import ABC, abstractmethod

from uds.packet import PacketAlias


class AbstractPacketsQueue(ABC):
    """Abstract definition of a queue with UDS packets."""

    @abstractmethod
    def __init__(self, packet_class: type) -> None:  # noqa: F841
        """
        Create a queue for storing UDS packets.

        :param packet_class: A class that defines UDS packets type which shall be accepted by this queue.
            This parameter is meant to restrict types of packets that are managed by this queue.

        :raise TypeError: Provided packet_class argument is not a class that inherits after
            :class:"~uds.packet.abstract_packet.AbstractUdsPacket" or
            :class:"~uds.packet.abstract_packet.AbstractUdsPacketRecord".
        """
        raise NotImplementedError

    def __del__(self) -> NoReturn:
        """
        Delete the queue safely.

        To satisfy safe closure of tasks using the queue:
         - prevent new tasks creations
         - await (till timeout) for closure of already started tasks
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Get number of packets that are currently stored by the queue."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        :return: True if queue is empty (does not contain any packets), False otherwise.
        """
        raise NotImplementedError

    def mark_task_done(self) -> None:
        """
        Inform that a task related to one packet was completed.

        This method is used for monitoring tasks so they can be completed safely and closed quietly.
        """
        raise NotImplementedError

    def block(self) -> None:
        """Block from putting new packets to the queue until all packets are gotten and processed."""
        raise NotImplementedError

    def clear(self) -> None:
        """Delete all packets stored by the queue."""
        raise NotImplementedError

    @abstractmethod
    async def get_packet(self) -> PacketAlias:
        """
        Get the next packet from the queue.

        :return: The next packet in the queue.
        """

    @abstractmethod
    async def put_packet(self, packet: PacketAlias) -> None:
        """
        Add a packet to the queue.

        :param packet: A packet to add to the queue.
        """

"""Module with common implementation of UDS Packets queues."""

__all__ = ["ReceivedPacketsQueue"]

from typing import NoReturn

from uds.messages import AbstractUdsPacketRecord


class ReceivedPacketsQueue:
    """Queue for storing received packets."""

    def __init__(self, packet_class: type = AbstractUdsPacketRecord) -> None:  # noqa: F841
        """
        Create a queue as a storage for received packets.

        :param packet_class: A class that defines UDS packets type that is accepted by this queue.
            One can use this parameter to restrict packets managed by this queue.

        :raise TypeError: Provided packet_class is not a class that inherits after
            :class:"uds.messages.uds_packet.AbstractUdsPacketRecord".
        """
        raise NotImplementedError

    def __del__(self) -> NoReturn:
        """Delete the object and safely stop all queue threads."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Get number of packets that are currently stored in the queue."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        :return: True if queue is empty (does not contain any packets), False otherwise.
        """
        raise NotImplementedError

    def packet_task_done(self) -> None:
        """
        Inform that a task related to one packet was completed.

        This method is used during closing all tasks safely and quietly.
        """
        raise NotImplementedError

    async def get_packet(self) -> AbstractUdsPacketRecord:
        """
        Get the next received packet from the queue.

        Note: If called, when there are no packets in the queue, then execution would await until another packet
            is received.

        :return: The next received packet.
        """
        raise NotImplementedError

    async def put_packet(self, packet: AbstractUdsPacketRecord) -> None:  # noqa: F841
        """
        Add a packet (that was just received) to the end of the queue.

        :param packet: A packet that was just received.
        """
        raise NotImplementedError

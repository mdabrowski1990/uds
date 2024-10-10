"""
A subpackage with tools for handling UDS packets.

It provides tools for:
 - data definitions for various UDS packet fields (:ref:`N_AI <knowledge-base-n-ai>`,
   :ref:`N_PCI <knowledge-base-n-pci>`, :ref:`N_Data <knowledge-base-n-data>`)
 - creating new packets
 - storing historic information about packets that were either received or transmitted
"""

from .abstract_packet import (
    AbstractUdsPacket,
    AbstractUdsPacketContainer,
    AbstractUdsPacketRecord,
    PacketsContainersSequence,
    PacketsRecordsSequence,
    PacketsRecordsTuple,
    PacketsTuple,
)
from .abstract_packet_type import AbstractUdsPacketType
from .can import AbstractCanPacketContainer, CanPacket, CanPacketRecord, CanPacketType

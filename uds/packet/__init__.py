"""
A subpackage with tools for handling UDS packets.

It provides tools for:
 - data definitions for various UDS packet fields (:ref:`N_AI <knowledge-base-n-ai>`,
   :ref:`N_PCI <knowledge-base-n-pci>`, :ref:`N_Data <knowledge-base-n-data>`)
 - creating new packets
 - storing historic information about packets that were either received or transmitted
"""

from .abstract_packet import AbstractUdsPacketType, AbstractUdsPacket, AbstractUdsPacketRecord, \
    PacketAlias, PacketsTuple, PacketsSequence, \
    PacketsDefinitionTuple, PacketsDefinitionSequence, \
    PacketsRecordsTuple, PacketsRecordsSequence, \
    PacketTypesTuple  # TODO: review

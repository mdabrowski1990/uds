.. _implementation-uds-packet:

UDS Packets
===========
Common implementation of UDS packets is located in :mod:`uds.packet` sub-package.

:ref:`UDS packets <knowledge-base-uds-packet>` implementation is divided into three parts:
 - `UDS Packet Type`_ - enums with :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>`
   values definitions
 - `UDS Packet`_ - storages for a temporary :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`
   definition on the user side
 - `UDS Packet Record`_ - storages for historic information of a :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`
   that was either received or transmitted


UDS Packet Type
---------------
UDS packet types are supposed to be understood as values of
:ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` that informs about format and information
carried in :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-n-pdu>`.

Supported values of UDS packet types are defined in following enum classes:
 - `AbstractUdsPacketType`_


AbstractUdsPacketType
`````````````````````
:class:`~uds.packet.abstract_packet.AbstractUdsPacketType` class is an empty enum that is a parent class for all concrete
UDS packet types enum classes. It **provides common API and values restriction** (UDS packet type values must be
4-bit integer) **for all children classes**.

.. warning:: A **user shall not use** :class:`~uds.packet.abstract_packet.AbstractUdsPacketType` **directly**,
    but one is able (and encouraged) to use :class:`~uds.packet.abstract_packet.AbstractUdsPacketType` implementation
    with any of its children classes.

Methods implemented in :class:`~uds.packet.abstract_packet.AbstractUdsPacketType` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
 - :meth:`~uds.utilities.enums.ExtendableEnum.add_member`
 - :meth:`~uds.packet.abstract_packet_type.AbstractUdsPacketType.is_initial_packet_type` - abstract

UDS Packet
----------
:ref:`UDS packets <knowledge-base-uds-packet>` **differs for each communication bus**, therefore
**multiple classes implementing them are defined**.
Each UDS packet class provides containers for :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`
information that are specific for a communication bus for which this class is relevant.
**Objects of UDS packet classes might be used to execute complex operations** (provided in other subpackages) such as
packets transmission or :ref:`desegmentation <knowledge-base-packets-desegmentation>`.

Implemented UDS packet classes:
 - `AbstractUdsPacket`_


AbstractUdsPacket
`````````````````
:class:`~uds.packet.abstract_packet.AbstractUdsPacket` class **contains common implementation and provides common API**
for all UDS Packet classes as they are inheriting after :class:`~uds.packet.abstract_packet.AbstractUdsPacket` class.

A **user shall not use** :class:`~uds.packet.abstract_packet.AbstractUdsPacket` **directly**, but one is able
(and encouraged) to use :class:`~uds.packet.abstract_packet.AbstractUdsPacket` implementation with any of its
children classes.

Properties implemented in :class:`~uds.packet.abstract_packet.AbstractUdsPacket` class:
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacket.raw_data` - settable
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacket.addressing` - settable
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacket.packet_type` - readable


UDS Packet Record
-----------------
UDS packet record is a container that stores historic information of :ref:`UDS packet (N_PDU) <knowledge-base-uds-packet>`
that was either received or transmitted.
UDS packets **differs for each communication bus**, therefore **multiple classes implementing UDS packet records are defined**.

A **user shall not create objects of UDS packet record classes** in normal cases, but one would probably use them quite
often as they are returned by other layers of :mod:`uds` package.

Implemented UDS packet record classes:
 - `AbstractUdsPacketRecord`_


AbstractUdsPacketRecord
```````````````````````
:class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` class **contains common implementation and provides common API**
for all UDS Packet classes as they are inheriting after :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` class.

A **user shall not use** :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` **directly**, but one is able
(and encouraged) to use :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` implementation with any of its
children classes.

Properties implemented in :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` class:
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacketRecord.frame` - readable
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacketRecord.direction` - readable
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacketRecord.packet_type` - readable
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacketRecord.raw_data` - readable and abstract (bus specific)
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacketRecord.addressing` - readable and abstract (bus specific)
 - :attr:`~uds.packet.abstract_packet.AbstractUdsPacketRecord.transmission_time` - readable and abstract (bus specific)

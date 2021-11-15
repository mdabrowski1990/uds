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
carried in :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`.

Supported values of UDS packet types are defined in following enum classes:
 - `AbstractUdsPacketType`_
 - `CanPacketType`_


AbstractUdsPacketType
`````````````````````
:class:`~uds.packet.abstract_packet.AbstractUdsPacketType` class is an empty enum that is a parent class for all concrete
UDS packet types enum classes. It **provides common API and values restriction** (UDS packet type values must be
4-bit integer) **for all children classes**.

.. warning:: A **user shall not use** :class:`~uds.packet.abstract_packet.AbstractUdsPacketType` **directly**,
    but one is able (and encouraged) to use :class:`~uds.packet.abstract_packet.AbstractUdsPacketType` implementation
    with any of its children classes.


CanPacketType
`````````````
:class:`~uds.packet.can_packet_type.CanPacketType` enum class contains definition of
:ref:`CAN specific Network Protocol Control Information <knowledge-base-can-n-pci>` values.

**Example code:**

    .. code-block::  python

        import uds

        # check if value is defined
        uds.packet.CanPacketType.is_member(uds.packet.CanPacketType.SINGLE_FRAME)
        uds.packet.CanPacketType.is_member(0xF)

        # add new member
        uds.packet.CanPacketType.add_member("NewMember", 0xF)

        # check if member was added
        uds.packet.CanPacketType.is_member(0xF)


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
 - `CanPacket`_


AbstractUdsPacket
`````````````````
:class:`~uds.packet.abstract_packet.AbstractUdsPacket` class **contains common implementation and provides common API**
for all UDS Packet classes.

.. warning:: A **user shall not use** :class:`~uds.packet.abstract_packet.AbstractUdsPacket` **directly**, but one is
    able (and encouraged) to use :class:`~uds.packet.abstract_packet.AbstractUdsPacket` implementation with any of its
    children classes.


CanPacket
`````````
:class:`~uds.packet.can_packet.CanPacket` class contains CAN specific implementation of
:ref:`UDS packets <knowledge-base-uds-packet>`.


**Example code:**

    .. code-block::  python

        import uds

        # create CAN Packet
        can_packet = uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.SINGLE_FRAME,
                                          addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                          addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                          payload=[0x3E, 0x00],
                                          can_id=0x682)

        # change CAN Packet data parameters
        can_packet.set_packet_data(packet_type=uds.packet.CanPacketType.FLOW_CONTROL,
                                   flow_status=uds.can.CanFlowStatus.ContinueToSend,
                                   dlc=8,
                                   block_size=4,
                                   st_min=0)

        # change CAN Packet addressing parameters
        can_packet.set_address_information(addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                           addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL,
                                           target_address=0x00,
                                           source_address=0xFF)


UDS Packet Record
-----------------
UDS packet record is a container that stores historic information of :ref:`UDS packet (N_PDU) <knowledge-base-uds-packet>`
that was either received or transmitted.
UDS packets **differs for each communication bus**, therefore **multiple classes implementing UDS packet records are defined**.

.. warning:: A **user shall not create objects of UDS packet record classes** in normal cases, but one would probably
    use them quite often as they are returned by other layers of :mod:`uds` package.

Implemented UDS packet record classes:
 - `AbstractUdsPacketRecord`_
 - `CanPacketRecord`_


AbstractUdsPacketRecord
```````````````````````
:class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` class **contains common implementation and provides common API**
for all UDS Packet Record classes.

.. warning:: A **user shall not use** :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` **directly**, but
    one is able (and encouraged) to use :class:`~uds.packet.abstract_packet.AbstractUdsPacketRecord` implementation
    with any of its children classes.


CanPacketRecord
```````````````
:class:`~uds.packet.can_packet_record.CanPacketRecord` class contains CAN specific implementation of
:ref:`UDS packets <knowledge-base-uds-packet>` records.

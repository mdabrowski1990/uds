Diagnostic Messages
===================

.. role:: python(code)
    :language: python


In this chapter, you will find information about :python:`messages` subpackage implementation. It contains code that
enables creation of entities that carry UDS data and helps to describe theirs transmission.

In implementation we distinguish following entities that carry diagnostic data:
 - `UDS Message`_ - carries application data (diagnostic service) on upper layers (layers 5-7 of UDS OSI model)
 - `UDS Packet`_ - packets that are exchanged between client and server during `UDS Message`_ segmentation
   (layers 3-4 of UDS OSI model); UDS Packet is called Network Protocol Data Unit (N_PDU)
 - `Bus Frame`_ - a single frame transmitted over any bus that carries any data that is not necessarily related to
   UDS communication (layers 1-2 of bus OSI model)

Additionally, you will find `Transmission Attributes`_ chapter which contains implementation details of enums that
are used to describe UDS transmission.


UDS Message
-----------
TODO during `UDS Message documentation task <https://github.com/mdabrowski1990/uds/issues/52>`_


UDS Packet
----------
To efficiently handle UDS Packets (Network Protocol Data Units - N_PDUs), the implementation is divided into two parts:
 - `UDS Packet Definition`_ - storage of UDS Packet (N_PDU) attributes that could be used to transmit UDS Packet on
   a dedicated bus
 - `UDS Packet Record`_ - record with historic information about either received or transmitted UDS Packet (N_PDU)


UDS Packet Definition
``````````````````````
UDS Packets slightly differ for each bus, therefore abstract class (AbstractUdsPacket_) is separated
out in the implementation. If you want to define UDS Packet (that might be sent later on), you should create
an object of any of concrete classes that inherits after :python:`AbstractUdsPacket` class.

Currently following classes are implemented to handle creation of new UDS Packets (N_PDUs):

 - AbstractUdsPacket_

AbstractUdsPacket
'''''''''''''''''
:python:`AbstractUdsPacket` class contains common implementation of all UDS Packet types. **You should never call**
:python:`AbstractUdsPacket` **class directly**, therefore in the example below :python:`ConcreteUdsPacket`
(as a concrete implementation of UDS Packet for desired bus) is used instead:

.. code-block::  python

   from uds.messages import AddressingType, ConcreteUdsPacket

   # you can define UDS Packet (N_PDU)
   packet = ConcreteUdsPacket(raw_data=[0x02, 0x3E, 0x00, 0x55, 0x55, 0x55, 0x55, 0x55],
                              addressing=AddressingType.PHYSICAL)

   # you can get attributes of the packet object
   print(packet.raw_data)
   print(packet.addressing)
   print(packet.packet_type)  # this will only work for concrete UDS Packet implementation

   # you can change values of UDS Packet object attributes
   packet.raw_data = (0x03, 0x22, 0xF1, 0x84, 0x00, 0x00, 0x00, 0x00)
   packet.addressing = "Functional"


UDS Packet Record
`````````````````
UDS Packet Record is a record with historic data of UDS Packet (N_PDU) that was either received or transmitted.
Due to difference in structure of UDS Packets for various buses, abstract class (AbstractUdsPacketRecord_) is separated
out in the implementation.

Currently following classes are implemented to store historic data of UDS Packets (N_PDUs):
 - AbstractUdsPacketRecord_

AbstractUdsPacketRecord
'''''''''''''''''''''''
:python:`AbstractUdsPacketRecord` class contains common implementation of all UDS Packets records for all buses.
**You should never call** :python:`AbstractUdsPacketRecord` **class directly**, therefore in the example below
:python:`ConcreteUdsPacketRecord` (as a concrete implementation of UDS Packet record for a certain bus) is used instead:

.. code-block::  python

   from uds.messages import TransmissionDirection, ConcreteUdsPacketRecord

   # usually, you would not be doing this by yourself as Transport Interface feature is meant to handle this feature
   packet_record = ConcreteUdsPacketRecord(frame=some_frame,
                                           direction=TransmissionDirection.RECEIVED,
                                           ...)  # ... represents additional arguments that are required by a concrete class

   # you can get attributes of the UDS Packet Record object
   print(packet_record.frame)
   print(packet_record.direction)
   print(packet_record.raw_data)
   print(packet_record.packet_type)
   print(packet_record.addressing)
   print(packet_record.transmission_time)


UDS Packet Type
```````````````
Network Protocol Control Information determines value of UDS Packet (N_PDU) type (e.g. whether this is
the only/the first/following UDS Packet). Due to differences in UDS specifications for various buses,
abstract class (AbstractPacketType_) is separated out in the implementation.

Currently following enums with UDS Packet Type (N_PCI) values are implemented:
 - AbstractPacketType_

AbstractPacketType
''''''''''''''''''
An empty enum with helper methods. It is meant to be parent class for all concrete UDS Packet Type enums classes.

.. code-block::  python

   from uds.messages import AbstractPacketType

    AbstractPacketType.is_member(value_to_check)  # checks whether value is enum member - returns true/false
    AbstractPacketType.validate_member(value_to_check)  # checks whether value is enum member - raises an exception if not a member
    AbstractPacketType.add_member(name="NEW_NPCI_NAME", value=0x0)  # adds a new member to enum class

Bus Frame
---------
TODO during first bus implementation, probably `CAN <https://github.com/mdabrowski1990/uds/milestone/3>`_.


Transmission Attributes
-----------------------
Transmission attributes are used to unambiguously describe UDS transmission.

Following enums are available:
 - TransmissionDirection_
 - AddressingType_


TransmissionDirection
`````````````````````
:python:`TransmissionDirection` enum is used to determine whether diagnostic data entity (frame/message/PDU) was
either received or transmitted.

.. code-block::  python

   from uds.messages import TransmissionDirection

   TransmissionDirection.RECEIVED
   TransmissionDirection.TRANSMITTED

AddressingType
``````````````
:python:`AddressingType` is used to determine type of transmission (one/many recipients and communication model).

.. code-block::  python

   from uds.messages import AddressingType

   AddressingType.PHYSICAL
   AddressingType.FUNCTIONAL
   AddressingType.BROADCAST  # in fact, this is FUNCTIONAL addressing with broadcast communication used, but it was separated to distinguish this case

Diagnostic Messages
===================

.. role:: python(code)
    :language: python

In this chapter, you will find information about :mod:`uds.messages` subpackage implementation. It contains code that
enables creation of entities that carry UDS data and helps to describe theirs transmission.

In implementation we distinguish following entities that carry diagnostic data:
 - `UDS Message`_ - carries application data (diagnostic service) on upper layers (layers 5-7 of UDS OSI model),
   it might also be called Application Protocol Data Unit (A_PDU)
 - `UDS Packet`_ - packets that are exchanged between client and server during `UDS Message`_ segmentation
   (layers 3-4 of UDS OSI model), it might also be called Network Protocol Data Unit (N_PDU)
 - `Bus Frame`_ - a single frame transmitted over any bus on lower layers (layers 1-2 of UDS/bus OSI model),
   it carries any data that is not necessarily related to UDS communication

Additionally, you will find `Transmission Attributes`_ and `UDS Data Enums`_ chapters which contain implementation
details about enums that help to describe transmission and data of aforementioned entities.


UDS Message
-----------
Diagnostic messages (either diagnostic requests or response messages) are called 'UDS Messages' in the implementation.

In the code, the diagnostic message features are divided into two parts:
 - :class:`~uds.messages.UdsMessage` - storage for diagnostic message (A_PDU) attributes that could be used by a user to transmit this
   UDS Message on a configured bus
 - :class:`~uds.messages.UdsMessageRecord` - record with historic information about either received or transmitted diagnostic message


UdsMessage
``````````
Diagnostic messages has common specification for all buses, therefore :class:`~uds.messages.UdsMessage` class has the only one
implementation which is the same regardless of bus used by a user. :python:`UdsMessage` is a storage
for diagnostic message attributes, therefore if you want to send any diagnostic message, you should prior create
:python:`UdsMessage` object first.


.. autoapiclass:: uds.messages.UdsMessage
   :members:
   :special-members:


.. code-block::  python

   from uds.messages import UdsMessage, AddressingType

   # example how to define a UDS Message
   uds_message = UdsMessage(raw_message=[0x10, 0x03],
                            addressing=AddressingType.PHYSICAL)

   # you have two attributes that you can freely change
   print(uds_message.raw_message)
   uds_message.raw_message = [0x3E, 0x00]
   print(uds_message.raw_message)

   print(uds_message.addressing)
   uds_message.addressing = AddressingType.FUNCTIONAL
   print(uds_message.addressing)


UdsMessageRecord
````````````````
.. autoapiclass:: uds.messages.UdsMessageRecord
   :members:
   :special-members:

Historic records with information about diagnostic messages that were either received or transmitted, are stored in
objects of :python:`UdsMessageRecord` class.

.. code-block::  python

   from uds.messages import UdsMessageRecord, AddressingType

   # usually, you would not be doing this by yourself as Client and Server features are meant to create objects of this class
   uds_message_records = UdsMessageRecord(raw_message=[0x10, 0x03],
                                          packets_records=[uds_packet_record])  # at least one packet - instance of `AbstractUdsPacketRecord` class

   # you can get attributes of the UDS Message Record object
   print(uds_message_records.raw_message)
   print(uds_message_records.packets_records)
   print(uds_message_records.addressing)
   print(uds_message_records.direction)
   print(uds_message_records.transmission_end)


UDS Packet
----------
To efficiently handle UDS Packets (Network Protocol Data Units - N_PDUs), the implementation is divided into two parts:
 - `UDS Packet Definition`_ - storage of UDS Packet (N_PDU) attributes that could be used by a user to transmit
   UDS Packet on a dedicated bus
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

   # usually, you would not be doing this by yourself as Transport Interface feature is meant to create objects of this class
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

    # you can check if value is member of AbstractPacketType enum
    AbstractPacketType.is_member(value_to_check)  # returns True if value is member, False otherwise
    AbstractPacketType.validate_member(value_to_check)  # raises an exception if value is not a member of the enum

    # you can add a new enum member
    AbstractPacketType.add_member(name="NEW_NPCI_NAME", value=0x0)

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
:python:`TransmissionDirection` enum is used to determine whether diagnostic data entity (message/packet/frame) was
either received or transmitted.

.. code-block::  python

   from uds.messages import TransmissionDirection

   TransmissionDirection.RECEIVED
   TransmissionDirection.TRANSMITTED

AddressingType
``````````````
:python:`AddressingType` is used to determine type of transmission (one/many recipient(s) and communication model).

.. code-block::  python

   from uds.messages import AddressingType

   AddressingType.PHYSICAL
   AddressingType.FUNCTIONAL
   AddressingType.BROADCAST  # in fact, this is FUNCTIONAL addressing with broadcast communication used, but it was separated to distinguish this case


UDS Data Enums
----------------
There are following enums that contains information related to UDS Messages data:
 - RequestSID_
 - ResponseSID_
 - NRC_


RequestSID
``````````
Enum with all known Service Identifier (SID) values that might be used in a request message.

.. code-block::  python

   from uds.messages import RequestSID

   # you can check if value is valid request sid
   RequestSID.is_request_sid(value_to_check)

   # you can check whether value is enum member
   RequestSID.is_member(value_to_check)  # returns True if value is member, False otherwise
   RequestSID.validate_member(value_to_check)  # raises an exception if value is not a member of the enum


ResponseSID
```````````
Enum with all known Response Service Identifier (RSID) values that might be used in a response message.

.. code-block::  python

   from uds.messages import ResponseSID

   # you can check if value is valid request sid
   ResponseSID.is_response_sid(value_to_check)

   # you can check whether value is enum member
   ResponseSID.is_member(value_to_check)  # returns True if value is member, False otherwise
   ResponseSID.validate_member(value_to_check)  # raises an exception if value is not a member of the enum


NRC
```
Enum with all known Negative Response Code (NRC) values that might be used in a negative response message.

.. code-block::  python

   from uds.messages import NRC

   # you can check whether value is NRC enum member
   NRC.is_member(value_to_check)  # returns True if value is member, False otherwise
   NRC.validate_member(value_to_check)  # raises an exception if value is not a member of the enum

   # you can add a new enum member
   NRC.add_member(name="NAME_FOR_NEW_MEMBER", value=0x00)

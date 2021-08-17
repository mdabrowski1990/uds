Diagnostic Messages
===================

.. role:: python(code)
    :language: python


In this chapter, you will find information about :python:`messages` subpackage implementation. It contains code that is
required to create and describe transmission of entities that carry diagnostic messages.

In implementation we distinguish following entities that carry diagnostic data:
 - `UDS Message`_ - carries application UDS data (diagnostic service) on upper layers (layers 5-7 of OSI model)
 - `Network Protocol Data Unit`_ - it is a single packet that was created after segmentation of UDS Message
   (layers 3-4 of OSI model)
 - `Bus Frame`_ - a single frame transmitted over any bus that carries any data (not necessarily related to
   UDS communication)

Additionally, you will find `Transmission Attributes`_ chapter which contains implementation details of enums that
are used to describe type and direction of these entities transmission.


UDS Message
-----------
TODO during `UDS Message documentation task <https://github.com/mdabrowski1990/uds/issues/52>`_


Network Protocol Data Unit
--------------------------
To efficiently use Network Protocol Data Units (N_PDUs), the implementation is divided into two parts:

- `Network Protocol Data Unit Definition`_ - storage of N_PDU attributes that could be used to transmit the N_PDU
  on a bus
- `Network Protocol Data Unit Record`_ - historic record with information about either received or transmitted N_PDU


Network Protocol Data Unit Definition
`````````````````````````````````````
Network Protocol Data Unit slightly differs for each bus type, therefore abstract class (AbstractNPDU_) is separated
out in the implementation. If you want to define a N_PDU (that might be sent later on), you should create an object of
any of concrete classes that inherits after :python:`AbstractNPDU` class.

Currently following classes are implemented to handle creation of new N_PDUs:
 - AbstractNPDU_

AbstractNPDU
''''''''''''
:python:`AbstractNPDU` class contains common implementation of all N_PDU types. **You should never call**
:python:`AbstractNPDU` **class directly**, therefore in the example below :python:`ConcreteNPDU` (as a concrete
implementation of N_PDU for desired bus) is used instead:

.. code-block::  python

   from uds.messages import AddressingType, ConcreteNPDU

   # you can define N_PDU
   pdu = ConcreteNPDU(raw_data=[0x02, 0x3E, 0x00, 0x55, 0x55, 0x55, 0x55, 0x55], addressing=AddressingType.PHYSICAL)

   # you can get attributes of the N_PDU object
   print(pdu.raw_data)
   print(pdu.addressing)
   print(pdu.pci)  # this will only be working for concrete N_PDU implementation

   # you can change values of N_PDU object attributes
   pdu.raw_data = (0x03, 0x22, 0xF1, 0x84, 0x00, 0x00, 0x00, 0x00)
   pdu.addressing = "Functional"


Network Protocol Data Unit Record
`````````````````````````````````
Network Protocol Data Unit Record is a record with historic data of N_PDU that was either received or transmitted.
Due to Network Protocol Data Units differences for various buses, abstract class (AbstractNPDURecord_) is separated
out in the implementation.

Currently following classes are implemented to store records of N_PDUs:
 - AbstractNPDURecord_

AbstractNPDURecord
''''''''''''''''''
:python:`AbstractNPDURecord` class contains common implementation of all N_PDU records for all buses.
**You should never call** :python:`AbstractNPDURecord` **class directly**, therefore in the example below
:python:`ConcreteNPDURecord` (as a concrete implementation of N_PDU record for desired bus) is used instead:

.. code-block::  python

   from uds.messages import TransmissionDirection, ConcreteNPDURecord

   # usually, you would not be doing this by yourself as Transport Interface feature is meant to handle this feature
   pdu_record = ConcreteNPDURecord(frame=some_frame, direction=TransmissionDirection.RECEIVED, ...)  # there might some additional arguments

   # you can get attributes of the N_PDU Record object
   print(pdu.frame)
   print(pdu.direction)
   print(pdu.raw_data)
   print(pdu.npci)
   print(pdu.addressing)
   print(pdu.transmission_time)


Network Protocol Control Information
````````````````````````````````````
Network Protocol Control Information determines type of `Network Protocol Data Unit`_ (e.g. whether this is
the only/the first/following N_PDU). Due to Network Protocol Control Information differences for various buses,
abstract class (AbstractNPCI_) is separated out in the implementation.

Currently following enums with N_PCI values are implemented:
 - AbstractNPCI_

AbstractNPCI
''''''''''''
An empty enum that is parent class for all N_PCI enums for concrete buses.


Bus Frame
---------
TODO during first bus implementation, probably `CAN <https://github.com/mdabrowski1990/uds/milestone/3>`_.


Transmission Attributes
-----------------------
Transmission attributes are used to unambiguously describe transmission of entities (`UDS Message`_,
`Network Protocol Data Unit`_, `Bus Frame`_) that carry diagnostic messages.

Following enums are used:
 - TransmissionDirection_
 - AddressingType_


TransmissionDirection
`````````````````````
:python:`TransmissionDirection` enum is used to determine whether entity (frame/message/PDU) was either received
or transmitted.

.. code-block::  python

   from uds.messages import TransmissionDirection

AddressingType
``````````````
:python:`AddressingType` is used to determine type of transmission (one/many recipients, communication model).

.. code-block::  python

   from uds.messages import AddressingType

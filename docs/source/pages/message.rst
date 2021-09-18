Diagnostic Messages
===================
Implementation related to diagnostic messages and packets is located in :mod:`uds.messages` sub-package.


UDS Message Implementation
--------------------------
Diagnostic messages implementation is divided into two parts:
 - `UdsMessage`_ - storage for a temporary diagnostic message definition on the user side
 - `UdsMessageRecord`_ - storage for historic information of a diagnostic message that was either received
   or transmitted


UdsMessage
```````````
:class:`~uds.messages.uds_message.UdsMessage` class is meant to provide containers for diagnostic messages information.
Once a diagnostic message object is created, it stores diagnostic message data that were provided by a user.
One can **use these objects to execute complex operations** (provided in other subpackages) such as diagnostic messages
transmission or segmentation.

All :class:`~uds.messages.uds_message.UdsMessage` **attributes (** :attr:`~uds.messages.uds_message.UdsMessage.payload`,
:attr:`~uds.messages.uds_message.UdsMessage.addressing` **) are validated on each value change**, therefore a user will
face an exception if one tries to set an invalid (incompatible with the annotation) value to of these attributes.

Example code:

.. code-block::  python

   from uds.messages import UdsMessage, AddressingType

   # example how to create an object
   uds_message = UdsMessage(payload=[0x10, 0x03],
                            addressing=AddressingType.PHYSICAL)

   # raw message attribute
   print(uds_message.payload)
   uds_message.payload = (0x62, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)
   print(uds_message.payload)
   uds_message.payload = [0x3E, 0x80]
   print(uds_message.payload)

   # addressing attribute
   print(uds_message.addressing)
   uds_message.addressing = AddressingType.FUNCTIONAL
   print(uds_message.addressing)
   uds_message.addressing = AddressingType.PHYSICAL.value
   print(uds_message.addressing)


UdsMessageRecord
````````````````
:class:`~uds.messages.uds_message.UdsMessageRecord` class is meant to provide container for historic information
of diagnostic messages that were either transmitted or received.
A **user shall not create objects of this class** in normal cases, but one would probably use them quite often as they
are returned by other layers of this package.

All :class:`~uds.messages.uds_message.UdsMessageRecord` **attributes (**
:attr:`~uds.messages.uds_message.UdsMessageRecord.payload`, :attr:`~uds.messages.uds_message.UdsMessageRecord.addressing`,
:attr:`~uds.messages.uds_message.UdsMessageRecord.direction`, :attr:`~uds.messages.uds_message.UdsMessageRecord.packets_records`,
:attr:`~uds.messages.uds_message.UdsMessageRecord.transmission_start`, :attr:`~uds.messages.uds_message.UdsMessageRecord.transmission_end`
**) are read only** (they are set only once upon an object creation) as history cannot be changed (can't it, right?),
therefore a user will face an exception if one tries to modify a value of any of these attributes.


UDS Packet Implementation
--------------------------
Packets implementation is divided into three parts:
 - `UdsPacketType`_
 - `UdsPacket`_
 - `UdsPacketRecord`_


UdsPacketType
`````````````
Currently implemented UDS packet types:
 - `AbstractUdsPacketType`_

AbstractUdsPacketType
'''''''''''''''''''''

UdsPacket
`````````
Currently implemented UDS packets:
 - `AbstractUdsPacket`_

AbstractUdsPacket
'''''''''''''''''


UdsPacketRecord
```````````````
Currently implemented UDS packets:
 - `AbstractUdsPacket`_

AbstractUdsPacketRecord
'''''''''''''''''''''''



UDS Messages Data
-----------------

Service Identifiers
```````````````````





Negative Response Codes
```````````````````````


Transmission Attributes
-----------------------


Addressing
``````````



Transmission Direction
``````````````````````



.. role:: python(code)
    :language: python

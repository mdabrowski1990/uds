Diagnostic Messages
===================
Implementation of diagnostic messages and packets is located in :mod:`uds.messages` sub-package.



UDS Message Implementation
--------------------------
Diagnostic messages implementation is divided into two parts:
 - `UdsMessage`_ - temporary definition a diagnostic message that (for instance) can be transmitted
 - `UdsMessageRecord`_ - storage for historic information of a diagnostic message that was either received
   or transmitted


UdsMessage
```````````
:class:`~uds.messages.uds_message.UdsMessage` class is meant to provide containers for diagnostic messages information.
Once a diagnostic message object is created, it stores diagnostic message data that were provided by a user.
One can use these objects to execute complex operations such as diagnostic messages transmission or segmentation.

All :class:`~uds.messages.uds_message.UdsMessage` attributes (:attr:`~uds.messages.uds_message.UdsMessage.payload`,
:attr:`~uds.messages.uds_message.UdsMessage.addressing`) are **validated on each value change** (a user will face
an exception if one tries to set an invalid value to of these attributes).


Example code:

.. code-block::  python

   from uds.messages import UdsMessage, AddressingType

   # example how to create an object
   uds_message = UdsMessage(payload=[0x10, 0x03], addressing=AddressingType.PHYSICAL)

   # raw message attribute
   print(uds_message.payload)
   uds_message.payload = (0x3E, 0x00)
   print(uds_message.payload)
   uds_message.payload = [0x54]
   print(uds_message.payload)

   # addressing attribute
   print(uds_message.addressing)
   uds_message.addressing = AddressingType.FUNCTIONAL
   print(uds_message.addressing)
   uds_message.addressing = AddressingType.PHYSICAL.value
   print(uds_message.addressing)


UdsMessageRecord
````````````````



UDS Packet Implementation
--------------------------


UDS Packet


UDS Packet Record
`````````````````



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

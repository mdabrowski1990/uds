Diagnostic Messages
===================
Implementation related to diagnostic messages and packets is located in :mod:`uds.messages` sub-package.


.. _implementation-diagnostic-message:

UDS Message Implementation
--------------------------
:ref:`Diagnostic messages <knowledge-base-diagnostic-message>` implementation is divided into two parts:
 - `UDS Message`_ - storage for a temporary diagnostic message definition on the user side
 - `UDS Message Record`_ - storage for historic information of a diagnostic message that was either received
   or transmitted


UDS Message
```````````
:class:`~uds.messages.uds_message.UdsMessage` class is meant to provide containers for
:ref:`diagnostic messages <knowledge-base-diagnostic-message>` information.
Once a diagnostic message object is created, it stores diagnostic message data that were provided by a user.
One can **use these objects to execute complex operations** (provided in other subpackages) such as diagnostic messages
transmission or :ref:`segmentation <knowledge-base-segmentation>`.

All :class:`~uds.messages.uds_message.UdsMessage` **attributes are validated on each value change**, therefore a user will
face an exception if one tries to set an invalid (incompatible with the annotation) value to of these attributes.

Attributes implemented in :class:`~uds.messages.uds_message.UdsMessage` class:
 - :attr:`~uds.messages.uds_message.UdsMessage.payload` - settable
 - :attr:`~uds.messages.uds_message.UdsMessage.addressing` - settable

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


UDS Message Record
``````````````````
:class:`~uds.messages.uds_message.UdsMessageRecord` class is meant to provide container for historic information
of :ref:`diagnostic messages <knowledge-base-diagnostic-message>` that were either transmitted or received.
A **user shall not create objects of this class** in normal cases, but one would probably use them quite often as they
are returned by other layers of :mod:`uds` package.

All :class:`~uds.messages.uds_message.UdsMessageRecord` **attributes are read only** (they are set only once upon
an object creation) as they store historic data and history cannot be changed (*can't it, right?*).
A user will face an exception if one tries to modify any attribute.

Attributes implemented in :class:`~uds.messages.uds_message.UdsMessageRecord` class:
 - :attr:`~uds.messages.uds_message.UdsMessageRecord.payload` - readable
 - :attr:`~uds.messages.uds_message.UdsMessageRecord.addressing` - readable
 - :attr:`~uds.messages.uds_message.UdsMessageRecord.direction` - readable
 - :attr:`~uds.messages.uds_message.UdsMessageRecord.packets_records` - readable
 - :attr:`~uds.messages.uds_message.UdsMessageRecord.transmission_start` - readable
 - :attr:`~uds.messages.uds_message.UdsMessageRecord.transmission_end` - readable


.. _implementation-uds-packet:

UDS Packet Implementation
--------------------------
:ref:`UDS packets <knowledge-base-uds-packet>` implementation is divided into three parts:
 - `UDS Packet Type`_ - enums with :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>`
   values definitions
 - `UDS Packet`_ - storages for a temporary :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`
   definition on the user side
 - `UDS Packet Record`_ - storages for historic information of a :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`
   that was either received or transmitted


UDS Packet Type
```````````````
UDS packet types are supposed to be understood as values of
:ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>`.
Supported values of UDS packet types are defined in specially designed for this purpose enum classes.

Enum classes that implements UDS packet types:
 - `AbstractUdsPacketType`_


AbstractUdsPacketType
'''''''''''''''''''''
:class:`~uds.messages.uds_packet.AbstractUdsPacketType` class is an empty enum that is a parent class for all concrete
UDS packet types enum classes. It **provides common API and values restriction** (UDS packet type values must be
4-bit integer) **for all children classes**.

A **user shall not use** :class:`~uds.messages.uds_packet.AbstractUdsPacketType` **directly**, but one is able
(and encouraged) to use :class:`~uds.messages.uds_packet.AbstractUdsPacketType` implementation with any of its
children classes.

Methods implemented in :class:`~uds.messages.uds_packet.AbstractUdsPacketType` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
 - :meth:`~uds.utilities.enums.ExtendableEnum.add_member`


UDS Packet
``````````
:ref:`UDS packets <knowledge-base-uds-packet>` **differs for each communication bus**, therefore
**multiple classes implementing them are defined**.
Each UDS packet class provides containers for :ref:`Network Protocol Data Unit (N_PDU) <knowledge-base-uds-packet>`
information that are specific for a communication bus for which this class is relevant.
**Objects of UDS packet classes might be used to execute complex operations** (provided in other subpackages) such as
packets transmission or :ref:`desegmentation <knowledge-base-desegmentation>`.

Implemented UDS packet classes:
 - `AbstractUdsPacket`_


AbstractUdsPacket
'''''''''''''''''
:class:`~uds.messages.uds_packet.AbstractUdsPacket` class **contains common implementation and provides common API**
for all UDS Packet classes as they are inheriting after :class:`~uds.messages.uds_packet.AbstractUdsPacket` class.

A **user shall not use** :class:`~uds.messages.uds_packet.AbstractUdsPacket` **directly**, but one is able
(and encouraged) to use :class:`~uds.messages.uds_packet.AbstractUdsPacket` implementation with any of its
children classes.

Properties implemented in :class:`~uds.messages.uds_packet.AbstractUdsPacket` class:
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacket.raw_data` - settable
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacket.addressing` - settable
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacket.packet_type` - readable
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacket.packet_type_enum` - readable and abstract (bus specific)
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacket.payload` - readable and abstract (bus specific)


UDS Packet Record
`````````````````
UDS packet record is a container that stores historic information of :ref:`UDS packet (N_PDU) <knowledge-base-uds-packet>`
that was either received or transmitted.
UDS packets **differs for each communication bus**, therefore **multiple classes implementing UDS packet records are defined**.

A **user shall not create objects of UDS packet record classes** in normal cases, but one would probably use them quite
often as they are returned by other layers of :mod:`uds` package.

Implemented UDS packet record classes:
 - `AbstractUdsPacketRecord`_


AbstractUdsPacketRecord
'''''''''''''''''''''''
:class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` class **contains common implementation and provides common API**
for all UDS Packet classes as they are inheriting after :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` class.

A **user shall not use** :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` **directly**, but one is able
(and encouraged) to use :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` implementation with any of its
children classes.

Properties implemented in :class:`~uds.messages.uds_packet.AbstractUdsPacketRecord` class:
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.frame` - readable
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.direction` - readable
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.packet_type` - readable
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.raw_data` - readable and abstract (bus specific)
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.payload` - readable and abstract (bus specific)
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.addressing` - readable and abstract (bus specific)
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.transmission_time` - readable and abstract (bus specific)
 - :attr:`~uds.messages.uds_packet.AbstractUdsPacketRecord.packet_type_enum` - readable and abstract (bus specific)


UDS Messages Data
-----------------
Implementation of data parameters that are defined by UDS specification.

UDS data parameters:
 - `Service Identifiers`_ - are implemented by:

   - `POSSIBLE_REQUEST_SIDS`_

   - `RequestSID`_

   - `POSSIBLE_RESPONSE_SIDS`_

   - `ResponseSID`_

 - `Negative Response Codes`_


Service Identifiers
```````````````````


POSSIBLE_REQUEST_SIDS
'''''''''''''''''''''
:attr:`~uds.messages.service_identifiers.POSSIBLE_REQUEST_SIDS` is a set with all possible values of
:ref:`Service Identifier <knowledge-base-sid>` data parameter in a :ref:`request message <knowledge-base-request-message>`.


RequestSID
''''''''''
Enum :class:`~uds.messages.service_identifiers.RequestSID` contains definitions of request
:ref:`Service Identifiers <knowledge-base-sid>` values.

Methods implemented in :class:`~uds.messages.service_identifiers.RequestSID` class:
 - :meth:`~uds.messages.service_identifiers.RequestSID.is_request_sid`
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
 - :meth:`~uds.utilities.enums.ExtendableEnum.add_member`


POSSIBLE_RESPONSE_SIDS
''''''''''''''''''''''
:attr:`~uds.messages.service_identifiers.POSSIBLE_RESPONSE_SIDS` is a set with all possible values of
:ref:`Service Identifier <knowledge-base-sid>` data parameter in a :ref:`response message <knowledge-base-response-message>`.


ResponseSID
'''''''''''
Enum :class:`~uds.messages.service_identifiers.ResponseSID` contains definitions of response
:ref:`Service Identifiers <knowledge-base-sid>` values.

Methods implemented in :class:`~uds.messages.service_identifiers.ResponseSID` class:
 - :meth:`~uds.messages.service_identifiers.ResponseSID.is_response_sid`
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
 - :meth:`~uds.utilities.enums.ExtendableEnum.add_member`


Negative Response Codes
```````````````````````
Enum :class:`~uds.messages.nrc.NRC` contains definitions of all common (defined by ISO 14229)
:ref:`Negative Response Codes <knowledge-base-nrc>` values.

Methods implemented in :class:`~uds.messages.nrc.NRC` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
 - :meth:`~uds.utilities.enums.ExtendableEnum.add_member`


Transmission Attributes
-----------------------
Attributes that describes UDS communication:
 - Addressing_ - enum with UDS communication models
 - `Transmission Direction`_ - enum with communication directions


Addressing
``````````
Enum :class:`~uds.messages.transmission_attributes.AddressingType` contains definitions of :ref:`addressing <knowledge-base-addressing>` values that determines UDS communication model:
 - :attr:`~uds.messages.transmission_attributes.AddressingType.PHYSICAL` - direct one to one communication
   (:ref:`physical addressing <knowledge-base-physical-addressing>`)
 - :attr:`~uds.messages.transmission_attributes.AddressingType.FUNCTIONAL` - one to many communication
   (:ref:`functional addressing <knowledge-base-functional-addressing>`)

Methods implemented in :class:`~uds.messages.transmission_attributes.AddressingType` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`


Transmission Direction
``````````````````````
Enum :class:`~uds.messages.transmission_attributes.TransmissionDirection` contains definitions of communication directions:
 - :attr:`~uds.messages.transmission_attributes.TransmissionDirection.RECEIVED` - incoming
 - :attr:`~uds.messages.transmission_attributes.TransmissionDirection.TRANSMITTED` - outcoming

Methods implemented in :class:`~uds.messages.transmission_attributes.TransmissionDirection` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`


.. role:: python(code)
    :language: python

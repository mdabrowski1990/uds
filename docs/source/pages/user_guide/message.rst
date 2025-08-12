.. _implementation-diagnostic-message:

Diagnostic Messages
===================
Implementation related to :ref:`diagnostic messages <knowledge-base-diagnostic-message>` is located in
:mod:`uds.message` sub-package.

It is divided into the following parts:

- `UDS Message`_ - for defining new diagnostic messages before sending
- `UDS Message Record`_ - for storing diagnostic messages that were either received or transmitted
- `Service Identifiers`_ - definition of :ref:`Service Identifier (SID) <knowledge-base-sid>` values
- `Negative Response Codes`_ - definition of :ref:`Negative Response Codes <knowledge-base-nrc>` values


UDS Message
-----------
:class:`~uds.message.uds_message.UdsMessage` class is meant to provide containers for a new
:ref:`diagnostic messages <knowledge-base-diagnostic-message>`.
These objects can be used for complex operations such as transmission or segmentation.

Attributes:

- :attr:`~uds.message.uds_message.UdsMessage.payload` - payload carried by this diagnostic message
- :attr:`~uds.message.uds_message.UdsMessage.addressing_type` - :ref:`addressing type <knowledge-base-addressing>`
  for which message is relevant

Methods:

- :meth:`~uds.message.uds_message.AbstractUdsMessageContainer.__str__` - object presentation in str format
- :meth:`~uds.message.uds_message.UdsMessage.__eq__` - checking whether two objects contain the same diagnostic message
  (they are considered equal, if values of their :attr:`~uds.message.uds_message.UdsMessage.payload`
  and :attr:`~uds.message.uds_message.UdsMessage.addressing_type` attributes are equal)

.. note:: All :class:`~uds.message.uds_message.UdsMessage` **attributes are validated on each value change**,
  therefore a user will face an exception if one tries to set an invalid (e.g. incompatible with the annotation)
  value to any of its attributes.

**Example code:**

  .. code-block::  python

    import uds

    # create example UDS Message
    uds_message = uds.message.UdsMessage(payload=[0x10, 0x03],
                                         addressing_type=uds.addressing.AddressingType.PHYSICAL)

    # payload attribute reassignment
    uds_message.payload = (0x62, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)

    # addressing type attribute reassignment
    uds_message.addressing_type = uds.addressing.AddressingType.FUNCTIONAL


UDS Message Record
------------------
:class:`~uds.message.uds_message.UdsMessageRecord` class is meant to provide containers for historic information
carried by either transmitted or received :ref:`diagnostic messages <knowledge-base-diagnostic-message>`.

Attributes:

- :attr:`~uds.message.uds_message.UdsMessageRecord.payload` - payload carried by this diagnostic message record
- :attr:`~uds.message.uds_message.UdsMessageRecord.addressing_type` - :ref:`addressing type <knowledge-base-addressing>`
  which was used to transmit this message
- :attr:`~uds.message.uds_message.UdsMessageRecord.packets_records` - packets that were exchanged (received or/and sent)
  to transmit this diagnostic message
- :attr:`~uds.message.uds_message.UdsMessageRecord.direction` - whether the message was received or sent
- :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_start` - date and time when the message transmission
  was started
- :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_end` - date and time when the message transmission
  was completed

Methods:

- :meth:`~uds.message.uds_message.UdsMessageRecord.__str__` - object presentation in str format
- :meth:`~uds.message.uds_message.UdsMessageRecord.__eq__` - checking whether two objects contain the same diagnostic message
  (they are considered equal, if values of their :attr:`~uds.message.uds_message.UdsMessageRecord.payload`,
  :attr:`~uds.message.uds_message.UdsMessageRecord.addressing_type` and
  :attr:`~uds.message.uds_message.UdsMessageRecord.direction` attributes are equal)

.. note:: A **user should not create objects of this class** in normal cases, but one would probably use them quite
  often as they are returned by other layers of :mod:`uds` package that take part in communication
  (e.g. :mod:`uds.transport_interface`).

.. warning:: All :class:`~uds.message.uds_message.UdsMessageRecord` **attributes are read only**
  (they are set only once upon an object creation) as they store historic data and history cannot be changed
  (*can't it, right?*).


Service Identifiers
-------------------
Definition of :ref:`Service Identifier (SID) <knowledge-base-sid>` values.


RequestSID
``````````
Enum :class:`~uds.message.service_identifiers.RequestSID` contains definitions of request
:ref:`Service Identifiers <knowledge-base-sid>` values.

Methods:

- :meth:`~uds.message.service_identifiers.RequestSID.is_request_sid` - check if provided value is a Request SID value
- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` - check if provided value is defined as a member of this Enum
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` - validate that provided value is defined as a member of
  this Enum
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member` - define a new Request SID value

.. warning:: :class:`~uds.message.service_identifiers.RequestSID` does not contain definition for every
  :attr:`~uds.message.service_identifiers.POSSIBLE_REQUEST_SIDS` value as some Request SID values are reserved for
  further extension by UDS specification and others are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method on
  :class:`~uds.message.service_identifiers.RequestSID` class to add Request SID value.

**Example code:**

  .. code-block::  python

    import uds

    # check if a value (0xBA in the example) is a Request SID value
    uds.message.RequestSID.is_request_sid(0xBA)  # True

    # check if there is member defined for the value
    uds.message.RequestSID.is_member(0xBA)  # False

    # define a new Request SID value
    new_member = uds.message.RequestSID.add_member("NewRequestSIDMemberName", 0xBA)

    # check if the value was successfully added as a new member
    uds.message.RequestSID.is_member(new_member)  # True
    uds.message.RequestSID.is_member(0xBA)  # True


ResponseSID
```````````
Enum :class:`~uds.message.service_identifiers.ResponseSID` contains definitions of response
:ref:`Service Identifiers <knowledge-base-sid>` values.

Methods:

- :meth:`~uds.message.service_identifiers.ResponseSID.is_response_sid` - check if provided value is a RSID value
- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` - check if provided value is defined as a member of this Enum
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` - validate that provided value is defined as a member of
  this Enum
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member` - define a new RSID value

.. warning:: :class:`~uds.message.service_identifiers.ResponseSID` does not contain definition for every
  :attr:`~uds.message.service_identifiers.POSSIBLE_RESPONSE_SIDS` value as some Response SID values are reserved for
  further extension by UDS specification and other are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method on
  :class:`~uds.message.service_identifiers.ResponseSID` class to add Response SID.

**Example code:**

  .. code-block::  python

    import uds

    # check if a value (0xFA in the example) is a Response SID value
    uds.message.ResponseSID.is_response_sid(0xFA)  # True

    # check if there is member defined for the value
    uds.message.ResponseSID.is_member(0xFA)  # False

    # example how to add a new Response SID value
    new_member = uds.message.ResponseSID.add_member("NewResponseSIDMemberName", 0xFA)

    # check if the value was successfully added as a new member
    uds.message.ResponseSID.is_member(new_member)  # True
    uds.message.ResponseSID.is_member(0xFA)  # True


Negative Response Codes
-----------------------
Enum :class:`~uds.message.nrc.NRC` contains definitions of all common (defined by ISO 14229)
:ref:`Negative Response Codes <knowledge-base-nrc>` values.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` - check if provided value is defined as a member of this Enum
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` - validate that provided value is defined as a member of
  this Enum
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member` - define a new NRC value

.. warning:: :class:`~uds.message.nrc.NRC` does not contain definition for every possible NRC value as some of them are
  reserved for further extension by UDS specification and other are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method on
  :class:`~uds.message.nrc.NRC` class to add NRC value that is specific for the system that you communicate with.

**Example code:**

  .. code-block::  python

    import uds

    # check if a value (0xF0 in the example) is a NRC value
    uds.message.NRC.is_member(0xF0)

    # example how to add a new NRC value
    new_member = uds.message.NRC.add_member("NewNRCMemberName", 0xF0)

    # check if the value was added as a new member
    uds.message.NRC.is_member(new_member)
    uds.message.NRC.is_member(0xF0)

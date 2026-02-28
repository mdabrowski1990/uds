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
:class:`~uds.message.uds_message.UdsMessage` class is meant to provide containers for new
:ref:`diagnostic messages <knowledge-base-diagnostic-message>`.
These objects can be used for complex operations such as transmission or segmentation.

Attributes:

- :attr:`~uds.message.uds_message.UdsMessage.payload`
- :attr:`~uds.message.uds_message.UdsMessage.addressing_type`

Methods:

- :meth:`~uds.message.uds_message.AbstractUdsMessageContainer.__str__`
- :meth:`~uds.message.uds_message.UdsMessage.__eq__`

.. note:: All :class:`~uds.message.uds_message.UdsMessage` **attributes are validated on each value change**,
  therefore a user will face an exception if one tries to set an invalid (e.g. incompatible with the annotation)
  value to any of its attributes.

**Example code:**

  .. code-block::  python

    import uds

    # create example UDS Message
    uds_message = uds.message.UdsMessage(payload=[0x10, 0x03],
                                         addressing_type=uds.addressing.AddressingType.PHYSICAL)

    # present created message
    print(uds_message)

    # change payload value
    uds_message.payload = (0x62, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)

    # change addressing type attribute
    uds_message.addressing_type = uds.addressing.AddressingType.FUNCTIONAL

    # present updated message
    print(uds_message)

    # compare uds messages
    uds_message == uds.message.UdsMessage(payload=[0x62, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF],
                                          addressing_type=uds.addressing.AddressingType.FUNCTIONAL)  # True


UDS Message Record
------------------
:class:`~uds.message.uds_message.UdsMessageRecord` class is meant to provide containers for recorded information
about transmitted or received :ref:`diagnostic messages <knowledge-base-diagnostic-message>`.

Attributes:

- :attr:`~uds.message.uds_message.UdsMessageRecord.payload`
- :attr:`~uds.message.uds_message.UdsMessageRecord.addressing_type`
- :attr:`~uds.message.uds_message.UdsMessageRecord.packets_records`
- :attr:`~uds.message.uds_message.UdsMessageRecord.direction`
- :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_start_time`
- :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_end_time`
- :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_start_timestamp`
- :attr:`~uds.message.uds_message.UdsMessageRecord.transmission_end_timestamp`

Methods:

- :meth:`~uds.message.uds_message.UdsMessageRecord.__str__`
- :meth:`~uds.message.uds_message.UdsMessageRecord.__eq__`

.. note:: **A user would not create objects of** :class:`~uds.message.uds_message.UdsMessageRecord` **class**
  in typical situations, but one would probably use them quite often as they are returned by communication layers
  (e.g. :mod:`uds.transport_interface`) of :mod:`uds` package.

.. warning:: All :class:`~uds.message.uds_message.UdsMessageRecord` **attributes are read-only**
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

- :meth:`~uds.message.service_identifiers.RequestSID.is_request_sid`
- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member`

.. warning:: :class:`~uds.message.service_identifiers.RequestSID` does not contain definition for every
  :attr:`~uds.message.service_identifiers.POSSIBLE_REQUEST_SIDS` value as some Request SID values are reserved for
  further extension by UDS specification and others are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` to add new SID values.

**Example code:**

  .. code-block::  python

    import uds

    # check if a value (0xBA in the example) is a Request SID value
    uds.message.RequestSID.is_request_sid(0xBA)  # True

    # check if there is member defined for the value
    uds.message.RequestSID.is_member(0xBA)  # False
    uds.message.RequestSID.validate_member(0xBA)  # raises ValueError

    # define a new Request SID value
    new_member = uds.message.RequestSID.add_member("NewRequestSIDMemberName", 0xBA)

    # check if the value was successfully added as a new member
    uds.message.RequestSID.is_member(new_member)  # True
    uds.message.RequestSID.is_member(0xBA)  # True
    uds.message.RequestSID.validate_member(new_member)  # new_member
    uds.message.RequestSID.validate_member(0xBA)  # new_member


ResponseSID
```````````
Enum :class:`~uds.message.service_identifiers.ResponseSID` contains definitions of response
:ref:`Service Identifiers <knowledge-base-sid>` values.

Methods:

- :meth:`~uds.message.service_identifiers.ResponseSID.is_response_sid`
- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member`

.. warning:: :class:`~uds.message.service_identifiers.ResponseSID` does not contain definition for every
  :attr:`~uds.message.service_identifiers.POSSIBLE_RESPONSE_SIDS` value as some Response SID values are reserved for
  further extension by UDS specification and other are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` to add new Response SID values.

**Example code:**

  .. code-block::  python

    import uds

    # check if a value (0xFA in the example) is a Response SID value
    uds.message.ResponseSID.is_response_sid(0xFA)  # True

    # check if there is member defined for the value
    uds.message.ResponseSID.is_member(0xFA)  # False
    uds.message.ResponseSID.validate_member(0xFA)  # raises ValueError

    # define a new Response SID value
    new_member = uds.message.ResponseSID.add_member("NewResponseSIDMemberName", 0xFA)

    # check if the value was successfully added as a new member
    uds.message.ResponseSID.is_member(new_member)  # True
    uds.message.ResponseSID.is_member(0xFA)  # True
    uds.message.ResponseSID.validate_member(new_member)  # new_member
    uds.message.ResponseSID.validate_member(0xFA)  # new_member


Adding new SID
``````````````
To define a new (non-standard) SID and RSID value at the same time,
use :func:`~uds.message.service_identifiers.add_sid` function.

**Example code:**

  .. code-block::  python

    import uds

    # check if a values (0xBA and 0xFA in the example) are Request and Response SID values
    uds.message.RequestSID.is_request_sid(0xBA)  # True
    uds.message.ResponseSID.is_response_sid(0xFA)  # True
    uds.message.RequestSID.is_member(0xBA)  # False
    uds.message.ResponseSID.is_member(0xFA)  # False

    # define custom SID and RSID members
    new_sid_member, new_rsid_member = uds.message.add_sid(sid=0xBA, name="CustomService")

    # check if the values were successfully added as new members
    uds.message.RequestSID.is_request_sid(0xBA)  # True
    uds.message.ResponseSID.is_response_sid(0xFA)  # True
    uds.message.RequestSID.is_member(0xBA)  # True
    uds.message.ResponseSID.is_member(0xFA)  # True


Negative Response Codes
-----------------------
Enum :class:`~uds.message.nrc.NRC` contains definitions of all common (defined by ISO 14229)
:ref:`Negative Response Codes <knowledge-base-nrc>` values.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member`

.. warning:: :class:`~uds.message.nrc.NRC` does not contain definition for every possible NRC value as some of them are
  reserved for further extension by UDS specification and other are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method on
  :class:`~uds.message.nrc.NRC` class to add NRC value that is specific for the system that you communicate with.

**Example code:**

  .. code-block::  python

    import uds

    # check if a value (0xF0 in the example) is a NRC value
    uds.message.NRC.is_member(0xF0)  # False
    uds.message.NRC.validate_member(0xF0)  # raises ValueError

    # define a new NRC value
    new_member = uds.message.NRC.add_member("NewNRCMemberName", 0xF0)

    # check if the value was added as a new member
    uds.message.NRC.is_member(new_member)  # True
    uds.message.NRC.is_member(0xF0)  # True
    uds.message.NRC.validate_member(new_member)  # new_member
    uds.message.NRC.validate_member(0xF0)  # new_member

Diagnostic Messages
===================
Implementation related to diagnostic messages is located in :mod:`uds.message` sub-package.


.. _implementation-diagnostic-message:

UDS Message Implementation
--------------------------
:ref:`Diagnostic messages <knowledge-base-diagnostic-message>` implementation is divided into two parts:
 - `UDS Message`_ - storage for a new diagnostic message definition
 - `UDS Message Record`_ - storage for historic information of a diagnostic message that was either received
   or transmitted


UDS Message
```````````
:class:`~uds.message.uds_message.UdsMessage` class is meant to provide containers for a new
:ref:`diagnostic messages <knowledge-base-diagnostic-message>` information.
Once a diagnostic message object is created, it stores all diagnostic message information that were provided by a user.
One can **use these objects to execute complex operations** (provided in other subpackages of :mod:`uds`)
such as diagnostic messages transmission or segmentation.

.. note:: All :class:`~uds.message.uds_message.UdsMessage` **attributes are validated on each value change**,
    therefore a user will face an exception if one tries to set an invalid (e.g. incompatible with the annotation)
    value to any of these attributes.

**Example code:**

    .. code-block::  python

        import uds

        # example how to create an object
        uds_message = uds.message.UdsMessage(payload=[0x10, 0x03],
                                             addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL)

        # raw message attribute reassignment
        uds_message.payload = (0x62, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)

        # addressing attribute reassignment
        uds_message.addressing_type = uds.transmission_attributes.AddressingType.FUNCTIONAL


UDS Message Record
``````````````````
:class:`~uds.message.uds_message.UdsMessageRecord` class is meant to provide containers for historic information
of :ref:`diagnostic messages <knowledge-base-diagnostic-message>` that were either transmitted or received.

.. note:: A **user should not create objects of this class** in normal cases, but one would probably use them quite
    often as they are returned by other layers of :mod:`uds` package.

.. warning:: All :class:`~uds.message.uds_message.UdsMessageRecord` **attributes are read only**
    (they are set only once upon an object creation) as they store historic data and history cannot be changed
    (*can't it, right?*).

    A user will face an exception if one tries to modify any attribute.


UDS Messages Data
-----------------
Implementation of data parameters that are part of diagnostic messages data.

UDS data parameters:
 - `Service Identifiers`_ - are implemented by:

   - `RequestSID`_

   - `ResponseSID`_

 - `Negative Response Codes`_


Service Identifiers
```````````````````
Implementation of :ref:`Service Identifier (SID) <knowledge-base-sid>` values.


RequestSID
''''''''''
Enum :class:`~uds.message.service_identifiers.RequestSID` contains definitions of request
:ref:`Service Identifiers <knowledge-base-sid>` values.

.. warning:: :class:`~uds.message.service_identifiers.RequestSID` does not contain definition for every
    :attr:`~uds.message.service_identifiers.POSSIBLE_REQUEST_SIDS` value as some Request SID values are reserved for
    further extension by UDS specification and others are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method on
    :class:`~uds.message.service_identifiers.RequestSID` class to add Request SID value.

**Example code:**

    .. code-block::  python

        import uds

        # check if a value (0xBA in the example) is a Request SID value
        uds.message.RequestSID.is_request_sid(0xBA)

        # check if there is member defined for the value
        uds.message.RequestSID.is_member(0xBA)

        # example how to add a new Request SID value
        new_member = uds.message.RequestSID.add_member("NewRequestSIDMemberName", 0xBA)

        # check if the value was added as a new member
        uds.message.RequestSID.is_member(new_member)
        uds.message.RequestSID.is_member(0xBA)


ResponseSID
'''''''''''
Enum :class:`~uds.message.service_identifiers.ResponseSID` contains definitions of response
:ref:`Service Identifiers <knowledge-base-sid>` values.

.. warning:: :class:`~uds.message.service_identifiers.ResponseSID` does not contain definition for every
    :attr:`~uds.message.service_identifiers.POSSIBLE_RESPONSE_SIDS` value as some Response SID values are reserved for
    further extension by UDS specification and other are ECU specific (defined by ECU's manufacturer).

.. note:: Use :meth:`~uds.utilities.enums.ExtendableEnum.add_member` method on
    :class:`~uds.message.service_identifiers.ResponseSID` class to add Response SID.

**Example code:**

    .. code-block::  python

        import uds

        # check if a value (0xFA in the example) is a Response SID value
        uds.message.ResponseSID.is_response_sid(0xFA)

        # check if there is member defined for the value
        uds.message.ResponseSID.is_member(0xFA)

        # example how to add a new Response SID value
        new_member = uds.message.ResponseSID.add_member("NewResponseSIDMemberName", 0xFA)

        # check if the value was added as a new member
        uds.message.ResponseSID.is_member(new_member)
        uds.message.ResponseSID.is_member(0xFA)


Negative Response Codes
```````````````````````
Enum :class:`~uds.message.nrc.NRC` contains definitions of all common (defined by ISO 14229)
:ref:`Negative Response Codes <knowledge-base-nrc>` values.

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

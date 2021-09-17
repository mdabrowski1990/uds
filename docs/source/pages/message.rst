Diagnostic Messages
===================
Implementation of diagnostic messages and packets is located in :mod:`uds.messages` sub-package.



UDS Message Implementation
--------------------------
Diagnostic messages implementation is divided into two parts:
 - `UDS Message Definition`_ - temporary definition a diagnostic message that (for instance) can be transmitted
 - `UDS Message Record`_ - storage for historic information of a diagnostic message that was either received
   or transmitted


UDS Message Definition
``````````````````````
.. autoclass:: uds.messages.uds_message.UdsMessage
   :noindex:
   :members:
   :special-members: __init__


Example use case:

.. code-block::  python

   from uds.messages import UdsMessage, AddressingType

   uds_message = UdsMessage(payload=[0x10, 0x03], addressing=AddressingType.PHYSICAL)




UDS Message Record
``````````````````
.. autoclass:: uds.messages.uds_message.UdsMessageRecord
   :noindex:
   :members:



UDS Packet Implementation
--------------------------


UDS Packet Definition
`````````````````````
.. autoclass:: uds.messages.uds_packet.AbstractUdsPacket
   :noindex:



UDS Packet Record
`````````````````
.. autoclass:: uds.messages.uds_packet.AbstractUdsPacketRecord
   :noindex:





UDS Messages Data
-----------------

Service Identifiers
```````````````````
.. autoclass:: uds.messages.service_identifiers.RequestSID
   :noindex:


.. autoclass:: uds.messages.service_identifiers.ResponseSID
   :noindex:


Negative Response Codes
```````````````````````
.. autoclass:: uds.messages.nrc.NRC
   :noindex:


Transmission Attributes
-----------------------


Addressing
``````````
.. autoclass:: uds.messages.transmission_attributes.AddressingType
   :noindex:


Transmission Direction
``````````````````````
.. autoclass:: uds.messages.transmission_attributes.TransmissionDirection
   :noindex:


.. role:: python(code)
    :language: python

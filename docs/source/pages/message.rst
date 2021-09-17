Diagnostic Messages
===================


Implementation of `diagnostic messages
<http://localhost:63342/uds/docs/build/html/pages/knowledge_base.html#diagnostic-message>`_.
implementation is located in :mod:`~uds.messages` sub-package.


UDS Message Implementation
--------------------------
Diagnostic Messages

UDS Message Definition
``````````````````````
:class:`~uds.messages.uds_message.UdsMessage`

.. autoclass:: uds.messages.uds_message.UdsMessage
   :noindex:
   :members:


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

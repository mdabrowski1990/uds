UDS Communication Model
=======================
UDS communication follows the
`Client–Server model <https://en.wikipedia.org/wiki/Client%E2%80%93server_model>`_.


.. _knowledge-base-client:

Client
------
The client role in UDS communication is typically performed by a **Diagnostic Tester**
(also called a *diagnostic tool*).
It initiates communication by sending :ref:`request messages <knowledge-base-request-message>`
and then receives one or more :ref:`diagnostic responses <knowledge-base-response-message>` from
:ref:`servers <knowledge-base-server>`.

In some cases, a request may be forwarded by a Gateway ECU to another ECU.
When this happens, the Gateway ECU temporarily assumes the role of a client within that
subnetwork.


Performance and Error Handling
``````````````````````````````
Time parameters defined by :ref:`ISO standards <knowledge-base-uds-standards>` on the client side:

- :ref:`P2Client <knowledge-base-p2-client>`
- :ref:`P2*Client <knowledge-base-p2*-client>`
- :ref:`P3Client_Phys <knowledge-base-p3-client-phys>`
- :ref:`P3Client_Func <knowledge-base-p3-client-func>`
- :ref:`P6Client <knowledge-base-p6-client>`
- :ref:`P6*Client <knowledge-base-p6*-client>`


.. _knowledge-base-server:

Server
------
The server role in UDS communication is always performed by
`Electronic Control Units (ECUs) <https://en.wikipedia.org/wiki/Electronic_control_unit>`_.
A server receives :ref:`diagnostic requests <knowledge-base-request-message>`
and provides the corresponding :ref:`diagnostic responses <knowledge-base-response-message>`.


Performance and Error Handling
``````````````````````````````
Time parameters defined by :ref:`ISO standards <knowledge-base-uds-standards>` on the server side:

- :ref:`P2Server <knowledge-base-p2-server>`
- :ref:`P2*Server <knowledge-base-p2*-server>`
- :ref:`P4Server <knowledge-base-p4-server>`

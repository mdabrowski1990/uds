.. _knowledge-base-osi-model:

UDS OSI Model
=============
The Unified Diagnostic Services (UDS) protocol can be described using
the `OSI model <https://en.wikipedia.org/wiki/OSI_model>`_.
Each OSI layer has specific responsibilities and relevant standards for UDS communications.


.. _knowledge-base-uds-standards:

UDS Standards
-------------
UDS is defined across multiple standards, which serve as the authoritative source of information and requirements
for this protocol.
The table below summarizes the main standards for different OSI layers and network types:

+--------------+-------------+-------------+-------------+-------------+----------------+-------------+
|   OSI Layer  |    Common   |     CAN     |   FlexRay   |   Ethernet  |     K-Line     |     LIN     |
+==============+=============+=============+=============+=============+================+=============+
| Layer 7      | ISO 14229-1 | ISO 14229-3 | ISO 14229-4 | ISO 14229-5 | ISO 14229-6    | ISO 14229-7 |
| Application  |             |             |             |             |                |             |
|              | ISO 27145-3 |             |             |             |                |             |
+--------------+-------------+-------------+-------------+-------------+----------------+-------------+
| Layer 6      | ISO 27145-2 |             |             |             |                |             |
| Presentation |             |             |             |             |                |             |
+--------------+-------------+-------------+-------------+-------------+----------------+-------------+
| Layer 5      | ISO 14229-2 |             |             |             |                |             |
| Session      |             |             |             |             |                |             |
+--------------+-------------+-------------+-------------+-------------+----------------+-------------+
| Layer 4      | ISO 27145-4 | ISO 15765-2 | ISO 10681-2 | ISO 13400-2 | Not applicable | ISO 17987-2 |
| Transport    |             |             |             |             |                |             |
+--------------+             |             |             |             |                |             |
| Layer 3      |             |             |             |             |                |             |
| Network      |             |             |             |             |                |             |
+--------------+             +-------------+-------------+-------------+----------------+-------------+
| Layer 2      |             | ISO 11898-1 | ISO 17458-2 | ISO 13400-3 | ISO 14230-2    | ISO 17987-3 |
| Data         |             |             |             |             |                |             |
+--------------+             +-------------+-------------+             +----------------+-------------+
| Layer 1      |             | ISO 11898-2 | ISO 17458-4 |             | ISO 14230-1    | ISO 17987-4 |
| Physical     |             |             |             |             |                |             |
|              |             | ISO 11898-3 |             |             |                |             |
+--------------+-------------+-------------+-------------+-------------+----------------+-------------+

where:

- **OSI Layer**: OSI layer for which the standard is relevant.
- **Common**: Standards applicable to UDS regardless of the underlying network.
- **CAN/FlexRay/Ethernet/K-Line/LIN**: Standards specific to UDS implementation on the given network.


.. _knowledge-base-pdu:

Protocol Data Units (PDUs)
--------------------------
Each OSI layer defines its own `Protocol Data Unit (PDU) <https://en.wikipedia.org/wiki/Protocol_data_unit>`_.
For simplicity, the UDS implementation distinguishes the following PDUs:

- **Application PDU (A_PDU)**: Represents a `diagnostic message` or `UDS message`.
  More information:
  - :ref:`knowledge base section - diagnostic message <knowledge-base-diagnostic-message>`
  - :ref:`implementation - diagnostic message <implementation-diagnostic-message>`

- **Network PDU (N_PDU)**: Represents a `packet`.
  More information:
  - :ref:`knowledge base section - packet <knowledge-base-packet>`
  - Implementation: :mod:`uds.packet`

- **Data PDU (D_PDU)**: Represents a `frame`. No internal documentation is provided; frame handling
  is typically performed by external libraries.

.. figure:: ../../diagrams/KnowledgeBase-PDUs.png
  :alt: UDS PDUs
  :figclass: align-center
  :width: 100%

  Illustration of UDS Protocol Data Units across OSI layers.

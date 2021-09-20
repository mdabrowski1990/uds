UDS OSI Model
=============
Overview of UDS `OSI model <https://en.wikipedia.org/wiki/OSI_model>`_.


UDS OSI Model Layers
--------------------
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+
|   OSI Layer  |            Standards           |              Functionalities              |                Implementation                |
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+
| Layer 7      | Common:                        | Diagnostic message:                       | Module uds.messages:                         |
| Application  |                                |                                           |                                              |
|              | - ISO 14229-1                  | - defining                                | - UdsMessage                                 |
|              |                                |                                           |                                              |
|              | - ISO 27145-3                  | - storing historic data                   | - UdsMessageRecord                           |
|              |                                |                                           |                                              |
|              |                                | - support for various SIDs values         | - RequestSID, POSSIBLE_REQUEST_SIDS          |
|              | CAN specific:                  |                                           |                                              |
|              |                                | - support for bus specific services       | - ResponseSID, POSSIBLE_RESPONSE_SIDS        |
|              | - ISO 14229-3                  |                                           |                                              |
|              |                                |                                           | - NRC                                        |
|              |                                |                                           |                                              |
|              | FlexRay specific:              |                                           | - AddressingType                             |
|              |                                |                                           |                                              |
|              | - ISO 14229-4                  |                                           | - TransmissionDirection                      |
|              |                                |                                           |                                              |
|              |                                |                                           |                                              |
|              | Ethernet specific:             |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 14229-5                  |                                           |                                              |
|              |                                |                                           |                                              |
|              |                                |                                           |                                              |
|              | K-Line specific:               |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 14229-6                  |                                           |                                              |
|              |                                |                                           |                                              |
|              |                                |                                           |                                              |
|              | LIN specific:                  |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 14229-7                  |                                           |                                              |
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+
| Layer 6      | Common:                        | - diagnostic messages data interpretation | *To be provided with database feature.*      |
| Presentation |                                |                                           |                                              |
|              | - ISO 27145-2                  | - messaging database import from a file   |                                              |
|              |                                |                                           |                                              |
|              |                                | - messaging database export to a file     |                                              |
|              | Unique per system:             |                                           |                                              |
|              |                                |                                           |                                              |
|              | - system manufacturer specific |                                           |                                              |
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+
| Layer 5      | Common:                        | - Client simulation                       | *To be provided with Client feature.*        |
| Session      |                                |                                           |                                              |
|              | - ISO 14229-2                  | - Server simulation                       | *To be provided with Server feature.*        |
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+
| Layer 4      | CAN specific:                  | UDS packets:                              | Module uds.messages:                         |
| Transport    |                                |                                           |                                              |
|              | - ISO 15765-2                  | - creating                                | - AbstractUdsPacket                          |
|              |                                | - storing historic data                   |                                              |
|              |                                |                                           | - AbstractUdsPacketRecord                    |
|              | FlexRay specific:              | - support for bus specific packets        |                                              |
|              |                                |                                           | - AbstractUdsPacketType                      |
|              | - 10681-2                      |                                           |                                              |
|              |                                |                                           |                                              |
|              |                                | UDS communication:                        | *To be extended with features:*              |
+--------------+ Ethernet specific:             |                                           |                                              |
| Layer 3      |                                | - diagnostic messages segmentation        | *- Segmentation*                             |
| Network      | - 13400-2                      |                                           |                                              |
|              |                                | - receiving packets                       | *- Transport Interface*                      |
|              |                                |                                           |                                              |
|              | LIN specific:                  | - transmitting packets                    |                                              |
|              |                                |                                           |                                              |
|              | - 17987-2                      | - errors handling                         |                                              |
|              |                                |                                           |                                              |
|              |                                | - errors simulation                       |                                              |
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+
| Layer 2      | CAN specific:                  | Bus handling:                             | External python packages for bus handling:   |
| Data         |                                |                                           |                                              |
|              | - ISO 11898-1                  | - creating frames                         | - `CAN <https://python-can.readthedocs.io>`_ |
|              |                                |                                           |                                              |
|              | - ISO 11898-2                  | - storing historic frames data            |                                              |
|              |                                |                                           | *More driver packages to be decided.*        |
|              | - ISO 11898-3                  | - frames receiving                        |                                              |
|              |                                |                                           |                                              |
|              |                                | - frames transmitting                     |                                              |
|              | FlexRay specific:              |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 17458-2                  |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 17458-4                  |                                           |                                              |
|              |                                |                                           |                                              |
|              |                                |                                           |                                              |
+--------------+ Ethernet specific:             |                                           |                                              |
| Layer 1      |                                |                                           |                                              |
| Physical     | - 13400-3                      |                                           |                                              |
|              |                                |                                           |                                              |
|              |                                |                                           |                                              |
|              | K-Line specific:               |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 14230-2                  |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 14230-1                  |                                           |                                              |
|              |                                |                                           |                                              |
|              |                                |                                           |                                              |
|              | LIN specific:                  |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 17987-3                  |                                           |                                              |
|              |                                |                                           |                                              |
|              | - ISO 17987-4                  |                                           |                                              |
+--------------+--------------------------------+-------------------------------------------+----------------------------------------------+

Columns explanation:
 - OSI Layer - layer of OSI Model
 - Standards - list of standards that describes UDS protocol on given layer
 - Functionalities - list of functionalities provided by UDS on given layer
 - Implementation - which modules/classes/objects implements presented functionalities in the UDS package


Protocol Data Units
-------------------
Each layer of OSI Model defines their own
`Protocol Data Unit (PDU) <https://en.wikipedia.org/wiki/Protocol_data_unit>`_.
To make things simpler for the users and our developers, in the implementation we distinguish following PDUs:

- Application Protocol Data Unit (A_PDU) - called `diagnostic message` or `UDS Message` in the implementation
  and documentation. More information about A_PDU can be found in:

  - :ref:`knowledge base section - diagnostic message <knowledge-base-diagnostic-message>`

  - :ref:`implementation - diagnostic message <implementation-diagnostic-message>`

- Network Protocol Data Unit (N_PDU) - called `UDS packet` in the implementation and documentation.
  More information about N_PDU can be found in:

  - :ref:`knowledge base section - UDS packet <knowledge-base-uds-packet>`

  - :ref:`implementation section - UDS packet <implementation-uds-packet>`

- Data Protocol Data Unit (D_PDU) - called `frame` in the implementation and documentation.
  We do not have any internal `frames <https://en.wikipedia.org/wiki/Frame_(networking)>`_ documentation.
  Implementation of frames is usually provided by external packages.


.. figure:: ../../diagrams/KnowledgeBase-PDUs.png
    :alt: UDS PDUs
    :figclass: align-center
    :width: 100%

    UDS Protocol Data Units on different layers of OSI Model.







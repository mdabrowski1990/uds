UDS OSI Model
=============
Overview of UDS `OSI model <https://en.wikipedia.org/wiki/OSI_model>`_ is presented in the table below.

+--------------+--------------------------------+-------------------------------------------+-----------------------------------------------------------------------------+
|   OSI Layer  |          ISO Standards         |              Functionalities              |                                Implementation                               |
+==============+================================+===========================================+=============================================================================+
| Layer 7      | Common:                        | Diagnostic message:                       | - UdsMessage                                                                |
| Application  |                                |                                           |                                                                             |
|              | - ISO 14229-1                  | - creating                                | - UdsMessageRecord                                                          |
|              |                                |                                           |                                                                             |
|              | - ISO 27145-3                  | - storing historic data                   | - RequestSID                                                                |
|              |                                |                                           |                                                                             |
|              |                                | - various SIDs support                    | - ResponseSID                                                               |
|              | CAN specific:                  |                                           |                                                                             |
|              |                                | - bus specific services                   | - NRC                                                                       |
|              | - ISO 14229-3                  |                                           |                                                                             |
|              |                                |                                           | - AddressingType                                                            |
|              |                                |                                           |                                                                             |
|              | FlexRay specific:              |                                           |                                                                             |
|              |                                |                                           | To be extended in milestones:                                               |
|              | - ISO 14229-4                  |                                           |                                                                             |
|              |                                |                                           | - `Database support <https://github.com/mdabrowski1990/uds/milestone/2>`_   |
|              |                                |                                           |                                                                             |
|              | Ethernet specific:             |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 14229-5                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | K-Line specific:               |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 14229-6                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | LIN specific:                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 14229-7                  |                                           |                                                                             |
+--------------+--------------------------------+-------------------------------------------+-----------------------------------------------------------------------------+
| Layer 6      | Common:                        | - diagnostic messages data interpretation | To be implemented in milestones:                                            |
| Presentation |                                |                                           |                                                                             |
|              | - ISO 27145-2                  | - messaging database import from a file   | - `Database support <https://github.com/mdabrowski1990/uds/milestone/2>`_   |
|              |                                |                                           |                                                                             |
|              |                                | - messaging database export to a file     |                                                                             |
|              | Unique per system:             |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - system manufacturer specific |                                           |                                                                             |
+--------------+--------------------------------+-------------------------------------------+-----------------------------------------------------------------------------+
| Layer 5      | Common:                        | - Client simulation                       | To be implemented in milestones:                                            |
| Session      |                                |                                           |                                                                             |
|              | - ISO 14229-2                  | - Server simulation                       | - `Client simulation <https://github.com/mdabrowski1990/uds/milestone/8>`_  |
|              |                                |                                           |                                                                             |
|              |                                |                                           | - `Server simulation <https://github.com/mdabrowski1990/uds/milestone/7>`_  |
+--------------+--------------------------------+-------------------------------------------+-----------------------------------------------------------------------------+
| Layer 4      | CAN specific:                  | UDS packets:                              | - AbstractUdsPacket                                                         |
| Transport    |                                |                                           |                                                                             |
|              | - ISO 15765-2                  | - creating                                | - AbstractUdsPacketRecord                                                   |
|              |                                | - storing historic data                   |                                                                             |
|              |                                |                                           | - AbstractUdsPacketType                                                     |
|              | FlexRay specific:              | - support for bus specific packets        |                                                                             |
|              |                                |                                           |                                                                             |
|              | - 10681-2                      |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                | UDS communication:                        |                                                                             |
|              | Ethernet specific:             |                                           |                                                                             |
+--------------+                                |                                           |                                                                             |
| Layer 3      | - 13400-2                      | - diagnostic messages segmentation        |                                                                             |
| Network      |                                |                                           |                                                                             |
|              |                                | - receiving packets                       |                                                                             |
|              | LIN specific:                  |                                           |                                                                             |
|              |                                | - transmitting packets                    |                                                                             |
|              | - 17987-2                      |                                           |                                                                             |
|              |                                | - errors handling                         |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                | - errors simulation                       |                                                                             |
+--------------+--------------------------------+-------------------------------------------+-----------------------------------------------------------------------------+
| Layer 2      | CAN specific:                  | Bus handling:                             | External python packages for bus handling:                                  |
| Data         |                                |                                           |                                                                             |
|              | - ISO 11898-1                  | - creating frames                         | - `CAN <https://python-can.readthedocs.io>`_                                |
|              |                                |                                           |                                                                             |
|              | - ISO 11898-2                  | - storing historic frames data            |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 11898-3                  | - frames receiving                        |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                | - frames transmitting                     |                                                                             |
|              | FlexRay specific:              |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 17458-2                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 17458-4                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                |                                           |                                                                             |
+--------------+ Ethernet specific:             |                                           |                                                                             |
| Layer 1      |                                |                                           |                                                                             |
| Physical     | - 13400-3                      |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | K-Line specific:               |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 14230-2                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 14230-1                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | LIN specific:                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 17987-3                  |                                           |                                                                             |
|              |                                |                                           |                                                                             |
|              | - ISO 17987-4                  |                                           |                                                                             |
+--------------+--------------------------------+-------------------------------------------+-----------------------------------------------------------------------------+

Columns explanation:
 - OSI Layer - layer of OSI Model
 - Standards - list of standards that describes UDS protocol on given layer
 - Functionalities - list of functionalities provided by UDS on given layer
 - Implementation - which modules/classes/objects implements these functionalities in the UDS package

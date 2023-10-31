UDS OSI Model
=============
Overview of UDS `OSI model <https://en.wikipedia.org/wiki/OSI_model>`_.


.. _knowledge-base-uds-standards:

UDS Standards
-------------
UDS is defined by multiple standards which are the main source of information and requirements about this protocol.
Full list of standards is included in the table below:

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

Where:
 - OSI Layer - OSI Model Layer for which standards are relevant
 - Common - standards mentioned in this column are always relevant for UDS communication regardless of bus used
 - CAN - standards which are specific for UDS on CAN implementation
 - FlexRay - standards which are specific for UDS on FlexRay implementation
 - Ethernet - standards which are specific for UDS on IP implementation
 - K-Line - standards which are specific for UDS on K-Line implementation
 - LIN - standards which are specific for UDS on LIN implementation


UDS Functionalities
-------------------
An overview of features that are required to fully implement UDS protocol is presented in the table below:

+--------------+-------------------------------------------+-------------------------------------------------------+
|   OSI Layer  |              Functionalities              |                     Implementation                    |
+==============+===========================================+=======================================================+
| Layer 7      | - diagnostic messages support             | - :mod:`uds.message`                                  |
| Application  |                                           |                                                       |
+--------------+-------------------------------------------+-------------------------------------------------------+
| Layer 6      | - diagnostic messages data interpretation | *To be provided with Database feature.*               |
| Presentation |                                           |                                                       |
|              | - messaging database import from a file   |                                                       |
|              |                                           |                                                       |
|              | - messaging database export to a file     |                                                       |
+--------------+-------------------------------------------+-------------------------------------------------------+
| Layer 5      | - Client simulation                       | *To be provided with Client feature.*                 |
| Session      |                                           |                                                       |
|              | - Server simulation                       | *To be provided with Server feature.*                 |
+--------------+-------------------------------------------+-------------------------------------------------------+
| Layer 4      | - UDS packet support                      | - :mod:`uds.packet`                                   |
| Transport    |                                           |                                                       |
|              | - bus specific segmentation               | - :mod:`uds.segmentation`                             |
|              |                                           |                                                       |
|              | - bus specific packets transmission       | - :mod:`uds.transport_interface`                      |
|              |                                           |                                                       |
|              |                                           | - :mod:`uds.can`                                      |
|              |                                           |                                                       |
|              |                                           | *Currently under development.*                        |
+--------------+                                           |                                                       |
| Layer 3      |                                           | *To be extended with support for:*                    |
| Network      |                                           |                                                       |
|              |                                           | - *Ethernet*                                          |
|              |                                           |                                                       |
|              |                                           | - *LIN*                                               |
|              |                                           |                                                       |
|              |                                           | - *K-Line*                                            |
|              |                                           |                                                       |
|              |                                           | - *FlexRay*                                           |
+--------------+-------------------------------------------+-------------------------------------------------------+
| Layer 2      | - frames transmission                     | External python packages for bus handling:            |
| Data         |                                           |                                                       |
|              | - frames receiving                        | -  CAN:                                               |
+--------------+                                           |                                                       |
| Layer 1      |                                           |   - `python-can <https://python-can.readthedocs.io>`_ |
| Physical     |                                           |                                                       |
|              |                                           | *More packages to be decided.*                        |
+--------------+-------------------------------------------+-------------------------------------------------------+

Where:
 - OSI Layer - considered OSI Model Layer
 - Functionalities - functionalities required in the implementation to handle considered UDS OSI layer
 - Implementation - UDS package implementation that provides mentioned functionalities


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

  - implementation - :mod:`uds.packet`

- Data Protocol Data Unit (D_PDU) - called `frame` in the implementation and documentation.
  We do not have any internal `frames <https://en.wikipedia.org/wiki/Frame_(networking)>`_ documentation.
  Implementation of frames is usually provided by external packages.

.. figure:: ../../diagrams/KnowledgeBase-PDUs.png
    :alt: UDS PDUs
    :figclass: align-center
    :width: 100%

    UDS Protocol Data Units on different layers of OSI Model.

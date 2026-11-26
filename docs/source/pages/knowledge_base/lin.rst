.. _knowledge-base-dolin:

Diagnostics over LIN
====================
Diagnostics over LIN (DoLIN), also known as LIN Transport Protocol (LIN-TP, ISO 17987-2),
is the transport layer communication protocol used by UDS for
:ref:`message segmentation <knowledge-base-segmentation>` on LIN networks.
In other words, DoLIN provides the adaptation that allows UDS to operate on LIN.
It is illustrated in the :ref:`UDS OSI Model <knowledge-base-osi-model>`.

LIN is a low-cost serial communication protocol primarily designed for communication
between electronic control units (ECUs) and peripheral devices in automotive networks.
It is commonly used for applications that do not require the bandwidth or complexity of CAN.

LIN uses a master-slave communication model, where the master node controls bus access and initiates
all frame transmissions according to a predefined schedule.


.. _knowledge-base-lin-versions:

LIN Versions
------------
`LIN Bus <https://en.wikipedia.org/wiki/Local_Interconnect_Network>`_ was released in multiple version over the years.


LIN 1.3
```````
- Supports classic checksum only
- Supports basic frame communication with up to 8 data bytes

:download:`LIN 1.3 Specification <../../specs/LIN/LIN_1_3.pdf>`


LIN 2.0
```````
- Introduces enhanced checksum
- Introduces diagnostic communication and transport protocol
- Introduces slave node configuration services
- Introduces byte array signals
- Introduces sporadic and event-triggered frames
- Introduces automatic baud-rate detection

:download:`LIN 2.0 Specification <../../specs/LIN/LIN_2_0.pdf>`


LIN 2.1
```````
- Extends slave node configuration services
- Introduces three diagnostic classes (I, II and III)
- Introduces functional diagnostic addressing
- Improves event-triggered frame collision resolution

:download:`LIN 2.1 Specification <../../specs/LIN/LIN_2_1.pdf>`


LIN 2.2A
````````
- Updates physical-layer bit-sampling requirements
- Corrects wake-up signal definition

:download:`LIN 2.2A Specification <../../specs/LIN/LIN_2_2_A.pdf>`


.. _knowledge-base-lin-frame:

LIN Frame
---------
A LIN frame consists of a header and a response.


LIN Header
``````````
The header is always transmitted by Master node.

The header contains the following fields:

- **Break** - signals the beginning of a new frame
- **Sync** - fixed synchronization byte (0x55), used by slave nodes to synchronize their baud rate with the master
- **Protected Identifier (PID)** - contains a 6-bit frame identifier and 2 parity bits


LIN Response
````````````
The response part is transmitted by either Master or Slave node.

The response contains:

- **Data** - payload containing up to 8 bytes
- **Checksum** - used to detect transmission errors

There are two checksum variants:

- **Classic checksum** - calculated over the data bytes only
- **Enhanced checksum** - calculated over the protected identifier and data bytes

Diagnostic frames always use the classic checksum for backwards compatibility reasons.


.. _knowledge-base-lin-packet:

LIN Packet
----------
LIN Packets (N_PDUs) are :ref:`LIN Frames <knowledge-base-lin-frame>` exchanged during DoLIN communication.

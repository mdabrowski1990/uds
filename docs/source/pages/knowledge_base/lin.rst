.. _knowledge-base-dolin:

Diagnostics over LIN
====================
Diagnostics over LIN (DoLIN), also known as UDS on LIN (UDSonLIN, ISO 14229-7),
is the transport layer communication protocol used by UDS for
:ref:`message segmentation <knowledge-base-segmentation>` on LIN networks.
In other words, DoLIN provides the adaptation that allows UDS to operate on LIN.
It is illustrated in the :ref:`UDS OSI Model <knowledge-base-osi-model>`.

LIN is a low-cost serial communication protocol primarily designed for communication
between electronic control units (ECUs) and peripheral devices in automotive networks.
It is commonly used for applications that do not require the bandwidth or complexity of CAN.

LIN uses a master-slave communication model, where the master node controls bus access and initiates
all frame transmissions according to a predefined schedule.


.. _knowledge-base-lin-frame:

LIN Frame
---------
A LIN frame consists of a header transmitted by the master node and a response
transmitted by either the master or a slave node.

The header contains the following fields:

- **Break** - signals the beginning of a new frame.
- **Sync** - fixed synchronization byte (0x55), used by slave nodes to synchronize their baud rate with the master.
- **Protected Identifier (PID)** - contains a 6-bit frame identifier and 2 parity bits.

The response contains:

- **Data** - payload containing up to 8 bytes.
- **Checksum** - used to detect transmission errors.

There are two checksum variants:

- **Classic checksum** - calculated over the data bytes only.
- **Enhanced checksum** - calculated over the protected identifier and data bytes.

Diagnostic frames always use the classic checksum.

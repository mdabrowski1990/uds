.. _knowledge-base-uds-packet:

UDS Packet
==========
UDS packet might also be called Network Protocol Data Unit (N_PDU). The packets are created during
:ref:`segmentation <knowledge-base-segmentation>` of a :ref:`diagnostic message <knowledge-base-diagnostic-message>`.
Each :ref:`diagnostic message <knowledge-base-diagnostic-message>` consists of at least one UDS Packet (N_PDU).
There are some packets which does not carry any diagnostic message data as they are used to manage the flow of
other packets.

UDS packet consists of following fields:
 - `Network Address Information`_ (N_AI) - packet addressing
 - `Network Data Field`_ (N_Data) - packet date
 - `Network Protocol Control Information`_ (N_PCI) - packet type


Network Address Information
---------------------------
Network Address Information (N_AI) contains address information which identifies the recipient(s) and the sender
between whom data exchange takes place. It also describes communication model (e.g. whether response is required)
for the message.


Network Data Field
------------------
Network Data Field (N_Data) carries diagnostic message data. It might be an entire diagnostic message data
(if a :ref:`diagnostic message <knowledge-base-diagnostic-message>` fits into one packet) or just a part of it
(if :ref:`segmentation <knowledge-base-segmentation>` had to be used to divide
a :ref:`diagnostic message <knowledge-base-diagnostic-message>` into smaller parts).


.. _knowledge-base-n-pci:

Network Protocol Control Information
------------------------------------
Network Protocol Control Information (N_PCI) identifies the type of `UDS packet`_ (Network Protocol Data Unit).
N_PCI values and their interpretation are bus specific.


UDS Packet on CAN
-----------------
In this chapter you will find information about UDS packets specific for CAN bus, therefore
**applicable only for UDS packets that are transmitted over CAN bus**.


.. _knowledge-base-can-addressing:

CAN Packet Addressing Formats
`````````````````````````````
The exchange of UDS Packets on CAN is supported by three addressing formats:
 - :ref:`Normal addressing <knowledge-base-can-normal-addressing>`
 - :ref:`Extended addressing <knowledge-base-can-extended-addressing>`
 - :ref:`Mixed addressing <knowledge-base-can-mixed-addressing>`


.. _knowledge-base-can-normal-addressing:

Normal addressing
'''''''''''''''''


.. _knowledge-base-can-extended-addressing:

Extended addressing
'''''''''''''''''''


.. _knowledge-base-can-mixed-addressing:

Mixed addressing
''''''''''''''''''''


.. _knowledge-base-can-data-field:

CAN Data Field
``````````````
CAN frames that are exchanged during UDS communication must have Data Length Code (DLC) equal to 8 (for CLASSICAL CAN
and CAN FD) or greater (for CAN FD). For details, refer to the table below.

+-----+--------------------------------------------------------------------+
| DLC |                             Description                            |
+=====+====================================================================+
|  <8 | *Invalid*                                                          |
|     |                                                                    |
|     | Values in this range are invalid for UDS communication.            |
+-----+--------------------------------------------------------------------+
|  8  | *Configured CAN frame maximum payload length of 8 bytes*           |
|     |                                                                    |
|     | For the use with CLASSICAL CAN and CAN FD type frames.             |
+-----+--------------------------------------------------------------------+
| >8  | *Configured CAN frame maximum payload length greater than 8 bytes* |
|     |                                                                    |
|     | For the use with CAN FD type frames only.                          |
|     |                                                                    |
|     | Possible values DLC values: 12, 16, 20, 24, 32, 48, 64             |
+-----+--------------------------------------------------------------------+

Where:
 - DLC - Data Length Code of a CAN frame, it is equal to number of data bytes carried by this CAN frame

.. note:: Number of bytes that carry diagnostic message payload depends on a type and format of a CAN packet as it is
   presented in :ref:`the table with CAN packets formats <knowledge-base-can-packets-format>`.


.. _knowledge-base-can-n-pci:

CAN Packet Types
````````````````
According to ISO 15765-2, CAN bus supports 4 types of UDS packets.

List of `Network Protocol Control Information`_ supported by CAN bus:
 - 0x0 - :ref:`Single Frame <knowledge-base-can-single-frame>`
 - 0x1 - :ref:`First Frame <knowledge-base-can-first-frame>`
 - 0x2 - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
 - 0x3 - :ref:`Flow Control <knowledge-base-can-flow-control>`
 - 0x4-0xF - values range reserved for future extension by ISO 15765

The format of all CAN packets is presented in the table below.

.. _knowledge-base-can-packets-format:

+-------------------+---------------------+---------+---------+---------+---------+---------+-----+
|     CAN N_PDU     |       Byte #1       | Byte #2 | Byte #3 | Byte #4 | Byte #5 | Byte #6 | ... |
|                   +----------+----------+         |         |         |         |         |     |
|                   | Bits 7-4 | Bits 3-0 |         |         |         |         |         |     |
+===================+==========+==========+=========+=========+=========+=========+=========+=====+
| Single Frame      | 0x0      | SF_DL    |         |         |         |         |         |     |
|                   |          |          |         |         |         |         |         |     |
| *DLC ≤ 8*         |          |          |         |         |         |         |         |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| Single Frame      | 0x0      | 0x0      | SF_DL   |         |         |         |         |     |
|                   |          |          |         |         |         |         |         |     |
| *DLC > 8*         |          |          |         |         |         |         |         |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| First Frame       | 0x1      | FF_DL              |         |         |         |         |     |
|                   |          |                    |         |         |         |         |     |
| *FF_DL ≤ 4095*    |          |                    |         |         |         |         |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| First Frame       | 0x1      | 0x0      | 0x00    | FF_DL                                 |     |
|                   |          |          |         |                                       |     |
| *FF_DL > 4095*    |          |          |         |                                       |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| Consecutive Frame | 0x2      | SN       |         |         |         |         |         |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| Flow Control      | 0x3      | FS       | BS      | ST_min  | N/A     | N/A     | N/A     | N/A |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+

Where:
 - DLC - Data Length Code of a CAN frame, it is equal to number of data bytes carried by this CAN frame
 - SF_DL - :ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>`
 - FF_DL - :ref:`First Frame Data Length <knowledge-base-can-first-frame-data-length>`
 - SN - :ref:`Sequence Number <knowledge-base-can-sequence-number>`
 - FS - :ref:`Flow Status <knowledge-base-can-flow-status>`
 - BS - :ref:`Block Size <knowledge-base-can-block-size>`
 - ST_min - :ref:`Separation Time minimum <knowledge-base-can-st-min>`
 - N/A - Not Applicable (byte does not carry any information)


.. _knowledge-base-can-single-frame:

Single Frame
''''''''''''
Single Frame (SF) shall be used by CAN entities to transmit a diagnostic message with a payload short enough to fit it
into a single CAN packet.
In other words, Single Frame carries payload of an entire diagnostic message.

.. note:: Maximal number of diagnostic message payload bytes that might be carried by SF depends on
   :ref:`its addressing format <knowledge-base-can-addressing>` and number of
   :ref:`data bytes carried by CAN message <knowledge-base-can-data-field>`.


.. _knowledge-base-can-single-frame-data-length:

Single Frame Data Length
........................
is 4-bit or 8-bit value which specifies number of diagnostic message payload bytes
   transmitted by a Single Frame


.. _knowledge-base-can-first-frame:

First Frame
'''''''''''


.. _knowledge-base-can-first-frame-data-length:

First Frame Data Length
.......................
is 12-bit or 4-byte value which specifies number of diagnostic message payload bytes
   transmitted by a First Frame and Consecutive Frames


.. _knowledge-base-can-consecutive-frame:

Consecutive Frame
'''''''''''''''''


.. _knowledge-base-can-sequence-number:

Sequence Number
...............
 is 4-bit value used to specify order of Consecutive Frames


.. _knowledge-base-can-flow-control:

Flow Control
''''''''''''


.. _knowledge-base-can-flow-status:

Flow Status
...........
is 4-bit value that is used to inform a sending network entity whether it can proceed with
   a Consecutive Frames transmission


.. _knowledge-base-can-block-size:

Block Size
..........
 is a one byte value specified by receiving entity that informs about number of Consecutive Frames
   to be sent in a one block of packets


.. _knowledge-base-can-st-min:

Separation Time Minimum
.......................
 is a one byte value specified by receiving entity that



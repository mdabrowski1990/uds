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
 - `Network Protocol Control Information`_ (N_PCI) - packet type
 - `Network Data Field`_ (N_Data) - packet date


Network Address Information
---------------------------
Network Address Information (N_AI) contains address information which identifies the recipient(s) and the sender
between whom data exchange takes place. It also describes communication model (e.g. whether response is required)
for the message.


.. _knowledge-base-n-pci:

Network Protocol Control Information
------------------------------------
Network Protocol Control Information (N_PCI) identifies the type of `UDS packet`_ (Network Protocol Data Unit).
N_PCI values and their interpretation are bus specific.


Network Data Field
------------------
Network Data Field (N_Data) carries diagnostic message data. It might be an entire diagnostic message data
(if a :ref:`diagnostic message <knowledge-base-diagnostic-message>` fits into one packet) or just a part of it
(if :ref:`segmentation <knowledge-base-segmentation>` had to be used to divide
a :ref:`diagnostic message <knowledge-base-diagnostic-message>` into smaller parts).


UDS Packet on CAN
-----------------
In this chapter you will find information about UDS packets specific for CAN bus, therefore
**applicable only for UDS packets that are transmitted over CAN bus**.


CAN Data Field
``````````````
The table below presents possible number of bytes (data length) for CAN frames that carry UDS packet over CAN bus.

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
|     | Possible values TX_DL values: 12, 16, 20, 24, 32, 48, 64           |
+-----+--------------------------------------------------------------------+

Where:
 - DLC - data length code of CAN frame equal to number of data bytes carried by CAN frame


.. _knowledge-base-can-n-pci:

CAN Packet Types
````````````````
List of `Network Protocol Control Information`_ values defined by ISO 15765 for CAN bus:
 - 0x0 - :ref:`Single Frame <knowledge-base-can-single-frame>`
 - 0x1 - :ref:`First Frame <knowledge-base-can-first-frame>`
 - 0x2 - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
 - 0x3 - :ref:`Flow Control <knowledge-base-can-flow-control>`
 - 0x4-0xF - values range reserved for future extension by ISO 15765

The format of all CAN packets is presented in the table below.

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
 - DLC - TODO
 - SF_DL -
 - FF_DL -
 - SN -
 - FS -
 - BS -
 - ST_min -
 - N/A -


.. _knowledge-base-can-single-frame:

Single Frame
''''''''''''
Single Frame (SF) shall be used by CAN nodes to transmit UDS message that fit




.. _knowledge-base-can-first-frame:

First Frame
'''''''''''


.. _knowledge-base-can-consecutive-frame:

Consecutive Frame
'''''''''''''''''


.. _knowledge-base-can-flow-control:

Flow Control
''''''''''''


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


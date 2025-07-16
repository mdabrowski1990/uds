.. _knowledge-base-packet:

Packet (N_PDU)
==============
In ISO Standards, the name Network :ref:`Protocol Data Unit <knowledge-base-pdu>` (N_PDU in short) is used.
For various reasons we decided to use Packet name instead.

The packets are created during :ref:`segmentation <knowledge-base-segmentation>` of a
:ref:`diagnostic message <knowledge-base-diagnostic-message>`.
Each :ref:`diagnostic message <knowledge-base-diagnostic-message>` consists of at least one Packet (N_PDU).

Packet contains following information:

  - `Network Address Information`_ (N_AI) - packet addressing
  - `Network Data Field`_ (N_Data) - packet data
  - `Network Protocol Control Information`_ (N_PCI) - packet type


.. _knowledge-base-n-ai:

Network Address Information
---------------------------
Network Address Information (N_AI) contains address information which identifies the recipient(s) and the sender
between whom data exchange takes place. It also describes communication model (e.g. whether response is required)
for the message.


.. _knowledge-base-n-data:

Network Data Field
------------------
Network Data Field (N_Data) carries diagnostic message data. It might be an entire diagnostic message data
(if a :ref:`diagnostic message <knowledge-base-diagnostic-message>` fits into one packet) or just a part of it
(if :ref:`segmentation <knowledge-base-segmentation>` had to be used to divide
a :ref:`diagnostic message <knowledge-base-diagnostic-message>` into smaller parts).

For some communication buses, some packets might not carry any data (e.g.
:ref:`CAN Flow Control <knowledge-base-can-flow-control>`) as they are used to manage the flow of packets.


.. _knowledge-base-n-pci:

Network Protocol Control Information
------------------------------------
Network Protocol Control Information (N_PCI) identifies the type of `Packet (N_PDU)`_.
N_PCI values and their interpretation are bus specific.


.. _knowledge-base-can-packet:

CAN Packet
----------
In this chapter you will find information about packets exchanged during UDS communication over CAN.
This part is specific for CAN bus and Diagnostic on CAN (ISO 15765).


.. _knowledge-base-can-frame:

CAN Frame
`````````
`CAN data frames <https://elearning.vector.com/mod/page/view.php?id=345>`_ are the only type of CAN frames that are used
during UDS communication. CAN data frames consist of many different fields, but the key in our case (used during
UDS communication) are listed below:

- CAN Identifier (CAN ID)

  CAN ID is a field that informs every receiving CAN node about a sender and a content of frames.
  CAN nodes shall filter out and ignore CAN frames that are not relevant for them. In a normal situation, a CAN node
  detects a transmission of incoming CAN frames and once the identifier value (of a CAN frame) is decoded,
  the CAN node shall stop further listening to the frame if the CAN node is not a recipient of the frame.

  There are two formats of CAN ID:

  - Standard (11-bit Identifier)
  - Extended (29-bit identifier)

- Data Length Code (DLC)

  Data Length Code (DLC) informs about number of CAN frame payload bytes that CAN Data Field contains.

- CAN Data Field

  CAN Data consists of CAN frame payload bytes. The number of bytes that CAN Data Field contains is determined by
  frame's DLC values as presented in the table:

  +-----+--------------------------+----------------------------+---------------------+
  | DLC | Number of CAN Data bytes | Supported by CLASSICAL CAN | Supported by CAN FD |
  +=====+==========================+============================+=====================+
  | 0x0 |             0            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x1 |             1            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x2 |             2            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x3 |             3            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x4 |             4            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x5 |             5            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x6 |             6            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x7 |             7            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x8 |             8            |             YES            |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0x9 |            12            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0xA |            16            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0xB |            20            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0xC |            24            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0xD |            32            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0xE |            48            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+
  | 0xF |            64            |             NO             |         YES         |
  +-----+--------------------------+----------------------------+---------------------+

.. note:: To learn more about CAN bus and CAN frame structure, we encourage you to read
  `CAN bus specification <http://esd.cs.ucr.edu/webres/can20.pdf>`_ and visit
  `e-learning portal of Vector Informatik GmbH <https://elearning.vector.com/>`_.


.. _knowledge-base-can-addressing:

CAN Packet Addressing Formats
`````````````````````````````
Each CAN Packet Addressing Format describes a different way of providing `Network Address Information`_ to all
recipients of CAN Packets.

The exchange of packets on CAN is supported by three addressing formats:

- :ref:`Normal addressing <knowledge-base-can-normal-addressing>`
- :ref:`Extended addressing <knowledge-base-can-extended-addressing>`
- :ref:`Mixed addressing <knowledge-base-can-mixed-addressing>`

.. warning:: Addressing format must be predefined and configured before any CAN packet is received as every
  CAN packet addressing format determines a different way of decoding CAN packets information
  (`Network Address Information`_, `Network Data Field`_ and `Network Protocol Control Information`_).

.. note:: Regardless of addressing format used, to transmit
  a :ref:`functionally addressed <knowledge-base-functional-addressing>` message over CAN, a sender is allowed to use
  :ref:`Single Frame <knowledge-base-can-single-frame>` packets only.

.. seealso:: `ISO 15765-4 <https://www.iso.org/standard/78384.html>`_ contains detailed information about
  CAN addressing formats.


.. _knowledge-base-can-normal-addressing:

Normal Addressing
'''''''''''''''''
Normal Addressing is used when direct communication with servers is possible (Diagnostic Tester is connected to
the same CAN network as ECUs).

If normal addressing format is used, then the value of CAN Identifier carries the entire `Network Address Information`_.
Basing on CAN Identifier value, it is possible to distinguish :ref:`an addressing type <knowledge-base-addressing>`,
a sender and a target/targets entities of a diagnostic packet/message.

.. note:: With normal addressing, both 11-bit (standard) and 29-bit (extended) CAN Identifiers are allowed.

Following parameters specifies `Network Address Information`_ when Normal Addressing is used:

- CAN ID - informs about transmitting and receiving nodes

ISO 15765-4 recommends to use following CAN Identifiers for Normal Addressing:

- 0x7DF - functionally addressed request message
- 0x7E0 - physical request to Engine Control Module
- 0x7E8 - physical response from Engine Control Module
- 0x7E1 - physical request to Transmission Control Module
- 0x7E9 - physical response from Transmission Control Module
- 0x7E2 -  physical request to ECU#3
- 0x7EA - physical response from ECU#3
- 0x7E3 -  physical request to ECU#4
- 0x7EB - physical response from ECU#4
- 0x7E4 -  physical request to ECU#5
- 0x7EC - physical response from ECU#5
- 0x7E5 -  physical request to ECU#6
- 0x7ED - physical response from ECU#6
- 0x7E6 -  physical request to ECU#7
- 0x7EE - physical response from ECU#7
- 0x7E7 -  physical request to ECU#8
- 0x7EF - physical response from ECU#8

.. note:: Correspondence between `Network Address Information`_ and the value of CAN Identifier is left open for
  a network designer unless :ref:`normal fixed addressing <knowledge-base-can-normal-fixed-addressing>` sub-format
  is used.

.. note:: `Network Protocol Control Information`_ is placed in the **first byte** of
  :ref:`CAN frame data field <knowledge-base-can-data-field>` if normal addressing format is used.


.. _knowledge-base-can-normal-fixed-addressing:

Normal Fixed Addressing
.......................
Normal fixed addressing format is a special case of :ref:`normal addressing <knowledge-base-can-normal-addressing>`
in which the mapping of the address information into the CAN identifier is further defined.

.. note:: With normal fixed addressing, only 29-bit (extended) CAN Identifiers are allowed.

Following parameters specifies `Network Address Information`_ when Normal Fixed Addressing is used:

- CAN ID (with embedded **Target Address** and **Source Address**) - **Source Address** informs about transmitting node
  and **Target Address** informs about receiving node

CAN Identifier values used for UDS communication using normal fixed addressing:

- For :ref:`physical addressed <knowledge-base-physical-addressing>` messages, CAN Identifier value is defined
  as presented below:

  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  |                | Priority | Reserved Bit | Data Page | Protocol data | Target  | Source  | Data          |
  |                |          |              |           | unit format   | Address | Address |               |
  +================+==========+==============+===========+===============+=========+=========+===============+
  | Bits number    |     3    |       1      |     1     |       8       |    8    |    8    |     16-512    |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | Content        |   0 - 7  |       0      |     0     |      218      |   N_TA  |   N_SA  | N_PCI, N_Data |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | CAN field      |                              CAN Identifier                             |    CAN Data   |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | CAN ID bits    |   28-26  |      25      |     24    |     23-16     |   15-8  |   7-0   |      ---      |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | CAN data bytes |    ---   |      ---     |    ---    |      ---      |   ---   |   ---   |      1-64     |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+

  .. code-block::

    # assuming priority parameter equals 0
    CAN_ID = 0xDATTSS

    # assuming priority parameter equals 6 (default value)
    CAN_ID = 0x18DATTSS

    # assuming priority parameter equals 7
    CAN_ID = 0x1CDATTSS


- For :ref:`functional addressed <knowledge-base-functional-addressing>` messages, CAN Identifier value is defined
  as presented below:

  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  |                | Priority | Reserved Bit | Data Page | Protocol data | Target  | Source  | Data          |
  |                |          |              |           | unit format   | Address | Address |               |
  +================+==========+==============+===========+===============+=========+=========+===============+
  | Bits number    |     3    |       1      |     1     |       8       |    8    |    8    |     16-512    |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | Content        |   0 - 7  |       0      |     0     |      219      |   N_TA  |   N_SA  | N_PCI, N_Data |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | CAN field      |                              CAN Identifier                             |    CAN Data   |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | CAN ID bits    |   28-26  |      25      |     24    |     23-16     |   15-8  |   7-0   |      ---      |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+
  | CAN data bytes |    ---   |      ---     |    ---    |      ---      |   ---   |   ---   |      1-64     |
  +----------------+----------+--------------+-----------+---------------+---------+---------+---------------+

  .. code-block::

    # assuming priority parameter equals 0
    CAN_ID = 0xDBTTSS

    # assuming priority parameter equals 6 (default value)
    CAN_ID = 0x18DBTTSS

    # assuming priority parameter equals 7
    CAN_ID = 0x1CDBTTSS

where:

- CAN_ID - value of **CAN Identifier**
- TT - two (hexadecimal) digits of a 8-bit **Target Address** value
- SS - two (hexadecimal) digits of a 8-bit **Source Address** value
- N_TA - Network **Target Address** parameter
- N_SA - Network **Source Address** parameter
- :ref:`N_PCI <knowledge-base-n-pci>` - Network Protocol Control Information
- :ref:`N_Data <knowledge-base-n-data>` - Network Data Field

ISO 15765-4 recommends to use following parameters for Normal Fixed Addressing:

- N_TA = 0xF1 and N_SA = 0xF1 - diagnostic tester parameters
- CAN ID = 0x18DB33F1 (N_TA=0x33, N_SA=0xF1) - functionally addressed request message
- CAN ID = 0x18DA??F1 (replace ?? with ECU's target address) - physically addressed request messages
- CAN ID = 0x18DAF1?? (replace ?? with ECU's source address) - physically addressed response messages


.. _knowledge-base-can-extended-addressing:

Extended Addressing
'''''''''''''''''''
Extended Addressing is used when direct communication with servers is not possible and Gateway is passing on messages
exchanged by diagnostic tester and targeted ECUs.

If extended addressing format is used, then the value of **the first CAN frame byte informs about a target** of
a packet and remaining `Network Address Information`_ (a sending entity and
:ref:`an addressing type <knowledge-base-addressing>`) are determined by CAN Identifier value.

.. note:: With extended addressing, both 11-bit (standard) and 29-bit (extended) CAN Identifiers are allowed.

Following parameters specifies `Network Address Information`_ when Extended Addressing is used:

- CAN ID - identifies network and message direction
- Target Address (located in the first data byte of a :ref:`CAN Frame <knowledge-base-can-frame>`) - informs about
  receiving and transmitting nodes within the network

.. note:: `Network Protocol Control Information`_ is placed in the **second byte** of
   :ref:`CAN frame data field <knowledge-base-can-data-field>` if extended addressing format is used.


.. _knowledge-base-can-mixed-addressing:

Mixed Addressing
''''''''''''''''
Mixed Addressing (just like Extended Addressing) is used when direct communication with servers is not possible and
Gateway is passing on messages exchanged by diagnostic tester and targeted ECUs.

Mixed addressing format specifies that **the first byte of a CAN frame is an extension** of
`Network Address Information`_.

.. note:: `Network Protocol Control Information`_ is placed in the **second byte** of
   :ref:`CAN frame data field <knowledge-base-can-data-field>` if mixed addressing format is used.


.. _knowledge-base-can-mixed-11-bit-addressing:

Mixed Addressing - 11-bit CAN Identifier
........................................
If mixed addressing format is used with 11-bit CAN Identifiers, then the value of **the first CAN frame byte extends**
the CAN Identifier and a combination of these data forms the entire `Network Address Information`_ of a CAN packet.

Following parameters specifies `Network Address Information`_ when Extended Addressing is used:

- CAN ID - informs about transmitting and receiving nodes withing the network (combining with **Addressing Extension**
  identifies those)
- Addressing Extension (located in the first data byte of a :ref:`CAN Frame <knowledge-base-can-frame>`) - selects
  network (the same value is used during communication in both directions)


.. _knowledge-base-can-mixed-29-bit-addressing:

Mixed Addressing - 29-bit CAN Identifier
........................................
If mixed addressing format is used with 29-bit CAN Identifiers, then the value of **the first CAN frame byte extends**
the CAN Identifier (that contains **Target Address** and **Sender Address** values) and
a combination of these data forms the entire `Network Address Information`_ of a CAN packet.

Following parameters specifies `Network Address Information`_ when Extended Addressing is used:

- CAN ID (with embedded **Target Address** and **Source Address**) - **Source Address** informs about transmitting node
  and **Target Address** informs about receiving node in the network (combining with **Addressing Extension** identifies
  those)
- Addressing Extension (located in the first data byte of a :ref:`CAN Frame <knowledge-base-can-frame>`) - selects
  network (the same value is used during communication in both directions)

CAN Identifier values used for UDS communication using mixed 29-bit addressing:

- For :ref:`physical addressed <knowledge-base-physical-addressing>` messages, CAN Identifier value is defined
  as presented below:

  +----------------+----------+--------------+-----------+---------------+---------+---------+----------------------+
  |                | Priority | Reserved Bit | Data Page | Protocol data | Target  | Source  | Data                 |
  |                |          |              |           | unit format   | Address | Address |                      |
  +================+==========+==============+===========+===============+=========+=========+======+===============+
  | Bits number    |     3    |       1      |     1     |       8       |    8    |    8    |   8  |     16-504    |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | Content        |   0 - 7  |       0      |     0     |      206      |   N_TA  |   N_SA  | N_AE | N_PCI, N_Data |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | CAN field      |                              CAN Identifier                             |       CAN Data       |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | CAN ID bits    |   28-26  |      25      |     24    |     23-16     |   15-8  |   7-0   |  --- |      ---      |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | CAN data bytes |    ---   |      ---     |    ---    |      ---      |   ---   |   ---   |   1  |      2-64     |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+

  .. code-block::

    # assuming priority parameter equals 0
    CAN_ID = 0xCETTSS

    # assuming priority parameter equals 6 (default value)
    CAN_ID = 0x18CETTSS

    # assuming priority parameter equals 7
    CAN_ID = 0x1CCETTSS

- For :ref:`functional addressed <knowledge-base-functional-addressing>` messages, CAN Identifier value is defined
  as presented below:

  +----------------+----------+--------------+-----------+---------------+---------+---------+----------------------+
  |                | Priority | Reserved Bit | Data Page | Protocol data | Target  | Source  | Data                 |
  |                |          |              |           | unit format   | Address | Address |                      |
  +================+==========+==============+===========+===============+=========+=========+======+===============+
  | Bits number    |     3    |       1      |     1     |       8       |    8    |    8    |   8  |     16-504    |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | Content        |   0 - 7  |       0      |     0     |      205      |   N_TA  |   N_SA  | N_AE | N_PCI, N_Data |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | CAN field      |                              CAN Identifier                             |       CAN Data       |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | CAN ID bits    |   28-26  |      25      |     24    |     23-16     |   15-8  |   7-0   |  --- |      ---      |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+
  | CAN data bytes |    ---   |      ---     |    ---    |      ---      |   ---   |   ---   |   1  |      2-64     |
  +----------------+----------+--------------+-----------+---------------+---------+---------+------+---------------+

  .. code-block::

    # assuming priority parameter equals 0
    CAN_ID = 0xCDTTSS

    # assuming priority parameter equals 6 (default value)
    CAN_ID = 0x18CDTTSS

    # assuming priority parameter equals 7
    CAN_ID = 0x1CCDTTSS

where:

- CAN_ID - value of **CAN Identifier**
- TT - two (hexadecimal) digits of a 8-bit **Target Address** value
- SS - two (hexadecimal) digits of a 8-bit **Source Address** value
- N_TA - Network **Target Address** parameter
- N_SA - Network **Source Address** parameter
- N_AE - Network **Addressing Extension** parameter
- :ref:`N_PCI <knowledge-base-n-pci>` - Network Protocol Control Information
- :ref:`N_Data <knowledge-base-n-data>` - Network Data Field


.. _knowledge-base-can-data-field:

CAN Data Field
``````````````
:ref:`CAN frames <knowledge-base-can-frame>` that are exchanged during UDS communication must have
Data Length Code (DLC) equal to 8 (for CLASSICAL CAN and CAN FD) or greater (for CAN FD).
The only exception is usage of `CAN Frame Data Optimization`_.

+-----+------------------------------------------------------------------------+
| DLC |                               Description                              |
+=====+========================================================================+
|  <8 | *Valid only for CAN frames using data optimization*                    |
|     |                                                                        |
|     | Values in this range are only valid for Single Frame, Flow Control and |
|     |                                                                        |
|     | Consecutive Frame that use CAN frame data optimization.                |
+-----+------------------------------------------------------------------------+
|  8  | *Configured CAN frame maximum payload length of 8 bytes*               |
|     |                                                                        |
|     | For the use with CLASSICAL CAN and CAN FD type frames.                 |
+-----+------------------------------------------------------------------------+
| >8  | *Configured CAN frame maximum payload length greater than 8 bytes*     |
|     |                                                                        |
|     | For the use with CAN FD type frames only.                              |
+-----+------------------------------------------------------------------------+

where:

- DLC - Data Length Code of a :ref:`CAN frame <knowledge-base-can-frame>`

.. note:: Number of bytes that carry diagnostic message payload depends on a type and a format of a CAN packet as it is
  presented in :ref:`the table with CAN packets formats <knowledge-base-can-packets-format>`.


.. _knowledge-base-can-frame-data-padding:

CAN Frame Data Padding
''''''''''''''''''''''
If a number of bytes specified in a Packet is shorter than a number of bytes in CAN frame's data field,
then the sender has to pad any unused bytes in the frame. This can only be a case for
:ref:`Single Frame <knowledge-base-can-single-frame>`, :ref:`Flow Control <knowledge-base-can-flow-control>` and
the last :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>` of a segmented message.
If not specified differently, the default value 0xCC shall be used for the frame padding to minimize the bit stuffing
insertions and bit alteration on the wire.

.. note:: CAN frame data padding is mandatory for :ref:`CAN frames <knowledge-base-can-frame>` with DLC>8 and
  optional for frames with DLC=8.


.. _knowledge-base-can-data-optimization:

CAN Frame Data Optimization
'''''''''''''''''''''''''''
CAN frame data optimization is an alternative to `CAN Frame Data Padding`_.
If a number of bytes specified in a CAN Packet is shorter than a number of bytes in CAN frame's data field,
then the sender might decrease DLC value of the :ref:`CAN frame <knowledge-base-can-frame>` to the minimal number
that is required to sent a desired number of data bytes in a single CAN packet.

.. note:: CAN Frame Data Optimization might always be used for CAN Packets with less than 8 bytes of data to send.

.. warning:: CAN Frame Data Optimization might not always be able to replace `CAN Frame Data Padding`_ when CAN FD
  is used. This is a consequence of DLC values from 9 to 15 meaning as these values are mapped into CAN frame data
  bytes numbers in a non-linear way (e.g. DLC=9 represents 12 data bytes).

  Example:

  *When a CAN Packet with 47 bytes of data is planned for a transmission, then DLC=14 can be used instead of DLC=15,*
  *to choose 48-byte instead of 64-byte long CAN frame. Unfortunately, the last byte of CAN Frame data has to be *
  *padded as there is no way to send over CAN a frame with exactly 47 bytes of data.*


.. _knowledge-base-can-n-pci:

CAN Packet Types
````````````````
According to ISO 15765-2, CAN bus supports 4 types of Packets.

List of all values of `Network Protocol Control Information`_ supported by CAN bus:

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
| First Frame       | 0x1      |        FF_DL       |         |         |         |         |     |
|                   |          |                    |         |         |         |         |     |
| *FF_DL ≤ 4095*    |          |                    |         |         |         |         |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| First Frame       | 0x1      | 0x0      | 0x00    |                 FF_DL                 |     |
|                   |          |          |         |                                       |     |
| *FF_DL > 4095*    |          |          |         |                                       |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| Consecutive Frame | 0x2      | SN       |         |         |         |         |         |     |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+
| Flow Control      | 0x3      | FS       | BS      | ST_min  | N/A     | N/A     | N/A     | N/A |
+-------------------+----------+----------+---------+---------+---------+---------+---------+-----+

where:

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
Single Frame (SF) is used by CAN entities to transmit a diagnostic message with a payload short enough to fit it
into a single CAN packet. In other words, Single Frame carries payload of an entire diagnostic message.
Number of payload bytes carried by SF is specified by
:ref:`Single Frame Data Length <knowledge-base-can-single-frame-data-length>` value.


.. _knowledge-base-can-single-frame-data-length:

Single Frame Data Length
........................
Single Frame Data Length (SF_DL) is 4-bit (for CAN packets with DLC<=8) or 8-bit (for CAN packets with DLC>8) value
carried by every Single Frame as presented in
:ref:`the table with CAN packet formats<knowledge-base-can-packets-format>`.
SF_DL specifies number of diagnostic message payload bytes transmitted in a Single Frame.

.. note:: Maximal value of SF_DL depends on Single Frame :ref:`addressing format <knowledge-base-can-addressing>`
  and :ref:`DLC of a CAN message <knowledge-base-can-data-field>` that carries this packet.


.. _knowledge-base-can-first-frame:

First Frame
'''''''''''
First Frame (FF) is used by CAN entities to indicate start of a diagnostic message transmission.
First Frames are only used during a transmission of a segmented diagnostic messages that could not fit into a
:ref:`Single Frame <knowledge-base-can-single-frame>`.
Number of payload bytes carried by FF is specified by
:ref:`First Frame Data Length <knowledge-base-can-first-frame-data-length>` value.


.. _knowledge-base-can-first-frame-data-length:

First Frame Data Length
.......................
First Frame Data Length (FF_DL) is 12-bit (if FF_DL ≤ 4095) or 4-byte (if FF_DL > 4095) value carried by every
First Frame. FF_DL specifies number of diagnostic message payload bytes of a diagnostic message which transmission
was initiated by a First Frame.

.. note:: Maximal value of FF_DL is 4294967295 (0xFFFFFFFF). It means that CAN bus is capable of transmitting
  diagnostic messages that contains up to nearly 4,3 GB of payload bytes.


.. _knowledge-base-can-consecutive-frame:

Consecutive Frame
'''''''''''''''''
Consecutive Frame (CF) is used by CAN entities to continue transmission of a diagnostic message.
:ref:`First Frame <knowledge-base-can-first-frame>` shall always precede (one or more) Consecutive Frames.
Consecutive Frames carry payload bytes of a diagnostic message that was not transmitted in
a :ref:`First Frame <knowledge-base-can-first-frame>` that preceded them.
To avoid ambiguity and to make sure that no Consecutive Frame is lost, the order of Consecutive Frames is determined by
:ref:`Sequence Number <knowledge-base-can-sequence-number>` value.


.. _knowledge-base-can-sequence-number:

Sequence Number
...............
Sequence Number (SN) is 4-bit value used to specify the order of Consecutive Frames.

The rules of proper Sequence Number value assignment are following:

  - SN value of the first :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>` that directly follows
    a :ref:`First Frame <knowledge-base-can-first-frame>` shall be set to 1
  - SN shall be incremented by 1 for each following :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
  - SN value shall not be affected by :ref:`Flow Control <knowledge-base-can-flow-control>` frames
  - when SN reaches the value of 15, it shall wraparound and be set to 0 in the next
    :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`


.. _knowledge-base-can-flow-control:

Flow Control
''''''''''''
Flow Control (FC) is used by receiving CAN entities to instruct sending entities to stop, start, pause or resume
transmission of :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

Flow Control packet contains following parameters:

- :ref:`Flow Status <knowledge-base-can-flow-status>`
- :ref:`Block Size <knowledge-base-can-block-size>`
- :ref:`Separation Time Minimum <knowledge-base-can-st-min>`


.. _knowledge-base-can-flow-status:

Flow Status
...........
Flow Status (FS) is 4-bit value that is used to inform a sending network entity whether it can proceed with
a Consecutive Frames transmission.

Values of Flow Status:

- 0x0 - ContinueToSend (CTS)

  ContinueToSend value of Flow Status informs a sender of a diagnostic message that receiving entity (that responded
  with CTS) is ready to receive a maximum of :ref:`Block Size <knowledge-base-can-block-size>` number of
  :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

  Reception of a :ref:`Flow Control <knowledge-base-can-flow-control>` frame with ContinueToSend value shall cause
  the sender to resume ConsecutiveFrames sending.

- 0x1 - wait (WAIT)

  Wait value of Flow Status informs a sender of a diagnostic message that receiving entity (that responded with WAIT)
  is not ready to receive another :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

  Reception of a :ref:`Flow Control <knowledge-base-can-flow-control>` frame with WAIT value shall cause
  the sender to pause ConsecutiveFrames sending and wait for another
  :ref:`Flow Control <knowledge-base-can-flow-control>` frame.

  Values of :ref:`Block Size <knowledge-base-can-block-size>` and :ref:`STmin <knowledge-base-can-st-min>` in
  the :ref:`Flow Control <knowledge-base-can-flow-control>` frame (that contains WAIT value of Flow Status)
  are not relevant and shall be ignored.

- 0x2 - Overflow (OVFLW)

  Overflow value of Flow Status informs a sender of a diagnostic message that receiving entity (that responded
  with OVFLW) is not able to receive a full diagnostic message as it is too big and reception of the message would
  result in `Buffer Overflow <https://en.wikipedia.org/wiki/Buffer_overflow>`_ on receiving side.
  In other words, the value of :ref:`FF_DL <knowledge-base-can-first-frame-data-length>` exceeds the buffer size of
  the receiving entity.

  Reception of a :ref:`Flow Control <knowledge-base-can-flow-control>` frame with Overflow value shall cause
  the sender to abort the transmission of a diagnostic message.

  Overflow value shall only be sent in a :ref:`Flow Control <knowledge-base-can-flow-control>` frame that directly
  follows a :ref:`First Frame <knowledge-base-can-first-frame>`.

  Values of :ref:`Block Size <knowledge-base-can-block-size>` and :ref:`STmin <knowledge-base-can-st-min>` in
  the :ref:`Flow Control <knowledge-base-can-flow-control>` frame (that contains OVFLW value of Flow Status)
  are not relevant and shall be ignored.

- 0x3-0xF - Reserved

  This range of values is reserved for future extension by ISO 15765.


.. _knowledge-base-can-block-size:

Block Size
..........
Block Size (BS) is a one byte value specified by receiving entity that informs about number of
:ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` to be sent in a one block of packets.

Block Size values:

- 0x00

  The value 0 of the Block Size parameter informs a sender that no more
  :ref:`Flow Control <knowledge-base-can-flow-control>` frames shall be sent during the transmission
  of the segmented message.

  Reception of Block Size = 0 shall cause the sender to send all remaining
  :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` without any stop for further
  :ref:`Flow Control <knowledge-base-can-flow-control>` frames from the receiving entity.

- 0x01-0xFF

  This range of Block Size values informs a sender the maximum number of
  :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>` that can be transmitted without an intermediate
  :ref:`Flow Control <knowledge-base-can-flow-control>` frames from the receiving entity.


.. _knowledge-base-can-st-min:

Separation Time Minimum
.......................
Separation Time minimum (STmin) is a one byte value specified by receiving entity that informs about minimum time gap
between the transmission of two following :ref:`Consecutive Frames <knowledge-base-can-consecutive-frame>`.

STmin values:

- 0x00-0x7F - Separation Time minimum range 0-127 ms

  The value of STmin in this range represents the value in milliseconds (ms).

  0x00 = 0 ms

  0xFF = 127 ms

- 0x80-0xF0 - Reserved

  This range of values is reserved for future extension by ISO 15765.

- 0xF1-0xF9 - Separation Time minimum range 100-900 μs

  The value of STmin in this range represents the value in microseconds (μs) according to the formula:

  .. code-block::

    (STmin - 0xF0) * 100 μs

  Meaning of example values:

  0xF1 -> 100 μs

  0xF5 -> 500 μs

  0xF9 -> 900 μs

- 0xFA-0xFF - Reserved

  This range of values is reserved for future extension by ISO 15765.

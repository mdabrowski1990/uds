.. _knowledge-base-packet:

Packet (N_PDU)
==============
In ISO Standards, the name Network :ref:`Protocol Data Unit <knowledge-base-pdu>` (N_PDU in short) is used.
For various reasons we decided to use **Packet** name instead.

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
Network Address Information (N_AI) field carries all :ref:`addressing <knowledge-base-addressing>` related information.

It identifiers:

- the sender
- recipient(s) of the packet
- :ref:`addressing <knowledge-base-addressing>` type (:ref:`Physical Addressing <knowledge-base-physical-addressing>`
  or :ref:`Functional Addressing <knowledge-base-functional-addressing>`) used


.. _knowledge-base-n-data:

Network Data Field
------------------
Network Data Field (N_Data) carries diagnostic message data. It might be an entire diagnostic message data
(if a :ref:`diagnostic message <knowledge-base-diagnostic-message>` fits into one packet) or just a part of it
(if :ref:`segmentation <knowledge-base-segmentation>` had to be used to divide
a :ref:`diagnostic message <knowledge-base-diagnostic-message>` into smaller parts).

For some communication buses, some packets might not carry any data (e.g.
:ref:`CAN Flow Control <knowledge-base-can-flow-control>`) as they are used to manage the packets flow.


.. _knowledge-base-n-pci:

Network Protocol Control Information
------------------------------------
Network Protocol Control Information (N_PCI) identifies the type of `Packet (N_PDU)`_.
N_PCI values and their interpretation are bus specific.

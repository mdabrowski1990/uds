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

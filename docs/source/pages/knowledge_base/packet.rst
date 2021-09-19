UDS Packet
==========
UDS packet is also called Network Protocol Data Unit (N_PDU). It is created during segmentation of a
diagnostic message. Each diagnostic message consists of at least one N_PDU. There are some packets (N_PDUs) which
does not carry any diagnostic message data as they are used to manage the flow of other packets (N_PDUs).

UDS packet (N_PDU) consists of following fields:
 - `Network Address Information`_ (N_AI) - packet addressing
 - `Network Protocol Control Information`_ (N_PCI) - packet type
 - `Network Data Field`_ (N_Data) - packet date


Network Address Information
'''''''''''''''''''''''''''
Network Address Information (N_AI) contains address information which identifies the recipient(s) and the sender
between whom data exchange takes place. It also describes communication model (e.g. whether response is required)
for the message.


Network Protocol Control Information
''''''''''''''''''''''''''''''''''''
Network Protocol Control Information (N_PCI) identifies the type of `UDS packet`_ (Network Protocol Data Unit).
Supported N_PCIs and theirs values interpretation are bus specific.


Network Data Field
''''''''''''''''''
Network Data Field (N_Data) carries diagnostic message data. It might be an entire diagnostic message data (if
diagnostic message fits into one packet) or just a part (a single packet) of it (if segmentation had to be
used to divide diagnostic message into smaller parts).

.. _knowledge-base-packet:

Packet (N_PDU)
==============
In ISO Standards, the term `Network Protocol Data Unit <knowledge-base-pdu>`_ (N_PDU) is used.
In this implementation, we refer to it as a **Packet**.

Packets are created during the :ref:`segmentation <knowledge-base-segmentation>` of a
:ref:`diagnostic message <knowledge-base-diagnostic-message>`.
Each diagnostic message consists of at least one **Packet** (N_PDU).

A **Packet** contains the following fields:

- `Network Address Information`_ (N_AI) — packet addressing
- `Network Data Field`_ (N_Data) — packet payload
- `Network Protocol Control Information`_ (N_PCI) — packet type


.. _knowledge-base-n-ai:

Network Address Information
---------------------------
The **Network Address Information (N_AI)** field carries all :ref:`addressing <knowledge-base-addressing>` information.

It identifies:

- The sender of the **Packet**
- The recipient(s) of the **Packet**
- The :ref:`addressing <knowledge-base-addressing>` type used


.. _knowledge-base-n-data:

Network Data Field
------------------
The **Network Data Field (N_Data)** carries the diagnostic message content.

- If the diagnostic message fits into a single **Packet**, N_Data contains the entire message.
- If segmentation is used, N_Data carries only a portion of the message.

On some communication buses, certain **Packets** may not carry any data (e.g.,
:ref:`CAN Flow Control <knowledge-base-can-flow-control>`), as they are used solely to manage the flow of packets.


.. _knowledge-base-n-pci:

Network Protocol Control Information
------------------------------------
The **Network Protocol Control Information (N_PCI)** field identifies the type of the **Packet (N_PDU)**.
N_PCI values and their interpretation are specific to each communication bus.


Segmentation
============
If`diagnostic message data to be transmitted does not fit into a single bus frame, then segmentation process
is required to divide diagnostic message into smaller pieces called UDS Packets. Each UDS Packet (or N_PDU)
fits into one frame. To visualize the concept, look on the figure below:

.. figure:: ../../diagrams/KnowledgeBase-PDUs.png
    :alt: UDS PDUs
    :figclass: align-center
    :width: 100%

    UDS Protocol Data Units on different layers of OSI Model.


To summarize, we distinguish (in UDS package implementation) following entities that take part in UDS communication on different layers of `UDS OSI Model`_:
 - Diagnostic message - also called 'Application Protocol Data Unit' (A_PDU)
 - ` packet - also called 'Network Protocol Data Unit' (N_PDU). UDS packets types and transmission rules are bus
   specific and always fit into one frame.
 - `Frame <https://en.wikipedia.org/wiki/Frame_(networking)>`_ - the smallest piece of information exchanged by nodes
   in a bus network. Only specific frames take part in UDS communication.

Segmentation process is specific for a bus on which UDS Packets would transmitted.
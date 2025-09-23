.. _knowledge-base-segmentation:

Segmentation
============


.. _knowledge-base-message-segmentation:

Message Segmentation
--------------------
To transmit a diagnostic message, its information (payload and addressing) must be encoded into one or more segments.
In this documentation, these segments are referred to as :ref:`Packets <knowledge-base-packet>`.

.. note:: The segmentation process is network-specific due to differences in topologies and communication models
   (e.g., Master/Slave) enforced by each network.


.. _knowledge-base-packets-desegmentation:

Packets Desegmentation
----------------------
Desegmentation is the reverse of :ref:`message segmentation <knowledge-base-message-segmentation>`.
It reconstructs a :ref:`diagnostic message <knowledge-base-diagnostic-message>` from one or more
:ref:`Packets <knowledge-base-packet>`.

.. note:: While a diagnostic message can be segmented in multiple ways, there is always only one correct method
   to perform desegmentation and decode the message from packets.

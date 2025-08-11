.. _knowledge-base-segmentation:

Segmentation
============


.. _knowledge-base-message-segmentation:

Message Segmentation
--------------------
To transmit a diagnostic message, its information (payload and addressing) must be unambiguously encoded into one
or more segments (those segments are called :ref:`Packets <knowledge-base-packet>` by this documentation)
that are specific for the bus used.

.. note:: Segmentation process is specific for each bus due to various topologies and
    communication models (e.g. Master/Slave) enforced by them.


.. _knowledge-base-packets-desegmentation:

Packets Desegmentation
----------------------
By desegmentation, we mean an unambiguous operation which is the reverse process to a `message segmentation`_.
It transforms one or more :ref:`packets <knowledge-base-packet>` into
a :ref:`diagnostic message <knowledge-base-diagnostic-message>`.

.. note:: There are many ways to segment a diagnostic message into packets, but there is always only one correct way
    to perform desegmentation and decode a diagnostic message out of packets.

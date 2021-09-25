.. _knowledge-base-segmentation:

Segmentation
============


.. _knowledge-base-message-segmentation:

Message Segmentation
--------------------
If diagnostic message data to be transmitted does not fit into a single frame, then segmentation process is required
to divide :ref:`diagnostic message <knowledge-base-diagnostic-message>` into smaller pieces called
:ref:`UDS packets <knowledge-base-uds-packet>`.


.. _knowledge-base-packets-desegmentation:

Packets Desegmentation
----------------------
Desegmentation is a reverse process to a `message segmentation`_. It transforms one or more
:ref:`UDS packets <knowledge-base-uds-packet>` into a :ref:`diagnostic message <knowledge-base-diagnostic-message>`.

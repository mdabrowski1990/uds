Performance and Error Handling
==============================
In this chapter of the documentation, we would explain performance and timing requirements for UDS communication
and how they are supposed to be handled by UDS entities.


CAN specific
------------

Performance
```````````
:ref:`ISO standards <knowledge-base-uds-standards>` defines following time values on the network layer of UDS
on CAN communication:

- N_As_
- N_Ar_
- N_Bs_
- N_Br_
- N_Cs_
- N_Cr_

.. figure:: ../../images/CAN_Timings.png
    :alt: Diagnostic on CAN timings
    :figclass: align-center
    :width: 100%

    Network layer time values (N_As, N_Ar, N_Bs, N_Br, N_Cs, N_Cr) present during UDS on CAN communication.

.. note::
  The example uses :ref:`segmented diagnostic message transmission <knowledge-base-segmented-message-transmission>`
  as all CAN timings values can be presented there (all these times are applicable in this case).
  For :ref:`unsegmented diagnostic message transmission <knowledge-base-unsegmented-message-transmission>` though,
  the only applicable time parameter is N_As_.


.. _knowledge-base-can-n-as:

N_As
''''
N_As is a time parameter related to transmission of any :ref:`CAN Packet <knowledge-base-uds-can-packet>` by a sender.
It is measured from the beginning of the :ref:`CAN Frame <knowledge-base-can-frame>` (that carries such CAN Packet)
transmission till the reception of a confirmation that this CAN Frame was received by a receiver.

Timeout value:
  1000 ms

Error handling:
  If N_As timeout is exceeded, then the transmission of
  the :ref:`diagnostic message <knowledge-base-diagnostic-message>` shall be aborted.

Affected :ref:`CAN Packets <knowledge-base-uds-can-packet>`:
  - :ref:`Single Frame <knowledge-base-can-single-frame>`
  - :ref:`First Frame <knowledge-base-can-first-frame>`
  - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`


.. _knowledge-base-can-n-ar:

N_Ar
''''
N_Ar is a time parameter related to transmission of any :ref:`CAN Packet <knowledge-base-uds-can-packet>` by a receiver.
It is measured from the beginning of the :ref:`CAN Frame <knowledge-base-can-frame>` (that carries such CAN Packet)
transmission till the reception of a confirmation that this CAN Frame was received by a sender.

Timeout value:
  1000 ms

Error handling:
  If N_Ar timeout is exceeded, then the reception of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.

Affected :ref:`CAN Packets <knowledge-base-uds-can-packet>`:
  - :ref:`Flow Control <knowledge-base-can-flow-control>`


.. _knowledge-base-can-n-bs:

N_Bs
''''
N_Bs is a time parameter related to :ref:`Flow Control (CAN Packet) <knowledge-base-can-flow-control>` reception
by a sender. It is measured from the end of the last CAN Packet transmission (either transmitted
:ref:`First Frame <knowledge-base-can-first-frame>`, :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
or received :ref:`Flow Control <knowledge-base-can-flow-control>`), till the reception of
:ref:`Flow Control <knowledge-base-can-flow-control>`.

Timeout value:
  1000 ms

Error handling:
  If N_Bs timeout is exceeded, then the reception of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.

Affected :ref:`CAN Packets <knowledge-base-uds-can-packet>`:
  - :ref:`Flow Control <knowledge-base-can-flow-control>`


.. _knowledge-base-can-n-br:

N_Br
''''
N_Br is a time parameter related to :ref:`Flow Control (CAN Packet) <knowledge-base-can-flow-control>` transmission
by a receiver. It is measured from the end of the last CAN Packet transmission (either received
:ref:`First Frame <knowledge-base-can-first-frame>`, :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`
or transmitted :ref:`Flow Control <knowledge-base-can-flow-control>`), till the start of
:ref:`Flow Control <knowledge-base-can-flow-control>` transmission.

Performance requirement:
  A receiving entity is obliged to transmit :ref:`Flow Control <knowledge-base-can-flow-control>` packet before value
  of N_Br achieves maximal value threshold.

  .. code-block::

    [N_Br] + [N_Ar] < 0.9 * [N_Bs timeout]
    [N_Br max] = 900ms - [N_Ar]

Affected :ref:`CAN Packets <knowledge-base-uds-can-packet>`:
  - :ref:`Flow Control <knowledge-base-can-flow-control>`


.. _knowledge-base-can-n-cs:

N_Cs
''''
N_Cs is a time parameter related to :ref:`Consecutive Frame (CAN Packet) <knowledge-base-can-consecutive-frame>`
transmission by a sender. It is measured from the end of the last CAN Packet transmission (either received
:ref:`Flow Control <knowledge-base-can-flow-control>` or transmitted
:ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`), till the start of
:ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>` transmission.

Performance requirement:
  A sending entity is obliged to transmit :ref:`Consecutive Frame <knowledge-base-can-flow-control>` packet before value
  of N_Cs achieves maximal value threshold.

  .. code-block::

    [N_Cs] + [N_As] < 0.9 * [N_Cr timeout]
    [N_Cs max] = 900ms - [N_As]

Affected :ref:`CAN Packets <knowledge-base-uds-can-packet>`:
  - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`


.. _knowledge-base-can-n-cr:

N_Cr
''''
N_Cr is a time parameter related to :ref:`Consecutive Frame (CAN Packet) <knowledge-base-can-consecutive-frame>`
reception by a receiver. It is measured from the end of the last CAN Packet transmission (either transmitted
:ref:`Flow Control <knowledge-base-can-flow-control>` or received
:ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`), till the reception of
:ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`.

Timeout value:
  1000 ms

Error handling:
  If N_Cr timeout is exceeded, then the reception of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.

Affected :ref:`CAN Packets <knowledge-base-uds-can-packet>`:
  - :ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>`


.. _knowledge-base-can-unexpected-packet-arrival:

Unexpected Packet handling
``````````````````````````
According to ISO 15765-2:2016:
    As a general rule, arrival of an unexpected N_PDU from any node shall be ignored, with the exception of SF N_PDUs
    and physically addressed FF N_PDUs; functionally addressed FirstFrames shall be ignored.
    When the specified action is to ignore an unexpected N_PDU, this means that the network layer shall not notify
    the upper layers of its arrival.

    Depending on the network layer design decision to support full- or half-duplex communication, the interpretation
    of “unexpected” differs:
    a) with half-duplex, point-to-point communication between two nodes is only possible in one direction at a time;
    b) with full-duplex, point-to-point communication between two nodes is possible in both directions at once.


Half-duplex
'''''''''''
Half-duplex means that only one UDS message (in one direction) can be transmitted at a time.
That means that each node has up to one role (either sender or receiver) at any time.

Handling of unexpected CAN packets in case of half-duplex communication:

+--------------+--------------------------+-------------------------+-----------------------+--------------+---------+
|    Status    |       Single Frame       |       First Frame       |   Consecutive Frame   | Flow Control | Unknown |
+==============+==========================+=========================+=======================+==============+=========+
| Idle         | Process the Single Frame | Process the First Frame | Ignore                | Ignore       | Ignore  |
|              |                          |                         |                       |              |         |
|              | as the start of          | as the start of         |                       |              |         |
|              |                          |                         |                       |              |         |
|              | a new message.           | a new message.          |                       |              |         |
+--------------+--------------------------+-------------------------+-----------------------+--------------+---------+
| Segmented    | Ignore                   | Ignore                  | Ignore                | Ignore       | Ignore  |
|              |                          |                         |                       |              |         |
| message      |                          |                         |                       |              |         |
|              |                          |                         |                       |              |         |
| transmission |                          |                         |                       |              |         |
|              |                          |                         |                       |              |         |
| in progress  |                          |                         |                       |              |         |
+--------------+--------------------------+-------------------------+-----------------------+--------------+---------+
| Segmented    | Terminate the current    | Terminate the current   | If awaited,           | Ignore       | Ignore  |
|              |                          |                         |                       |              |         |
| message      | message reception        | message reception and   | then process          |              |         |
|              |                          |                         |                       |              |         |
| reception    | and process              | process the First Frame | the Consecutive Frame |              |         |
|              |                          |                         |                       |              |         |
| in progress  | the Single Frame         | as the start of         | in the on-going       |              |         |
|              |                          |                         |                       |              |         |
|              | as the start of          | a new message.          | reception and perform |              |         |
|              |                          |                         |                       |              |         |
|              | a new message.           |                         | required checks       |              |         |
|              |                          |                         |                       |              |         |
|              |                          |                         | (e.g. Sequence Number |              |         |
|              |                          |                         |                       |              |         |
|              |                          |                         | in order).            |              |         |
|              |                          |                         |                       |              |         |
|              |                          |                         | Otherwise, ignore it. |              |         |
+--------------+--------------------------+-------------------------+-----------------------+--------------+---------+


Full-duplex
'''''''''''
Full-duplex means that UDS message can be transmitted in both directions at once.
That means that a node could be sender of one UDS message and receiver of another one at the same time.

Handling of unexpected CAN packets in case of full-duplex communication:

+--------------+--------------------------+-------------------------+-------------------------+--------------+---------+
|    Status    |       Single Frame       |       First Frame       |    Consecutive Frame    | Flow Control | Unknown |
+==============+==========================+=========================+=========================+==============+=========+
| Idle         | Process the Single Frame | Process the First Frame | Ignore                  | Ignore       | Ignore  |
|              |                          |                         |                         |              |         |
|              | as the start of          | as the start of         |                         |              |         |
|              |                          |                         |                         |              |         |
|              | a new message.           | a new message.          |                         |              |         |
+--------------+--------------------------+-------------------------+-------------------------+--------------+---------+
| Segmented    | If a message reception   | If a message reception  | If a message reception  | Ignore       | Ignore  |
|              |                          |                         |                         |              |         |
| message      | is in progress then see  | is in progress then see | is in progress then see |              |         |
|              |                          |                         |                         |              |         |
| transmission | the corresponding cell   | the corresponding cell  | the corresponding cell  |              |         |
|              |                          |                         |                         |              |         |
| in progress  | in the row below.        | in the row below.       | in the row below.       |              |         |
|              |                          |                         |                         |              |         |
|              | Otherwise, process       | Otherwise, process      | Otherwise, ignore it.   |              |         |
|              |                          |                         |                         |              |         |
|              | the Single Frame as      | the First Frame as      |                         |              |         |
|              |                          |                         |                         |              |         |
|              | the start of             | the start of            |                         |              |         |
|              |                          |                         |                         |              |         |
|              | a new message.           | a new message.          |                         |              |         |
+--------------+--------------------------+-------------------------+-------------------------+--------------+---------+
| Segmented    | Terminate the current    | Terminate the current   | If awaited, then        | Ignore       | Ignore  |
|              |                          |                         |                         |              |         |
| message      | message reception and    | message reception and   | process the Consecutive |              |         |
|              |                          |                         |                         |              |         |
| reception    | process the Single       | process the First Frame | Frame in the on-going   |              |         |
|              |                          |                         |                         |              |         |
| in progress  | Frame as the start       | as the start of         | reception and perform   |              |         |
|              |                          |                         |                         |              |         |
|              | of a new message.        | a new message.          | required checks (e.g.   |              |         |
|              |                          |                         |                         |              |         |
|              |                          |                         | Sequence Number in      |              |         |
|              |                          |                         |                         |              |         |
|              |                          |                         | order).                 |              |         |
|              |                          |                         |                         |              |         |
|              |                          |                         | Otherwise, ignore it.   |              |         |
+--------------+--------------------------+-------------------------+-------------------------+--------------+---------+

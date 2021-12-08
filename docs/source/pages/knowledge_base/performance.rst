Performance and Error Handling
==============================
In this chapter of the documentation, we would explain performance and timing requirements for UDS communication
and how they are supposed to be handled by UDS entities.


CAN specific
------------

.. figure:: ../../images/CAN_Timings.png
    :alt: Diagnostic on CAN timings
    :figclass: align-center
    :width: 100%

    Diagnostic on CAN timings (N_As, N_Ar, N_Bs, N_Br, N_Cs, N_Cr).


N_As
````
N_As is a time parameter related to :ref:`CAN Packet <knowledge-base-uds-can-packet>` transmission on a sender side.
It is measured from the beginning of the :ref:`CAN Frame <knowledge-base-can-frame>` (that carries CAN Packet)
transmission till the reception of a confirmation that the CAN Frame was received by a receiving side.

Timeout value:
  1000 ms

Error handling:
  If N_As timeout is exceeded, then the transmission of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.


N_Ar
````
N_Ar is a time parameter related to :ref:`CAN Packet <knowledge-base-uds-can-packet>` reception on a receiver side.
It is measured from the beginning of the :ref:`CAN Frame <knowledge-base-can-frame>` (that carries CAN Packet)
transmission till the reception of a confirmation that the CAN Frame was received by a sending side.

Timeout value:
  1000 ms

Error handling:
  If N_Ar timeout is exceeded, then the reception of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.


N_Bs
````
N_Bs is a time parameter related to :ref:`Flow Control (CAN Packet) <knowledge-base-can-flow-control>` reception
on a sender side.
It is measured from the end of the last CAN Packet transmission (either transmitted :ref:`First Frame <knowledge-base-can-first-frame>`,
:ref:`Consecutive Frame <knowledge-base-can-consecutive-frame>` or received :ref:`Flow Control <knowledge-base-can-flow-control>`),
till the reception of :ref:`Flow Control <knowledge-base-can-flow-control>`.

Timeout value:
  1000 ms

Error handling:
  If N_Bs timeout is exceeded, then the reception of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.


N_Br
````

N_Cs
````

N_Cr
````

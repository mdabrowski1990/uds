.. _knowledge-base-dolin:

Diagnostics over LIN
====================
Diagnostics over LIN (DoLIN), also known as LIN Transport Protocol (LIN-TP, ISO 17987-2),
is the transport layer communication protocol used by UDS for
:ref:`message segmentation <knowledge-base-segmentation>` on LIN networks.
In other words, DoLIN provides the adaptation that allows UDS to operate on LIN.
It is illustrated in the :ref:`UDS OSI Model <knowledge-base-osi-model>`.

LIN is a low-cost serial communication protocol primarily designed for communication
between electronic control units (ECUs) and peripheral devices in automotive networks.
It is commonly used for applications that do not require the bandwidth or complexity of CAN.

LIN uses a master-slave communication model, where the master node controls bus access and initiates
all frame transmissions according to a predefined schedule.


.. _knowledge-base-lin-versions:

LIN Versions
------------
`LIN Bus <https://en.wikipedia.org/wiki/Local_Interconnect_Network>`_ was released in multiple version over the years.


LIN 1.3
```````
- Supports classic checksum only
- Supports basic frame communication with up to 8 data bytes

:download:`LIN 1.3 Specification <../../specs/LIN/LIN_1_3.pdf>`


LIN 2.0
```````
- Introduces enhanced checksum
- Introduces diagnostic communication and transport protocol
- Introduces slave node configuration services
- Introduces byte array signals
- Introduces sporadic and event-triggered frames
- Introduces automatic baud-rate detection

:download:`LIN 2.0 Specification <../../specs/LIN/LIN_2_0.pdf>`


LIN 2.1
```````
- Extends slave node configuration services
- Introduces three diagnostic classes (I, II and III)
- Introduces functional diagnostic addressing
- Improves event-triggered frame collision resolution

:download:`LIN 2.1 Specification <../../specs/LIN/LIN_2_1.pdf>`


LIN 2.2A
````````
- Updates physical-layer bit-sampling requirements
- Corrects wake-up signal definition

:download:`LIN 2.2A Specification <../../specs/LIN/LIN_2_2_A.pdf>`


.. _knowledge-base-lin-frame:

LIN Frame
---------
A LIN frame consists of a header and a response.


LIN Header
``````````
The header is always transmitted by Master node.

The header contains the following fields:

- **Break** - signals the beginning of a new frame
- **Sync** - fixed synchronization byte (0x55), used by slave nodes to synchronize their baud rate with the master
- **Protected Identifier (PID)** - contains a 6-bit frame identifier and 2 parity bits


LIN Response
````````````
The response part is transmitted by either Master or Slave node.

The response contains:

- **Data** - payload containing up to 8 bytes
- **Checksum** - used to detect transmission errors

There are two checksum variants:

- **Classic checksum** - calculated over the data bytes only
- **Enhanced checksum** - calculated over the protected identifier and data bytes

Diagnostic frames always use the classic checksum for backwards compatibility reasons.


.. _knowledge-base-lin-packet:

LIN Packet
----------
LIN Packets (N_PDUs) are :ref:`LIN Frames <knowledge-base-lin-frame>` exchanged during DoLIN communication.


.. _knowledge-base-lin-nad:

NAD
```
Network NAD is 1 byte parameter located in the first byte in each LIN diagnostic frame.

Based on NAD value, the communication model is distinguished:

- 0x00: Not Applicable, reserved for sleep command frame

- 0x01-0x7D: :ref:`physical address <knowledge-base-lin-physical-address>`

- 0x7E: :ref:`functional address <knowledge-base-lin-functional-address>`

- 0x7F: :ref:`broadcast address <knowledge-base-lin-broadcast-address>`

- 0x80-0xFF: for vehicle manufacturer definition


.. _knowledge-base-lin-n-pci:

LIN Packet Types
````````````````


.. _knowledge-base-lin-single-frame:

Single Frame
''''''''''''


.. _knowledge-base-lin-single-frame-data-length:

Single Frame Data Length
........................



.. _knowledge-base-lin-first-frame:

First Frame
'''''''''''


.. _knowledge-base-lin-first-frame-data-length:

First Frame Data Length
.......................



.. _knowledge-base-lin-consecutive-frame:

Consecutive Frame
'''''''''''''''''


.. _knowledge-base-lin-sequence-number:

Sequence Number
...............


Addressing Types
````````````````


Physical
''''''''


Functional
''''''''''


Broadcast
'''''''''



.. _knowledge-base-lin-performance-and-error-handling:

Performance and Error Handling
------------------------------
ISO 17987-2 defines the following network layer parameters for Diagnostics over LIN (DoLIN):

- N_As_
- N_Cs_
- N_Cr_

.. figure:: ../../images/LIN_Timings.png
  :alt: Diagnostic on LIN timings
  :figclass: align-center
  :width: 100%

  Network layer time values (N_As, N_Cs, N_Cr) present during UDS on LIN communication.

.. note:: The example uses
  :ref:`segmented diagnostic message transmission <knowledge-base-lin-segmented-message-transmission>`
  as it enables to present all LIN timing parameters.
  For :ref:`unsegmented diagnostic message transmission <knowledge-base-lin-unsegmented-message-transmission>` though,
  the only applicable time parameter is N_As_.


.. _knowledge-base-lin-n-as:

N_As
````
N_As is the time parameter of a :ref:`LIN Packet <knowledge-base-lin-packet>` transmission.
It is measured on Master side from the moment its transport layer requests for a diagnostic frame to be transmitted
till the frame has been fully transmitted on the bus.

Timeout value:
  1000ms

Error handling:
  If N_As timeout is exceeded, the transmission of
  the :ref:`diagnostic message <knowledge-base-diagnostic-message>` shall be aborted.

Affected :ref:`LIN Packets <knowledge-base-lin-packet>`:

- :ref:`Single Frame <knowledge-base-lin-single-frame>`
- :ref:`First Frame <knowledge-base-lin-first-frame>`
- :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>`


.. _knowledge-base-lin-n-cs:

N_Cs
````
N_Cs is the time parameter related to :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>` packet
transmission by a sender.
It is measured from the end of the last transmitted LIN Packet (either
:ref:`First Frame <knowledge-base-lin-first-frame>` or :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>`)
until the next :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>` is requested.

Performance requirement:
  A sending entity shall transmit the :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>` packet
  before N_Cs reaches its maximal allowed value.

  .. code-block::

    [N_Cs] + [N_As] < 0.9 * [N_Cr timeout]
    [N_Cs max] = 900ms - [N_As]

Affected :ref:`LIN Packets <knowledge-base-lin-packet>`:

- :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>`


.. _knowledge-base-lin-n-cr:

N_Cr
````
N_Cr is the time parameter related to :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>` packet
reception by a receiver.
It is measured from the end of the last received LIN Packet (either
:ref:`First Frame <knowledge-base-lin-first-frame>` or :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>`)
until the reception of :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>`.

Timeout value:
  1000ms

Error handling:
  If the N_Cr timeout is exceeded, the reception of the :ref:`diagnostic message <knowledge-base-diagnostic-message>`
  shall be aborted.

Affected :ref:`LIN Packets <knowledge-base-lin-packet>`:

- :ref:`Consecutive Frame <knowledge-base-lin-consecutive-frame>`

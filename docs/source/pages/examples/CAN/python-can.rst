.. _examples-python-can:

Python-CAN
==========
Examples with `python-can`_ package being used for controlling CAN bus (handling CAN frames transmission and reception).

.. seealso:: https://github.com/mdabrowski1990/uds/tree/main/examples/can/python-can


Kvaser interface
----------------
Examples with `Kvaser CAN interfaces`_ used as a hardware device to send and receive CAN messages.

.. seealso:: https://github.com/mdabrowski1990/uds/tree/main/examples/can/python-can/kvaser


Synchronous implementation
``````````````````````````

Message handling
''''''''''''''''

- Send UDS message:

.. include:: ../../../../../examples/can/python-can/kvaser/send_message.py
  :code: python

- Receive UDS message:

.. include:: ../../../../../examples/can/python-can/kvaser/receive_message.py
  :code: python

- Send UDS message on one interface, receive on the other:

.. include:: ../../../../../examples/can/python-can/kvaser/send_and_receive_message.py
  :code: python


Packet handling
'''''''''''''''

- Send CAN packets:

.. include:: ../../../../../examples/can/python-can/kvaser/send_packet.py
  :code: python

- Receive CAN packets:

.. include:: ../../../../../examples/can/python-can/kvaser/receive_packet.py
  :code: python

- Send CAN packets on one interface, receive on the other:

.. include:: ../../../../../examples/can/python-can/kvaser/send_and_receive_packet.py
  :code: python


Asynchronous implementation
```````````````````````````

Message handling
''''''''''''''''

- Send UDS message:

.. include:: ../../../../../examples/can/python-can/kvaser/send_message_asyncio.py
  :code: python

- Receive UDS message:

.. include:: ../../../../../examples/can/python-can/kvaser/receive_message_asyncio.py
  :code: python

- Send UDS message on one interface, receive on the other:

.. include:: ../../../../../examples/can/python-can/kvaser/send_and_receive_message_asyncio.py
  :code: python


Packet handling
'''''''''''''''

- Send CAN packets:

.. include:: ../../../../../examples/can/python-can/kvaser/send_packet_asyncio.py
  :code: python

- Receive CAN packets:

.. include:: ../../../../../examples/can/python-can/kvaser/receive_packet_asyncio.py
  :code: python

- Send CAN packets on one interface, receive on the other:

.. include:: ../../../../../examples/can/python-can/kvaser/send_and_receive_packet_asyncio.py
  :code: python


.. _python-can: https://github.com/hardbyte/python-can

.. _Kvaser CAN interfaces: https://www.kvaser.com/products-services/our-products/#/?descriptors=pc_int

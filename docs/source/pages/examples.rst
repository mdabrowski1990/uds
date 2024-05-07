Examples
========
Location of all example files: https://github.com/mdabrowski1990/uds/tree/main/examples


CAN
---
Code examples of UDS protocol communication over CAN bus.

.. seealso:: https://github.com/mdabrowski1990/uds/tree/main/examples/can


.. _example-python-can:

Python-CAN
``````````
Examples with `python-can`_ package being used for controlling CAN bus (handling CAN frames transmission and reception).

.. seealso:: https://github.com/mdabrowski1990/uds/tree/main/examples/can/python-can


Kvaser interface
''''''''''''''''
- Send CAN packets (synchronous implementation):

.. include:: ../../../examples/can/python-can/kvaser/send_packets.py
    :code: python

- Send CAN packets (asynchronous implementation):

.. include:: ../../../examples/can/python-can/kvaser/send_packets_asyncio.py
    :code: python

- Receive CAN packets (synchronous implementation):

.. include:: ../../../examples/can/python-can/kvaser/receive_packets.py
    :code: python

- Receive CAN packets (asynchronous implementation):

.. include:: ../../../examples/can/python-can/kvaser/receive_packets_asyncio.py
    :code: python


.. seealso:: https://github.com/mdabrowski1990/uds/tree/main/examples/can/python-can/kvaser


.. _python-can: https://github.com/hardbyte/python-can

.. _Kvaser CAN interfaces: https://www.kvaser.com/products-services/our-products/#/?descriptors=pc_int

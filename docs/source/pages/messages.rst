Diagnostic Messages
===================

.. role:: python(code)
    :language: python

In this chapter, you will find information about objects that carry diagnostic data on a different layer of OSI model.

In implementation we distinguish:
 - `UDS Message`_ - carries application UDS data on upper layers (layers 5-7 of OSI model)
 - `Network Protocol Data Unit`_ - it is a single packet that was created after segmentation of UDS Message
   (layers 3-4 of OSI model)
 - `Bus Frame`_ - a single frame transmitted over any bus that carries any data (not necessarily related to
   UDS communication)


UDS Message
-----------
TODO during `UDS Message documentation task <https://github.com/mdabrowski1990/uds/issues/52>`_


Network Protocol Data Unit
--------------------------


N_PDU impl
````````````


AbstractNPDU
''''''''''''




Bus Frame
---------



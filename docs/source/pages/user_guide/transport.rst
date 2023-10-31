Transport Interfaces
====================
Transport interfaces are meant to handle Physical (layer 1), Data (layer 2), Network (layer 3) and Transport (layer 4)
layers of UDS OSI model which are unique for every communication bus. First two layers (Physical and Data Link) are
usually handled by some external packages. Abstract API that is common for all Transport Interfaces (and therefore buses)
is defined in :class:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface` class.

.. toctree::
    :maxdepth: 1
    :caption: Implementation of Transport Interface:

    transport/can.rst
    transport/flexray.rst
    transport/ethernet.rst
    transport/kline.rst
    transport/lin.rst
    transport/custom.rst

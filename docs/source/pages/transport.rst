Transport Interfaces
====================
Transport interfaces are meant to handle Physical (layer 1), Data (layer 2), Network (layer 3) and Transport (layer 4)
layers of UDS OSI model which are unique for every communication bus. First two layers (Physical and Data Link) are
usually handled by external packages (e.g. `python-can <https://python-can.readthedocs.io/en/master/#>`_ handles
first two layers for CAN bus).


.. toctree::
   :maxdepth: 1
   :caption: Transport Interface Implementations:

   transport/can.rst
   transport/ethernet.rst
   transport/lin.rst
   transport/flexray.rst
   transport/kline.rst
   transport/custom.rst


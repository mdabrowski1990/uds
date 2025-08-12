Transport Interfaces
====================
Transport interfaces are meant to handle Physical (layer 1), Data (layer 2), Network (layer 3) and Transport (layer 4)
layers of :ref:`UDS OSI model <knowledge-base-osi-model>` which are unique for every communication bus/network.
First two layers (Physical and Data Link) are handled by some external packages.
The implementation that is common for all Transport Interfaces is located in :mod:`uds.transport_interface`
sub-package.

AbstractTransportInterface
--------------------------
Abstract API that is common for all Transport Interfaces (and therefore buses/networks) is defined in
:class:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface` class.

Attributes:

- :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.segmenter` - segmenter object
  used by this Transport Interface for handling :ref:`segmentation processes <knowledge-base-segmentation>`
- :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.addressing_information`
  - addressing information parameters used by simulated UDS entity
- :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.network_manager`
  - python object used as a network manager (sends and receives frames on/from connected network)

Methods:

- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.is_supported_network_manager`
  - check if provided object can be used as a network manager by this Transport Interface
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.send_packet` - send a single
  packet synchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.async_send_packet` - send
  a single packet asynchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.receive_packet` - receive
  a single packet synchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.async_receive_packet`
  - receive a single packet asynchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.send_message` - send
  a diagnostic message synchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.async_send_message` - send
  a diagnostic message asynchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.receive_message` - receive
  a diagnostic message synchronously
- :meth:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.async_receive_message`
  - receive a diagnostic message asynchronously

.. warning:: **A user shall not use**
  :class:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.

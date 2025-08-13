UDS over Custom Network
=======================
This part of the documentation guides how to use this package's features for networks that are either not implemented
or implemented for other network managers that you plan to use.

To use features of this package, you have to have following implementation prepared in line with the guidelines of this
document:

- `Addressing`_
- `Packet`_
- `Segmentation`_
- `Transport Interface`_

For example, if you want to create UDS over CAN implementation for your own (e.g. in-house implemented) CAN network
manager, all you have to do, is to implement concrete class of CAN Transport Interface
(:class:`~uds.can.transport_interface.common.AbstractCanTransportInterface`).

For network types that are not fully implemented (:ref:`networks implementation status <implementation-status>`) yet,
you must provide your own implementation.

.. seealso:: User guide for :ref:`Diagnostic over CAN <implementation-docan>` and CAN implementation (:mod:`uds.can`).


Addressing
----------
Network specific addressing related implementation is restricted to defining concrete Addressing Information class.
Addressing Information classes define containers for Addressing related parameters. Properly defined object stores
all parameters required for both distinguishing incoming and outcoming packets (for both
:ref:`addressing types <knowledge-base-addressing>`).


AbstractAddressingInformation
`````````````````````````````
:class:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation` defines common API and
contains common code for all addressing information storages. It is located in
:mod:`uds.addressing.abstract_addressing_information`.

Attributes:

- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.rx_physical_params`
- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.tx_physical_params`
- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.rx_functional_params`
- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.tx_functional_params`

Methods:

- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.validate_addressing_params`
- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.is_input_packet`
- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.get_other_end`

Requires implementation in concrete classes (abstract attributes and methods):

- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation._validate_addressing_information`
- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.validate_addressing_params`
- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.is_input_packet`

.. warning:: **A user shall not use**
  :class:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.

.. seealso:: Addressing implementation for CAN - :mod:`uds.can.addressing`


Packet
------
Abstract implementation for Packet feature is located in :mod:`uds.packet`. It contains following abstract classes:

- :class:`~uds.packet.abstract_packet.AbstractPacket`,
- :class:`~uds.packet.abstract_packet.AbstractPacketRecord`
- :class:`~uds.packet.abstract_packet_type.AbstractPacketType`


AbstractPacket
``````````````
:class:`~uds.packet.abstract_packet.AbstractPacket` defines common structure for packets. It is located
:mod:`uds.packet.abstract_packet`.

Attributes:

- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.raw_frame_data`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.packet_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.data_length`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.addressing_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.payload`

Methods:

- :meth:`~uds.packet.abstract_packet.AbstractPacketContainer.__str__`

Requires implementation in concrete classes (abstract attributes and methods):

- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.raw_frame_data`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.packet_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.data_length`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.addressing_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.payload`

.. note:: Each network type would require additional attributes defined.

.. seealso:: Packets implementation for CAN:

  - :class:`~uds.packet.abstract_packet.AbstractPacket.__init__`
  - :class:`~uds.can.packet.abstract_container.AbstractCanPacketContainer`
  - :class:`~uds.can.packet.can_packet.CanPacket`


AbstractPacketRecord
````````````````````
:class:`~uds.packet.abstract_packet.AbstractPacketRecord` defines common structure for packet records
(storage for information about packets that were either transmitted or received).
It is located :mod:`uds.packet.abstract_packet`.

Attributes:

- :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.frame`
- :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.direction`
- :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.transmission_time`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.raw_frame_data`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.packet_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.data_length`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.addressing_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.payload`

Methods:

- :meth:`~uds.packet.abstract_packet.AbstractPacketRecord._validate_frame`
- :meth:`~uds.packet.abstract_packet.AbstractPacketRecord._validate_attributes`
- :meth:`~uds.packet.abstract_packet.AbstractPacketRecord.__init__`
- :meth:`~uds.packet.abstract_packet.AbstractPacketRecord.__str__`

Requires implementation in concrete classes (abstract attributes and methods):

- :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.frame`
- :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.direction`
- :attr:`~uds.packet.abstract_packet.AbstractPacketRecord.transmission_time`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.raw_frame_data`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.packet_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.data_length`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.addressing_type`
- :attr:`~uds.packet.abstract_packet.AbstractPacketContainer.payload`
- :meth:`~uds.packet.abstract_packet.AbstractPacketRecord._validate_frame`
- :meth:`~uds.packet.abstract_packet.AbstractPacketRecord._validate_attributes`

.. note:: Each network type would require additional attributes defined.

.. seealso:: Packet records implementation for CAN - :class:`~uds.can.packet.can_packet.AbstractPacketRecord`


AbstractPacketType
``````````````````
:class:`~uds.packet.abstract_packet_type.AbstractPacketType` is an enum with all possible
:ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` values.
It is located :mod:`uds.packet.abstract_packet_type`.

Methods:

- :meth:`~uds.packet.abstract_packet_type.AbstractPacketType.is_initial_packet_type`

Requires implementation in concrete classes (abstract attributes and methods):

- attributes for each possible :ref:`Network Protocol Control Information (N_PCI) <knowledge-base-n-pci>` value
- :meth:`~uds.packet.abstract_packet_type.AbstractPacketType.is_initial_packet_type`

.. seealso:: Packet types defined for CAN - :class:`~uds.can.packet.can_packet_type.CanPacketType`


Segmentation - TODO
-------------------
Common part of :ref:`segmentation process <knowledge-base-segmentation>` implementation is located in
:mod:`uds.segmentation` sub-package with concrete segmenters defined in sub-packages for dedicated network
types (e.g. :class:`~uds.can.segmenter.CanSegmenter` is located in :mod:`uds.can` sub-package).


AbstractSegmenter
`````````````````
:class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` defines common API and contains common code for all
segmenter classes. Each concrete segmenter class handles segmentation process for a specific network type.

Attributes:

- :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.supported_addressing_information_class` - concrete
  dedicated Addressing Information class (subclass of
  :class:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation`)
  for network type supported by this segmenter
- :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.supported_packet_class` - concrete
  dedicated Packet class (subclass of :class:`~uds.packet.abstract_packet.AbstractPacket`)
  for network type supported by this segmenter
- :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.supported_packet_record_class` - concrete
  dedicated Packet Record class (subclass of :class:`~uds.packet.abstract_packet.AbstractPacketRecord`)
  for network type supported by this segmenter
- :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.addressing_information` - Addressing Information used
  by UDS entity for which segmentation process to be managed

Methods:

- :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_supported_packet_type` - checks whether provided
  object is a packet of a type that can be handled by this segmenter
- :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_supported_packets_sequence_type` - checks whether
  provided object is a sequence fill with packets of supported type
- :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_input_packet` - check if provided packet targets
  this UDS entity (according to configured
  :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.addressing_information`)
- :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_desegmented_message` - check if provided object is
  a complete sequence of packets that can form exactly one diagnostic message
- :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.desegmentation` - perform
  :ref:`desegmentation <knowledge-base-packets-desegmentation>` and form a diagnostic message out of provided packets
- :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.desegmentation` - perform
  :ref:`segmentation <knowledge-base-message-segmentation>` and divide provided diagnostic message into packets

.. warning:: **A user shall not use**
  :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.


Transport Interface - TODO
--------------------------
Transport interfaces are meant to handle Physical (layer 1), Data (layer 2), Network (layer 3) and Transport (layer 4)
layers of :ref:`UDS OSI model <knowledge-base-osi-model>` which are unique for every communication bus/network.
First two layers (Physical and Data Link) are handled by some external packages.
The implementation that is common for all Transport Interfaces is located in :mod:`uds.transport_interface`
sub-package.


AbstractTransportInterface
``````````````````````````
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

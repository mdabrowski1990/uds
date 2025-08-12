Segmentation
============
Common part of :ref:`segmentation process <knowledge-base-segmentation>` implementation is located in
:mod:`uds.segmentation` sub-package with concrete segmenters defined in sub-packages for dedicated network
types (e.g. :class:`~uds.can.segmenter.CanSegmenter` is located in :mod:`uds.can` sub-package).


AbstractSegmenter
-----------------
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

.. warning:: A **user shall not use** :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` **directly**,
  but one is able (and encouraged) to use :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter`
  implementation on any of its children classes.

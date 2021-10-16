Segmentation
============
Implementation related to :ref:`segmentation process <knowledge-base-segmentation>` is located in :mod:`uds.segmentation`
sub-package.


AbstractSegmenter
-----------------
:class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` defines common API and contains common code for all
segmenter classes. Each concrete segmenter class implements segmentation
`strategy <https://www.tutorialspoint.com/design_pattern/strategy_pattern.htm>`_ for a specific bus.

.. warning:: A **user shall not use** :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` **directly**,
   but one is able (and encouraged) to use :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter`
   implementation with any of its children classes.

Attributes defined in :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` class:
 - :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.supported_packet_classes` - readable and abstract (bus specific)
 - :attr:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.initial_packet_types` - readable and abstract (bus specific)

Methods defined in :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` class:
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_supported_packet`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_supported_packets_sequence`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_initial_packet`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.get_consecutive_packets_number`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_following_packets_sequence`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.is_complete_packets_sequence`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.segmentation`
 - :meth:`~uds.segmentation.abstract_segmenter.AbstractSegmenter.desegmentation`

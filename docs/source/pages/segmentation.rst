Segmentation
============
Implementation of :ref:`segmentation process <knowledge-base-segmentation>` is located in :mod:`uds.segmentation`
sub-package.


AbstractSegmenter
-----------------
:class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` defines common API and contains common code for all
segmenter classes. Each concrete segmenter class implements segmentation duty for a specific bus.

.. warning:: A **user shall not use** :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` **directly**,
    but one is able (and encouraged) to use :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter`
    implementation with any of its children classes.

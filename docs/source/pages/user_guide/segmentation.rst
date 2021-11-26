Segmentation
============
Implementation of :ref:`segmentation process <knowledge-base-segmentation>` is located in :mod:`uds.segmentation`
sub-package.


AbstractSegmenter
-----------------
:class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` defines common API and contains common code for all
segmenter classes. Each concrete segmenter class handles segmentation process for a specific bus.

.. warning:: A **user shall not use** :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` **directly**,
    but one is able (and encouraged) to use :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter`
    implementation with any of its children classes.


CanSegmenter
------------
:class:`~uds.segmentation.can_segmenter.CanSegmenter` handles segmentation process on CAN bus.

Following functionalities are provided by :class:`~uds.segmentation.can_segmenter.CanSegmenter`:

- Configuration of the segmenter:

  As a user, you are able to configure :class:`~uds.segmentation.can_segmenter.CanSegmenter`


  **Example code:**

    .. code-block::  python

        import uds


- Diagnostic message segmentation:

- CAN packets desegmentation:

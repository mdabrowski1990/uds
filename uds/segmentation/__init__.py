"""
A subpackage with tools for handing segmentation.

:ref:`Segmentation <knowledge-base-segmentation>` defines two processes:
 - :ref:`diagnostic message segmentation <knowledge-base-message-segmentation>`
 - :ref:`packets desegmentation <knowledge-base-packets-desegmentation>`

This subpackage contains implementation of:
 - common API interface for all segmentation duties
 - classes that handles segmentation for each bus
"""

from .abstract_segmenter import SegmentationError, AbstractSegmenter

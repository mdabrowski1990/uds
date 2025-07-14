"""
A subpackage with tools for segmentation handing.

:ref:`Segmentation <knowledge-base-segmentation>` defines two processes:
 - :ref:`diagnostic message segmentation <knowledge-base-message-segmentation>`
 - :ref:`packets desegmentation <knowledge-base-packets-desegmentation>`

This subpackage contains implementation of common API interface for all segmentation tasks.
"""

from .abstract_segmenter import AbstractSegmenter, SegmentationError

"""
A subpackage with tools for executing :ref:`segmentation <knowledge-base-segmentation>`.

It defines:
 - common API interface for all segmentation duties
 - classes that handles segmentation for each bus
"""

from .abstract_segmenter import SegmentationError, AbstractSegmenter

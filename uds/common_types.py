"""Container with common types (and its aliases) used in the package by many modules."""

__all__ = ["TimeMilliseconds"]

from typing import Union

# General
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint for Python 3.9.
# pylint: disable=unsubscriptable-object
TimeMilliseconds = Union[int, float]

"""Container with all types (and its aliases) used by the module."""

__all__ = ["RawByte", "RawMessage", "PDUs"]

from typing import Sequence

from .pdu import AbstractPDU

RawByte = int
# TODO: since python 3.9 Sequence can be replaced with Union[list[int], tuple[int]]
#  keep Sequences way for backward compatibility with older Python version or create specific file version for
#  Python 3.9 or newer
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint for Python 3.9.
RawMessage = Sequence[RawByte]  # pylint: disable=unsubscriptable-object
PDUs = Sequence[AbstractPDU]  # pylint: disable=unsubscriptable-object

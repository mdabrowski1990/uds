"""Container with all types (and its aliases) used by the module."""

__all__ = ["RawByte", "RawMessage", "PDUs"]

from typing import Sequence

from .pdu import AbstractPDU

# TODO: since python 3.9 it can be replaced with Union[list[int], tuple[int]]; keep this way for backward compatibility
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint.
RawByte = int
RawMessage = Sequence[RawByte]  # pylint: disable=unsubscriptable-object
PDUs = Sequence[AbstractPDU]  # pylint: disable=unsubscriptable-object

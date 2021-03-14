"""Container with all types (and its aliases) used by the module."""

__all__ = ["RawByte", "RawMessage", "RawMessageTuple", "PDUs", "PDUsTuple"]

from typing import Union, Tuple, List

from .pdu import AbstractPDU

RawByte = int
# TODO: since python 3.9 List[int] can be replaced with list[int] (similar for tuples)
#  keep this way for backward compatibility with older Python versions or create specific file version for
#  Python 3.9 or newer
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint for Python 3.9.
# pylint: disable=unsubscriptable-object
RawMessageTuple = Tuple[RawByte, ...]
RawMessage = Union[RawMessageTuple, List[RawByte]]
PDUsTuple = Tuple[AbstractPDU, ...]
PDUs = Union[PDUsTuple, List[AbstractPDU]]

"""Container with all types (and its aliases) used by the module."""

__all__ = ["PDU", "PDUs",
           "UdsMessage", "UdsRequest", "UdsRequests", "UdsResponse", "UdsResponses",
           "TimeMilliseconds"]

from typing import List, Union

from uds.messages import AbstractPDU, UdsResponse, UdsRequest
from uds.utilities import TimeMilliseconds

PDU = AbstractPDU
PDUs = List[AbstractPDU]

UdsMessage = Union[UdsResponse, UdsRequest]  # pylint: disable=unsubscriptable-object
UdsResponses = List[UdsResponse]
UdsRequests = List[UdsRequest]

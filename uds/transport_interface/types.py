"""Container with all types (and its aliases) used by the module."""

__all__ = ["PDU", "PDUs",
           "UdsMessage", "UdsRequest", "UdsRequests", "UdsResponse", "UdsResponses",
           "TimeMilliseconds"]

from typing import List, Union

from uds.messages import AbstractNPDU, UdsResponse, UdsRequest
from uds.utilities import TimeMilliseconds

PDU = AbstractNPDU
PDUs = List[AbstractNPDU]

UdsMessage = Union[UdsResponse, UdsRequest]  # pylint: disable=unsubscriptable-object
UdsResponses = List[UdsResponse]
UdsRequests = List[UdsRequest]

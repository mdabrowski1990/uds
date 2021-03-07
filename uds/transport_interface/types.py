"""Container with all types (and its aliases) used by the module."""

__all__ = ["AddressingType", "AddressingTypes", "PDU", "PDUs",
           "UdsMessage", "UdsRequest", "UdsResponse", "UdsResponses"]

from typing import List, Union

from uds.messages import AddressingType, AbstractPDU, UdsResponse, UdsRequest

AddressingTypes = List[AddressingType]

PDU = AbstractPDU
PDUs = List[AbstractPDU]

UdsMessage = Union[UdsResponse, UdsRequest]  # pylint: disable=unsubscriptable-object
UdsResponses = List[UdsResponse]

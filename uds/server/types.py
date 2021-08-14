"""Container with all types (and its aliases) used by the module."""

__all__ = ["AddressingTypesContainer", "AddressingTypesSet", "AddressingType",
           "UdsRequest", "UdsResponse", "ResponseSID", "NRC",
           "SIDRawValue", "SIDRawValuesContainer", "SIDRawValuesSet", "POSSIBLE_REQUEST_SIDS",
           "StateName", "StateNames", "StateValue", "StateValuesContainer", "CurrentStatesValues", "StateTransition",
           "TimeMilliseconds",
           "ResponsesTimetable",
           "TransportInterfaceServer"]

from typing import Any, Union, List, Tuple, Set, Dict
from datetime import datetime

from uds.utilities import TimeMilliseconds
from uds.transport_interface import TransportInterfaceServer
from uds.messages import UdsRequest, UdsResponse, AddressingType, ResponseSID, POSSIBLE_REQUEST_SIDS, NRC

# pylint: disable=unsubscriptable-object

# UDS Messages related
AddressingTypesSet = Set[AddressingType]
AddressingTypesContainer = Union[List[AddressingType], Tuple[AddressingType, ...], AddressingTypesSet]
SIDRawValue = int
SIDRawValuesSet = Set[SIDRawValue]
SIDRawValuesContainer = Union[List[SIDRawValue], Tuple[SIDRawValue, ...], SIDRawValuesSet]

# ServerState related
StateName = str
StateNames = Set[StateName]
StateValue = Any
StateValuesContainer = Union[List[StateValue], Tuple[StateValue, ...], Set[StateValue]]
StateTransition = Tuple[StateValue, StateValue]
CurrentStatesValues = Dict[StateName, StateValue]

# Server related
PlannedResponse = Tuple[UdsResponse, datetime]
ResponsesTimetable = List[PlannedResponse]

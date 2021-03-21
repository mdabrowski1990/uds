"""Container with all types (and its aliases) used by the module."""

__all__ = ["AddressingType", "AddressingTypesContainer", "AddressingTypesSet",
           "UdsRequest", "UdsResponse", "SIDRawValue", "SIDRawValuesContainer", "SIDRawValuesSet",
           "StateName", "StateNames", "StateValue", "StateValuesContainer", "CurrentStatesValues", "StateTransition",
           "TimeMilliseconds"]

from typing import Any, Union, List, Tuple, Set, Dict

from uds.common_types import TimeMilliseconds
from uds.messages import UdsRequest, UdsResponse, AddressingType

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

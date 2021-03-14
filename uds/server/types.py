"""Container with all types (and its aliases) used by the module."""

__all__ = ["AddressingType", "AddressingTypesContainer", "AddressingTypesSet",
           "UdsRequest", "UdsResponse", "SIDRawValue", "SIDRawValuesContainer", "SIDRawValuesSet",
           "StateName", "StateNames", "StateValue", "StateValuesContainer", "CurrentStatesValues", "StateTransition",
           "TimeMilliseconds"]

from typing import Any, Union, List, Tuple, Set, Dict

from uds.messages import UdsRequest, UdsResponse, AddressingType

# General
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint for Python 3.9.
# pylint: disable=unsubscriptable-object
TimeMilliseconds = Union[int, float]

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

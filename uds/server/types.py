"""Container with all types (and its aliases) used by the module."""

# __all__ = ["TimeMilliseconds"]

from typing import Any, Optional, Union, Tuple, Set, Container, Dict, List

from uds.messages import UdsRequest, UdsResponse, AddressingType


# General
TimeMilliseconds = Union[int, float]

# ServerState related
StateName = str
StateNames = Set[StateName]
StateValue = Any
StateValues = Container[StateValue]
StateTransition = Tuple[StateValue, StateValue]
RequestSID = int
RequestSIDs = Container[RequestSID]
AddressingTypes = Union[Tuple[AddressingType, ...], List[AddressingType], Set[AddressingType]]
CurrentStatesValues = Dict[StateName, StateValue]

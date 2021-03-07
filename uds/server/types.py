"""Container with all types (and its aliases) used by the module."""

__all__ = ["AddressingType", "AddressingTypes",
           "UdsRequest", "UdsResponse", "RequestSIDRawValue", "RequestSIDRawValues",
           "StateName", "StateNames", "StateValue", "StateValues", "StateTransition", "CurrentStatesValues",
           "TimeMilliseconds"]

from typing import Any, Union, Tuple, Set, Container, Dict

from uds.messages import UdsRequest, UdsResponse, AddressingType


# General
TimeMilliseconds = Union[int, float]

# UDS Messages related
AddressingTypes = Container[AddressingType]
RequestSIDRawValue = int
RequestSIDRawValues = Container[RequestSIDRawValue]

# ServerState related
StateName = str
StateNames = Set[StateName]
StateValue = Any
StateValues = Container[StateValue]
StateTransition = Tuple[StateValue, StateValue]
CurrentStatesValues = Dict[StateName, StateValue]

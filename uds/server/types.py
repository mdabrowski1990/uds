"""Container with all types (and its aliases) used by the module."""

__all__ = ["AddressingType", "AddressingTypes",
           "UdsRequest", "UdsResponse", "RequestSIDRawValue", "RequestSIDRawValues",
           "StateName", "StateNames", "StateValue", "StateValues", "StateTransition", "CurrentStatesValues",
           "TimeMilliseconds"]

from typing import Any, Union, Tuple, Set, Iterable, Dict

from uds.messages import UdsRequest, UdsResponse, AddressingType


# General
# TODO: prospector supports only pylint version 2.5 that has serious problem with Aliases in Python 3.9.
#  Remove unsubscriptable-object once prospector supports newer versions of pylint for Python 3.9.
TimeMilliseconds = Union[int, float]  # pylint: disable=unsubscriptable-object

# UDS Messages related
AddressingTypes = Iterable[AddressingType]
RequestSIDRawValue = int
RequestSIDRawValues = Iterable[RequestSIDRawValue]

# ServerState related
StateName = str
StateNames = Set[StateName]
StateValue = Any
StateValues = Iterable[StateValue]
StateTransition = Tuple[StateValue, StateValue]
CurrentStatesValues = Dict[StateName, StateValue]

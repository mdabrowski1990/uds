"""Definitions of typical diagnostic communication states."""

__all__ = ["DEFAULT_DIAGNOSTIC_SESSION_STATE",
           "DEFAULT_SECURITY_ACCESS_STATE",
           "DEFAULT_AUTHENTICATION_STATE",
           "DEFAULT_SECURED_TRANSMISSION_STATE",
           "DEFAULT_ENGINE_STATE", ]

from .state import State
from uds.addressing import AddressingType

DEFAULT_DIAGNOSTIC_SESSION_STATE = State(name="Session",
                                         possible_values=range(0x80))
DEFAULT_SECURITY_ACCESS_STATE = State(name="Unlocked SecurityAccess level",
                                      possible_values={"Locked", *range(1, 0x80, 2)})
DEFAULT_AUTHENTICATION_STATE = State(name="Authentication state",
                                     possible_values={"noone authenticated",
                                                      "Client authenticated",
                                                      "Server authenticated",
                                                      "Client and server authenticated"})
DEFAULT_SECURED_TRANSMISSION_STATE = State(name="Secured Transmission",
                                           possible_values={"yes", "no"})
DEFAULT_ENGINE_STATE = State(name="Engine state",
                             possible_values={"ON", "OFF"})
DEFAULT_ADDRESSING_TYPE_STATE = State(name="AddressingType",
                                      possible_values=set(AddressingType))

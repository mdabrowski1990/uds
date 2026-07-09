"""Definitions of typical :ref:`diagnostic communication states <knowledge-base-states>`."""

__all__ = ["DEFAULT_DIAGNOSTIC_SESSION_STATE",
           "DEFAULT_SECURITY_ACCESS_STATE",
           "DEFAULT_AUTHENTICATION_STATE",
           "DEFAULT_SECURED_TRANSMISSION_STATE",
           "DEFAULT_IGNITION_STATE",
           "DEFAULT_ENGINE_STATE",
           "DEFAULT_ADDRESSING_TYPE_STATE"]

from uds.addressing import AddressingType

from .state import State

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
DEFAULT_IGNITION_STATE = State(name="Ignition",
                             possible_values={"ON", "OFF"})
DEFAULT_ENGINE_STATE = State(name="Engine",
                             possible_values={"ON", "OFF"})
DEFAULT_ADDRESSING_TYPE_STATE = State(name="AddressingType",
                                      possible_values=set(AddressingType))

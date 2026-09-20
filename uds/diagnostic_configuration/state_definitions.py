"""Predefined State objects representing common :ref:`diagnostic communication states <knowledge-base-states>`."""

__all__ = ["DEFAULT_DIAGNOSTIC_SESSION_STATE",
           "DEFAULT_SECURITY_ACCESS_STATE",
           "DEFAULT_AUTHENTICATION_STATE",
           "DEFAULT_IGNITION_STATE",
           "DEFAULT_ENGINE_STATE",
           "DEFAULT_SECURED_TRANSMISSION_STATE",
           "DEFAULT_ADDRESSING_TYPE_STATE"]

from uds.addressing import AddressingType
from uds.utilities import OFF_ON_MAPPING

from .state import State

DEFAULT_DIAGNOSTIC_SESSION_STATE = State(name="Session",
                                         possible_values=range(0x80))
"""State representing the current :ref:`Diagnostic Session <knowledge-base-state-session>`."""

DEFAULT_SECURITY_ACCESS_STATE = State(name="SecurityAccess",
                                      possible_values={"Locked", *range(1, 0x80, 2)})
"""State representing the currently unlocked :ref:`Security Access <knowledge-base-state-security-access>` level."""

DEFAULT_AUTHENTICATION_STATE = State(name="Authentication",
                                     possible_values={"noone authenticated",
                                                      "Client authenticated",
                                                      "Server authenticated",
                                                      "Client and server authenticated"})
"""State representing the current :ref:`Authentication <knowledge-base-state-authentication>` status."""

DEFAULT_IGNITION_STATE = State(name="Ignition",
                               possible_values=OFF_ON_MAPPING.values())
"""State indicating whether the vehicle ignition is ON or OFF."""

DEFAULT_ENGINE_STATE = State(name="Engine",
                             possible_values=OFF_ON_MAPPING.values())
"""State indicating whether the engine is running."""

DEFAULT_SECURED_TRANSMISSION_STATE = State(name="SecuredTransmission",
                                           possible_values={"yes", "no"})
"""State indicating whether secured data transmission is active."""

DEFAULT_ADDRESSING_TYPE_STATE = State(name="AddressingType",
                                      possible_values=set(AddressingType))
"""State representing the current :class:`~uds.addressing.AddressingType`."""

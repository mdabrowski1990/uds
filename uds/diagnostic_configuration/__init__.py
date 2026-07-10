"""
Implementation for diagnostic configuration.

Tools for assessing states in which diagnostic messages are accessible by ECU.
"""

from .ecu_configuration import EcuDiagnosticConfiguration
from .state import State
from .state_definitions import (
    DEFAULT_ADDRESSING_TYPE_STATE,
    DEFAULT_AUTHENTICATION_STATE,
    DEFAULT_DIAGNOSTIC_SESSION_STATE,
    DEFAULT_ENGINE_STATE,
    DEFAULT_IGNITION_STATE,
    DEFAULT_SECURED_TRANSMISSION_STATE,
    DEFAULT_SECURITY_ACCESS_STATE,
)

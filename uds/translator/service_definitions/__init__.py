"""Base definitions of translators for diagnostic services."""

from .clear_diagnostic_information import (
    CLEAR_DIAGNOSTIC_INFORMATION,
    CLEAR_DIAGNOSTIC_INFORMATION_2013,
    CLEAR_DIAGNOSTIC_INFORMATION_2020,
)
from .diagnostic_session_control import DIAGNOSTIC_SESSION_CONTROL
from .ecu_reset import ECU_RESET
from .read_dtc_information import READ_DTC_INFORMATION, READ_DTC_INFORMATION_2013, READ_DTC_INFORMATION_2020
from .tester_present import TESTER_PRESENT

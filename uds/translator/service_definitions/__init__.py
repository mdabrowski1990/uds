"""Base definitions of translators for diagnostic services."""

from .authentication import AUTHENTICATION
from .clear_diagnostic_information import (
    CLEAR_DIAGNOSTIC_INFORMATION,
    CLEAR_DIAGNOSTIC_INFORMATION_2013,
    CLEAR_DIAGNOSTIC_INFORMATION_2020,
)
from .diagnostic_session_control import DIAGNOSTIC_SESSION_CONTROL
from .dynamically_define_data_identifier import (
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020,
)
from .ecu_reset import ECU_RESET
from .read_data_by_identifier import READ_DATA_BY_IDENTIFIER, READ_DATA_BY_IDENTIFIER_2013, READ_DATA_BY_IDENTIFIER_2020
from .read_data_by_periodic_identifier import READ_DATA_BY_PERIODIC_IDENTIFIER
from .read_dtc_information import READ_DTC_INFORMATION, READ_DTC_INFORMATION_2013, READ_DTC_INFORMATION_2020
from .read_memory_by_address import READ_MEMORY_BY_ADDRESS
from .security_access import SECURITY_ACCESS
from .tester_present import TESTER_PRESENT

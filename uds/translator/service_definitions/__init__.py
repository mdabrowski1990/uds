"""Translators for :ref:`diagnostic services <knowledge-base-service>`."""

from .access_timing_parameter import ACCESS_TIMING_PARAMETER_2013
from .authentication import AUTHENTICATION
from .clear_diagnostic_information import (
    CLEAR_DIAGNOSTIC_INFORMATION,
    CLEAR_DIAGNOSTIC_INFORMATION_2013,
    CLEAR_DIAGNOSTIC_INFORMATION_2020,
)
from .control_dtc_setting import CONTROL_DTC_SETTING
from .diagnostic_session_control import DIAGNOSTIC_SESSION_CONTROL
from .dynamically_define_data_identifier import (
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020,
)
from .ecu_reset import ECU_RESET
from .input_output_control_by_identifier import (
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013,
    INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020,
)
from .read_data_by_identifier import READ_DATA_BY_IDENTIFIER, READ_DATA_BY_IDENTIFIER_2013, READ_DATA_BY_IDENTIFIER_2020
from .read_data_by_periodic_identifier import READ_DATA_BY_PERIODIC_IDENTIFIER
from .read_dtc_information import READ_DTC_INFORMATION, READ_DTC_INFORMATION_2013, READ_DTC_INFORMATION_2020
from .read_memory_by_address import READ_MEMORY_BY_ADDRESS
from .read_scaling_data_by_identifier import (
    READ_SCALING_DATA_BY_IDENTIFIER,
    READ_SCALING_DATA_BY_IDENTIFIER_2013,
    READ_SCALING_DATA_BY_IDENTIFIER_2020,
)
from .request_download import REQUEST_DOWNLOAD
from .request_file_transfer import REQUEST_FILE_TRANSFER, REQUEST_FILE_TRANSFER_2013, REQUEST_FILE_TRANSFER_2020
from .request_transfer_exit import REQUEST_TRANSFER_EXIT
from .request_upload import REQUEST_UPLOAD
from .response_on_event import RESPONSE_ON_EVENT, RESPONSE_ON_EVENT_2013, RESPONSE_ON_EVENT_2020
from .routine_control import ROUTINE_CONTROL
from .secured_data_transmission import (
    SECURED_DATA_TRANSMISSION,
    SECURED_DATA_TRANSMISSION_2013,
    SECURED_DATA_TRANSMISSION_2020,
)
from .security_access import SECURITY_ACCESS
from .tester_present import TESTER_PRESENT
from .transfer_data import TRANSFER_DATA
from .write_data_by_identifier import (
    WRITE_DATA_BY_IDENTIFIER,
    WRITE_DATA_BY_IDENTIFIER_2013,
    WRITE_DATA_BY_IDENTIFIER_2020,
)
from .write_memory_by_address import WRITE_MEMORY_BY_ADDRESS

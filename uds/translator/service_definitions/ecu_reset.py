"""Translation for ECUReset (SID 0x11) service."""

__all__ = ["ECU_RESET", "ECU_RESET_2020", "ECU_RESET_2013"]

from uds.message import RequestSID
from uds.translator.data_record_definitions import (
    CONDITIONAL_POWER_DOWN_TIME,
    ECU_RESET_SUB_FUNCTION_2013,
    ECU_RESET_SUB_FUNCTION_2020,
)
from uds.translator.service import Service

ECU_RESET_2013 = Service(request_sid=RequestSID.ECUReset,
                         request_structure=[ECU_RESET_SUB_FUNCTION_2013],
                         response_structure=[ECU_RESET_SUB_FUNCTION_2013])
"""Translator for :ref:`ECUReset <knowledge-base-service-ecu-reset>` service compatible with ISO 14229-1:2013."""
ECU_RESET_2020 = Service(request_sid=RequestSID.ECUReset,
                         request_structure=[ECU_RESET_SUB_FUNCTION_2020],
                         response_structure=[ECU_RESET_SUB_FUNCTION_2020,
                                             CONDITIONAL_POWER_DOWN_TIME])
"""Translator for :ref:`ECUReset <knowledge-base-service-ecu-reset>` service compatible with ISO 14229-1:2020."""

ECU_RESET = ECU_RESET_2020
"""Default translator for :ref:`ECUReset <knowledge-base-service-ecu-reset>` service."""

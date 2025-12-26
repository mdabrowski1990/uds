""":ref:`ReadDTCInformation (SID 0x19) <knowledge-base-service-read-dtc-information>` translation."""

__all__ = ["READ_DTC_INFORMATION", "READ_DTC_INFORMATION_2020", "READ_DTC_INFORMATION_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2013,
    CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2020,
    CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2013,
    CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2020,
    READ_DTC_INFORMATION_SUB_FUNCTION_2013,
    READ_DTC_INFORMATION_SUB_FUNCTION_2020,
)
from ..service import Service

READ_DTC_INFORMATION_2020 = Service(request_sid=RequestSID.ReadDTCInformation,
                                    request_structure=(READ_DTC_INFORMATION_SUB_FUNCTION_2020,
                                                       CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2020),
                                    response_structure=(READ_DTC_INFORMATION_SUB_FUNCTION_2020,
                                                        CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2020))
"""Translator for :ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` service compatible with
ISO 14229-1:2020."""

READ_DTC_INFORMATION_2013 = Service(request_sid=RequestSID.ReadDTCInformation,
                                    request_structure=(READ_DTC_INFORMATION_SUB_FUNCTION_2013,
                                                       CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2013),
                                    response_structure=(READ_DTC_INFORMATION_SUB_FUNCTION_2013,
                                                        CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2013))
"""Translator for :ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` service compatible with
ISO 14229-1:2013."""

READ_DTC_INFORMATION = READ_DTC_INFORMATION_2020
"""Default translator for :ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` service."""

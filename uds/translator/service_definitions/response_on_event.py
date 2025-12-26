"""Translation for :ref:`ResponseOnEvent (SID 0x86) <knowledge-base-service-response-on-event>` service."""

__all__ = ["RESPONSE_ON_EVENT", "RESPONSE_ON_EVENT_2020", "RESPONSE_ON_EVENT_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2013,
    CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2020,
    CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2013,
    CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2020,
    RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
    RESPONSE_ON_EVENT_SUB_FUNCTION_2020,
)
from ..service import Service

RESPONSE_ON_EVENT_2013 = Service(request_sid=RequestSID.ResponseOnEvent,
                                 request_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
                                                    CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2013),
                                 response_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
                                                     CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2013))
"""Translator for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service
compatible with ISO 14229-1:2013."""

RESPONSE_ON_EVENT_2020 = Service(request_sid=RequestSID.ResponseOnEvent,
                                 request_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2020,
                                                    CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2020),
                                 response_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2020,
                                                     CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2020))
"""Translator for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service
compatible with ISO 14229-1:2020."""

RESPONSE_ON_EVENT = RESPONSE_ON_EVENT_2020
"""Default translator for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service."""

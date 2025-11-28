"""Translation for ResponseOnEvent (SID 0x31) service."""

__all__ = ["RESPONSE_ON_EVENT"]

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import (
    RESPONSE_ON_EVENT_SUB_FUNCTION_2013, RESPONSE_ON_EVENT_SUB_FUNCTION_2020
)
from ..service import Service

REQUEST_CONTINUATION_MAPPING_2013 = {
}
REQUEST_CONTINUATION_MAPPING_2020 = {
}

RESPONSE_CONTINUATION_MAPPING_2013 = {
}
RESPONSE_CONTINUATION_MAPPING_2020 = {
}

CONDITIONAL_REQUEST_CONTINUATION_2013 = ConditionalMappingDataRecord(
    mapping=REQUEST_CONTINUATION_MAPPING_2013 | {key + offset: value
                                                 for key, value in REQUEST_CONTINUATION_MAPPING_2013.items()
                                                 for offset in (0x00, 0x40, 0x80, 0xC0)})
CONDITIONAL_REQUEST_CONTINUATION_2020 = ConditionalMappingDataRecord(
    mapping=REQUEST_CONTINUATION_MAPPING_2020 | {key + offset: value
                                                 for key, value in REQUEST_CONTINUATION_MAPPING_2020.items()
                                                 for offset in (0x00, 0x40, 0x80, 0xC0)})

CONDITIONAL_RESPONSE_CONTINUATION_2013 = ConditionalMappingDataRecord(
    mapping=RESPONSE_CONTINUATION_MAPPING_2013 | {key + offset: value
                                                  for key, value in RESPONSE_CONTINUATION_MAPPING_2013.items()
                                                  for offset in (0x00, 0x40, 0x80, 0xC0)})
CONDITIONAL_RESPONSE_CONTINUATION_2020 = ConditionalMappingDataRecord(
    mapping=RESPONSE_CONTINUATION_MAPPING_2020 | {key + offset: value
                                                  for key, value in RESPONSE_CONTINUATION_MAPPING_2020.items()
                                                  for offset in (0x00, 0x40, 0x80, 0xC0)})

RESPONSE_ON_EVENT_2013 = Service(request_sid=RequestSID.ResponseOnEvent,
                                 request_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
                                                    CONDITIONAL_REQUEST_CONTINUATION_2013),
                                 response_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
                                                     CONDITIONAL_RESPONSE_CONTINUATION_2013))
"""Translator for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service
compatible with ISO 14229-1:2013."""

RESPONSE_ON_EVENT_2020 = Service(request_sid=RequestSID.ResponseOnEvent,
                                 request_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2020,
                                                    CONDITIONAL_REQUEST_CONTINUATION_2020),
                                 response_structure=(RESPONSE_ON_EVENT_SUB_FUNCTION_2020,
                                                     CONDITIONAL_RESPONSE_CONTINUATION_2020))
"""Translator for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service 
compatible with ISO 14229-1:2020."""

RESPONSE_ON_EVENT = RESPONSE_ON_EVENT_2020
"""Default translator for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service."""

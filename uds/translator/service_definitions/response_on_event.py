"""Translation for ResponseOnEvent (SID 0x31) service."""

__all__ = ["RESPONSE_ON_EVENT"]

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import (
    EVENT_TYPE_RECORD_DID_2013,
    EVENT_TYPE_RECORD_DID_2020,
    EVENT_TYPE_RECORD_DID_COMPARE_2013,
    EVENT_TYPE_RECORD_DID_COMPARE_2020,
    EVENT_TYPE_RECORD_DTC_STATUS_MASK,
    EVENT_TYPE_RECORD_READ_DTC_SUB_FUNCTION_2020,
    EVENT_TYPE_RECORD_TIMER_SCHEDULE,
    EVENT_WINDOW_TIME_2013,
    EVENT_WINDOW_TIME_2020,
    RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
    RESPONSE_ON_EVENT_SUB_FUNCTION_2020, EVENT_TYPE_RECORD_READ_DTC_RECORD_2020, EVENT_TYPE_RECORD_READ_DTC_RECORD_2020, CONDITIONAL_EVENT_TYPE_RECORD_DTC_RECORD,
)
from ..service import Service

REQUEST_CONTINUATION_MAPPING_2013 = {
    0x00: (EVENT_WINDOW_TIME_2013,),
    0x01: (EVENT_WINDOW_TIME_2013, EVENT_TYPE_RECORD_DTC_STATUS_MASK),
    0x02: (EVENT_WINDOW_TIME_2013, EVENT_TYPE_RECORD_TIMER_SCHEDULE),
    0x03: (EVENT_WINDOW_TIME_2013, EVENT_TYPE_RECORD_DID_2013),
    0x04: (EVENT_WINDOW_TIME_2013, ),
    0x05: (EVENT_WINDOW_TIME_2013, ),
    0x06: (EVENT_WINDOW_TIME_2013, ),
    0x07: (EVENT_WINDOW_TIME_2013, EVENT_TYPE_RECORD_DID_COMPARE_2013),
}
REQUEST_CONTINUATION_MAPPING_2020 = {
    0x00: (EVENT_WINDOW_TIME_2020, ),
    0x01: (EVENT_WINDOW_TIME_2020, EVENT_TYPE_RECORD_DTC_STATUS_MASK),
    0x03: (EVENT_WINDOW_TIME_2020, EVENT_TYPE_RECORD_DID_2020),
    0x04: (EVENT_WINDOW_TIME_2020, ),
    0x05: (EVENT_WINDOW_TIME_2020, ),
    0x06: (EVENT_WINDOW_TIME_2020, ),
    0x07: (EVENT_WINDOW_TIME_2020, EVENT_TYPE_RECORD_DID_COMPARE_2020),
    0x08: (EVENT_WINDOW_TIME_2020, EVENT_TYPE_RECORD_READ_DTC_SUB_FUNCTION_2020),
    0x09: (EVENT_WINDOW_TIME_2020, EVENT_TYPE_RECORD_READ_DTC_RECORD_2020, CONDITIONAL_EVENT_TYPE_RECORD_DTC_RECORD),
}

RESPONSE_CONTINUATION_MAPPING_2013 = {
}
RESPONSE_CONTINUATION_MAPPING_2020 = {
}

CONDITIONAL_REQUEST_CONTINUATION_2013 = ConditionalMappingDataRecord(mapping=REQUEST_CONTINUATION_MAPPING_2013,
                                                                     value_mask=0x3F)
CONDITIONAL_REQUEST_CONTINUATION_2020 = ConditionalMappingDataRecord(mapping=REQUEST_CONTINUATION_MAPPING_2020,
                                                                     value_mask=0x3F)

CONDITIONAL_RESPONSE_CONTINUATION_2013 = ConditionalMappingDataRecord(mapping=RESPONSE_CONTINUATION_MAPPING_2013,
                                                                      value_mask=0x3F)
CONDITIONAL_RESPONSE_CONTINUATION_2020 = ConditionalMappingDataRecord(mapping=RESPONSE_CONTINUATION_MAPPING_2020,
                                                                      value_mask=0x3F)

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

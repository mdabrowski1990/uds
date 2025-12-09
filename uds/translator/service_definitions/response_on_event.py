"""Translation for ResponseOnEvent (SID 0x31) service."""

__all__ = ["RESPONSE_ON_EVENT", "RESPONSE_ON_EVENT_2020", "RESPONSE_ON_EVENT_2013"]

from typing import Tuple, Union, List

from uds.message import RequestSID

from .. import RawDataRecord
from ..data_record import ConditionalFormulaDataRecord, ConditionalMappingDataRecord, MappingDataRecord
from ..data_record_definitions import (
    CONDITIONAL_EVENT_TYPE_RECORD_09,
    EVENT_TYPE_RECORD_01,
    EVENT_TYPE_RECORD_02,
    EVENT_TYPE_RECORD_03_2013,
    EVENT_TYPE_RECORD_03_2020,
    EVENT_TYPE_RECORD_07_2013,
    EVENT_TYPE_RECORD_07_2020,
    EVENT_TYPE_RECORD_08_2020,
    EVENT_TYPE_RECORD_09_2020,
    EVENT_WINDOW_TIME_2013,
    EVENT_WINDOW_TIME_2020,
    NUMBER_OF_IDENTIFIED_EVENTS,
    RESPONSE_ON_EVENT_SUB_FUNCTION_2013,
    RESPONSE_ON_EVENT_SUB_FUNCTION_2020,
    SERVICE_TO_RESPOND,
)
from ..data_record_definitions.did import (
    get_event_type_record_03_2013,
    get_event_type_record_03_2020,
    get_event_type_record_07_2013,
    get_event_type_record_07_2020,
)
from ..data_record_definitions.dtc import (
    get_conditional_event_type_record_09,
    get_event_type_record_01,
    get_event_type_record_09,
)
from ..data_record_definitions.other import (
    event_type_of_active_event_2013,
    event_type_of_active_event_2020,
    get_event_type_record_02,
    get_event_type_record_08,
    get_event_window_2013,
    get_event_window_2020,
    get_service_to_respond,
)
from ..service import Service


def get_active_events_2013(number_of_activated_events: int
                           ) -> Tuple[Union[RawDataRecord, MappingDataRecord, ConditionalMappingDataRecord], ...]:
    """
    Get activated events (event = reportActivatedEvents).

    :param number_of_activated_events: Number of activated events.

    :return: Data Records for Activated Events.
    """
    data_records: List[Union[RawDataRecord, MappingDataRecord, ConditionalMappingDataRecord]] = []
    for event_number in range(1, number_of_activated_events + 1):
        data_records.append(event_type_of_active_event_2013(event_number))
        data_records.append(ConditionalMappingDataRecord(mapping={
            0x01: (get_event_window_2013(event_number),
                   get_event_type_record_01(event_number),
                   get_service_to_respond(event_number)),
            0x02: (get_event_window_2013(event_number),
                   get_event_type_record_02(event_number),
                   get_service_to_respond(event_number)),
            0x03: (get_event_window_2013(event_number),
                   get_event_type_record_03_2013(event_number),
                   get_service_to_respond(event_number)),
            0x07: (get_event_window_2013(event_number),
                   get_event_type_record_07_2013(event_number),
                   get_service_to_respond(event_number)),
        },
            value_mask=0x3F))
    return tuple(data_records)


def get_active_events_2020(number_of_activated_events: int
                           ) -> Tuple[Union[RawDataRecord, MappingDataRecord, ConditionalMappingDataRecord], ...]:
    """
    Get activated events (event = reportActivatedEvents).

    :param number_of_activated_events: Number of activated events.

    :return: Data Records for Activated Events.
    """
    data_records: List[Union[RawDataRecord, MappingDataRecord, ConditionalMappingDataRecord]] = []
    for event_number in range(1, number_of_activated_events + 1):
        data_records.append(event_type_of_active_event_2020(event_number))
        data_records.append(ConditionalMappingDataRecord(mapping={
            0x01: (get_event_window_2020(event_number),
                   get_event_type_record_01(event_number),
                   get_service_to_respond(event_number)),
            0x03: (get_event_window_2020(event_number),
                   get_event_type_record_03_2020(event_number),
                   get_service_to_respond(event_number)),
            0x07: (get_event_window_2020(event_number),
                   get_event_type_record_07_2020(event_number),
                   get_service_to_respond(event_number)),
            0x08: (get_event_window_2020(event_number),
                   get_event_type_record_08(event_number),
                   get_service_to_respond(event_number)),
            0x09: (get_event_window_2020(event_number),
                   get_event_type_record_09(event_number),
                   get_conditional_event_type_record_09(event_number),
                   get_service_to_respond(event_number)),
        },
            value_mask=0x3F))
    return tuple(data_records)


CONDITIONAL_ACTIVATED_EVENTS_2013 = ConditionalFormulaDataRecord(formula=get_active_events_2013)
CONDITIONAL_ACTIVATED_EVENTS_2020 = ConditionalFormulaDataRecord(formula=get_active_events_2020)

REQUEST_CONTINUATION_MAPPING_2013 = {
    0x00: (EVENT_WINDOW_TIME_2013,),
    0x01: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x02: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_02,
           SERVICE_TO_RESPOND),
    0x03: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_03_2013,
           SERVICE_TO_RESPOND),
    0x04: (EVENT_WINDOW_TIME_2013,),
    0x05: (EVENT_WINDOW_TIME_2013,),
    0x06: (EVENT_WINDOW_TIME_2013,),
    0x07: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_07_2013,
           SERVICE_TO_RESPOND),
}
REQUEST_CONTINUATION_MAPPING_2020 = {
    0x00: (EVENT_WINDOW_TIME_2020,),
    0x01: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x03: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_03_2020,
           SERVICE_TO_RESPOND),
    0x04: (EVENT_WINDOW_TIME_2020,),
    0x05: (EVENT_WINDOW_TIME_2020,),
    0x06: (EVENT_WINDOW_TIME_2020,),
    0x07: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_07_2020,
           SERVICE_TO_RESPOND),
    0x08: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_08_2020,
           SERVICE_TO_RESPOND),
    0x09: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_09_2020, CONDITIONAL_EVENT_TYPE_RECORD_09,
           SERVICE_TO_RESPOND),
}

RESPONSE_CONTINUATION_MAPPING_2013 = {
    0x00: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013),
    0x01: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x02: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_02,
           SERVICE_TO_RESPOND),
    0x03: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_03_2013,
           SERVICE_TO_RESPOND),
    0x04: (NUMBER_OF_IDENTIFIED_EVENTS, CONDITIONAL_ACTIVATED_EVENTS_2013),
    0x05: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013),
    0x06: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013),
    0x07: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_07_2013,
           SERVICE_TO_RESPOND),
}
RESPONSE_CONTINUATION_MAPPING_2020 = {
    0x00: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020),
    0x01: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x03: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_03_2020,
           SERVICE_TO_RESPOND),
    0x04: (NUMBER_OF_IDENTIFIED_EVENTS, CONDITIONAL_ACTIVATED_EVENTS_2020),
    0x05: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020),
    0x06: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020),
    0x07: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_07_2020,
           SERVICE_TO_RESPOND),
    0x08: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_08_2020,
           SERVICE_TO_RESPOND),
    0x09: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_09_2020, CONDITIONAL_EVENT_TYPE_RECORD_09,
           SERVICE_TO_RESPOND),
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

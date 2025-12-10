"""Translation for AccessTimingParameter (SID 0x83) service."""

__all__ = ["ACCESS_TIMING_PARAMETER_2013"]

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import (
    ACCESS_TIMING_PARAMETER_SUB_FUNCTION,
    TIMING_PARAMETER_REQUEST_RECORD,
    TIMING_PARAMETER_RESPONSE_RECORD,
)
from ..service import Service

REQUEST_CONTINUATION_MAPPING_2013 = {
    0x01: (),
    0x02: (),
    0x03: (),
    0x04: (TIMING_PARAMETER_REQUEST_RECORD,),
}

RESPONSE_CONTINUATION_MAPPING_2013 = {
    0x01: (TIMING_PARAMETER_RESPONSE_RECORD,),
    0x02: (),
    0x03: (TIMING_PARAMETER_RESPONSE_RECORD,),
    0x04: (),
}

CONDITIONAL_REQUEST_CONTINUATION_2013 = ConditionalMappingDataRecord(mapping=REQUEST_CONTINUATION_MAPPING_2013,
                                                                     value_mask=0x7F)

CONDITIONAL_RESPONSE_CONTINUATION_2013 = ConditionalMappingDataRecord(mapping=RESPONSE_CONTINUATION_MAPPING_2013,
                                                                      value_mask=0x7F)

ACCESS_TIMING_PARAMETER_2013 = Service(request_sid=RequestSID.AccessTimingParameter,
                                       request_structure=(ACCESS_TIMING_PARAMETER_SUB_FUNCTION,
                                                          CONDITIONAL_REQUEST_CONTINUATION_2013),
                                       response_structure=(ACCESS_TIMING_PARAMETER_SUB_FUNCTION,
                                                           CONDITIONAL_RESPONSE_CONTINUATION_2013))
"""Translator for :ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` service
compatible with ISO 14229-1:2013."""

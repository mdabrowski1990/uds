"""Translation for RoutineControl (SID 0x31) service."""

__all__ = ["ROUTINE_CONTROL"]

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import (
    OPTIONAL_ROUTINE_STATUS,
    RID,
    ROUTINE_CONTROL_OPTION,
    ROUTINE_CONTROL_SUB_FUNCTION,
    ROUTINE_STATUS,
)
from ..service import Service

RESPONSE_CONTINUATION_MAPPING = {
    0x01: (RID, OPTIONAL_ROUTINE_STATUS),
    0x02: (RID, OPTIONAL_ROUTINE_STATUS),
    0x03: (RID, ROUTINE_STATUS),
}

CONDITIONAL_RESPONSE_CONTINUATION = ConditionalMappingDataRecord(
    mapping=RESPONSE_CONTINUATION_MAPPING | {key + 0x80: value
                                             for key, value in RESPONSE_CONTINUATION_MAPPING.items()})

ROUTINE_CONTROL = Service(request_sid=RequestSID.RoutineControl,
                          request_structure=(ROUTINE_CONTROL_SUB_FUNCTION,
                                             RID,
                                             ROUTINE_CONTROL_OPTION),
                          response_structure=(ROUTINE_CONTROL_SUB_FUNCTION,
                                              CONDITIONAL_RESPONSE_CONTINUATION))
"""Default translator for :ref:`RoutineControl <knowledge-base-service-routine-control>` service."""

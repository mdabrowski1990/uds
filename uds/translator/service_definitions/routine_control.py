"""Translation for :ref:`RoutineControl (SID 0x31) <knowledge-base-service-routine-control>` service."""

__all__ = ["ROUTINE_CONTROL"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_ROUTINE_CONTROL_RESPONSE,
    RID,
    ROUTINE_CONTROL_OPTION,
    ROUTINE_CONTROL_SUB_FUNCTION,
)
from ..service import Service

ROUTINE_CONTROL = Service(request_sid=RequestSID.RoutineControl,
                          request_structure=(ROUTINE_CONTROL_SUB_FUNCTION,
                                             RID,
                                             ROUTINE_CONTROL_OPTION),
                          response_structure=(ROUTINE_CONTROL_SUB_FUNCTION,
                                              CONDITIONAL_ROUTINE_CONTROL_RESPONSE))
"""Default translator for :ref:`RoutineControl <knowledge-base-service-routine-control>` service."""

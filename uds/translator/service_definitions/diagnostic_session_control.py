"""Translation for DiagnosticSessionControl (SID 0x10) service."""

__all__ = ["DIAGNOSTIC_SESSION_CONTROL"]

from uds.message import RequestSID
from uds.translator.data_record_definitions import DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION, SESSION_PARAMETER_RECORD
from uds.translator.service import Service

DIAGNOSTIC_SESSION_CONTROL = Service(request_sid=RequestSID.DiagnosticSessionControl,
                                     request_structure=[DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION],
                                     response_structure=[DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION,
                                                         SESSION_PARAMETER_RECORD])
"""Default translator for :ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` 
service."""

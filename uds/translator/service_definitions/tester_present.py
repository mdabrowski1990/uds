"""Translation for TesterPresent (SID 0x3E) service."""

__all__ = ["TESTER_PRESENT"]

from uds.message import RequestSID
from uds.translator.data_record_definitions import TESTER_PRESENT_SUB_FUNCTION
from uds.translator.service import Service

TESTER_PRESENT = Service(request_sid=RequestSID.TesterPresent,
                         request_structure=[TESTER_PRESENT_SUB_FUNCTION],
                         response_structure=[TESTER_PRESENT_SUB_FUNCTION])
"""Default translator for :ref:`TesterPresent <knowledge-base-service-tester-present>` service."""

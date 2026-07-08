""":ref:`TesterPresent (SID 0x3E) <knowledge-base-service-tester-present>` translation."""

__all__ = ["TESTER_PRESENT"]

from uds.message import RequestSID

from ..data_record_definitions import TESTER_PRESENT_SUBFUNCTION
from ..service import Service

TESTER_PRESENT = Service(request_sid=RequestSID.TesterPresent,
                         request_structure=[TESTER_PRESENT_SUBFUNCTION],
                         response_structure=[TESTER_PRESENT_SUBFUNCTION])
"""Default translator for :ref:`TesterPresent <knowledge-base-service-tester-present>` service."""

""":ref:`LinkControl (SID 0x87) <knowledge-base-service-link-control>` translation."""

__all__ = ["LINK_CONTROL"]

from uds.message import RequestSID

from ..data_record_definitions import CONDITIONAL_LINK_CONTROL_REQUEST, LINK_CONTROL_SUB_FUNCTION
from ..service import Service

LINK_CONTROL = Service(request_sid=RequestSID.LinkControl,
                       request_structure=(LINK_CONTROL_SUB_FUNCTION, CONDITIONAL_LINK_CONTROL_REQUEST),
                       response_structure=(LINK_CONTROL_SUB_FUNCTION,))
"""Default translator for :ref:`LinkControl <knowledge-base-service-link-control>` service."""

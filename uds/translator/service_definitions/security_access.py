"""Translation for SecurityAccess (SID 0x27) service."""

__all__ = ["SECURITY_ACCESS"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_SECURITY_ACCESS_REQUEST,
    CONDITIONAL_SECURITY_ACCESS_RESPONSE,
    SECURITY_ACCESS_SUB_FUNCTION,
)
from ..service import Service

SECURITY_ACCESS = Service(request_sid=RequestSID.SecurityAccess,
                          request_structure=(SECURITY_ACCESS_SUB_FUNCTION, CONDITIONAL_SECURITY_ACCESS_REQUEST),
                          response_structure=(SECURITY_ACCESS_SUB_FUNCTION, CONDITIONAL_SECURITY_ACCESS_RESPONSE))
"""Default translator for :ref:`SECURITY_ACCESS <knowledge-base-service-security-access>` service."""

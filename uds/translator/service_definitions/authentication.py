""":ref:`Authentication (SID 0x29) <knowledge-base-service-authentication>` translation."""

__all__ = ["AUTHENTICATION"]

from uds.message import RequestSID

from ..data_record_definitions import (
    AUTHENTICATION_SUB_FUNCTION,
    CONDITIONAL_AUTHENTICATION_REQUEST,
    CONDITIONAL_AUTHENTICATION_RESPONSE,
)
from ..service import Service

AUTHENTICATION = Service(request_sid=RequestSID.Authentication,
                         request_structure=(AUTHENTICATION_SUB_FUNCTION,
                                            CONDITIONAL_AUTHENTICATION_REQUEST),
                         response_structure=(AUTHENTICATION_SUB_FUNCTION,
                                             CONDITIONAL_AUTHENTICATION_RESPONSE))
"""Default translator for :ref:`Authentication <knowledge-base-service-authentication>` service."""

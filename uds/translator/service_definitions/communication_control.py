""":ref:`CommunicationControl (SID 0x28) <knowledge-base-service-communication-control>` translation."""

__all__ = ["COMMUNICATION_CONTROL"]

from uds.message import RequestSID

from ..data_record_definitions import COMMUNICATION_CONTROL_SUBFUNCTION, CONDITIONAL_COMMUNICATION_CONTROL_REQUEST
from ..service import Service

COMMUNICATION_CONTROL = Service(request_sid=RequestSID.CommunicationControl,
                                request_structure=(COMMUNICATION_CONTROL_SUBFUNCTION,
                                                   CONDITIONAL_COMMUNICATION_CONTROL_REQUEST),
                                response_structure=(COMMUNICATION_CONTROL_SUBFUNCTION,))
"""Default translator for :ref:`CommunicationControl <knowledge-base-service-communication-control>` service."""

"""Translation for RequestTransferExit (SID 0x3) service."""

__all__ = ["REQUEST_TRANSFER_EXIT"]

from uds.message import RequestSID

from ..data_record_definitions import TRANSFER_REQUEST_PARAMETER, TRANSFER_RESPONSE_PARAMETER
from ..service import Service

REQUEST_TRANSFER_EXIT = Service(request_sid=RequestSID.RequestTransferExit,
                                request_structure=(TRANSFER_REQUEST_PARAMETER,),
                                response_structure=(TRANSFER_RESPONSE_PARAMETER,))
"""Default translator for :ref:`RequestTransferExit <knowledge-base-service-request-transfer-exit>` service."""

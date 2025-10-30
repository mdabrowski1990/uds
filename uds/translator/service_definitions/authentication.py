"""Translation for Authentication (SID 0x29) service."""

__all__ = ["AUTHENTICATION"]

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import AUTHENTICATION_SUB_FUNCTION
from ..service import Service

REQUEST_CONTINUATION_MAPPING = {
    # TODO
}
RESPONSE_CONTINUATION_MAPPING = {
    # TODO
}

CONDITIONAL_REQUEST_CONTINUATION = ConditionalMappingDataRecord(
    mapping=REQUEST_CONTINUATION_MAPPING | {key + 0x80: value
                                            for key, value in REQUEST_CONTINUATION_MAPPING.items()})
CONDITIONAL_RESPONSE_CONTINUATION = ConditionalMappingDataRecord(
    mapping=RESPONSE_CONTINUATION_MAPPING | {key + 0x80: value
                                             for key, value in RESPONSE_CONTINUATION_MAPPING.items()})

AUTHENTICATION = Service(request_sid=RequestSID.CommunicationControl,
                         request_structure=(AUTHENTICATION_SUB_FUNCTION,
                                            CONDITIONAL_REQUEST_CONTINUATION),
                         response_structure=(AUTHENTICATION_SUB_FUNCTION,
                                             CONDITIONAL_RESPONSE_CONTINUATION))
"""Default translator for :ref:`Authentication <knowledge-base-service-authentication>` service."""

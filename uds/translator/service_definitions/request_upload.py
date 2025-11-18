"""Translation for RequestUpload (SID 0x35) service."""

__all__ = ["REQUEST_UPLOAD"]

from uds.message import RequestSID

from ..data_record_definitions import (
    ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
    CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH,
    CONDITIONAL_MEMORY_ADDRESS_AND_SIZE,
    DATA_FORMAT_IDENTIFIER,
    LENGTH_FORMAT_IDENTIFIER,
)
from ..service import Service

REQUEST_UPLOAD = Service(request_sid=RequestSID.RequestUpload,
                         request_structure=(DATA_FORMAT_IDENTIFIER,
                                            ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
                                            CONDITIONAL_MEMORY_ADDRESS_AND_SIZE),
                         response_structure=(LENGTH_FORMAT_IDENTIFIER,
                                             CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH))
"""Default translator for :ref:`RequestUpload <knowledge-base-service-request-upload>` service."""

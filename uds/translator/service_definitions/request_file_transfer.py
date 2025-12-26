"""Translation for :ref:`RequestFileTransfer (SID 0x38) <knowledge-base-service-request-file-transfer>` service."""

__all__ = ["REQUEST_FILE_TRANSFER", "REQUEST_FILE_TRANSFER_2020", "REQUEST_FILE_TRANSFER_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2013,
    CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2020,
    CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2013,
    CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2020,
    MODE_OF_OPERATION_2013,
    MODE_OF_OPERATION_2020,
)
from ..service import Service

REQUEST_FILE_TRANSFER_2020 = Service(request_sid=RequestSID.RequestFileTransfer,
                                     request_structure=(MODE_OF_OPERATION_2020,
                                                        CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2020),
                                     response_structure=(MODE_OF_OPERATION_2020,
                                                         CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2020))
"""Translator for :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` service
compatible with ISO 14229-1:2020."""

REQUEST_FILE_TRANSFER_2013 = Service(request_sid=RequestSID.RequestFileTransfer,
                                     request_structure=(MODE_OF_OPERATION_2013,
                                                        CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2013),
                                     response_structure=(MODE_OF_OPERATION_2013,
                                                         CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2013))
"""Translator for :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` service
compatible with ISO 14229-1:2013."""

REQUEST_FILE_TRANSFER = REQUEST_FILE_TRANSFER_2020
"""Default translator for :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` service."""

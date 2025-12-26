"""Translation for :ref:`TransferData (SID 0x36) <knowledge-base-service-transfer-data>` service."""

__all__ = ["TRANSFER_DATA"]

from uds.message import RequestSID

from ..data_record_definitions import BLOCK_SEQUENCE_COUNTER, TRANSFER_REQUEST_PARAMETER, TRANSFER_RESPONSE_PARAMETER
from ..service import Service

TRANSFER_DATA = Service(request_sid=RequestSID.TransferData,
                        request_structure=(BLOCK_SEQUENCE_COUNTER,
                                           TRANSFER_REQUEST_PARAMETER),
                        response_structure=(BLOCK_SEQUENCE_COUNTER,
                                            TRANSFER_RESPONSE_PARAMETER))
"""Default translator for :ref:`TransferData <knowledge-base-service-transfer-data>` service."""

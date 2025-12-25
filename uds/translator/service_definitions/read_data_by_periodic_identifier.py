"""Translation for ReadDataByPeriodicIdentifier (SID 0x2A) service."""

__all__ = ["READ_DATA_BY_PERIODIC_IDENTIFIER"]

from uds.message import RequestSID

from ..data_record_definitions import CONDITIONAL_PERIODIC_DID, DATA, OPTIONAL_PERIODIC_DID, TRANSMISSION_MODE
from ..service import Service

READ_DATA_BY_PERIODIC_IDENTIFIER = Service(request_sid=RequestSID.ReadDataByPeriodicIdentifier,
                                           request_structure=(TRANSMISSION_MODE,
                                                              CONDITIONAL_PERIODIC_DID),
                                           response_structure=(OPTIONAL_PERIODIC_DID, DATA))
"""Default translator for :ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>`
service."""

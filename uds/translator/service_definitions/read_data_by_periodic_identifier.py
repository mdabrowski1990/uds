"""Translation for ReadDataByPeriodicIdentifier (SID 0x2A) service."""

__all__ = []

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import DATA, MULTIPLE_PERIODIC_DID, OPTIONAL_PERIODIC_DID, TRANSMISSION_MODE
from ..service import Service

CONDITIONAL_PERIODIC_DIDS = ConditionalMappingDataRecord(mapping={
    0x01: (MULTIPLE_PERIODIC_DID,),
    0x02: (MULTIPLE_PERIODIC_DID,),
    0x03: (MULTIPLE_PERIODIC_DID,),
    0x04: (),
})

READ_DATA_BY_PERIODIC_IDENTIFIER = Service(request_sid=RequestSID.ReadDataByIdentifier,
                                           request_structure=(TRANSMISSION_MODE, CONDITIONAL_PERIODIC_DIDS),
                                           response_structure=(OPTIONAL_PERIODIC_DID, DATA))
"""Default translator for :ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>`
service."""

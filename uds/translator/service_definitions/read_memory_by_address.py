"""Translation for ReadMemoryByAddress (SID 0x23) service."""

__all__ = ["READ_MEMORY_BY_ADDRESS"]

from uds.message import RequestSID

from ..data_record_definitions import ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER, CONDITIONAL_MEMORY_ADDRESS_AND_SIZE, DATA
from ..service import Service

READ_MEMORY_BY_ADDRESS = Service(request_sid=RequestSID.ReadMemoryByAddress,
                                 request_structure=(ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
                                                    CONDITIONAL_MEMORY_ADDRESS_AND_SIZE),
                                 response_structure=(DATA,))
"""Default translator for :ref:`ReadMemoryByAddress <knowledge-base-service-read-memory-by-address>` service."""

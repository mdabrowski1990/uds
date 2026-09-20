""":ref:`WriteMemoryByAddress (SID 0x3D) <knowledge-base-service-write-memory-by-address>` translation."""

__all__ = ["WRITE_MEMORY_BY_ADDRESS"]

from uds.message import RequestSID

from ..data_record_definitions import (
    ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
    CONDITIONAL_DATA,
    CONDITIONAL_MEMORY_ADDRESS_AND_SIZE,
)
from ..service import Service

WRITE_MEMORY_BY_ADDRESS = Service(request_sid=RequestSID.WriteMemoryByAddress,
                                  request_structure=(ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
                                                     CONDITIONAL_MEMORY_ADDRESS_AND_SIZE,
                                                     CONDITIONAL_DATA),
                                  response_structure=(ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
                                                      CONDITIONAL_MEMORY_ADDRESS_AND_SIZE))
"""Default translator for :ref:`WriteMemoryByAddress <knowledge-base-service-write-memory-by-address>` service."""

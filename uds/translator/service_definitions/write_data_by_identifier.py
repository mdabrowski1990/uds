""":ref:`WriteDataByIdentifier (SID 0x2E) <knowledge-base-service-write-data-by-identifier>` translation."""

__all__ = ["WRITE_DATA_BY_IDENTIFIER", "WRITE_DATA_BY_IDENTIFIER_2020", "WRITE_DATA_BY_IDENTIFIER_2013"]

from uds.message import RequestSID

from ..data_record_definitions import DID_2013, DID_2020
from ..data_record_definitions.formula import get_did_data_2013, get_did_data_2020
from ..service import Service

WRITE_DATA_BY_IDENTIFIER_2020 = Service(request_sid=RequestSID.WriteDataByIdentifier,
                                        request_structure=(DID_2020, get_did_data_2020()),
                                        response_structure=(DID_2020,))
"""Translator for :ref:`WriteDataByIdentifier <knowledge-base-service-write-data-by-identifier>` service
compatible with ISO 14229-1:2020."""

WRITE_DATA_BY_IDENTIFIER_2013 = Service(request_sid=RequestSID.WriteDataByIdentifier,
                                        request_structure=(DID_2013, get_did_data_2013()),
                                        response_structure=(DID_2013,))
"""Translator for :ref:`WriteDataByIdentifier <knowledge-base-service-write-data-by-identifier>` service
compatible with ISO 14229-1:2013."""

WRITE_DATA_BY_IDENTIFIER = WRITE_DATA_BY_IDENTIFIER_2020
"""Default translator for :ref:`WriteDataByIdentifier <knowledge-base-service-write-data-by-identifier>` service."""

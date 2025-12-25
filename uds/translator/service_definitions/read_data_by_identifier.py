"""Translation for :ref:`ReadDataByIdentifier (SID 0x22) <knowledge-base-service-read-data-by-identifier>` service."""

__all__ = ["READ_DATA_BY_IDENTIFIER", "READ_DATA_BY_IDENTIFIER_2020", "READ_DATA_BY_IDENTIFIER_2013"]

from uds.message import RequestSID
from uds.utilities import REPEATED_DATA_RECORDS_NUMBER

from ..data_record_definitions import MULTIPLE_DID_2013, MULTIPLE_DID_2020
from ..data_record_definitions.formula import get_dids_2013, get_dids_2020
from ..service import Service

DIDS_2013 = (*get_dids_2013(did_count=1, record_number=None, optional=False),
             *get_dids_2013(did_count=REPEATED_DATA_RECORDS_NUMBER, record_number=None, optional=True)[2:])
DIDS_2020 = (*get_dids_2020(did_count=1, record_number=None, optional=False),
             *get_dids_2020(did_count=REPEATED_DATA_RECORDS_NUMBER, record_number=None, optional=True)[2:])

READ_DATA_BY_IDENTIFIER_2020 = Service(request_sid=RequestSID.ReadDataByIdentifier,
                                       request_structure=(MULTIPLE_DID_2020,),
                                       response_structure=DIDS_2020)
"""Translator for :ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` service
compatible with ISO 14229-1:2020."""

READ_DATA_BY_IDENTIFIER_2013 = Service(request_sid=RequestSID.ReadDataByIdentifier,
                                       request_structure=(MULTIPLE_DID_2013,),
                                       response_structure=DIDS_2013)
"""Translator for :ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` service
compatible with ISO 14229-1:2013."""

READ_DATA_BY_IDENTIFIER = READ_DATA_BY_IDENTIFIER_2020
"""Default translator for :ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` service."""

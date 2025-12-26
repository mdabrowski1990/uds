""":ref:`ReadScalingDataByIdentifier (SID 0x24) <knowledge-base-service-read-scaling-data-by-identifier>` translation."""  # pylint: disable=line-too-long

__all__ = ["READ_SCALING_DATA_BY_IDENTIFIER",
           "READ_SCALING_DATA_BY_IDENTIFIER_2020", "READ_SCALING_DATA_BY_IDENTIFIER_2013"]

from uds.message import RequestSID

from ..data_record_definitions import DID_2013, DID_2020, SCALING_DATA_RECORDS
from ..service import Service

READ_SCALING_DATA_BY_IDENTIFIER_2020 = Service(request_sid=RequestSID.ReadScalingDataByIdentifier,
                                               request_structure=(DID_2020,),
                                               response_structure=(DID_2020, *SCALING_DATA_RECORDS))
"""Translator for :ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` service
compatible with ISO 14229-1:2020."""

READ_SCALING_DATA_BY_IDENTIFIER_2013 = Service(request_sid=RequestSID.ReadScalingDataByIdentifier,
                                               request_structure=(DID_2013,),
                                               response_structure=(DID_2013, *SCALING_DATA_RECORDS))
"""Translator for :ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` service
compatible with ISO 14229-1:2013."""

READ_SCALING_DATA_BY_IDENTIFIER = READ_SCALING_DATA_BY_IDENTIFIER_2020
"""Default translator for :ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>`
service."""

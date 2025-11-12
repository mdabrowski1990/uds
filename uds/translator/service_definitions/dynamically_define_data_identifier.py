"""Translation for DynamicallyDefineDataIdentifier (SID 0x2C) service."""

__all__ = ["DYNAMICALLY_DEFINE_DATA_IDENTIFIER",
           "DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020", "DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013"]

from uds.message import RequestSID

from ..data_record import ConditionalMappingDataRecord
from ..data_record_definitions import (
    ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
    CONDITIONAL_DATA_FROM_MEMORY,
    DATA_FROM_DID_2013,
    DATA_FROM_DID_2020,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
    DYNAMICALLY_DEFINED_DID,
    OPTIONAL_DYNAMICALLY_DEFINED_DID,
)
from ..service import Service

REQUEST_CONTINUATION_MAPPING_2013 = {
    0x01: (DYNAMICALLY_DEFINED_DID, DATA_FROM_DID_2013,),
    0x02: (DYNAMICALLY_DEFINED_DID, ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER, CONDITIONAL_DATA_FROM_MEMORY,),
    0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID,),
}
REQUEST_CONTINUATION_MAPPING_2020 = {
    0x01: (DYNAMICALLY_DEFINED_DID, DATA_FROM_DID_2020,),
    0x02: (DYNAMICALLY_DEFINED_DID, ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER, CONDITIONAL_DATA_FROM_MEMORY,),
    0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID,),
}

RESPONSE_CONTINUATION_MAPPING = {
    0x01: (DYNAMICALLY_DEFINED_DID,),
    0x02: (DYNAMICALLY_DEFINED_DID,),
    0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID,),
}

CONDITIONAL_REQUEST_CONTINUATION_2013 = ConditionalMappingDataRecord(
    mapping=REQUEST_CONTINUATION_MAPPING_2013 | {key + 0x80: value
                                                 for key, value in REQUEST_CONTINUATION_MAPPING_2013.items()})
CONDITIONAL_REQUEST_CONTINUATION_2020 = ConditionalMappingDataRecord(
    mapping=REQUEST_CONTINUATION_MAPPING_2020 | {key + 0x80: value
                                                 for key, value in REQUEST_CONTINUATION_MAPPING_2020.items()})

CONDITIONAL_RESPONSE_CONTINUATION = ConditionalMappingDataRecord(
    mapping=RESPONSE_CONTINUATION_MAPPING | {key + 0x80: value
                                             for key, value in RESPONSE_CONTINUATION_MAPPING.items()})

DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013 = Service(request_sid=RequestSID.DynamicallyDefineDataIdentifier,
                                                  request_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                     CONDITIONAL_REQUEST_CONTINUATION_2013),
                                                  response_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                      CONDITIONAL_RESPONSE_CONTINUATION))
"""Translator for :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>`
service compatible with ISO 14229-1:2013."""

DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020 = Service(request_sid=RequestSID.DynamicallyDefineDataIdentifier,
                                                  request_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                     CONDITIONAL_REQUEST_CONTINUATION_2020),
                                                  response_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                      CONDITIONAL_RESPONSE_CONTINUATION))
"""Translator for :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>`
service compatible with ISO 14229-1:2020."""

DYNAMICALLY_DEFINE_DATA_IDENTIFIER = DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020
"""Default translator for
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` service."""

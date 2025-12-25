"""
Translation for
:ref:`DynamicallyDefineDataIdentifier (SID 0x2C) <knowledge-base-service-dynamically-define-data-identifier>` service.
"""

__all__ = ["DYNAMICALLY_DEFINE_DATA_IDENTIFIER",
           "DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020", "DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2013,
    CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2020,
    CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2013,
    CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2020,
    DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
)
from ..service import Service

DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020 = Service(request_sid=RequestSID.DynamicallyDefineDataIdentifier,
                                                  request_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                     CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2020),
                                                  response_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                      CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2020))
"""Translator for :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>`
service compatible with ISO 14229-1:2020."""

DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2013 = Service(request_sid=RequestSID.DynamicallyDefineDataIdentifier,
                                                  request_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                     CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2013),
                                                  response_structure=(DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION,
                                                                      CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2013))
"""Translator for :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>`
service compatible with ISO 14229-1:2013."""

DYNAMICALLY_DEFINE_DATA_IDENTIFIER = DYNAMICALLY_DEFINE_DATA_IDENTIFIER_2020
"""Default translator for
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` service."""

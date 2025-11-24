"""Translation for SecuredDataTransmission (SID 0x84) service."""

__all__ = ["SECURED_DATA_TRANSMISSION", "SECURED_DATA_TRANSMISSION_2020", "SECURED_DATA_TRANSMISSION_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    ADMINISTRATIVE_PARAMETER,
    CONDITIONAL_SECURED_DATA_TRANSMISSION_REQUEST,
    CONDITIONAL_SECURED_DATA_TRANSMISSION_RESPONSE,
    SECURITY_DATA_REQUEST_RECORD,
    SECURITY_DATA_RESPONSE_RECORD,
    SIGNATURE_ENCRYPTION_CALCULATION,
    SIGNATURE_LENGTH,
)
from ..service import Service

SECURED_DATA_TRANSMISSION_2013 = Service(request_sid=RequestSID.SecuredDataTransmission,
                                         request_structure=(SECURITY_DATA_REQUEST_RECORD,),
                                         response_structure=(SECURITY_DATA_RESPONSE_RECORD,))
"""Translator for :ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>` service
compatible with ISO 14229-1:2013."""

SECURED_DATA_TRANSMISSION_2020 = Service(request_sid=RequestSID.SecuredDataTransmission,
                                         request_structure=(ADMINISTRATIVE_PARAMETER,
                                                            SIGNATURE_ENCRYPTION_CALCULATION,
                                                            SIGNATURE_LENGTH,
                                                            CONDITIONAL_SECURED_DATA_TRANSMISSION_REQUEST),
                                         response_structure=(ADMINISTRATIVE_PARAMETER,
                                                             SIGNATURE_ENCRYPTION_CALCULATION,
                                                             SIGNATURE_LENGTH,
                                                             CONDITIONAL_SECURED_DATA_TRANSMISSION_RESPONSE))
"""Translator for :ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>` service
compatible with ISO 14229-1:2020."""

SECURED_DATA_TRANSMISSION = SECURED_DATA_TRANSMISSION_2020
"""Default translator for :ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>`
service."""

""":ref:`InputOutputControlByIdentifier (SID 0x2F) <knowledge-base-service-input-output-control-by-identifier>` translation."""  # pylint: disable=line-too-long

__all__ = ["INPUT_OUTPUT_CONTROL_BY_IDENTIFIER",
           "INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020",
           "INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013"]

from uds.message import RequestSID

from ..data_record_definitions import (
    CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2013,
    CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2020,
    CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2013,
    CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2020,
    DID_2013,
    DID_2020,
)
from ..service import Service

INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020 = Service(
    request_sid=RequestSID.InputOutputControlByIdentifier,
    request_structure=(DID_2020,
                       CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2020),
    response_structure=(DID_2020,
                        CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2020))
"""Translator for :ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>`
service compatible with ISO 14229-1:2020."""

INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013 = Service(
    request_sid=RequestSID.InputOutputControlByIdentifier,
    request_structure=(DID_2013,
                       CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2013),
    response_structure=(DID_2013,
                        CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2013))
"""Translator for :ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>`
service compatible with ISO 14229-1:2013."""

INPUT_OUTPUT_CONTROL_BY_IDENTIFIER = INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020
"""Default translator for
:ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` service."""

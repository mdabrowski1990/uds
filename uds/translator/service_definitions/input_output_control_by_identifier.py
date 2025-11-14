"""Translation for InputOutputControlByIdentifier (SID 0x2E) service."""

__all__ = ["INPUT_OUTPUT_CONTROL_BY_IDENTIFIER",
           "INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020",
           "INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013"]

from uds.message import RequestSID

from ..data_record import AliasMessageStructure, ConditionalFormulaDataRecord, ConditionalMappingDataRecord
from ..data_record_definitions import (
    DID_2013,
    DID_2020,
    INPUT_OUTPUT_CONTROL_PARAMETER,
    get_did_data_2013,
    get_did_data_2020,
    get_did_data_mask_2013,
    get_did_data_mask_2020,
)
from ..service import Service

CONDITIONAL_CONTROL_STATE_2013 = get_did_data_2013(name="controlState")
CONDITIONAL_CONTROL_STATE_2020 = get_did_data_2020(name="controlState")

CONDITIONAL_CONTROL_ENABLE_MASK_2013 = get_did_data_mask_2013(name="controlEnableMask", optional=True)
CONDITIONAL_CONTROL_ENABLE_MASK_2020 = get_did_data_mask_2020(name="controlEnableMask", optional=True)


def get_request_continuation_2013(did: int) -> AliasMessageStructure:
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: (),
                0x01: (),
                0x02: (*CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did),
                       *CONDITIONAL_CONTROL_ENABLE_MASK_2013.get_message_continuation(did)),
                0x03: (),
            }))


def get_request_continuation_2020(did: int) -> AliasMessageStructure:
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: (),
                0x01: (),
                0x02: (*CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did),
                       *CONDITIONAL_CONTROL_ENABLE_MASK_2020.get_message_continuation(did)),
                0x03: (),
            }))


def get_response_continuation_2013(did: int) -> AliasMessageStructure:
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did),
                0x01: CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did),
                0x02: CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did),
                0x03: CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did),
            }))


def get_response_continuation_2020(did: int) -> AliasMessageStructure:
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did),
                0x01: CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did),
                0x02: CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did),
                0x03: CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did),
            }))


CONDITIONAL_REQUEST_CONTINUATION_2013 = ConditionalFormulaDataRecord(formula=get_request_continuation_2013)
CONDITIONAL_REQUEST_CONTINUATION_2020 = ConditionalFormulaDataRecord(formula=get_request_continuation_2020)

CONDITIONAL_RESPONSE_CONTINUATION_2013 = ConditionalFormulaDataRecord(formula=get_response_continuation_2013)
CONDITIONAL_RESPONSE_CONTINUATION_2020 = ConditionalFormulaDataRecord(formula=get_response_continuation_2020)

INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2013 = Service(request_sid=RequestSID.InputOutputControlByIdentifier,
                                                  request_structure=(DID_2013,
                                                                     CONDITIONAL_REQUEST_CONTINUATION_2013),
                                                  response_structure=(DID_2013,
                                                                      CONDITIONAL_RESPONSE_CONTINUATION_2013))
"""Translator for :ref:`InputOutputControlByIdentifier <knowledge-base-service-write-data-by-identifier>` service
compatible with ISO 14229-1:2013."""

INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020 = Service(request_sid=RequestSID.InputOutputControlByIdentifier,
                                                  request_structure=(DID_2020,
                                                                     CONDITIONAL_REQUEST_CONTINUATION_2020),
                                                  response_structure=(DID_2020,
                                                                      CONDITIONAL_RESPONSE_CONTINUATION_2020))
"""Translator for :ref:`InputOutputControlByIdentifier <knowledge-base-service-write-data-by-identifier>` service
compatible with ISO 14229-1:2020."""

INPUT_OUTPUT_CONTROL_BY_IDENTIFIER = INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_2020
"""Default translator for :ref:`InputOutputControlByIdentifier <knowledge-base-service-write-data-by-identifier>`
service."""

"""Definitions for Conditional Data Records."""  # pylint: disable=too-many-lines

__all__ = [
    # Shared
    "CONDITIONAL_MEMORY_ADDRESS_AND_SIZE",
    "CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH",
    # SID 0x11
    "CONDITIONAL_POWER_DOWN_TIME",
    # SID 0x19
    "CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2020", "CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2013",
    "CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2020", "CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2013",
    # SID 0x24
    "SCALING_DATA_RECORDS",
    # SID 0x27
    "CONDITIONAL_SECURITY_ACCESS_REQUEST",
    "CONDITIONAL_SECURITY_ACCESS_RESPONSE",
    # SID 0x28
    "CONDITIONAL_COMMUNICATION_CONTROL_REQUEST",
    # SID 0x29
    "CONDITIONAL_CERTIFICATE_CLIENT",
    "CONDITIONAL_CERTIFICATE_SERVER",
    "CONDITIONAL_CERTIFICATE_DATA",
    "CONDITIONAL_CHALLENGE_CLIENT", "CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT",
    "CONDITIONAL_CHALLENGE_SERVER",
    "CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT",
    "CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER",
    "CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_CLIENT",
    "CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER",
    "CONDITIONAL_OPTIONAL_NEEDED_ADDITIONAL_PARAMETER",
    "CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER",
    "CONDITIONAL_OPTIONAL_SESSION_KEY_INFO",
    "CONDITIONAL_AUTHENTICATION_REQUEST",
    "CONDITIONAL_AUTHENTICATION_RESPONSE",
    # SID 0x2A
    "CONDITIONAL_PERIODIC_DID",
    # SID 0x2C
    "CONDITIONAL_DATA_FROM_MEMORY",
    "CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2020",
    "CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2013",
    "CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2020",
    "CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2013",
    # SID 0x2F
    "CONDITIONAL_CONTROL_STATE_2020", "CONDITIONAL_CONTROL_STATE_2013",
    "CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2020", "CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2013",
    "CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2020",
    "CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2013",
    "CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2020",
    "CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2013",
    # SID 0x31
    "CONDITIONAL_ROUTINE_CONTROL_RESPONSE",
    # SID 0x38
    "CONDITIONAL_FILE_AND_PATH_NAME",
    "CONDITIONAL_FILE_SIZES",
    "CONDITIONAL_FILE_SIZES_OR_DIR_INFO",
    "CONDITIONAL_DIR_INFO",
    "CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER",
    "CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2020", "CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2013",
    "CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2020", "CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2013",
    # SID 0x3D
    "CONDITIONAL_DATA",
    # SID 0x83
    "CONDITIONAL_ACCESS_TIMING_PARAMETER_REQUEST_2013",
    "CONDITIONAL_ACCESS_TIMING_PARAMETER_RESPONSE_2013",
    # SID 0x84
    "CONDITIONAL_SECURED_DATA_TRANSMISSION_REQUEST",
    "CONDITIONAL_SECURED_DATA_TRANSMISSION_RESPONSE",
    # SID 0x86
    "EVENT_WINDOW_TIME_2020", "EVENT_WINDOW_TIME_2013",
    "EVENT_TYPE_RECORD_01",
    "EVENT_TYPE_RECORD_02_2013",
    "EVENT_TYPE_RECORD_03_2020", "EVENT_TYPE_RECORD_03_2013",
    "EVENT_TYPE_RECORD_07_2020", "EVENT_TYPE_RECORD_07_2013",
    "EVENT_TYPE_RECORD_08_2020",
    "EVENT_TYPE_RECORD_09_2020", "CONDITIONAL_EVENT_TYPE_RECORD_09_2020",
    "SERVICE_TO_RESPOND",
    "CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2020", "CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2013",
    "CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2020", "CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2013",
    # SID 0x87
    "CONDITIONAL_LINK_CONTROL_REQUEST",
]

from uds.utilities import REPEATED_DATA_RECORDS_NUMBER

from ..data_record import (
    AliasMessageStructure,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    RawDataRecord,
)
from .did import (
    DATA_FROM_DID_2013,
    DATA_FROM_DID_2020,
    DYNAMICALLY_DEFINED_DID_2013,
    DYNAMICALLY_DEFINED_DID_2020,
    MULTIPLE_PERIODIC_DID,
    OPTIONAL_DYNAMICALLY_DEFINED_DID_2013,
    OPTIONAL_DYNAMICALLY_DEFINED_DID_2020,
    OPTIONAL_MULTIPLE_PERIODIC_DID,
)
from .dtc import (
    DTC,
    DTC_AND_STATUS,
    DTC_COUNT,
    DTC_EXTENDED_DATA_RECORD_NUMBER,
    DTC_EXTENDED_DATA_RECORDS_DATA_LIST,
    DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST,
    DTC_FORMAT_IDENTIFIER,
    DTC_FUNCTIONAL_GROUP_IDENTIFIER,
    DTC_READINESS_GROUP_IDENTIFIER,
    DTC_SEVERITY_AVAILABILITY_MASK,
    DTC_SEVERITY_MASK,
    DTC_SNAPSHOT_RECORD_NUMBER,
    DTC_STATUS_AVAILABILITY_MASK,
    DTC_STATUS_MASK,
    DTC_STORED_DATA_RECORD_NUMBER,
    DTC_STORED_DATA_RECORD_NUMBERS_LIST,
    DTCS_AND_STATUSES_LIST,
    MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTER,
    MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER,
    MULTIPLE_DTC_AND_STATUS,
    MULTIPLE_DTC_SEVERITY_DTC_AND_STATUS,
    MULTIPLE_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS,
    OPTIONAL_DTC_AND_STATUS,
    OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER,
    OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST,
    OPTIONAL_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS,
    OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
    OPTIONAL_DTCS_AND_STATUSES_LIST,
)
from .formula import (
    get_activated_events_2013,
    get_activated_events_2020,
    get_data,
    get_data_from_memory,
    get_did_data_2013,
    get_did_data_2020,
    get_did_data_mask_2013,
    get_did_data_mask_2020,
    get_did_records_formula_2013,
    get_did_records_formula_2020,
    get_dir_info,
    get_event_type_record_01,
    get_event_type_record_02_2013,
    get_event_type_record_03_2013,
    get_event_type_record_03_2020,
    get_event_type_record_07_2013,
    get_event_type_record_07_2020,
    get_event_type_record_08_2020,
    get_event_type_record_09_2020,
    get_event_type_record_09_2020_continuation,
    get_event_window_2013,
    get_event_window_2020,
    get_file_path_and_name,
    get_file_sizes,
    get_file_sizes_or_dir_info,
    get_max_number_of_block_length,
    get_max_number_of_block_length_file_transfer,
    get_memory_size_and_memory_address,
    get_raw_data_record_with_length_formula,
    get_scaling_byte_extension_formula,
    get_secured_data_transmission_request,
    get_secured_data_transmission_response,
    get_security_access_request,
    get_security_access_response,
    get_service_to_respond,
)
from .other import (
    ADDITIONAL_PARAMETER_LENGTH,
    ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER,
    ALGORITHM_INDICATOR,
    AUTHENTICATION_RETURN_PARAMETER,
    CERTIFICATE_CLIENT_LENGTH,
    CERTIFICATE_DATA_LENGTH,
    CERTIFICATE_EVALUATION,
    CERTIFICATE_SERVER_LENGTH,
    CHALLENGE_CLIENT_LENGTH,
    CHALLENGE_SERVER_LENGTH,
    COMMUNICATION_CONFIGURATION,
    COMMUNICATION_TYPE,
    DATA_FORMAT_IDENTIFIER,
    EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH,
    EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH,
    FILE_AND_PATH_NAME_LENGTH,
    FILE_POSITION,
    FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH,
    FILE_SIZE_PARAMETER_LENGTH,
    INPUT_OUTPUT_CONTROL_PARAMETER,
    LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER,
    LINK_CONTROL_MODE_IDENTIFIER,
    LINK_RECORD,
    MEMORY_SELECTION,
    NEEDED_ADDITIONAL_PARAMETER_LENGTH,
    NODE_IDENTIFICATION_NUMBER,
    NUMBER_OF_ACTIVATED_EVENTS,
    NUMBER_OF_IDENTIFIED_EVENTS,
    POWER_DOWN_TIME,
    PROOF_OF_OWNERSHIP_CLIENT_LENGTH,
    PROOF_OF_OWNERSHIP_SERVER_LENGTH,
    SCALING_BYTE_LENGTH,
    SCALING_BYTE_TYPE,
    SESSION_KEY_INFO_LENGTH,
    TIMING_PARAMETER_REQUEST_RECORD_2013,
    TIMING_PARAMETER_RESPONSE_RECORD_2013,
)
from .rid import OPTIONAL_ROUTINE_STATUS, RID, ROUTINE_STATUS

# Shared

CONDITIONAL_MEMORY_ADDRESS_AND_SIZE = ConditionalFormulaDataRecord(formula=get_memory_size_and_memory_address)
"""Definition of conditional `memoryAddress` and `memorySize` Data Records."""

CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH = ConditionalFormulaDataRecord(formula=get_max_number_of_block_length)
"""Definition of conditional `maxNumberOfBlockLength` Data Record."""

# SID 0x11

CONDITIONAL_POWER_DOWN_TIME = ConditionalMappingDataRecord(mapping={0x4: [POWER_DOWN_TIME]},
                                                           default_message_continuation=[],
                                                           value_mask=0x7F)
"""Definition of conditional `powerDownTime` Data Record."""

# SID 0x19

_DID_RECORDS_2020 = tuple(ConditionalFormulaDataRecord(formula=get_did_records_formula_2020(record_number + 1))
                          for record_number in range(REPEATED_DATA_RECORDS_NUMBER))
"""Collection of `DID` Data Records (compatible with ISO 14229-1:2020)."""
_DID_RECORDS_2013 = tuple(ConditionalFormulaDataRecord(formula=get_did_records_formula_2013(record_number + 1))
                          for record_number in range(REPEATED_DATA_RECORDS_NUMBER))
"""Collection of `DID` Data Records (compatible with ISO 14229-1:2013)."""

_DID_COUNT_RECORDS = tuple(RawDataRecord(name=f"DIDCount#{record_number + 1}",
                                         length=8,
                                         min_occurrences=1,
                                         max_occurrences=1,
                                         unit="DIDs")
                           for record_number in range(REPEATED_DATA_RECORDS_NUMBER))
"""Collection of `DIDCount` Data Records."""

_DTC_SNAPSHOT_RECORDS_2020 = tuple(item
                                   for snapshot_record in zip(OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
                                                              _DID_COUNT_RECORDS,
                                                              _DID_RECORDS_2020)
                                   for item in snapshot_record)
"""Collection of DTC Snapshot Data Records (compatible with ISO 14229-1:2020)."""
_DTC_SNAPSHOT_RECORDS_2013 = tuple(item
                                   for snapshot_record in zip(OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
                                                              _DID_COUNT_RECORDS,
                                                              _DID_RECORDS_2013)
                                   for item in snapshot_record)
"""Collection of DTC Snapshot Data Records (compatible with ISO 14229-1:2013)."""

_DTC_EXTENDED_DATA_RECORDS = tuple(item
                                   for data_records in zip(OPTIONAL_DTCS_AND_STATUSES_LIST,
                                                           DTC_EXTENDED_DATA_RECORDS_DATA_LIST)
                                   for item in data_records)
"""Collection of DTC Extended Data Records."""

_DTC_STORED_DATA_RECORDS_2020 = tuple(item
                                      for stored_data_record in zip(DTC_STORED_DATA_RECORD_NUMBERS_LIST,
                                                                    DTCS_AND_STATUSES_LIST,
                                                                    _DID_COUNT_RECORDS,
                                                                    _DID_RECORDS_2020)
                                      for item in stored_data_record)
"""Collection of DTC Stored Data Records (compatible with ISO 14229-1:2020)."""
_DTC_STORED_DATA_RECORDS_2013 = tuple(item
                                      for stored_data_record in zip(DTC_STORED_DATA_RECORD_NUMBERS_LIST,
                                                                    DTCS_AND_STATUSES_LIST,
                                                                    _DID_COUNT_RECORDS,
                                                                    _DID_RECORDS_2013)
                                      for item in stored_data_record)
"""Collection of DTC Stored Data Records (compatible with ISO 14229-1:2013)."""

CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2020 = ConditionalMappingDataRecord(mapping={
    0x01: (DTC_STATUS_MASK,),
    0x02: (DTC_STATUS_MASK,),
    0x03: (),
    0x04: (DTC, DTC_SNAPSHOT_RECORD_NUMBER),
    0x05: (DTC_STORED_DATA_RECORD_NUMBER,),
    0x06: (DTC, DTC_EXTENDED_DATA_RECORD_NUMBER),
    0x07: (DTC_SEVERITY_MASK, DTC_STATUS_MASK),
    0x08: (DTC_SEVERITY_MASK, DTC_STATUS_MASK),
    0x09: (DTC,),
    0x0A: (),
    0x0B: (),
    0x0C: (),
    0x0D: (),
    0x0E: (),
    0x14: (),
    0x15: (),
    0x16: (DTC_EXTENDED_DATA_RECORD_NUMBER,),
    0x17: (DTC_STATUS_MASK, MEMORY_SELECTION),
    0x18: (DTC, DTC_SNAPSHOT_RECORD_NUMBER, MEMORY_SELECTION),
    0x19: (DTC, DTC_EXTENDED_DATA_RECORD_NUMBER, MEMORY_SELECTION),
    0x1A: (DTC_EXTENDED_DATA_RECORD_NUMBER,),
    0x42: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_MASK, DTC_SEVERITY_MASK),
    0x55: (DTC_FUNCTIONAL_GROUP_IDENTIFIER,),
    0x56: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_READINESS_GROUP_IDENTIFIER),
},
    value_mask=0x7F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` request message."""

CONDITIONAL_READ_DTC_INFORMATION_REQUEST_2013 = ConditionalMappingDataRecord(mapping={
    0x01: (DTC_STATUS_MASK,),
    0x02: (DTC_STATUS_MASK,),
    0x03: (),
    0x04: (DTC, DTC_SNAPSHOT_RECORD_NUMBER),
    0x05: (DTC_STORED_DATA_RECORD_NUMBER,),
    0x06: (DTC, DTC_EXTENDED_DATA_RECORD_NUMBER),
    0x07: (DTC_SEVERITY_MASK, DTC_STATUS_MASK),
    0x08: (DTC_SEVERITY_MASK, DTC_STATUS_MASK),
    0x09: (DTC,),
    0x0A: (),
    0x0B: (),
    0x0C: (),
    0x0D: (),
    0x0E: (),
    0x0F: (DTC_STATUS_MASK,),
    0x10: (DTC, DTC_EXTENDED_DATA_RECORD_NUMBER),
    0x11: (DTC_STATUS_MASK,),
    0x12: (DTC_STATUS_MASK,),
    0x13: (DTC_STATUS_MASK,),
    0x14: (),
    0x15: (),
    0x16: (DTC_EXTENDED_DATA_RECORD_NUMBER,),
    0x17: (DTC_STATUS_MASK, MEMORY_SELECTION),
    0x18: (DTC, DTC_SNAPSHOT_RECORD_NUMBER, MEMORY_SELECTION),
    0x19: (DTC, DTC_EXTENDED_DATA_RECORD_NUMBER, MEMORY_SELECTION),
    0x42: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_MASK, DTC_SEVERITY_MASK),
    0x55: (DTC_FUNCTIONAL_GROUP_IDENTIFIER,),
},
    value_mask=0x7F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` request message."""

CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2020 = ConditionalMappingDataRecord(mapping={
    0x01: (DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER, DTC_COUNT),
    0x02: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x03: (MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER,),
    0x04: (DTC_AND_STATUS, *_DTC_SNAPSHOT_RECORDS_2020),
    0x05: _DTC_STORED_DATA_RECORDS_2020,
    0x06: (DTC_AND_STATUS, *DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST),
    0x07: (DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER, DTC_COUNT),
    0x08: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS),
    0x09: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS),
    0x0A: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x0B: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0C: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0D: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0E: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x14: (MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTER,),
    0x15: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x16: (DTC_EXTENDED_DATA_RECORD_NUMBER, *_DTC_EXTENDED_DATA_RECORDS),
    0x17: (MEMORY_SELECTION, DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x18: (MEMORY_SELECTION, DTC_AND_STATUS, *_DTC_SNAPSHOT_RECORDS_2020),
    0x19: (MEMORY_SELECTION, DTC_AND_STATUS, OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER,
           DTC_EXTENDED_DATA_RECORDS_DATA_LIST[0], *OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST[1:]),
    0x1A: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER, MULTIPLE_DTC_AND_STATUS),
    0x42: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_AVAILABILITY_MASK, DTC_SEVERITY_AVAILABILITY_MASK,
           DTC_FORMAT_IDENTIFIER, MULTIPLE_DTC_SEVERITY_DTC_AND_STATUS),
    0x55: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER,
           MULTIPLE_DTC_AND_STATUS),
    0x56: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER,
           DTC_READINESS_GROUP_IDENTIFIER, MULTIPLE_DTC_AND_STATUS)
},
    value_mask=0x7F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` response message."""

CONDITIONAL_READ_DTC_INFORMATION_RESPONSE_2013 = ConditionalMappingDataRecord(mapping={
    0x01: (DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER, DTC_COUNT),
    0x02: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x03: (MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER,),
    0x04: (DTC_AND_STATUS, *_DTC_SNAPSHOT_RECORDS_2013),
    0x05: _DTC_STORED_DATA_RECORDS_2013,
    0x06: (DTC_AND_STATUS, *DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST),
    0x07: (DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER, DTC_COUNT),
    0x08: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS),
    0x09: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS),
    0x0A: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x0B: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0C: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0D: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0E: (DTC_STATUS_AVAILABILITY_MASK, OPTIONAL_DTC_AND_STATUS),
    0x0F: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x10: (DTC_AND_STATUS, *DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST),
    0x11: (DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER, DTC_COUNT),
    0x12: (DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER, DTC_COUNT),
    0x13: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x14: (MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTER,),
    0x15: (DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x16: (DTC_EXTENDED_DATA_RECORD_NUMBER, *_DTC_EXTENDED_DATA_RECORDS),
    0x17: (MEMORY_SELECTION, DTC_STATUS_AVAILABILITY_MASK, MULTIPLE_DTC_AND_STATUS),
    0x18: (MEMORY_SELECTION, DTC_AND_STATUS, *_DTC_SNAPSHOT_RECORDS_2013),
    0x19: (MEMORY_SELECTION, DTC_AND_STATUS, OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER,
           DTC_EXTENDED_DATA_RECORDS_DATA_LIST[0], *OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST[1:]),
    0x42: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_AVAILABILITY_MASK, DTC_SEVERITY_AVAILABILITY_MASK,
           DTC_FORMAT_IDENTIFIER, MULTIPLE_DTC_SEVERITY_DTC_AND_STATUS),
    0x55: (DTC_FUNCTIONAL_GROUP_IDENTIFIER, DTC_STATUS_AVAILABILITY_MASK, DTC_FORMAT_IDENTIFIER,
           MULTIPLE_DTC_AND_STATUS),
},
    value_mask=0x7F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` response message."""

# SID 0x24

_SCALING_BYTES_RECORDS = tuple(RawDataRecord(name=f"scalingByte#{index}",
                                             children=(SCALING_BYTE_TYPE, SCALING_BYTE_LENGTH),
                                             length=8,
                                             min_occurrences=1 if index == 1 else 0,
                                             max_occurrences=1)
                               for index in range(1, REPEATED_DATA_RECORDS_NUMBER + 1))
"""Collection of `scalingByte` Data Records."""

_SCALING_BYTES_EXTENSIONS_RECORDS = tuple(
    ConditionalFormulaDataRecord(formula=get_scaling_byte_extension_formula(index))
    for index in range(1, REPEATED_DATA_RECORDS_NUMBER + 1))
"""Collection of `scalingByteExtension` Data Records."""

SCALING_DATA_RECORDS = tuple(item
                             for scaling_data_records in zip(_SCALING_BYTES_RECORDS, _SCALING_BYTES_EXTENSIONS_RECORDS)
                             for item in scaling_data_records)
"""Collection of `scalingByte` and `scalingByteExtension` Data Records."""

# SID 0x27

CONDITIONAL_SECURITY_ACCESS_REQUEST = ConditionalFormulaDataRecord(formula=get_security_access_request)
"""Definition of conditional continuation of
:ref:`SecurityAccess <knowledge-base-service-security-access>` request message."""

CONDITIONAL_SECURITY_ACCESS_RESPONSE = ConditionalFormulaDataRecord(formula=get_security_access_response)
"""Definition of conditional continuation of
:ref:`SecurityAccess <knowledge-base-service-security-access>` response message."""

# SID 0x28

CONDITIONAL_COMMUNICATION_CONTROL_REQUEST = ConditionalMappingDataRecord(
    value_mask=0x7F,
    default_message_continuation=(COMMUNICATION_TYPE,),
    mapping={
        0x04: (COMMUNICATION_TYPE, NODE_IDENTIFICATION_NUMBER),
        0x05: (COMMUNICATION_TYPE, NODE_IDENTIFICATION_NUMBER),
    })
"""Definition of conditional continuation of
:ref:`CommunicationControl <knowledge-base-service-communication-control>` request message."""

# SID 0x29

CONDITIONAL_CERTIFICATE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="certificateClient",
                                                    accept_zero_length=False))
"""Definition of conditional `certificateClient` Data Record."""

CONDITIONAL_CERTIFICATE_SERVER = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="certificateServer",
                                                    accept_zero_length=False))
"""Definition of conditional `certificateServer` Data Record."""

CONDITIONAL_CERTIFICATE_DATA = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="certificateData",
                                                    accept_zero_length=False))
"""Definition of conditional `certificateData` Data Record."""

CONDITIONAL_CHALLENGE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="challengeClient",
                                                    accept_zero_length=False))
"""Definition of conditional `challengeClient` Data Record."""
CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="challengeClient",
                                                    accept_zero_length=True))
"""Definition of optional conditional `challengeClient` Data Record."""

CONDITIONAL_CHALLENGE_SERVER = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="challengeServer",
                                                    accept_zero_length=False))
"""Definition of conditional `challengeServer` Data Record."""

CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="proofOfOwnershipClient",
                                                    accept_zero_length=False))
"""Definition of conditional `proofOfOwnershipClient` Data Record."""

CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="proofOfOwnershipServer",
                                                    accept_zero_length=False))
"""Definition of conditional `proofOfOwnershipServer` Data Record."""

CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_CLIENT = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="ephemeralPublicKeyClient",
                                                    accept_zero_length=True))
"""Definition of optional conditional `ephemeralPublicKeyClient` Data Record."""

CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="ephemeralPublicKeyServer",
                                                    accept_zero_length=True))
"""Definition of optional conditional `ephemeralPublicKeyServer` Data Record."""

CONDITIONAL_OPTIONAL_NEEDED_ADDITIONAL_PARAMETER = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="neededAdditionalParameter",
                                                    accept_zero_length=True))
"""Definition of optional conditional `neededAdditionalParameter` Data Record."""

CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="additionalParameter",
                                                    accept_zero_length=True))
"""Definition of optional conditional `additionalParameter` Data Record."""

CONDITIONAL_OPTIONAL_SESSION_KEY_INFO = ConditionalFormulaDataRecord(
    formula=get_raw_data_record_with_length_formula(data_record_name="sessionKeyInfo",
                                                    accept_zero_length=True))
"""Definition of optional conditional `sessionKeyInfo` Data Record."""

CONDITIONAL_AUTHENTICATION_REQUEST = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x00: (),
        0x01: (COMMUNICATION_CONFIGURATION,
               CERTIFICATE_CLIENT_LENGTH, CONDITIONAL_CERTIFICATE_CLIENT,
               CHALLENGE_CLIENT_LENGTH, CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT),
        0x02: (COMMUNICATION_CONFIGURATION,
               CERTIFICATE_CLIENT_LENGTH, CONDITIONAL_CERTIFICATE_CLIENT,
               CHALLENGE_CLIENT_LENGTH, CONDITIONAL_CHALLENGE_CLIENT),
        0x03: (PROOF_OF_OWNERSHIP_CLIENT_LENGTH, CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT,
               EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH, CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_CLIENT),
        0x04: (CERTIFICATE_EVALUATION,
               CERTIFICATE_DATA_LENGTH, CONDITIONAL_CERTIFICATE_DATA),
        0x05: (COMMUNICATION_CONFIGURATION, ALGORITHM_INDICATOR),
        0x06: (ALGORITHM_INDICATOR,
               PROOF_OF_OWNERSHIP_CLIENT_LENGTH, CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT,
               CHALLENGE_CLIENT_LENGTH, CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT,
               ADDITIONAL_PARAMETER_LENGTH, CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER),
        0x07: (ALGORITHM_INDICATOR,
               PROOF_OF_OWNERSHIP_CLIENT_LENGTH, CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT,
               CHALLENGE_CLIENT_LENGTH, CONDITIONAL_CHALLENGE_CLIENT,
               ADDITIONAL_PARAMETER_LENGTH, CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER),
        0x08: (),
    })
"""Definition of conditional continuation of
:ref:`Authentication <knowledge-base-service-authentication>` request message."""

CONDITIONAL_AUTHENTICATION_RESPONSE = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x00: (AUTHENTICATION_RETURN_PARAMETER,),
        0x01: (AUTHENTICATION_RETURN_PARAMETER,
               CHALLENGE_SERVER_LENGTH, CONDITIONAL_CHALLENGE_SERVER,
               EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH, CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER),
        0x02: (AUTHENTICATION_RETURN_PARAMETER,
               CHALLENGE_SERVER_LENGTH, CONDITIONAL_CHALLENGE_SERVER,
               CERTIFICATE_SERVER_LENGTH, CONDITIONAL_CERTIFICATE_SERVER,
               PROOF_OF_OWNERSHIP_SERVER_LENGTH, CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER,
               EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH, CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER),
        0x03: (AUTHENTICATION_RETURN_PARAMETER,
               SESSION_KEY_INFO_LENGTH, CONDITIONAL_OPTIONAL_SESSION_KEY_INFO),
        0x04: (AUTHENTICATION_RETURN_PARAMETER,),
        0x05: (AUTHENTICATION_RETURN_PARAMETER, ALGORITHM_INDICATOR,
               CHALLENGE_SERVER_LENGTH, CONDITIONAL_CHALLENGE_SERVER,
               NEEDED_ADDITIONAL_PARAMETER_LENGTH, CONDITIONAL_OPTIONAL_NEEDED_ADDITIONAL_PARAMETER),
        0x06: (AUTHENTICATION_RETURN_PARAMETER, ALGORITHM_INDICATOR,
               SESSION_KEY_INFO_LENGTH, CONDITIONAL_OPTIONAL_SESSION_KEY_INFO),
        0x07: (AUTHENTICATION_RETURN_PARAMETER, ALGORITHM_INDICATOR,
               PROOF_OF_OWNERSHIP_SERVER_LENGTH, CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER,
               SESSION_KEY_INFO_LENGTH, CONDITIONAL_OPTIONAL_SESSION_KEY_INFO),
        0x08: (AUTHENTICATION_RETURN_PARAMETER,),
    })
"""Definition of conditional continuation of
:ref:`Authentication <knowledge-base-service-authentication>` response message."""

# SID 0x2A

CONDITIONAL_PERIODIC_DID = ConditionalMappingDataRecord(mapping={
    0x01: (MULTIPLE_PERIODIC_DID,),
    0x02: (MULTIPLE_PERIODIC_DID,),
    0x03: (MULTIPLE_PERIODIC_DID,),
    0x04: (OPTIONAL_MULTIPLE_PERIODIC_DID,),
})
"""Definition of conditional `Periodic DID` Data Record."""

# SID 0x2C

CONDITIONAL_DATA_FROM_MEMORY = ConditionalFormulaDataRecord(formula=get_data_from_memory)
"""Definition of conditional `Data from Memory` Data Record."""

CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2020 = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x01: (DYNAMICALLY_DEFINED_DID_2020, DATA_FROM_DID_2020,),
        0x02: (DYNAMICALLY_DEFINED_DID_2020, ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER, CONDITIONAL_DATA_FROM_MEMORY,),
        0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID_2020,),
    })
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` request message."""

CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_REQUEST_2013 = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x01: (DYNAMICALLY_DEFINED_DID_2013, DATA_FROM_DID_2013,),
        0x02: (DYNAMICALLY_DEFINED_DID_2013, ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER, CONDITIONAL_DATA_FROM_MEMORY,),
        0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID_2013,),
    })
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` request message."""

CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2020 = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x01: (DYNAMICALLY_DEFINED_DID_2020,),
        0x02: (DYNAMICALLY_DEFINED_DID_2020,),
        0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID_2020,),
    })
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` response message."""

CONDITIONAL_DYNAMICALLY_DEFINE_DATA_IDENTIFIER_RESPONSE_2013 = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x01: (DYNAMICALLY_DEFINED_DID_2013,),
        0x02: (DYNAMICALLY_DEFINED_DID_2013,),
        0x03: (OPTIONAL_DYNAMICALLY_DEFINED_DID_2013,),
    })
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` response message."""

# SID 0x2F

CONDITIONAL_CONTROL_STATE_2020 = get_did_data_2020(name="controlState")
"""Definition of conditional (compatible with ISO 14229-1:2020) `controlState` Data Record."""
CONDITIONAL_CONTROL_STATE_2013 = get_did_data_2013(name="controlState")
"""Definition of conditional (compatible with ISO 14229-1:2013) `controlState` Data Record."""

CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2020 = get_did_data_mask_2020(name="controlEnableMask", optional=True)
"""Definition of optional conditional (compatible with ISO 14229-1:2020) `controlEnableMask` Data Record."""
CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2013 = get_did_data_mask_2013(name="controlEnableMask", optional=True)
"""Definition of optional conditional (compatible with ISO 14229-1:2013) `controlEnableMask` Data Record."""


def get_input_output_control_by_identifier_request_2020(did: int) -> AliasMessageStructure:
    """
    Get message continuation (after DID Data Record) for InputOutputControlByIdentifier request.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param did: Value of proceeding DID.

    :return: Following Data Records that are consistent with ISO 14229-1:2020.
    """
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: (),
                0x01: (),
                0x02: (),
                0x03: (*CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did),
                       *CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2020.get_message_continuation(did)),
            }))


def get_input_output_control_by_identifier_request_2013(did: int) -> AliasMessageStructure:
    """
    Get continuation (after DID Data Record) of InputOutputControlByIdentifier request message.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param did: Value of proceeding DID.

    :return: Following Data Records that are consistent with ISO 14229-1:2013.
    """
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: (),
                0x01: (),
                0x02: (),
                0x03: (*CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did),
                       *CONDITIONAL_OPTIONAL_CONTROL_ENABLE_MASK_2013.get_message_continuation(did)),
            }))


def get_input_output_control_by_identifier_response_2020(did: int) -> AliasMessageStructure:
    """
    Get message continuation (after DID Data Record) for InputOutputControlByIdentifier positive response.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param did: Value of proceeding DID.

    :return: Following Data Records that are consistent with ISO 14229-1:2020.
    """
    control_state_data_records_2020 = CONDITIONAL_CONTROL_STATE_2020.get_message_continuation(did)
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: control_state_data_records_2020,
                0x01: control_state_data_records_2020,
                0x02: control_state_data_records_2020,
                0x03: control_state_data_records_2020,
            }))


def get_input_output_control_by_identifier_response_2013(did: int) -> AliasMessageStructure:
    """
    Get message continuation (after DID Data Record) for InputOutputControlByIdentifier positive response.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param did: Value of proceeding DID.

    :return: Following Data Records that are consistent with ISO 14229-1:2013.
    """
    control_state_data_records_2013 = CONDITIONAL_CONTROL_STATE_2013.get_message_continuation(did)
    return (INPUT_OUTPUT_CONTROL_PARAMETER,
            ConditionalMappingDataRecord(mapping={
                0x00: control_state_data_records_2013,
                0x01: control_state_data_records_2013,
                0x02: control_state_data_records_2013,
                0x03: control_state_data_records_2013,
            }))


CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2020 = ConditionalFormulaDataRecord(
    formula=get_input_output_control_by_identifier_request_2020)
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` request message."""
CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_REQUEST_2013 = ConditionalFormulaDataRecord(
    formula=get_input_output_control_by_identifier_request_2013)
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` request message."""

CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2020 = ConditionalFormulaDataRecord(
    formula=get_input_output_control_by_identifier_response_2020)
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` response message."""
CONDITIONAL_INPUT_OUTPUT_CONTROL_BY_IDENTIFIER_RESPONSE_2013 = ConditionalFormulaDataRecord(
    formula=get_input_output_control_by_identifier_response_2013)
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` response message."""

# SID 0x31

CONDITIONAL_ROUTINE_CONTROL_RESPONSE = ConditionalMappingDataRecord(mapping={
    0x01: (RID, OPTIONAL_ROUTINE_STATUS),
    0x02: (RID, OPTIONAL_ROUTINE_STATUS),
    0x03: (RID, ROUTINE_STATUS),
},
    value_mask=0x7F)
"""Definition of conditional continuation of
:ref:`RoutineControl <knowledge-base-service-routine-control>` response message."""

# SID 0x38

CONDITIONAL_FILE_AND_PATH_NAME = ConditionalFormulaDataRecord(formula=get_file_path_and_name)
"""Definition of conditional `filePathAndName` Data Record."""

CONDITIONAL_FILE_SIZES = ConditionalFormulaDataRecord(formula=get_file_sizes)
"""Definition of conditional `fileSizeUnCompressed` and `fileSizeCompressed` Data Records."""

CONDITIONAL_FILE_SIZES_OR_DIR_INFO = ConditionalFormulaDataRecord(formula=get_file_sizes_or_dir_info)
"""Definition of conditional `fileSizeUncompressedOrDirInfoLength` and `fileSizeCompressed` Data Records."""

CONDITIONAL_DIR_INFO = ConditionalFormulaDataRecord(formula=get_dir_info)
"""Definition of conditional `fileSizeUncompressedOrDirInfoLength` Data Record."""

CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER = ConditionalFormulaDataRecord(
    formula=get_max_number_of_block_length_file_transfer)
"""Definition of conditional `maxNumberOfBlockLength` Data Record that is part of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` message."""

CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2020 = ConditionalMappingDataRecord(mapping={
    0x01: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES),
    0x02: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME),
    0x03: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES),
    0x04: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER),
    0x05: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME),
    0x06: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES),
})
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` request message."""

CONDITIONAL_REQUEST_FILE_TRANSFER_REQUEST_2013 = ConditionalMappingDataRecord(mapping={
    0x01: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES),
    0x02: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME),
    0x03: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES),
    0x04: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME,
           DATA_FORMAT_IDENTIFIER),
    0x05: (FILE_AND_PATH_NAME_LENGTH, CONDITIONAL_FILE_AND_PATH_NAME),
})
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` request message."""

CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2020 = ConditionalMappingDataRecord(mapping={
    0x01: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER),
    0x02: (),
    0x03: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER),
    0x04: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES_OR_DIR_INFO),
    0x05: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH, CONDITIONAL_DIR_INFO),
    0x06: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER,
           FILE_POSITION),
})
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` response message."""

CONDITIONAL_REQUEST_FILE_TRANSFER_RESPONSE_2013 = ConditionalMappingDataRecord(mapping={
    0x01: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER),
    0x02: (),
    0x03: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER),
    0x04: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH, CONDITIONAL_FILE_SIZES_OR_DIR_INFO),
    0x05: (LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER, CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER,
           DATA_FORMAT_IDENTIFIER,
           FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH, CONDITIONAL_DIR_INFO),
})
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` response message."""

# SID 0x3D

CONDITIONAL_DATA = ConditionalFormulaDataRecord(formula=get_data)
"""Definition of conditional `data` Data Record."""

# SID 0x83

CONDITIONAL_ACCESS_TIMING_PARAMETER_REQUEST_2013 = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x01: (),
        0x02: (),
        0x03: (),
        0x04: (TIMING_PARAMETER_REQUEST_RECORD_2013,),
    })
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` request message."""

CONDITIONAL_ACCESS_TIMING_PARAMETER_RESPONSE_2013 = ConditionalMappingDataRecord(
    value_mask=0x7F,
    mapping={
        0x01: (TIMING_PARAMETER_RESPONSE_RECORD_2013,),
        0x02: (),
        0x03: (TIMING_PARAMETER_RESPONSE_RECORD_2013,),
        0x04: (),
    })
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` response message."""

# SID 0x84

CONDITIONAL_SECURED_DATA_TRANSMISSION_REQUEST = ConditionalFormulaDataRecord(
    formula=get_secured_data_transmission_request)
"""Definition of conditional continuation of
:ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>`request message."""

CONDITIONAL_SECURED_DATA_TRANSMISSION_RESPONSE = ConditionalFormulaDataRecord(
    formula=get_secured_data_transmission_response)
"""Definition of conditional continuation of
:ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>` response message."""

# SID 0x86

EVENT_WINDOW_TIME_2020 = get_event_window_2020()
"""Definition of `eventWindowTime` Data Record (compatible with ISO 14229-1:2020)."""
EVENT_WINDOW_TIME_2013 = get_event_window_2013()
"""Definition of `eventWindowTime` Data Record (compatible with ISO 14229-1:2013)."""

CONDITIONAL_ACTIVATED_EVENTS_2020 = ConditionalFormulaDataRecord(formula=get_activated_events_2020)
"""Definition conditional Data Record (compatible with ISO 14229-1:2020) with Activated Events."""
CONDITIONAL_ACTIVATED_EVENTS_2013 = ConditionalFormulaDataRecord(formula=get_activated_events_2013)
"""Definition conditional Data Record (compatible with ISO 14229-1:2013) with Activated Events."""

EVENT_TYPE_RECORD_01 = get_event_type_record_01()
"""Definition of `eventTypeRecord` Data Record for `event` equal to 0x01."""
EVENT_TYPE_RECORD_02_2013 = get_event_type_record_02_2013()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2013) for `event` equal to 0x02."""
EVENT_TYPE_RECORD_03_2020 = get_event_type_record_03_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x03."""
EVENT_TYPE_RECORD_03_2013 = get_event_type_record_03_2013()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2013) for `event` equal to 0x03."""
EVENT_TYPE_RECORD_07_2020 = get_event_type_record_07_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x07."""
EVENT_TYPE_RECORD_07_2013 = get_event_type_record_07_2013()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2013) for `event` equal to 0x07."""
EVENT_TYPE_RECORD_08_2020 = get_event_type_record_08_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x08."""
EVENT_TYPE_RECORD_09_2020 = get_event_type_record_09_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x09."""
CONDITIONAL_EVENT_TYPE_RECORD_09_2020 = get_event_type_record_09_2020_continuation()
"""Continuation of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x09."""

SERVICE_TO_RESPOND = get_service_to_respond()
"""Definition of `serviceToRespondToRecord` Data Record."""

CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2020 = ConditionalMappingDataRecord(mapping={
    0x00: (EVENT_WINDOW_TIME_2020,),
    0x01: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x03: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_03_2020,
           SERVICE_TO_RESPOND),
    0x04: (EVENT_WINDOW_TIME_2020,),
    0x05: (EVENT_WINDOW_TIME_2020,),
    0x06: (EVENT_WINDOW_TIME_2020,),
    0x07: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_07_2020,
           SERVICE_TO_RESPOND),
    0x08: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_08_2020),
    0x09: (EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_09_2020, CONDITIONAL_EVENT_TYPE_RECORD_09_2020),
},
    value_mask=0x3F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` request message."""

CONDITIONAL_RESPONSE_ON_EVENT_REQUEST_2013 = ConditionalMappingDataRecord(mapping={
    0x00: (EVENT_WINDOW_TIME_2013,),
    0x01: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x02: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_02_2013,
           SERVICE_TO_RESPOND),
    0x03: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_03_2013,
           SERVICE_TO_RESPOND),
    0x04: (EVENT_WINDOW_TIME_2013,),
    0x05: (EVENT_WINDOW_TIME_2013,),
    0x06: (EVENT_WINDOW_TIME_2013,),
    0x07: (EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_07_2013,
           SERVICE_TO_RESPOND),
},
    value_mask=0x3F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` request message."""


CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2020 = ConditionalMappingDataRecord(mapping={
    0x00: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020),
    0x01: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x03: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_03_2020,
           SERVICE_TO_RESPOND),
    0x04: (NUMBER_OF_ACTIVATED_EVENTS, CONDITIONAL_ACTIVATED_EVENTS_2020),
    0x05: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020),
    0x06: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020),
    0x07: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_07_2020,
           SERVICE_TO_RESPOND),
    0x08: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_08_2020),
    0x09: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2020,
           EVENT_TYPE_RECORD_09_2020, CONDITIONAL_EVENT_TYPE_RECORD_09_2020),
},
    value_mask=0x3F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2020) of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` response message."""

CONDITIONAL_RESPONSE_ON_EVENT_RESPONSE_2013 = ConditionalMappingDataRecord(mapping={
    0x00: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013),
    0x01: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_01,
           SERVICE_TO_RESPOND),
    0x02: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_02_2013,
           SERVICE_TO_RESPOND),
    0x03: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_03_2013,
           SERVICE_TO_RESPOND),
    0x04: (NUMBER_OF_ACTIVATED_EVENTS, CONDITIONAL_ACTIVATED_EVENTS_2013),
    0x05: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013),
    0x06: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013),
    0x07: (NUMBER_OF_IDENTIFIED_EVENTS, EVENT_WINDOW_TIME_2013,
           EVENT_TYPE_RECORD_07_2013,
           SERVICE_TO_RESPOND),
},
    value_mask=0x3F)
"""Definition of conditional continuation (compatible with ISO 14229-1:2013) of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` response message."""

# SID 0x87

CONDITIONAL_LINK_CONTROL_REQUEST = ConditionalMappingDataRecord(value_mask=0x7F,
                                                                mapping={
                                                                    0x01: (LINK_CONTROL_MODE_IDENTIFIER,),
                                                                    0x02: (LINK_RECORD,),
                                                                    0x03: (),
                                                                })
"""Definition of conditional continuation of
:ref:`LinkControl <knowledge-base-service-link-control>` request message."""

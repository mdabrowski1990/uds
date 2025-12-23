"""Definitions for Conditional Data Records."""

__all__ = [
    # Shared
    "CONDITIONAL_MEMORY_ADDRESS_AND_SIZE",
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
    # SID 0x86
    "EVENT_TYPE_RECORD_01",
    "EVENT_TYPE_RECORD_03_2020", "EVENT_TYPE_RECORD_03_2013",
    "EVENT_TYPE_RECORD_07_2020", "EVENT_TYPE_RECORD_07_2013",
    "EVENT_TYPE_RECORD_09_2020", "CONDITIONAL_EVENT_TYPE_RECORD_09_2020"
]

from uds.utilities import REPEATED_DATA_RECORDS_NUMBER

from ..data_record import ConditionalFormulaDataRecord, RawDataRecord
from .dtc import (
    DTC_EXTENDED_DATA_RECORDS_DATA_LIST,
    DTC_STORED_DATA_RECORD_NUMBERS_LIST,
    DTCS_AND_STATUSES_LIST,
    OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
    OPTIONAL_DTCS_AND_STATUSES_LIST,
)
from .formula import (
    get_conditional_event_type_record_09_2020,
    get_did_records_formula_2013,
    get_did_records_formula_2020,
    get_event_type_record_01,
    get_event_type_record_03_2013,
    get_event_type_record_03_2020,
    get_event_type_record_07_2013,
    get_event_type_record_07_2020,
    get_event_type_record_09_2020,
    get_formula_for_raw_data_record_with_length,
    get_memory_size_and_memory_address,
)

DTC_DIDS_RECORDS_LIST_2013 = [
    ConditionalFormulaDataRecord(formula=get_did_records_formula_2013(record_number + 1))
    for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
DTC_DIDS_RECORDS_LIST_2020 = [
    ConditionalFormulaDataRecord(formula=get_did_records_formula_2020(record_number + 1))
    for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
RECORDS_DID_COUNTS_LIST = [RawDataRecord(name=f"DIDCount#{record_number + 1}",
                                         length=8,
                                         min_occurrences=1,
                                         max_occurrences=1,
                                         unit="DIDs")
                           for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]

DTC_SNAPSHOT_RECORDS_LIST_2013 = [
    item for snapshot_record in zip(OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
                                    RECORDS_DID_COUNTS_LIST,
                                    DTC_DIDS_RECORDS_LIST_2013)
    for item in snapshot_record]
DTC_SNAPSHOT_RECORDS_LIST_2020 = [
    item for snapshot_record in zip(OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST,
                                    RECORDS_DID_COUNTS_LIST,
                                    DTC_DIDS_RECORDS_LIST_2020)
    for item in snapshot_record]

DTCS_WITH_STATUSES_AND_EXTENDED_DATA_RECORDS_DATA_LIST = [
    item for data_records in zip(OPTIONAL_DTCS_AND_STATUSES_LIST,
                                 DTC_EXTENDED_DATA_RECORDS_DATA_LIST)
    for item in data_records]

DTC_STORED_DATA_RECORDS_LIST_2013 = [
    item for stored_data_record in zip(DTC_STORED_DATA_RECORD_NUMBERS_LIST,
                                       DTCS_AND_STATUSES_LIST,
                                       RECORDS_DID_COUNTS_LIST,
                                       DTC_DIDS_RECORDS_LIST_2013)
    for item in stored_data_record]
DTC_STORED_DATA_RECORDS_LIST_2020 = [
    item for stored_data_record in zip(DTC_STORED_DATA_RECORD_NUMBERS_LIST,
                                       DTCS_AND_STATUSES_LIST,
                                       RECORDS_DID_COUNTS_LIST,
                                       DTC_DIDS_RECORDS_LIST_2020)
    for item in stored_data_record]

# Shared

CONDITIONAL_MEMORY_ADDRESS_AND_SIZE = ConditionalFormulaDataRecord(formula=get_memory_size_and_memory_address)
"""Definition of conditional `memoryAddress` and `memorySize` Data Records."""

# SID 0x29

CONDITIONAL_CERTIFICATE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="certificateClient",
                                                        accept_zero_length=False))
"""Definition of conditional `certificateClient` Data Record."""

CONDITIONAL_CERTIFICATE_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="certificateServer",
                                                        accept_zero_length=False))
"""Definition of conditional `certificateServer` Data Record."""

CONDITIONAL_CERTIFICATE_DATA = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="certificateData",
                                                        accept_zero_length=False))
"""Definition of conditional `certificateData` Data Record."""

CONDITIONAL_CHALLENGE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="challengeClient",
                                                        accept_zero_length=False))
"""Definition of conditional `challengeClient` Data Record."""
CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="challengeClient",
                                                        accept_zero_length=True))
"""Definition of optional conditional `challengeClient` Data Record."""

CONDITIONAL_CHALLENGE_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="challengeServer",
                                                        accept_zero_length=False))
"""Definition of conditional `challengeServer` Data Record."""

CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="proofOfOwnershipClient",
                                                        accept_zero_length=False))
"""Definition of conditional `proofOfOwnershipClient` Data Record."""

CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="proofOfOwnershipServer",
                                                        accept_zero_length=False))
"""Definition of conditional `proofOfOwnershipServer` Data Record."""

CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="ephemeralPublicKeyClient",
                                                        accept_zero_length=True))
"""Definition of optional conditional `ephemeralPublicKeyClient` Data Record."""

CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="ephemeralPublicKeyServer",
                                                        accept_zero_length=True))
"""Definition of optional conditional `ephemeralPublicKeyServer` Data Record."""

CONDITIONAL_OPTIONAL_NEEDED_ADDITIONAL_PARAMETER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="neededAdditionalParameter",
                                                        accept_zero_length=True))
"""Definition of optional conditional `neededAdditionalParameter` Data Record."""

CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="additionalParameter",
                                                        accept_zero_length=True))
"""Definition of optional conditional `additionalParameter` Data Record."""

CONDITIONAL_OPTIONAL_SESSION_KEY_INFO = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="sessionKeyInfo",
                                                        accept_zero_length=True))
"""Definition of optional conditional `sessionKeyInfo` Data Record."""

# SID 0x86

EVENT_TYPE_RECORD_01 = get_event_type_record_01()
"""Definition of `eventTypeRecord` Data Record for `event` equal to 0x01."""
EVENT_TYPE_RECORD_03_2020 = get_event_type_record_03_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x03."""
EVENT_TYPE_RECORD_03_2013 = get_event_type_record_03_2013()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2013) for `event` equal to 0x03."""
EVENT_TYPE_RECORD_07_2020 = get_event_type_record_07_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x07."""
EVENT_TYPE_RECORD_07_2013 = get_event_type_record_07_2013()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2013) for `event` equal to 0x07."""
EVENT_TYPE_RECORD_09_2020 = get_event_type_record_09_2020()
"""Definition of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x09."""
CONDITIONAL_EVENT_TYPE_RECORD_09_2020 = get_conditional_event_type_record_09_2020()
"""Continuation of `eventTypeRecord` Data Record (compatible with ISO 14229-1:2020) for `event` equal to 0x09."""

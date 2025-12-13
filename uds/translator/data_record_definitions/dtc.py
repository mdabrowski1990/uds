"""DTC related Data Records definitions."""

__all__ = [
    # DTC
    "GROUP_OF_DTC", "DTC_COUNT", "DTC",
    # DTC Status
    "DTC_STATUS", "DTC_STATUS_MASK", "DTC_STATUS_AVAILABILITY_MASK",
    # DTC Severity
    "DTC_SEVERITY", "DTC_SEVERITY_MASK", "DTC_SEVERITY_AVAILABILITY_MASK",
    # DTC Snapshot Data
    "DTC_SNAPSHOT_RECORD_NUMBER", "DTC_SNAPSHOT_RECORDS_LIST_2013", "DTC_SNAPSHOT_RECORDS_LIST_2020",
    # DTC Extended Data
    "DTC_EXTENDED_DATA_RECORD_NUMBER", "OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER",
    "DTC_EXTENDED_DATA_RECORDS_DATA_LIST", "OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST",
    "DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST",
    # DTC Stored Data
    "DTC_STORED_DATA_RECORD_NUMBER",
    "DTC_STORED_DATA_RECORDS_LIST_2013", "DTC_STORED_DATA_RECORDS_LIST_2020",
    # DTC Format Identifier
    "DTC_FORMAT_IDENTIFIER",
    # DTC Functional Group Identifier
    "DTC_FUNCTIONAL_GROUP_IDENTIFIER",
    # DTC Readiness Group Identifier
    "DTC_READINESS_GROUP_IDENTIFIER",
    # Other
    "FAULT_DETECTION_COUNTER",
    "EVENT_TYPE_RECORD_01", "EVENT_TYPE_RECORD_09_2020",
    "CONDITIONAL_EVENT_TYPE_RECORD_09",
    # Mixed
    "DTC_AND_STATUS", "OPTIONAL_DTC_AND_STATUS", "MULTIPLE_DTC_AND_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SEVERITY_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTERS",
    "OPTIONAL_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER_RECORDS",
    "DTCS_WITH_STATUSES_AND_EXTENDED_DATA_RECORDS_DATA_LIST",
]

from typing import Optional

from uds.utilities import REPEATED_DATA_RECORDS_NUMBER

from ..data_record import (
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    MappingDataRecord,
    RawDataRecord,
    TextDataRecord,
    TextEncoding,
)
from .did import get_did_records_formula_2013, get_did_records_formula_2020
from .other import MEMORY_SELECTION, RESERVED_BIT
from .sub_functions import REPORT_TYPE_2020

# Common
NO_YES_MAPPING = {0: "no", 1: "yes"}
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


# formulas
def get_event_type_record_01(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get eventTypeRecord Data Record for event equal to 0x01.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventTypeRecord Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(DTC_STATUS_MASK,))


def get_event_type_record_09_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get eventTypeRecord Data Record for event equal to 0x09.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventTypeRecord Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=16,
                         children=(DTC_STATUS_MASK,
                                   RESERVED_BIT,
                                   REPORT_TYPE_2020))


def get_conditional_event_type_record_09_2020(event_number: Optional[int] = None) -> ConditionalMappingDataRecord:
    """
    Get conditional continuation for eventTypeRecord Data Record (event equal to 0x09).

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created Conditional Data Record.
    """
    if event_number is None:
        return ConditionalMappingDataRecord(mapping={0x04: (DTC_SNAPSHOT_RECORD_NUMBER,),
                                                     0x06: (DTC_EXTENDED_DATA_RECORD_NUMBER,),
                                                     0x18: (DTC_SNAPSHOT_RECORD_NUMBER, MEMORY_SELECTION),
                                                     0x19: (DTC_EXTENDED_DATA_RECORD_NUMBER, MEMORY_SELECTION), },
                                            value_mask=0x7F)
    return ConditionalMappingDataRecord(mapping={
        0x04: (MappingDataRecord(name=f"DTCSnapshotRecordNumber#{event_number}",
                                 values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                 length=8),),
        0x06: (MappingDataRecord(name=f"DTCExtDataRecordNumber#{event_number}",
                                 values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                 length=8),),
        0x18: (MappingDataRecord(name=f"DTCSnapshotRecordNumber#{event_number}",
                                 values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                 length=8),
               RawDataRecord(name=f"MemorySelection#{event_number}",
                             length=8)),
        0x19: (MappingDataRecord(name=f"DTCExtDataRecordNumber#{event_number}",
                                 values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                 length=8),
               RawDataRecord(name=f"MemorySelection#{event_number}",
                             length=8)),
    },
        value_mask=0x7F)


# DTC
GROUP_OF_DTC = RawDataRecord(name="groupOfDTC",
                             length=24)
DTC_COUNT = RawDataRecord(name="DTCCount",
                          length=16,
                          unit="DTCs")
DTC = TextDataRecord(name="DTC",
                     encoding=TextEncoding.DTC_OBD_FORMAT,
                     min_occurrences=1,
                     max_occurrences=1,
                     enforce_reoccurring=False)

# DTC Status
DTC_STATUS_BIT0 = MappingDataRecord(name="testFailed",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT1 = MappingDataRecord(name="testFailedThisOperationCycle",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT2 = MappingDataRecord(name="pendingDTC",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT3 = MappingDataRecord(name="confirmedDTC",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT4 = MappingDataRecord(name="testNotCompletedSinceLastClear",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT5 = MappingDataRecord(name="testFailedSinceLastClear",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT6 = MappingDataRecord(name="testNotCompletedThisOperationCycle",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BIT7 = MappingDataRecord(name="warningIndicatorRequested",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
DTC_STATUS_BITS = (DTC_STATUS_BIT7,
                   DTC_STATUS_BIT6,
                   DTC_STATUS_BIT5,
                   DTC_STATUS_BIT4,
                   DTC_STATUS_BIT3,
                   DTC_STATUS_BIT2,
                   DTC_STATUS_BIT1,
                   DTC_STATUS_BIT0)
DTC_STATUS_MASK = RawDataRecord(name="DTCStatusMask",
                                children=DTC_STATUS_BITS,
                                length=8)
DTC_STATUS_AVAILABILITY_MASK = RawDataRecord(name="DTCStatusAvailabilityMask",
                                             children=DTC_STATUS_BITS,
                                             length=8)
DTC_STATUS = RawDataRecord(name="DTCStatus",
                           children=DTC_STATUS_BITS,
                           length=8)

# DTC Severity
DTC_SEVERITY_BIT0 = MappingDataRecord(name="DTCClass_0",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT1 = MappingDataRecord(name="DTCClass_1",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT2 = MappingDataRecord(name="DTCClass_2",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT3 = MappingDataRecord(name="DTCClass_3",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT4 = MappingDataRecord(name="DTCClass_4",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT5 = MappingDataRecord(name="maintenanceOnly",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT6 = MappingDataRecord(name="checkAtNextHalt",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BIT7 = MappingDataRecord(name="checkImmediately",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
DTC_SEVERITY_BITS = (DTC_SEVERITY_BIT7,
                     DTC_SEVERITY_BIT6,
                     DTC_SEVERITY_BIT5,
                     DTC_SEVERITY_BIT4,
                     DTC_SEVERITY_BIT3,
                     DTC_SEVERITY_BIT2,
                     DTC_SEVERITY_BIT1,
                     DTC_SEVERITY_BIT0)
DTC_SEVERITY = RawDataRecord(name="DTCSeverity",
                             children=DTC_SEVERITY_BITS,
                             length=8)
DTC_SEVERITY_MASK = RawDataRecord(name="DTCSeverityMask",
                                  children=DTC_SEVERITY_BITS,
                                  length=8)
DTC_SEVERITY_AVAILABILITY_MASK = RawDataRecord(name="DTCSeverityAvailabilityMask",
                                               children=DTC_SEVERITY_BITS,
                                               length=8)

# DTC Snapshot Data
DTC_SNAPSHOT_RECORD_NUMBER_MAPPING = {
    0xFF: "all"
}

DTC_SNAPSHOT_RECORD_NUMBER = MappingDataRecord(name="DTCSnapshotRecordNumber",
                                               values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                               length=8)
OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST = [MappingDataRecord(name=f"DTCSnapshotRecordNumber#{record_number + 1}",
                                                                values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                                                length=8,
                                                                min_occurrences=0,
                                                                max_occurrences=1)
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

# DTC Extended Data
DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING = {
    0xFE: "all regulated emissions data",
    0xFF: "all",
}
OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCExtDataRecordNumber",
                                                             values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                                             length=8,
                                                             min_occurrences=0,
                                                             max_occurrences=1)
DTC_EXTENDED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCExtDataRecordNumber",
                                                    values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                                    length=8)
DTC_EXTENDED_DATA_RECORDS_NUMBERS_LIST = [RawDataRecord(name=f"DTCExtDataRecordNumber#{record_number + 1}",
                                                        length=8,
                                                        min_occurrences=0,
                                                        max_occurrences=1)
                                          for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
DTC_EXTENDED_DATA_RECORDS_DATA_LIST = [RawDataRecord(name=f"DTCExtDataRecord#{record_number + 1}",
                                                     length=8,
                                                     min_occurrences=1,
                                                     max_occurrences=None)
                                       for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST = [RawDataRecord(name=f"DTCExtDataRecord#{record_number + 1}",
                                                              length=8,
                                                              min_occurrences=0,
                                                              max_occurrences=None)
                                                for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST = [
    item for extended_data_record in zip(DTC_EXTENDED_DATA_RECORDS_NUMBERS_LIST,
                                         DTC_EXTENDED_DATA_RECORDS_DATA_LIST)
    for item in extended_data_record]

# DTC Stored Data
DTC_STORED_DATA_RECORD_NUMBER_MAPPING = {
    0xFF: "all",
}
DTC_STORED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCStoredDataRecordNumber",
                                                  values_mapping=DTC_STORED_DATA_RECORD_NUMBER_MAPPING,
                                                  length=8)
DTC_STORED_DATA_RECORD_NUMBERS_LIST = [MappingDataRecord(name=f"DTCStoredDataRecordNumber#{record_number + 1}",
                                                         values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                                         length=8,
                                                         min_occurrences=1 if record_number == 0 else 0,
                                                         max_occurrences=1)
                                       for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]

# DTC Format Identifier
DTC_FORMAT_IDENTIFIER_MAPPING = {
    0x00: "SAE J2012-DA DTC Format 00",
    0x01: "ISO 14229-1 DTC Format",
    0x02: "SAE J1939-73 DTC Format",
    0x03: "ISO 11992-4 DTC Format",
    0x04: "SAE J2012-DA DTC Format 04"
}
DTC_FORMAT_IDENTIFIER = MappingDataRecord(name="DTCFormatIdentifier",
                                          values_mapping=DTC_FORMAT_IDENTIFIER_MAPPING,
                                          length=8)

# DTC Functional Group Identifier
DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING = {
    0x33: "Emissions-system group",
    0xD0: "Safety-system group",
    0xFE: "VOBD system",
    0xFF: "all"
}
# TODO: separate from DTCFunctionalUnit (https://github.com/mdabrowski1990/uds/issues/413)
DTC_FUNCTIONAL_GROUP_IDENTIFIER = MappingDataRecord(name="FunctionalGroupIdentifier",
                                                    values_mapping=DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING,
                                                    length=8)

# DTC Readiness Group Identifier
DTC_READINESS_GROUP_IDENTIFIER = RawDataRecord(name="DTCReadinessGroupIdentifier",
                                               length=8)

# Other
FAULT_DETECTION_COUNTER = RawDataRecord(name="FaultDetectionCounter",
                                        length=8)

EVENT_TYPE_RECORD_01 = get_event_type_record_01()

EVENT_TYPE_RECORD_09_2020 = get_event_type_record_09_2020()
CONDITIONAL_EVENT_TYPE_RECORD_09 = get_conditional_event_type_record_09_2020()

# Mixed
DTC_AND_STATUS = RawDataRecord(name="DTC and DTCStatus",
                               length=32,
                               children=(DTC, DTC_STATUS))
OPTIONAL_DTC_AND_STATUS = RawDataRecord(name="DTC and DTCStatus",
                                        length=32,
                                        children=(DTC, DTC_STATUS),
                                        min_occurrences=0,
                                        max_occurrences=1)
MULTIPLE_DTC_AND_STATUS_RECORDS = RawDataRecord(name="DTC and DTCStatus",
                                                length=32,
                                                children=(DTC, DTC_STATUS),
                                                min_occurrences=0,
                                                max_occurrences=None)
DTCS_AND_STATUSES_LIST = [RawDataRecord(name=f"DTC and DTCStatus#{record_number + 1}",
                                        length=32,
                                        children=(DTC, DTC_STATUS))
                          for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
OPTIONAL_DTCS_AND_STATUSES_LIST = [RawDataRecord(name=f"DTC and DTCStatus#{record_number + 1}",
                                                 length=32,
                                                 children=(DTC, DTC_STATUS),
                                                 min_occurrences=0,
                                                 max_occurrences=1)
                                   for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]

MULTIPLE_DTC_AND_SEVERITY_STATUS_RECORDS = RawDataRecord(name="Severity, DTC and DTC Status",
                                                         length=40,
                                                         children=(DTC_SEVERITY, DTC, DTC_STATUS),
                                                         min_occurrences=0,
                                                         max_occurrences=None)

MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTERS = RawDataRecord(name="DTC and Fault Detection Counter",
                                                          length=32,
                                                          children=(DTC, FAULT_DETECTION_COUNTER),
                                                          min_occurrences=0,
                                                          max_occurrences=None)

OPTIONAL_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS = RawDataRecord(
    name="Severity, Functional Unit, DTC and DTCStatus",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_GROUP_IDENTIFIER,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=1)
MULTIPLE_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS = RawDataRecord(
    name="Severity, Functional Unit, DTC and DTCStatus",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_GROUP_IDENTIFIER,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=None)

MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER_RECORDS = RawDataRecord(name="DTC and DTCSnapshotRecordNumber",
                                                                length=32,
                                                                children=(DTC, DTC_SNAPSHOT_RECORD_NUMBER),
                                                                min_occurrences=0,
                                                                max_occurrences=None)

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

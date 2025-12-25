"""DTC related Data Records definitions."""

__all__ = [
    # DTC
    "GROUP_OF_DTC",
    "DTC",
    "DTC_COUNT",
    # DTC Status
    "DTC_STATUS_BIT7",
    "DTC_STATUS_BIT6",
    "DTC_STATUS_BIT5",
    "DTC_STATUS_BIT4",
    "DTC_STATUS_BIT3",
    "DTC_STATUS_BIT2",
    "DTC_STATUS_BIT1",
    "DTC_STATUS_BIT0",
    "DTC_STATUS_BITS",
    "DTC_STATUS", "DTC_STATUS_MASK", "DTC_STATUS_AVAILABILITY_MASK",
    # DTC Severity
    "DTC_SEVERITY_BIT7",
    "DTC_SEVERITY_BIT6",
    "DTC_SEVERITY_BIT5",
    "DTC_SEVERITY_BIT4",
    "DTC_SEVERITY_BIT3",
    "DTC_SEVERITY_BIT2",
    "DTC_SEVERITY_BIT1",
    "DTC_SEVERITY_BIT0",
    "DTC_SEVERITY_BITS",
    "DTC_SEVERITY", "DTC_SEVERITY_MASK", "DTC_SEVERITY_AVAILABILITY_MASK",
    # DTC Snapshot Data
    "DTC_SNAPSHOT_RECORD_NUMBER",
    "OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST",
    # DTC Extended Data
    "DTC_EXTENDED_DATA_RECORD_NUMBER", "OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER",
    "DTC_EXTENDED_DATA_RECORDS_NUMBERS_LIST",
    "DTC_EXTENDED_DATA_RECORDS_DATA_LIST", "OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST",
    "DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST",
    # DTC Stored Data
    "DTC_STORED_DATA_RECORD_NUMBER",
    "DTC_STORED_DATA_RECORD_NUMBERS_LIST",
    # DTC Format Identifier
    "DTC_FORMAT_IDENTIFIER",
    # DTC Functional Group Identifier
    "DTC_FUNCTIONAL_GROUP_IDENTIFIER",
    # DTC Readiness Group Identifier
    "DTC_READINESS_GROUP_IDENTIFIER",
    # DTC Functional Unit
    "DTC_FUNCTIONAL_UNIT",
    # DTC Fault Detection Counter
    "FAULT_DETECTION_COUNTER",
    # Mixed
    "DTC_AND_STATUS", "OPTIONAL_DTC_AND_STATUS", "MULTIPLE_DTC_AND_STATUS",
    "DTCS_AND_STATUSES_LIST", "OPTIONAL_DTCS_AND_STATUSES_LIST",
    "MULTIPLE_DTC_SEVERITY_DTC_AND_STATUS",
    "MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTER",
    "OPTIONAL_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS", "MULTIPLE_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS",
    "MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER",
]



from uds.utilities import (
    DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
    DTC_FORMAT_IDENTIFIER_MAPPING,
    DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING,
    DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
    DTC_STORED_DATA_RECORD_NUMBER_MAPPING,
    GROUP_OF_DTC_MAPPING,
    NO_YES_MAPPING,
    REPEATED_DATA_RECORDS_NUMBER,
    get_signed_value_decoding_formula,
    get_signed_value_encoding_formula,
)

from ..data_record import CustomFormulaDataRecord, MappingDataRecord, RawDataRecord, TextDataRecord, TextEncoding

# DTC

GROUP_OF_DTC = MappingDataRecord(name="groupOfDTC",
                                 length=24,
                                 values_mapping=GROUP_OF_DTC_MAPPING)
"""Definition of `groupOfDTC` Data Record."""

DTC = TextDataRecord(name="DTC",
                     encoding=TextEncoding.DTC_OBD_FORMAT,
                     min_occurrences=1,
                     max_occurrences=1,
                     enforce_reoccurring=False)
"""Definition of :ref:`DTC <knowledge-base-dtc>` Data Record."""

DTC_COUNT = RawDataRecord(name="DTCCount",
                          length=16,
                          unit="DTCs")
"""Definition of `DTCCount` Data Record."""

# DTC Status

DTC_STATUS_BIT7 = MappingDataRecord(name="warningIndicatorRequested",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 7 (MSB)."""
DTC_STATUS_BIT6 = MappingDataRecord(name="testNotCompletedThisOperationCycle",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 6."""
DTC_STATUS_BIT5 = MappingDataRecord(name="testFailedSinceLastClear",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 5."""
DTC_STATUS_BIT4 = MappingDataRecord(name="testNotCompletedSinceLastClear",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 4."""
DTC_STATUS_BIT3 = MappingDataRecord(name="confirmedDTC",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 3."""
DTC_STATUS_BIT2 = MappingDataRecord(name="pendingDTC",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 2."""
DTC_STATUS_BIT1 = MappingDataRecord(name="testFailedThisOperationCycle",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 1."""
DTC_STATUS_BIT0 = MappingDataRecord(name="testFailed",
                                    length=1,
                                    values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCStatus <knowledge-base-dtc-status>` bit 0 (LSB)."""

DTC_STATUS_BITS = (DTC_STATUS_BIT7,
                   DTC_STATUS_BIT6,
                   DTC_STATUS_BIT5,
                   DTC_STATUS_BIT4,
                   DTC_STATUS_BIT3,
                   DTC_STATUS_BIT2,
                   DTC_STATUS_BIT1,
                   DTC_STATUS_BIT0)
"""Collection of Data Records with :ref:`DTCStatus <knowledge-base-dtc-status>` bits."""

DTC_STATUS = RawDataRecord(name="DTCStatus",
                           children=DTC_STATUS_BITS,
                           length=8)
"""Definition of :ref:`DTCStatus <knowledge-base-dtc-status>` Data Record."""

DTC_STATUS_MASK = RawDataRecord(name="DTCStatusMask",
                                children=DTC_STATUS_BITS,
                                length=8)
"""Definition of `DTCStatusMask` Data Record."""

DTC_STATUS_AVAILABILITY_MASK = RawDataRecord(name="DTCStatusAvailabilityMask",
                                             children=DTC_STATUS_BITS,
                                             length=8)
"""Definition of `DTCStatusAvailabilityMask` Data Record."""

# DTC Severity

DTC_SEVERITY_BIT7 = MappingDataRecord(name="checkImmediately",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 7 (MSB)."""
DTC_SEVERITY_BIT6 = MappingDataRecord(name="checkAtNextHalt",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 6."""
DTC_SEVERITY_BIT5 = MappingDataRecord(name="maintenanceOnly",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 5."""
DTC_SEVERITY_BIT4 = MappingDataRecord(name="DTCClass_4",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 4."""
DTC_SEVERITY_BIT3 = MappingDataRecord(name="DTCClass_3",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 3."""
DTC_SEVERITY_BIT2 = MappingDataRecord(name="DTCClass_2",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 2."""
DTC_SEVERITY_BIT1 = MappingDataRecord(name="DTCClass_1",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 1."""
DTC_SEVERITY_BIT0 = MappingDataRecord(name="DTCClass_0",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of Data Record for :ref:`DTCSeverity <knowledge-base-dtc-severity>` bit 0 (LSB)."""

DTC_SEVERITY_BITS = (DTC_SEVERITY_BIT7,
                     DTC_SEVERITY_BIT6,
                     DTC_SEVERITY_BIT5,
                     DTC_SEVERITY_BIT4,
                     DTC_SEVERITY_BIT3,
                     DTC_SEVERITY_BIT2,
                     DTC_SEVERITY_BIT1,
                     DTC_SEVERITY_BIT0)
"""Collection of Data Records with :ref:`DTCSeverity <knowledge-base-dtc-severity>` bits."""

DTC_SEVERITY = RawDataRecord(name="DTCSeverity",
                             children=DTC_SEVERITY_BITS,
                             length=8)
"""Definition of :ref:`DTCSeverity <knowledge-base-dtc-severity>` Data Record."""

DTC_SEVERITY_MASK = RawDataRecord(name="DTCSeverityMask",
                                  children=DTC_SEVERITY_BITS,
                                  length=8)
"""Definition of `DTCSeverityMask` Data Record."""

DTC_SEVERITY_AVAILABILITY_MASK = RawDataRecord(name="DTCSeverityAvailabilityMask",
                                               children=DTC_SEVERITY_BITS,
                                               length=8)
"""Definition of `DTCSeverityAvailabilityMask` Data Record."""

# DTC Snapshot Data

DTC_SNAPSHOT_RECORD_NUMBER = MappingDataRecord(name="DTCSnapshotRecordNumber",
                                               values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                               length=8)
"""Definition of `DTCSnapshotRecordNumber` Data Record."""

OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST = [MappingDataRecord(name=f"DTCSnapshotRecordNumber#{record_number + 1}",
                                                                values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                                                length=8,
                                                                min_occurrences=0,
                                                                max_occurrences=1)
                                              for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of optional `DTCSnapshotRecordNumber` Data Records."""

# DTC Extended Data

DTC_EXTENDED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCExtDataRecordNumber",
                                                    values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                                    length=8)
"""Definition of `DTCExtDataRecordNumber` Data Record."""

OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCExtDataRecordNumber",
                                                             values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                                             length=8,
                                                             min_occurrences=0,
                                                             max_occurrences=1)
"""Definition of optional `DTCExtDataRecordNumber` Data Record."""

DTC_EXTENDED_DATA_RECORDS_NUMBERS_LIST = [RawDataRecord(name=f"DTCExtDataRecordNumber#{record_number + 1}",
                                                        length=8,
                                                        min_occurrences=0,
                                                        max_occurrences=1)
                                          for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of `DTCExtDataRecordNumber` Data Records."""

DTC_EXTENDED_DATA_RECORDS_DATA_LIST = [RawDataRecord(name=f"DTCExtDataRecord#{record_number + 1}",
                                                     length=8,
                                                     min_occurrences=1,
                                                     max_occurrences=None)
                                       for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of `DTCExtDataRecord` Data Records."""

OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST = [RawDataRecord(name=f"DTCExtDataRecord#{record_number + 1}",
                                                              length=8,
                                                              min_occurrences=0,
                                                              max_occurrences=None)
                                                for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of optional `DTCExtDataRecord` Data Records."""

DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST = [
    item for extended_data_record in zip(DTC_EXTENDED_DATA_RECORDS_NUMBERS_LIST,
                                         DTC_EXTENDED_DATA_RECORDS_DATA_LIST)
    for item in extended_data_record]
"""Collection of `DTCExtDataRecordNumber` and corresponding `DTCExtDataRecord` Data Records."""

# DTC Stored Data

DTC_STORED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCStoredDataRecordNumber",
                                                  values_mapping=DTC_STORED_DATA_RECORD_NUMBER_MAPPING,
                                                  length=8)
"""Definition of `DTCStoredDataRecordNumber` Data Record."""

DTC_STORED_DATA_RECORD_NUMBERS_LIST = [MappingDataRecord(name=f"DTCStoredDataRecordNumber#{record_number + 1}",
                                                         values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                                         length=8,
                                                         min_occurrences=1 if record_number == 0 else 0,
                                                         max_occurrences=1)
                                       for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of `DTCStoredDataRecordNumber` Data Records."""

# DTC Format Identifier

DTC_FORMAT_IDENTIFIER = MappingDataRecord(name="DTCFormatIdentifier",
                                          values_mapping=DTC_FORMAT_IDENTIFIER_MAPPING,
                                          length=8)
"""Definition of `DTCFormatIdentifier` Data Record."""

# DTC Functional Group Identifier

DTC_FUNCTIONAL_GROUP_IDENTIFIER = MappingDataRecord(name="FunctionalGroupIdentifier",
                                                    values_mapping=DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING,
                                                    length=8)
"""Definition of :ref:`FunctionalGroupIdentifier <knowledge-base-dtc-functional-group-identifier>` Data Record."""

# DTC Readiness Group Identifier

DTC_READINESS_GROUP_IDENTIFIER = RawDataRecord(name="DTCReadinessGroupIdentifier",
                                               length=8)
"""Definition of :ref:`DTCReadinessGroupIdentifier <knowledge-base-dtc-readiness-group>` Data Record."""

# DTC Functional Unit

DTC_FUNCTIONAL_UNIT = RawDataRecord(name="DTCFunctionalUnit",
                                    length=8)
"""Definition of :ref:`DTCFunctionalUnit <knowledge-base-dtc-functional-unit>` Data Record."""

# DTC Fault Detection Counter

FAULT_DETECTION_COUNTER = CustomFormulaDataRecord(name="DTCFaultDetectionCounter",
                                                  length=8,
                                                  encoding_formula=get_signed_value_encoding_formula(8),
                                                  decoding_formula=get_signed_value_decoding_formula(8))
"""Definition of :ref:`DTCFaultDetectionCounter <knowledge-base-dtc-fault-detection-counter>` Data Record."""

# Mixed

DTC_AND_STATUS = RawDataRecord(name="DTC and DTCStatus",
                               length=32,
                               children=(DTC, DTC_STATUS))
"""Definition of `DTC and DTCStatus` Data Record."""

OPTIONAL_DTC_AND_STATUS = RawDataRecord(name="DTC and DTCStatus",
                                        length=32,
                                        children=(DTC, DTC_STATUS),
                                        min_occurrences=0,
                                        max_occurrences=1)
"""Definition of optional `DTC and DTCStatus` Data Record."""

MULTIPLE_DTC_AND_STATUS = RawDataRecord(name="DTC and DTCStatus",
                                        length=32,
                                        children=(DTC, DTC_STATUS),
                                        min_occurrences=0,
                                        max_occurrences=None)
"""Definition of multiple `DTC and DTCStatus` Data Record."""

DTCS_AND_STATUSES_LIST = [RawDataRecord(name=f"DTC and DTCStatus#{record_number + 1}",
                                        length=32,
                                        children=(DTC, DTC_STATUS))
                          for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of `DTC and DTCStatus` Data Records."""

OPTIONAL_DTCS_AND_STATUSES_LIST = [RawDataRecord(name=f"DTC and DTCStatus#{record_number + 1}",
                                                 length=32,
                                                 children=(DTC, DTC_STATUS),
                                                 min_occurrences=0,
                                                 max_occurrences=1)
                                   for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]
"""Collection of optional `DTC and DTCStatus` Data Records."""

MULTIPLE_DTC_SEVERITY_DTC_AND_STATUS = RawDataRecord(name="DTCSeverity, DTC and DTCStatus",
                                                     length=40,
                                                     children=(DTC_SEVERITY, DTC, DTC_STATUS),
                                                     min_occurrences=0,
                                                     max_occurrences=None)
"""Definition of multiple `DTCSeverity, DTC and DTCStatus` Data Record."""

MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTER = RawDataRecord(name="DTC and DTCFaultDetectionCounter",
                                                         length=32,
                                                         children=(DTC, FAULT_DETECTION_COUNTER),
                                                         min_occurrences=0,
                                                         max_occurrences=None)
"""Definition of multiple `DTC and DTCFaultDetectionCounter` Data Record."""

OPTIONAL_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS = RawDataRecord(
    name="DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_UNIT,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=1)
"""Definition of optional `DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus` Data Record."""

MULTIPLE_DTC_SEVERITY_FUNCTIONAL_UNIT_DTC_AND_STATUS = RawDataRecord(
    name="DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_UNIT,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=None)
"""Definition of multiple `DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus` Data Record."""

MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER = RawDataRecord(name="DTC and DTCSnapshotRecordNumber",
                                                        length=32,
                                                        children=(DTC, DTC_SNAPSHOT_RECORD_NUMBER),
                                                        min_occurrences=0,
                                                        max_occurrences=None)
"""Definition of multiple `DTC and DTCSnapshotRecordNumber` Data Record."""

"""DTC related Data Records definitions."""

__all__ = [
    # DTC
    "GROUP_OF_DTC", "DTC_COUNT", "DTC",
    # DTC Status
    "DTC_STATUS", "DTC_STATUS_MASK", "DTC_STATUS_AVAILABILITY_MASK",
    # DTC Severity
    "DTC_SEVERITY", "DTC_SEVERITY_MASK", "DTC_SEVERITY_AVAILABILITY_MASK",
    # DTC Snapshot Data
    "DTC_SNAPSHOT_RECORD_NUMBER",
    # DTC Extended Data
    "DTC_EXTENDED_DATA_RECORD_NUMBER", "OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER",
    "DTC_EXTENDED_DATA_RECORDS_DATA_LIST", "OPTIONAL_DTC_EXTENDED_DATA_RECORDS_DATA_LIST",
    "DTC_EXTENDED_DATA_RECORDS_NUMBERS_AND_DATA_LIST",
    # DTC Stored Data
    "DTC_STORED_DATA_RECORD_NUMBER",
    # DTC Format Identifier
    "DTC_FORMAT_IDENTIFIER",
    # DTC Functional Group Identifier
    "DTC_FUNCTIONAL_GROUP_IDENTIFIER",
    # DTC Readiness Group Identifier
    "DTC_READINESS_GROUP_IDENTIFIER",
    # Other
    "DTC_FUNCTIONAL_UNIT",
    "FAULT_DETECTION_COUNTER",
    # Mixed
    "DTC_AND_STATUS", "OPTIONAL_DTC_AND_STATUS", "MULTIPLE_DTC_AND_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SEVERITY_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTERS",
    "OPTIONAL_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER_RECORDS",
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
)

from ..data_record import MappingDataRecord, RawDataRecord, TextDataRecord, TextEncoding

# DTC

GROUP_OF_DTC = MappingDataRecord(name="groupOfDTC",
                                 length=24,
                                 values_mapping=GROUP_OF_DTC_MAPPING)
"""Definition of `groupOfDTC` Data Record that is part of
:ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` message."""

DTC = TextDataRecord(name="DTC",
                     encoding=TextEncoding.DTC_OBD_FORMAT,
                     min_occurrences=1,
                     max_occurrences=1,
                     enforce_reoccurring=False)
"""Definition of :ref:`DTC <knowledge-base-dtc>` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

DTC_COUNT = RawDataRecord(name="DTCCount",
                          length=16,
                          unit="DTCs")
"""Definition of `DTCCount` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

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
"""Definition of :ref:`DTCStatus <knowledge-base-dtc-status>` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

DTC_STATUS_MASK = RawDataRecord(name="DTCStatusMask",
                                children=DTC_STATUS_BITS,
                                length=8)
"""Definition of `DTCStatusMask` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

DTC_STATUS_AVAILABILITY_MASK = RawDataRecord(name="DTCStatusAvailabilityMask",
                                             children=DTC_STATUS_BITS,
                                             length=8)
"""Definition of `DTCStatusAvailabilityMask` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

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
"""Definition of :ref:`DTCSeverity <knowledge-base-dtc-severity>` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

DTC_SEVERITY_MASK = RawDataRecord(name="DTCSeverityMask",
                                  children=DTC_SEVERITY_BITS,
                                  length=8)
"""Definition of `DTCSeverityMask` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

DTC_SEVERITY_AVAILABILITY_MASK = RawDataRecord(name="DTCSeverityAvailabilityMask",
                                               children=DTC_SEVERITY_BITS,
                                               length=8)
"""Definition of `DTCSeverityAvailabilityMask` Data Record that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` message."""

# DTC Snapshot Data

DTC_SNAPSHOT_RECORD_NUMBER = MappingDataRecord(name="DTCSnapshotRecordNumber",
                                               values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                               length=8)













OPTIONAL_DTC_SNAPSHOT_RECORDS_NUMBERS_LIST = [MappingDataRecord(name=f"DTCSnapshotRecordNumber#{record_number + 1}",
                                                                values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                                                length=8,
                                                                min_occurrences=0,
                                                                max_occurrences=1)
                                              for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]


# DTC Extended Data

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

DTC_FORMAT_IDENTIFIER = MappingDataRecord(name="DTCFormatIdentifier",
                                          values_mapping=DTC_FORMAT_IDENTIFIER_MAPPING,
                                          length=8)

# DTC Functional Group Identifier

DTC_FUNCTIONAL_GROUP_IDENTIFIER = MappingDataRecord(name="FunctionalGroupIdentifier",
                                                    values_mapping=DTC_FUNCTIONAL_GROUP_IDENTIFIER_MAPPING,
                                                    length=8)

# DTC Readiness Group Identifier
DTC_READINESS_GROUP_IDENTIFIER = RawDataRecord(name="DTCReadinessGroupIdentifier",
                                               length=8)

# Other
DTC_FUNCTIONAL_UNIT = RawDataRecord(name="DTCFunctionalUnit",
                                    length=8)
FAULT_DETECTION_COUNTER = RawDataRecord(name="DTCFaultDetectionCounter",
                                        length=8)



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

MULTIPLE_DTC_AND_SEVERITY_STATUS_RECORDS = RawDataRecord(name="DTCSeverity, DTC and DTCStatus",
                                                         length=40,
                                                         children=(DTC_SEVERITY, DTC, DTC_STATUS),
                                                         min_occurrences=0,
                                                         max_occurrences=None)

MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTERS = RawDataRecord(name="DTC and DTCFaultDetectionCounter",
                                                          length=32,
                                                          children=(DTC, FAULT_DETECTION_COUNTER),
                                                          min_occurrences=0,
                                                          max_occurrences=None)

OPTIONAL_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS = RawDataRecord(
    name="DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_UNIT,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=1)
MULTIPLE_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS = RawDataRecord(
    name="DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_UNIT,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=None)

MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER_RECORDS = RawDataRecord(name="DTC and DTCSnapshotRecordNumber",
                                                                length=32,
                                                                children=(DTC, DTC_SNAPSHOT_RECORD_NUMBER),
                                                                min_occurrences=0,
                                                                max_occurrences=None)

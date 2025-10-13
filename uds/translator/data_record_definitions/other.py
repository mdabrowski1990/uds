"""Remaining Data Records definitions."""

__all__ = [
    # SID 0x10
    "P2_SERVER_MAX", "P2_EXT_SERVER_MAX", "SESSION_PARAMETER_RECORD",
    # SID 0x11
    "POWER_DOWN_TIME", "CONDITIONAL_POWER_DOWN_TIME",
    # SID 0x14
    "GROUP_OF_DTC", "OPTIONAL_MEMORY_SELECTION",
    # SID 0x19
    "DTC_STATUS_MASK", "DTC_STATUS_AVAILABILITY_MASK", "DTC_STATUS",
    "DTC_SEVERITY_MASK", "DTC_SEVERITY_AVAILABILITY_MASK",
    "DTC_FUNCTIONAL_GROUP_IDENTIFIER", "DTC_FORMAT_IDENTIFIER", "DTC_READINESS_GROUP_IDENTIFIER",
    "DTC", "DTC_COUNT", "MEMORY_SELECTION",
    "DTC_SNAPSHOT_RECORD_NUMBER", "DTC_STORED_DATA_RECORD_NUMBER",
    "OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER", "DTC_EXTENDED_DATA_RECORD_NUMBER", "DTC_EXTENDED_DATA_RECORDS",
    "MULTIPLE_DTC_AND_STATUS_RECORDS", "OPTIONAL_DTC_AND_STATUS_RECORD",
    "MULTIPLE_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS",
    "OPTIONAL_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SEVERITY_STATUS_RECORDS",
    "MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER_RECORDS",
    "MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTERS",
]

from ..data_record import (
    ConditionalMappingDataRecord,
    LinearFormulaDataRecord,
    MappingAndLinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
    TextDataRecord,
    TextEncoding,
)

# shared
NO_YES_MAPPING = {0: "no", 1: "yes"}
# SID 0x10
P2_SERVER_MAX = LinearFormulaDataRecord(name="P2Server_max",
                                        length=16,
                                        factor=1,
                                        offset=0,
                                        unit="ms")
P2_EXT_SERVER_MAX = LinearFormulaDataRecord(name="P2*Server_max",
                                            length=16,
                                            factor=10,
                                            offset=0,
                                            unit="ms")
SESSION_PARAMETER_RECORD = RawDataRecord(name="sessionParameterRecord",
                                         length=32,
                                         children=(P2_SERVER_MAX, P2_EXT_SERVER_MAX))
# SID 0x11
POWER_DOWN_TIME = MappingAndLinearFormulaDataRecord(name="powerDownTime",
                                                    length=8,
                                                    values_mapping={0xFF: "ERROR"},
                                                    factor=1,
                                                    offset=0,
                                                    unit="s")
CONDITIONAL_POWER_DOWN_TIME = ConditionalMappingDataRecord(mapping={0x4: [POWER_DOWN_TIME]},
                                                           default_message_continuation=[])
# SID 0x14
GROUP_OF_DTC = RawDataRecord(name="groupOfDTC",
                             length=24)
OPTIONAL_MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                          length=8,
                                          min_occurrences=0,
                                          max_occurrences=1)
# SID 0x19
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
DTC_STATUS_BITS = (DTC_STATUS_BIT7,
                   DTC_STATUS_BIT6,
                   DTC_STATUS_BIT5,
                   DTC_STATUS_BIT4,
                   DTC_STATUS_BIT3,
                   DTC_STATUS_BIT2,
                   DTC_STATUS_BIT1,
                   DTC_STATUS_BIT0)
DTC_SEVERITY_BITS = (DTC_SEVERITY_BIT7,
                     DTC_SEVERITY_BIT6,
                     DTC_SEVERITY_BIT5,
                     DTC_SEVERITY_BIT4,
                     DTC_SEVERITY_BIT3,
                     DTC_SEVERITY_BIT2,
                     DTC_SEVERITY_BIT1,
                     DTC_SEVERITY_BIT0)
DTC_STATUS = RawDataRecord(name="DTC Status",
                           children=DTC_STATUS_BITS,
                           length=8)
DTC_SEVERITY = RawDataRecord(name="DTC Severity",
                             children=DTC_SEVERITY_BITS,
                             length=8)
DTC_STATUS_MASK = RawDataRecord(name="DTCStatusMask",
                                children=DTC_STATUS_BITS,
                                length=8)
DTC_SEVERITY_MASK = RawDataRecord(name="DTCSeverityMask",
                                  children=DTC_SEVERITY_BITS,
                                  length=8)
DTC_STATUS_AVAILABILITY_MASK = RawDataRecord(name="DTCStatusAvailabilityMask",
                                             children=DTC_STATUS_BITS,
                                             length=8)
DTC_SEVERITY_AVAILABILITY_MASK = RawDataRecord(name="DTCSeverityAvailabilityMask",
                                               children=DTC_SEVERITY_BITS,
                                               length=8)
DTC = TextDataRecord(name="DTC",
                     encoding=TextEncoding.DTC_OBD_FORMAT,
                     min_occurrences=1,
                     max_occurrences=1)
DTC_COUNT = RawDataRecord(name="DTCCount",
                          length=16,
                          unit="DTCs")
MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                 length=8)
DTC_FAULT_DETECTION = RawDataRecord(name="FaultDetectionCounter",
                                    length=8)
DTC_FORMAT_IDENTIFIER = MappingDataRecord(name="DTCFormatIdentifier",
                                          values_mapping={
                                              0x00: "SAE J2012-DA DTC Format 00",
                                              0x01: "ISO 14229-1 DTC Format",
                                              0x02: "SAE J1939-73 DTC Format",
                                              0x03: "ISO 11992-4 DTC Format",
                                              0x04: "SAE J2012-DA DTC Format 04"
                                          },
                                          length=8)
DTC_FUNCTIONAL_GROUP_IDENTIFIER = MappingDataRecord(name="FunctionalGroupIdentifier",
                                                    values_mapping={
                                                        0x33: "Emissions-system group",
                                                        0xD0: "Safety-system group",
                                                        0xFE: "VOBD system",
                                                        0xFF: "all"
                                                    },
                                                    length=8)
DTC_READINESS_GROUP_IDENTIFIER = RawDataRecord(name="DTCReadinessGroupIdentifier",
                                               length=8)
DTC_SNAPSHOT_RECORD_NUMBER = MappingDataRecord(name="DTCSnapshotRecordNumber",
                                               values_mapping={
                                                   0xFF: "all"
                                               },
                                               length=8)
DTC_STORED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCStoredDataRecordNumber",
                                              values_mapping={
                                                  0xFF: "all"
                                              },
                                              length=8)
DTC_EXTENDED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCExtDataRecordNumber",
                                                    values_mapping={
                                                        0xFE: "all regulated emissions data",
                                                        0xFF: "all",
                                                    },
                                                    length=8)
OPTIONAL_DTC_EXTENDED_DATA_RECORD_NUMBER = MappingDataRecord(name="DTCExtDataRecordNumber",
                                                             values_mapping={
                                                                 0xFE: "all regulated emissions data",
                                                                 0xFF: "all",
                                                             },
                                                             length=8,
                                                             min_occurrences=0,
                                                             max_occurrences=1)
DTC_EXTENDED_DATA_RECORD_NUMBERS = {
    record_number:  RawDataRecord(name=f"DTCExtDataRecordNumber#{record_number}",
                                  length=8,
                                  min_occurrences=0,
                                  max_occurrences=1)
    for record_number in range(1, 254)
}
DTC_EXTENDED_DATA_RECORDS_DATA = {
    record_number: RawDataRecord(name=f"DTCExtDataRecord#{record_number}",
                                 length=8,
                                 min_occurrences=1,
                                 max_occurrences=None)
    for record_number in range(1, 254)
}
DTC_EXTENDED_DATA_RECORDS = [item for record_number in range(1, 254)
                             for item in (DTC_EXTENDED_DATA_RECORD_NUMBERS[record_number],
                                          DTC_EXTENDED_DATA_RECORDS_DATA[record_number])]

OPTIONAL_DTC_AND_STATUS_RECORD = RawDataRecord(name="DTC and Status",
                                               length=32,
                                               children=(DTC, DTC_STATUS),
                                               min_occurrences=0,
                                               max_occurrences=1)
MULTIPLE_DTC_AND_STATUS_RECORDS = RawDataRecord(name="DTC and Status",
                                                length=32,
                                                children=(DTC, DTC_STATUS),
                                                min_occurrences=0,
                                                max_occurrences=None)
MULTIPLE_DTC_AND_SNAPSHOT_RECORD_NUMBER_RECORDS = RawDataRecord(name="DTC and Snapshot Record Number",
                                                                length=32,
                                                                children=(DTC, DTC_SNAPSHOT_RECORD_NUMBER),
                                                                min_occurrences=0,
                                                                max_occurrences=None)
OPTIONAL_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS = RawDataRecord(
    name="Severity, Functional Unit, DTC and Status",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_GROUP_IDENTIFIER,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=1)
MULTIPLE_DTC_AND_SEVERITY_FUNCTIONAL_UNIT_STATUS_RECORDS = RawDataRecord(
    name="Severity, Functional Unit, DTC and Status",
    length=48,
    children=(DTC_SEVERITY,
              DTC_FUNCTIONAL_GROUP_IDENTIFIER,
              DTC,
              DTC_STATUS),
    min_occurrences=0,
    max_occurrences=None)
MULTIPLE_DTC_AND_SEVERITY_STATUS_RECORDS = RawDataRecord(name="Severity, DTC and DTC Status",
                                                         length=40,
                                                         children=(DTC_SEVERITY,
                                                                   DTC,
                                                                   DTC_STATUS),
                                                         min_occurrences=0,
                                                         max_occurrences=None)
MULTIPLE_DTC_AND_FAULT_DETECTION_COUNTERS = RawDataRecord(name="DTC and Fault Detection Counter",
                                                          length=32,
                                                          children=(DTC,
                                                                    DTC_FAULT_DETECTION),
                                                          min_occurrences=0,
                                                          max_occurrences=None)

"""Remaining Data Records definitions."""

__all__ = [
    # SID 0x10
    "P2_SERVER_MAX", "P2_EXT_SERVER_MAX", "SESSION_PARAMETER_RECORD",
    # SID 0x11
    "POWER_DOWN_TIME", "CONDITIONAL_POWER_DOWN_TIME",
    # SID 0x14
    "GROUP_OF_DTC", "MEMORY_SELECTION",
    # SID 0x19
    "DTC_STATUS_MASK", "DTC_STATUS_AVAILABILITY_MASK",
    "MULTIPLE_DTC_AND_STATUS_RECORDS", "OPTIONAL_SINGLE_DTC_AND_STATUS_RECORD",
    "DTC_FORMAT_IDENTIFIER", "DTC_COUNT",
]

from ..data_record import (
    ConditionalMappingDataRecord,
    LinearFormulaDataRecord,
    MappingAndLinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
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
MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                 length=8,
                                 min_occurrences=0,
                                 max_occurrences=1)
# SID 0x19
DTC = RawDataRecord(name="DTC",
                    length=24)
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
DTC_STATUS = RawDataRecord(name="DTCStatusMask",
                           children=DTC_STATUS_BITS,
                           length=8)
DTC_STATUS_MASK = RawDataRecord(name="DTCStatusMask",
                                children=DTC_STATUS_BITS,
                                length=8)
DTC_STATUS_AVAILABILITY_MASK = RawDataRecord(name="DTCStatusAvailabilityMask",
                                             children=DTC_STATUS_BITS,
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
DTC_COUNT = RawDataRecord(name="DTCCount",
                          length=16,
                          unit="DTCs")
MULTIPLE_DTC_AND_STATUS_RECORDS = RawDataRecord(name="DTC and Status",
                                                length=32,
                                                children=(DTC, DTC_STATUS),
                                                min_occurrences=0,
                                                max_occurrences=None)
OPTIONAL_SINGLE_DTC_AND_STATUS_RECORD = RawDataRecord(name="DTC and Status",
                                                       length=32,
                                                       children=(DTC, DTC_STATUS),
                                                       min_occurrences=0,
                                                       max_occurrences=1)

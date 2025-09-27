"""Data Records definitions for sub-functions."""

__all__ = [
    # shared
    "SPRMIB",
    # SID 0x10
    "DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION", "DIAGNOSTIC_SESSION_TYPE", "DIAGNOSTIC_SESSIONS_MAPPING",
    # SID 0x11
    "ECU_RESET_SUB_FUNCTION_2020", "ECU_RESET_SUB_FUNCTION_2013", "RESET_TYPE_2020", "RESET_TYPE_2013",
    "RESET_TYPES_MAPPING_2020", "RESET_TYPES_MAPPING_2013",
    # SID 0x3E
    "TESTER_PRESENT_SUB_FUNCTION", "ZERO_SUB_FUNCTION",
]

from uds.translator.data_record.mapping_data_record import MappingDataRecord
from uds.translator.data_record.raw_data_record import RawDataRecord

# shared
SPRMIB = MappingDataRecord(name="suppressPosRspMsgIndicationBit",
                           length=1,
                           values_mapping={
                               1: "yes",
                               0: "no",
                           })
# SID 0x10
DIAGNOSTIC_SESSIONS_MAPPING = {
    0x01: "defaultSession",
    0x02: "programmingSession",
    0x03: "extendedDiagnosticSession",
    0x04: "safetySystemDiagnosticSession",
}
DIAGNOSTIC_SESSION_TYPE = MappingDataRecord(name="diagnosticSessionType",
                                            length=7,
                                            values_mapping=DIAGNOSTIC_SESSIONS_MAPPING)
DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                        length=8,
                                                        children=[SPRMIB, DIAGNOSTIC_SESSION_TYPE])
# SID 0x11
RESET_TYPES_MAPPING_2013 = {
    0x01: "hardReset",
}
RESET_TYPES_MAPPING_2020 = {
    0x01: "hardReset",
    0x02: "keyOffOnReset",
    0x03: "softReset",
    0x04: "enableRapidPowerShutDown",
    0x05: "disableRapidPowerShutDown",
}
RESET_TYPE_2013 = MappingDataRecord(name="resetType",
                                    length=7,
                                    values_mapping=RESET_TYPES_MAPPING_2013)
RESET_TYPE_2020 = MappingDataRecord(name="resetType",
                                    length=7,
                                    values_mapping=RESET_TYPES_MAPPING_2020)
ECU_RESET_SUB_FUNCTION_2013 = RawDataRecord(name="SubFunction",
                                       length=8,
                                       children=[SPRMIB, RESET_TYPE_2013])
ECU_RESET_SUB_FUNCTION_2020 = RawDataRecord(name="SubFunction",
                                       length=8,
                                       children=[SPRMIB, RESET_TYPES_MAPPING_2020])
# SID 0x3E
ZERO_SUB_FUNCTION = RawDataRecord(name="zeroSubFunction",
                                  length=7)
TESTER_PRESENT_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=[SPRMIB, ZERO_SUB_FUNCTION])

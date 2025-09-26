"""Data Records definitions for sub-functions."""

__all__ = [
    "SPRMIB",
    "DIAGNOSTIC_SESSION_TYPE", "DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION",
    "ZERO_SUB_FUNCTION", "TESTER_PRESENT_SUB_FUNCTION",
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
DIAGNOSTIC_SESSION_TYPE = MappingDataRecord(name="diagnosticSessionType",
                                            length=7,
                                            values_mapping={
                                                0x01: "defaultSession",
                                                0x02: "programmingSession",
                                                0x03: "extendedDiagnosticSession",
                                                0x04: "safetySystemDiagnosticSession",
                                            })
DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                        length=8,
                                                        children=[SPRMIB, DIAGNOSTIC_SESSION_TYPE])
# SID 0x3E
ZERO_SUB_FUNCTION = RawDataRecord(name="zeroSubFunction",
                                  length=7)
TESTER_PRESENT_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=[SPRMIB, ZERO_SUB_FUNCTION])

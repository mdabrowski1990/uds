"""Data Records definitions for sub-functions."""

__all__ = [
    # shared
    "SPRMIB", "MAPPING_YES_NO",
    # SID 0x10
    "DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION", "DIAGNOSTIC_SESSION_TYPE", "DIAGNOSTIC_SESSIONS_MAPPING",
    # SID 0x11
    "ECU_RESET_SUB_FUNCTION", "RESET_TYPE", "RESET_TYPES_MAPPING",
    # SID 0x19
    "READ_DTC_INFORMATION_SUB_FUNCTION_2020", "READ_DTC_INFORMATION_SUB_FUNCTION_2013",
    "REPORT_TYPE_2020", "REPORT_TYPE_2013", "REPORT_TYPES_MAPPING_2020", "REPORT_TYPES_MAPPING_2013",
    # SID 0x27
    "SECURITY_ACCESS_SUB_FUNCTION", "SECURITY_ACCESS_TYPE", "SECURITY_ACCESS_TYPES_MAPPING",
    # SID 0x28
    "COMMUNICATION_CONTROL_SUB_FUNCTION", "CONTROL_TYPE", "CONTROL_TYPE_MAPPING",
    # SID 0x29
    "AUTHENTICATION_SUB_FUNCTION", "AUTHENTICATION_TASK", "AUTHENTICATION_TASK_MAPPING",
    # SID 0x2C
    "DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION", "DEFINITION_TYPE", "DEFINITION_TYPE_MAPPING",
    # SID 0x31
    "ROUTINE_CONTROL_SUB_FUNCTION", "ROUTINE_CONTROL_TYPE", "ROUTINE_CONTROL_TYPE_MAPPING",
    # SID 0x3E
    "TESTER_PRESENT_SUB_FUNCTION", "ZERO_SUB_FUNCTION", "ZERO_SUB_FUNCTION_MAPPING",
    # SID 0x83
    "ACCESS_TIMING_PARAMETER_SUB_FUNCTION", "TIMING_PARAMETER_ACCESS_TYPE", "TIMING_PARAMETER_ACCESS_TYPE_MAPPING",
    # SID 0x85
    "CONTROL_DTC_SETTING_SUB_FUNCTION", "DTC_SETTING_TYPE", "DTC_SETTING_TYPE_MAPPING",
]

from ..data_record import MappingDataRecord, RawDataRecord

# shared
MAPPING_YES_NO = {
    1: "yes",
    0: "no",
}
SPRMIB = MappingDataRecord(name="suppressPosRspMsgIndicationBit",
                           length=1,
                           values_mapping=MAPPING_YES_NO)

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
RESET_TYPES_MAPPING = {
    0x01: "hardReset",
    0x02: "keyOffOnReset",
    0x03: "softReset",
    0x04: "enableRapidPowerShutDown",
    0x05: "disableRapidPowerShutDown",
}
RESET_TYPE = MappingDataRecord(name="resetType",
                               length=7,
                               values_mapping=RESET_TYPES_MAPPING)
ECU_RESET_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                       length=8,
                                       children=[SPRMIB, RESET_TYPE])

# SID 0x19
REPORT_TYPES_MAPPING_2013 = {
    0x01: "reportNumberOfDTCByStatusMask",
    0x02: "reportDTCByStatusMask",
    0x03: "reportDTCSnapshotIdentification",
    0x04: "reportDTCSnapshotRecordByDTCNumber",
    0x05: "reportDTCStoredDataByRecordNumber",
    0x06: "reportDTCExtDataRecordByDTCNumber",
    0x07: "reportNumberOfDTCBySeverityMaskRecord",
    0x08: "reportDTCBySeverityMaskRecord",
    0x09: "reportSeverityInformationOfDTC",
    0x0A: "reportSupportedDTC",
    0x0B: "reportFirstTestFailedDTC",
    0x0C: "reportFirstConfirmedDTC",
    0x0D: "reportMostRecentTestFailedDTC",
    0x0E: "reportMostRecentConfirmedDTC",
    0x0F: "reportMirrorMemoryDTCByStatusMask",
    0x10: "reportMirrorMemoryDTCExtDataRecordByDTCNumber",
    0x11: "reportNumberOfMirrorMemoryDTCByStatusMask",
    0x12: "reportNumberOfEmissionsOBDDTCByStatusMask",
    0x13: "reportEmissionsOBDDTCByStatusMask",
    0x14: "reportDTCFaultDetectionCounter",
    0x15: "reportDTCWithPermanentStatus",
    0x16: "reportDTCExtDataRecordByRecordNumber",
    0x17: "reportUserDefMemoryDTCByStatusMask",
    0x18: "reportUserDefMemoryDTCSnapshotRecordByDTCNumber",
    0x19: "reportUserDefMemoryDTCExtDataRecordByDTCNumber",
    0x42: "reportWWHOBDDTCByMaskRecord",
    0x55: "reportWWHOBDDTCWithPermanentStatus",
}
REPORT_TYPES_MAPPING_2020 = {
    0x01: "reportNumberOfDTCByStatusMask",
    0x02: "reportDTCByStatusMask",
    0x03: "reportDTCSnapshotIdentification",
    0x04: "reportDTCSnapshotRecordByDTCNumber",
    0x05: "reportDTCStoredDataByRecordNumber",
    0x06: "reportDTCExtDataRecordByDTCNumber",
    0x07: "reportNumberOfDTCBySeverityMaskRecord",
    0x08: "reportDTCBySeverityMaskRecord",
    0x09: "reportSeverityInformationOfDTC",
    0x0A: "reportSupportedDTC",
    0x0B: "reportFirstTestFailedDTC",
    0x0C: "reportFirstConfirmedDTC",
    0x0D: "reportMostRecentTestFailedDTC",
    0x0E: "reportMostRecentConfirmedDTC",
    0x14: "reportDTCFaultDetectionCounter",
    0x15: "reportDTCWithPermanentStatus",
    0x16: "reportDTCExtDataRecordByRecordNumber",
    0x17: "reportUserDefMemoryDTCByStatusMask",
    0x18: "reportUserDefMemoryDTCSnapshotRecordByDTCNumber",
    0x19: "reportUserDefMemoryDTCExtDataRecordByDTCNumber",
    0x1A: "reportSupportedDTCExtDataRecord",
    0x42: "reportWWHOBDDTCByMaskRecord",
    0x55: "reportWWHOBDDTCWithPermanentStatus",
    0x56: "reportDTCInformationByDTCReadinessGroupIdentifier",
}
REPORT_TYPE_2013 = MappingDataRecord(name="reportType",
                                     length=7,
                                     values_mapping=REPORT_TYPES_MAPPING_2013)
REPORT_TYPE_2020 = MappingDataRecord(name="reportType",
                                     length=7,
                                     values_mapping=REPORT_TYPES_MAPPING_2020)
READ_DTC_INFORMATION_SUB_FUNCTION_2013 = RawDataRecord(name="SubFunction",
                                                       length=8,
                                                       children=[SPRMIB, REPORT_TYPE_2013])
READ_DTC_INFORMATION_SUB_FUNCTION_2020 = RawDataRecord(name="SubFunction",
                                                       length=8,
                                                       children=[SPRMIB, REPORT_TYPE_2020])

# SID 0x27
SECURITY_ACCESS_TYPES_MAPPING = {
    sub_function_value: sub_function_description
    for i in range(1, 0x42, 2)
    for sub_function_value, sub_function_description in {
        i: f"Request Seed - level {i} (vehicle manufacturer specific)",
        i + 1: f"Send Key - level {i} (vehicle manufacturer specific)",
    }.items()
} | {
    sub_function_value: sub_function_description
    for i in range(0x61, 0x7E, 2)
    for sub_function_value, sub_function_description in {
        i: f"Request Seed - level {i} (system supplier specific)",
        i + 1: f"Send Key - level {i} (system supplier specific)"
    }.items()
} | {
    0x5F: "Request Seed - level 95, end of life (ISO 26021-2)",
    0x60: "Send Key - level 95, end of life (ISO 26021-2)",
}
SECURITY_ACCESS_TYPE = MappingDataRecord(name="securityAccessType",
                                         length=7,
                                         values_mapping=SECURITY_ACCESS_TYPES_MAPPING)
SECURITY_ACCESS_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                             length=8,
                                             children=[SPRMIB, SECURITY_ACCESS_TYPE])

# SID 0x28
CONTROL_TYPE_MAPPING = {
    0x00: "enableRxAndTx",
    0x01: "enableRxAndDisableTx",
    0x02: "disableRxAndEnableTx",
    0x03: "disableRxAndTx",
    0x04: "enableRxAndDisableTxWithEnhancedAddressInformation",
    0x05: "enableRxAndTxWithEnhancedAddressInformation",
}
CONTROL_TYPE = MappingDataRecord(name="controlType",
                                 length=7,
                                 values_mapping=CONTROL_TYPE_MAPPING)
COMMUNICATION_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                   length=8,
                                                   children=[SPRMIB, CONTROL_TYPE])

# SID 0x29
AUTHENTICATION_TASK_MAPPING = {
    0x00: "deAuthenticate",
    0x01: "verifyCertificateUnidirectional",
    0x02: "verifyCertificateBidirectional",
    0x03: "proofOfOwnership",
    0x04: "transmitCertificate",
    0x05: "requestChallengeForAuthentication",
    0x06: "verifyProofOfOwnershipUnidirectional",
    0x07: "verifyProofOfOwnershipBidirectional",
    0x08: "authenticationConfiguration",
}
AUTHENTICATION_TASK = MappingDataRecord(name="authenticationTask",
                                        length=7,
                                        values_mapping=AUTHENTICATION_TASK_MAPPING)
AUTHENTICATION_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=[SPRMIB, AUTHENTICATION_TASK])

# SID 0x2C
DEFINITION_TYPE_MAPPING = {
    0x01: "defineByIdentifier",
    0x02: "defineByMemoryAddress",
    0x03: "clearDynamicallyDefinedDataIdentifier",
}
DEFINITION_TYPE = MappingDataRecord(name="definitionType",
                                    length=7,
                                    values_mapping=DEFINITION_TYPE_MAPPING)
DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                                length=8,
                                                                children=[SPRMIB, DEFINITION_TYPE])

# SID 0x31
ROUTINE_CONTROL_TYPE_MAPPING = {
    0x01: "startRoutine",
    0x02: "stopRoutine",
    0x03: "requestRoutineResults",
}
ROUTINE_CONTROL_TYPE = MappingDataRecord(name="routineControlType",
                                         length=7,
                                         values_mapping=ROUTINE_CONTROL_TYPE_MAPPING)
ROUTINE_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                             length=8,
                                             children=[SPRMIB, ROUTINE_CONTROL_TYPE])

# SID 0x3E
ZERO_SUB_FUNCTION_MAPPING = {
    0x00: "zeroSubFunction",
}
ZERO_SUB_FUNCTION = MappingDataRecord(name="zeroSubFunction",
                                      length=7,
                                      values_mapping=ZERO_SUB_FUNCTION_MAPPING)
TESTER_PRESENT_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=[SPRMIB, ZERO_SUB_FUNCTION])

# SID 0x83
TIMING_PARAMETER_ACCESS_TYPE_MAPPING = {
    0x01: "readExtendedTimingParameterSet",
    0x02: "setTimingParametersToDefaultValues",
    0x03: "readCurrentlyActiveTimingParameters",
    0x04: "setTimingParametersToGivenValues",
}
TIMING_PARAMETER_ACCESS_TYPE = MappingDataRecord(name="timingParameterAccessType",
                                                 length=7,
                                                 values_mapping=TIMING_PARAMETER_ACCESS_TYPE_MAPPING)
ACCESS_TIMING_PARAMETER_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                     length=8,
                                                     children=[SPRMIB, TIMING_PARAMETER_ACCESS_TYPE])

# SID 0x85
DTC_SETTING_TYPE_MAPPING = {
    0x01: "on",
    0x02: "off",
}
DTC_SETTING_TYPE = MappingDataRecord(name="DTCSettingType",
                                     length=7,
                                     values_mapping=DTC_SETTING_TYPE_MAPPING)
CONTROL_DTC_SETTING_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                 length=8,
                                                 children=[SPRMIB, DTC_SETTING_TYPE])

"""SubFunction related constants."""

__all__ = [
    "DIAGNOSTIC_SESSION_TYPE_MAPPING",  # SID 0x10
    "RESET_TYPE_MAPPING",  # SID 0x11
    "REPORT_TYPE_MAPPING_2020", "REPORT_TYPE_MAPPING_2013",  # SID 0x19
    "SECURITY_ACCESS_TYPE_MAPPING",  # SID 0x27
    "CONTROL_TYPE_MAPPING",  # SID 0x28
    "AUTHENTICATION_TASK_MAPPING",  # SID 0x29
    "DEFINITION_TYPE_MAPPING",  # SID 0x2C
    "ROUTINE_CONTROL_TYPE_MAPPING",  # SID 0x31
    "ZERO_SUB_FUNCTION_MAPPING",  # SID 0x3E
    "TIMING_PARAMETER_ACCESS_TYPE_MAPPING_2013",  # SID 0x83
    "DTC_SETTING_TYPE_MAPPING",  # SID 0x85
    "EVENT_MAPPING_2020", "EVENT_MAPPING_2013", "STORAGE_STATE_MAPPING",  # SID 0x86
    "LINK_CONTROL_TYPE_MAPPING",  # SID 0x87
]

from typing import Dict

# SID 0x10
DIAGNOSTIC_SESSION_TYPE_MAPPING: Dict[int, str] = {
    0x01: "defaultSession",
    0x02: "programmingSession",
    0x03: "extendedDiagnosticSession",
    0x04: "safetySystemDiagnosticSession",
}
"""Values mapping for `diagnosticSessionType` Data Record that is part of
:ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` SubFunction."""

# SID 0x11
RESET_TYPE_MAPPING: Dict[int, str] = {
    0x01: "hardReset",
    0x02: "keyOffOnReset",
    0x03: "softReset",
    0x04: "enableRapidPowerShutDown",
    0x05: "disableRapidPowerShutDown",
}
"""Values mapping for `resetType` Data Record that is part of
:ref:`ECUReset <knowledge-base-service-ecu-reset>` SubFunction."""

# SID 0x19
REPORT_TYPE_MAPPING_2020: Dict[int, str] = {
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
"""Values mapping for `reportType` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` SubFunction."""
REPORT_TYPE_MAPPING_2013: Dict[int, str] = {
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
"""Values mapping for `reportType` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` SubFunction."""

# SID 0x27
SECURITY_ACCESS_TYPE_MAPPING = {
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
"""Values mapping for `securityAccessType` Data Record that is part of
:ref:`SecurityAccess <knowledge-base-service-security-access>` SubFunction."""

# SID 0x28
CONTROL_TYPE_MAPPING: Dict[int, str] = {
    0x00: "enableRxAndTx",
    0x01: "enableRxAndDisableTx",
    0x02: "disableRxAndEnableTx",
    0x03: "disableRxAndTx",
    0x04: "enableRxAndDisableTxWithEnhancedAddressInformation",
    0x05: "enableRxAndTxWithEnhancedAddressInformation",
}
"""Values mapping for `controlType` Data Record that is part of
:ref:`CommunicationControl <knowledge-base-service-communication-control>` SubFunction."""

# SID 0x29
AUTHENTICATION_TASK_MAPPING: Dict[int, str] = {
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
"""Values mapping for `authenticationTask` Data Record that is part of
:ref:`Authentication <knowledge-base-service-authentication>` SubFunction."""

# SID 0x2C
DEFINITION_TYPE_MAPPING: Dict[int, str] = {
    0x01: "defineByIdentifier",
    0x02: "defineByMemoryAddress",
    0x03: "clearDynamicallyDefinedDataIdentifier",
}
"""Values mapping for `definitionType` Data Record that is part of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` SubFunction."""

# SID 0x31
ROUTINE_CONTROL_TYPE_MAPPING: Dict[int, str] = {
    0x01: "startRoutine",
    0x02: "stopRoutine",
    0x03: "requestRoutineResults",
}
"""Values mapping for `routineControlType` Data Record that is part of
:ref:`RoutineControl <knowledge-base-service-routine-control>` SubFunction."""

# SID 0x3E
ZERO_SUB_FUNCTION_MAPPING: Dict[int, str] = {
    0x00: "zeroSubFunction",
}
"""Values mapping for `zeroSubFunction` Data Record that is part of
:ref:`TesterPresent <knowledge-base-service-tester-present>` SubFunction."""

# SID 0x83
TIMING_PARAMETER_ACCESS_TYPE_MAPPING_2013: Dict[int, str] = {
    0x01: "readExtendedTimingParameterSet",
    0x02: "setTimingParametersToDefaultValues",
    0x03: "readCurrentlyActiveTimingParameters",
    0x04: "setTimingParametersToGivenValues",
}
"""Values mapping for `timingParameterAccessType` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` SubFunction."""

# SID 0x85
DTC_SETTING_TYPE_MAPPING: Dict[int, str] = {
    0x01: "on",
    0x02: "off",
}
"""Values mapping for `DTCSettingType` Data Record that is part of
:ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` SubFunction."""

# SID 0x86
EVENT_MAPPING_2020: Dict[int, str] = {
    0x00: "stopResponseOnEvent",
    0x01: "onDTCStatusChange",
    0x03: "onChangeOfDataIdentifier",
    0x04: "reportActivatedEvents",
    0x05: "startResponseOnEvent",
    0x06: "clearResponseOnEvent",
    0x07: "onComparisonOfValues",
    0x08: "reportMostRecentDtcOnStatusChange",
    0x09: "reportDTCRecordInformationOnDtcStatusChange",
}
"""Values mapping for `event` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""
EVENT_MAPPING_2013: Dict[int, str] = {
    0x00: "stopResponseOnEvent",
    0x01: "onDTCStatusChange",
    0x02: "onTimerInterrupt",
    0x03: "onChangeOfDataIdentifier",
    0x04: "reportActivatedEvents",
    0x05: "startResponseOnEvent",
    0x06: "clearResponseOnEvent",
    0x07: "onComparisonOfValues",
}
"""Values mapping for `event` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""

STORAGE_STATE_MAPPING: Dict[int, str] = {
    0x00: "doNotStoreEvent",
    0x01: "storeEvent",
}
"""Values mapping for `storageState` Data Record that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""

# SID 0x87
LINK_CONTROL_TYPE_MAPPING: Dict[int, str] = {
    0x01: "verifyModeTransitionWithFixedParameter",
    0x02: "verifyModeTransitionWithSpecificParameter",
    0x03: "transitionMode",
}
"""Values mapping for `linkControlType` Data Record that is part of
:ref:`LinkControl <knowledge-base-service-link-control>` SubFunction."""

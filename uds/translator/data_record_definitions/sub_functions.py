"""Data Records definitions for sub-functions."""

__all__ = [
    # shared
    "SPRMIB",
    # SID 0x10
    "DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION", "DIAGNOSTIC_SESSION_TYPE",
    # SID 0x11
    "ECU_RESET_SUB_FUNCTION", "RESET_TYPE",
    # SID 0x19
    "READ_DTC_INFORMATION_SUB_FUNCTION_2020", "REPORT_TYPE_2020",
    "READ_DTC_INFORMATION_SUB_FUNCTION_2013", "REPORT_TYPE_2013",
    # SID 0x27
    "SECURITY_ACCESS_SUB_FUNCTION", "SECURITY_ACCESS_TYPE",
    # SID 0x28
    "COMMUNICATION_CONTROL_SUB_FUNCTION", "CONTROL_TYPE",
    # SID 0x29
    "AUTHENTICATION_SUB_FUNCTION", "AUTHENTICATION_TASK",
    # SID 0x2C
    "DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION", "DEFINITION_TYPE",
    # SID 0x31
    "ROUTINE_CONTROL_SUB_FUNCTION", "ROUTINE_CONTROL_TYPE",
    # SID 0x3E
    "TESTER_PRESENT_SUB_FUNCTION", "ZERO_SUB_FUNCTION",
    # SID 0x83
    "ACCESS_TIMING_PARAMETER_SUB_FUNCTION_2013", "TIMING_PARAMETER_ACCESS_TYPE_2013",
    # SID 0x85
    "CONTROL_DTC_SETTING_SUB_FUNCTION", "DTC_SETTING_TYPE",
    # SID 0x86
    "RESPONSE_ON_EVENT_SUB_FUNCTION_2020", "EVENT_TYPE_2020", "EVENT_2020",
    "RESPONSE_ON_EVENT_SUB_FUNCTION_2013", "EVENT_TYPE_2013", "EVENT_2013",
    "STORAGE_STATE",
    # SID 0x87
    "LINK_CONTROL_SUB_FUNCTION", "LINK_CONTROL_TYPE",
]

from uds.utilities import (
    AUTHENTICATION_TASK_MAPPING,
    CONTROL_TYPE_MAPPING,
    DEFINITION_TYPE_MAPPING,
    DIAGNOSTIC_SESSION_TYPE_MAPPING,
    DTC_SETTING_TYPE_MAPPING,
    EVENT_MAPPING_2013,
    EVENT_MAPPING_2020,
    LINK_CONTROL_TYPE_MAPPING,
    NO_YES_MAPPING,
    REPORT_TYPE_MAPPING_2013,
    REPORT_TYPE_MAPPING_2020,
    RESET_TYPE_MAPPING,
    ROUTINE_CONTROL_TYPE_MAPPING,
    SECURITY_ACCESS_TYPE_MAPPING,
    STORAGE_STATE_MAPPING,
    TIMING_PARAMETER_ACCESS_TYPE_MAPPING_2013,
    ZERO_SUB_FUNCTION_MAPPING,
)

from ..data_record import MappingDataRecord, RawDataRecord

# shared
SPRMIB = MappingDataRecord(name="suppressPosRspMsgIndicationBit",
                           length=1,
                           values_mapping=NO_YES_MAPPING)
"""Definition of `suppressPosRspMsgIndicationBit` Data Record that is part of every SubFunction."""

# SID 0x10
DIAGNOSTIC_SESSION_TYPE = MappingDataRecord(name="diagnosticSessionType",
                                            length=7,
                                            values_mapping=DIAGNOSTIC_SESSION_TYPE_MAPPING)
"""Definition of `diagnosticSessionType` Data Record that is part of
:ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` SubFunction."""

DIAGNOSTIC_SESSION_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                        length=8,
                                                        children=(SPRMIB, DIAGNOSTIC_SESSION_TYPE))
"""Definition of :ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` SubFunction."""

# SID 0x11
RESET_TYPE = MappingDataRecord(name="resetType",
                               length=7,
                               values_mapping=RESET_TYPE_MAPPING)
"""Definition of `resetType` Data Record that is part of
:ref:`ECUReset <knowledge-base-service-ecu-reset>` SubFunction."""

ECU_RESET_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                       length=8,
                                       children=(SPRMIB, RESET_TYPE))
"""Definition of :ref:`ECUReset <knowledge-base-service-ecu-reset>` SubFunction."""

# SID 0x19
REPORT_TYPE_2020 = MappingDataRecord(name="reportType",
                                     length=7,
                                     values_mapping=REPORT_TYPE_MAPPING_2020)
"""Definition of `reportType` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` SubFunction."""
REPORT_TYPE_2013 = MappingDataRecord(name="reportType",
                                     length=7,
                                     values_mapping=REPORT_TYPE_MAPPING_2013)
"""Definition of `reportType` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` SubFunction."""

READ_DTC_INFORMATION_SUB_FUNCTION_2020 = RawDataRecord(name="SubFunction",
                                                       length=8,
                                                       children=(SPRMIB, REPORT_TYPE_2020))
"""Definition (compatible with SIO 14229-1:2020) of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` SubFunction."""
READ_DTC_INFORMATION_SUB_FUNCTION_2013 = RawDataRecord(name="SubFunction",
                                                       length=8,
                                                       children=(SPRMIB, REPORT_TYPE_2013))
"""Definition (compatible with SIO 14229-1:2013) of
:ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` SubFunction."""

# SID 0x27
SECURITY_ACCESS_TYPE = MappingDataRecord(name="securityAccessType",
                                         length=7,
                                         values_mapping=SECURITY_ACCESS_TYPE_MAPPING)
"""Definition of `securityAccessType` Data Record that is part of
:ref:`SecurityAccess <knowledge-base-service-security-access>` SubFunction."""

SECURITY_ACCESS_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                             length=8,
                                             children=(SPRMIB, SECURITY_ACCESS_TYPE))
"""Definition of :ref:`SecurityAccess <knowledge-base-service-security-access>` SubFunction."""

# SID 0x28
CONTROL_TYPE = MappingDataRecord(name="controlType",
                                 length=7,
                                 values_mapping=CONTROL_TYPE_MAPPING)
"""Definition of `controlType` Data Record that is part of
:ref:`CommunicationControl <knowledge-base-service-communication-control>` SubFunction."""

COMMUNICATION_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                   length=8,
                                                   children=(SPRMIB, CONTROL_TYPE))
"""Definition of :ref:`CommunicationControl <knowledge-base-service-communication-control>` SubFunction."""

# SID 0x29
AUTHENTICATION_TASK = MappingDataRecord(name="authenticationTask",
                                        length=7,
                                        values_mapping=AUTHENTICATION_TASK_MAPPING)
"""Definition of `authenticationTask` Data Record that is part of
:ref:`Authentication <knowledge-base-service-authentication>` SubFunction."""

AUTHENTICATION_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=(SPRMIB, AUTHENTICATION_TASK))
"""Definition of :ref:`Authentication <knowledge-base-service-authentication>` SubFunction."""

# SID 0x2C
DEFINITION_TYPE = MappingDataRecord(name="definitionType",
                                    length=7,
                                    values_mapping=DEFINITION_TYPE_MAPPING)
"""Definition of `definitionType` Data Record that is part of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` SubFunction."""

DYNAMICALLY_DEFINE_DATA_IDENTIFIER_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                                length=8,
                                                                children=(SPRMIB, DEFINITION_TYPE))
"""Definition of
:ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` SubFunction."""

# SID 0x31
ROUTINE_CONTROL_TYPE = MappingDataRecord(name="routineControlType",
                                         length=7,
                                         values_mapping=ROUTINE_CONTROL_TYPE_MAPPING)
"""Definition of `routineControlType` Data Record that is part of
:ref:`RoutineControl <knowledge-base-service-routine-control>` SubFunction."""

ROUTINE_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                             length=8,
                                             children=(SPRMIB, ROUTINE_CONTROL_TYPE))
"""Definition of :ref:`RoutineControl <knowledge-base-service-routine-control>` SubFunction."""

# SID 0x3E
ZERO_SUB_FUNCTION = MappingDataRecord(name="zeroSubFunction",
                                      length=7,
                                      values_mapping=ZERO_SUB_FUNCTION_MAPPING)
"""Definition of `zeroSubFunction` Data Recird that is part of
:ref:`TesterPresent <knowledge-base-service-tester-present>` SubFunction."""

TESTER_PRESENT_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                            length=8,
                                            children=(SPRMIB, ZERO_SUB_FUNCTION))
"""Definition of :ref:`TesterPresent <knowledge-base-service-tester-present>` SubFunction."""

# SID 0x83
TIMING_PARAMETER_ACCESS_TYPE_2013 = MappingDataRecord(name="timingParameterAccessType",
                                                      length=7,
                                                      values_mapping=TIMING_PARAMETER_ACCESS_TYPE_MAPPING_2013)
"""Definition of `timingParameterAccessType` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` SubFunction."""

ACCESS_TIMING_PARAMETER_SUB_FUNCTION_2013 = RawDataRecord(name="SubFunction",
                                                          length=8,
                                                          children=(SPRMIB, TIMING_PARAMETER_ACCESS_TYPE_2013))
"""Definition (compatible with SIO 14229-1:2013) of
:ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` SubFunction."""

# SID 0x85
DTC_SETTING_TYPE = MappingDataRecord(name="DTCSettingType",
                                     length=7,
                                     values_mapping=DTC_SETTING_TYPE_MAPPING)
"""Definition of `DTCSettingType` Data Record that is part of
:ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` SubFunction."""

CONTROL_DTC_SETTING_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                                 length=8,
                                                 children=(SPRMIB, DTC_SETTING_TYPE))
"""Definition of :ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` SubFunction."""

# SID 0x86
EVENT_2020 = MappingDataRecord(name="event",
                               length=6,
                               values_mapping=EVENT_MAPPING_2020)
"""Definition of `event` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""
EVENT_2013 = MappingDataRecord(name="event",
                               length=6,
                               values_mapping=EVENT_MAPPING_2013)
"""Definition of `event` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""


STORAGE_STATE = MappingDataRecord(name="storageState",
                                  length=1,
                                  values_mapping=STORAGE_STATE_MAPPING)
"""Definition of `storageState` Data Record that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""

EVENT_TYPE_2020 = RawDataRecord(name="eventType",
                                length=7,
                                children=(STORAGE_STATE, EVENT_2020))
"""Definition of `eventType` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""
EVENT_TYPE_2013 = RawDataRecord(name="eventType",
                                length=7,
                                children=(STORAGE_STATE, EVENT_2013))
"""Definition of `eventType` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""

RESPONSE_ON_EVENT_SUB_FUNCTION_2020 = RawDataRecord(name="SubFunction",
                                                    length=8,
                                                    children=(SPRMIB, EVENT_TYPE_2020))
"""Definition (compatible with SIO 14229-1:2020) of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""
RESPONSE_ON_EVENT_SUB_FUNCTION_2013 = RawDataRecord(name="SubFunction",
                                                    length=8,
                                                    children=(SPRMIB, EVENT_TYPE_2013))
"""Definition (compatible with SIO 14229-1:2013) of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` SubFunction."""

# SID 0x87
LINK_CONTROL_TYPE = MappingDataRecord(name="linkControlType",
                                      length=7,
                                      values_mapping=LINK_CONTROL_TYPE_MAPPING)
"""Definition of `linkControlType` Data Record that is part of
:ref:`LinkControl <knowledge-base-service-link-control>` SubFunction."""

LINK_CONTROL_SUB_FUNCTION = RawDataRecord(name="SubFunction",
                                          length=8,
                                          children=(SPRMIB, LINK_CONTROL_TYPE))
"""Definition of :ref:`LinkControl <knowledge-base-service-link-control>` SubFunction."""

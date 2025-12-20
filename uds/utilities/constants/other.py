"""Other constants used in the project."""

__all__ = [
    # Shared
    "REPEATED_DATA_RECORDS_NUMBER",
    "NO_YES_MAPPING",
    "COMPRESSION_METHOD_MAPPING", "ENCRYPTION_METHOD_MAPPING",
    # SID 0x11
    "POWER_DOWN_TIME_MAPPING",
    # SID 0x24
    "EXPONENT_BIT_LENGTH", "MANTISSA_BIT_LENGTH",
    "SCALING_BYTE_TYPE_MAPPING",
    "FORMULA_IDENTIFIER_MAPPING",
    "UNIT_OR_FORMAT_MAPPING",
    "STATE_AND_CONNECTION_TYPE_TYPE_MAPPING", "STATE_AND_CONNECTION_TYPE_DIRECTION_MAPPING",
    "STATE_AND_CONNECTION_TYPE_LEVEL_MAPPING" , "STATE_AND_CONNECTION_TYPE_STATE_MAPPING",
    # SID 0x28
    "MESSAGE_TYPE_MAPPING",
    "NETWORKS_MAPPING",
    "NODE_IDENTIFICATION_NUMBER_MAPPING",
    # SID 0x29
    "AUTHENTICATION_RETURN_PARAMETER_MAPPING",
    # SID 0x2A
    "TRANSMISSION_MODE_MAPPING",
    # SID 0x2F
    "INPUT_OUTPUT_CONTROL_PARAMETER_MAPPING",
    # SID 0x38
    "MODE_OF_OPERATION_MAPPING_2020", "MODE_OF_OPERATION_MAPPING_2013",
    # SID 0x86
    "EVENT_WINDOW_TIME_MAPPING_2020", "EVENT_WINDOW_TIME_MAPPING_2013",
    "COMPARISON_LOGIC_MAPPING",
    "COMPARE_SIGN_MAPPING",
    "TIMER_SCHEDULE_MAPPING_2013",
    # SID 0x87
    "LINK_CONTROL_MODE_IDENTIFIER_MAPPING",
]

from typing import Dict

# Shared
REPEATED_DATA_RECORDS_NUMBER: int = 100  # TODO: remove if possible

NO_YES_MAPPING: Dict[int, str] = {0: "no", 1: "yes"}
"""Generic `no` and `yes` values mapping."""

COMPRESSION_METHOD_MAPPING: Dict[int, str] = {
                                                 0: "no compression",
                                             } | {
                                                 value: f"compression #{value}" for value in range(1, 0x10)
                                             }
"""Values mapping for compressionMethod Data Record that is part of messages for multiple services."""

ENCRYPTION_METHOD_MAPPING: Dict[int, str] = {
                                                0: "no encryption",
                                            } | {
                                                value: f"encryption #{value}" for value in range(1, 0x10)
                                            }
"""Values mapping for encryptingMethod Data Record that is part of messages for multiple services."""

# SID 0x11
POWER_DOWN_TIME_MAPPING: Dict[int, str] = {
    0xFF: "failure or time unavailable"
}
"""Values mapping for `powerDownTime` Data Record that is part of
:ref:`ECUReset <knowledge-base-service-ecu-reset>` message."""

# SID 0x24
EXPONENT_BIT_LENGTH: int = 4
"""Number of bits used for constant's exponent value by
:ref:`ReadScalingDataByIdentifier service <knowledge-base-service-read-scaling-data-by-identifier>`"""

MANTISSA_BIT_LENGTH: int = 12
"""Number of bits used for constant's mantissa value by
:ref:`ReadScalingDataByIdentifier service <knowledge-base-service-read-scaling-data-by-identifier>`"""

SCALING_BYTE_TYPE_MAPPING: Dict[int, str] = {
    0x0: "unSignedNumeric",
    0x1: "signedNumeric",
    0x2: "bitMappedReportedWithOutMask",
    0x3: "bitMappedReportedWithMask",
    0x4: "BinaryCodedDecimal",
    0x5: "stateEncodedVariable",
    0x6: "ASCII",
    0x7: "signedFloatingPoint",
    0x8: "packet",
    0x9: "formula",
    0xA: "unit/format",
    0xB: "stateAndConnectionType",
}
"""Values mapping for (scalingByte) `type` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

FORMULA_IDENTIFIER_MAPPING: Dict[int, str] = {
    0x00: "y = C0 * x + C1",
    0x01: "y = C0 * (x + C1)",
    0x02: "y = C0 / (x + C1) + C2",
    0x03: "y = x / C0 + C1",
    0x04: "y = (x + C0) / C1",
    0x05: "y = (x + C0) / C1 + C2",
    0x06: "y = C0 * x",
    0x07: "y = x / C0",
    0x08: "y = x + C0",
    0x09: "y = x * C0 / C1",
}
"""Values mapping for `formulaIdentifier` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

UNIT_OR_FORMAT_MAPPING: Dict[int, str] = {
    0x00: "No unit, no prefix",
    0x01: "Meter [m] - length",
    0x02: "Foot [ft] - length",
    0x03: "Inch [in] - length",
    0x04: "Yard [yd] - length",
    0x05: "Mile (English) [mi] - length",
    0x06: "Gram [g] - mass",
    0x07: "Ton (metric) [t] - mass",
    0x08: "Second [s] - time",
    0x09: "Minute [min] - time",
    0x0A: "Hour [h] - time",
    0x0B: "Day [d] - time",
    0x0C: "Year [y] - time",
    0x0D: "Ampere [A] - current",
    0x0E: "Volt [V] - voltage",
    0x0F: "Coulomb [C] - electric charge",
    0x10: "Ohm [Ω] - resistance",
    0x11: "Farad [F] - capacitance",
    0x12: "Henry [H] - inductance",
    0x13: "Siemens [S] - electric conductance",
    0x14: "Weber [Wb] - magnetic flux",
    0x15: "Tesla [T] - magnetic flux density",
    0x16: "Kelvin [K] - thermodynamic temperature",
    0x17: "Celsius [°C] - thermodynamic temperature",
    0x18: "Fahrenheit [°F] - thermodynamic temperature",
    0x19: "Candela [cd] - luminous intensity",
    0x1A: "Radian [rad] - plane angle",
    0x1B: "Degree [°] - plane angle",
    0x1C: "Hertz [Hz] - frequency",
    0x1D: "Joule [J] - energy",
    0x1E: "Newton [N] - force",
    0x1F: "Kilopond [kp] - force",
    0x20: "Pound force [lbf] - force",
    0x21: "Watt [W] - power",
    0x22: "Horse power (metric) [hk] - power",
    0x23: "Horse power (UK and US) [hp] - power",
    0x24: "Pascal [Pa] - pressure",
    0x25: "Bar [bar] - pressure",
    0x26: "Atmosphere [atm] - pressure",
    0x27: "Pound force per square inch [psi] - pressure",
    0x28: "Becquerel [Bq] - radioactivity",
    0x29: "Lumen [Lm] - light flux",
    0x2A: "Lux [lx] - illuminance",
    0x2B: "Litre [l] - volume",
    0x2C: "Gallon (British) - volume",
    0x2D: "Gallon (US liq) - volume",
    0x2E: "Cubic inch [cu in] - volume",
    0x2F: "Meter per second [m/s] - speed",
    0x30: "Kilometer per hour [km/h] - speed",
    0x31: "Mile per hour [mph] - speed",
    0x32: "Revolutions per second [rps] - angular velocity",
    0x33: "Revolutions per minute [rpm] - angular velocity",
    0x34: "Counts",
    0x35: "Percent [%]",
    0x36: "Milligram per stroke [mg/stroke] - mass per engine stroke",
    0x37: "Meter per square second [m/s2] - acceleration",
    0x38: "Newton meter [Nm] - moment (e.g. torsion moment)",
    0x39: "Litre per minute [l/min] - flow",
    0x3A: "Watt per square meter [W/m2] - intensity",
    0x3B: "Bar per second [bar/s] - pressure change",
    0x3C: "Radians per second [rad/s] - angular velocity",
    0x3D: "Radians per square second [rad/s2] - angular acceleration",
    0x3E: "Kilogram per square meter [kg/m2]",
    0x40: "Exa (prefix) [E] - 10^18",
    0x41: "Peta (prefix) [P] - 10^15",
    0x42: "Tera (prefix) [T] - 10^12",
    0x43: "Giga (prefix) [G] - 10^9",
    0x44: "Mega (prefix) [M] - 10^6",
    0x45: "Kilo (prefix) [k] - 10^3",
    0x46: "Hecto (prefix) [h] - 10^2",
    0x47: "Deca (prefix) [da] - 10",
    0x48: "Deci (prefix) [d] - 10^-1",
    0x49: "Centi (prefix) [c] - 10^-2",
    0x4A: "Milli (prefix) [m] - 10^-3",
    0x4B: "Micro (prefix) [μ] - 10^-6",
    0x4C: "Nano (prefix) [n] - 10^-9",
    0x4D: "Pico (prefix) [p] - 10^-12",
    0x4E: "Femto (prefix) [f] - 10^-15",
    0x4F: "Atto (prefix) [a] - 10^-18",
    0x50: "Year/Month/Day - date",
    0x51: "Day/Month/Year - date",
    0x52: "Month/Day/Year - date",
    0x53: "Week - calendar week",
    0x54: "UTC Hour/Minute/Second - time",
    0x55: "Hour/Minute/Second - time",
    0x56: "Second/Minute/Hour/Day/Month/Year - date and time",
    0x57: "Second/Minute/Hour/Day/Month/Year/Local minute offset/Local hour offset "
          "- date and time",
    0x58: "Second/Minute/Hour/Month/Day/Year - date and time",
    0x59: "Second/Minute/Hour/Month/Day/Year/Local minute offset/Local hour offset "
          "- date and time",
}
"""Values mapping for `unit/format` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

STATE_AND_CONNECTION_TYPE_TYPE_MAPPING: Dict[int, str] = {
    0x0: "Internal signal",
    0x1: "2 states (low by default)",
    0x2: "2 states (high by default)",
    0x3: "3 states",
}
"""Values mapping for (stateAndConnectionType) `type` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

STATE_AND_CONNECTION_TYPE_DIRECTION_MAPPING: Dict[int, str] = {
    0x0: "Input signal",
    0x1: "Output signal",
}
"""Values mapping for (stateAndConnectionType) `direction` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

STATE_AND_CONNECTION_TYPE_LEVEL_MAPPING: Dict[int, str] = {
    0x0: "Signal at low level (ground)",
    0x1: "Signal at middle level (between ground and +)",
    0x2: "Signal at high level (+)",
}
"""Values mapping for (stateAndConnectionType) `level` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

STATE_AND_CONNECTION_TYPE_STATE_MAPPING: Dict[int, str] = {
    0x0: "Not Active",
    0x1: "Active, function 1",
    0x2: "Error detected",
    0x3: "Not available",
    0x4: "Active, function 2",
}
"""Values mapping for (stateAndConnectionType) `state` Data Record that is part of
:ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` message."""

# SID 0x28
MESSAGE_TYPE_MAPPING: Dict[int, str] = {
    0: "reserved",
    1: "normalCommunicationMessages",
    2: "networkManagementCommunicationMessages",
    3: "networkManagementCommunicationMessages and normalCommunicationMessages",
}
"""Values mapping for `messagesType` Data Record that is part of
:ref:`CommunicationControl <knowledge-base-service-communication-control>` message."""

NETWORKS_MAPPING: Dict[int, str] = {
                                       0x0: "all connected networks",
                                       0xF: "network on which this request is received",
                                   } | {
                                       raw_value: f"subnet {raw_value}" for raw_value in range(1, 0xF)
                                   }
"""Values mapping for `networks` Data Record that is part of
:ref:`CommunicationControl <knowledge-base-service-communication-control>` message."""

NODE_IDENTIFICATION_NUMBER_MAPPING: Dict[int, str] = {
    0: "reserved"
}
"""Values mapping for `nodeIdentificationNumber` Data Record that is part of
:ref:`CommunicationControl <knowledge-base-service-communication-control>` message."""

# SID 0x29
AUTHENTICATION_RETURN_PARAMETER_MAPPING: Dict[int, str] = {
    0x00: "RequestAccepted",
    0x01: "GeneralReject",
    0x02: "AuthenticationConfiguration",
    0x03: "AuthenticationConfiguration ACR with asymmetric cryptography",
    0x04: "AuthenticationConfiguration ACR with symmetric cryptography",
    0x10: "DeAuthentication successful",
    0x11: "CertificateVerified, OwnershipVerificationNecessary",
    0x12: "OwnershipVerified, AuthenticationComplete",
    0x13: "CertificateVerified",
}
"""Values mapping for `authenticationReturnParameter` Data Record that is part of
:ref:`Authentication <knowledge-base-service-authentication>` message."""

# SID 0x2A
TRANSMISSION_MODE_MAPPING: Dict[int, str] = {
    0x01: "sendAtSlowRate",
    0x02: "sendAtMediumRate",
    0x03: "sendAtFastRate",
    0x04: "stopSending",
}
"""Values mapping for `transmissionMode` Data Record that is part of
:ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>` message."""

# SID 0x2F
INPUT_OUTPUT_CONTROL_PARAMETER_MAPPING: Dict[int, str] = {
    0x00: "returnControlToECU",
    0x01: "resetToDefault",
    0x02: "freezeCurrentState",
    0x03: "shortTermAdjustment",
}
"""Values mapping for `inputOutputControlParameter` Data Record that is part of
:ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` message."""

# SID 0x38
MODE_OF_OPERATION_MAPPING_2020: Dict[int, str] = {
    0x01: "AddFile",
    0x02: "DeleteFile",
    0x03: "ReplaceFile",
    0x04: "ReadFile",
    0x05: "ReadDir",
    0x06: "ResumeFile",
}
"""Values mapping for `modeOfOperation` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` message."""
MODE_OF_OPERATION_MAPPING_2013: Dict[int, str] = {
    0x01: "AddFile",
    0x02: "DeleteFile",
    0x03: "ReplaceFile",
    0x04: "ReadFile",
    0x05: "ReadDir",
}
"""Values mapping for `modeOfOperation` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` message."""

# SID 0x86
EVENT_WINDOW_TIME_MAPPING_2020: Dict[int, str] = {
    0x02: "infiniteTimeToResponse",
    0x03: "shortEventWindowTime",
    0x04: "mediumEventWindowTime",
    0x05: "longEventWindowTime",
    0x06: "powerWindowTime",
    0x07: "ignitionWindowTime",
    0x08: "manufacturerTriggerEventWindowTime"
}
"""Values mapping for `eventWindowTime` Data Record (compatible with ISO 14229-1:2020) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` message."""
EVENT_WINDOW_TIME_MAPPING_2013: Dict[int, str] = {
    0x02: "infiniteTimeToResponse"
}
"""Values mapping for `eventWindowTime` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` message."""

COMPARISON_LOGIC_MAPPING: Dict[int, str] = {
    0x01: "<",
    0x02: ">",
    0x03: "=",
    0x04: "<>",
}
"""Values mapping for `Comparison logic` Data Record that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` message."""

COMPARE_SIGN_MAPPING: Dict[int, str] = {
    0: "Comparison without sign",
    1: "Comparison with sign",
}
"""Values mapping for `Compare Sign` Data Record that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` message."""

TIMER_SCHEDULE_MAPPING_2013: Dict[int, str] = {
    0x01: "Slow rate",
    0x02: "Medium rate",
    0x03: "Fast rate",
}
"""Values mapping for `Timer schedule` Data Record (compatible with ISO 14229-1:2013) that is part of
:ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` message."""

# SID 0x87
LINK_CONTROL_MODE_IDENTIFIER_MAPPING: Dict[int, str] = {
    0x01: "PC9600Baud",
    0x02: "PC19200Baud",
    0x03: "PC38400Baud",
    0x04: "PC57600Baud",
    0x05: "PC115200Baud",
    0x10: "CAN125000Baud",
    0x11: "CAN250000Baud",
    0x12: "CAN500000Baud",
    0x13: "CAN1000000Baud",
    0x20: "ProgrammingSetup",
}
"""Values mapping for `linkControlModeIdentifier` Data Record that is part of
:ref:`LinkControl <knowledge-base-service-link-control>` message."""

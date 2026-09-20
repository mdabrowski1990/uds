"""Remaining Data Records definitions."""

__all__ = [
    # Shared
    "RESERVED_BIT", "RESERVED_2BITS", "RESERVED_4BITS", "RESERVED_9BITS",
    "DATA",
    "ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER", "MEMORY_ADDRESS_LENGTH", "MEMORY_SIZE_LENGTH",
    "DATA_FORMAT_IDENTIFIER", "COMPRESSION_METHOD", "ENCRYPTION_METHOD",
    "LENGTH_FORMAT_IDENTIFIER", "MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER",
    "TRANSFER_REQUEST_PARAMETER", "TRANSFER_RESPONSE_PARAMETER",
    # SID 0x10
    "SESSION_PARAMETER_RECORD", "P2_SERVER_MAX", "P2_EXT_SERVER_MAX",
    # SID 0x11
    "POWER_DOWN_TIME",
    # SID 0x14
    "OPTIONAL_MEMORY_SELECTION",
    # SID 0x19
    "MEMORY_SELECTION",
    # SID 0x22
    "ACTIVE_DIAGNOSTIC_SESSION",
    # SID 0x24
    "SCALING_BYTE_TYPE",
    "SCALING_BYTE_LENGTH",
    "FORMULA_IDENTIFIER",
    "EXPONENT", "MANTISSA",
    "UNIT_OR_FORMAT",
    "STATE_AND_CONNECTION_TYPE_TYPE", "STATE_AND_CONNECTION_TYPE_DIRECTION",
    "STATE_AND_CONNECTION_TYPE_LEVEL", "STATE_AND_CONNECTION_TYPE_STATE",
    "STATE_AND_CONNECTION_TYPE",
    # SID 0x27
    "SECURITY_ACCESS_DATA",
    "SECURITY_SEED",
    "SECURITY_KEY",
    # SID 0x28
    "COMMUNICATION_TYPE", "MESSAGES_TYPE", "NETWORKS",
    "NODE_IDENTIFICATION_NUMBER",
    # SID 0x29
    "CERTIFICATE_CLIENT_LENGTH", "CERTIFICATE_SERVER_LENGTH", "CERTIFICATE_DATA_LENGTH",
    "CHALLENGE_CLIENT_LENGTH", "CHALLENGE_SERVER_LENGTH",
    "PROOF_OF_OWNERSHIP_CLIENT_LENGTH", "PROOF_OF_OWNERSHIP_SERVER_LENGTH",
    "EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH", "EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH",
    "NEEDED_ADDITIONAL_PARAMETER_LENGTH", "ADDITIONAL_PARAMETER_LENGTH",
    "SESSION_KEY_INFO_LENGTH",
    "COMMUNICATION_CONFIGURATION",
    "CERTIFICATE_EVALUATION",
    "ALGORITHM_INDICATOR",
    "AUTHENTICATION_RETURN_PARAMETER",
    # SID 0x2A
    "TRANSMISSION_MODE",
    # SID 0x2F
    "INPUT_OUTPUT_CONTROL_PARAMETER",
    # SID 0x36
    "BLOCK_SEQUENCE_COUNTER",
    # SID 0x38
    "MODE_OF_OPERATION_2020", "MODE_OF_OPERATION_2013",
    "FILE_AND_PATH_NAME_LENGTH",
    "FILE_SIZE_PARAMETER_LENGTH",
    "FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH",
    "LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER",
    "FILE_POSITION",
    # SID 0x83
    "TIMING_PARAMETER_REQUEST_RECORD_2013", "TIMING_PARAMETER_RESPONSE_RECORD_2013",
    # SID 0x84
    "SECURITY_DATA_REQUEST_RECORD_2013", "SECURITY_DATA_RESPONSE_RECORD_2013",
    "ADMINISTRATIVE_PARAMETER",
    "IS_SIGNATURE_REQUESTED",
    "IS_MESSAGE_SIGNED",
    "IS_MESSAGE_ENCRYPTED",
    "IS_PRE_ESTABLISHED_KEY_USED",
    "IS_REQUEST_MESSAGE",
    "SIGNATURE_ENCRYPTION_CALCULATION",
    "SIGNATURE_LENGTH",
    "ANTI_REPLAY_COUNTER",
    "INTERNAL_SID", "INTERNAL_RSID",
    "INTERNAL_REQUEST_PARAMETERS", "INTERNAL_RESPONSE_PARAMETERS",
    # SID 0x85
    "DTC_SETTING_CONTROL_OPTION_RECORD",
    # SID 0x86
    "NUMBER_OF_IDENTIFIED_EVENTS", "NUMBER_OF_ACTIVATED_EVENTS",
    "COMPARISON_LOGIC", "COMPARE_VALUE", "HYSTERESIS_VALUE",
    "COMPARE_SIGN", "BITS_NUMBER", "BIT_OFFSET", "LOCALIZATION",
    # SID 0x87
    "LINK_RECORD",
    "LINK_CONTROL_MODE_IDENTIFIER",
]


from uds.utilities import (
    AUTHENTICATION_RETURN_PARAMETER_MAPPING,
    COMPARE_SIGN_MAPPING,
    COMPARISON_LOGIC_MAPPING,
    COMPRESSION_METHOD_MAPPING,
    DIAGNOSTIC_SESSION_TYPE_MAPPING,
    ENCRYPTION_METHOD_MAPPING,
    EXPONENT_BIT_LENGTH,
    FORMULA_IDENTIFIER_MAPPING,
    INPUT_OUTPUT_CONTROL_PARAMETER_MAPPING,
    LINK_CONTROL_MODE_IDENTIFIER_MAPPING,
    MANTISSA_BIT_LENGTH,
    MESSAGE_TYPE_MAPPING,
    MODE_OF_OPERATION_MAPPING_2013,
    MODE_OF_OPERATION_MAPPING_2020,
    NETWORKS_MAPPING,
    NO_YES_MAPPING,
    NODE_IDENTIFICATION_NUMBER_MAPPING,
    POWER_DOWN_TIME_MAPPING,
    SCALING_BYTE_TYPE_MAPPING,
    STATE_AND_CONNECTION_TYPE_DIRECTION_MAPPING,
    STATE_AND_CONNECTION_TYPE_LEVEL_MAPPING,
    STATE_AND_CONNECTION_TYPE_STATE_MAPPING,
    STATE_AND_CONNECTION_TYPE_TYPE_MAPPING,
    TIMER_SCHEDULE_MAPPING_2013,
    TRANSMISSION_MODE_MAPPING,
    UNIT_OR_FORMAT_MAPPING,
    get_signed_value_decoding_formula,
    get_signed_value_encoding_formula,
)

from ..data_record import (
    CustomFormulaDataRecord,
    LinearFormulaDataRecord,
    MappingAndLinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
)

# Shared

RESERVED_BIT = RawDataRecord(name="reserved",
                             length=1)
"""Definition of 1-bit long reserved Data Record."""
RESERVED_2BITS = RawDataRecord(name="reserved",
                               length=2)
"""Definition of 2-bit long reserved Data Record."""
RESERVED_4BITS = RawDataRecord(name="reserved",
                               length=4)
"""Definition of 4-bit long reserved Data Record."""
RESERVED_9BITS = RawDataRecord(name="reserved-9bits",
                               length=9)
"""Definition of 9-bit long reserved Data Record."""

DATA = RawDataRecord(name="data",
                     length=8,
                     min_occurrences=1,
                     max_occurrences=None)
"""Definition of Data Record with data of unknown length."""

MEMORY_ADDRESS_LENGTH = RawDataRecord(name="memoryAddressLength",
                                      length=4,
                                      unit="bytes")
"""Definition of `memoryAddressLength` Data Record."""
MEMORY_SIZE_LENGTH = RawDataRecord(name="memorySizeLength",
                                   length=4,
                                   unit="bytes")
"""Definition of `memorySizeLength` Data Record."""
ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER = RawDataRecord(name="addressAndLengthFormatIdentifier",
                                                     length=8,
                                                     children=(MEMORY_SIZE_LENGTH, MEMORY_ADDRESS_LENGTH))
"""Definition of `addressAndLengthFormatIdentifier` Data Record."""

COMPRESSION_METHOD = MappingDataRecord(name="compressionMethod",
                                       length=4,
                                       values_mapping=COMPRESSION_METHOD_MAPPING)
"""Definition of `compressionMethod` Data Record."""
ENCRYPTION_METHOD = MappingDataRecord(name="encryptingMethod",
                                      length=4,
                                      values_mapping=ENCRYPTION_METHOD_MAPPING)
"""Definition of `encryptingMethod` Data Record."""
DATA_FORMAT_IDENTIFIER = RawDataRecord(name="dataFormatIdentifier",
                                       length=8,
                                       children=(COMPRESSION_METHOD, ENCRYPTION_METHOD))
"""Definition of `dataFormatIdentifier` Data Record."""

MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER = RawDataRecord(name="maxNumberOfBlockLengthBytesNumber",
                                                        length=4,
                                                        unit="bytes")
"""Definition of `maxNumberOfBlockLengthBytesNumber` Data Record."""
LENGTH_FORMAT_IDENTIFIER = RawDataRecord(name="lengthFormatIdentifier",
                                         length=8,
                                         children=(MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER, RESERVED_4BITS))
"""Definition of `lengthFormatIdentifier` Data Record."""

TRANSFER_REQUEST_PARAMETER = RawDataRecord(name="transferRequestParameter",
                                           length=8,
                                           min_occurrences=0,
                                           max_occurrences=None)
"""Definition of `transferRequestParameter` Data Record."""
TRANSFER_RESPONSE_PARAMETER = RawDataRecord(name="transferResponseParameter",
                                            length=8,
                                            min_occurrences=0,
                                            max_occurrences=None)
"""Definition of `transferResponseParameter` Data Record."""

# SID 0x10

P2_SERVER_MAX = LinearFormulaDataRecord(name="P2Server_max",
                                        length=16,
                                        factor=1,
                                        offset=0,
                                        unit="ms")
"""Definition of `P2Server_max` Data Record."""
P2_EXT_SERVER_MAX = LinearFormulaDataRecord(name="P2*Server_max",
                                            length=16,
                                            factor=10,
                                            offset=0,
                                            unit="ms")
"""Definition of `P2*Server_max` Data Record."""
SESSION_PARAMETER_RECORD = RawDataRecord(name="sessionParameterRecord",
                                         length=32,
                                         children=(P2_SERVER_MAX, P2_EXT_SERVER_MAX))
"""Definition of `sessionParameterRecord` Data Record."""

# SID 0x11

POWER_DOWN_TIME = MappingAndLinearFormulaDataRecord(name="powerDownTime",
                                                    length=8,
                                                    values_mapping=POWER_DOWN_TIME_MAPPING,
                                                    factor=1,
                                                    offset=0,
                                                    unit="s")
"""Definition of `powerDownTime` Data Record."""

# SID 0x14

OPTIONAL_MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                          length=8,
                                          min_occurrences=0,
                                          max_occurrences=1)
"""Definition of optional `MemorySelection` Data Record."""

# SID 0x19

MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                 length=8)
"""Definition of `MemorySelection` Data Record."""

# SID 0x22

ACTIVE_DIAGNOSTIC_SESSION = MappingDataRecord(name="ActiveDiagnosticSession",
                                              values_mapping=DIAGNOSTIC_SESSION_TYPE_MAPPING,
                                              length=7)
"""Definition of `ActiveDiagnosticSession` Data Record."""

# SID 0x24

SCALING_BYTE_TYPE = MappingDataRecord(name="type",
                                      length=4,
                                      values_mapping=SCALING_BYTE_TYPE_MAPPING)
"""Definition of (scaling byte) `type` Data Record."""

SCALING_BYTE_LENGTH = RawDataRecord(name="numberOfBytesOfParameter",
                                    length=4,
                                    unit="bytes")
"""Definition of `numberOfBytesOfParameter` Data Record."""

FORMULA_IDENTIFIER = MappingDataRecord(name="formulaIdentifier",
                                       length=8,
                                       values_mapping=FORMULA_IDENTIFIER_MAPPING)
"""Definition of `formulaIdentifier` Data Record."""

EXPONENT = CustomFormulaDataRecord(name="Exponent",
                                   length=EXPONENT_BIT_LENGTH,
                                   encoding_formula=get_signed_value_encoding_formula(EXPONENT_BIT_LENGTH),
                                   decoding_formula=get_signed_value_decoding_formula(EXPONENT_BIT_LENGTH))
"""Definition of `Exponent` Data Record."""

MANTISSA = CustomFormulaDataRecord(name="Mantissa",
                                   length=MANTISSA_BIT_LENGTH,
                                   encoding_formula=get_signed_value_encoding_formula(MANTISSA_BIT_LENGTH),
                                   decoding_formula=get_signed_value_decoding_formula(MANTISSA_BIT_LENGTH))
"""Definition of `Mantissa` Data Record."""

UNIT_OR_FORMAT = MappingDataRecord(name="unit/format",
                                   length=8,
                                   values_mapping=UNIT_OR_FORMAT_MAPPING)
"""Definition of `unit/format` Data Record."""

STATE_AND_CONNECTION_TYPE_TYPE = MappingDataRecord(name="type",
                                                   length=2,
                                                   values_mapping=STATE_AND_CONNECTION_TYPE_TYPE_MAPPING)
"""Definition of (state and connection type) `type` Data Record."""

STATE_AND_CONNECTION_TYPE_DIRECTION = MappingDataRecord(name="direction",
                                                        length=1,
                                                        values_mapping=STATE_AND_CONNECTION_TYPE_DIRECTION_MAPPING)
"""Definition of (state and connection type) `direction` Data Record."""

STATE_AND_CONNECTION_TYPE_LEVEL = MappingDataRecord(name="level",
                                                    length=2,
                                                    values_mapping=STATE_AND_CONNECTION_TYPE_LEVEL_MAPPING)
"""Definition of (state and connection type) `level` Data Record."""

STATE_AND_CONNECTION_TYPE_STATE = MappingDataRecord(name="state",
                                                    length=3,
                                                    values_mapping=STATE_AND_CONNECTION_TYPE_STATE_MAPPING)
"""Definition of (state and connection type) `state` Data Record."""

STATE_AND_CONNECTION_TYPE = RawDataRecord(name="stateAndConnectionType",
                                          length=8,
                                          children=(STATE_AND_CONNECTION_TYPE_TYPE,
                                                    STATE_AND_CONNECTION_TYPE_DIRECTION,
                                                    STATE_AND_CONNECTION_TYPE_LEVEL,
                                                    STATE_AND_CONNECTION_TYPE_STATE))
"""Definition of `stateAndConnectionType` Data Record."""

# SID 0x27
SECURITY_ACCESS_DATA = RawDataRecord(name="securityAccessData",
                                     length=8,
                                     min_occurrences=0,
                                     max_occurrences=None)
"""Definition of `securityAccessData` Data Record."""

SECURITY_SEED = RawDataRecord(name="securitySeed",
                              length=8,
                              min_occurrences=1,
                              max_occurrences=None)
"""Definition of `securitySeed` Data Record."""

SECURITY_KEY = RawDataRecord(name="securityKey",
                             length=8,
                             min_occurrences=1,
                             max_occurrences=None)
"""Definition of `securityKey` Data Record."""

# SID 0x28

MESSAGES_TYPE = MappingDataRecord(name="messagesType",
                                  length=2,
                                  values_mapping=MESSAGE_TYPE_MAPPING)
"""Definition of `messagesType` Data Record."""

NETWORKS = MappingDataRecord(name="networks",
                                  length=4,
                                  values_mapping=NETWORKS_MAPPING)
"""Definition of `networks` Data Record."""

COMMUNICATION_TYPE = RawDataRecord(name="communicationType",
                                   length=8,
                                   children=(MESSAGES_TYPE, RESERVED_2BITS, NETWORKS))
"""Definition of `communicationType` Data Record."""

NODE_IDENTIFICATION_NUMBER = MappingDataRecord(name="nodeIdentificationNumber",
                                               length=16,
                                               values_mapping=NODE_IDENTIFICATION_NUMBER_MAPPING)
"""Definition of `nodeIdentificationNumber` Data Record."""

# SID 0x29

CERTIFICATE_CLIENT_LENGTH = RawDataRecord(name="lengthOfCertificateClient",
                                          length=16,
                                          unit="bytes")
"""Definition of `lengthOfCertificateClient` Data Record."""

CERTIFICATE_SERVER_LENGTH = RawDataRecord(name="lengthOfCertificateServer",
                                          length=16,
                                          unit="bytes")
"""Definition of `lengthOfCertificateServer` Data Record."""

CERTIFICATE_DATA_LENGTH = RawDataRecord(name="lengthOfCertificateData",
                                        length=16,
                                        unit="bytes")
"""Definition of `lengthOfCertificateData` Data Record."""

CHALLENGE_CLIENT_LENGTH = RawDataRecord(name="lengthOfChallengeClient",
                                        length=16,
                                        unit="bytes")
"""Definition of `lengthOfChallengeClient` Data Record."""

CHALLENGE_SERVER_LENGTH = RawDataRecord(name="lengthOfChallengeServer",
                                        length=16,
                                        unit="bytes")
"""Definition of `lengthOfChallengeServer` Data Record."""

PROOF_OF_OWNERSHIP_CLIENT_LENGTH = RawDataRecord(name="lengthOfProofOfOwnershipClient",
                                                 length=16,
                                                 unit="bytes")
"""Definition of `lengthOfProofOfOwnershipClient` Data Record."""

PROOF_OF_OWNERSHIP_SERVER_LENGTH = RawDataRecord(name="lengthOfProofOfOwnershipServer",
                                                 length=16,
                                                 unit="bytes")
"""Definition of `lengthOfProofOfOwnershipServer` Data Record."""

EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH = RawDataRecord(name="lengthOfEphemeralPublicKeyClient",
                                                   length=16,
                                                   unit="bytes")
"""Definition of `lengthOfEphemeralPublicKeyClient` Data Record."""

EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH = RawDataRecord(name="lengthOfEphemeralPublicKeyServer",
                                                   length=16,
                                                   unit="bytes")
"""Definition of `lengthOfEphemeralPublicKeyServer` Data Record."""

NEEDED_ADDITIONAL_PARAMETER_LENGTH = RawDataRecord(name="lengthOfNeededAdditionalParameter",
                                                   length=16,
                                                   unit="bytes")
"""Definition of `lengthOfNeededAdditionalParameter` Data Record."""

ADDITIONAL_PARAMETER_LENGTH = RawDataRecord(name="lengthOfAdditionalParameter",
                                            length=16,
                                            unit="bytes")
"""Definition of `lengthOfAdditionalParameter` Data Record."""

SESSION_KEY_INFO_LENGTH = RawDataRecord(name="lengthOfSessionKeyInfo",
                                        length=16,
                                        unit="bytes")
"""Definition of `lengthOfSessionKeyInfo` Data Record."""

COMMUNICATION_CONFIGURATION = RawDataRecord(name="communicationConfiguration",
                                            length=8)
"""Definition of `communicationConfiguration` Data Record."""

CERTIFICATE_EVALUATION = RawDataRecord(name="certificateEvaluationId",
                                       length=8)
"""Definition of `certificateEvaluationId` Data Record."""

ALGORITHM_INDICATOR = RawDataRecord(name="algorithmIndicator",
                                    length=8,
                                    min_occurrences=16,
                                    max_occurrences=16)
"""Definition of `algorithmIndicator` Data Record."""

AUTHENTICATION_RETURN_PARAMETER = MappingDataRecord(name="authenticationReturnParameter",
                                                    length=8,
                                                    values_mapping=AUTHENTICATION_RETURN_PARAMETER_MAPPING)
"""Definition of `authenticationReturnParameter` Data Record."""

# SID 0x2A

TRANSMISSION_MODE = MappingDataRecord(name="transmissionMode",
                                      length=8,
                                      values_mapping=TRANSMISSION_MODE_MAPPING)
"""Definition of `transmissionMode` Data Record."""

# SID 0x2F

INPUT_OUTPUT_CONTROL_PARAMETER = MappingDataRecord(name="inputOutputControlParameter",
                                                   length=8,
                                                   values_mapping=INPUT_OUTPUT_CONTROL_PARAMETER_MAPPING)
"""Definition of `inputOutputControlParameter` Data Record."""

# SID 0x36

BLOCK_SEQUENCE_COUNTER = RawDataRecord(name="blockSequenceCounter",
                                       length=8)
"""Definition of `blockSequenceCounter` Data Record."""

# SID 0x38

MODE_OF_OPERATION_2020 = MappingDataRecord(name="modeOfOperation",
                                           length=8,
                                           values_mapping=MODE_OF_OPERATION_MAPPING_2020)
"""Definition of `modeOfOperation` Data Record (compatible with ISO 14229-1:2020)."""
MODE_OF_OPERATION_2013 = MappingDataRecord(name="modeOfOperation",
                                           length=8,
                                           values_mapping=MODE_OF_OPERATION_MAPPING_2013)
"""Definition of `modeOfOperation` Data Record (compatible with ISO 14229-1:2013)."""

FILE_AND_PATH_NAME_LENGTH = RawDataRecord(name="filePathAndNameLength",
                                          length=16,
                                          unit="bytes")
"""Definition of `filePathAndNameLength` Data Record."""

FILE_SIZE_PARAMETER_LENGTH = RawDataRecord(name="fileSizeParameterLength",
                                           length=8,
                                           unit="bytes")
"""Definition of `fileSizeParameterLength` Data Record."""

FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH = RawDataRecord(name="fileSizeOrDirInfoParameterLength",
                                                       length=16,
                                                       unit="bytes")
"""Definition of `fileSizeOrDirInfoParameterLength` Data Record."""

LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER = RawDataRecord(name="lengthFormatIdentifier",
                                                       length=8,
                                                       unit="bytes")
"""Definition of `lengthFormatIdentifier` Data Record."""

FILE_POSITION = RawDataRecord(name="filePosition",
                              length=64)
"""Definition of `filePosition` Data Record."""

# SID 0x83

TIMING_PARAMETER_REQUEST_RECORD_2013 = RawDataRecord(name="TimingParameterRequestRecord",
                                                     length=8,
                                                     min_occurrences=1,
                                                     max_occurrences=None)
"""Definition of `TimingParameterRequestRecord` Data Record (compatible with ISO 14229-1:2013)."""

TIMING_PARAMETER_RESPONSE_RECORD_2013 = RawDataRecord(name="TimingParameterResponseRecord",
                                                      length=8,
                                                      min_occurrences=1,
                                                      max_occurrences=None)
"""Definition of `TimingParameterResponseRecord` Data Record (compatible with ISO 14229-1:2013)."""

# SID 0x84

SECURITY_DATA_REQUEST_RECORD_2013 = RawDataRecord(name="securityDataRequestRecord",
                                                  length=8,
                                                  min_occurrences=1,
                                                  max_occurrences=None)
"""Definition of `securityDataRequestRecord` Data Record (compatible with ISO 14229-1:2013)."""

SECURITY_DATA_RESPONSE_RECORD_2013 = RawDataRecord(name="securityDataResponseRecord",
                                                   length=8,
                                                   min_occurrences=1,
                                                   max_occurrences=None)
"""Definition of `securityDataResponseRecord` Data Record (compatible with ISO 14229-1:2013)."""

IS_SIGNATURE_REQUESTED = MappingDataRecord(name="Signature on the response is requested.",
                                           length=1,
                                           values_mapping=NO_YES_MAPPING)
"""Definition of `Signature on the response is requested.` Data Record."""

IS_MESSAGE_SIGNED = MappingDataRecord(name="Message is signed.",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
"""Definition of `Message is signed.` Data Record."""

IS_MESSAGE_ENCRYPTED = MappingDataRecord(name="Message is encrypted.",
                                         length=1,
                                         values_mapping=NO_YES_MAPPING)
"""Definition of `Message is encrypted.` Data Record."""

IS_PRE_ESTABLISHED_KEY_USED = MappingDataRecord(name="A pre-established key is used.",
                                                length=1,
                                                values_mapping=NO_YES_MAPPING)
"""Definition of `A pre-established key is used.` Data Record."""

IS_REQUEST_MESSAGE = MappingDataRecord(name="Message is request message.",
                                       length=1,
                                       values_mapping=NO_YES_MAPPING)
"""Definition of `Message is request message.` Data Record."""

ADMINISTRATIVE_PARAMETER = RawDataRecord(name="Administrative Parameter",
                                         length=16,
                                         children=(RESERVED_9BITS,
                                                   IS_SIGNATURE_REQUESTED,
                                                   IS_MESSAGE_SIGNED,
                                                   IS_MESSAGE_ENCRYPTED,
                                                   IS_PRE_ESTABLISHED_KEY_USED,
                                                   RESERVED_2BITS,
                                                   IS_REQUEST_MESSAGE))
"""Definition of `Administrative Parameter` Data Record."""

SIGNATURE_ENCRYPTION_CALCULATION = RawDataRecord(name="Signature/Encryption Calculation",
                                                 length=8)
"""Definition of `Signature/Encryption Calculation` Data Record."""

SIGNATURE_LENGTH = RawDataRecord(name="Signature Length",
                                 length=16,
                                 unit="bytes")
"""Definition of `Signature Length` Data Record."""

ANTI_REPLAY_COUNTER = RawDataRecord(name="Anti-replay Counter",
                                    length=16)
"""Definition of `Anti-replay Counter` Data Record."""

INTERNAL_SID = RawDataRecord(name="Internal Message Service Request ID",
                             length=8)
"""Definition of `Internal Message Service Request ID` Data Record."""

INTERNAL_RSID = RawDataRecord(name="Internal Message Service Response ID",
                              length=8)
"""Definition of `Internal Message Service Response ID` Data Record."""

INTERNAL_REQUEST_PARAMETERS = RawDataRecord(name="Service Specific Parameters",
                                            length=8,
                                            min_occurrences=0,
                                            max_occurrences=None)
"""Definition of `Service Specific Parameters` Data Record."""

INTERNAL_RESPONSE_PARAMETERS = RawDataRecord(name="Response Specific Parameters",
                                             length=8,
                                             min_occurrences=0,
                                             max_occurrences=None)
"""Definition of `Response Specific Parameters` Data Record."""

# SID 0x85

DTC_SETTING_CONTROL_OPTION_RECORD = RawDataRecord(name="DTCSettingControlOptionRecord",
                                                  length=8,
                                                  min_occurrences=0,
                                                  max_occurrences=None)
"""Definition of `DTCSettingControlOptionRecord` Data Record."""

# SID 0x86

NUMBER_OF_IDENTIFIED_EVENTS = RawDataRecord(name="numberOfIdentifiedEvents",
                                            length=8)
"""Definition of `numberOfIdentifiedEvents` Data Record."""

NUMBER_OF_ACTIVATED_EVENTS = RawDataRecord(name="numberOfActivatedEvents",
                                           length=8)
"""Definition of `numberOfActivatedEvents` Data Record."""

COMPARISON_LOGIC = MappingDataRecord(name="Comparison logic",
                                     length=8,
                                     values_mapping=COMPARISON_LOGIC_MAPPING)
"""Definition of `Comparison logic` Data Record."""

COMPARE_VALUE = RawDataRecord(name="Compare Value",
                              length=32)
"""Definition of `Compare Value` Data Record."""

HYSTERESIS_VALUE = RawDataRecord(name="Hysteresis Value",
                                 length=8)
"""Definition of `Hysteresis Value` Data Record."""

COMPARE_SIGN = MappingDataRecord(name="Compare Sign",
                                 length=1,
                                 values_mapping=COMPARE_SIGN_MAPPING)
"""Definition of `Compare Sign` Data Record."""

BITS_NUMBER = CustomFormulaDataRecord(name="Bits Number",
                                      length=5,
                                      encoding_formula=lambda physical_value: physical_value % 32,
                                      decoding_formula=lambda raw_value: 32 if raw_value == 0 else raw_value,
                                      unit="bits")
"""Definition of `Bits Number` Data Record."""

BIT_OFFSET = RawDataRecord(name="Bit Offset",
                           length=10,
                           unit="bits")
"""Definition of `Bit Offset` Data Record."""

LOCALIZATION = RawDataRecord(name="Localization",
                             length=16,
                             children=(COMPARE_SIGN,
                                       BITS_NUMBER,
                                       BIT_OFFSET))
"""Definition of `Localization` Data Record."""

TIMER_SCHEDULE_2013 = MappingDataRecord(name="Timer schedule",
                                        length=8,
                                        values_mapping=TIMER_SCHEDULE_MAPPING_2013)
"""Definition of `Timer schedule` Data Record (compatible with ISO 14229-1:2013)."""

# SID 0x87

LINK_CONTROL_MODE_IDENTIFIER = MappingDataRecord(name="linkControlModeIdentifier",
                                                 length=8,
                                                 values_mapping=LINK_CONTROL_MODE_IDENTIFIER_MAPPING)
"""Definition of `linkControlModeIdentifier` Data Record."""

LINK_RECORD = RawDataRecord(name="linkRecord",
                            length=24)
"""Definition of `linkRecord` Data Record."""

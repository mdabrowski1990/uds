"""Remaining Data Records definitions."""  # pylint: disable=too-many-lines

__all__ = [
    # Shared
    "RESERVED_BIT",
    "DATA",
    "ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER",
    "DATA_FORMAT_IDENTIFIER", "LENGTH_FORMAT_IDENTIFIER",
    "TRANSFER_REQUEST_PARAMETER", "TRANSFER_RESPONSE_PARAMETER",
    # SID 0x10
    "P2_SERVER_MAX", "P2_EXT_SERVER_MAX", "SESSION_PARAMETER_RECORD",
    # SID 0x11
    "POWER_DOWN_TIME", "CONDITIONAL_POWER_DOWN_TIME",
    # SID 0x14
    "OPTIONAL_MEMORY_SELECTION",
    # SID 0x19
    "MEMORY_SELECTION",
    # SID 0x22
    "ACTIVE_DIAGNOSTIC_SESSION",
    # SID 0x29
    "COMMUNICATION_CONFIGURATION", "CERTIFICATE_EVALUATION", "ALGORITHM_INDICATOR", "AUTHENTICATION_RETURN_PARAMETER",
    "CERTIFICATE_CLIENT_LENGTH",
    "CERTIFICATE_SERVER_LENGTH",
    "CERTIFICATE_DATA_LENGTH",
    "CHALLENGE_CLIENT_LENGTH",
    "CHALLENGE_SERVER_LENGTH",
    "PROOF_OF_OWNERSHIP_CLIENT_LENGTH",
    "PROOF_OF_OWNERSHIP_SERVER_LENGTH",
    "EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH",
    "EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH",
    "SESSION_KEY_INFO_LENGTH",
    "ADDITIONAL_PARAMETER_LENGTH",
    "NEEDED_ADDITIONAL_PARAMETER_LENGTH",
    # SID 0x2A
    "TRANSMISSION_MODE",
    # SID 0x2F
    "INPUT_OUTPUT_CONTROL_PARAMETER",
    # SID 0x36
    "BLOCK_SEQUENCE_COUNTER",
    # SID 0x38
    "MODE_OF_OPERATION_2013", "MODE_OF_OPERATION_2020",
    "FILE_AND_PATH_NAME_LENGTH",
    "FILE_SIZE_PARAMETER_LENGTH",
    "LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER",
    "FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH",
    "FILE_POSITION",
    # SID 0x83
    "TIMING_PARAMETER_REQUEST_RECORD", "TIMING_PARAMETER_RESPONSE_RECORD",
    # SID 0x84
    "SECURITY_DATA_REQUEST_RECORD", "SECURITY_DATA_RESPONSE_RECORD",
    "ADMINISTRATIVE_PARAMETER",
    "SIGNATURE_ENCRYPTION_CALCULATION",
    "SIGNATURE_LENGTH",
    "ANTI_REPLAY_COUNTER",
    "INTERNAL_SID", "INTERNAL_RSID", "INTERNAL_REQUEST_PARAMETERS", "INTERNAL_RESPONSE_PARAMETERS",
    # SID 0x85
    "DTC_SETTING_CONTROL_OPTION_RECORD",
    # SID 0x86
    "NUMBER_OF_IDENTIFIED_EVENTS", "NUMBER_OF_ACTIVATED_EVENTS",
    "COMPARISON_LOGIC", "COMPARE_VALUE", "HYSTERESIS_VALUE",
    "COMPARE_SIGN", "BITS_NUMBER", "BIT_OFFSET", "LOCALIZATION",
    "EVENT_TYPE_RECORD_02",
    # SID 0x87
    "LINK_RECORD",
    "LINK_CONTROL_MODE_IDENTIFIER",
    "CONDITIONAL_LINK_CONTROL_REQUEST",
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
    ConditionalMappingDataRecord,
    CustomFormulaDataRecord,
    LinearFormulaDataRecord,
    MappingAndLinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
)

# Shared

RESERVED_BIT = RawDataRecord(name="reserved",
                             length=1)
RESERVED_2BITS = RawDataRecord(name="reserved",
                               length=2)
RESERVED_4BITS = RawDataRecord(name="reserved",
                               length=4)
RESERVED_9BITS = RawDataRecord(name="reserved-9bits",
                               length=9)

DATA = RawDataRecord(name="data",
                     length=8,
                     min_occurrences=1,
                     max_occurrences=None)

MEMORY_ADDRESS_LENGTH = RawDataRecord(name="memoryAddressLength",
                                      length=4,
                                      unit="bytes")
MEMORY_SIZE_LENGTH = RawDataRecord(name="memorySizeLength",
                                   length=4,
                                   unit="bytes")
ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER = RawDataRecord(name="addressAndLengthFormatIdentifier",
                                                     length=8,
                                                     children=(MEMORY_SIZE_LENGTH, MEMORY_ADDRESS_LENGTH))



COMPRESSION_METHOD = MappingDataRecord(name="compressionMethod",
                                       length=4,
                                       values_mapping=COMPRESSION_METHOD_MAPPING)
ENCRYPTION_METHOD = MappingDataRecord(name="encryptingMethod",
                                      length=4,
                                      values_mapping=ENCRYPTION_METHOD_MAPPING)
DATA_FORMAT_IDENTIFIER = RawDataRecord(name="dataFormatIdentifier",
                                       length=8,
                                       children=(COMPRESSION_METHOD, ENCRYPTION_METHOD))

MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER = RawDataRecord(name="maxNumberOfBlockLengthBytesNumber",
                                                        length=4,
                                                        unit="bytes")
LENGTH_FORMAT_IDENTIFIER = RawDataRecord(name="lengthFormatIdentifier",
                                         length=8,
                                         children=(MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER, RESERVED_4BITS))



TRANSFER_REQUEST_PARAMETER = RawDataRecord(name="transferRequestParameter",
                                           length=8,
                                           min_occurrences=0,
                                           max_occurrences=None)
TRANSFER_RESPONSE_PARAMETER = RawDataRecord(name="transferResponseParameter",
                                            length=8,
                                            min_occurrences=0,
                                            max_occurrences=None)

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
                                                    values_mapping=POWER_DOWN_TIME_MAPPING,
                                                    factor=1,
                                                    offset=0,
                                                    unit="s")
CONDITIONAL_POWER_DOWN_TIME = ConditionalMappingDataRecord(mapping={0x4: [POWER_DOWN_TIME]},
                                                           default_message_continuation=[],
                                                           value_mask=0x7F)

# SID 0x14
OPTIONAL_MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                          length=8,
                                          min_occurrences=0,
                                          max_occurrences=1)

# SID 0x19
MEMORY_SELECTION = RawDataRecord(name="MemorySelection",
                                 length=8)

# SID 0x22
ACTIVE_DIAGNOSTIC_SESSION = MappingDataRecord(name="ActiveDiagnosticSession",
                                              values_mapping=DIAGNOSTIC_SESSION_TYPE_MAPPING,
                                              length=7)

# SID 0x24
SCALING_BYTE_TYPE = MappingDataRecord(name="type",
                                      length=4,
                                      values_mapping=SCALING_BYTE_TYPE_MAPPING)
SCALING_BYTE_LENGTH = RawDataRecord(name="numberOfBytesOfParameter",
                                    length=4,
                                    unit="bytes")

FORMULA_IDENTIFIER = MappingDataRecord(name="formulaIdentifier",
                                       length=8,
                                       values_mapping=FORMULA_IDENTIFIER_MAPPING)

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

STATE_AND_CONNECTION_TYPE_TYPE = MappingDataRecord(name="type",
                                                   length=2,
                                                   values_mapping=STATE_AND_CONNECTION_TYPE_TYPE_MAPPING)
STATE_AND_CONNECTION_TYPE_DIRECTION = MappingDataRecord(name="direction",
                                                        length=1,
                                                        values_mapping=STATE_AND_CONNECTION_TYPE_DIRECTION_MAPPING)
STATE_AND_CONNECTION_TYPE_LEVEL = MappingDataRecord(name="level",
                                                    length=2,
                                                    values_mapping=STATE_AND_CONNECTION_TYPE_LEVEL_MAPPING)
STATE_AND_CONNECTION_TYPE_STATE = MappingDataRecord(name="state",
                                                    length=3,
                                                    values_mapping=STATE_AND_CONNECTION_TYPE_STATE_MAPPING)
STATE_AND_CONNECTION_TYPE = RawDataRecord(name="stateAndConnectionType",
                                          length=8,
                                          children=(STATE_AND_CONNECTION_TYPE_TYPE,
                                                    STATE_AND_CONNECTION_TYPE_DIRECTION,
                                                    STATE_AND_CONNECTION_TYPE_LEVEL,
                                                    STATE_AND_CONNECTION_TYPE_STATE))

# SID 0x27
SECURITY_ACCESS_DATA = RawDataRecord(name="securityAccessData",
                                     length=8,
                                     min_occurrences=0,
                                     max_occurrences=None)
SECURITY_SEED = RawDataRecord(name="securitySeed",
                              length=8,
                              min_occurrences=1,
                              max_occurrences=None)
SECURITY_KEY = RawDataRecord(name="securityKey",
                             length=8,
                             min_occurrences=1,
                             max_occurrences=None)


# SID 0x28
MESSAGES_TYPE = MappingDataRecord(name="messagesType",
                                  length=2,
                                  values_mapping=MESSAGE_TYPE_MAPPING)
NETWORKS = MappingDataRecord(name="networks",
                                  length=4,
                                  values_mapping=NETWORKS_MAPPING)
COMMUNICATION_TYPE = RawDataRecord(name="communicationType",
                                   length=8,
                                   children=(MESSAGES_TYPE, RESERVED_2BITS, NETWORKS))
NODE_IDENTIFICATION_NUMBER = MappingDataRecord(name="nodeIdentificationNumber",
                                               length=16,
                                               values_mapping=NODE_IDENTIFICATION_NUMBER_MAPPING)

# SID 0x29
CERTIFICATE_CLIENT_LENGTH = RawDataRecord(name="lengthOfCertificateClient",
                                          length=16,
                                          unit="bytes")


CERTIFICATE_SERVER_LENGTH = RawDataRecord(name="lengthOfCertificateServer",
                                          length=16,
                                          unit="bytes")


CERTIFICATE_DATA_LENGTH = RawDataRecord(name="lengthOfCertificateData",
                                        length=16,
                                        unit="bytes")


CHALLENGE_CLIENT_LENGTH = RawDataRecord(name="lengthOfChallengeClient",
                                        length=16,
                                        unit="bytes")


CHALLENGE_SERVER_LENGTH = RawDataRecord(name="lengthOfChallengeServer",
                                        length=16,
                                        unit="bytes")


PROOF_OF_OWNERSHIP_CLIENT_LENGTH = RawDataRecord(name="lengthOfProofOfOwnershipClient",
                                                 length=16,
                                                 unit="bytes")


PROOF_OF_OWNERSHIP_SERVER_LENGTH = RawDataRecord(name="lengthOfProofOfOwnershipServer",
                                                 length=16,
                                                 unit="bytes")


EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH = RawDataRecord(name="lengthOfEphemeralPublicKeyClient",
                                                   length=16,
                                                   unit="bytes")


EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH = RawDataRecord(name="lengthOfEphemeralPublicKeyServer",
                                                   length=16,
                                                   unit="bytes")


NEEDED_ADDITIONAL_PARAMETER_LENGTH = RawDataRecord(name="lengthOfNeededAdditionalParameter",
                                                   length=16,
                                                   unit="bytes")


ADDITIONAL_PARAMETER_LENGTH = RawDataRecord(name="lengthOfAdditionalParameter",
                                            length=16,
                                            unit="bytes")


SESSION_KEY_INFO_LENGTH = RawDataRecord(name="lengthOfSessionKeyInfo",
                                        length=16,
                                        unit="bytes")


COMMUNICATION_CONFIGURATION = RawDataRecord(name="communicationConfiguration",
                                            length=8)
CERTIFICATE_EVALUATION = RawDataRecord(name="certificateEvaluationId",
                                       length=8)
ALGORITHM_INDICATOR = RawDataRecord(name="algorithmIndicator",
                                    length=8,
                                    min_occurrences=16,
                                    max_occurrences=16)
AUTHENTICATION_RETURN_PARAMETER = MappingDataRecord(
    name="authenticationReturnParameter",
    length=8,
    values_mapping=AUTHENTICATION_RETURN_PARAMETER_MAPPING)

# SID 0x2A
TRANSMISSION_MODE = MappingDataRecord(name="transmissionMode",
                                      length=8,
                                      values_mapping=TRANSMISSION_MODE_MAPPING)

# SID 0x2F
INPUT_OUTPUT_CONTROL_PARAMETER = MappingDataRecord(name="inputOutputControlParameter",
                                                   length=8,
                                                   values_mapping=INPUT_OUTPUT_CONTROL_PARAMETER_MAPPING)

# SID 0x36
BLOCK_SEQUENCE_COUNTER = RawDataRecord(name="blockSequenceCounter",
                                       length=8)

# SID 0x38
MODE_OF_OPERATION_2013 = MappingDataRecord(name="modeOfOperation",
                                           length=8,
                                           values_mapping=MODE_OF_OPERATION_MAPPING_2013)
MODE_OF_OPERATION_2020 = MappingDataRecord(name="modeOfOperation",
                                           length=8,
                                           values_mapping=MODE_OF_OPERATION_MAPPING_2020)

FILE_AND_PATH_NAME_LENGTH = RawDataRecord(name="filePathAndNameLength",
                                          length=16,
                                          unit="bytes")


FILE_SIZE_PARAMETER_LENGTH = RawDataRecord(name="fileSizeParameterLength",
                                           length=8,
                                           unit="bytes")


FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH = RawDataRecord(name="fileSizeOrDirInfoParameterLength",
                                                       length=16,
                                                       unit="bytes")


LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER = RawDataRecord(name="lengthFormatIdentifier",
                                                       length=8,
                                                       unit="bytes")


FILE_POSITION = RawDataRecord(name="filePosition",
                              length=64)



# SID 0x83
TIMING_PARAMETER_REQUEST_RECORD = RawDataRecord(name="TimingParameterRequestRecord",
                                                length=8,
                                                min_occurrences=1,
                                                max_occurrences=None)
TIMING_PARAMETER_RESPONSE_RECORD = RawDataRecord(name="TimingParameterResponseRecord",
                                                 length=8,
                                                 min_occurrences=1,
                                                 max_occurrences=None)

# SID 0x84
SECURITY_DATA_REQUEST_RECORD = RawDataRecord(name="securityDataRequestRecord",
                                             length=8,
                                             min_occurrences=1,
                                             max_occurrences=None)
SECURITY_DATA_RESPONSE_RECORD = RawDataRecord(name="securityDataResponseRecord",
                                              length=8,
                                              min_occurrences=1,
                                              max_occurrences=None)

IS_SIGNATURE_REQUESTED = MappingDataRecord(name="Signature on the response is requested.",
                                           length=1,
                                           values_mapping=NO_YES_MAPPING)
IS_MESSAGE_SIGNED = MappingDataRecord(name="Message is signed.",
                                      length=1,
                                      values_mapping=NO_YES_MAPPING)
IS_MESSAGE_ENCRYPTED = MappingDataRecord(name="Message is encrypted.",
                                         length=1,
                                         values_mapping=NO_YES_MAPPING)
IS_PRE_ESTABLISHED_KEY_USED = MappingDataRecord(name="A pre-established key is used.",
                                                length=1,
                                                values_mapping=NO_YES_MAPPING)
IS_REQUEST_MESSAGE = MappingDataRecord(name="Message is request message.",
                                       length=1,
                                       values_mapping=NO_YES_MAPPING)
ADMINISTRATIVE_PARAMETER = RawDataRecord(name="Administrative Parameter",
                                         length=16,
                                         children=(RESERVED_9BITS,
                                                   IS_SIGNATURE_REQUESTED,
                                                   IS_MESSAGE_SIGNED,
                                                   IS_MESSAGE_ENCRYPTED,
                                                   IS_PRE_ESTABLISHED_KEY_USED,
                                                   RESERVED_2BITS,
                                                   IS_REQUEST_MESSAGE))

SIGNATURE_ENCRYPTION_CALCULATION = RawDataRecord(name="Signature/Encryption Calculation",
                                                 length=8)

SIGNATURE_LENGTH = RawDataRecord(name="Signature Length",
                                 length=16,
                                 unit="bytes")

ANTI_REPLAY_COUNTER = RawDataRecord(name="Anti-replay Counter",
                                    length=16)

INTERNAL_SID = RawDataRecord(name="Internal Message Service Request ID",
                             length=8)
INTERNAL_RSID = RawDataRecord(name="Internal Message Service Response ID",
                              length=8)
INTERNAL_REQUEST_PARAMETERS = RawDataRecord(name="Service Specific Parameters",
                                            length=8,
                                            min_occurrences=0,
                                            max_occurrences=None)
INTERNAL_RESPONSE_PARAMETERS = RawDataRecord(name="Response Specific Parameters",
                                             length=8,
                                             min_occurrences=0,
                                             max_occurrences=None)

# SID 0x85
DTC_SETTING_CONTROL_OPTION_RECORD = RawDataRecord(name="DTCSettingControlOptionRecord",
                                                  length=8,
                                                  min_occurrences=0,
                                                  max_occurrences=None)

# SID 0x86
NUMBER_OF_IDENTIFIED_EVENTS = RawDataRecord(name="numberOfIdentifiedEvents",
                                            length=8)
NUMBER_OF_ACTIVATED_EVENTS = RawDataRecord(name="numberOfActivatedEvents",
                                           length=8)

COMPARISON_LOGIC = MappingDataRecord(name="Comparison logic",
                                     length=8,
                                     values_mapping=COMPARISON_LOGIC_MAPPING)
COMPARE_VALUE = RawDataRecord(name="Compare Value",
                              length=32)
HYSTERESIS_VALUE = RawDataRecord(name="Hysteresis Value",
                                 length=8)

COMPARE_SIGN = MappingDataRecord(name="Compare Sign",
                                 length=1,
                                 values_mapping=COMPARE_SIGN_MAPPING)
BITS_NUMBER = CustomFormulaDataRecord(name="Bits Number",
                                      length=5,
                                      encoding_formula=lambda physical_value: physical_value % 32,
                                      decoding_formula=lambda raw_value: 32 if raw_value == 0 else raw_value,
                                      unit="bits")
BIT_OFFSET = RawDataRecord(name="Bit Offset",
                           length=10,
                           unit="bits")
LOCALIZATION = RawDataRecord(name="Localization",
                             length=16,
                             children=(COMPARE_SIGN,
                                       BITS_NUMBER,
                                       BIT_OFFSET))


TIMER_SCHEDULE_2013 = MappingDataRecord(name="Timer schedule",
                                        length=8,
                                        values_mapping=TIMER_SCHEDULE_MAPPING_2013)

EVENT_TYPE_RECORD_02 = RawDataRecord(name="eventTypeRecord",
                                     length=8,
                                     children=(TIMER_SCHEDULE_2013,))


# SID 0x87
LINK_CONTROL_MODE_IDENTIFIER = MappingDataRecord(name="linkControlModeIdentifier",
                                                 length=8,
                                                 values_mapping=LINK_CONTROL_MODE_IDENTIFIER_MAPPING)
LINK_RECORD = RawDataRecord(name="linkRecord",
                            length=24)
CONDITIONAL_LINK_CONTROL_REQUEST = ConditionalMappingDataRecord(value_mask=0x7F,
                                                                mapping={
                                                                    0x01: (LINK_CONTROL_MODE_IDENTIFIER,),
                                                                    0x02: (LINK_RECORD,),
                                                                    0x03: (),
                                                                })

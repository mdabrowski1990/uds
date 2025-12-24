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
    # SID 0x27
    "CONDITIONAL_SECURITY_ACCESS_REQUEST", "CONDITIONAL_SECURITY_ACCESS_RESPONSE",
    # SID 0x28
    "CONDITIONAL_COMMUNICATION_CONTROL_REQUEST",
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
    "FILE_AND_PATH_NAME_LENGTH", "CONDITIONAL_FILE_AND_PATH_NAME",
    "FILE_SIZE_PARAMETER_LENGTH", "CONDITIONAL_FILE_SIZES",
    "LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER",
    "FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH", "CONDITIONAL_FILE_SIZES_OR_DIR_INFO", "CONDITIONAL_DIR_INFO",
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
    "CONDITIONAL_SECURED_DATA_TRANSMISSION_REQUEST", "CONDITIONAL_SECURED_DATA_TRANSMISSION_RESPONSE",
    # SID 0x85
    "DTC_SETTING_CONTROL_OPTION_RECORD",
    # SID 0x86
    "NUMBER_OF_IDENTIFIED_EVENTS", "NUMBER_OF_ACTIVATED_EVENTS",
    "COMPARISON_LOGIC", "COMPARE_VALUE", "HYSTERESIS_VALUE",
    "COMPARE_SIGN", "BITS_NUMBER", "BIT_OFFSET", "LOCALIZATION",
    "EVENT_WINDOW_TIME_2013", "EVENT_WINDOW_TIME_2020",
    "EVENT_TYPE_RECORD_08_2020",
    "EVENT_TYPE_RECORD_02",
    "SERVICE_TO_RESPOND",
    # SID 0x87
    "LINK_RECORD",
    "LINK_CONTROL_MODE_IDENTIFIER",
    "CONDITIONAL_LINK_CONTROL_REQUEST",
]


from typing import Optional, Tuple, Union

from uds.utilities import (
    AUTHENTICATION_RETURN_PARAMETER_MAPPING,
    COMPARE_SIGN_MAPPING,
    COMPARISON_LOGIC_MAPPING,
    COMPRESSION_METHOD_MAPPING,
    DIAGNOSTIC_SESSION_TYPE_MAPPING,
    ENCRYPTION_METHOD_MAPPING,
    EVENT_WINDOW_TIME_MAPPING_2013,
    EVENT_WINDOW_TIME_MAPPING_2020,
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
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    CustomFormulaDataRecord,
    LinearFormulaDataRecord,
    MappingAndLinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
    TextDataRecord,
    TextEncoding,
)
from .sub_functions import EVENT_TYPE_2013, EVENT_TYPE_2020, REPORT_TYPE_2020

# Formulas
























def get_file_path_and_name(file_path_and_name_length: int) -> Tuple[TextDataRecord]:
    """
    Get `filePathAndName` Data Record of given bytes length.

    :param file_path_and_name_length: Bytes length of `filePathAndName` Data Record.

    :raise ValueError: Provided `filePathAndNameLength` value equals 0.

    :return: Tuple with `filePathAndName` Data Record.
    """
    if file_path_and_name_length == 0:
        raise ValueError("Value of `filePathAndNameLength` must be greater than 0.")
    return (TextDataRecord(name="filePathAndName",
                           encoding=TextEncoding.ASCII,
                           min_occurrences=file_path_and_name_length,
                           max_occurrences=file_path_and_name_length,
                           enforce_reoccurring=True),)


def get_file_sizes(file_size_parameter_length: int) -> Tuple[RawDataRecord, RawDataRecord]:
    """
    Get file size Data Records of given bytes length.

    :param file_size_parameter_length: Bytes length of `fileSizeUnCompressed` and `fileSizeCompressed` Data Records.

    :raise ValueError: Provided `fileSizeParameterLength` value equals 0.

    :return: Tuple with `fileSizeUnCompressed` and `fileSizeCompressed` Data Records.
    """
    if file_size_parameter_length == 0:
        raise ValueError("Value of `fileSizeParameterLength` must be greater than 0.")
    return (RawDataRecord(name="fileSizeUnCompressed",
                          length=8 * file_size_parameter_length,
                          unit="bytes"),
            RawDataRecord(name="fileSizeCompressed",
                          length=8 * file_size_parameter_length,
                          unit="bytes"))


def get_file_sizes_or_dir_info(file_size_or_dir_info_parameter_length: int) -> Tuple[RawDataRecord, RawDataRecord]:
    """
    Get file size Data Records of given bytes length.

    :param file_size_or_dir_info_parameter_length: Bytes length of `fileSizeUncompressedOrDirInfoLength`
        and `fileSizeCompressed` Data Records.

    :raise ValueError: Provided `fileSizeOrDirInfoParameterLength` value equals 0.

    :return: Tuple with `fileSizeUncompressedOrDirInfoLength` and `fileSizeCompressed` Data Records.
    """
    if file_size_or_dir_info_parameter_length == 0:
        raise ValueError("Value of `fileSizeOrDirInfoParameterLength` must be greater than 0.")
    return (RawDataRecord(name="fileSizeUncompressedOrDirInfoLength",
                          length=8 * file_size_or_dir_info_parameter_length,
                          unit="bytes"),
            RawDataRecord(name="fileSizeCompressed",
                          length=8 * file_size_or_dir_info_parameter_length,
                          unit="bytes"))


def get_dir_info(file_size_or_dir_info_parameter_length: int) -> Tuple[RawDataRecord]:
    """
    Get dir info Data Record of given bytes length.

    :param file_size_or_dir_info_parameter_length: Bytes length of `fileSizeUncompressedOrDirInfoLength` Data Record.

    :raise ValueError: Provided `fileSizeOrDirInfoParameterLength` value equals 0.

    :return: Tuple with `file_size_or_dir_info_parameter_length` Data Record.
    """
    if file_size_or_dir_info_parameter_length == 0:
        raise ValueError("Value of `fileSizeOrDirInfoParameterLength` must be greater than 0.")
    return (RawDataRecord(name="fileSizeUncompressedOrDirInfoLength",
                          length=8 * file_size_or_dir_info_parameter_length,
                          unit="bytes"),)


def get_security_access_request(sub_function: int) -> Tuple[RawDataRecord]:
    """
    Get SecurityAccess Data Records that are part of request message for given SubFunction value.

    :param sub_function: SubFunction value.

    :return: Data Records that are present in the request message after given SubFunction value.
    """
    if sub_function % 2:
        return (SECURITY_ACCESS_DATA,)
    return (SECURITY_KEY,)


def get_security_access_response(sub_function: int) -> Union[Tuple[RawDataRecord], Tuple[()]]:
    """
    Get SecurityAccess Data Records that are part of response message for given SubFunction value.

    :param sub_function: SubFunction value.

    :return: Data Records that are present in the response message after given SubFunction value.
    """
    if sub_function % 2:
        return (SECURITY_SEED,)
    return ()


def get_communication_control_request(sub_function: int
                                      ) -> Union[Tuple[RawDataRecord, MappingDataRecord], Tuple[RawDataRecord]]:
    """
    Get CommunicationControl Data Records that are part of request message for given SubFunction value.

    :param sub_function: SubFunction value.

    :return: Data Records that are present in the request message after given SubFunction value.
    """
    if sub_function & 0x7F in {0x04, 0x05}:
        return COMMUNICATION_TYPE, NODE_IDENTIFICATION_NUMBER
    return (COMMUNICATION_TYPE,)


def get_secured_data_transmission_request(signature_length: int) -> Union[
        Tuple[RawDataRecord, RawDataRecord, RawDataRecord, RawDataRecord],
        Tuple[RawDataRecord, RawDataRecord, RawDataRecord]]:
    """
    Get SecuredDataTransmission Data Records that are part of request message after given Signature Length value.

    :param signature_length: Value of Signature Length.

    :return: Data Records that are present in the request message after given Signature Length value.
    """
    if signature_length == 0:
        return (ANTI_REPLAY_COUNTER,
                INTERNAL_SID,
                INTERNAL_REQUEST_PARAMETERS)
    signature = RawDataRecord(name="Signature/MAC",
                              length=8,
                              min_occurrences=signature_length,
                              max_occurrences=signature_length,
                              enforce_reoccurring=True)
    return (ANTI_REPLAY_COUNTER,
            INTERNAL_SID,
            INTERNAL_REQUEST_PARAMETERS,
            signature)


def get_secured_data_transmission_response(signature_length: int) -> Union[
        Tuple[RawDataRecord, RawDataRecord, RawDataRecord, RawDataRecord],
        Tuple[RawDataRecord, RawDataRecord, RawDataRecord]]:
    """
    Get SecuredDataTransmission Data Records that are part of response message after given Signature Length value.

    :param signature_length: Value of Signature Length.

    :return: Data Records that are present in the response message after given Signature Length value.
    """
    if signature_length == 0:
        return (ANTI_REPLAY_COUNTER,
                INTERNAL_RSID,
                INTERNAL_RESPONSE_PARAMETERS)
    signature = RawDataRecord(name="Signature/MAC",
                              length=8,
                              min_occurrences=signature_length,
                              max_occurrences=signature_length,
                              enforce_reoccurring=True)
    return (ANTI_REPLAY_COUNTER,
            INTERNAL_RSID,
            INTERNAL_RESPONSE_PARAMETERS,
            signature)


def get_event_window_2013(event_number: Optional[int] = None) -> MappingDataRecord:
    """
    Get eventWindowTime Data Record compatible with ISO 14229-1:2013 version.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventWindowTime Data Record.
    """
    return MappingDataRecord(name="eventWindowTime" if event_number is None else f"eventWindowTime#{event_number}",
                             length=8,
                             values_mapping=EVENT_WINDOW_TIME_MAPPING_2013)


def get_event_window_2020(event_number: Optional[int] = None) -> MappingDataRecord:
    """
    Get eventWindowTime Data Record compatible with ISO 14229-1:2020 version.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventWindowTime Data Record.
    """
    return MappingDataRecord(name="eventWindowTime" if event_number is None else f"eventWindowTime#{event_number}",
                             length=8,
                             values_mapping=EVENT_WINDOW_TIME_MAPPING_2020)


def get_service_to_respond(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get serviceToRespondToRecord Data Record.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created serviceToRespondToRecord Data Record.
    """
    return RawDataRecord(name="serviceToRespondToRecord" if event_number is None
                              else f"serviceToRespondToRecord#{event_number}",
                         length=8,
                         min_occurrences=1,
                         max_occurrences=None)


def get_event_type_of_active_event_2013(event_number: int) -> RawDataRecord:
    """
    Get eventTypeOfActiveEvent Data Record.

    :param event_number: Number of the active event.

    :return: Created eventTypeOfActiveEvent Data Record.
    """
    return RawDataRecord(name=f"eventTypeOfActiveEvent#{event_number}",
                         length=8,
                         children=(RESERVED_BIT,
                                   EVENT_TYPE_2013))


def get_event_type_of_active_event_2020(event_number: int) -> RawDataRecord:
    """
    Get eventTypeOfActiveEvent Data Record.

    :param event_number: Number of the active event.

    :return: Created eventTypeOfActiveEvent Data Record.
    """
    return RawDataRecord(name=f"eventTypeOfActiveEvent#{event_number}",
                         length=8,
                         children=(RESERVED_BIT,
                                   EVENT_TYPE_2020))


def get_event_type_record_02(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get eventTypeRecord Data Record for event equal to 0x02.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventTypeRecord Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(TIMER_SCHEDULE,))


def get_event_type_record_08_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get eventTypeRecord Data Record for event equal to 0x08.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventTypeRecord Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(RESERVED_BIT,
                                   REPORT_TYPE_2020))


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
CONDITIONAL_SECURITY_ACCESS_REQUEST = ConditionalFormulaDataRecord(formula=get_security_access_request)
CONDITIONAL_SECURITY_ACCESS_RESPONSE = ConditionalFormulaDataRecord(formula=get_security_access_response)

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
# TODO: change CONDITIONAL_COMMUNICATION_CONTROL_REQUEST to ConditionalMappingDataRecord
#  https://github.com/mdabrowski1990/uds/issues/413
CONDITIONAL_COMMUNICATION_CONTROL_REQUEST = ConditionalFormulaDataRecord(formula=get_communication_control_request)

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
CONDITIONAL_FILE_AND_PATH_NAME = ConditionalFormulaDataRecord(formula=get_file_path_and_name)

FILE_SIZE_PARAMETER_LENGTH = RawDataRecord(name="fileSizeParameterLength",
                                           length=8,
                                           unit="bytes")
CONDITIONAL_FILE_SIZES = ConditionalFormulaDataRecord(formula=get_file_sizes)

FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH = RawDataRecord(name="fileSizeOrDirInfoParameterLength",
                                                       length=16,
                                                       unit="bytes")
CONDITIONAL_DIR_INFO = ConditionalFormulaDataRecord(formula=get_dir_info)
CONDITIONAL_FILE_SIZES_OR_DIR_INFO = ConditionalFormulaDataRecord(formula=get_file_sizes_or_dir_info)

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

CONDITIONAL_SECURED_DATA_TRANSMISSION_REQUEST = ConditionalFormulaDataRecord(
    formula=get_secured_data_transmission_request)
CONDITIONAL_SECURED_DATA_TRANSMISSION_RESPONSE = ConditionalFormulaDataRecord(
    formula=get_secured_data_transmission_response)

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
EVENT_WINDOW_TIME_2020 = get_event_window_2020()
EVENT_WINDOW_TIME_2013 = get_event_window_2013()

EVENT_TYPE_RECORD_08_2020 = get_event_type_record_08_2020()

TIMER_SCHEDULE = MappingDataRecord(name="Timer schedule",
                                   length=8,
                                   values_mapping=TIMER_SCHEDULE_MAPPING_2013)

EVENT_TYPE_RECORD_02 = RawDataRecord(name="eventTypeRecord",
                                     length=8,
                                     children=(TIMER_SCHEDULE,))

SERVICE_TO_RESPOND = get_service_to_respond()

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

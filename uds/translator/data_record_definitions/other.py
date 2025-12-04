"""Remaining Data Records definitions."""  # pylint: disable=too-many-lines

__all__ = [
    # Shared
    "RESERVED_BIT",
    "DATA",
    "ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER", "CONDITIONAL_MEMORY_ADDRESS_AND_SIZE",
    "DATA_FORMAT_IDENTIFIER", "LENGTH_FORMAT_IDENTIFIER", "CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH",
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
    # SID 0x24
    "SCALING_DATA_RECORDS",
    # SID 0x27
    "CONDITIONAL_SECURITY_ACCESS_REQUEST", "CONDITIONAL_SECURITY_ACCESS_RESPONSE",
    # SID 0x28
    "CONDITIONAL_COMMUNICATION_CONTROL_REQUEST",
    # SID 0x29
    "COMMUNICATION_CONFIGURATION", "CERTIFICATE_EVALUATION", "ALGORITHM_INDICATOR", "AUTHENTICATION_RETURN_PARAMETER",
    "CERTIFICATE_CLIENT_LENGTH", "CONDITIONAL_CERTIFICATE_CLIENT",
    "CERTIFICATE_SERVER_LENGTH", "CONDITIONAL_CERTIFICATE_SERVER",
    "CERTIFICATE_DATA_LENGTH", "CONDITIONAL_CERTIFICATE_DATA",
    "CHALLENGE_CLIENT_LENGTH", "CONDITIONAL_CHALLENGE_CLIENT", "CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT",
    "CHALLENGE_SERVER_LENGTH", "CONDITIONAL_CHALLENGE_SERVER",
    "PROOF_OF_OWNERSHIP_CLIENT_LENGTH", "CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT",
    "PROOF_OF_OWNERSHIP_SERVER_LENGTH", "CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER",
    "EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH", "CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_CLIENT",
    "EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH", "CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER",
    "SESSION_KEY_INFO_LENGTH", "CONDITIONAL_OPTIONAL_SESSION_KEY_INFO",
    "ADDITIONAL_PARAMETER_LENGTH", "CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER",
    "NEEDED_ADDITIONAL_PARAMETER_LENGTH", "CONDITIONAL_OPTIONAL_NEEDED_ADDITIONAL_PARAMETER",
    # SID 0x2A
    "TRANSMISSION_MODE",
    # SID 0x2C
    "CONDITIONAL_DATA_FROM_MEMORY",
    # SID 0x2F
    "INPUT_OUTPUT_CONTROL_PARAMETER",
    # SID 0x36
    "BLOCK_SEQUENCE_COUNTER",
    # SID 0x38
    "MODE_OF_OPERATION_2013", "MODE_OF_OPERATION_2020",
    "FILE_AND_PATH_NAME_LENGTH", "CONDITIONAL_FILE_AND_PATH_NAME",
    "FILE_SIZE_PARAMETER_LENGTH", "CONDITIONAL_FILE_SIZES",
    "LENGTH_FORMAT_IDENTIFIER_FILE_TRANSFER", "CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER",
    "FILE_SIZE_OR_DIR_INFO_PARAMETER_LENGTH", "CONDITIONAL_FILE_SIZES_OR_DIR_INFO", "CONDITIONAL_DIR_INFO",
    "FILE_POSITION",
    # SID 0x3D
    "CONDITIONAL_DATA",
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
    "NUMBER_OF_IDENTIFIED_EVENTS",
    "COMPARISON_LOGIC", "COMPARE_VALUE", "HYSTERESIS_VALUE",
    "COMPARE_SIGN", "BITS_NUMBER", "BIT_OFFSET", "LOCALIZATION",
    "EVENT_WINDOW_TIME_2013", "EVENT_WINDOW_TIME_2020",
    "EVENT_TYPE_RECORD_08_2020",
    "EVENT_TYPE_RECORD_02",
    "SERVICE_TO_RESPOND"
]

from decimal import Decimal
from typing import Callable, Optional, Tuple, Union

from uds.utilities import EXPONENT_BIT_LENGTH, MANTISSA_BIT_LENGTH, REPEATED_DATA_RECORDS_NUMBER, InconsistencyError

from ..data_record import (
    AliasMessageStructure,
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
from .sub_functions import (
    DIAGNOSTIC_SESSIONS_MAPPING,
    EVENT_TYPE_2013,
    EVENT_TYPE_2020,
    MAPPING_YES_NO,
    REPORT_TYPE_2020,
)


# Formulas
def get_formula_for_raw_data_record_with_length(data_record_name: str,
                                                accept_zero_length: bool
                                                ) -> Callable[[int], Union[Tuple[RawDataRecord], Tuple[()]]]:
    """
    Get formula for Conditional Data Record that returns Raw Data Record with given name.

    :param data_record_name: Name for Raw Data Record name.
    :param accept_zero_length: True to accept length equal zero else False.

    :return: Formula for creating Raw Data Record that is proceeded by (bytes) length parameter.
    """
    def get_raw_data_record(length: int) -> Union[Tuple[RawDataRecord], Tuple[()]]:
        if accept_zero_length and length == 0:
            return ()
        if length > 0:
            return (RawDataRecord(name=data_record_name,
                                  length=8,
                                  min_occurrences=length,
                                  max_occurrences=length,
                                  enforce_reoccurring=True),)
        raise ValueError("Unexpected length value provided. "
                         f"Expected: {0 if accept_zero_length else 1} <= length (int type). "
                         f"Actual value: {length!r}.")
    return get_raw_data_record


def get_memory_size_and_memory_address(address_and_length_format_identifier: int
                                       ) -> Tuple[RawDataRecord, RawDataRecord]:
    """
    Get `memoryAddress` and `memorySize` Data Records for given `addressAndLengthFormatIdentifier` value.

    :param address_and_length_format_identifier: Proceeding `addressAndLengthFormatIdentifier` value.

    :raise ValueError: At least one of the `addressAndLengthFormatIdentifier` nibbles
        (`memoryAddressLength` or `memorySizeLength`) equals 0.

    :return: Tuple with `memoryAddress` and `memorySize` Data Records.
    """
    memory_size_length = (address_and_length_format_identifier & 0xF0) >> 4
    memory_address_length = address_and_length_format_identifier & 0x0F
    if memory_address_length == 0 or memory_size_length == 0:
        raise ValueError("Provided `addressAndLengthFormatIdentifier` value "
                         f"(0x{address_and_length_format_identifier:02X}) is incorrect as both contained values"
                         f"`memoryAddressLength` ({memory_address_length}) and "
                         f"`memorySizeLength` ({memory_size_length}) must be greater than 0.")
    return (RawDataRecord(name="memoryAddress", length=8 * memory_address_length),
            RawDataRecord(name="memorySize", length=8 * memory_size_length, unit="bytes"))


def get_data(memory_size_length: int) -> Tuple[RawDataRecord]:
    """
    Get `data` Data Record for given `memorySizeLength` value.

    :param memory_size_length: Proceeding `memorySizeLength` value.

    :raise ValueError: Provided `memorySizeLength` equals 0.

    :return: Tuple with `data` Data Record.
    """
    if memory_size_length == 0:
        raise ValueError("Value of `memorySizeLength` must be greater than 0.")
    return (RawDataRecord(name="data",
                          length=8,
                          min_occurrences=memory_size_length,
                          max_occurrences=memory_size_length),)


def get_data_from_memory(address_and_length_format_identifier: int) -> Tuple[RawDataRecord]:
    """
    Get `Data from Memory` Data Record for given `addressAndLengthFormatIdentifier` value.

    :param address_and_length_format_identifier: Proceeding `addressAndLengthFormatIdentifier` value.

    :raise ValueError: At least one of the `addressAndLengthFormatIdentifier` nibbles
        (`memoryAddressLength` or `memorySizeLength`) equals 0.

    :return: Tuple with `Data from Memory` Data Record.
    """
    memory_size_length = (address_and_length_format_identifier & 0xF0) >> 4
    memory_address_length = address_and_length_format_identifier & 0x0F
    if memory_address_length == 0 or memory_size_length == 0:
        raise ValueError("Provided `addressAndLengthFormatIdentifier` value "
                         f"(0x{address_and_length_format_identifier:02X}) is incorrect as both contained values"
                         f"`memoryAddressLength` ({memory_address_length}) and "
                         f"`memorySizeLength` ({memory_size_length}) must be greater than 0.")
    return (RawDataRecord(name="Data from Memory",
                          length=8 * (memory_address_length + memory_size_length),
                          children=(RawDataRecord(name="memoryAddress", length=8 * memory_address_length),
                                    RawDataRecord(name="memorySize", length=8 * memory_size_length, unit="bytes")),
                          min_occurrences=1,
                          max_occurrences=None),)


def get_max_number_of_block_length(length_format_identifier: int) -> Tuple[RawDataRecord]:
    """
    Get `maxNumberOfBlockLength` Data Record for given `lengthFormatIdentifier` value.

    .. warning:: This method must not be used for
        :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` service as it contains
        `lengthFormatIdentifier` in different format.

    :param length_format_identifier: Proceeding `lengthFormatIdentifier` value.

    :raise ValueError: The high nibble of `lengthFormatIdentifier` (`maxNumberOfBlockLengthBytesNumber`) equals 0.

    :return: Tuple with `maxNumberOfBlockLength` Data Record.
    """
    bytes_number = (length_format_identifier & 0xF0) >> 4
    if bytes_number == 0:
        raise ValueError(f"Provided `lengthFormatIdentifier` value (0x{length_format_identifier:02X}) is incorrect "
                         f"as contained value `maxNumberOfBlockLengthBytesNumber` ({bytes_number}) "
                         "must be greater than 0.")
    return (RawDataRecord(name="maxNumberOfBlockLength", length=8 * bytes_number, unit="bytes"),)


def get_max_number_of_block_length_file_transfer(length_format_identifier: int) -> Tuple[RawDataRecord]:
    """
    Get `maxNumberOfBlockLength` Data Record for given `lengthFormatIdentifier` value.

    .. warning:: This method is specific for :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>`
        service as it contains `lengthFormatIdentifier` in slightly different format.

    :param length_format_identifier: Proceeding `lengthFormatIdentifier` value.

    :raise ValueError: Provided `lengthFormatIdentifier` equals 0.

    :return: Tuple with `maxNumberOfBlockLength` Data Record.
    """
    if length_format_identifier == 0:
        raise ValueError("Value of `lengthFormatIdentifier` must be greater than 0.")
    return (RawDataRecord(name="maxNumberOfBlockLength", length=8 * length_format_identifier, unit="bytes"),)


def get_scaling_byte_extension(scaling_byte: int,
                               scaling_byte_number: int
                               ) -> Tuple[Union[RawDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get scalingByteExtension Data Records for given scalingByte value.

    :param scaling_byte: Proceeding `scalingByte` value.
    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :raise InconsistencyError: Provided `scalingByte` equals 0x20.

    :return: Data Records for scalingByteExtension.
    """
    parameter_type = (scaling_byte & 0xF0) >> 4
    number_of_bytes = scaling_byte & 0x0F
    if parameter_type == 0x2:  # bitMappedReportedWithOutMask
        if number_of_bytes == 0:
            raise InconsistencyError("Provided `scalingByte` value is incorrect (0x20) - byte length equals 0.")
        return (RawDataRecord(name=f"scalingByteExtension#{scaling_byte_number}",
                              length=8 * number_of_bytes,
                              children=(RawDataRecord(name="validityMask",
                                                      length=8 * number_of_bytes),)),)
    if parameter_type == 0x9:  # formula
        return (RawDataRecord(name=f"scalingByteExtension#{scaling_byte_number}",
                              length=FORMULA_IDENTIFIER.length,
                              children=(FORMULA_IDENTIFIER,)),
                ConditionalFormulaDataRecord(
                    formula=get_formula_data_records_for_formula_parameters(scaling_byte_number)),)
    if parameter_type == 0xA:  # unit/format
        return (RawDataRecord(name=f"scalingByteExtension#{scaling_byte_number}",
                              length=UNIT_OR_FORMAT.length,
                              children=(UNIT_OR_FORMAT,)),)
    if parameter_type == 0xB:  # stateAndConnectionType
        return (RawDataRecord(name=f"scalingByteExtension#{scaling_byte_number}",
                              length=STATE_AND_CONNECTION_TYPE.length,
                              children=(STATE_AND_CONNECTION_TYPE,)),)
    return ()


def get_scaling_byte_extension_formula(scaling_byte_number: int) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting scalingByteExtension Data Records.

    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :return: Formula for given scaling byte number.
    """
    return lambda scaling_byte: get_scaling_byte_extension(scaling_byte=scaling_byte,
                                                           scaling_byte_number=scaling_byte_number)


def get_data_records_for_formula_parameters(formula_identifier: int,
                                            scaling_byte_number: int) -> Tuple[CustomFormulaDataRecord, ...]:
    """
    Get coefficients' Data Records for formula type parameter.

    :param formula_identifier: Formula Identifier used.
    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :raise ValueError: Undefined value of Formula Identifier was provided.

    :return: Tuple with coefficients' Data Records for given formula type parameter.
    """
    physical_value = FORMULA_IDENTIFIER.get_physical_value(formula_identifier)
    if isinstance(physical_value, str) and "C0" in physical_value:
        data_records = []
        constant_index = 0
        encoding_formula = get_encode_float_value_formula(exponent_bit_length=EXPONENT_BIT_LENGTH,
                                                          mantissa_bit_length=MANTISSA_BIT_LENGTH)
        decoding_formula = get_decode_float_value_formula(exponent_bit_length=EXPONENT_BIT_LENGTH,
                                                          mantissa_bit_length=MANTISSA_BIT_LENGTH)
        length = EXPONENT_BIT_LENGTH + MANTISSA_BIT_LENGTH
        while f"C{constant_index}" in physical_value:
            data_records.append(CustomFormulaDataRecord(name=f"C{constant_index}#{scaling_byte_number}",
                                                        length=length,
                                                        children=(EXPONENT, MANTISSA),
                                                        encoding_formula=encoding_formula,
                                                        decoding_formula=decoding_formula))
            constant_index += 1
        return tuple(data_records)
    raise ValueError(f"Unknown formula identifier was provided: 0x{formula_identifier:02X}.")


def get_formula_data_records_for_formula_parameters(scaling_byte_number: int
                                                    ) -> Callable[[int], Tuple[CustomFormulaDataRecord, ...]]:
    """
    Get formula that can be used by Conditional Data Record for getting formula coefficients.

    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :return: Formula for given scaling byte number.
    """
    return lambda formula_identifier: get_data_records_for_formula_parameters(formula_identifier=formula_identifier,
                                                                              scaling_byte_number=scaling_byte_number)


def get_decode_signed_value_formula(bit_length: int) -> Callable[[int], int]:
    """
    Get formula for decoding signed integer value.

    :param bit_length: Number of bits used for signed integer value.

    :raise TypeError: Provided value is not int type.
    :raise ValueError: Provided value is out of range.

    :return: Formula for decoding singed integer value from unsigned integer value.
    """
    if not isinstance(bit_length, int):
        raise TypeError("Provided `bit_length` value is not int type.")
    if bit_length < 2:
        raise ValueError(f"Provided `bit_length` is too small for store signed integer value: {bit_length}.")

    def decode_signed_value(value: int) -> int:
        max_value = (1 << bit_length) - 1
        msb_value = 1 << (bit_length - 1)
        if not 0 <= value <= max_value:
            raise ValueError(f"Provided value is out of range (0 <= value <= {max_value}): {value}.")
        return (- (value & msb_value)) + (value & (max_value ^ msb_value))
    return decode_signed_value


def get_encode_signed_value_formula(bit_length: int) -> Callable[[int], int]:
    """
    Get formula for encoding signed integer value.

    :param bit_length: Number of bits used for signed integer value.

    :raise TypeError: Provided value is not int type.
    :raise ValueError: Provided value is out of range.

    :return: Formula for encoding singed integer value into unsinged integer value.
    """
    if not isinstance(bit_length, int):
        raise TypeError("Provided `bit_length` value is not int type.")
    if bit_length < 2:
        raise ValueError(f"Provided `bit_length` is too small for store signed integer value: {bit_length}.")

    def encode_signed_value(value: int) -> int:
        msb_value = 1 << (bit_length - 1)
        min_value = - msb_value
        max_value = msb_value - 1
        if not min_value <= value <= max_value:
            raise ValueError(f"Provided value is out of range ({min_value} <= value <= {max_value}): {value}.")
        if value >= 0:
            return value
        return 2 * msb_value + value
    return encode_signed_value


def get_decode_float_value_formula(exponent_bit_length: int, mantissa_bit_length: int) -> Callable[[int], float]:
    """
    Get formula for decoding float value.

    :param exponent_bit_length: Number of bits used for exponent's signed integer value.
    :param mantissa_bit_length: Number of bits used for mantissa's signed integer value.

    :return: Formula for decoding float value from unsigned integer value.
    """
    exponent_encode_formula = get_encode_signed_value_formula(exponent_bit_length)
    mantissa_encode_formula = get_encode_signed_value_formula(mantissa_bit_length)
    exponent_mask = ((1 << exponent_bit_length) - 1) << mantissa_bit_length
    mantissa_mask = (1 << mantissa_bit_length) - 1

    def get_float_value(value: int) -> float:
        exponent_unsigned_value = (value & exponent_mask) >> mantissa_bit_length
        mantissa_unsigned_value = value & mantissa_mask
        exponent_value: int = exponent_encode_formula(exponent_unsigned_value)
        mantissa_value: int = mantissa_encode_formula(mantissa_unsigned_value)
        return float(10 ** exponent_value) * mantissa_value
    return get_float_value


def get_encode_float_value_formula(exponent_bit_length: int, mantissa_bit_length: int) -> Callable[[float], int]:
    """
    Get formula for encoding float value.

    :param exponent_bit_length: Number of bits used for exponent's signed integer value.
    :param mantissa_bit_length: Number of bits used for mantissa's signed integer value.

    :return: Formula for encoding float value into unsigned integer value.
    """
    exponent_decode_formula = get_decode_signed_value_formula(exponent_bit_length)
    mantissa_decode_formula = get_decode_signed_value_formula(mantissa_bit_length)

    def get_unsinged_value(value: float) -> int:
        sign, digits, exponent_signed_value = Decimal(str(value)).normalize().as_tuple()
        if not isinstance(exponent_signed_value, int):
            raise ValueError("No handling for literal values.")
        mantissa_signed_value = int(f"{'-' if sign else ''}{''.join((str(digit) for digit in digits))}")
        exponent_unsigned_value = exponent_decode_formula(exponent_signed_value)
        mantissa_unsigned_value = mantissa_decode_formula(mantissa_signed_value)
        return (exponent_unsigned_value << mantissa_bit_length) + mantissa_unsigned_value
    return get_unsinged_value


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
    return MappingDataRecord(name="eventWindowTime" if event_number is None
    else f"eventWindowTime#{event_number}",
                             length=8,
                             values_mapping={
                                 0x02: "infiniteTimeToResponse",
                             })


def get_event_window_2020(event_number: Optional[int] = None) -> MappingDataRecord:
    """
    Get eventWindowTime Data Record compatible with ISO 14229-1:2020 version.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventWindowTime Data Record.
    """
    return MappingDataRecord(name="eventWindowTime" if event_number is None
    else f"eventWindowTime#{event_number}",
                             length=8,
                             values_mapping={
                                 0x02: "infiniteTimeToResponse",
                                 0x03: "shortEventWindowTime",
                                 0x04: "mediumEventWindowTime",
                                 0x05: "longEventWindowTime",
                                 0x06: "powerWindowTime",
                                 0x07: "ignitionWindowTime",
                                 0x08: "manufacturerTriggerEventWindowTime",
                             })


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


def event_type_of_active_event_2013(event_number: int) -> RawDataRecord:
    """
    Get eventTypeOfActiveEvent Data Record.

    :param event_number: Number of the active event.

    :return: Created eventTypeOfActiveEvent Data Record.
    """
    return RawDataRecord(name=f"eventTypeOfActiveEvent#{event_number}",
                         length=8,
                         children=(RESERVED_BIT,
                                   EVENT_TYPE_2013))


def event_type_of_active_event_2020(event_number: int) -> RawDataRecord:
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
    return RawDataRecord(name="eventTypeRecord" if event_number is None
    else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(TIMER_SCHEDULE,))


def get_event_type_record_08(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get eventTypeRecord Data Record for event equal to 0x02.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventTypeRecord Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None
    else f"eventTypeRecord#{event_number}",
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

CONDITIONAL_MEMORY_ADDRESS_AND_SIZE = ConditionalFormulaDataRecord(formula=get_memory_size_and_memory_address)

COMPRESSION_METHOD = MappingDataRecord(name="compressionMethod",
                                       length=4,
                                       values_mapping={
                                           0: "no compression",
                                       } | {
                                           value: f"compression #{value}" for value in range(1, 0x10)
                                       })
ENCRYPTION_METHOD = MappingDataRecord(name="encryptingMethod",
                                      length=4,
                                      values_mapping={
                                          0: "no encryption",
                                      } | {
                                          value: f"encryption #{value}" for value in range(1, 0x10)
                                      })
DATA_FORMAT_IDENTIFIER = RawDataRecord(name="dataFormatIdentifier",
                                       length=8,
                                       children=(COMPRESSION_METHOD, ENCRYPTION_METHOD))

MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER = RawDataRecord(name="maxNumberOfBlockLengthBytesNumber",
                                                        length=4,
                                                        unit="bytes")
LENGTH_FORMAT_IDENTIFIER = RawDataRecord(name="lengthFormatIdentifier",
                                         length=8,
                                         children=(MAX_NUMBER_OF_BLOCK_LENGTH_BYTES_NUMBER, RESERVED_4BITS))

CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH = ConditionalFormulaDataRecord(formula=get_max_number_of_block_length)

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
                                                    values_mapping={0xFF: "failure or time unavailable"},
                                                    factor=1,
                                                    offset=0,
                                                    unit="s")
CONDITIONAL_POWER_DOWN_TIME = ConditionalMappingDataRecord(mapping={0x4: [POWER_DOWN_TIME]},
                                                           default_message_continuation=[])

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
                                              values_mapping=DIAGNOSTIC_SESSIONS_MAPPING,
                                              length=7)

# SID 0x24
SCALING_BYTE_TYPE = MappingDataRecord(name="type",
                                      length=4,
                                      values_mapping={
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
                                      })
SCALING_BYTE_LENGTH = RawDataRecord(name="numberOfBytesOfParameter",
                                    length=4,
                                    unit="bytes")
SCALING_BYTES_LIST = [RawDataRecord(name=f"scalingByte#{index + 1}",
                                    children=(SCALING_BYTE_TYPE, SCALING_BYTE_LENGTH),
                                    length=8,
                                    min_occurrences=1 if index == 0 else 0,
                                    max_occurrences=1)
                      for index in range(REPEATED_DATA_RECORDS_NUMBER)]
SCALING_BYTES_EXTENSIONS_LIST = [ConditionalFormulaDataRecord(formula=get_scaling_byte_extension_formula(index + 1))
                                 for index in range(REPEATED_DATA_RECORDS_NUMBER)]
SCALING_DATA_RECORDS = [item for scaling_data_records in zip(SCALING_BYTES_LIST,
                                                             SCALING_BYTES_EXTENSIONS_LIST)
                        for item in scaling_data_records]

FORMULA_IDENTIFIER = MappingDataRecord(name="formulaIdentifier",
                                       length=8,
                                       values_mapping={
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
                                       })
EXPONENT = CustomFormulaDataRecord(name="Exponent",
                                   length=EXPONENT_BIT_LENGTH,
                                   encoding_formula=get_encode_signed_value_formula(EXPONENT_BIT_LENGTH),
                                   decoding_formula=get_decode_signed_value_formula(EXPONENT_BIT_LENGTH))
MANTISSA = CustomFormulaDataRecord(name="Mantissa",
                                   length=MANTISSA_BIT_LENGTH,
                                   encoding_formula=get_encode_signed_value_formula(MANTISSA_BIT_LENGTH),
                                   decoding_formula=get_decode_signed_value_formula(MANTISSA_BIT_LENGTH))

UNIT_OR_FORMAT = MappingDataRecord(name="unit/format",
                                   length=8,
                                   values_mapping={
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
                                   })

SIGNAL_ACCESS = MappingDataRecord(
    name="signalAccess",
    length=2,
    values_mapping={
        0x0: "Internal signal",  # not available in ECU connector
        0x1: "Low side switch (2 states)",  # Pull-down resistor input type
        0x2: "High side switch (2 states)",  # Pull-up resistor input type
        0x3: "Low side and high side switch (2 states)",  # Pull-up and pull-down resistor input type
    })
SIGNAL_TYPE = MappingDataRecord(name="signalType",
                                length=1,
                                values_mapping={
                                    0x0: "Input signal",
                                    0x1: "Output signal",
                                })
SIGNAL = MappingDataRecord(name="signal",
                           length=2,
                           values_mapping={
                               0x0: "Signal at low level (ground)",
                               0x1: "Signal at middle level (between ground and +)",
                               0x2: "Signal at high level (+)",
                           })
STATE = MappingDataRecord(name="state",
                          length=3,
                          values_mapping={
                              0x0: "Not Active",
                              0x1: "Active, function 1",
                              0x2: "Error detected",
                              0x3: "Not available",
                              0x4: "Active, function 2",
                          })
STATE_AND_CONNECTION_TYPE = RawDataRecord(name="stateAndConnectionType",
                                          length=8,
                                          children=(SIGNAL_ACCESS, SIGNAL_TYPE, SIGNAL, STATE))

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
                                  values_mapping={
                                      0: "reserved",
                                      1: "normalCommunicationMessages",
                                      2: "networkManagementCommunicationMessages",
                                      3: "networkManagementCommunicationMessages and normalCommunicationMessages",
                                  })
NETWORKS = MappingDataRecord(name="networks",
                                  length=4,
                                  values_mapping={
                                      0x0: "all connected networks",
                                      0xF: "network on which this request is received",
                                  } | {
                                      raw_value: f"subnet {raw_value}" for raw_value in range(1, 0xF)
                                  })
COMMUNICATION_TYPE = RawDataRecord(name="communicationType",
                                   length=8,
                                   children=(MESSAGES_TYPE, RESERVED_2BITS, NETWORKS))
NODE_IDENTIFICATION_NUMBER = MappingDataRecord(name="nodeIdentificationNumber",
                                               length=16,
                                               values_mapping={0: "reserved"})
CONDITIONAL_COMMUNICATION_CONTROL_REQUEST = ConditionalFormulaDataRecord(formula=get_communication_control_request)

# SID 0x29
CERTIFICATE_CLIENT_LENGTH = RawDataRecord(name="lengthOfCertificateClient",
                                          length=16,
                                          unit="bytes")
CONDITIONAL_CERTIFICATE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="certificateClient",
                                                        accept_zero_length=False))

CERTIFICATE_SERVER_LENGTH = RawDataRecord(name="lengthOfCertificateServer",
                                          length=16,
                                          unit="bytes")
CONDITIONAL_CERTIFICATE_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="certificateServer",
                                                        accept_zero_length=False))

CERTIFICATE_DATA_LENGTH = RawDataRecord(name="lengthOfCertificateData",
                                        length=16,
                                        unit="bytes")
CONDITIONAL_CERTIFICATE_DATA = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="certificateData",
                                                        accept_zero_length=False))

CHALLENGE_CLIENT_LENGTH = RawDataRecord(name="lengthOfChallengeClient",
                                        length=16,
                                        unit="bytes")
CONDITIONAL_CHALLENGE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="challengeClient",
                                                        accept_zero_length=False))
CONDITIONAL_OPTIONAL_CHALLENGE_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="challengeClient",
                                                        accept_zero_length=True))

CHALLENGE_SERVER_LENGTH = RawDataRecord(name="lengthOfChallengeServer",
                                        length=16,
                                        unit="bytes")
CONDITIONAL_CHALLENGE_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="challengeServer",
                                                        accept_zero_length=False))

PROOF_OF_OWNERSHIP_CLIENT_LENGTH = RawDataRecord(name="lengthOfProofOfOwnershipClient",
                                                 length=16,
                                                 unit="bytes")
CONDITIONAL_PROOF_OF_OWNERSHIP_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="proofOfOwnershipClient",
                                                        accept_zero_length=False))

PROOF_OF_OWNERSHIP_SERVER_LENGTH = RawDataRecord(name="lengthOfProofOfOwnershipServer",
                                                 length=16,
                                                 unit="bytes")
CONDITIONAL_PROOF_OF_OWNERSHIP_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="proofOfOwnershipServer",
                                                        accept_zero_length=False))

EPHEMERAL_PUBLIC_KEY_CLIENT_LENGTH = RawDataRecord(name="lengthOfEphemeralPublicKeyClient",
                                                   length=16,
                                                   unit="bytes")
CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_CLIENT = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="ephemeralPublicKeyClient",
                                                        accept_zero_length=True))

EPHEMERAL_PUBLIC_KEY_SERVER_LENGTH = RawDataRecord(name="lengthOfEphemeralPublicKeyServer",
                                                   length=16,
                                                   unit="bytes")
CONDITIONAL_OPTIONAL_EPHEMERAL_PUBLIC_KEY_SERVER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="ephemeralPublicKeyServer",
                                                        accept_zero_length=True))

NEEDED_ADDITIONAL_PARAMETER_LENGTH = RawDataRecord(name="lengthOfNeededAdditionalParameter",
                                                   length=16,
                                                   unit="bytes")
CONDITIONAL_OPTIONAL_NEEDED_ADDITIONAL_PARAMETER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="neededAdditionalParameter",
                                                        accept_zero_length=True))

ADDITIONAL_PARAMETER_LENGTH = RawDataRecord(name="lengthOfAdditionalParameter",
                                            length=16,
                                            unit="bytes")
CONDITIONAL_OPTIONAL_ADDITIONAL_PARAMETER = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="additionalParameter",
                                                        accept_zero_length=True))

SESSION_KEY_INFO_LENGTH = RawDataRecord(name="lengthOfSessionKeyInfo",
                                        length=16,
                                        unit="bytes")
CONDITIONAL_OPTIONAL_SESSION_KEY_INFO = ConditionalFormulaDataRecord(
    formula=get_formula_for_raw_data_record_with_length(data_record_name="sessionKeyInfo",
                                                        accept_zero_length=True))

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
    values_mapping={
        0x00: "RequestAccepted",
        0x01: "GeneralReject",
        0x02: "AuthenticationConfiguration",
        0x03: "AuthenticationConfiguration ACR with asymmetric cryptography",
        0x04: "AuthenticationConfiguration ACR with symmetric cryptography",
        0x10: "DeAuthentication successful",
        0x11: "CertificateVerified, OwnershipVerificationNecessary",
        0x12: "OwnershipVerified, AuthenticationComplete",
        0x13: "CertificateVerified",
    })

# SID 0x2A
TRANSMISSION_MODE = MappingDataRecord(name="transmissionMode",
                                      length=8,
                                      values_mapping={
                                          0x01: "sendAtSlowRate",
                                          0x02: "sendAtMediumRate",
                                          0x03: "sendAtFastRate",
                                          0x04: "stopSending",
                                      })

# SID 0x2C
CONDITIONAL_DATA_FROM_MEMORY = ConditionalFormulaDataRecord(formula=get_data_from_memory)

# SID 0x2F
INPUT_OUTPUT_CONTROL_PARAMETER = MappingDataRecord(name="inputOutputControlParameter",
                                                   length=8,
                                                   values_mapping={
                                                       0x00: "returnControlToECU",
                                                       0x01: "resetToDefault",
                                                       0x02: "freezeCurrentState",
                                                       0x03: "shortTermAdjustment",
                                                   })

# SID 0x36
BLOCK_SEQUENCE_COUNTER = RawDataRecord(name="blockSequenceCounter",
                                       length=8)

# SID 0x38
MODE_OF_OPERATION_2013 = MappingDataRecord(name="modeOfOperation",
                                           length=8,
                                           values_mapping={
                                               0x01: "AddFile",
                                               0x02: "DeleteFile",
                                               0x03: "ReplaceFile",
                                               0x04: "ReadFile",
                                               0x05: "ReadDir",
                                           })
MODE_OF_OPERATION_2020 = MappingDataRecord(name="modeOfOperation",
                                           length=8,
                                           values_mapping={
                                               0x01: "AddFile",
                                               0x02: "DeleteFile",
                                               0x03: "ReplaceFile",
                                               0x04: "ReadFile",
                                               0x05: "ReadDir",
                                               0x06: "ResumeFile",
                                           })

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
CONDITIONAL_MAX_NUMBER_OF_BLOCK_LENGTH_FILE_TRANSFER = ConditionalFormulaDataRecord(
    formula=get_max_number_of_block_length_file_transfer)

FILE_POSITION = RawDataRecord(name="filePosition",
                              length=64)

# SID 0x3D
CONDITIONAL_DATA = ConditionalFormulaDataRecord(formula=get_data)

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
                                           values_mapping=MAPPING_YES_NO)
IS_MESSAGE_SIGNED = MappingDataRecord(name="Message is signed.",
                                      length=1,
                                      values_mapping=MAPPING_YES_NO)
IS_MESSAGE_ENCRYPTED = MappingDataRecord(name="Message is encrypted.",
                                         length=1,
                                         values_mapping=MAPPING_YES_NO)
IS_PRE_ESTABLISHED_KEY_USED = MappingDataRecord(name="A pre-established key is used.",
                                                length=1,
                                                values_mapping=MAPPING_YES_NO)
IS_REQUEST_MESSAGE = MappingDataRecord(name="Message is request message.",
                                       length=1,
                                       values_mapping=MAPPING_YES_NO)
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

COMPARISON_LOGIC = MappingDataRecord(name="Comparison logic",
                                     length=8,
                                     values_mapping={
                                         0x01: "<",
                                         0x02: ">",
                                         0x03: "=",
                                         0x04: "<>",
                                     })
COMPARE_VALUE = RawDataRecord(name="Compare Value",
                              length=32)
HYSTERESIS_VALUE = LinearFormulaDataRecord(name="Hysteresis Value",
                                           length=8,
                                           offset=0,
                                           factor=100/255)

COMPARE_SIGN = MappingDataRecord(name="Compare Sign",
                                 length=1,
                                 values_mapping={
                                     0: "Comparison without sign",
                                     1: "Comparison with sign",
                                 })
BITS_NUMBER = CustomFormulaDataRecord(name="Bits Number",
                                      length=5,
                                      encoding_formula=lambda physical_value: 32 if physical_value == 0 else physical_value,
                                      decoding_formula=lambda raw_value: raw_value%32,
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

EVENT_TYPE_RECORD_08_2020 = get_event_type_record_08()

TIMER_SCHEDULE = MappingDataRecord(name="Timer schedule",
                                   length=8,
                                   values_mapping={
                                       0x01: "Slow rate",
                                       0x02: "Medium rate",
                                       0x03: "Fast rate",
                                   })

EVENT_TYPE_RECORD_02 = RawDataRecord(name="eventTypeRecord",
                                     length=8,
                                     children=(TIMER_SCHEDULE,))

SERVICE_TO_RESPOND = get_service_to_respond()

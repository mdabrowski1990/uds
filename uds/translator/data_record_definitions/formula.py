"""Formulas used by Conditional Data Records"""

__all__ = [
    # Shared
    "get_formula_raw_data_record_with_length",
    "get_formula_decode_float_value", "get_formula_encode_float_value",
    "get_did_2020", "get_did_2013",
    "get_dids_2020", "get_dids_2013",
    "get_did_data_2020", "get_did_data_2013",
    "get_memory_size_and_memory_address",
    "get_max_number_of_block_length",
    # SID 0x19
    "get_did_records_formula_2020", "get_did_records_formula_2013",
    # SID 0x24
    "get_scaling_byte_extension", "get_formula_scaling_byte_extension",
    "get_coefficients", "get_formula_coefficients",
    # SID 0x27
    "get_security_access_request",
    "get_security_access_response",
    # SID 0x2C
    "get_data_from_memory",
    # SID 0x2F
    "get_did_data_mask_2020", "get_did_data_mask_2013",
    # SID 0x38
    "get_file_path_and_name",
    "get_file_sizes",
    "get_file_sizes_or_dir_info",
    "get_dir_info",
    "get_max_number_of_block_length_file_transfer",
    # SID 0x3D
    "get_data",
    # SID 0x86
    "get_event_type_record_01",
    "get_event_type_record_03_2020", "get_event_type_record_03_2013",
    "get_event_type_record_07_2020", "get_event_type_record_07_2013",
    "get_event_type_record_09_2020",
    "get_event_type_record_09_2020_continuation",
]

from decimal import Decimal
from typing import Callable, List, Optional, Tuple, Union

from uds.utilities import (
    DID_BIT_LENGTH,
    DID_MAPPING_2013,
    DID_MAPPING_2020,
    DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
    DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
    EXPONENT_BIT_LENGTH,
    MANTISSA_BIT_LENGTH,
    InconsistencyError,
    get_signed_value_decoding_formula,
    get_signed_value_encoding_formula,
)

from ..data_record import (
    AbstractDataRecord,
    AliasMessageStructure,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    CustomFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
    TextDataRecord,
    TextEncoding,
)
from .did import DID_2013, DID_2020, DID_DATA_MAPPING_2013, DID_DATA_MAPPING_2020
from .dtc import DTC_EXTENDED_DATA_RECORD_NUMBER, DTC_SNAPSHOT_RECORD_NUMBER, DTC_STATUS_MASK
from .other import (
    ANTI_REPLAY_COUNTER,
    COMPARE_VALUE,
    COMPARISON_LOGIC,
    EVENT_WINDOW_TIME_MAPPING_2013,
    EVENT_WINDOW_TIME_MAPPING_2020,
    EXPONENT,
    FORMULA_IDENTIFIER,
    HYSTERESIS_VALUE,
    INTERNAL_REQUEST_PARAMETERS,
    INTERNAL_RESPONSE_PARAMETERS,
    INTERNAL_RSID,
    INTERNAL_SID,
    LOCALIZATION,
    MANTISSA,
    MEMORY_SELECTION,
    RESERVED_BIT,
    SECURITY_ACCESS_DATA,
    SECURITY_KEY,
    SECURITY_SEED,
    STATE_AND_CONNECTION_TYPE,
    TIMER_SCHEDULE_2013,
    UNIT_OR_FORMAT,
)
from .sub_functions import EVENT_TYPE_2013, EVENT_TYPE_2020, REPORT_TYPE_2020

# Shared


def get_formula_raw_data_record_with_length(data_record_name: str,
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


def get_formula_decode_float_value(exponent_bit_length: int, mantissa_bit_length: int) -> Callable[[int], float]:
    """
    Get formula for decoding float value.

    :param exponent_bit_length: Number of bits used for exponent's signed integer value.
    :param mantissa_bit_length: Number of bits used for mantissa's signed integer value.

    :return: Formula for decoding float value from unsigned integer value.
    """
    exponent_encode_formula = get_signed_value_encoding_formula(exponent_bit_length)
    mantissa_encode_formula = get_signed_value_encoding_formula(mantissa_bit_length)
    exponent_mask = ((1 << exponent_bit_length) - 1) << mantissa_bit_length
    mantissa_mask = (1 << mantissa_bit_length) - 1

    def get_float_value(value: int) -> float:
        exponent_unsigned_value = (value & exponent_mask) >> mantissa_bit_length
        mantissa_unsigned_value = value & mantissa_mask
        exponent_value: int = exponent_encode_formula(exponent_unsigned_value)
        mantissa_value: int = mantissa_encode_formula(mantissa_unsigned_value)
        return float(10 ** exponent_value) * mantissa_value
    return get_float_value


def get_formula_encode_float_value(exponent_bit_length: int, mantissa_bit_length: int) -> Callable[[float], int]:
    """
    Get formula for encoding float value.

    :param exponent_bit_length: Number of bits used for exponent's signed integer value.
    :param mantissa_bit_length: Number of bits used for mantissa's signed integer value.

    :return: Formula for encoding float value into unsigned integer value.
    """
    exponent_decode_formula = get_signed_value_decoding_formula(exponent_bit_length)
    mantissa_decode_formula = get_signed_value_decoding_formula(mantissa_bit_length)

    def get_unsinged_value(value: float) -> int:
        sign, digits, exponent_signed_value = Decimal(str(value)).normalize().as_tuple()
        if not isinstance(exponent_signed_value, int):
            raise ValueError("No handling for literal values.")
        mantissa_signed_value = int(f"{'-' if sign else ''}{''.join((str(digit) for digit in digits))}")
        exponent_unsigned_value = exponent_decode_formula(exponent_signed_value)
        mantissa_unsigned_value = mantissa_decode_formula(mantissa_signed_value)
        return (exponent_unsigned_value << mantissa_bit_length) + mantissa_unsigned_value
    return get_unsinged_value


def get_did_2020(name: str, optional: bool = False) -> MappingDataRecord:
    """
    Get `DID` Data Record compatible with ISO 14229-1:2020 version.

    :param name: Name to assign to the Data Record.
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: Created DID Data Record.
    """
    return MappingDataRecord(name=name,
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2020,
                             min_occurrences=0 if optional else 1,
                             max_occurrences=1)


def get_did_2013(name: str, optional: bool = False) -> MappingDataRecord:
    """
    Get `DID` Data Record compatible with ISO 14229-1:2013 version.

    :param name: Name to assign to the Data Record.
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: Created DID Data Record.
    """
    return MappingDataRecord(name=name,
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2013,
                             min_occurrences=0 if optional else 1,
                             max_occurrences=1)


def get_dids_2020(did_count: int,
                  record_number: Optional[int],
                  optional: bool = False) -> Tuple[Union[MappingDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get DIDs related Data Records for given record (e.g. Snapshot or Stored Data).

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param did_count: Number of DIDs that are part of the record that contains DIDs.
    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: DIDs related Data Records that are part of the record.
    """
    data_records: List[Union[MappingDataRecord, ConditionalFormulaDataRecord]] = []
    for did_number in range(1, did_count + 1):
        name = f"DID#{did_number}" if record_number is None else f"DID#{record_number}_{did_number}"
        data_records.append(get_did_2020(name=name, optional=optional))
        data_records.append(get_did_data_2020(name=f"{name} data"))
    return tuple(data_records)


def get_dids_2013(did_count: int,
                  record_number: Optional[int],
                  optional: bool = False) -> Tuple[Union[MappingDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get DIDs related Data Records for given record (e.g. Snapshot or Stored Data).

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param did_count: Number of DIDs that are part of the record that contains DIDs.
    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: DIDs related Data Records that are part of the record.
    """
    data_records: List[Union[MappingDataRecord, ConditionalFormulaDataRecord]] = []
    for did_number in range(1, did_count + 1):
        name = f"DID#{did_number}" if record_number is None else f"DID#{record_number}_{did_number}"
        data_records.append(get_did_2013(name=name, optional=optional))
        data_records.append(get_did_data_2013(name=f"{name} data"))
    return tuple(data_records)


def get_did_data_2020(name: str = "DID data") -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data that is compatible with ISO 14229-1:2020 version.

    :param name: Name for the Data Record that contains whole DID data.

    :return: Conditional Data Record for DID data.
    """
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)

    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2020.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
        return (RawDataRecord(name=name,
                              children=data_records,
                              length=total_length,
                              min_occurrences=1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])


def get_did_data_2013(name: str = "DID data") -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data that is compatible with ISO 14229-1:2013 version.

    :param name: Name for the Data Record that contains whole DID data.

    :return: Conditional Data Record for DID data.
    """
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)

    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2013.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
        return (RawDataRecord(name=name,
                              children=data_records,
                              length=total_length,
                              min_occurrences=1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])


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


# SID 0x19


def get_did_records_formula_2020(record_number: Optional[int]) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting DID related Data Records.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).

    :return: Formula for given record (e.g. Snapshot or Stored Data).
    """
    return lambda did_count: get_dids_2020(did_count=did_count,
                                           record_number=record_number)


def get_did_records_formula_2013(record_number: Optional[int]) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting DID related Data Records.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).

    :return: Formula for given record (e.g. Snapshot or Stored Data).
    """
    return lambda did_count: get_dids_2013(did_count=did_count,
                                           record_number=record_number)


# SID 0x24


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
                ConditionalFormulaDataRecord(formula=get_formula_coefficients(scaling_byte_number)),)
    if parameter_type == 0xA:  # unit/format
        return (RawDataRecord(name=f"scalingByteExtension#{scaling_byte_number}",
                              length=UNIT_OR_FORMAT.length,
                              children=(UNIT_OR_FORMAT,)),)
    if parameter_type == 0xB:  # stateAndConnectionType
        return (RawDataRecord(name=f"scalingByteExtension#{scaling_byte_number}",
                              length=STATE_AND_CONNECTION_TYPE.length,
                              children=(STATE_AND_CONNECTION_TYPE,)),)
    return ()


def get_formula_scaling_byte_extension(scaling_byte_number: int) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting scalingByteExtension Data Records.

    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :return: Formula for given scaling byte number.
    """
    return lambda scaling_byte: get_scaling_byte_extension(scaling_byte=scaling_byte,
                                                           scaling_byte_number=scaling_byte_number)


def get_coefficients(formula_identifier: int, scaling_byte_number: int) -> Tuple[CustomFormulaDataRecord, ...]:
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
        encoding_formula = get_formula_encode_float_value(exponent_bit_length=EXPONENT_BIT_LENGTH,
                                                          mantissa_bit_length=MANTISSA_BIT_LENGTH)
        decoding_formula = get_formula_decode_float_value(exponent_bit_length=EXPONENT_BIT_LENGTH,
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


def get_formula_coefficients(scaling_byte_number: int) -> Callable[[int], Tuple[CustomFormulaDataRecord, ...]]:
    """
    Get formula that can be used by Conditional Data Record for getting formula coefficients.

    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :return: Formula for given scaling byte number.
    """
    return lambda formula_identifier: get_coefficients(formula_identifier=formula_identifier,
                                                       scaling_byte_number=scaling_byte_number)


# SID 0x27


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


# SID 0x2C


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


# SID 0x2F


def get_did_data_mask_2020(name: str, optional: bool) -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data mask that is compatible with ISO 14229-1:2020 version.

    :param name: Name for the Data Record that contains whole DID data mask.
    :param optional: Whether the field is optional or mandatory.

    :return: Conditional Data Record for DID data.
    """
    default_did_data_mask = RawDataRecord(name=name,
                                          length=8,
                                          min_occurrences=0 if optional else 1,
                                          max_occurrences=None)

    def _get_mask_data_record(data_record: AbstractDataRecord) -> RawDataRecord:
        return MappingDataRecord(name=f"{data_record.name} (mask)",
                                 length=data_record.length,
                                 values_mapping={0: "no",
                                                 data_record.max_raw_value: "yes"},
                                 children=[_get_mask_data_record(child) for child in data_record.children],
                                 min_occurrences=data_record.min_occurrences,
                                 max_occurrences=data_record.max_occurrences)

    def _get_did_data_mask(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2020.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        mask_data_records = []
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
            mask_data_records.append(_get_mask_data_record(dr))
        return (RawDataRecord(name=name,
                              children=mask_data_records,
                              length=total_length,
                              min_occurrences=0 if optional else 1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data_mask,
                                        default_message_continuation=[default_did_data_mask])


def get_did_data_mask_2013(name: str, optional: bool) -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data mask that is compatible with ISO 14229-1:2013 version.

    :param name: Name for the Data Record that contains whole DID data mask.
    :param optional: Whether the field is optional or mandatory.

    :return: Conditional Data Record for DID data.
    """
    default_did_data_mask = RawDataRecord(name=name,
                                          length=8,
                                          min_occurrences=0 if optional else 1,
                                          max_occurrences=None)

    def _get_mask_data_record(data_record: AbstractDataRecord) -> RawDataRecord:
        return MappingDataRecord(name=f"{data_record.name} (mask)",
                                 length=data_record.length,
                                 values_mapping={0: "no",
                                                 data_record.max_raw_value: "yes"},
                                 children=[_get_mask_data_record(child) for child in data_record.children],
                                 min_occurrences=data_record.min_occurrences,
                                 max_occurrences=data_record.max_occurrences)

    def _get_did_data_mask(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2013.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        mask_data_records = []
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
            mask_data_records.append(_get_mask_data_record(dr))
        return (RawDataRecord(name=name,
                              children=mask_data_records,
                              length=total_length,
                              min_occurrences=0 if optional else 1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data_mask,
                                        default_message_continuation=[default_did_data_mask])


# SID 0x38


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


# SID 0x3D


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


# SID 0x84


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


# SID 0x86


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


def get_event_type_record_01(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x01.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(DTC_STATUS_MASK,))


def get_event_type_record_02_2013(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get eventTypeRecord Data Record for event equal to 0x02.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created eventTypeRecord Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(TIMER_SCHEDULE_2013,))


def get_event_type_record_03_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x03.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=DID_BIT_LENGTH,
                         children=(DID_2020,))


def get_event_type_record_03_2013(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x03.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=DID_BIT_LENGTH,
                         children=(DID_2013,))


def get_event_type_record_07_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x07.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=80,
                         children=(DID_2020,
                                   COMPARISON_LOGIC,
                                   COMPARE_VALUE,
                                   HYSTERESIS_VALUE,
                                   LOCALIZATION))


def get_event_type_record_07_2013(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x07.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=80,
                         children=(DID_2013,
                                   COMPARISON_LOGIC,
                                   COMPARE_VALUE,
                                   HYSTERESIS_VALUE,
                                   LOCALIZATION))


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


def get_event_type_record_09_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x09.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=16,
                         children=(DTC_STATUS_MASK,
                                   RESERVED_BIT,
                                   REPORT_TYPE_2020))


def get_event_type_record_09_2020_continuation(event_number: Optional[int] = None) -> ConditionalMappingDataRecord:
    """
    Get continuation for `eventTypeRecord` Data Record (`event` equal to 0x09).

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created Conditional Data Record.
    """
    if event_number is None:
        return ConditionalMappingDataRecord(mapping={0x04: (DTC_SNAPSHOT_RECORD_NUMBER,),
                                                     0x06: (DTC_EXTENDED_DATA_RECORD_NUMBER,),
                                                     0x18: (DTC_SNAPSHOT_RECORD_NUMBER, MEMORY_SELECTION),
                                                     0x19: (DTC_EXTENDED_DATA_RECORD_NUMBER, MEMORY_SELECTION), },
                                            value_mask=0x7F)
    return ConditionalMappingDataRecord(mapping={
        0x04: (MappingDataRecord(name=f"DTCSnapshotRecordNumber#{event_number}",
                                 values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                 length=8),),
        0x06: (MappingDataRecord(name=f"DTCExtDataRecordNumber#{event_number}",
                                 values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                 length=8),),
        0x18: (MappingDataRecord(name=f"DTCSnapshotRecordNumber#{event_number}",
                                 values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                 length=8),
               RawDataRecord(name=f"MemorySelection#{event_number}",
                             length=8)),
        0x19: (MappingDataRecord(name=f"DTCExtDataRecordNumber#{event_number}",
                                 values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                 length=8),
               RawDataRecord(name=f"MemorySelection#{event_number}",
                             length=8)),
    },
        value_mask=0x7F)

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

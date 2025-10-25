"""Remaining Data Records definitions."""

__all__ = [
    # Shared
    "RESERVED_BIT",
    "DATA",
    "ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER", "CONDITIONAL_MEMORY_ADDRESS_AND_SIZE",
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
]

from decimal import Decimal
from typing import Callable, Tuple

from uds.utilities import REPEATED_DATA_RECORDS_NUMBER, InconsistencyError, MANTISSA_BIT_LENGTH, EXPONENT_BIT_LENGTH

from ..data_record import (
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    CustomFormulaDataRecord,
    LinearFormulaDataRecord,
    MappingAndLinearFormulaDataRecord,
    MappingDataRecord,
    RawDataRecord,
)
from .sub_functions import DIAGNOSTIC_SESSIONS_MAPPING


# Formulas
def get_memory_size_and_memory_address(address_and_length_format_identifier: int
                                       ) -> Tuple[RawDataRecord, RawDataRecord]:
    """
    Get memoryAddress and memorySize Data Records for given addressAndLengthFormatIdentifier value.

    :param address_and_length_format_identifier: Proceeding `addressAndLengthFormatIdentifier` value.

    :return: Data Records for memoryAddress and memorySize.
    """
    memory_size_length = (address_and_length_format_identifier & 0xF0) >> 4
    memory_address_length = address_and_length_format_identifier & 0x0F
    if (not 0x00 <= address_and_length_format_identifier <= 0xFF
            or memory_address_length == 0
            or memory_size_length == 0):
        raise ValueError("Provided `addressAndLengthFormatIdentifier` value "
                         f"(0x{address_and_length_format_identifier:02X}) is incorrect as both "
                         f"memoryAddressLength ({memory_address_length}) and memorySizeLength ({memory_size_length}) "
                         "must be greater than 0.")
    return (RawDataRecord(name="memoryAddress", length=8 * memory_address_length),
            RawDataRecord(name="memorySize", length=8 * memory_size_length))


def get_scaling_byte_extension(scaling_byte: int) -> Tuple:
    parameter_type = (scaling_byte & 0xF0) >> 4
    number_of_bytes = scaling_byte & 0x0F
    if not 0x00 <= scaling_byte <= 0xFF:
        raise ValueError(f"Provided `scalingByte` value is out of range: 0x{scaling_byte:02X}.")
    if parameter_type == 0x2:  # bitMappedReportedWithOutMask
        if number_of_bytes == 0:
            raise InconsistencyError("Provided `scalingByte` value is incorrect (0x20) - byte length equals 0.")
        return (RawDataRecord(name="ValidityMask",
                              length=8*number_of_bytes),)
    if parameter_type == 0x9:  # formula
        return (FORMULA_IDENTIFIER,
                ConditionalFormulaDataRecord(formula=get_data_records_for_formula_parameters))
    # TODO: more cases
    return ()


def get_data_records_for_formula_parameters(formula_identifier: int) -> Tuple[CustomFormulaDataRecord, ...]:
    """
    Get Data Records for formula type parameter.

    :param formula_identifier: Formula Identifier used by the parameter.

    :return: Tuple with Data Records for given formula type parameter.
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
            data_records.append(CustomFormulaDataRecord(name=f"C{constant_index}",
                                                        length=length,
                                                        children=(EXPONENT, MANTISSA),
                                                        encoding_formula=encoding_formula,
                                                        decoding_formula=decoding_formula))
            constant_index += 1
        return tuple(data_records)
    raise ValueError(f"Unknown formula identifier was provided: 0x{formula_identifier:02X}.")


def get_decode_signed_value_formula(bit_length: int) -> Callable[[int], int]:
    """
    Get formula for decoding signed integer value.

    :param bit_length: Number of bits used for signed integer value.

    :raise TypeError: Provided value is not int type.
    :raise ValueError: Provided value is out of range.

    :return: Formula for decoding singed integer value from unsinged integer value.
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
        exponent_signed_value = (value & exponent_mask) >> mantissa_bit_length
        mantissa_signed_value = value & mantissa_mask
        exponent_value = exponent_encode_formula(exponent_signed_value)
        mantissa_value = mantissa_encode_formula(mantissa_signed_value)
        return (10 ** exponent_value) * mantissa_value
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
        mantissa_signed_value = int(f"{'-' if sign else ''}{''.join((str(digit) for digit in digits))}")
        exponent_unsigned_value = exponent_decode_formula(exponent_signed_value)
        mantissa_unsigned_value = mantissa_decode_formula(mantissa_signed_value)
        return (exponent_unsigned_value << mantissa_bit_length) + mantissa_unsigned_value
    return get_unsinged_value

# Shared
RESERVED_BIT = RawDataRecord(name="Reserved",
                             length=1)

DATA = RawDataRecord(name="Data",
                     length=8,
                     min_occurrences=1,
                     max_occurrences=None)

MEMORY_ADDRESS_LENGTH = RawDataRecord(name="memoryAddressLength",
                                      length=4)
MEMORY_SIZE_LENGTH = RawDataRecord(name="memorySizeLength",
                                   length=4)
ADDRESS_AND_LENGTH_FORMAT_IDENTIFIER = RawDataRecord(name="addressAndLengthFormatIdentifier",
                                                     length=8,
                                                     children=(MEMORY_SIZE_LENGTH, MEMORY_ADDRESS_LENGTH))

CONDITIONAL_MEMORY_ADDRESS_AND_SIZE = ConditionalFormulaDataRecord(formula=get_memory_size_and_memory_address)

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
                                                    values_mapping={0xFF: "ERROR"},
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
FORMULA_IDENTIFIER = MappingDataRecord(name="FormulaIdentifier",
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
SCALING_BYTE_TYPE = MappingDataRecord(name="Type",
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
SCALING_BYTE_LENGTH = RawDataRecord(name="NumberOfBytes",
                                    length=4,
                                    unit="bytes")
SCALING_BYTES_LIST = [RawDataRecord(name=f"scalingByte#{record_number + 1}",
                                    children=(SCALING_BYTE_TYPE, SCALING_BYTE_LENGTH),
                                    length=8,
                                    min_occurrences=1 if record_number == 0 else 0,
                                    max_occurrences=1)
                      for record_number in range(REPEATED_DATA_RECORDS_NUMBER)]

# ConditionalFormulaDataRecord()
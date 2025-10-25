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

from typing import Tuple, Callable
from uds.utilities import REPEATED_DATA_RECORDS_NUMBER, InconsistencyError

from ..data_record import (
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    LinearFormulaDataRecord,
    CustomFormulaDataRecord,
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
                ConditionalFormulaDataRecord(formula=get_formula_parameters))
    return ()


def get_formula_parameters(formula_identifier: int) -> Tuple[CustomFormulaDataRecord, ...]:
    physical_value = FORMULA_IDENTIFIER.get_physical_value(formula_identifier)
    if isinstance(physical_value, str) and "C0" in physical_value:
        data_records = []
        constant_index = 0
        while f"C{constant_index}" in physical_value:
            ...  # TODO: create custom formula data records using float formulas
    raise ValueError(f"Unknown formula identifier was provided: 0x{formula_identifier:02X}.")


def get_encode_signed_value_formula(bits: int) -> Callable[[int], int]:
    def encode_signed_value(value: int) -> int:
        max_value = (1 << bits) - 1
        msb = 1 << (bits - 1)
        if not 0 <= value <= max_value:
            raise ValueError(f"Provided value is out of range (0 <= value <= {max_value}): {value}.")
        return (- (value & msb)) + (value & (max_value ^ msb))
    return encode_signed_value


def get_decode_signed_value_formula(bits: int) -> Callable[[int], int]:
    def decode_signed_value(value: int) -> int:
        msb = 1 << (bits - 1)
        min_value = - msb
        max_value = msb - 1
        if not min_value <= value <= max_value:
            raise ValueError(f"Provided value is out of range ({min_value} <= value <= {max_value}): {value}.")
        if value >= 0:
            return value
        return 2*msb + value
    return decode_signed_value


# TODO: formulas (encode and decode) for float with various length (current use case 4 bit exponent, 12 bit mantissa)


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
                                   length=4,
                                   encoding_formula=get_encode_signed_value_formula(4),
                                   decoding_formula=get_decode_signed_value_formula(4))
MANTISSA = CustomFormulaDataRecord(name="Mantissa",
                                   length=12,
                                   encoding_formula=get_encode_signed_value_formula(12),
                                   decoding_formula=get_decode_signed_value_formula(12))
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
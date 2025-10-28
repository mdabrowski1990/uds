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
    "SCALING_DATA_RECORDS",
    # SID 0x27
    "CONDITIONAL_SECURITY_ACCESS_REQUEST", "CONDITIONAL_SECURITY_ACCESS_RESPONSE",
    # SID 28
    "CONDITIONAL_COMMUNICATION_CONTROL_REQUEST"
]

from decimal import Decimal
from typing import Callable, Tuple, Union

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


def get_scaling_byte_extension(scaling_byte: int,
                               scaling_byte_number: int
                               ) -> Tuple[Union[RawDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get scalingByteExtension Data Records for given scalingByte value.

    :param scaling_byte: Proceeding `scalingByte` value.
    :param scaling_byte_number: Order numbers of the scalingByte and scalingByteExtension Data Records.

    :return: Data Records for scalingByteExtension.
    """
    parameter_type = (scaling_byte & 0xF0) >> 4
    number_of_bytes = scaling_byte & 0x0F
    if not 0x00 <= scaling_byte <= 0xFF:
        raise ValueError(f"Provided `scalingByte#{scaling_byte_number}` value is out of range: "
                         f"0x{scaling_byte:02X}.")
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
        # TODO: ISO 14229-1 does not explain how to combine units (e.g. Volt [V]) and prefixes (e.g. milli [m])/formulas
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


# Shared
RESERVED_BIT = RawDataRecord(name="reserved",
                             length=1)
RESERVED_2BITS = RawDataRecord(name="reserved",
                               length=2)

DATA = RawDataRecord(name="data",
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
CONDITIONAL_SECURITY_ACCESS_REQUEST = ConditionalFormulaDataRecord(
    formula=lambda security_access_type: (SECURITY_ACCESS_DATA, ) if security_access_type % 2 else (SECURITY_KEY, ))
CONDITIONAL_SECURITY_ACCESS_RESPONSE = ConditionalFormulaDataRecord(
    formula=lambda security_access_type: (SECURITY_SEED, ) if security_access_type % 2 else ())

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
CONDITIONAL_COMMUNICATION_CONTROL_REQUEST = ConditionalFormulaDataRecord(
    formula=lambda control_type: (COMMUNICATION_TYPE, NODE_IDENTIFICATION_NUMBER) if control_type & 0x7F in {0x04, 0x05}
    else (COMMUNICATION_TYPE,))

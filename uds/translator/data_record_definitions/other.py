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
]

from typing import Tuple

from ..data_record import (
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
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

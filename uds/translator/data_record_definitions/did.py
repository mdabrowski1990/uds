"""Data Records definitions for :ref:`Data Identifiers <knowledge-base-did>`."""

__all__ = [
    # Shared
    "DID_DATA_MAPPING_2020", "DID_DATA_MAPPING_2013",
    "DID_2020", "DID_2013",
    "MULTIPLE_DID_2020", "MULTIPLE_DID_2013",
    # SID 0x2A
    "OPTIONAL_PERIODIC_DID", "MULTIPLE_PERIODIC_DID", "OPTIONAL_MULTIPLE_PERIODIC_DID",
    # SID 0x2C
    "DYNAMICALLY_DEFINED_DID_2020", "DYNAMICALLY_DEFINED_DID_2013",
    "OPTIONAL_DYNAMICALLY_DEFINED_DID_2020", "OPTIONAL_DYNAMICALLY_DEFINED_DID_2013",
    "SOURCE_DID_2020", "SOURCE_DID_2013",
    "POSITION_IN_DID",
    "DID_MEMORY_SIZE",
    "DATA_FROM_DID_2020", "DATA_FROM_DID_2013",
]


from typing import Dict

from uds.utilities import (
    DID_BIT_LENGTH,
    DID_MAPPING_2013,
    DID_MAPPING_2020,
    PERIODIC_DID_BIT_LENGTH,
    PERIODIC_DID_OFFSET,
)

from ..data_record import AliasMessageStructure, LinearFormulaDataRecord, MappingDataRecord, RawDataRecord
from .other import ACTIVE_DIAGNOSTIC_SESSION, RESERVED_BIT

# Shared

DID_DATA_MAPPING_2020: Dict[int, AliasMessageStructure] = {
    0xF186: (RESERVED_BIT, ACTIVE_DIAGNOSTIC_SESSION),
}
"""DID values mapping (compatible with ISO 14229-1:2020) to DID data message structure."""
DID_DATA_MAPPING_2013: Dict[int, AliasMessageStructure] = {
    0xF186: DID_DATA_MAPPING_2020[0xF186],
}
"""DID values mapping (compatible with ISO 14229-1:2013) to DID data message structure."""

DID_2020 = MappingDataRecord(name="DID",
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2020)
"""Definition of :ref:`DID <knowledge-base-did>` Data Record (compatible with ISO 14229-1:2020)."""
DID_2013 = MappingDataRecord(name="DID",
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2013)
"""Definition of :ref:`DID <knowledge-base-did>` Data Record (compatible with ISO 14229-1:2013)."""

MULTIPLE_DID_2020 = MappingDataRecord(name="DID",
                                      length=DID_BIT_LENGTH,
                                      values_mapping=DID_MAPPING_2020,
                                      min_occurrences=1,
                                      max_occurrences=None)
"""Definition of multiple :ref:`DIDs <knowledge-base-did>` Data Record (compatible with ISO 14229-1:2020)."""
MULTIPLE_DID_2013 = MappingDataRecord(name="DID",
                                      length=DID_BIT_LENGTH,
                                      values_mapping=DID_MAPPING_2013,
                                      min_occurrences=1,
                                      max_occurrences=None)
"""Definition of multiple :ref:`DIDs <knowledge-base-did>` Data Record (compatible with ISO 14229-1:2013)."""

# SID 0x2A

OPTIONAL_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                length=PERIODIC_DID_BIT_LENGTH,
                                                offset=PERIODIC_DID_OFFSET,
                                                factor=1,
                                                min_occurrences=0,
                                                max_occurrences=1)
"""Definition of optional `Periodic DID` Data Record."""

MULTIPLE_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                length=PERIODIC_DID_BIT_LENGTH,
                                                offset=PERIODIC_DID_OFFSET,
                                                factor=1,
                                                min_occurrences=1,
                                                max_occurrences=None)
"""Definition of multiple `Periodic DID` Data Record."""

OPTIONAL_MULTIPLE_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                         length=PERIODIC_DID_BIT_LENGTH,
                                                         offset=PERIODIC_DID_OFFSET,
                                                         factor=1,
                                                         min_occurrences=0,
                                                         max_occurrences=None)
"""Definition of optional, multiple `Periodic DID` Data Record."""

# SID 0x2C

DYNAMICALLY_DEFINED_DID_2020 = MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
                                                 length=DID_BIT_LENGTH,
                                                 values_mapping=DID_MAPPING_2020)
"""Definition of `dynamicallyDefinedDataIdentifier` Data Record (compatible with ISO 14229-1:2020)."""
DYNAMICALLY_DEFINED_DID_2013 = MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
                                                 length=DID_BIT_LENGTH,
                                                 values_mapping=DID_MAPPING_2013)
"""Definition of `dynamicallyDefinedDataIdentifier` Data Record (compatible with ISO 14229-1:2020)."""

OPTIONAL_DYNAMICALLY_DEFINED_DID_2020 = MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
                                                          length=DID_BIT_LENGTH,
                                                          values_mapping=DID_MAPPING_2020,
                                                          min_occurrences=0,
                                                          max_occurrences=1)
"""Definition of optional `dynamicallyDefinedDataIdentifier` Data Record (compatible with ISO 14229-1:2020)."""
OPTIONAL_DYNAMICALLY_DEFINED_DID_2013 = MappingDataRecord(name="dynamicallyDefinedDataIdentifier",
                                                          length=DID_BIT_LENGTH,
                                                          values_mapping=DID_MAPPING_2013,
                                                          min_occurrences=0,
                                                          max_occurrences=1)
"""Definition of optional `dynamicallyDefinedDataIdentifier` Data Record (compatible with ISO 14229-1:2013)"""

SOURCE_DID_2020 = MappingDataRecord(name="sourceDataIdentifier",
                                    length=DID_BIT_LENGTH,
                                    values_mapping=DID_MAPPING_2020)
"""Definition of Source :ref:`DID <knowledge-base-did>` Data Record (compatible with ISO 14229-1:2020)."""
SOURCE_DID_2013 = MappingDataRecord(name="sourceDataIdentifier",
                                    length=DID_BIT_LENGTH,
                                    values_mapping=DID_MAPPING_2013)
"""Definition of Source :ref:`DID <knowledge-base-did>` Data Record (compatible with ISO 14229-1:2013)."""

POSITION_IN_DID = RawDataRecord(name="positionInSourceDataRecord",
                                length=8)
"""Definition of `positionInSourceDataRecord` Data Record."""

DID_MEMORY_SIZE = RawDataRecord(name="memorySize",
                                length=8,
                                unit="bytes")
"""Definition of `memorySize` Data Record."""

DATA_FROM_DID_2020 = RawDataRecord(name="Data from DID",
                                   length=32,
                                   children=(
                                       SOURCE_DID_2020,
                                       POSITION_IN_DID,
                                       DID_MEMORY_SIZE
                                   ),
                                   min_occurrences=1,
                                   max_occurrences=None)
"""Definition of `Data from DID` Data Record (compatible with ISO 14229-1:2020)."""
DATA_FROM_DID_2013 = RawDataRecord(name="Data from DID",
                                   length=32,
                                   children=(
                                       SOURCE_DID_2013,
                                       POSITION_IN_DID,
                                       DID_MEMORY_SIZE
                                   ),
                                   min_occurrences=1,
                                   max_occurrences=None)
"""Definition of `Data from DID` Data Record (compatible with ISO 14229-1:2013)."""

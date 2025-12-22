"""Data Records definitions for :ref:`Data Identifiers <knowledge-base-did>`."""

__all__ = [
    "DID_2020", "DID_2013",
    "DID_DATA_MAPPING_2020", "DID_DATA_MAPPING_2013",
    "DYNAMICALLY_DEFINED_DID", "OPTIONAL_DYNAMICALLY_DEFINED_DID", "OPTIONAL_PERIODIC_DID",
    "MULTIPLE_DID_2020", "MULTIPLE_DID_2013",
    "MULTIPLE_PERIODIC_DID", "OPTIONAL_MULTIPLE_PERIODIC_DID",
    "DATA_FROM_DID_2013", "DATA_FROM_DID_2020",
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

DID_DATA_MAPPING_2020: Dict[int, AliasMessageStructure] = {
    0xF186: (RESERVED_BIT, ACTIVE_DIAGNOSTIC_SESSION),
}
"""DID values mapping (compatible with ISO 14229-1:2020) to DID data message structure."""
DID_DATA_MAPPING_2013: Dict[int, AliasMessageStructure] = {
    0xF186: DID_DATA_MAPPING_2020[0xF186],
}
"""DID values mapping (compatible with ISO 14229-1:2013) to DID data message structure."""


DID_2013 = MappingDataRecord(name="DID",
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2013)
DID_2020 = MappingDataRecord(name="DID",
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2020)
SOURCE_DID_2013 = MappingDataRecord(name="sourceDataIdentifier",
                                    length=DID_BIT_LENGTH,
                                    values_mapping=DID_MAPPING_2013)
SOURCE_DID_2020 = MappingDataRecord(name="sourceDataIdentifier",
                                    length=DID_BIT_LENGTH,
                                    values_mapping=DID_MAPPING_2020)
DYNAMICALLY_DEFINED_DID = RawDataRecord(name="dynamicallyDefinedDataIdentifier",
                                        length=DID_BIT_LENGTH)
OPTIONAL_DYNAMICALLY_DEFINED_DID = RawDataRecord(name="dynamicallyDefinedDataIdentifier",
                                                 length=DID_BIT_LENGTH,
                                                 min_occurrences=0,
                                                 max_occurrences=1)
OPTIONAL_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                length=PERIODIC_DID_BIT_LENGTH,
                                                offset=PERIODIC_DID_OFFSET,
                                                factor=1,
                                                min_occurrences=0,
                                                max_occurrences=1)
MULTIPLE_DID_2013 = MappingDataRecord(name="DID",
                                      length=DID_BIT_LENGTH,
                                      values_mapping=DID_MAPPING_2013,
                                      min_occurrences=1,
                                      max_occurrences=None)
MULTIPLE_DID_2020 = MappingDataRecord(name="DID",
                                      length=DID_BIT_LENGTH,
                                      values_mapping=DID_MAPPING_2020,
                                      min_occurrences=1,
                                      max_occurrences=None)
MULTIPLE_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                length=PERIODIC_DID_BIT_LENGTH,
                                                offset=PERIODIC_DID_OFFSET,
                                                factor=1,
                                                min_occurrences=1,
                                                max_occurrences=None)
OPTIONAL_MULTIPLE_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                         length=PERIODIC_DID_BIT_LENGTH,
                                                         offset=PERIODIC_DID_OFFSET,
                                                         factor=1,
                                                         min_occurrences=0,
                                                         max_occurrences=None)

POSITION_IN_DID = RawDataRecord(name="positionInSourceDataRecord",
                                length=8)
DID_MEMORY_SIZE = RawDataRecord(name="memorySize",
                                length=8,
                                unit="bytes")

DATA_FROM_DID_2013 = RawDataRecord(name="Data from DID",
                                   length=32,
                                   children=(
                                       SOURCE_DID_2013,
                                       POSITION_IN_DID,
                                       DID_MEMORY_SIZE
                                   ),
                                   min_occurrences=1,
                                   max_occurrences=None)
DATA_FROM_DID_2020 = RawDataRecord(name="Data from DID",
                                   length=32,
                                   children=(
                                       SOURCE_DID_2020,
                                       POSITION_IN_DID,
                                       DID_MEMORY_SIZE
                                   ),
                                   min_occurrences=1,
                                   max_occurrences=None)


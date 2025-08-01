"""
Package with implementation for all type of Data Records.

Each Data Record contains mapping (translation) of raw data (sequence of bits in diagnostic message payload) to some
meaningful information (e.g. physical value, text).
"""

from .abstract_data_record import (
    AbstractDataRecord,
    MultipleOccurrencesInfo,
    MultiplePhysicalValues,
    PhysicalValueAlias,
    SingleOccurrenceInfo,
    SinglePhysicalValueAlias,
)
from .conditional_data_record import (
    DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION,
    AbstractConditionalDataRecord,
    AliasMessageStructure,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
)
from .mapping_data_record import MappingDataRecord
from .raw_data_record import RawDataRecord
from .text_data_record import TextDataRecord, TextEncoding

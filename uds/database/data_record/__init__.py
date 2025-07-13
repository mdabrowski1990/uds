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
from .mapping_data_record import MappingDataRecord
from .raw_data_record import RawDataRecord

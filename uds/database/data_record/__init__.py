"""
Package with implementation for all type of Data Records.

Each Data Record contains mapping (translation) of raw data (sequence of bits in diagnostic message payload) to some
meaningful information (e.g. physical value, text).
"""

__all__ = [
    "AbstractDataRecord", "DataRecordPhysicalValueAlias", "DataRecordValueAlias", "DecodedDataRecord",
    "RawDataRecord",
]

from .abstract_data_record import (
    AbstractDataRecord,
    DataRecordPhysicalValueAlias,
    DataRecordValueAlias,
    DecodedDataRecord,
)
from .raw_data_record import RawDataRecord

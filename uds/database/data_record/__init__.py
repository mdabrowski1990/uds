"""
Package with implementation for all type of Data Records.

Each Data Record contains mapping (translation) of raw data (sequence of bits in diagnostic message payload) to some
meaningful information (e.g. physical value, text).
"""

from .abstract_data_record import (
    AbstractDataRecord,
    PhysicalValueAlias,
)
# from .raw_data_record import RawDataRecord  # TODO
# TODO: mapping and container

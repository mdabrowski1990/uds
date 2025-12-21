"""Formulas used by Conditional Data Records"""

__all__ = [
    "get_event_type_record_01",
    "get_event_type_record_09_2020",
    "get_conditional_event_type_record_09_2020",
]

from typing import Optional
from uds.utilities import (
    DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
    DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
)

from ..data_record import (
    ConditionalMappingDataRecord,
    MappingDataRecord,
    RawDataRecord,
)
from .other import MEMORY_SELECTION, RESERVED_BIT
from .sub_functions import REPORT_TYPE_2020
from .dtc import DTC_STATUS_MASK, DTC_SNAPSHOT_RECORD_NUMBER, DTC_EXTENDED_DATA_RECORD_NUMBER


# SID 0x86

def get_event_type_record_01(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x01.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=8,
                         children=(DTC_STATUS_MASK,))


def get_event_type_record_09_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x09.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=16,
                         children=(DTC_STATUS_MASK,
                                   RESERVED_BIT,
                                   REPORT_TYPE_2020))


def get_conditional_event_type_record_09_2020(event_number: Optional[int] = None) -> ConditionalMappingDataRecord:
    """
    Get continuation for `eventTypeRecord` Data Record (`event` equal to 0x09).

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created Conditional Data Record.
    """
    if event_number is None:
        return ConditionalMappingDataRecord(mapping={0x04: (DTC_SNAPSHOT_RECORD_NUMBER,),
                                                     0x06: (DTC_EXTENDED_DATA_RECORD_NUMBER,),
                                                     0x18: (DTC_SNAPSHOT_RECORD_NUMBER, MEMORY_SELECTION),
                                                     0x19: (DTC_EXTENDED_DATA_RECORD_NUMBER, MEMORY_SELECTION), },
                                            value_mask=0x7F)
    return ConditionalMappingDataRecord(mapping={
        0x04: (MappingDataRecord(name=f"DTCSnapshotRecordNumber#{event_number}",
                                 values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                 length=8),),
        0x06: (MappingDataRecord(name=f"DTCExtDataRecordNumber#{event_number}",
                                 values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                 length=8),),
        0x18: (MappingDataRecord(name=f"DTCSnapshotRecordNumber#{event_number}",
                                 values_mapping=DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
                                 length=8),
               RawDataRecord(name=f"MemorySelection#{event_number}",
                             length=8)),
        0x19: (MappingDataRecord(name=f"DTCExtDataRecordNumber#{event_number}",
                                 values_mapping=DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
                                 length=8),
               RawDataRecord(name=f"MemorySelection#{event_number}",
                             length=8)),
    },
        value_mask=0x7F)

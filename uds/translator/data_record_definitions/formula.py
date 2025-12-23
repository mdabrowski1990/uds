"""Formulas used by Conditional Data Records"""

__all__ = [
    # Shared
    "get_formula_for_raw_data_record_with_length",
    "get_did_2020", "get_did_2013",
    "get_dids_2020", "get_dids_2013",
    "get_did_data_2020", "get_did_data_2013",
    "get_memory_size_and_memory_address",
    # SID 0x19
    "get_did_records_formula_2020", "get_did_records_formula_2013",
    # SID 0x2F
    "get_did_data_mask_2020", "get_did_data_mask_2013",
    # SID 0x86
    "get_event_type_record_01",
    "get_event_type_record_03_2020", "get_event_type_record_03_2013",
    "get_event_type_record_07_2020", "get_event_type_record_07_2013",
    "get_event_type_record_09_2020",
    "get_conditional_event_type_record_09_2020",
]

from typing import Callable, List, Optional, Tuple, Union

from uds.utilities import (
    DID_BIT_LENGTH,
    DID_MAPPING_2013,
    DID_MAPPING_2020,
    DTC_EXTENDED_DATA_RECORD_NUMBER_MAPPING,
    DTC_SNAPSHOT_RECORD_NUMBER_MAPPING,
)

from ..data_record import (
    AbstractDataRecord,
    AliasMessageStructure,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    MappingDataRecord,
    RawDataRecord,
)
from .did import DID_2013, DID_2020, DID_DATA_MAPPING_2013, DID_DATA_MAPPING_2020
from .dtc import DTC_EXTENDED_DATA_RECORD_NUMBER, DTC_SNAPSHOT_RECORD_NUMBER, DTC_STATUS_MASK
from .other import COMPARE_VALUE, COMPARISON_LOGIC, HYSTERESIS_VALUE, LOCALIZATION, MEMORY_SELECTION, RESERVED_BIT
from .sub_functions import REPORT_TYPE_2020

# Shared


def get_formula_for_raw_data_record_with_length(data_record_name: str,
                                                accept_zero_length: bool
                                                ) -> Callable[[int], Union[Tuple[RawDataRecord], Tuple[()]]]:
    """
    Get formula for Conditional Data Record that returns Raw Data Record with given name.

    :param data_record_name: Name for Raw Data Record name.
    :param accept_zero_length: True to accept length equal zero else False.

    :return: Formula for creating Raw Data Record that is proceeded by (bytes) length parameter.
    """
    def get_raw_data_record(length: int) -> Union[Tuple[RawDataRecord], Tuple[()]]:
        if accept_zero_length and length == 0:
            return ()
        if length > 0:
            return (RawDataRecord(name=data_record_name,
                                  length=8,
                                  min_occurrences=length,
                                  max_occurrences=length,
                                  enforce_reoccurring=True),)
        raise ValueError("Unexpected length value provided. "
                         f"Expected: {0 if accept_zero_length else 1} <= length (int type). "
                         f"Actual value: {length!r}.")
    return get_raw_data_record


def get_did_2020(name: str, optional: bool = False) -> MappingDataRecord:
    """
    Get `DID` Data Record compatible with ISO 14229-1:2020 version.

    :param name: Name to assign to the Data Record.
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: Created DID Data Record.
    """
    return MappingDataRecord(name=name,
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2020,
                             min_occurrences=0 if optional else 1,
                             max_occurrences=1)


def get_did_2013(name: str, optional: bool = False) -> MappingDataRecord:
    """
    Get `DID` Data Record compatible with ISO 14229-1:2013 version.

    :param name: Name to assign to the Data Record.
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: Created DID Data Record.
    """
    return MappingDataRecord(name=name,
                             length=DID_BIT_LENGTH,
                             values_mapping=DID_MAPPING_2013,
                             min_occurrences=0 if optional else 1,
                             max_occurrences=1)


def get_dids_2020(did_count: int,
                  record_number: Optional[int],
                  optional: bool = False) -> Tuple[Union[MappingDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get DIDs related Data Records for given record (e.g. Snapshot or Stored Data).

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param did_count: Number of DIDs that are part of the record that contains DIDs.
    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: DIDs related Data Records that are part of the record.
    """
    data_records: List[Union[MappingDataRecord, ConditionalFormulaDataRecord]] = []
    for did_number in range(1, did_count + 1):
        name = f"DID#{did_number}" if record_number is None else f"DID#{record_number}_{did_number}"
        data_records.append(get_did_2020(name=name, optional=optional))
        data_records.append(get_did_data_2020(name=f"{name} data"))
    return tuple(data_records)


def get_dids_2013(did_count: int,
                  record_number: Optional[int],
                  optional: bool = False) -> Tuple[Union[MappingDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get DIDs related Data Records for given record (e.g. Snapshot or Stored Data).

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param did_count: Number of DIDs that are part of the record that contains DIDs.
    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: DIDs related Data Records that are part of the record.
    """
    data_records: List[Union[MappingDataRecord, ConditionalFormulaDataRecord]] = []
    for did_number in range(1, did_count + 1):
        name = f"DID#{did_number}" if record_number is None else f"DID#{record_number}_{did_number}"
        data_records.append(get_did_2013(name=name, optional=optional))
        data_records.append(get_did_data_2013(name=f"{name} data"))
    return tuple(data_records)


def get_did_data_2020(name: str = "DID data") -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data that is compatible with ISO 14229-1:2020 version.

    :param name: Name for the Data Record that contains whole DID data.

    :return: Conditional Data Record for DID data.
    """
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)

    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2020.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
        return (RawDataRecord(name=name,
                              children=data_records,
                              length=total_length,
                              min_occurrences=1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])


def get_did_data_2013(name: str = "DID data") -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data that is compatible with ISO 14229-1:2013 version.

    :param name: Name for the Data Record that contains whole DID data.

    :return: Conditional Data Record for DID data.
    """
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)

    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2013.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
        return (RawDataRecord(name=name,
                              children=data_records,
                              length=total_length,
                              min_occurrences=1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])


def get_memory_size_and_memory_address(address_and_length_format_identifier: int
                                       ) -> Tuple[RawDataRecord, RawDataRecord]:
    """
    Get `memoryAddress` and `memorySize` Data Records for given `addressAndLengthFormatIdentifier` value.

    :param address_and_length_format_identifier: Proceeding `addressAndLengthFormatIdentifier` value.

    :raise ValueError: At least one of the `addressAndLengthFormatIdentifier` nibbles
        (`memoryAddressLength` or `memorySizeLength`) equals 0.

    :return: Tuple with `memoryAddress` and `memorySize` Data Records.
    """
    memory_size_length = (address_and_length_format_identifier & 0xF0) >> 4
    memory_address_length = address_and_length_format_identifier & 0x0F
    if memory_address_length == 0 or memory_size_length == 0:
        raise ValueError("Provided `addressAndLengthFormatIdentifier` value "
                         f"(0x{address_and_length_format_identifier:02X}) is incorrect as both contained values"
                         f"`memoryAddressLength` ({memory_address_length}) and "
                         f"`memorySizeLength` ({memory_size_length}) must be greater than 0.")
    return (RawDataRecord(name="memoryAddress", length=8 * memory_address_length),
            RawDataRecord(name="memorySize", length=8 * memory_size_length, unit="bytes"))


# SID 0x19


def get_did_records_formula_2020(record_number: Optional[int]) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting DID related Data Records.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).

    :return: Formula for given record (e.g. Snapshot or Stored Data).
    """
    return lambda did_count: get_dids_2020(did_count=did_count,
                                           record_number=record_number)


def get_did_records_formula_2013(record_number: Optional[int]) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting DID related Data Records.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).

    :return: Formula for given record (e.g. Snapshot or Stored Data).
    """
    return lambda did_count: get_dids_2013(did_count=did_count,
                                           record_number=record_number)


# SID 0x2F


def get_did_data_mask_2020(name: str, optional: bool) -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data mask that is compatible with ISO 14229-1:2020 version.

    :param name: Name for the Data Record that contains whole DID data mask.
    :param optional: Whether the field is optional or mandatory.

    :return: Conditional Data Record for DID data.
    """
    default_did_data_mask = RawDataRecord(name=name,
                                          length=8,
                                          min_occurrences=0 if optional else 1,
                                          max_occurrences=None)

    def _get_mask_data_record(data_record: AbstractDataRecord) -> RawDataRecord:
        return MappingDataRecord(name=f"{data_record.name} (mask)",
                                 length=data_record.length,
                                 values_mapping={0: "no",
                                                 data_record.max_raw_value: "yes"},
                                 children=[_get_mask_data_record(child) for child in data_record.children],
                                 min_occurrences=data_record.min_occurrences,
                                 max_occurrences=data_record.max_occurrences)

    def _get_did_data_mask(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2020.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        mask_data_records = []
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
            mask_data_records.append(_get_mask_data_record(dr))
        return (RawDataRecord(name=name,
                              children=mask_data_records,
                              length=total_length,
                              min_occurrences=0 if optional else 1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data_mask,
                                        default_message_continuation=[default_did_data_mask])


def get_did_data_mask_2013(name: str, optional: bool) -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data mask that is compatible with ISO 14229-1:2013 version.

    :param name: Name for the Data Record that contains whole DID data mask.
    :param optional: Whether the field is optional or mandatory.

    :return: Conditional Data Record for DID data.
    """
    default_did_data_mask = RawDataRecord(name=name,
                                          length=8,
                                          min_occurrences=0 if optional else 1,
                                          max_occurrences=None)

    def _get_mask_data_record(data_record: AbstractDataRecord) -> RawDataRecord:
        return MappingDataRecord(name=f"{data_record.name} (mask)",
                                 length=data_record.length,
                                 values_mapping={0: "no",
                                                 data_record.max_raw_value: "yes"},
                                 children=[_get_mask_data_record(child) for child in data_record.children],
                                 min_occurrences=data_record.min_occurrences,
                                 max_occurrences=data_record.max_occurrences)

    def _get_did_data_mask(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2013.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        mask_data_records = []
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
            mask_data_records.append(_get_mask_data_record(dr))
        return (RawDataRecord(name=name,
                              children=mask_data_records,
                              length=total_length,
                              min_occurrences=0 if optional else 1,
                              max_occurrences=1),)

    return ConditionalFormulaDataRecord(formula=_get_did_data_mask,
                                        default_message_continuation=[default_did_data_mask])


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


def get_event_type_record_03_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x03.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=DID_BIT_LENGTH,
                         children=(DID_2020,))


def get_event_type_record_03_2013(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x03.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=DID_BIT_LENGTH,
                         children=(DID_2013,))


def get_event_type_record_07_2020(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x07.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=80,
                         children=(DID_2020,
                                   COMPARISON_LOGIC,
                                   COMPARE_VALUE,
                                   HYSTERESIS_VALUE,
                                   LOCALIZATION))


def get_event_type_record_07_2013(event_number: Optional[int] = None) -> RawDataRecord:
    """
    Get `eventTypeRecord` Data Record for `event` equal to 0x07.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param event_number: Order number of the event record to contain this Data Record.
        None if there are no records.

    :return: Created `eventTypeRecord` Data Record.
    """
    return RawDataRecord(name="eventTypeRecord" if event_number is None else f"eventTypeRecord#{event_number}",
                         length=80,
                         children=(DID_2013,
                                   COMPARISON_LOGIC,
                                   COMPARE_VALUE,
                                   HYSTERESIS_VALUE,
                                   LOCALIZATION))


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

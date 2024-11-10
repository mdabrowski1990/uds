import pytest

from uds.database.data_record import RawDataRecord
from uds.database.data_record.abstract_data_record import  DataRecordType


def test_raw_data_record_initialization():
    record = RawDataRecord(name="TestRawDataRecord", length=16)
    assert record.name == "TestRawDataRecord"
    assert record.length == 16
    assert record.data_record_type == DataRecordType.RAW
    assert record.is_reoccurring is False
    assert record.min_occurrences == 1
    assert record.max_occurrences == 1
    assert record.contains == ()
    assert record.decode(1234) == 1234
    assert record.encode(1234) == 1234


def test_raw_data_record_invalid_name():
    with pytest.raises(TypeError):
        RawDataRecord(name=123, length=16)

def test_raw_data_record_invalid_length():
    with pytest.raises(ValueError):
        RawDataRecord(name="TestRecord", length=-1)
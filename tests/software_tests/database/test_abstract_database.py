import pytest
from mock import Mock, patch

from uds.addressing import AddressingType
from uds.database.abstract_database import AbstractDatabase, RequestSID, ResponseSID, UdsMessage, UdsMessageRecord

SCRIPT_LOCATION = "uds.database.abstract_database"


class TestAbstractDatabase:

    def setup_method(self):
        self.mock_database = Mock(spec=AbstractDatabase)

    # encode

    @pytest.mark.parametrize("sid", [Mock(), 1])
    @pytest.mark.parametrize("data_records_values", [
        {"data_record_1": 1, "data_record_2": "Some Value", "data_record_3": 543.234},
        {"a": 2.3, "b": 543, "c": "xyz"},
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_encode__type_error(self, mock_isinstance, sid, data_records_values):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractDatabase.encode(self.mock_database, sid=sid, **data_records_values)
        mock_isinstance.assert_called_once_with(sid, int)

    @pytest.mark.parametrize("sid", [Mock(), 1, RequestSID.RequestDownload, ResponseSID.WriteDataByIdentifier])
    @pytest.mark.parametrize("data_records_values", [
        {"data_record_1": 1, "data_record_2": "Some Value", "data_record_3": 543.234},
        {"a": 2.3, "b": 543, "c": "xyz"},
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_encode__value_error(self, mock_isinstance, sid, data_records_values):
        self.mock_database.services = {}
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            AbstractDatabase.encode(self.mock_database, sid=sid, **data_records_values)
        mock_isinstance.assert_called_once_with(sid, int)

    @pytest.mark.parametrize("sid", [1, RequestSID.RequestDownload, ResponseSID.WriteDataByIdentifier])
    @pytest.mark.parametrize("data_records_values", [
        {"data_record_1": 1, "data_record_2": "Some Value", "data_record_3": 543.234},
        {"a": 2.3, "b": 543, "c": "xyz"},
    ])
    def test_encode(self, sid, data_records_values):
        mock_service = Mock()
        self.mock_database.services = {sid: mock_service}
        assert (AbstractDatabase.encode(self.mock_database, sid=sid, **data_records_values)
                == mock_service.encode.return_value)
        mock_service.encode.assert_called_once_with(sid=sid, **data_records_values)

    # decode

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x10, 0x03], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessageRecord, payload=[0x62, *range(255)])
    ])
    def test_decode__value_error(self, message):
        self.mock_database.services = {}
        with pytest.raises(ValueError):
            AbstractDatabase.decode(self.mock_database, message)

    @pytest.mark.parametrize("message", [
        UdsMessage(payload=[0x10, 0x03], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessageRecord, payload=[0x62, *range(255)])
    ])
    def test_decode(self, message):
        mock_service = Mock()
        self.mock_database.services = {message.payload[0]: mock_service}
        assert AbstractDatabase.decode(self.mock_database, message) == mock_service.decode.return_value

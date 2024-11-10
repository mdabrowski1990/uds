import pytest
from mock import Mock, patch

from uds.database.data_record import AbstractDataRecord

SCRIPT_LOCATION = "uds.database.data_record"


class TestAbstractDataRecord:

    def setup_method(self):
        self.mock_data_record = Mock(spec=AbstractDataRecord)

    # __init__

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_name = Mock()
        with pytest.raises(TypeError):
            AbstractDataRecord.__init__(self.mock_data_record, mock_name)
        mock_isinstance.assert_called_once_with(mock_name, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__valid(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_name = Mock()
        assert AbstractDataRecord.__init__(self.mock_data_record, mock_name) is None
        assert self.mock_data_record._AbstractDataRecord__name == mock_name.strip.return_value
        mock_isinstance.assert_called_once_with(mock_name, str)
        mock_name.strip.assert_called_once_with()

    # name

    def test_name(self):
        self.mock_data_record._AbstractDataRecord__name = Mock()
        assert AbstractDataRecord.name.fget(self.mock_data_record) == self.mock_data_record._AbstractDataRecord__name

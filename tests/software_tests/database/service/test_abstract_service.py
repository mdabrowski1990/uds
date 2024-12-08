import pytest
from mock import Mock


from uds.database.service.abstract_service import AbstractService


class TestAbstractService:
    """Unit tests for Abstract Service."""

    def setup_method(self):
        self.mock_abstract_service = Mock(spec=AbstractService)

    # encode

    @pytest.mark.parametrize("sid, request_sid, response_sid", [
        (1, 1, 2),
        (0x11, 0x11, 0x51),
    ])
    @pytest.mark.parametrize("data_records_values", [
        {},
        {"a": 1, "b": 2, "c": 3, "xyz": None}
    ])
    def test_encode__request(self, sid, request_sid, response_sid, data_records_values):
        self.mock_abstract_service.request_sid = request_sid
        self.mock_abstract_service.response_sid = response_sid
        assert (AbstractService.encode(self=self.mock_abstract_service, sid=sid, **data_records_values)
                == self.mock_abstract_service.encode_request.return_value)
        self.mock_abstract_service.encode_request.assert_called_once_with(**data_records_values)

    @pytest.mark.parametrize("sid, request_sid, response_sid", [
        (2, 1, 2),
        (0x51, 0x11, 0x51),
    ])
    @pytest.mark.parametrize("data_records_values", [
        {},
        {"a": 1, "b": 2, "c": 3, "xyz": None}
    ])
    def test_encode__response(self, sid, request_sid, response_sid, data_records_values):
        self.mock_abstract_service.request_sid = request_sid
        self.mock_abstract_service.response_sid = response_sid
        assert (AbstractService.encode(self=self.mock_abstract_service, sid=sid, **data_records_values)
                == self.mock_abstract_service.encode_response.return_value)
        self.mock_abstract_service.encode_response.assert_called_once_with(**data_records_values)

    @pytest.mark.parametrize("sid, request_sid, response_sid", [
        (0, 1, 2),
        (0x11, 0x10, 0x50),
    ])
    @pytest.mark.parametrize("data_records_values", [
        {},
        {"a": 1, "b": 2, "c": 3, "xyz": None}
    ])
    def test_encode__value_error(self, sid, request_sid, response_sid, data_records_values):
        self.mock_abstract_service.request_sid = request_sid
        self.mock_abstract_service.response_sid = response_sid
        with pytest.raises(ValueError):
            AbstractService.encode(self=self.mock_abstract_service, sid=sid, **data_records_values)
        self.mock_abstract_service.encode_request.asseert_not_called()
        self.mock_abstract_service.encode_response.asseert_not_called()

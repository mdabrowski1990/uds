import pytest
from mock import MagicMock, Mock, call, patch

from uds.database.service.service import (
    NRC,
    RESPONSE_REQUEST_SID_DIFF,
    RequestSID,
    ResponseSID,
    Service,
    SingleOccurrenceInfo,
)

SCRIPT_LOCATION = "uds.database.service.service"

class TestService:
    """Unit tests for `Service` class."""

    def setup_method(self):
        self.mock_service = Mock(spec=Service,
                                 NEGATIVE_RESPONSE_LENGTH=3)
        # patching
        self._patcher_conditional_data_record = patch(f"{SCRIPT_LOCATION}.AbstractConditionalDataRecord")
        self.mock_conditional_data_record = self._patcher_conditional_data_record.start()
        self._patcher_request_sid_validate_member = patch(f"{SCRIPT_LOCATION}.RequestSID.validate_member")
        self.mock_request_sid_validate_member = self._patcher_request_sid_validate_member.start()
        self._patcher_response_sid_validate_member = patch(f"{SCRIPT_LOCATION}.ResponseSID.validate_member")
        self.mock_response_sid_validate_member = self._patcher_response_sid_validate_member.start()
        self._patcher_nrc_validate_member = patch(f"{SCRIPT_LOCATION}.NRC.validate_member")
        self.mock_nrc_validate_member = self._patcher_nrc_validate_member.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_conditional_data_record.stop()
        self._patcher_request_sid_validate_member.stop()
        self._patcher_response_sid_validate_member.stop()
        self._patcher_nrc_validate_member.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("request_sid, request_structure, response_structure", [
        (Mock(), Mock(), Mock()),
        (RequestSID.RequestUpload, [], [Mock()]),
    ])
    def test_init__mandatory_args(self, request_sid, request_structure, response_structure):
        assert Service.__init__(self.mock_service,
                                request_sid=request_sid,
                                request_structure=request_structure,
                                response_structure=response_structure) is None
        assert self.mock_service.request_sid == request_sid
        assert self.mock_service.request_structure == request_structure
        assert self.mock_service.response_structure == response_structure
        assert self.mock_service.supported_nrc == tuple(NRC)

    @pytest.mark.parametrize("request_sid, request_structure, response_structure, supported_nrc", [
        (Mock(), Mock(), Mock(), Mock()),
        (RequestSID.RequestUpload, [], [Mock()], [Mock()]),
    ])
    def test_init__all_args(self, request_sid, request_structure, response_structure, supported_nrc):
        assert Service.__init__(self.mock_service,
                                request_sid=request_sid,
                                request_structure=request_structure,
                                response_structure=response_structure,
                                supported_nrc=supported_nrc) is None
        assert self.mock_service.request_sid == request_sid
        assert self.mock_service.request_structure == request_structure
        assert self.mock_service.response_structure == response_structure
        assert self.mock_service.supported_nrc == supported_nrc

    # request_sid

    def test_request_sid__get(self):
        self.mock_service._Service__request_sid = Mock()
        assert Service.request_sid.fget(self.mock_service) == self.mock_service._Service__request_sid

    @pytest.mark.parametrize("value", [0, RequestSID.Authentication])
    def test_request_sid__set__valid(self, value):
        mock_name = Mock()
        mock_request_sid = MagicMock()
        mock_request_sid.name = mock_name
        mock_response_sid = MagicMock()
        mock_response_sid.name = mock_name
        self.mock_request_sid_validate_member.return_value = mock_request_sid
        self.mock_response_sid_validate_member.return_value = mock_response_sid
        assert Service.request_sid.fset(self.mock_service, value) is None
        assert self.mock_service._Service__request_sid == mock_request_sid
        assert self.mock_service._Service__response_sid == mock_response_sid
        self.mock_request_sid_validate_member.assert_called_once_with(value)
        self.mock_response_sid_validate_member.assert_called_once_with(value + RESPONSE_REQUEST_SID_DIFF)

    @pytest.mark.parametrize("value", [MagicMock(), RequestSID.Authentication])
    def test_request_sid__set__value_error(self, value):
        with pytest.raises(ValueError):
            Service.request_sid.fset(self.mock_service, value)
            
    # response_sid
    
    def test_response_sid__get(self):
        self.mock_service._Service__response_sid = Mock()
        assert Service.response_sid.fget(self.mock_service) == self.mock_service._Service__response_sid

    # request_structure

    def test_request_structure__get(self):
        self.mock_service._Service__request_structure = Mock()
        assert Service.request_structure.fget(self.mock_service) == self.mock_service._Service__request_structure

    @pytest.mark.parametrize("value", [(Mock(), Mock()), []])
    def test_request_sid__set(self, value):
        assert Service.request_structure.fset(self.mock_service, value) is None
        assert self.mock_service._Service__request_structure == tuple(value)
        self.mock_service.validate_message_structure.assert_called_once_with(value)
        
    # response_structure
    
    def test_response_structure__get(self):
        self.mock_service._Service__response_structure = Mock()
        assert Service.response_structure.fget(self.mock_service) == self.mock_service._Service__response_structure

    @pytest.mark.parametrize("value", [(Mock(), Mock()), []])
    def test_request_sid__set(self, value):
        assert Service.response_structure.fset(self.mock_service, value) is None
        assert self.mock_service._Service__response_structure == tuple(value)
        self.mock_service.validate_message_structure.assert_called_once_with(value)
        
    # supported_nrc
    
    def test_supported_nrc__get(self):
        self.mock_service._Service__supported_nrc = Mock()
        assert Service.supported_nrc.fget(self.mock_service) == self.mock_service._Service__supported_nrc

    @pytest.mark.parametrize("value", [(Mock(), Mock()), tuple(NRC)])
    def test_request_sid__set(self, value):
        assert Service.supported_nrc.fset(self.mock_service, value) is None
        assert self.mock_service._Service__supported_nrc == set(value)
        self.mock_nrc_validate_member.assert_has_calls([call(nrc) for nrc in value], any_order=True)

    # name

    def test_name__get(self):
        assert Service.name.fget(self.mock_service) == self.mock_service.request_sid.name

    # _get_rsid_info

    def test_get_rsid_info(self):
        assert (Service._get_rsid_info(self.mock_service)
                == SingleOccurrenceInfo(name="RSID",
                                        length=8,
                                        raw_value=self.mock_service.response_sid.value,
                                        physical_value=self.mock_service.response_sid.name,
                                        children=tuple()))

    # _get_sid_info

    def test_get_sid_info(self):
        assert (Service._get_sid_info(self.mock_service)
                == SingleOccurrenceInfo(name="SID",
                                        length=8,
                                        raw_value=self.mock_service.request_sid.value,
                                        physical_value=self.mock_service.request_sid.name,
                                        children=tuple()))

    # _get_nrc_info

    @pytest.mark.parametrize("nrc", [Mock(), NRC.AuthenticationRequired])
    def test_get_nrc_info(self, nrc):
        assert (Service._get_nrc_info(nrc)
                == SingleOccurrenceInfo(name="NRC",
                                        length=8,
                                        raw_value=self.mock_nrc_validate_member.return_value.value,
                                        physical_value=self.mock_nrc_validate_member.return_value.name,
                                        children=tuple()))
        self.mock_nrc_validate_member.assert_called_once_with(nrc)

    # validate_message_structure

    @pytest.mark.parametrize("value", [Mock(), []])
    def test_validate_message_structure(self, value):
        assert Service.validate_message_structure(value) is None
        self.mock_conditional_data_record.validate_message_continuation.assert_called_once_with(value)

    # decode_request

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode_request__value_error(self, payload):
        with pytest.raises(ValueError):
            Service.decode_request(self.mock_service, payload)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode_request__valid(self, payload):
        self.mock_service.request_sid = payload[0]
        self.mock_service._decode_payload.return_value = [MagicMock(), MagicMock(), MagicMock()]
        assert (Service.decode_request(self.mock_service, payload)
                == self.mock_service._get_sid_info.return_value, *self.mock_service._decode_payload.return_value)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_service._decode_payload.assert_called_once_with(
            payload=payload[1:],
            message_continuation=self.mock_service.request_structure)

    # decode_positive_response

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode_positive_response__value_error(self, payload):
        with pytest.raises(ValueError):
            Service.decode_positive_response(self.mock_service, payload)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode_positive_response__valid(self, payload):
        self.mock_service.response_sid = payload[0]
        self.mock_service._decode_payload.return_value = [MagicMock(), MagicMock(), MagicMock()]
        assert (Service.decode_positive_response(self.mock_service, payload)
                == self.mock_service._get_rsid_info.return_value, *self.mock_service._decode_payload.return_value)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_service._decode_payload.assert_called_once_with(
            payload=payload[1:],
            message_continuation=self.mock_service.request_structure)

    # decode_negative_response

    @pytest.mark.parametrize("payload", [b"\x7F\x12", [0x7F, 0x65, 0x8A, 0xB1]])
    def test_decode_negative_response__value_error__length(self, payload):
        with pytest.raises(ValueError):
            Service.decode_negative_response(self.mock_service, payload)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("payload", [b"\x7E\x12\x34", [0x00, 0x65, 0x8A]])
    def test_decode_negative_response__value_error__rsid(self, payload):
        with pytest.raises(ValueError):
            Service.decode_negative_response(self.mock_service, payload)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("payload", [b"\x7F\x12\x34", [0x7F, 0x65, 0x8A]])
    def test_decode_negative_response__value_error__sid(self, payload):
        with pytest.raises(ValueError):
            Service.decode_negative_response(self.mock_service, payload)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)

    @pytest.mark.parametrize("payload", [b"\x7F\x12\x34", [0x7F, 0x65, 0x8A]])
    def test_decode_negative_response__valid(self, payload):
        self.mock_service.request_sid = payload[1]
        self.mock_service.supported_nrc = {payload[2]}
        assert (Service.decode_negative_response(self.mock_service, payload)
                == (self.mock_service._get_rsid_info.return_value,
                    self.mock_service._get_sid_info.return_value,
                    self.mock_service._get_nrc_info.return_value))
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("payload", [b"\x7F\x12\x34", [0x7F, 0x65, 0x8A]])
    def test_decode_negative_response__valid__warning(self, payload):
        self.mock_service.request_sid = payload[1]
        self.mock_service.supported_nrc = set()
        assert (Service.decode_negative_response(self.mock_service, payload)
                == (self.mock_service._get_rsid_info.return_value,
                    self.mock_service._get_sid_info.return_value,
                    self.mock_service._get_nrc_info.return_value))
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_warn.assert_called_once()

    # decode

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode__request(self, payload):
        self.mock_service.request_sid = payload[0]
        assert Service.decode(self.mock_service,
                              payload=payload) == self.mock_service.decode_request.return_value

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode__positive_response(self, payload):
        self.mock_service.response_sid = payload[0]
        assert Service.decode(self.mock_service,
                              payload=payload) == self.mock_service.decode_positive_response.return_value

    @pytest.mark.parametrize("payload", [[ResponseSID.NegativeResponse, *range(100, 232)],
                                         bytes([ResponseSID.NegativeResponse]) + b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode__negative_response(self, payload):
        assert Service.decode(self.mock_service,
                              payload=payload) == self.mock_service.decode_negative_response.return_value

    @pytest.mark.parametrize("payload", [[*range(100, 232)], b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87"])
    def test_decode__value_error(self, payload):
        with pytest.raises(ValueError):
            Service.decode(self.mock_service, payload=payload)

    # encode_request

    @pytest.mark.parametrize("data_records_values, request_sid, payload_continuation", [
        (MagicMock(), 0xA5, bytearray(b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87")),
        ({"a": 1, "b": [{"zyx a": 94}, 0xFF]}, RequestSID.ControlDTCSetting, bytearray([0xBE, 0xEF])),
    ])
    def test_encode_request(self, data_records_values,
                            request_sid, payload_continuation):
        self.mock_service.request_sid = request_sid
        self.mock_service._encode_message_continuation.return_value = payload_continuation
        assert (Service.encode_request(self.mock_service, data_records_values=data_records_values)
                == bytearray([request_sid]) + payload_continuation)
        self.mock_service._encode_message_continuation.assert_called_once_with(
            structure=self.mock_service.response_structure,
            data_records_values=data_records_values)

    # encode_positive_response

    @pytest.mark.parametrize("data_records_values, response_sid, payload_continuation", [
        (MagicMock(), 0xA5, bytearray(b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87")),
        ({"a": 1, "b": [{"zyx a": 94}, 0xFF]}, ResponseSID.ControlDTCSetting, bytearray([0xBE, 0xEF])),
    ])
    def test_encode_positive_response(self, data_records_values,
                                      response_sid, payload_continuation):
        self.mock_service.response_sid = response_sid
        self.mock_service._encode_message_continuation.return_value = payload_continuation
        assert (Service.encode_positive_response(self.mock_service, data_records_values=data_records_values)
                == bytearray([response_sid]) + payload_continuation)
        self.mock_service._encode_message_continuation.assert_called_once_with(
            structure=self.mock_service.response_structure,
            data_records_values=data_records_values)

    # encode_negative_response

    @pytest.mark.parametrize("nrc, sid", [
        (0x00, 0x5A),
        (NRC.NoResponseFromSubnetComponent, 0xB2),
    ])
    def test_encode_negative_response__warning(self, nrc, sid):
        self.mock_service.request_sid = sid
        self.mock_service.supported_nrc = set()
        assert (Service.encode_negative_response(self.mock_service, nrc)
                == bytearray((ResponseSID.NegativeResponse, sid, nrc)))
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("nrc, sid", [
        (0x00, 0x5A),
        (NRC.NoResponseFromSubnetComponent, 0xB2),
    ])
    def test_encode_negative_response__no_warning(self, nrc, sid):
        self.mock_service.request_sid = sid
        self.mock_service.supported_nrc = {nrc}
        assert (Service.encode_negative_response(self.mock_service, nrc)
                == bytearray((ResponseSID.NegativeResponse, sid, nrc)))
        self.mock_warn.assert_not_called()

    # encode

    @pytest.mark.parametrize("data_records_values", [MagicMock(), {"a": 1, "b": [{"zyx a": 94}, 0xFF]}])
    def test_encode__request(self, data_records_values):
        assert Service.encode(self.mock_service,
                              sid=self.mock_service.request_sid,
                              data_records_values=data_records_values) == self.mock_service.encode_request.return_value
        self.mock_service.encode_request.assert_called_once_with(data_records_values=data_records_values)

    @pytest.mark.parametrize("data_records_values", [MagicMock(), {"a": 1, "b": [{"zyx a": 94}, 0xFF]}])
    def test_encode__positive_response(self, data_records_values):
        assert (Service.encode(self.mock_service,
                              sid=self.mock_service.response_sid,
                              data_records_values=data_records_values)
                == self.mock_service.encode_positive_response.return_value)
        self.mock_service.encode_positive_response.assert_called_once_with(data_records_values=data_records_values)

    @pytest.mark.parametrize("data_records_values", [MagicMock(), {"a": 1, "b": [{"zyx a": 94}, 0xFF]}])
    def test_encode__negative_response(self, data_records_values):
        assert (Service.encode(self.mock_service,
                              sid=ResponseSID.NegativeResponse,
                              data_records_values=data_records_values)
                == self.mock_service.encode_negative_response.return_value)
        self.mock_service.encode_negative_response.assert_called_once_with(**data_records_values)

    @pytest.mark.parametrize("sid, data_records_values", [
        (Mock(), MagicMock()),
        (RequestSID.RequestDownload, {"a": 1, "b": [{"zyx a": 94}, 0xFF]}),
    ])
    def test_encode__value_error(self, sid, data_records_values):
        with pytest.raises(ValueError):
            Service.encode(self.mock_service,
                           sid=sid,
                           data_records_values=data_records_values)

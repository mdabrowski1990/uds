import pytest
from mock import MagicMock, Mock, call, patch

from uds.database.data_record import (
    ConditionalFormulaDataRecord,
    LinearFormulaDataRecord,
    MappingDataRecord,
    MultipleOccurrencesInfo,
    RawDataRecord,
)
from uds.database.service.service import (
    NRC,
    RESPONSE_REQUEST_SID_DIFF,
    AbstractConditionalDataRecord,
    AbstractDataRecord,
    RequestSID,
    ResponseSID,
    Sequence,
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
        self._patcher_validate_message_continuation \
            = patch(f"{SCRIPT_LOCATION}.AbstractConditionalDataRecord.validate_message_continuation")
        self.mock_validate_message_continuation = self._patcher_validate_message_continuation.start()
        self._patcher_request_sid_validate_member = patch(f"{SCRIPT_LOCATION}.RequestSID.validate_member")
        self.mock_request_sid_validate_member = self._patcher_request_sid_validate_member.start()
        self._patcher_response_sid_validate_member = patch(f"{SCRIPT_LOCATION}.ResponseSID.validate_member")
        self.mock_response_sid_validate_member = self._patcher_response_sid_validate_member.start()
        self._patcher_nrc_validate_member = patch(f"{SCRIPT_LOCATION}.NRC.validate_member")
        self.mock_nrc_validate_member = self._patcher_nrc_validate_member.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_int_to_bytes = patch(f"{SCRIPT_LOCATION}.int_to_bytes")
        self.mock_int_to_bytes = self._patcher_int_to_bytes.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_validate_message_continuation.stop()
        self._patcher_request_sid_validate_member.stop()
        self._patcher_response_sid_validate_member.stop()
        self._patcher_nrc_validate_member.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_int_to_bytes.stop()
        self._patcher_warn.stop()

    @staticmethod
    def get_data_record_occurrences(**kwargs):
        if kwargs["value"] is None:
            return []
        if isinstance(kwargs["value"], Sequence):
            return [MagicMock() for _ in kwargs["value"]]
        return [MagicMock()]

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

    def test_get_rsid_info__positive(self):
        assert (Service._get_rsid_info(self.mock_service)
                == SingleOccurrenceInfo(name="RSID",
                                        length=8,
                                        raw_value=self.mock_service.response_sid.value,
                                        physical_value=self.mock_service.response_sid.name,
                                        children=tuple(),
                                        unit=None))

    def test_get_rsid_info__negative(self):
        assert (Service._get_rsid_info(self.mock_service, positive=False)
                == SingleOccurrenceInfo(name="RSID",
                                        length=8,
                                        raw_value=ResponseSID.NegativeResponse.value,
                                        physical_value=ResponseSID.NegativeResponse.name,
                                        children=tuple(),
                                        unit=None))

    # _get_sid_info

    def test_get_sid_info(self):
        assert (Service._get_sid_info(self.mock_service)
                == SingleOccurrenceInfo(name="SID",
                                        length=8,
                                        raw_value=self.mock_service.request_sid.value,
                                        physical_value=self.mock_service.request_sid.name,
                                        children=tuple(),
                                        unit=None))

    # _get_nrc_info

    @pytest.mark.parametrize("nrc", [Mock(), NRC.AuthenticationRequired])
    def test_get_nrc_info(self, nrc):
        assert (Service._get_nrc_info(nrc)
                == SingleOccurrenceInfo(name="NRC",
                                        length=8,
                                        raw_value=self.mock_nrc_validate_member.return_value.value,
                                        physical_value=self.mock_nrc_validate_member.return_value.name,
                                        children=tuple(),
                                        unit=None))
        self.mock_nrc_validate_member.assert_called_once_with(nrc)

    # _get_data_record_occurrences

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=0, max_occurrences=1,
              min_raw_value=0, max_raw_value=0xFF),
         [0x10]),
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=1, max_occurrences=1,
              min_raw_value=0, max_raw_value=0x7),
         None),
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=0, max_occurrences=8,
              min_raw_value=0, max_raw_value=0xFF),
         0x0),
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=0, max_occurrences=8,
              min_raw_value=0, max_raw_value=0xFF),
         None),
    ])
    def test_get_data_record_occurrences__type_error(self, data_record, value):
        with pytest.raises(TypeError):
            Service._get_data_record_occurrences(data_record=data_record, value=value)

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=0, max_occurrences=1,
              min_raw_value=0, max_raw_value=0xFF),
         0x100),
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=1, max_occurrences=1,
              min_raw_value=0, max_raw_value=0x7),
         0x8),
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=0, max_occurrences=8,
              min_raw_value=0, max_raw_value=0xFF),
         [-1, 0]),
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=0, max_occurrences=8,
              min_raw_value=0, max_raw_value=0xF),
         [0x10, 0, 2]),
    ])
    def test_get_data_record_occurrences__value_error(self, data_record, value):
        with pytest.raises(ValueError):
            Service._get_data_record_occurrences(data_record=data_record, value=value)

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=0, max_occurrences=8,
              min_raw_value=0, max_raw_value=0xFF),
         []),
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=0, max_occurrences=1,
              min_raw_value=0, max_raw_value=0x7),
         None),
    ])
    def test_get_data_record_occurrences__valid__no_occurrences(self, data_record, value):
        assert Service._get_data_record_occurrences(data_record=data_record, value=value) == []

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=1, max_occurrences=1,
              min_raw_value=0, max_raw_value=0xFF),
         0x0),
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=0, max_occurrences=1,
              min_raw_value=0, max_raw_value=0x7),
         0x7),
    ])
    def test_get_data_record_occurrences__valid__single_raw_value(self, data_record, value):
        assert Service._get_data_record_occurrences(data_record=data_record, value=value) == [value]

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=1, max_occurrences=1,
              min_raw_value=0, max_raw_value=0xFF),
         {"a": 1, "b": 2}),
        (Mock(spec=AbstractDataRecord, is_reoccurring=False, min_occurrences=0, max_occurrences=1,
              min_raw_value=0, max_raw_value=0x7),
         {"param X": 0x00, "param Y": 0xFF, "123": 654}),
    ])
    def test_get_data_record_occurrences__valid__single_mapping(self, data_record, value):
        assert (Service._get_data_record_occurrences(data_record=data_record, value=value)
                == [data_record.get_raw_value_from_children.return_value])
        data_record.get_raw_value_from_children.assert_called_once_with(value)

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=4, max_occurrences=4,
              min_raw_value=0, max_raw_value=0xFF),
         [0xFF, {"param X": 0x00, "param Y": 0xFF, "123": 654}, 0x00, {"param X": 0x1, "param Y": 0x2, "123": 4}]),
        (Mock(spec=AbstractDataRecord, is_reoccurring=True, min_occurrences=0, max_occurrences=None,
              min_raw_value=0, max_raw_value=0x7),
         [0x0, 0x1, 0x7, {"a": 1, "b": 2}, {"a": 1, "b": 2}, {"a": 0, "b": 0}]),
    ])
    def test_get_data_record_occurrences__valid__multiple_occurrences(self, data_record, value):
        expected_value = []
        expected_calls = []
        for _value in value:
            if isinstance(_value, int):
                expected_value.append(_value)
            else:
                expected_value.append(data_record.get_raw_value_from_children.return_value)
                expected_calls.append(call(_value))
        assert Service._get_data_record_occurrences(data_record=data_record, value=value) == expected_value
        data_record.get_raw_value_from_children.assert_has_calls(expected_calls, any_order=False)

    # _decode_payload

    # TODO

    # _encode_message

    @pytest.mark.parametrize("message_structure, data_records_values", [
        ([Mock(name="xyz", length=8)], {"xyz": 1}),
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=8),
          Mock(name="Param 2", length=1)], {"Param 1": 0, "Param 2": 0}),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__not_implemented(self, mock_get_data_record_occurrences,
                                             message_structure, data_records_values):
        mock_get_data_record_occurrences.return_value = [0]
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        with pytest.raises(NotImplementedError):
            Service._encode_message(data_records_values=data_records_values,
                                    message_structure=message_structure)

    @pytest.mark.parametrize("message_structure, data_records_values", [
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=7)],
         {"Param 1": 0}),
        ([Mock(spec=AbstractDataRecord, name="Data Record - 1", length=7),
          Mock(spec=AbstractDataRecord, name="Data Record - 2", length=3)],
         {"Data Record - 1": [{"Data Record - 1.1": 0, "Data Record - 1.2": 2},
                              0,
                              {"Data Record - 1.1": 9, "Data Record - 1.2": {"A": 1, "B": 2}}],
          "Data Record - 2": [{"Data Record - 2.1": 0, "Data Record - 2.2": 2}, 0]}),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__runtime_error(self, mock_get_data_record_occurrences,
                                                 message_structure, data_records_values):
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        with pytest.raises(RuntimeError):
            Service._encode_message(data_records_values=data_records_values,
                                    message_structure=message_structure)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=data_records_values[dr.name])
                                                           for dr in message_structure], any_order=False)
        self.mock_int_to_bytes.assert_not_called()

    @pytest.mark.parametrize("message_structure, data_records_values, payload", [
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=8)],
         {"Param 1": 0},
         b"\x92\x8B\x7A\xDC"),
        ([Mock(spec=AbstractDataRecord, name="XYZ", length=24)],
         {"XYZ": {"Child 1": 1, "Child 2": 2, "Child 3": 0}},
         b"\xCA\xFE"),
        ([Mock(spec=AbstractDataRecord, name="A #1", length=1),
          Mock(spec=AbstractDataRecord, name="A #2", length=2)],
         {"A #1": [0, 1, 0, 1], "A #2": [0x3, 0x0]},
         b"\xBE\xEF"),
        ([Mock(spec=AbstractDataRecord, name="Data Record - 1", length=7),
          Mock(spec=AbstractDataRecord, name="Data Record - 2", length=3)],
         {"Data Record - 1": [{"Data Record - 1.1": 0, "Data Record - 1.2": 2},
                              0,
                              {"Data Record - 1.1": 9, "Data Record - 1.2": {"A": 1, "B": 2}}],
          "Data Record - 2": [{"Data Record - 2.1": 0, "Data Record - 2.2": 2}]},
         [0xCa, 0xFF, 0xE, 0x56]),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__valid__no_condition(self, mock_get_data_record_occurrences,
                                                 message_structure, data_records_values,
                                                 payload):
        self.mock_int_to_bytes.return_value = payload
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        assert Service._encode_message(data_records_values=data_records_values,
                                       message_structure=message_structure) == bytearray(payload)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=data_records_values[dr.name])
                                                           for dr in message_structure], any_order=False)
        self.mock_int_to_bytes.assert_called_once()

    @pytest.mark.parametrize("message_structure, data_records_values, message_continuation, payload", [
        ([Mock(spec=AbstractDataRecord, name="A #1", length=2),
          Mock(spec=AbstractConditionalDataRecord)],
         {"A #1": [0, 1, 0, 1], "A #2": [0x3, 0x0]},
         [Mock(spec=AbstractDataRecord, name="A #2", length=4)],
         b"\xBE\xEF"),
        ([Mock(spec=AbstractDataRecord, name="Data Record - 1", length=8),
          Mock(spec=AbstractConditionalDataRecord)],
         {"Data Record - 1": [{"Data Record - 1.1": 0, "Data Record - 1.2": 2},
                              0,
                              {"Data Record - 1.1": 9, "Data Record - 1.2": {"A": 1, "B": 2}}],
          "Data Record - 2": [{"Data Record - 2.1": 0, "Data Record - 2.2": 2}]},
         [Mock(spec=AbstractDataRecord, name="Data Record - 2", length=24)],
         [0xCa, 0xFF, 0xE, 0x56]),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__valid__with_condition(self, mock_get_data_record_occurrences,
                                                   message_structure, data_records_values,
                                                   message_continuation, payload):
        self.mock_int_to_bytes.return_value = payload
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure + message_continuation:
            data_record.name = data_record._extract_mock_name()
        mock_get_message_continuation = Mock(return_value=message_continuation)
        message_structure[-1].get_message_continuation = mock_get_message_continuation
        assert Service._encode_message(data_records_values=data_records_values,
                                       message_structure=message_structure) == bytearray(payload + payload)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=data_records_values[dr.name])
                                                           for dr in message_structure + message_continuation
                                                           if isinstance(dr, AbstractDataRecord)],
                                                          any_order=False)
        self.mock_int_to_bytes.assert_called()
        mock_get_message_continuation.assert_called_once()

    # validate_message_structure

    @pytest.mark.parametrize("value", [Mock(), []])
    def test_validate_message_structure(self, value):
        assert Service.validate_message_structure(value) is None
        self.mock_validate_message_continuation.assert_called_once_with(value)

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
        self.mock_service._get_rsid_info.assert_called_once_with(positive=False)

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
        self.mock_service._get_rsid_info.assert_called_once_with(positive=False)

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
        self.mock_service._encode_message.return_value = payload_continuation
        assert (Service.encode_request(self.mock_service, data_records_values=data_records_values)
                == bytearray([request_sid]) + payload_continuation)
        self.mock_service._encode_message.assert_called_once_with(
            message_structure=self.mock_service.request_structure,
            data_records_values=data_records_values)

    # encode_positive_response

    @pytest.mark.parametrize("data_records_values, response_sid, payload_continuation", [
        (MagicMock(), 0xA5, bytearray(b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87")),
        ({"a": 1, "b": [{"zyx a": 94}, 0xFF]}, ResponseSID.ControlDTCSetting, bytearray([0xBE, 0xEF])),
    ])
    def test_encode_positive_response(self, data_records_values,
                                      response_sid, payload_continuation):
        self.mock_service.response_sid = response_sid
        self.mock_service._encode_message.return_value = payload_continuation
        assert (Service.encode_positive_response(self.mock_service, data_records_values=data_records_values)
                == bytearray([response_sid]) + payload_continuation)
        self.mock_service._encode_message.assert_called_once_with(
            message_structure=self.mock_service.response_structure,
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


@pytest.mark.integration
class TestServiceIntegration:
    """Integration tests for `Service` class."""

    def setup_class(self):
        self.diagnostic_session_control = Service(
            request_sid=RequestSID.DiagnosticSessionControl,
            request_structure=[
                RawDataRecord(name="subFunction",
                              length=8,
                              children=[
                                  MappingDataRecord(name="SPRMIB",
                                                    length=1,
                                                    values_mapping={0: "no", 1: "yes"}),
                                  MappingDataRecord(name="diagnosticSessionType",
                                                    length=7,
                                                    values_mapping={1: "Default",
                                                                    2: "Programming",
                                                                    3: "Extended"})
                              ])
            ],
            response_structure=[
                RawDataRecord(name="subFunction",
                              length=8,
                              children=[
                                  MappingDataRecord(name="SPRMIB",
                                                    length=1,
                                                    values_mapping={0: "no", 1: "yes"}),
                                  MappingDataRecord(name="diagnosticSessionType",
                                                    length=7,
                                                    values_mapping={1: "Default",
                                                                    2: "Programming",
                                                                    3: "Extended"})
                              ]),
                RawDataRecord(name="sessionParameterRecord",
                              length=32,
                              children=[
                                  LinearFormulaDataRecord(name="P2Server_max",
                                                          length=16,
                                                          factor=1,
                                                          offset=0,
                                                          unit="ms"),
                                  LinearFormulaDataRecord(name="P2*Server_max",
                                                          length=16,
                                                          factor=10,
                                                          offset=0,
                                                          unit="ms")
                              ])
            ]
        )
        self.read_memory_by_address = Service(
            request_sid=RequestSID.ReadMemoryByAddress,
            request_structure=[
                RawDataRecord(name="addressAndLengthFormatIdentifier",
                              length=8,
                              children=[
                                  RawDataRecord(name="memorySizeLength",
                                                length=4),
                                  RawDataRecord(name="memoryAddressLength",
                                                length=4)
                              ]),
                ConditionalFormulaDataRecord(
                    formula=lambda addressAndLengthFormatIdentifier: [
                        RawDataRecord(name="memoryAddress", length=8*(addressAndLengthFormatIdentifier & 0xF)),
                        RawDataRecord(name="memorySize", length=8*(addressAndLengthFormatIdentifier >> 4))
                    ]
                )
            ],
            response_structure=[
                RawDataRecord(name="data",
                              length=8,
                              min_occurrences=1,
                              max_occurrences=None)
            ]
        )

    # encode

    @pytest.mark.parametrize("sid, data_records_values, payload", [
        (
            0x10,
            {"subFunction": 0x40},
            bytearray([0x10, 0x40])
        ),
        (
            0x50,
            {
                "subFunction": {"SPRMIB": 1, "diagnosticSessionType": 3},
                "sessionParameterRecord": {"P2Server_max": 0x1234, "P2*Server_max": 0x5678}
            },
            bytearray([0x50, 0x83, 0x12, 0x34, 0x56, 0x78])
        ),
        (
            0x7F,
            {"nrc": 0x84},
            bytearray([0x7F, 0x10, 0x84])
        ),
    ])
    def test_encode_1(self, sid, data_records_values, payload):
        assert self.diagnostic_session_control.encode(sid=sid, data_records_values=data_records_values) == payload

    @pytest.mark.parametrize("sid, data_records_values, payload", [
        (
            RequestSID.ReadMemoryByAddress,
            {
                "addressAndLengthFormatIdentifier": 0x24,
                "memoryAddress": 0x20481392,
                "memorySize": 0x0103
            },
            bytearray([0x23, 0x24, 0x20, 0x48, 0x13, 0x92, 0x01, 0x03])
        ),
        (
            ResponseSID.ReadMemoryByAddress,
            {
                "addressAndLengthFormatIdentifier": 0x24,
                "data": [0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F],
            },
            bytearray(b"\x63\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F")
        ),
        (
            ResponseSID.NegativeResponse,
            {
                "nrc": NRC.ServiceNotSupportedInActiveSession
            },
            bytearray([0x7F, 0x23, 0x7F])
        )
    ])
    def test_encode_2(self, sid, data_records_values, payload):
        assert self.read_memory_by_address.encode(sid=sid, data_records_values=data_records_values) == payload

    # decode

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            bytearray([0x10, 0x40]),
            (
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x10,
                                     physical_value="DiagnosticSessionControl",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="subFunction",
                                     length=8,
                                     raw_value=0x40,
                                     physical_value=0x40,
                                     children=(
                                         SingleOccurrenceInfo(name="SPRMIB",
                                                              length=1,
                                                              raw_value=0,
                                                              physical_value="no",
                                                              children=tuple(),
                                                              unit=None),
                                         SingleOccurrenceInfo(name="diagnosticSessionType",
                                                              length=7,
                                                              raw_value=0x40,
                                                              physical_value=0x40,
                                                              children=tuple(),
                                                              unit=None),
                                     ),
                                     unit=None),
            )
        ),
        (
            bytearray([0x50, 0x83, 0x12, 0x34, 0x56, 0x78]),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x50,
                                     physical_value="DiagnosticSessionControl",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="subFunction",
                                     length=8,
                                     raw_value=0x83,
                                     physical_value=0x83,
                                     children=(
                                             SingleOccurrenceInfo(name="SPRMIB",
                                                                  length=1,
                                                                  raw_value=1,
                                                                  physical_value="yes",
                                                                  children=tuple(),
                                                                  unit=None),
                                             SingleOccurrenceInfo(name="diagnosticSessionType",
                                                                  length=7,
                                                                  raw_value=0x03,
                                                                  physical_value="Extended",
                                                                  children=tuple(),
                                                                  unit=None),
                                     ),
                                     unit=None),
                SingleOccurrenceInfo(name="sessionParameterRecord",
                                     length=32,
                                     raw_value=0x12345678,
                                     physical_value=0x12345678,
                                     children=(
                                             SingleOccurrenceInfo(name="P2Server_max",
                                                                  length=16,
                                                                  raw_value=0x1234,
                                                                  physical_value=0x1234,
                                                                  children=tuple(),
                                                                  unit="ms"),
                                             SingleOccurrenceInfo(name="P2*Server_max",
                                                                  length=16,
                                                                  raw_value=0x5678,
                                                                  physical_value=0x5678 * 10,
                                                                  children=tuple(),
                                                                  unit="ms"),
                                     ),
                                     unit=None)
            )
        ),
        (
            bytearray([0x7F, 0x10, 0x84]),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="NegativeResponse",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x10,
                                     physical_value="DiagnosticSessionControl",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="NRC",
                                     length=8,
                                     raw_value=0x84,
                                     physical_value="EngineIsNotRunning",
                                     children=tuple(),
                                     unit=None),
            )
        ),
    ])
    def test_decode_1(self, payload, decoded_message):
        assert self.diagnostic_session_control.decode(payload=payload) == decoded_message

    @pytest.mark.parametrize("payload, decoded_message", [
        (
            bytearray([0x23, 0x24, 0x20, 0x48, 0x13, 0x92, 0x01, 0x03]),
            (
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x23,
                                     physical_value="ReadMemoryByAddress",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="addressAndLengthFormatIdentifier",
                                     length=8,
                                     raw_value=0x24,
                                     physical_value=0x24,
                                     children=(
                                         SingleOccurrenceInfo(name="memorySizeLength",
                                                              length=4,
                                                              raw_value=0x2,
                                                              physical_value=0x2,
                                                              children=tuple(),
                                                              unit=None),
                                         SingleOccurrenceInfo(name="memoryAddressLength",
                                                              length=4,
                                                              raw_value=0x4,
                                                              physical_value=0x4,
                                                              children=tuple(),
                                                              unit=None),
                                     ),
                                     unit=None),
                SingleOccurrenceInfo(name="memoryAddress",
                                     length=32,
                                     raw_value=0x20481392,
                                     physical_value=0x20481392,
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="memorySize",
                                     length=16,
                                     raw_value=0x0103,
                                     physical_value=0x0103,
                                     children=tuple(),
                                     unit=None),
            )
        ),
        (
            bytearray(b"\x63\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F"),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x63,
                                     physical_value="ReadMemoryByAddress",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="data",
                                     length=8,
                                     raw_value=[0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F],
                                     physical_value=(0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F),
                                     children=[tuple()] * 16,
                                     unit=None),
            )
        ),
        (
            bytearray([0x7F, 0x23, 0x7F]),
            (
                SingleOccurrenceInfo(name="RSID",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="NegativeResponse",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="SID",
                                     length=8,
                                     raw_value=0x23,
                                     physical_value="ReadMemoryByAddress",
                                     children=tuple(),
                                     unit=None),
                SingleOccurrenceInfo(name="NRC",
                                     length=8,
                                     raw_value=0x7F,
                                     physical_value="ServiceNotSupportedInActiveSession",
                                     children=tuple(),
                                     unit=None),
            )
        ),
    ])
    def test_decode_2(self, payload, decoded_message):
        assert self.read_memory_by_address.decode(payload=payload) == decoded_message

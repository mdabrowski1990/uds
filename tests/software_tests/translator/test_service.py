from copy import deepcopy

import pytest
from mock import MagicMock, Mock, call, patch

from uds.translator.service import (
    NRC,
    RESPONSE_REQUEST_SID_DIFF,
    AbstractConditionalDataRecord,
    AbstractDataRecord,
    InconsistencyError,
    RequestSID,
    ResponseSID,
    Sequence,
    Service,
    SingleOccurrenceInfo,
)

SCRIPT_LOCATION = "uds.translator.service"

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
    def test_request_structure__set(self, value):
        assert Service.request_structure.fset(self.mock_service, value) is None
        assert self.mock_service._Service__request_structure == tuple(value)
        self.mock_service.validate_message_structure.assert_called_once_with(value)
        
    # response_structure
    
    def test_response_structure__get(self):
        self.mock_service._Service__response_structure = Mock()
        assert Service.response_structure.fget(self.mock_service) == self.mock_service._Service__response_structure

    @pytest.mark.parametrize("value", [(Mock(), Mock()), []])
    def test_response_structure__set(self, value):
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

    # _get_single_data_record_occurrence

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=0,
              max_occurrences=1,
              min_raw_value=0,
              max_raw_value=0xFF),
         [0x10]),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=1,
              max_occurrences=1,
              min_raw_value=0,
              max_raw_value=0x7),
         None),
    ])
    def test_get_single_data_record_occurrence__type_error(self, data_record, value):
        with pytest.raises(TypeError):
            Service._get_single_data_record_occurrence(data_record=data_record, value=value)

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=0,
              max_occurrences=1,
              min_raw_value=0,
              max_raw_value=0xFF),
         0x100),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=1,
              max_occurrences=1,
              min_raw_value=0,
              max_raw_value=0x7),
         -1),
    ])
    def test_get_single_data_record_occurrence__value_error(self, data_record, value):
        with pytest.raises(ValueError):
            Service._get_single_data_record_occurrence(data_record=data_record, value=value)

    def test_get_single_data_record_occurrence__valid__no_occurrence(self):
        mock_data_record = Mock(spec=AbstractDataRecord,
                                is_reoccurring=False,
                                min_occurrences=0,
                                max_occurrences=1)
        assert Service._get_single_data_record_occurrence(data_record=mock_data_record, value=None) == []

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=1,
              max_occurrences=1,
              min_raw_value=0,
              max_raw_value=0xFF),
         0xFF),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=0,
              max_occurrences=1,
              min_raw_value=0,
              max_raw_value=0x7),
         0),
    ])
    def test_get_single_data_record_occurrence__valid__single_raw_value(self, data_record, value):
        assert Service._get_single_data_record_occurrence(data_record=data_record, value=value) == [value]

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=1,
              max_occurrences=1),
         {"a": 1, "b": 2}),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=False,
              min_occurrences=0,
              max_occurrences=1),
         {"param X": 0x00, "param Y": 0xFF, "123": 654}),
    ])
    def test_get_single_data_record_occurrence__valid__single_mapping(self, data_record, value):
        assert (Service._get_single_data_record_occurrence(data_record=data_record, value=value)
                == [data_record.get_raw_value_from_children.return_value])
        data_record.get_raw_value_from_children.assert_called_once_with(value)

    # _get_reoccurring_data_record_occurrences

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_reoccurring_data_record_occurrences__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_data_record = Mock()
        mock_value = Mock()
        with pytest.raises(TypeError):
            Service._get_reoccurring_data_record_occurrences(data_record=mock_data_record, value=mock_value)
        mock_isinstance.assert_called_once_with(mock_value, Sequence)

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=0,
              max_occurrences=8),
         list(range(9))),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=4,
              max_occurrences=8,
              min_raw_value=0,
              max_raw_value=0xF),
         [0, 0, 0]),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=0,
              max_occurrences=2,
              min_raw_value=0,
              max_raw_value=0xF),
         [0xF, -1, 0x5]),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=0,
              max_occurrences=8,
              min_raw_value=0,
              max_raw_value=0xFF),
         [54.23, "Something"]),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=0,
              max_occurrences=8,
              min_raw_value=0,
              max_raw_value=0xF),
         [0x10, 0, 2]),
    ])
    def test_get_reoccurring_data_record_occurrences__value_error(self, data_record, value):
        with pytest.raises(ValueError):
            Service._get_reoccurring_data_record_occurrences(data_record=data_record, value=value)


    def test_get_reoccurring_data_record_occurrences__valid__no_occurrences(self):
        mock_data_record = Mock(spec=AbstractDataRecord,
                                is_reoccurring=True,
                                min_occurrences=0,
                                max_occurrences=None)
        assert Service._get_reoccurring_data_record_occurrences(data_record=mock_data_record, value=[]) == []

    @pytest.mark.parametrize("data_record, value", [
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=4,
              max_occurrences=4,
              min_raw_value=0,
              max_raw_value=0xFF),
         [0xFF,
          {"param X": 0x00, "param Y": 0xFF, "123": 654},
          0x00,
          {"param X": 0x1, "param Y": 0x2, "123": 4}]),
        (Mock(spec=AbstractDataRecord,
              is_reoccurring=True,
              min_occurrences=0,
              max_occurrences=None,
              min_raw_value=0,
              max_raw_value=0x7),
         [0x0,
          0x1,
          0x7,
          {"a": 1, "b": 2},
          {"a": 1, "b": 2},
          {"a": 0, "b": 0}]),
    ])
    def test_get_reoccurring_data_record_occurrences__valid__multiple_occurrences(self, data_record, value):
        expected_value = []
        expected_calls = []
        for _value in value:
            if isinstance(_value, int):
                expected_value.append(_value)
            else:
                expected_value.append(data_record.get_raw_value_from_children.return_value)
                expected_calls.append(call(_value))
        assert Service._get_reoccurring_data_record_occurrences(data_record=data_record, value=value) == expected_value
        data_record.get_raw_value_from_children.assert_has_calls(expected_calls, any_order=False)

    # _get_data_record_occurrences

    @patch(f"{SCRIPT_LOCATION}.Service._get_reoccurring_data_record_occurrences")
    @patch(f"{SCRIPT_LOCATION}.Service._get_single_data_record_occurrence")
    def test_get_data_record_occurrences__single(self, mock_get_single_data_record_occurrence,
                                                 mock_get_reoccurring_data_record_occurrences):
        mock_data_record = Mock(spec=AbstractDataRecord, is_reoccurring=False)
        mock_value = MagicMock()
        assert (Service._get_data_record_occurrences(data_record=mock_data_record, value=mock_value)
                == mock_get_single_data_record_occurrence.return_value)
        mock_get_single_data_record_occurrence.assert_called_once_with(data_record=mock_data_record,
                                                                       value=mock_value)
        mock_get_reoccurring_data_record_occurrences.assert_not_called()

    @patch(f"{SCRIPT_LOCATION}.Service._get_reoccurring_data_record_occurrences")
    @patch(f"{SCRIPT_LOCATION}.Service._get_single_data_record_occurrence")
    def test_get_data_record_occurrences__multiple(self, mock_get_single_data_record_occurrence,
                                                 mock_get_reoccurring_data_record_occurrences):
        mock_data_record = Mock(spec=AbstractDataRecord, is_reoccurring=True)
        mock_value = MagicMock()
        assert (Service._get_data_record_occurrences(data_record=mock_data_record, value=mock_value)
                == mock_get_reoccurring_data_record_occurrences.return_value)
        mock_get_reoccurring_data_record_occurrences.assert_called_once_with(data_record=mock_data_record,
                                                                             value=mock_value)
        mock_get_single_data_record_occurrence.assert_not_called()

    # _decode_payload

    @pytest.mark.parametrize("payload, message_structure", [
        ([0xFF], [Mock(length=8, min_occurrences=0, max_occurrences=1)]),
         (list(range(100)), [Mock(spec=AbstractDataRecord, length=48, min_occurrences=1, max_occurrences=1),
                             Mock(length=8, min_occurrences=10, max_occurrences=None)]),
    ])
    def test_decode_payload__not_implemented(self, payload, message_structure):
        with pytest.raises(NotImplementedError):
            Service._decode_payload(payload=payload, message_structure=message_structure)

    @pytest.mark.parametrize("payload, message_structure", [
        ([0xFF], [Mock(spec=AbstractDataRecord, length=8, min_occurrences=2, max_occurrences=2)]),
         (list(range(4)), [Mock(spec=AbstractDataRecord, length=40, min_occurrences=1, max_occurrences=1),
                           Mock(spec=AbstractDataRecord, length=16, min_occurrences=10, max_occurrences=None)]),
    ])
    def test_decode_payload__value_error(self, payload, message_structure):
        with pytest.raises(ValueError):
            Service._decode_payload(payload=payload, message_structure=message_structure)

    @pytest.mark.parametrize("payload, message_structure", [
        ([0xFF], [Mock(spec=AbstractDataRecord, length=7, min_occurrences=0, max_occurrences=1)]),
         (list(range(100)), [Mock(spec=AbstractDataRecord, length=40, min_occurrences=1, max_occurrences=1),
                             Mock(spec=AbstractDataRecord, length=16, min_occurrences=10, max_occurrences=None)]),
    ])
    def test_decode_payload__runtime_error(self, payload, message_structure):
        with pytest.raises(RuntimeError):
            Service._decode_payload(payload=payload, message_structure=message_structure)

    @pytest.mark.parametrize("payload, message_structure, message_continuation", [
        ((0xCA, 0xFE),
         [Mock(spec=AbstractDataRecord, length=7, min_occurrences=0, max_occurrences=1),
          Mock(spec=AbstractConditionalDataRecord)],
         [Mock(spec=AbstractDataRecord, length=1, min_occurrences=9, max_occurrences=9)]),
        (list(range(100)),
         [Mock(spec=AbstractDataRecord, length=9, min_occurrences=10, max_occurrences=10),
          Mock(spec=AbstractConditionalDataRecord)],
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=None)]),
    ])
    def test_decode_payload__condition_runtime_error(self, payload, message_structure, message_continuation):
        self.mock_int_to_bytes.return_value = b"\x00"
        mock_get_message_continuation = Mock(return_value=message_continuation)
        message_structure[-1].get_message_continuation = mock_get_message_continuation
        with pytest.raises(RuntimeError):
            Service._decode_payload(payload=payload, message_structure=message_structure)

    @pytest.mark.parametrize("payload, message_structure", [
        ([0xFF], [Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=1)]),
        (b"\x12\x34\x56\x78\x9A", [Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8),
                                   Mock(spec=AbstractDataRecord, length=8, min_occurrences=2, max_occurrences=2),
                                   Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1)]),
         (list(range(100)), [Mock(spec=AbstractDataRecord, length=48, min_occurrences=1, max_occurrences=1),
                             Mock(spec=AbstractDataRecord, length=8, min_occurrences=10, max_occurrences=None)]),
    ])
    def test_decode_payload__valid__no_condition(self, payload, message_structure):
        assert (Service._decode_payload(payload=payload,
                                        message_structure=message_structure)
                == tuple(data_record.get_occurrence_info.return_value for data_record in message_structure))

    @pytest.mark.parametrize("payload, message_structure, message_continuation", [
        ((0xCA, 0xFE),
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=1),
          Mock(spec=AbstractConditionalDataRecord)],
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=1, max_occurrences=1)]),
        (list(range(100)),
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=10, max_occurrences=10),
          Mock(spec=AbstractConditionalDataRecord)],
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=None)]),
    ])
    def test_decode_payload__valid__condition(self, payload, message_structure, message_continuation):
        self.mock_int_to_bytes.side_effect = [tuple(payload[:message_structure[0].max_occurrences]),
                                              tuple(payload[message_structure[0].max_occurrences:])]
        mock_get_message_continuation = Mock(return_value=message_continuation)
        message_structure[-1].get_message_continuation = mock_get_message_continuation
        message_continuation[0].get_occurrence_info.return_value = {
            "length": message_continuation[0].length,
            "raw_value": range(int(len(payload[message_structure[0].max_occurrences:]) * 8 // message_continuation[0].length))
        }
        assert (Service._decode_payload(payload=payload,
                                        message_structure=message_structure)
                == tuple(dr.get_occurrence_info.return_value
                         for dr in message_structure + message_continuation if isinstance(dr, AbstractDataRecord)))
        self.mock_int_to_bytes.assert_called_once()

    @pytest.mark.parametrize("payload, message_structure, message_continuation", [
        ((0xCA, 0xFE),
         [Mock(spec=AbstractDataRecord, length=16, min_occurrences=1, max_occurrences=1),
          Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=1),
          Mock(spec=AbstractConditionalDataRecord)],
         [Mock(spec=AbstractDataRecord, length=1, min_occurrences=8, max_occurrences=8)]),
        ([],
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=1),
          Mock(spec=AbstractConditionalDataRecord)],
         [Mock(spec=AbstractDataRecord, length=8, min_occurrences=0, max_occurrences=None)]),
    ])
    def test_decode_payload__valid__with_uncalled_condition(self, payload, message_structure, message_continuation):
        mock_get_message_continuation = Mock(return_value=message_continuation)
        message_structure[-1].get_message_continuation = mock_get_message_continuation
        assert isinstance(Service._decode_payload(payload=payload, message_structure=message_structure), tuple)
        # self.mock_int_to_bytes.assert_not_called()

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
        values_copy = deepcopy(data_records_values)
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        with pytest.raises(RuntimeError):
            Service._encode_message(data_records_values=data_records_values,
                                    message_structure=message_structure)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=values_copy[dr.name])
                                                           for dr in message_structure], any_order=False)
        self.mock_int_to_bytes.assert_not_called()

    @pytest.mark.parametrize("message_structure, data_records_values", [
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=8)],
         {"Param 1": 0, "Param 2": 1}),
        ([Mock(spec=AbstractDataRecord, name="XYZ", length=24)],
         {"XYZ": {"Child 1": 1, "Child 2": 2, "Child 3": 0}, "ABC": None}),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__value_error(self, mock_get_data_record_occurrences,
                                         message_structure, data_records_values):
        values_copy = deepcopy(data_records_values)
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        with pytest.raises(ValueError):
            Service._encode_message(data_records_values=data_records_values,
                                    message_structure=message_structure)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=values_copy[dr.name])
                                                           for dr in message_structure], any_order=False)
        self.mock_int_to_bytes.assert_not_called()

    @pytest.mark.parametrize("message_structure, data_records_values", [
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=8)],
         {}),
        ([Mock(spec=AbstractDataRecord, name="Data Record - 1", length=7),
          Mock(spec=AbstractDataRecord, name="Data Record - 2", length=3)],
         {"Data Record - 1": [{"Data Record - 1.1": 0, "Data Record - 1.2": 2},
                              0,
                              {"Data Record - 1.1": 9, "Data Record - 1.2": {"A": 1, "B": 2}}],
          "Data Record - 3": [{"Data Record - 3.1": 0, "Data Record - 3.2": 2}]}),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__inconsistency_error(self, mock_get_data_record_occurrences,
                                         message_structure, data_records_values):
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        with pytest.raises(InconsistencyError):
            Service._encode_message(data_records_values=data_records_values,
                                    message_structure=message_structure)
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
        values_copy = deepcopy(data_records_values)
        self.mock_int_to_bytes.return_value = payload
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        assert Service._encode_message(data_records_values=data_records_values,
                                       message_structure=message_structure) == bytearray(payload)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=values_copy[dr.name])
                                                           for dr in message_structure], any_order=False)
        self.mock_int_to_bytes.assert_called_once()

    @pytest.mark.parametrize("message_structure, data_records_values, message_continuation, payload", [
        ([Mock(spec=AbstractDataRecord, name="PAram", length=8),
          Mock(spec=AbstractConditionalDataRecord)],
         {"PAram": 0xD0},
         [],
         b"\xD0"),
        ([Mock(spec=AbstractDataRecord, name="A #1", length=2),
          Mock(spec=AbstractConditionalDataRecord),
          Mock(spec=AbstractDataRecord, name="A #3", length=8)],
         {"A #1": [0, 1, 0, 1], "A #2": [0x3, 0x0], "A #3": 0xFF},
         [Mock(spec=AbstractDataRecord, name="A #2", length=4)],
         b"\xBE\xEF"),
        ([Mock(spec=AbstractDataRecord, name="Data Record - 1", length=8),
          Mock(spec=AbstractConditionalDataRecord),
          Mock(spec=AbstractConditionalDataRecord, get_message_continuation=Mock(return_value=[]))],
         {"Data Record - 1": [{"Data Record - 1.1": 0, "Data Record - 1.2": 2},
                              0,
                              {"Data Record - 1.1": 9, "Data Record - 1.2": {"A": 1, "B": 2}}],
          "Data Record - 2": [{"Data Record - 2.1": 0, "Data Record - 2.2": 2}]},
         [Mock(spec=AbstractDataRecord, name="Data Record - 2", length=24)],
         [0xCA, 0xFF, 0x0E, 0x56]),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__valid__condition(self, mock_get_data_record_occurrences,
                                              message_structure, data_records_values,
                                              message_continuation, payload):
        values_copy = deepcopy(data_records_values)
        self.mock_int_to_bytes.return_value = payload
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure + message_continuation:
            data_record.name = data_record._extract_mock_name()
        mock_get_message_continuation = Mock(return_value=message_continuation)
        message_structure[1].get_message_continuation = mock_get_message_continuation
        assert Service._encode_message(data_records_values=data_records_values,
                                       message_structure=message_structure) == bytearray(payload)
        mock_get_data_record_occurrences.assert_has_calls([call(data_record=dr, value=values_copy[dr.name])
                                                           for dr in message_structure + message_continuation
                                                           if isinstance(dr, AbstractDataRecord)],
                                                          any_order=True)
        self.mock_int_to_bytes.assert_called()
        mock_get_message_continuation.assert_called_once()

    @pytest.mark.parametrize("message_structure, data_records_values, message_continuation_1, message_continuation_2, "
                             "payload", [
        ([Mock(spec=AbstractDataRecord, name="Data Record - 1", length=8),
          Mock(spec=AbstractConditionalDataRecord),
          Mock(spec=AbstractConditionalDataRecord)],
         {"Data Record - 1": [{"Data Record - 1.1": 0, "Data Record - 1.2": 2},
                              0,
                              {"Data Record - 1.1": 9, "Data Record - 1.2": {"A": 1, "B": 2}}],
          "Data Record - 2": [{"Data Record - 2.1": 0, "Data Record - 2.2": 2}],
          "Data Record - 3": 0x00},
         [Mock(spec=AbstractDataRecord, name="Data Record - 2", length=8)],
         [Mock(spec=AbstractDataRecord, name="Data Record - 3", length=8)],
         [0x12, 0x34, 0x56]),
        ([Mock(spec=AbstractDataRecord, name="A", length=8),
          Mock(spec=AbstractConditionalDataRecord),
          Mock(spec=AbstractConditionalDataRecord),
          Mock(spec=AbstractDataRecord, name="D", length=16)],
         {"A": 0xF0,
          "B1": 0xE1,
          "B2": 0xD2,
          "C": 0xC3,
          "D": 0xB4A5},
         [Mock(spec=AbstractDataRecord, name="B1", length=8), Mock(spec=AbstractDataRecord, name="B2", length=8)],
         [Mock(spec=AbstractDataRecord, name="C", length=8, min_occurrences=0)],
         [0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5]),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__valid__condition_after_condition(self, mock_get_data_record_occurrences,
                                                              message_structure, data_records_values,
                                                              message_continuation_1, message_continuation_2, payload):
        values_copy = deepcopy(data_records_values)
        self.mock_int_to_bytes.return_value = payload
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure + message_continuation_1 + message_continuation_2:
            data_record.name = data_record._extract_mock_name()
        mock_get_message_continuation_1 = Mock(return_value=message_continuation_1)
        mock_get_message_continuation_2 = Mock(return_value=message_continuation_2)
        message_structure[1].get_message_continuation = mock_get_message_continuation_1
        message_structure[2].get_message_continuation = mock_get_message_continuation_2
        assert Service._encode_message(data_records_values=data_records_values,
                                       message_structure=message_structure) == bytearray(payload)
        mock_get_data_record_occurrences.assert_has_calls(
            [call(data_record=dr, value=values_copy[dr.name])
             for dr in message_structure + message_continuation_1 + message_continuation_2
             if isinstance(dr, AbstractDataRecord)],
            any_order=True)
        self.mock_int_to_bytes.assert_called()
        mock_get_message_continuation_1.assert_called_once()
        mock_get_message_continuation_2.assert_called_once()

    @pytest.mark.parametrize("message_structure, data_records_values, payload", [
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=8),
          Mock(spec=AbstractConditionalDataRecord)],
         {"Param 1": []},
         b""),
        ([Mock(spec=AbstractDataRecord, name="Param 1", length=8, min_occurrences=0, max_occurrences=1),
          Mock(spec=AbstractConditionalDataRecord)],
         {},
         b""),
    ])
    @patch(f"{SCRIPT_LOCATION}.Service._get_data_record_occurrences")
    def test_encode_message__valid__with_uncalled_condition(self, mock_get_data_record_occurrences,
                                                            message_structure, data_records_values,
                                                            payload):
        self.mock_int_to_bytes.return_value = payload
        mock_get_data_record_occurrences.side_effect = self.get_data_record_occurrences
        for data_record in message_structure:
            data_record.name = data_record._extract_mock_name()
        assert Service._encode_message(data_records_values=data_records_values,
                                       message_structure=message_structure) == bytearray(payload + payload)
        self.mock_int_to_bytes.assert_called()

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
            message_structure=self.mock_service.request_structure)

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
            message_structure=self.mock_service.response_structure)

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
    def test_decode__value_error(self, payload):
        with pytest.raises(ValueError):
            Service.decode(self.mock_service, payload=payload)

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

    @pytest.mark.parametrize("sid, rsid, data_records_values", [
        (None, None, {}),
        (Mock(), Mock(), Mock()),
    ])
    def test_encode__value_error(self, sid, rsid, data_records_values):
        with pytest.raises(ValueError):
            Service.encode(self.mock_service, sid=sid, rsid=rsid, data_records_values=data_records_values)

    @pytest.mark.parametrize("data_records_values", [
        {"NRC": 0x10, "unindentifeid": 0},
        {},
    ])
    def test_encode__inconsistency_error(self, data_records_values):
        with pytest.raises(InconsistencyError):
            Service.encode(self.mock_service,
                           sid=None,
                           rsid=ResponseSID.NegativeResponse,
                           data_records_values=data_records_values)

    @pytest.mark.parametrize("data_records_values", [Mock(), {"a": 1, "b": [{"zyx a": 94}, 0xFF]}])
    def test_encode__request(self, data_records_values):
        assert (Service.encode(self.mock_service,
                              sid=self.mock_service.request_sid,
                              data_records_values=data_records_values)
                == self.mock_service.encode_request.return_value)
        self.mock_service.encode_request.assert_called_once_with(data_records_values=data_records_values)

    @pytest.mark.parametrize("data_records_values", [{}, {"a": 1, "b": [{"zyx a": 94}, 0xFF]}])
    def test_encode__positive_response(self, data_records_values):
        assert (Service.encode(self.mock_service,
                               rsid=self.mock_service.response_sid,
                               data_records_values=data_records_values)
                == self.mock_service.encode_positive_response.return_value)
        self.mock_service.encode_positive_response.assert_called_once_with(data_records_values=data_records_values)

    @pytest.mark.parametrize("data_records_values", [{"NRC": 1}, {"NRC": Mock()}])
    def test_encode__negative_response(self, data_records_values):
        assert (Service.encode(self.mock_service,
                               rsid=ResponseSID.NegativeResponse,
                               sid=self.mock_service.request_sid,
                               data_records_values=data_records_values)
                == self.mock_service.encode_negative_response.return_value)
        self.mock_service.encode_negative_response.assert_called_once_with(nrc=data_records_values["NRC"])

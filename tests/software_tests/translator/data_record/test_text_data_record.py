import pytest
from mock import MagicMock, Mock, patch

from uds.translator.data_record.text_data_record import (
    MAX_DTC_VALUE,
    MIN_DTC_VALUE,
    TextDataRecord,
    TextEncoding,
    decode_ascii,
    decode_bcd,
    decode_dtc,
    encode_dtc,
)

SCRIPT_LOCATION = "uds.translator.data_record.text_data_record"


class TestEncodingAndDecodingFunctions:
    """Unit tests for encoding and decoding functions used by TextDataRecord."""

    # decode_ascii

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            decode_ascii(value)
        mock_isinstance.assert_called_once_with(value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__value_error__non_ascii(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_len = Mock(return_value=1)
        mock_value = MagicMock(spec=str, __len__=mock_len)
        mock_value.isascii.return_value = False
        with pytest.raises(ValueError):
            decode_ascii(mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_value.isascii.assert_called_once_with()

    @pytest.mark.parametrize("length_value", [0, 2])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__value_error__wrong_length(self, mock_isinstance, length_value):
        mock_isinstance.return_value = True
        mock_len = Mock(return_value=length_value)
        mock_value = MagicMock(spec=str, __len__=mock_len)
        mock_value.isascii.return_value = True
        with pytest.raises(ValueError):
            decode_ascii(mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_len.assert_called_once_with()

    @patch(f"{SCRIPT_LOCATION}.ord")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__valid(self, mock_isinstance, mock_ord):
        mock_isinstance.return_value = True
        mock_len = Mock(return_value=1)
        mock_value = MagicMock(spec=str, __len__=mock_len)
        mock_value.isascii.return_value = True
        assert decode_ascii(mock_value) == mock_ord.return_value
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_value.isascii.assert_called_once_with()
        mock_ord.assert_called_once_with(mock_value)
        mock_len.assert_called_once_with()

    # decode_bcd

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_bcd__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            decode_bcd(value)
        mock_isinstance.assert_called_once_with(value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_bcd__value_error__non_bcd(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_len = Mock(return_value=1)
        mock_value = MagicMock(spec=str, __len__=mock_len)
        mock_value.isdecimal.return_value = False
        with pytest.raises(ValueError):
            decode_bcd(mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_value.isdecimal.assert_called_once_with()

    @pytest.mark.parametrize("length_value", [0, 2])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_bcd__value_error__wrong_length(self, mock_isinstance, length_value):
        mock_isinstance.return_value = True
        mock_len = Mock(return_value=length_value)
        mock_value = MagicMock(spec=str, __len__=mock_len)
        mock_value.isdecimal.return_value = True
        with pytest.raises(ValueError):
            decode_bcd(mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_len.assert_called_once_with()

    @patch(f"{SCRIPT_LOCATION}.int")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_bcd__valid(self, mock_isinstance, mock_int):
        mock_isinstance.return_value = True
        mock_len = Mock(return_value=1)
        mock_value = MagicMock(spec=str, __len__=mock_len)
        mock_value.isdecimal.return_value = True
        assert decode_bcd(mock_value) == mock_int.return_value
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_value.isdecimal.assert_called_once_with()
        mock_int.assert_called_once_with(mock_value)
        mock_len.assert_called_once_with()

    # decode_dtc

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_dtc__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            decode_dtc(value)
        mock_isinstance.assert_called_once_with(value, str)

    @pytest.mark.parametrize("value", ["P0FFF00", "A0123-00", "0x123456", "U012-300"])
    def test_decode_dtc__value_error(self, value):
        with pytest.raises(ValueError):
            decode_dtc(value)

    @pytest.mark.parametrize("obd_dtc, uds_dtc", [
        ("p0000-00", 0x000000),
        ("C1FED-CB", 0x5FEDCB),
        ("b3F4E-5D", 0xBF4E5D),
        ("U3FFF-FF", 0xFFFFFF),
    ])
    def test_decode_dtc__valid(self, obd_dtc, uds_dtc):
        assert decode_dtc(obd_dtc) == uds_dtc

    # encode_dtc

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_encode_dtc__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            encode_dtc(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [MIN_DTC_VALUE - 1, MAX_DTC_VALUE + 1])
    def test_decode_dtc__value_error(self, value):
        with pytest.raises(ValueError):
            encode_dtc(value)

    @pytest.mark.parametrize("obd_dtc, uds_dtc", [
        ("P0000-00", 0x000000),
        ("C1FED-CB", 0x5FEDCB),
        ("B0123-45", 0x812345),
        ("U3FFF-FF", 0xFFFFFF),
    ])
    def test_decode_dtc__valid(self, obd_dtc, uds_dtc):
        assert encode_dtc(uds_dtc) == obd_dtc


class TestTextDataRecord:
    """Unit tests for `TextDataRecord` class."""

    def setup_method(self):
        self.mock_data_record = Mock(spec=TextDataRecord)
        # patching
        self._patcher_abstract_data_record_init = patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
        self.mock_abstract_data_record_init = self._patcher_abstract_data_record_init.start()
        self._patcher_abstract_data_record_get_physical_values \
            = patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.get_physical_values")
        self.mock_abstract_data_record_get_physical_values \
            = self._patcher_abstract_data_record_get_physical_values.start()
        self._patcher_text_encoding_validate_member = patch(f"{SCRIPT_LOCATION}.TextEncoding.validate_member")
        self.mock_text_encoding_validate_member = self._patcher_text_encoding_validate_member.start()

    def teardown_method(self):
        self._patcher_abstract_data_record_init.stop()
        self._patcher_abstract_data_record_get_physical_values.stop()
        self._patcher_text_encoding_validate_member.stop()

    # __init__

    @pytest.mark.parametrize("name, encoding, min_occurrences, max_occurrences", [
        (Mock(), Mock(), Mock(), Mock()),
        ("Some Name", TextEncoding.ASCII, 0, None),
    ])
    def test_init(self, name, encoding, min_occurrences, max_occurrences):
        mock_length = Mock(spec=int)
        mock_encoding = MagicMock(__getitem__=MagicMock(return_value=mock_length))
        mock_encodings = MagicMock(__getitem__=MagicMock(return_value=mock_encoding))
        self.mock_data_record._TextDataRecord__ENCODINGS = mock_encodings
        assert TextDataRecord.__init__(self.mock_data_record,
                                       name=name,
                                       encoding=encoding,
                                       min_occurrences=min_occurrences,
                                       max_occurrences=max_occurrences) is None
        assert self.mock_data_record.encoding == encoding
        self.mock_abstract_data_record_init.assert_called_once_with(name=name,
                                                                    children=tuple(),
                                                                    min_occurrences=min_occurrences,
                                                                    max_occurrences=max_occurrences,
                                                                    length=mock_length)
        mock_encodings.__getitem__.assert_called_once_with(encoding)
        mock_encoding.__getitem__.assert_called_once_with("length")

    # encoding

    def test_encoding__get(self):
        self.mock_data_record._TextDataRecord__encoding = Mock()
        assert TextDataRecord.encoding.fget(self.mock_data_record) == self.mock_data_record._TextDataRecord__encoding

    @pytest.mark.parametrize("value", [Mock(), "Some Encoding"])
    def test_encoding__set(self, value):
        self.mock_data_record._TextDataRecord__encoding = Mock()
        assert TextDataRecord.encoding.fset(self.mock_data_record, value) is None
        assert self.mock_data_record._TextDataRecord__encoding == self.mock_text_encoding_validate_member.return_value
        self.mock_text_encoding_validate_member.assert_called_once_with(value)

    # max_raw_value

    def test_max_raw_value__ascii(self):
        self.mock_data_record.encoding = TextEncoding.ASCII
        assert TextDataRecord.max_raw_value.fget(self.mock_data_record) == 0x7F

    def test_max_raw_value__bcd(self):
        self.mock_data_record.encoding = TextEncoding.BCD
        assert TextDataRecord.max_raw_value.fget(self.mock_data_record) == 9

    def test_max_raw_value__dtc(self):
        self.mock_data_record.encoding = TextEncoding.DTC_OBD_FORMAT
        assert TextDataRecord.max_raw_value.fget(self.mock_data_record) == MAX_DTC_VALUE

    def test_max_raw_value__not_implemented(self):
        self.mock_data_record.encoding = Mock()
        with pytest.raises(NotImplementedError):
            TextDataRecord.max_raw_value.fget(self.mock_data_record)

    # get_physical_values

    @pytest.mark.parametrize("raw_values, characters", [
        (range(10), "0"),
        ([Mock(), Mock(), Mock()], "a"),
    ])
    def test_get_physical_values(self, raw_values, characters):
        self.mock_abstract_data_record_get_physical_values.return_value = tuple(characters)
        assert TextDataRecord.get_physical_values(self.mock_data_record, *raw_values) == characters
        self.mock_abstract_data_record_get_physical_values.assert_called_once_with(*raw_values)

    # get_physical_value

    @pytest.mark.parametrize("raw_value", [Mock(), 0])
    def test_get_physical_value(self, raw_value):
        mock_encode = Mock()
        mock_encoding = MagicMock(__getitem__=MagicMock(return_value=mock_encode))
        mock_encodings = MagicMock(__getitem__=MagicMock(return_value=mock_encoding))
        self.mock_data_record._TextDataRecord__ENCODINGS = mock_encodings
        assert TextDataRecord.get_physical_value(self.mock_data_record, raw_value=raw_value) == mock_encode.return_value
        self.mock_data_record._validate_raw_value.assert_called_once_with(raw_value)
        mock_encodings.__getitem__.assert_called_once_with(self.mock_data_record.encoding)
        mock_encoding.__getitem__.assert_called_once_with("encode")

    # get_raw_value

    @pytest.mark.parametrize("physical_value", [Mock(), "Some character"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_raw_value__type_error(self, mock_isinstance, physical_value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TextDataRecord.get_raw_value(self.mock_data_record, physical_value=physical_value)
        mock_isinstance.assert_called_once_with(physical_value, str)

    @pytest.mark.parametrize("physical_value", ["a", "1"])
    def test_get_raw_value(self, physical_value):
        mock_decode = Mock()
        mock_encoding = MagicMock(__getitem__=MagicMock(return_value=mock_decode))
        mock_encodings = MagicMock(__getitem__=MagicMock(return_value=mock_encoding))
        self.mock_data_record._TextDataRecord__ENCODINGS = mock_encodings
        assert (TextDataRecord.get_raw_value(self.mock_data_record, physical_value=physical_value)
                == mock_decode.return_value)
        mock_encodings.__getitem__.assert_called_once_with(self.mock_data_record.encoding)
        mock_encoding.__getitem__.assert_called_once_with("decode")


@pytest.mark.integration
class TestTextDataRecordIntegration:
    """Integration tests for `TextDataRecord` class."""

    def setup_class(self):
        self.bcd = TextDataRecord(name="BCD",
                                  encoding=TextEncoding.BCD)
        self.ascii = TextDataRecord(name="ASCII",
                                    encoding=TextEncoding.ASCII)
        self.dtc = TextDataRecord(name="DTC",
                                  min_occurrences=1,
                                  max_occurrences=1,
                                  encoding=TextEncoding.DTC_OBD_FORMAT)

    # get_physical_values

    @pytest.mark.parametrize("raw_values, text", [
        (range(10), "0123456789"),
        ([9, 0, 9, 0, 5, 2], "909052"),
    ])
    def test_get_physical_values__bcd(self, raw_values, text):
        assert self.bcd.get_physical_values(*raw_values) == text

    @pytest.mark.parametrize("raw_values, text", [
        ([0x53, 0x6f, 0x6d, 0x65, 0x20, 0x56, 0x61, 0x6c, 0x75, 0x65], "Some Value"),
        ((0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x7F), "\x00\x10\x20\x30\x40\x50\x60\x70\x7F"),
    ])
    def test_get_physical_values__ascii(self, raw_values, text):
        assert self.ascii.get_physical_values(*raw_values) == text

    # get_physical_value

    @pytest.mark.parametrize("raw_value", [0xA, 0xF])
    def test_get_physical_value__bcd__value_error(self, raw_value):
        with pytest.raises(ValueError):
            self.bcd.get_physical_value(raw_value)

    @pytest.mark.parametrize("raw_value", [0x80, 0xA7, 0xFF])
    def test_get_physical_value__ascii__value_error(self, raw_value):
        with pytest.raises(ValueError):
            self.ascii.get_physical_value(raw_value)

    @pytest.mark.parametrize("raw_value, text", [
        (0x012345, "P0123-45"),
        (0x634567, "C2345-67"),
        (0x812345, "B0123-45"),
        (0xDFEDCB, "U1FED-CB"),
    ])
    def test_get_physical_value__dtc(self, raw_value, text):
        assert self.dtc.get_physical_value(raw_value) == text

    # get_raw_value

    @pytest.mark.parametrize("character", ["A", "12"])
    def test_get_raw_value__bcd__value_error(self, character):
        with pytest.raises(ValueError):
            self.bcd.get_raw_value(character)

    @pytest.mark.parametrize("character", ["ó", "ǖ", "ABC"])
    def test_get_raw_value__ascii__value_error(self, character):
        with pytest.raises(ValueError):
            self.ascii.get_raw_value(character)

    # raw and physical value conversion

    @pytest.mark.parametrize("raw_value", [0, 1, 9])
    def test_get_physical_value_get_raw_value__bcd(self, raw_value):
        character = self.bcd.get_physical_value(raw_value)
        assert self.bcd.get_raw_value(character) == raw_value

    @pytest.mark.parametrize("raw_value", [0x00, 0x57, 0x7F])
    def test_get_physical_value_get_raw_value__ascii(self, raw_value):
        character = self.ascii.get_physical_value(raw_value)
        assert self.ascii.get_raw_value(character) == raw_value

    @pytest.mark.parametrize("uds_dtc", [0x000000, 0x9F0E35, 0xFFFFFF])
    def test_get_physical_value_get_raw_value__dtc(self, uds_dtc):
        obd_dtc = self.dtc.get_physical_value(uds_dtc)
        assert self.dtc.get_raw_value(obd_dtc) == uds_dtc

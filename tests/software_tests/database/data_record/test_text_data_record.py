import pytest
from mock import MagicMock, Mock, call, patch

from uds.database.data_record.text_data_record import TextDataRecord, TextEncoding

SCRIPT_LOCATION = "uds.database.data_record.text_data_record"


class TestTextDataRecord:
    """Unit tests for TextDataRecord."""

    def setup_method(self):
        self.mock_data_record = Mock(spec=TextDataRecord)
        # patching
        self._patcher_abstract_data_record_init = patch(f"{SCRIPT_LOCATION}.AbstractDataRecord.__init__")
        self.mock_abstract_data_record_init = self._patcher_abstract_data_record_init.start()
        self._patcher_text_encoding_validate_member = patch(f"{SCRIPT_LOCATION}.TextEncoding.validate_member")
        self.mock_text_encoding_validate_member = self._patcher_text_encoding_validate_member.start()

    def teardown_method(self):
        self._patcher_abstract_data_record_init.stop()
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

    # __decode_ascii

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TextDataRecord._TextDataRecord__decode_ascii(value)
        mock_isinstance.assert_called_once_with(value, str)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_value = Mock(spec=str)
        mock_value.isascii.return_value = False
        with pytest.raises(ValueError):
            TextDataRecord._TextDataRecord__decode_ascii(mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_value.isascii.assert_called_once_with()

    @patch(f"{SCRIPT_LOCATION}.ord")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_decode_ascii__valid(self, mock_isinstance, mock_ord):
        mock_isinstance.return_value = True
        mock_value = Mock(spec=str)
        mock_value.isascii.return_value = True
        assert TextDataRecord._TextDataRecord__decode_ascii(mock_value) == mock_ord.return_value
        mock_isinstance.assert_called_once_with(mock_value, str)
        mock_value.isascii.assert_called_once_with()
        mock_ord.assert_called_once_with(mock_value)

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

    def test_max_raw_value__not_implemented(self):
        self.mock_data_record.encoding = Mock()
        with pytest.raises(NotImplementedError):
            TextDataRecord.max_raw_value.fget(self.mock_data_record)

    # get_physical_values

    def test_get_physical_values__runtime_error(self):
        self.mock_data_record.is_reoccurring = False
        with pytest.raises(RuntimeError):
            TextDataRecord.get_physical_values(self.mock_data_record, Mock(), Mock())

    def test_get_physical_values__value_error(self):
        self.mock_data_record.is_reoccurring = True
        with pytest.raises(ValueError):
            TextDataRecord.get_physical_values(self.mock_data_record)

    @pytest.mark.parametrize("raw_values, character", [
        (range(10), "0"),
        ([Mock(), Mock(), Mock()], "a"),
    ])
    def test_get_physical_values(self, raw_values, character):
        self.mock_data_record.is_reoccurring = True
        self.mock_data_record.get_physical_value.return_value = character
        assert (TextDataRecord.get_physical_values(self.mock_data_record, *raw_values)
                == str(character) * len(raw_values))
        self.mock_data_record.get_physical_value.assert_has_calls([call(raw_value) for raw_value in raw_values],
                                                                  any_order=False)

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
@pytest.mark.integration
class TestTextDataRecordIntegration:
    """Integration tests for the TextDataRecord class."""

    def setup_class(self):
        self.bcd = TextDataRecord(name="BCD",
                                  encoding=TextEncoding.BCD)
        self.ascii = TextDataRecord(name="ASCII",
                                    encoding=TextEncoding.ASCII)

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

    # get_raw_value

    @pytest.mark.parametrize("character", ["A", " "])
    def test_get_raw_value__bcd__value_error(self, character):
        with pytest.raises(ValueError):
            self.bcd.get_raw_value(character)

    @pytest.mark.parametrize("character", ["ó", "ǖ", "♬"])
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

import pytest
from mock import Mock, patch, MagicMock

from time import perf_counter, time

from uds.utilities.conversions import (
    MAX_DTC_VALUE,
    MIN_DTC_VALUE,
    Endianness,
    InconsistencyError,
    bytes_to_hex,
    bytes_to_int,
    get_signed_value_decoding_formula,
    get_signed_value_encoding_formula,
    int_to_bytes,
    int_to_obd_dtc,
    obd_dtc_to_int, TimeSync
)

SCRIPT_LOCATION = "uds.utilities.conversions"


class TestFunctions:
    """Unit tests for module functions."""

    def setup_method(self):
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_endianness = patch(f"{SCRIPT_LOCATION}.Endianness.validate_member")
        self.mock_validate_endianness = self._patcher_validate_endianness.start()

    def teardown_method(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_endianness.stop()

    # bytes_to_hex

    @pytest.mark.parametrize("bytes_list, expected_output", [
        (b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F",
         "(0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F)"),
        ([0x00], "(0x00)"),
    ])
    def test_bytes_to_hex(self, bytes_list, expected_output):
        assert bytes_to_hex(bytes_list) == expected_output
        self.mock_validate_raw_bytes.assert_called_once_with(bytes_list)

    # bytes_to_int

    @pytest.mark.parametrize("bytes_list, endianness, expected_output", [
        ([], Endianness.BIG_ENDIAN, 0),
        ([0xF0], Endianness.LITTLE_ENDIAN, 0xF0),
        ((0xF0, 0xE1), Endianness.BIG_ENDIAN, 0xF0E1),
        (bytearray([0xF0, 0xE1]), Endianness.LITTLE_ENDIAN, 0xE1F0),
        ([0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.BIG_ENDIAN, 0x987654321F),
        (bytes([0x98, 0x76, 0x54, 0x32, 0x1F]), Endianness.LITTLE_ENDIAN, 0x1F32547698),
    ])
    def test_bytes_to_int(self, bytes_list, endianness, expected_output):
        self.mock_validate_endianness.side_effect = lambda arg: arg
        assert bytes_to_int(bytes_list=bytes_list, endianness=endianness) == expected_output
        self.mock_validate_raw_bytes.assert_called_once_with(bytes_list, allow_empty=True)
        if bytes_list:
            self.mock_validate_endianness.assert_called_once_with(endianness)

    # int_to_bytes

    @pytest.mark.parametrize("int_value", [None, 5., "not an integer value"])
    def test_int_to_bytes__int_value_type_error(self, int_value):
        with pytest.raises(TypeError):
            int_to_bytes(int_value=int_value)

    @pytest.mark.parametrize("int_value", [0, 100])
    @pytest.mark.parametrize("size", [5., "not an integer value"])
    def test_int_to_bytes__size_type_error(self, int_value, size):
        with pytest.raises(TypeError):
            int_to_bytes(int_value=int_value, size=size)

    @pytest.mark.parametrize("int_value", [-99, -1])
    def test_int_to_bytes__int_value_value_error(self, int_value):
        with pytest.raises(ValueError):
            int_to_bytes(int_value=int_value)

    @pytest.mark.parametrize("int_value", [0, 100])
    @pytest.mark.parametrize("size", [-99, -1])
    def test_int_to_bytes__size_value_error(self, int_value, size):
        with pytest.raises(ValueError):
            int_to_bytes(int_value=int_value, size=size)

    @pytest.mark.parametrize("endianness, int_value, size", [
        (Endianness.LITTLE_ENDIAN, 1, 0),
        (Endianness.BIG_ENDIAN, 0xF0E1, 1),
        (Endianness.LITTLE_ENDIAN, 0xE1F0, 1),
        (Endianness.BIG_ENDIAN, 0x987654321F, 4),
    ])
    def test_int_to_bytes__size_too_small(self, int_value, endianness, size):
        with pytest.raises(InconsistencyError):
            int_to_bytes(int_value=int_value, endianness=endianness, size=size)

    @pytest.mark.parametrize("expected_output, endianness, int_value", [
        (bytes([0]), Endianness.BIG_ENDIAN, 0),
        (bytes([0]), Endianness.LITTLE_ENDIAN, 0),
        (bytes([0xF0]), Endianness.BIG_ENDIAN, 0xF0),
        (bytes([0xF0]), Endianness.LITTLE_ENDIAN, 0xF0),
        (bytes([0xF0, 0xE1]), Endianness.BIG_ENDIAN, 0xF0E1),
        (bytes([0xF0, 0xE1]), Endianness.LITTLE_ENDIAN, 0xE1F0),
        (bytes([0x98, 0x76, 0x54, 0x32, 0x1F]), Endianness.BIG_ENDIAN, 0x987654321F),
        (bytes([0x98, 0x76, 0x54, 0x32, 0x1F]), Endianness.LITTLE_ENDIAN, 0x1F32547698),
    ])
    def test_int_to_bytes(self, int_value, endianness, expected_output):
        self.mock_validate_endianness.return_value = endianness
        assert int_to_bytes(int_value=int_value, endianness=endianness) == expected_output
        self.mock_validate_endianness.assert_called_once_with(endianness)

    @pytest.mark.parametrize("expected_output, endianness, int_value, size", [
        (bytes(), Endianness.LITTLE_ENDIAN, 0, 0),
        (bytes([0]), Endianness.BIG_ENDIAN, 0, 1),
        (bytes([0, 0]), Endianness.LITTLE_ENDIAN, 0, 2),
        (bytes([0, 0, 0xF0]), Endianness.BIG_ENDIAN, 0xF0, 3),
        (bytes([0xF0, 0, 0, 0, 0]), Endianness.LITTLE_ENDIAN, 0xF0, 5),
        (bytes([0, 0xF0, 0xE1]), Endianness.BIG_ENDIAN, 0xF0E1, 3),
        (bytes([0xF0, 0xE1]), Endianness.LITTLE_ENDIAN, 0xE1F0, 2),
        (bytes([0, 0x98, 0x76, 0x54, 0x32, 0x1F]), Endianness.BIG_ENDIAN, 0x987654321F, 6),
        (bytes([0x98, 0x76, 0x54, 0x32, 0x1F, 0]), Endianness.LITTLE_ENDIAN, 0x1F32547698, 6),
    ])
    def test_int_to_bytes__with_size(self, int_value, endianness, size, expected_output):
        self.mock_validate_endianness.return_value = endianness
        assert int_to_bytes(int_value=int_value, endianness=endianness, size=size) == expected_output
        self.mock_validate_endianness.assert_called_once_with(endianness)

    # obd_dtc_to_int

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_obd_dtc_to_int__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            obd_dtc_to_int(value)
        mock_isinstance.assert_called_once_with(value, str)

    @pytest.mark.parametrize("value", ["P0FFF00", "A0123-00", "0x123456", "U012-300"])
    def test_obd_dtc_to_int__value_error(self, value):
        with pytest.raises(ValueError):
            obd_dtc_to_int(value)

    @pytest.mark.parametrize("obd_dtc, uds_dtc", [
        ("p0000-00", 0x000000),
        ("C1FED-CB", 0x5FEDCB),
        ("b3F4E-5D", 0xBF4E5D),
        ("U3FFF-FF", 0xFFFFFF),
    ])
    def test_obd_dtc_to_int__valid(self, obd_dtc, uds_dtc):
        assert obd_dtc_to_int(obd_dtc) == uds_dtc

    # int_to_obd_dtc

    @pytest.mark.parametrize("value", [Mock(), "Some Value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_int_to_obd_dtc__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            int_to_obd_dtc(value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [MIN_DTC_VALUE - 1, MAX_DTC_VALUE + 1])
    def test_int_to_obd_dtc__value_error(self, value):
        with pytest.raises(ValueError):
            int_to_obd_dtc(value)

    @pytest.mark.parametrize("obd_dtc, uds_dtc", [
        ("P0000-00", 0x000000),
        ("C1FED-CB", 0x5FEDCB),
        ("B0123-45", 0x812345),
        ("U3FFF-FF", 0xFFFFFF),
    ])
    def test_int_to_obd_dtc__valid(self, obd_dtc, uds_dtc):
        assert int_to_obd_dtc(uds_dtc) == obd_dtc

    # get_signed_value_decoding_formula

    @pytest.mark.parametrize("bit_length", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_decode_signed_value_formula__type_error(self, mock_isinstance, bit_length):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            get_signed_value_decoding_formula(bit_length)
        mock_isinstance.assert_called_once_with(bit_length, int)

    @pytest.mark.parametrize("bit_length", [1, -5])
    def test_get_decode_signed_value_formula__value_error(self, bit_length):
        with pytest.raises(ValueError):
            get_signed_value_decoding_formula(bit_length)

    @pytest.mark.parametrize("bit_length, value_out_of_range", [
        (4, -1),
        (12, 4096),
    ])
    def test_get_decode_signed_value_formula__formula_value_error(self, bit_length, value_out_of_range):
        formula = get_signed_value_decoding_formula(bit_length)
        with pytest.raises(ValueError):
            formula(value_out_of_range)

    @pytest.mark.parametrize("bit_length, encoding_mapping", [
        (4, {0x0: 0, 0x7: 7, 0x8: -8, 0xF: -1}),
        (12, {0x000: 0, 0x7FF: 2047, 0x800: -2048, 0xFFF: -1}),
    ])
    def test_get_decode_signed_value_formula(self, bit_length, encoding_mapping):
        formula = get_signed_value_decoding_formula(bit_length)
        assert all(formula(unsigned_value) == signed_value
                   for unsigned_value, signed_value in encoding_mapping.items())

    # get_signed_value_encoding_formula

    @pytest.mark.parametrize("bit_length", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_encode_signed_value_formula__type_error(self, mock_isinstance, bit_length):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            get_signed_value_encoding_formula(bit_length)
        mock_isinstance.assert_called_once_with(bit_length, int)

    @pytest.mark.parametrize("bit_length", [1, -5])
    def test_get_encode_signed_value_formula__value_error(self, bit_length):
        with pytest.raises(ValueError):
            get_signed_value_encoding_formula(bit_length)

    @pytest.mark.parametrize("bit_length, value_out_of_range", [
        (4, -9),
        (12, 2048),
    ])
    def test_get_encode_signed_value_formula__formula_value_error(self, bit_length, value_out_of_range):
        formula = get_signed_value_encoding_formula(bit_length)
        with pytest.raises(ValueError):
            formula(value_out_of_range)

    @pytest.mark.parametrize("bit_length, encoding_mapping", [
        (4, {0x0: 0, 0x7: 7, 0x8: -8, 0xF: -1}),
        (12, {0x000: 0, 0x7FF: 2047, 0x800: -2048, 0xFFF: -1}),
    ])
    def test_get_encode_signed_value_formula(self, bit_length, encoding_mapping):
        formula = get_signed_value_encoding_formula(bit_length)
        assert all(formula(signed_value) == unsigned_value
                   for unsigned_value, signed_value in encoding_mapping.items())


class TestTimeSync:
    """Unit tests for `TimeSync` class."""

    def setup_method(self):
        self.mock_time_sync = Mock(spec=TimeSync,
                                   samples_number=Mock(),
                                   sync_expiration=Mock(),
                                   _TimeSync__last_sync_timestamp=Mock(),
                                   _TimeSync__offset=Mock())
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_time = patch(f"{SCRIPT_LOCATION}.time")
        self.mock_time = self._patcher_time.start()

    def teardown_method(self):
        self._patcher_perf_counter.stop()
        self._patcher_time.stop()

    # __init__

    @patch(f"{SCRIPT_LOCATION}.hasattr")
    def test_init__initial(self, mock_hasattr):
        mock_hasattr.return_value = False
        assert TimeSync.__init__(self.mock_time_sync) is None
        assert self.mock_time_sync.samples_number == self.mock_time_sync.DEFAULT_SAMPLES_NUMBER
        assert self.mock_time_sync.sync_expiration == self.mock_time_sync.DEFAULT_SYNC_EXPIRATION
        assert self.mock_time_sync._TimeSync__last_sync_timestamp is None
        assert self.mock_time_sync._TimeSync__offset is None

    @patch(f"{SCRIPT_LOCATION}.hasattr")
    def test_init__following(self, mock_hasattr):
        mock_hasattr.return_value = True
        assert TimeSync.__init__(self.mock_time_sync) is None
        assert self.mock_time_sync.samples_number != self.mock_time_sync.DEFAULT_SAMPLES_NUMBER
        assert self.mock_time_sync.sync_expiration != self.mock_time_sync.DEFAULT_SYNC_EXPIRATION
        assert self.mock_time_sync._TimeSync__last_sync_timestamp is not None
        assert self.mock_time_sync._TimeSync__offset is not None

    @pytest.mark.parametrize("initial, samples_number, sync_expiration", [
        (True, 1, 10),
        (False, 15, 3.69),
    ])
    @patch(f"{SCRIPT_LOCATION}.hasattr")
    def test_init__update(self, mock_hasattr, initial, samples_number, sync_expiration):
        mock_hasattr.return_value = not initial
        assert TimeSync.__init__(self.mock_time_sync,
                                 samples_number=samples_number,
                                 sync_expiration=sync_expiration) is None
        assert self.mock_time_sync.samples_number == samples_number
        assert self.mock_time_sync.sync_expiration == sync_expiration

    # __new__

    def test_new__no_instance(self):
        TimeSync._instance = None
        instance = TimeSync.__new__(TimeSync)
        assert TimeSync._instance is instance
        assert isinstance(instance, TimeSync)

    def test_new__instance_exists(self):
        mock_instance = Mock(spec=TimeSync)
        TimeSync._instance = mock_instance
        assert TimeSync.__new__(TimeSync) is mock_instance
        assert TimeSync._instance is mock_instance

    # samples_number

    def test_samples_number__get(self):
        self.mock_time_sync._TimeSync__samples_number = Mock()
        assert TimeSync.samples_number.fget(self.mock_time_sync) == self.mock_time_sync._TimeSync__samples_number

    @pytest.mark.parametrize("value", [Mock(), None])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_samples_number__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TimeSync.samples_number.fset(self.mock_time_sync, value)
        mock_isinstance.assert_called_once_with(value, int)

    @pytest.mark.parametrize("value", [0, -5])
    def test_samples_number__set__value_error(self, value):
        with pytest.raises(ValueError):
            TimeSync.samples_number.fset(self.mock_time_sync, value)

    @pytest.mark.parametrize("value", [1, 12])
    def test_samples_number__set__valid(self, value):
        assert TimeSync.samples_number.fset(self.mock_time_sync, value) is None
        assert self.mock_time_sync._TimeSync__samples_number == value
        
    # sync_expiration

    def test_sync_expiration__get(self):
        self.mock_time_sync._TimeSync__sync_expiration = Mock()
        assert TimeSync.sync_expiration.fget(self.mock_time_sync) == self.mock_time_sync._TimeSync__sync_expiration

    @pytest.mark.parametrize("value", [Mock(), None])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_sync_expiration__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TimeSync.sync_expiration.fset(self.mock_time_sync, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [0, -0.1])
    def test_sync_expiration__set__value_error(self, value):
        with pytest.raises(ValueError):
            TimeSync.sync_expiration.fset(self.mock_time_sync, value)

    @pytest.mark.parametrize("value", [0.0001, 1])
    def test_sync_expiration__set__valid(self, value):
        assert TimeSync.sync_expiration.fset(self.mock_time_sync, value) is None
        assert self.mock_time_sync._TimeSync__sync_expiration == value

    # last_sync_timestamp

    def test_last_sync_timestamp__get(self):
        self.mock_time_sync._TimeSync__last_sync_timestamp = Mock()
        assert (TimeSync.last_sync_timestamp.fget(self.mock_time_sync)
                == self.mock_time_sync._TimeSync__last_sync_timestamp)

    # is_sync_outdated

    def test_is_sync_outdated__get__never_synced(self):
        self.mock_time_sync.last_sync_timestamp = None
        assert TimeSync.is_sync_outdated.fget(self.mock_time_sync) is True

    def test_is_sync_outdated__get__true(self):
        self.mock_time_sync.last_sync_timestamp = Mock()
        mock_is_outdated = Mock(return_value=True)
        mock_sub = Mock(side_effect=lambda other: self.mock_perf_counter.return_value)
        self.mock_perf_counter.return_value = MagicMock(__gt__=mock_is_outdated,
                                                        __sub__=mock_sub)
        assert TimeSync.is_sync_outdated.fget(self.mock_time_sync) is True
        mock_is_outdated.assert_called_once_with(self.mock_time_sync.sync_expiration)
        mock_sub.assert_called_once_with(self.mock_time_sync.last_sync_timestamp)

    def test_is_sync_outdated__get__false(self):
        self.mock_time_sync.last_sync_timestamp = Mock()
        mock_is_outdated = Mock(return_value=False)
        mock_sub = Mock(side_effect=lambda other: self.mock_perf_counter.return_value)
        self.mock_perf_counter.return_value = MagicMock(__gt__=mock_is_outdated,
                                                        __sub__=mock_sub)
        assert TimeSync.is_sync_outdated.fget(self.mock_time_sync) is False
        mock_is_outdated.assert_called_once_with(self.mock_time_sync.sync_expiration)
        mock_sub.assert_called_once_with(self.mock_time_sync.last_sync_timestamp)

    # offset

    def test_offset__get(self):
        self.mock_time_sync._TimeSync__offset = Mock()
        assert TimeSync.offset.fget(self.mock_time_sync) == self.mock_time_sync._TimeSync__offset

    # sync

    def test_sync(self):
        self.mock_time_sync.samples_number = 3
        mock_time_sub = Mock(side_effect=lambda other: self.mock_time.return_value)
        self.mock_time.return_value = MagicMock(__sub__=mock_time_sub)
        mock_perf_counter_sub = Mock(side_effect=lambda other: self.mock_perf_counter.return_value)
        mock_perf_counter_lt = Mock(return_value=True)
        self.mock_perf_counter.return_value = MagicMock(__sub__=mock_perf_counter_sub,
                                                        __lt__=mock_perf_counter_lt)
        assert TimeSync.sync(self.mock_time_sync) is self.mock_time_sync.offset
        assert self.mock_time_sync._TimeSync__last_sync_timestamp == self.mock_perf_counter.return_value
        assert mock_perf_counter_lt.call_count == self.mock_time_sync.samples_number

    # time_to_perf_counter

    @pytest.mark.parametrize("is_sync_outdated, time_value, offset", [
        (True, 123.456, 789.012),
        (False, 81, -5),
    ])
    def test_time_to_perf_counter(self, is_sync_outdated, time_value, offset):
        self.mock_time_sync.is_sync_outdated = is_sync_outdated
        self.mock_time_sync.offset = offset
        assert TimeSync.time_to_perf_counter(self.mock_time_sync, time_value=time_value) == time_value - offset
        self.mock_time.sync.call_count == int(is_sync_outdated)

    @pytest.mark.parametrize("is_sync_outdated, time_value, min_value, offset", [
        (True, 123.456, 0, 789.012),
        (False, 81, 86.001, -5),
    ])
    def test_time_to_perf_counter__min_value(self, is_sync_outdated, time_value, min_value, offset):
        self.mock_time_sync.is_sync_outdated = is_sync_outdated
        self.mock_time_sync.offset = offset
        assert (TimeSync.time_to_perf_counter(self.mock_time_sync, time_value=time_value, min_value=min_value)
                == min_value)
        self.mock_time.sync.call_count == int(is_sync_outdated)

    @pytest.mark.parametrize("is_sync_outdated, time_value, max_value, offset", [
        (True, 789.012, 654.321, 123.456),
        (False, 81, 85.999, -5),
    ])
    def test_time_to_perf_counter__max_value(self, is_sync_outdated, time_value, max_value, offset):
        self.mock_time_sync.is_sync_outdated = is_sync_outdated
        self.mock_time_sync.offset = offset
        assert (TimeSync.time_to_perf_counter(self.mock_time_sync, time_value=time_value, max_value=max_value)
                == max_value)
        self.mock_time.sync.call_count == int(is_sync_outdated)

    # perf_counter_to_time

    @pytest.mark.parametrize("is_sync_outdated, perf_counter_value, offset", [
        (True, 123.456, 789.012),
        (False, 81, -5),
    ])
    def test_perf_counter_to_time(self, is_sync_outdated, perf_counter_value, offset):
        self.mock_time_sync.is_sync_outdated = is_sync_outdated
        self.mock_time_sync.offset = offset
        assert (TimeSync.perf_counter_to_time(self.mock_time_sync,
                                              perf_counter_value=perf_counter_value) == perf_counter_value + offset)
        self.mock_time.sync.call_count == int(is_sync_outdated)

    @pytest.mark.parametrize("is_sync_outdated, perf_counter_value, min_value, offset", [
        (True, 123.456, 1000, 789.012),
        (False, 81, 76.001, -5),
    ])
    def test_perf_counter_to_time__min_value(self, is_sync_outdated, perf_counter_value, min_value, offset):
        self.mock_time_sync.is_sync_outdated = is_sync_outdated
        self.mock_time_sync.offset = offset
        assert (TimeSync.perf_counter_to_time(self.mock_time_sync,
                                              perf_counter_value=perf_counter_value,
                                              min_value=min_value) == min_value)
        self.mock_time.sync.call_count == int(is_sync_outdated)

    @pytest.mark.parametrize("is_sync_outdated, perf_counter_value, max_value, offset", [
        (True, 789.012, 854.321, 123.456),
        (False, 81, 75.999, -5),
    ])
    def test_perf_counter_to_time__max_value(self, is_sync_outdated, perf_counter_value, max_value, offset):
        self.mock_time_sync.is_sync_outdated = is_sync_outdated
        self.mock_time_sync.offset = offset
        assert (TimeSync.perf_counter_to_time(self.mock_time_sync,
                                              perf_counter_value=perf_counter_value,
                                              max_value=max_value) == max_value)
        self.mock_time.sync.call_count == int(is_sync_outdated)


@pytest.mark.integration
class TestFunctionsIntegration:
    """Integration tests for functions."""

    @pytest.mark.parametrize("int_value", [0, 0x43, 0xFF, 0x0123456789ABCDEF, 0x7B0000440000])
    @pytest.mark.parametrize("size", [None, 10, 16])
    @pytest.mark.parametrize("endianness", list(Endianness))
    def test_int_to_bytes_to_int(self, int_value, endianness, size):
        bytes_list = int_to_bytes(int_value, size=size, endianness=endianness)
        assert bytes_to_int(bytes_list, endianness=endianness) == int_value


@pytest.mark.integration
class TestTimeSyncIntegration:
    """Integration tests for `TimeSync` class."""

    ACCURACY = 0.00001

    def test_time_to_perf_counter(self):
        ts = TimeSync()
        ts.sync()
        perf_now = perf_counter()
        time_now = time()
        converted_perf = ts.time_to_perf_counter(time_value=time_now)
        assert perf_now - self.ACCURACY <= converted_perf <= perf_now + self.ACCURACY

    def test_perf_counter_to_time(self):
        ts = TimeSync()
        ts.sync()
        perf_now = perf_counter()
        time_now = time()
        converted_time = ts.perf_counter_to_time(perf_counter_value=perf_now)
        assert time_now - self.ACCURACY <= converted_time <= time_now + self.ACCURACY

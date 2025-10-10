import pytest
from mock import Mock, patch

from uds.utilities.conversions import (
    MAX_DTC_VALUE,
    MIN_DTC_VALUE,
    Endianness,
    InconsistencyError,
    bytes_to_hex,
    bytes_to_int,
    int_to_bytes,
    int_to_obd_dtc,
    obd_dtc_to_int,
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
        ([0xF0], Endianness.BIG_ENDIAN, 0xF0),
        ([0xF0], Endianness.LITTLE_ENDIAN, 0xF0),
        ((0xF0, 0xE1), Endianness.BIG_ENDIAN, 0xF0E1),
        (bytearray([0xF0, 0xE1]), Endianness.LITTLE_ENDIAN, 0xE1F0),
        ([0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.BIG_ENDIAN, 0x987654321F),
        (bytes([0x98, 0x76, 0x54, 0x32, 0x1F]), Endianness.LITTLE_ENDIAN, 0x1F32547698),
    ])
    def test_bytes_to_int(self, bytes_list, endianness, expected_output):
        self.mock_validate_endianness.side_effect = lambda arg: arg
        assert bytes_to_int(bytes_list=bytes_list, endianness=endianness) == expected_output
        self.mock_validate_raw_bytes.assert_called_once_with(bytes_list)
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
    def test_obd_dtc_to_int__value_error(self, value):
        with pytest.raises(ValueError):
            int_to_obd_dtc(value)

    @pytest.mark.parametrize("obd_dtc, uds_dtc", [
        ("P0000-00", 0x000000),
        ("C1FED-CB", 0x5FEDCB),
        ("B0123-45", 0x812345),
        ("U3FFF-FF", 0xFFFFFF),
    ])
    def test_obd_dtc_to_int__valid(self, obd_dtc, uds_dtc):
        assert int_to_obd_dtc(uds_dtc) == obd_dtc


@pytest.mark.integration
class TestIntegration:
    """Integration tests for functions."""

    @pytest.mark.parametrize("int_value", [0, 0x43, 0xFF, 0x0123456789ABCDEF, 0x7B0000440000])
    @pytest.mark.parametrize("size", [None, 10, 16])
    @pytest.mark.parametrize("endianness", list(Endianness))
    def test_int_to_bytes_to_int(self, int_value, endianness, size):
        bytes_list = int_to_bytes(int_value, size=size, endianness=endianness)
        assert bytes_to_int(bytes_list, endianness=endianness) == int_value

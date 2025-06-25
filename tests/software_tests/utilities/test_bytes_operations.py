import pytest
from mock import patch

from uds.utilities import ValidatedEnum
from uds.utilities.bytes_operations import Endianness, InconsistentArgumentsError, bytes_to_int, int_to_bytes

SCRIPT_LOCATION = "uds.utilities.bytes_operations"


class TestEndianness:
    """Unit tests for `Endianness` class."""

    def test_inheritance_validated_enum(self):
        assert issubclass(Endianness, ValidatedEnum)


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
        (Endianness.BIG_ENDIAN, 0xF0E1, 1),
        (Endianness.LITTLE_ENDIAN, 0xE1F0, 1),
        (Endianness.BIG_ENDIAN, 0x987654321F, 4),
        (Endianness.LITTLE_ENDIAN, 0x1F32547698, 2),
    ])
    def test_int_to_bytes__size_too_small(self, int_value, endianness, size):
        with pytest.raises(InconsistentArgumentsError):
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


@pytest.mark.integration
class TestIntegration:
    """Integration tests for functions."""

    @pytest.mark.parametrize("int_value", [0, 0x43, 0xFF, 0x0123456789ABCDEF, 0x7B0000440000])
    @pytest.mark.parametrize("size", [None, 10, 16])
    @pytest.mark.parametrize("endianness", list(Endianness))
    def test_int_to_bytes_to_int(self, int_value, endianness, size):
        bytes_list = int_to_bytes(int_value, size=size, endianness=endianness)
        assert bytes_to_int(bytes_list, endianness=endianness) == int_value

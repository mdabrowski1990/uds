import pytest
from mock import patch

from uds.utilities import ValidatedEnum
from uds.utilities.bytes_operations import Endianness, bytes_list_to_int, int_to_bytes_list, \
    InconsistentArgumentsError


class TestEndianness:
    """Unit tests for `Endianness` class."""

    def test_inheritance_validated_enum(self):
        assert issubclass(Endianness, ValidatedEnum)


class TestFunctions:
    """Unit tests for module functions."""

    SCRIPT_LOCATION = "uds.utilities.bytes_operations"

    def setup(self):
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_validate_endianness = patch(f"{self.SCRIPT_LOCATION}.Endianness.validate_member")
        self.mock_validate_endianness = self._patcher_validate_endianness.start()

    def teardown(self):
        self._patcher_validate_raw_bytes.stop()
        self._patcher_validate_endianness.stop()

    # bytes_list_to_int

    @pytest.mark.parametrize("bytes_list, endianness, expected_output", [
        ([0xF0], Endianness.BIG_ENDIAN, 0xF0),
        ([0xF0], Endianness.LITTLE_ENDIAN, 0xF0),
        ([0xF0, 0xE1], Endianness.BIG_ENDIAN, 0xF0E1),
        ([0xF0, 0xE1], Endianness.LITTLE_ENDIAN, 0xE1F0),
        ([0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.BIG_ENDIAN, 0x987654321F),
        ([0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.LITTLE_ENDIAN, 0x1F32547698),
    ])
    def test_bytes_list_to_int(self, bytes_list, endianness, expected_output):
        assert bytes_list_to_int(bytes_list=bytes_list, endianness=endianness) == expected_output
        self.mock_validate_raw_bytes.assert_called_once_with(bytes_list)
        self.mock_validate_endianness.assert_called_once_with(endianness)

    # int_to_bytes_list

    @pytest.mark.parametrize("int_value", [None, 5., "not an integer value"])
    def test_int_to_bytes_list__int_value_type_error(self, int_value):
        with pytest.raises(TypeError):
            int_to_bytes_list(int_value=int_value)

    @pytest.mark.parametrize("int_value", [0, 100])
    @pytest.mark.parametrize("list_size", [5., "not an integer value"])
    def test_int_to_bytes_list__list_size_type_error(self, int_value, list_size):
        with pytest.raises(TypeError):
            int_to_bytes_list(int_value=int_value, list_size=list_size)

    @pytest.mark.parametrize("int_value", [-99, -1])
    def test_int_to_bytes_list__int_value_value_error(self, int_value):
        with pytest.raises(ValueError):
            int_to_bytes_list(int_value=int_value)

    @pytest.mark.parametrize("int_value", [0, 100])
    @pytest.mark.parametrize("list_size", [-99, -1])
    def test_int_to_bytes_list__list_size_value_error(self, int_value, list_size):
        with pytest.raises(ValueError):
            int_to_bytes_list(int_value=int_value, list_size=list_size)

    @pytest.mark.parametrize("endianness", [None, "some unknown endianness"])
    @pytest.mark.parametrize("int_value", [0, 0xF0E1])
    def test_int_to_bytes_list__unknown_endianness(self, int_value, endianness):
        with pytest.raises(NotImplementedError):
            int_to_bytes_list(int_value=int_value, endianness=endianness)

    @pytest.mark.parametrize("endianness, int_value, list_size", [
        (Endianness.BIG_ENDIAN, 0xF0E1, 1),
        (Endianness.LITTLE_ENDIAN, 0xE1F0, 1),
        (Endianness.BIG_ENDIAN, 0x987654321F, 4),
        (Endianness.LITTLE_ENDIAN, 0x1F32547698, 2),
    ])
    def test_int_to_bytes_list__list_size_too_small(self, int_value, endianness, list_size):
        with pytest.raises(InconsistentArgumentsError):
            int_to_bytes_list(int_value=int_value, endianness=endianness, list_size=list_size)

    @pytest.mark.parametrize("expected_output, endianness, int_value", [
        ([0], Endianness.BIG_ENDIAN, 0),
        ([0], Endianness.LITTLE_ENDIAN, 0),
        ([0xF0], Endianness.BIG_ENDIAN, 0xF0),
        ([0xF0], Endianness.LITTLE_ENDIAN, 0xF0),
        ([0xF0, 0xE1], Endianness.BIG_ENDIAN, 0xF0E1),
        ([0xF0, 0xE1], Endianness.LITTLE_ENDIAN, 0xE1F0),
        ([0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.BIG_ENDIAN, 0x987654321F),
        ([0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.LITTLE_ENDIAN, 0x1F32547698),
    ])
    def test_int_to_bytes_list(self, int_value, endianness, expected_output):
        assert int_to_bytes_list(int_value=int_value, endianness=endianness) == expected_output
        self.mock_validate_endianness.assert_called_once_with(endianness)

    @pytest.mark.parametrize("expected_output, endianness, int_value, list_size", [
        ([0], Endianness.BIG_ENDIAN, 0, 1),
        ([0, 0], Endianness.LITTLE_ENDIAN, 0, 2),
        ([0, 0, 0xF0], Endianness.BIG_ENDIAN, 0xF0, 3),
        ([0xF0, 0, 0, 0, 0], Endianness.LITTLE_ENDIAN, 0xF0, 5),
        ([0, 0xF0, 0xE1], Endianness.BIG_ENDIAN, 0xF0E1, 3),
        ([0xF0, 0xE1], Endianness.LITTLE_ENDIAN, 0xE1F0, 2),
        ([0, 0x98, 0x76, 0x54, 0x32, 0x1F], Endianness.BIG_ENDIAN, 0x987654321F, 6),
        ([0x98, 0x76, 0x54, 0x32, 0x1F, 0], Endianness.LITTLE_ENDIAN, 0x1F32547698, 6),
    ])
    def test_int_to_bytes_list__with_list_size(self, int_value, endianness, list_size, expected_output):
        assert int_to_bytes_list(int_value=int_value, endianness=endianness, list_size=list_size) == expected_output
        self.mock_validate_endianness.assert_called_once_with(endianness)


@pytest.mark.integration
class TestIntegration:
    """Integration tests for functions."""

    @pytest.mark.parametrize("int_value", [0, 0x43, 0xFF, 0x0123456789ABCDEF, 0x7B0000440000])
    @pytest.mark.parametrize("list_size", [None, 10, 16])
    @pytest.mark.parametrize("endianness", list(Endianness))
    def test_int_to_bytes_list_to_int(self, int_value, endianness, list_size):
        bytes_list = int_to_bytes_list(int_value, list_size=list_size, endianness=endianness)
        assert bytes_list_to_int(bytes_list, endianness=endianness) == int_value

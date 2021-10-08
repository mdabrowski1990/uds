import pytest

from uds.utilities.common_types import validate_raw_bytes, validate_raw_byte


class TestFunctions:
    """Test of all functions in this scope."""

    # validate_raw_byte

    @pytest.mark.parametrize("value", [0x00, 0x01, 0x12, 0xAA, 0xFE, 0xFF])
    def test_validate_raw_byte__valid(self, value):
        assert validate_raw_byte(value=value) is None

    @pytest.mark.parametrize("value", [None, float("inf"), 0.0, "5"])
    def test_validate_raw_byte__invalid_type(self, value):
        with pytest.raises(TypeError):
            validate_raw_byte(value=value)

    @pytest.mark.parametrize("value", [-3298761, -1, 0x100, 99999])
    def test_validate_raw_byte__invalid_value(self, value):
        with pytest.raises(ValueError):
            validate_raw_byte(value=value)

    # validate_raw_bytes

    def test_validate_raw_bytes__valid(self, example_raw_bytes):
        assert validate_raw_bytes(value=example_raw_bytes) is None

    @pytest.mark.parametrize("invalid_raw_bytes", [None, "abc", {1, 2, 3}, 5, 76.5, False])
    def test_validate_raw_bytes__invalid_type(self, invalid_raw_bytes):
        with pytest.raises(TypeError):
            validate_raw_bytes(value=invalid_raw_bytes)

    @pytest.mark.parametrize("invalid_raw_bytes", [tuple(), [], [-1], (0x100,), [1, 0.2], [22, "1"], (None, 0)])
    def test_validate_raw_bytes__invalid_value(self, invalid_raw_bytes):
        with pytest.raises(ValueError):
            validate_raw_bytes(value=invalid_raw_bytes)

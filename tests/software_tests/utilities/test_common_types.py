import pytest

from uds.utilities.common_types import validate_raw_bytes


class TestFunctions:
    """Test of all functions in this scope."""

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

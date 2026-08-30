from unittest.mock import Mock, patch

import pytest

from uds.utilities.helpers import validate_time, validate_timeout

SCRIPT_LOCATION = "uds.utilities.helpers"


class TestFunctions:
    """Unit tests for module functions."""

    # validate_time

    @pytest.mark.parametrize("value", [None, 0, Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_time__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            validate_time(value)
        mock_isinstance.assert_called_once_with(value, (int, float))


    @pytest.mark.parametrize("value", [-0.231, -0.00001])
    def test_validate_time__value_error(self, value):
        with pytest.raises(ValueError):
            validate_time(value)

    def test_validate_time__value_error__zero(self):
        with pytest.raises(ValueError):
            assert validate_time(0, accept_zero=False)

    @pytest.mark.parametrize("value", [0.1, 543])
    def test_validate_time__valid(self, value):
        assert validate_time(value) is None

    def test_validate_time__valid__accept_zero(self):
        assert validate_time(0, accept_zero=True) is None

    # validate_timeout

    @pytest.mark.parametrize("value", ["some value", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_timeout__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            validate_timeout(value)
        mock_isinstance.assert_called_once_with(value, (int, float))


    @pytest.mark.parametrize("value", [0, -0.231])
    def test_validate_timeout__value_error(self, value):
        with pytest.raises(ValueError):
            validate_timeout(value)


    @pytest.mark.parametrize("value", [None, 0.1, 543])
    def test_validate_timeout__valid(self, value):
        assert validate_timeout(value) is None

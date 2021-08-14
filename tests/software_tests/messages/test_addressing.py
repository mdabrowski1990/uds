import pytest
from mock import patch, Mock
from enum import Enum, IntEnum

from uds.messages.addressing import AddressingType


class TestAddressingType:

    SCRIPT_LOCATION = "uds.messages.addressing"

    def test_is_addressing_type__true(self, example_addressing_type):
        assert AddressingType.is_addressing_type(value=example_addressing_type) is True

    @pytest.mark.parametrize("not_addressing_type", [None, 0.1, Mock(spec=Enum), Mock(spec=IntEnum),
                                                     AddressingType.PHYSICAL.value])
    def test_is_addressing_type__false(self, not_addressing_type):
        assert AddressingType.is_addressing_type(value=not_addressing_type) is False

    @patch(f"{SCRIPT_LOCATION}.AddressingType.is_addressing_type")
    @pytest.mark.parametrize("value_to_check", [None, AddressingType.PHYSICAL, "something"])
    def test_validate_addressing_type__valid(self, mock_is_addressing_type, value_to_check):
        mock_is_addressing_type.return_value = True
        assert AddressingType.validate_addressing_type(value=value_to_check) is None
        mock_is_addressing_type.assert_called_once_with(value=value_to_check)

    @patch(f"{SCRIPT_LOCATION}.AddressingType.is_addressing_type")
    @pytest.mark.parametrize("value_to_check", [None, AddressingType.PHYSICAL, "something"])
    def test_validate_addressing_type__invalid(self, mock_is_addressing_type, value_to_check):
        mock_is_addressing_type.return_value = False
        with pytest.raises(TypeError):
            AddressingType.validate_addressing_type(value=value_to_check)
        mock_is_addressing_type.assert_called_once_with(value=value_to_check)
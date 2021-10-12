import pytest

from mock import patch

from uds.packet.can_flow_control import CanSTminTranslator, CanFlowStatus
from uds.utilities import ValidatedEnum, NibbleEnum


class TestCanFlowStatus:
    """Tests for 'CanFlowStatus' class."""

    def test_inheritance__validated_enum(self):
        assert issubclass(CanFlowStatus, ValidatedEnum)

    def test_inheritance__nibble_enum(self):
        assert issubclass(CanFlowStatus, NibbleEnum)


class TestCanSTmin:
    """Tests for 'CanSTmin' class."""

    SCRIPT_LOCATION = "uds.packet.can_flow_control"

    def setup(self):
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_warn.stop()

    # _is_ms_value

    @pytest.mark.parametrize("value", [0, 0., 1, 30, 59, 65., 99, 101, 126, 127, 127.])
    def test_is_ms_value__true(self, value):
        assert CanSTminTranslator._is_ms_value(value) is True

    @pytest.mark.parametrize("value", [-1, 128, 1.1, 6.0001, 99.9999])
    def test_is_ms_value__false(self, value):
        assert CanSTminTranslator._is_ms_value(value) is False

    # _is_100us_value

    @pytest.mark.parametrize("value", [0.1*v for v in range(1, 10)])
    def test_is_100us_value__true(self, value):
        assert CanSTminTranslator._is_100us_value(value) is True

    @pytest.mark.parametrize("value", [0, 0.0, 0.10001, 0.75, 0.89999, 1])
    def test_is_100us_value__false(self, value):
        assert CanSTminTranslator._is_100us_value(value) is False

    # encode

    @pytest.mark.parametrize("raw_value, time_value", [
        (0x00, 0),
        (0x01, 1),
        (0x7E, 126),
        (0x7F, 127),
        (0xF1, 0.1),
        (0xF2, 0.2),
        (0xF8, 0.8),
        (0xF9, 0.9),
    ])
    def test_encode__valid(self, raw_value, time_value):
        assert CanSTminTranslator.encode(raw_value) == time_value
        self.mock_validate_raw_byte.assert_called_once_with(raw_value)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("raw_value", [0x80, 0x95, 0xA1, 0xBA, 0xC0, 0xD7, 0xE3, 0xF0, 0xFA, 0xFE, 0xFF])
    def test_encode__unknown(self, raw_value):
        assert CanSTminTranslator.encode(raw_value) == CanSTminTranslator.MAX_STMIN_TIME
        self.mock_validate_raw_byte.assert_called_once_with(raw_value)
        self.mock_warn.assert_called_once()

    # decode

    @pytest.mark.parametrize("value", [None, "1 ms", [1, 1]])
    def test_decode__type_error(self, value):
        with pytest.raises(TypeError):
            CanSTminTranslator.decode(value)

    @pytest.mark.parametrize("value", [128, -1, 0.15, 0.11, 0.95])
    def test_decode__value_error(self, value):
        with pytest.raises(ValueError):
            CanSTminTranslator.decode(value)

    @pytest.mark.parametrize("raw_value, time_value", [
        (0x00, 0),
        (0x01, 1),
        (0x7E, 126),
        (0x7F, 127),
        (0xF1, 0.1),
        (0xF2, 0.2),
        (0xF8, 0.8),
        (0xF9, 0.9),
    ])
    def test_decode__valid(self, raw_value, time_value):
        assert CanSTminTranslator.decode(time_value) == raw_value
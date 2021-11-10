import pytest
from mock import patch

from uds.can.flow_control import CanSTminTranslator, CanFlowStatus, CanFlowControlHandler, \
    CanAddressingFormat
from uds.utilities import ValidatedEnum, NibbleEnum


class TestCanFlowStatus:
    """Tests for 'CanFlowStatus' class."""

    def test_inheritance__validated_enum(self):
        assert issubclass(CanFlowStatus, ValidatedEnum)

    def test_inheritance__nibble_enum(self):
        assert issubclass(CanFlowStatus, NibbleEnum)


class TestCanSTmin:
    """Tests for 'CanSTmin' class."""

    SCRIPT_LOCATION = "uds.can.flow_control"

    def setup(self):
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_warn.stop()

    # decode

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
        assert CanSTminTranslator.decode(raw_value) == time_value
        self.mock_validate_raw_byte.assert_called_once_with(raw_value)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("raw_value", [0x80, 0x95, 0xA1, 0xBA, 0xC0, 0xD7, 0xE3, 0xF0, 0xFA, 0xFE, 0xFF])
    def test_decode__unknown(self, raw_value):
        assert CanSTminTranslator.decode(raw_value) == CanSTminTranslator.MAX_STMIN_TIME
        self.mock_validate_raw_byte.assert_called_once_with(raw_value)
        self.mock_warn.assert_called_once()

    # encode

    @pytest.mark.parametrize("value", [None, "1 ms", [1, 1]])
    def test_encode__type_error(self, value):
        with pytest.raises(TypeError):
            CanSTminTranslator.encode(value)

    @pytest.mark.parametrize("value", [128, -1, 0.15, 0.11, 0.95])
    def test_encode__value_error(self, value):
        with pytest.raises(ValueError):
            CanSTminTranslator.encode(value)

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
        assert CanSTminTranslator.encode(time_value) == raw_value

    # is_time_value

    @pytest.mark.parametrize("value", [None, "1 ms", [1, 1]])
    def test_is_time_value__invalid_type(self, value):
        assert CanSTminTranslator.is_time_value(value) is False

    @pytest.mark.parametrize("value", [1, 0.1, 0.5, 999])
    @pytest.mark.parametrize("is_ms_value, is_100us_value, result", [
        (True, False, True),
        (False, True, True),
        (False, False, False),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSTminTranslator._is_ms_value")
    @patch(f"{SCRIPT_LOCATION}.CanSTminTranslator._is_100us_value")
    def test_is_time_value__result(self, mock_is_100us_value, mock_is_ms_value, is_ms_value, is_100us_value, result,
                                   value):
        mock_is_100us_value.return_value = is_100us_value
        mock_is_ms_value.return_value = is_ms_value
        assert CanSTminTranslator.is_time_value(value) is result

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


@pytest.mark.integration
class TestCanSTminIntegration:
    """Integration tests for CanSTmin class."""

    @pytest.mark.parametrize("raw_value", [0x00, 0x01, 0x12, 0x50, 0x6D, 0x7E, 0x7F, 0xF1, 0xF4, 0xF9])
    def test_decode_and_encode(self, raw_value):
        time_value = CanSTminTranslator.decode(raw_value)
        assert CanSTminTranslator.encode(time_value) == raw_value

    @pytest.mark.parametrize("time_value", [0, 1, 43, 126, 127] + [0.1*i for i in range(1, 10)])
    def test_encode_and_decode(self, time_value):
        raw_value = CanSTminTranslator.encode(time_value)
        assert CanSTminTranslator.decode(raw_value) == time_value


class TestCanFlowControlHandler:
    """Tests for `CanFlowControlHandler` class."""

    SCRIPT_LOCATION = TestCanSTmin.SCRIPT_LOCATION


class TestCanFlowControlHandlerIntegration:
    """Integration tests for `CanFlowControlHandler` class."""

    # create_valid_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "flow_status": CanFlowStatus.Overflow}, [0x32, 0xCC, 0xCC]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0x00,
          "st_min": 0xFF,
          "dlc": 0xF,
          "filler_byte": 0x9B,
          "target_address": 0xA1}, [0x30, 0x00, 0xFF] + ([0x98] * 61)),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0xFF,
          "st_min": 0x00,
          "dlc": 8,
          "filler_byte": 0x85,
          "target_address": 0xA1}, [0xA1, 0x30, 0xFF, 0x00, 0x85, 0x85, 0x85, 0x85]),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "flow_status": CanFlowStatus.Wait,
          "filler_byte": 0x39,
          "dlc": 4,
          "address_extension": 0x0B}, [0x0B, 0x31, 0x39, 0x39]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "flow_status": 1,
          "filler_byte": 0x99,
          "target_address": 0x9A,
          "address_extension": 0xFF}, [0xFF, 0x31, 0x99, 0x99]),
    ])
    def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanFlowControlHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "flow_status": CanFlowStatus.Overflow,
         "dlc": 4},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "flow_status": 4},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "flow_status": CanFlowStatus.ContinueToSend,
         "block_size": 0xFF,
         "st_min": 0x00,
         "dlc": 3,
         "target_address": 0xA1},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "flow_status": CanFlowStatus.Wait,
         "dlc": 3,
         "address_extension": 0x0B},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "flow_status": CanFlowStatus.ContinueToSend,
         "block_size": 0x100,
         "st_min": 0x100,
         "target_address": 0x9A,
         "address_extension": 0xFF}
    ])
    def test_create_valid_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanFlowControlHandler.create_valid_frame_data(**kwargs)

    # create_any_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "flow_status": CanFlowStatus.ContinueToSend,
          "dlc": 1}, [0x30]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "flow_status": 0xF,
          "dlc": 0xF,
          "filler_byte": 0x9B,
          "target_address": 0xA1}, [0x3F] + ([0x98] * 63)),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "flow_status": CanFlowStatus.Wait,
          "block_size": 0xFF,
          "st_min": 0x00,
          "dlc": 8,
          "filler_byte": 0x85,
          "target_address": 0xA1}, [0xA1, 0x31, 0xFF, 0x00, 0x85, 0x85, 0x85, 0x85]),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "flow_status": 5,
          "filler_byte": 0x39,
          "dlc": 6,
          "address_extension": 0x0B}, [0x0B, 0x35, 0x39, 0x39, 0x39, 0x39]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "flow_status": 3,
          "filler_byte": 0x99,
          "target_address": 0x9A,
          "address_extension": 0xFF}, [0xFF, 0x30, 0x99]),
    ])
    def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanFlowControlHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "flow_status": 0x10,
         "dlc": 3},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "flow_status": CanFlowStatus.Overflow,
         "dlc": 0},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "flow_status": CanFlowStatus.ContinueToSend,
         "block_size": 0xFF,
         "st_min": 0x00,
         "dlc": 3,
         "target_address": 0xA1},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "flow_status": CanFlowStatus.Wait,
         "dlc": 1,
         "address_extension": 0x0B},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "flow_status": CanFlowStatus.ContinueToSend,
         "block_size": 0x100,
         "target_address": 0x9A,
         "address_extension": 0xFF}
    ])
    def test_create_any_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanFlowControlHandler.create_any_frame_data(**kwargs)

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, [0x30, 0x12, 0x34]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x31, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xA1, 0x32, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0xBC, 0x30, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x90, 0x30, 0x17, 0xFE] + ([0xCC] * 60)),
    ])
    def test_validate_frame_data__valid(self, addressing_format, raw_frame_data):
        assert CanFlowControlHandler.validate_frame_data(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, [0x30, 0x12]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x31, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xA1, 0x32, 0xCC)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0xBC, 0x34, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x90, 0x30, 0x17, 0xFE] + ([0xCC] * 59)),
    ])
    def test_validate_frame_data__invalid(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            CanFlowControlHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)


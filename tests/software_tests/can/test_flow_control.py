import pytest
from mock import MagicMock, Mock, call, patch

from uds.can import CanAddressingFormat
from uds.can.flow_control import (
    AbstractFlowControlParametersGenerator,
    CanDlcHandler,
    CanFlowControlHandler,
    CanFlowStatus,
    CanSTminTranslator,
    DefaultFlowControlParametersGenerator,
    InconsistentArgumentsError,
)
from uds.utilities import NibbleEnum, ValidatedEnum

SCRIPT_LOCATION = "uds.can.flow_control"


class TestCanFlowStatus:
    """Unit tests for 'CanFlowStatus' class."""

    def test_inheritance__validated_enum(self):
        assert issubclass(CanFlowStatus, ValidatedEnum)

    def test_inheritance__nibble_enum(self):
        assert issubclass(CanFlowStatus, NibbleEnum)


class TestCanSTmin:
    """Unit tests for 'CanSTmin' class."""

    def setup_method(self):
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_warn.stop()

    # decode

    @pytest.mark.parametrize("raw_value, time_value", [
        (0x00, 0),
        (0x2A, 42),
        (0x7F, 127),
        (0xF1, 0.1),
        (0xF4, 0.4),
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

    @pytest.mark.parametrize("value", [None, "1 ms"])
    def test_encode__type_error(self, value):
        with pytest.raises(TypeError):
            CanSTminTranslator.encode(value)

    @pytest.mark.parametrize("value", [128, -1, 0.15])
    def test_encode__value_error(self, value):
        with pytest.raises(ValueError):
            CanSTminTranslator.encode(value)

    @pytest.mark.parametrize("raw_value, time_value", [
        (0x00, 0),
        (0x2A, 42),
        (0x7F, 127),
        (0xF1, 0.1),
        (0xF4, 0.4),
        (0xF9, 0.9),
    ])
    def test_encode__valid(self, raw_value, time_value):
        assert CanSTminTranslator.encode(time_value) == raw_value

    # is_time_value

    @pytest.mark.parametrize("value", [None, "1 ms", [1, 1]])
    def test_is_time_value__invalid_type(self, value):
        assert CanSTminTranslator.is_time_value(value) is False

    @pytest.mark.parametrize("value", [1, 0.5])
    @pytest.mark.parametrize("is_ms_value, is_100us_value", [
        (True, False),
        (False, True),
        (False, False),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSTminTranslator._is_ms_value")
    @patch(f"{SCRIPT_LOCATION}.CanSTminTranslator._is_100us_value")
    def test_is_time_value__result(self, mock_is_100us_value, mock_is_ms_value, is_ms_value, is_100us_value,
                                   value):
        mock_is_100us_value.return_value = is_100us_value
        mock_is_ms_value.return_value = is_ms_value
        assert CanSTminTranslator.is_time_value(value) is (is_ms_value or is_100us_value)

    # _is_ms_value

    @pytest.mark.parametrize("value", [0, 0., 59, 65., 127, 127.])
    def test_is_ms_value__true(self, value):
        assert CanSTminTranslator._is_ms_value(value) is True

    @pytest.mark.parametrize("value", [-1, 128, 1.1, 99.9999])
    def test_is_ms_value__false(self, value):
        assert CanSTminTranslator._is_ms_value(value) is False

    # _is_100us_value

    @pytest.mark.parametrize("value", [0.1, 0.7, 0.9])
    def test_is_100us_value__true(self, value):
        assert CanSTminTranslator._is_100us_value(value) is True

    @pytest.mark.parametrize("value", [0, 0.0, 0.10001, 1])
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
    """Unit tests for `CanFlowControlHandler` class."""

    def setup_method(self):
        self._patcher_validate_nibble = patch(f"{SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_encode_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.encode_dlc")
        self.mock_encode_dlc = self._patcher_encode_dlc.start()
        self._patcher_decode_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.decode_dlc")
        self.mock_decode_dlc = self._patcher_decode_dlc.start()
        self._patcher_get_min_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
        self.mock_get_min_dlc = self._patcher_get_min_dlc.start()
        self._patcher_encode_ai_data_bytes = \
            patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_validate_flow_status = patch(f"{SCRIPT_LOCATION}.CanFlowStatus.validate_member")
        self.mock_validate_flow_status = self._patcher_validate_flow_status.start()

    def teardown_method(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_min_dlc.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_validate_flow_status.stop()

    # create_valid_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, flow_status, block_size, st_min", [
        (CanDlcHandler.MIN_BASE_UDS_DLC, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (3, bytearray(), bytearray([0x30, 0x12, 0x56])),
        (4, bytearray([0x5A]), bytearray([0x31, 0x00, 0x00])),
        (8, bytearray([0xF0]), bytearray([0x32, 0xCC, 0xCC])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status")
    def test_create_valid_frame_data__valid_with_dlc(self, mock_encode_flow_status,
                                                     addressing_format, target_address, address_extension,
                                                     dlc, filler_byte, flow_status, block_size, st_min,
                                                     data_bytes_number, ai_data_bytes, fs_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_flow_status.return_value = fs_data_bytes
        fc_frame_data = CanFlowControlHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension,
                                                                      flow_status=flow_status,
                                                                      block_size=block_size,
                                                                      st_min=st_min,
                                                                      dlc=dlc,
                                                                      filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status,
                                                        block_size=block_size,
                                                        st_min=st_min,
                                                        filler_byte=filler_byte)
        assert isinstance(fc_frame_data, bytearray)
        assert len(fc_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, flow_status, block_size, st_min", [
        (CanDlcHandler.MIN_BASE_UDS_DLC, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (3, bytearray(), bytearray([0x30, 0x12, 0x56])),
        (4, bytearray([0x5A]), bytearray([0x31, 0x00, 0x00])),
        (8, bytearray([0xF0]), bytearray([0x32, 0xCC, 0xCC])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status")
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.get_min_dlc")
    def test_create_valid_frame_data__valid_without_dlc(self, mock_get_min_dlc, mock_encode_flow_status,
                                                        addressing_format, target_address, address_extension,
                                                        dlc, filler_byte, flow_status, block_size, st_min,
                                                        data_bytes_number, ai_data_bytes, fs_data_bytes):
        mock_get_min_dlc.return_value = dlc
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_flow_status.return_value = fs_data_bytes
        fc_frame_data = CanFlowControlHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension,
                                                                      flow_status=flow_status,
                                                                      block_size=block_size,
                                                                      st_min=st_min,
                                                                      dlc=None,
                                                                      filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        mock_get_min_dlc.assert_called_once_with(addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status,
                                                        block_size=block_size,
                                                        st_min=st_min,
                                                        filler_byte=filler_byte)
        assert isinstance(fc_frame_data, bytearray)
        assert len(fc_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (CanDlcHandler.MIN_BASE_UDS_DLC - 2, 0x66, 2, [], [0x30, 0x12, 0x56]),
        (CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0x99, 5, [0xFF], [0x31, 0x00, 0x00]),
    ])
    @pytest.mark.parametrize("flow_status, block_size, st_min", [
        (CanFlowStatus.ContinueToSend, 0x00, 0xFF),
        (2, None, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status")
    def test_create_valid_frame_data__inconsistent_args(self, mock_encode_flow_status,
                                                        addressing_format, target_address, address_extension,
                                                        dlc, filler_byte, flow_status, block_size, st_min,
                                                        data_bytes_number, ai_data_bytes, fs_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_flow_status.return_value = fs_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanFlowControlHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                          target_address=target_address,
                                                          address_extension=address_extension,
                                                          flow_status=flow_status,
                                                          block_size=block_size,
                                                          st_min=st_min,
                                                          dlc=dlc,
                                                          filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status,
                                                        block_size=block_size,
                                                        st_min=st_min,
                                                        filler_byte=filler_byte)

    # create_any_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, flow_status, block_size, st_min", [
        (CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (3, bytearray(), bytearray([0x30, 0x12, 0x56])),
        (4, bytearray([0x5A]), bytearray([0x31, 0x00, 0x00])),
        (8, bytearray([0xF0]), bytearray([0x32, 0xCC, 0xCC])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler._CanFlowControlHandler__encode_any_flow_status")
    def test_create_any_frame_data__valid(self, mock_encode_flow_status,
                                          addressing_format, target_address, address_extension,
                                          dlc, filler_byte, flow_status, block_size, st_min,
                                          data_bytes_number, ai_data_bytes, fs_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_flow_status.return_value = fs_data_bytes
        fc_frame_data = CanFlowControlHandler.create_any_frame_data(addressing_format=addressing_format,
                                                                    target_address=target_address,
                                                                    address_extension=address_extension,
                                                                    flow_status=flow_status,
                                                                    block_size=block_size,
                                                                    st_min=st_min,
                                                                    dlc=dlc,
                                                                    filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status,
                                                        block_size=block_size,
                                                        st_min=st_min)
        assert isinstance(fc_frame_data, bytearray)
        assert len(fc_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, flow_status, block_size, st_min", [
        (CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (2, bytearray(), bytearray([0x30, 0x12, 0x56])),
        (1, bytearray([0x5A]), bytearray([0x31])),
        (0, bytearray([0xF0]), bytearray([0x32, 0xCC, 0xCC])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler._CanFlowControlHandler__encode_any_flow_status")
    def test_create_any_frame_data__invalid(self, mock_encode_flow_status,
                                            addressing_format, target_address, address_extension,
                                            dlc, filler_byte, flow_status, block_size, st_min,
                                            data_bytes_number, ai_data_bytes, fs_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_flow_status.return_value = fs_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanFlowControlHandler.create_any_frame_data(addressing_format=addressing_format,
                                                        target_address=target_address,
                                                        address_extension=address_extension,
                                                        flow_status=flow_status,
                                                        block_size=block_size,
                                                        st_min=st_min,
                                                        dlc=dlc,
                                                        filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status,
                                                        block_size=block_size,
                                                        st_min=st_min)

    # is_flow_control

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, (0x30, 0x00, 0x00)),
        (1, [0x01, 0x32] + list(range(46))),
        (0, [0x32] + list(range(7))),
    ])
    def test_is_flow_control__true(self, addressing_format, raw_frame_data,
                                   ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanFlowControlHandler.is_flow_control(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is True
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, (0x0F, 0xFE, 0xDC, 0xBA, 0x98, 0x76)),
        (1, [0x01, 0x10] + list(range(46))),
        (0, [0x25] + list(range(47))),
        (1, (0x13, 0xFE, 0x21)),
    ])
    def test_is_flow_control__false(self, addressing_format, raw_frame_data, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanFlowControlHandler.is_flow_control(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is False
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # decode_flow_status

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, [0x30, 0x12, 0x34]),
        (1, (0x31, 0x3F, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowStatus")
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.is_flow_control")
    def test_decode_flow_status(self, mock_is_flow_control, mock_can_flow_status_class,
                                addressing_format, raw_frame_data, ai_bytes_number):
        mock_is_flow_control.return_value = True
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanFlowControlHandler.decode_flow_status(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data) == mock_can_flow_status_class.return_value
        mock_is_flow_control.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_can_flow_status_class.assert_called_once_with(raw_frame_data[ai_bytes_number] & 0xF)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [
        [0x30, 0x12, 0x34],
        (0x31, 0x3F, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.is_flow_control")
    def test_decode_flow_status__value_error(self, mock_is_flow_control,
                                             addressing_format, raw_frame_data):
        mock_is_flow_control.return_value = False
        with pytest.raises(ValueError):
            CanFlowControlHandler.decode_flow_status(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        mock_is_flow_control.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_not_called()

    # decode_block_size

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, [0x30, 0x12, 0x34]),
        (1, (0x31, 0x3F, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.decode_flow_status")
    def test_decode_block_size(self, mock_decode_flow_status,
                               addressing_format, raw_frame_data, ai_bytes_number):
        mock_decode_flow_status.return_value = CanFlowStatus.ContinueToSend
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        block_size = CanFlowControlHandler.decode_block_size(addressing_format=addressing_format,
                                                             raw_frame_data=raw_frame_data)
        assert block_size == raw_frame_data[ai_bytes_number + CanFlowControlHandler.BS_BYTE_POSITION]
        mock_decode_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [
        [0x30, 0x12, 0x34],
        (0x31, 0x3F, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55),
    ])
    @pytest.mark.parametrize("flow_status", ["something else", 0xF])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.decode_flow_status")
    def test_decode_block_size__value_error(self, mock_decode_flow_status,
                                            addressing_format, raw_frame_data, flow_status):
        mock_decode_flow_status.return_value = flow_status
        with pytest.raises(ValueError):
            CanFlowControlHandler.decode_block_size(addressing_format=addressing_format,
                                                    raw_frame_data=raw_frame_data)
        mock_decode_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_not_called()

    # decode_st_min

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, [0x30, 0x12, 0x34]),
        (1, (0x31, 0x3F, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.decode_flow_status")
    def test_decode_st_min(self, mock_decode_flow_status,
                           addressing_format, raw_frame_data, ai_bytes_number):
        mock_decode_flow_status.return_value = CanFlowStatus.ContinueToSend
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        block_size = CanFlowControlHandler.decode_st_min(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        assert block_size == raw_frame_data[ai_bytes_number + CanFlowControlHandler.STMIN_BYTE_POSITION]
        mock_decode_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [
        [0x30, 0x12, 0x34],
        (0x31, 0x3F, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55),
    ])
    @pytest.mark.parametrize("flow_status", ["something else", 0xF])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.decode_flow_status")
    def test_decode_st_min__value_error(self, mock_decode_flow_status,
                                        addressing_format, raw_frame_data, flow_status):
        mock_decode_flow_status.return_value = flow_status
        with pytest.raises(ValueError):
            CanFlowControlHandler.decode_st_min(addressing_format=addressing_format,
                                                raw_frame_data=raw_frame_data)
        mock_decode_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_not_called()

    # get_min_dlc

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number", [0, 1, 2])
    def test_get_min_dlc(self, addressing_format, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanFlowControlHandler.get_min_dlc(addressing_format=addressing_format) \
               == self.mock_get_min_dlc.return_value
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_get_min_dlc.assert_called_once_with(ai_bytes_number + CanFlowControlHandler.FS_BYTES_USED)

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing format", "some raw frame data"),
        ("another format", range(5)),
    ])
    @pytest.mark.parametrize("min_dlc, decoded_dlc", [
        (7, 8),
        (13, 15),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.decode_flow_status")
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.get_min_dlc")
    def test_validate_frame_data__valid(self, mock_get_min_dlc, mock_decode_flow_status,
                                        addressing_format, raw_frame_data,
                                        decoded_dlc, min_dlc):
        mock_get_min_dlc.return_value = min_dlc
        self.mock_encode_dlc.return_value = decoded_dlc
        CanFlowControlHandler.validate_frame_data(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_decode_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format)

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing format", "some raw frame data"),
        ("another format", range(5)),
    ])
    @pytest.mark.parametrize("min_dlc, decoded_dlc", [
        (4, 7),
        (9, 8),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.decode_flow_status")
    @patch(f"{SCRIPT_LOCATION}.CanFlowControlHandler.get_min_dlc")
    def test_validate_frame_data__invalid_dlc(self, mock_get_min_dlc, mock_decode_flow_status,
                                              addressing_format, raw_frame_data,
                                              decoded_dlc, min_dlc):
        mock_get_min_dlc.return_value = min_dlc
        self.mock_encode_dlc.return_value = decoded_dlc
        with pytest.raises(ValueError):
            CanFlowControlHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_decode_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                        raw_frame_data=raw_frame_data)
        mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format)

    # __encode_valid_flow_status

    @pytest.mark.parametrize("flow_status, block_size, st_min", [
        (CanFlowStatus.ContinueToSend, 0x12, 0x34),
        (CanFlowStatus.Overflow, 0xF0, 0xA6),
        (CanFlowStatus.Wait, 0xD8, 0x7E),
    ])
    def test_encode_valid_flow_status__all_args(self, flow_status, block_size, st_min):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status(flow_status=flow_status,
                                                                                               block_size=block_size,
                                                                                               st_min=st_min)
        assert fs_data_bytes == bytearray([0x30 + flow_status, block_size, st_min])
        self.mock_validate_flow_status.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_has_calls([call(block_size), call(st_min)], any_order=True)

    @pytest.mark.parametrize("flow_status, filler_byte", [
        (CanFlowStatus.Overflow, 0x52),
        (CanFlowStatus.Wait, 0x99),
    ])
    def test_encode_valid_flow_status__fs_only(self, flow_status, filler_byte):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status(flow_status=flow_status,
                                                                                               filler_byte=filler_byte)
        assert fs_data_bytes == bytearray([0x30 + flow_status, filler_byte, filler_byte])
        self.mock_validate_flow_status.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("block_size, st_min", [
        (None, 0x34),
        (0xF0, None),
        (0x00, 0xFF),
    ])
    def test_encode_valid_flow_status__cts(self, block_size, st_min):
        CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status(flow_status=CanFlowStatus.ContinueToSend,
                                                                               block_size=block_size,
                                                                               st_min=st_min)
        self.mock_validate_flow_status.assert_called_once_with(CanFlowStatus.ContinueToSend)
        self.mock_validate_raw_byte.assert_has_calls([call(block_size), call(st_min)], any_order=True)

    # __encode_any_flow_status

    @pytest.mark.parametrize("flow_status, block_size, st_min", [
        (CanFlowStatus.ContinueToSend, 0x12, 0x34),
        (0xD, 0xF0, 0xA6),
        (0x9, 0xD8, 0x7E),
    ])
    def test_encode_any_flow_status__all_args(self, flow_status, block_size, st_min):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_any_flow_status(flow_status=flow_status,
                                                                                             block_size=block_size,
                                                                                             st_min=st_min)
        assert fs_data_bytes == bytearray([0x30 + flow_status, block_size, st_min])
        self.mock_validate_nibble.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_has_calls([call(block_size), call(st_min)], any_order=True)

    @pytest.mark.parametrize("flow_status, block_size, st_min", [
        (0xF, 0xF0, None),
        (0xB, None, 0x7E),
    ])
    def test_encode_any_flow_status__fs_and_one_arg(self, flow_status, block_size, st_min):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_any_flow_status(flow_status=flow_status,
                                                                                             block_size=block_size,
                                                                                             st_min=st_min)
        assert fs_data_bytes == bytearray([0x30 + flow_status, block_size or st_min or 0])
        self.mock_validate_nibble.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_called_once()

    @pytest.mark.parametrize("flow_status", [0, 5, 15])
    def test_encode_any_flow_status__fs_only(self, flow_status):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_any_flow_status(flow_status=flow_status)
        assert fs_data_bytes == bytearray([0x30 + flow_status])
        self.mock_validate_nibble.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_not_called()


@pytest.mark.integration
class TestCanFlowControlHandlerIntegration:
    """Integration tests for `CanFlowControlHandler` class."""

    # create_valid_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "flow_status": CanFlowStatus.Overflow}, bytearray([0x32, 0xCC, 0xCC])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0x00,
          "st_min": 0xFF,
          "dlc": 0xF,
          "filler_byte": 0x9B,
          "target_address": 0xA1}, bytearray([0x30, 0x00, 0xFF] + ([0x9B] * 61))),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "flow_status": CanFlowStatus.ContinueToSend,
          "block_size": 0xFF,
          "st_min": 0x00,
          "dlc": 8,
          "filler_byte": 0x85,
          "target_address": 0xA1}, bytearray([0xA1, 0x30, 0xFF, 0x00, 0x85, 0x85, 0x85, 0x85])),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "flow_status": CanFlowStatus.Wait,
          "filler_byte": 0x39,
          "dlc": 4,
          "address_extension": 0x0B}, bytearray([0x0B, 0x31, 0x39, 0x39])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "flow_status": 1,
          "block_size": 0xED,
          "st_min": 0xCB,
          "filler_byte": 0x99,
          "target_address": 0x9A,
          "address_extension": 0xFF}, bytearray([0xFF, 0x31, 0xED, 0xCB])),
    ])
    def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanFlowControlHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
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
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "flow_status": CanFlowStatus.ContinueToSend,
          "dlc": 1}, bytearray([0x30])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "flow_status": 0xF,
          "dlc": 0xF,
          "filler_byte": 0x9B,
          "target_address": 0xA1}, bytearray([0x3F] + ([0x9B] * 63))),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "flow_status": CanFlowStatus.Wait,
          "block_size": 0xFF,
          "st_min": 0x00,
          "dlc": 8,
          "filler_byte": 0x85,
          "target_address": 0xA1}, bytearray([0xA1, 0x31, 0xFF, 0x00, 0x85, 0x85, 0x85, 0x85])),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "flow_status": 5,
          "dlc": 2,
          "address_extension": 0x0B}, bytearray([0x0B, 0x35])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "flow_status": 3,
          "dlc": 3,
          "filler_byte": 0x99,
          "target_address": 0x9A,
          "address_extension": 0xFF}, bytearray([0xFF, 0x33, 0x99])),
    ])
    def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanFlowControlHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
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
         "dlc": 8,
         "block_size": 0x100,
         "target_address": 0x9A,
         "address_extension": 0xFF}
    ])
    def test_create_any_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanFlowControlHandler.create_any_frame_data(**kwargs)

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x30, 0x12, 0x34]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x31, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xA1, 0x32, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0xBC, 0x30, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x90, 0x30, 0x17, 0xFE] + ([0xCC] * 60)),
    ])
    def test_validate_frame_data__valid(self, addressing_format, raw_frame_data):
        assert CanFlowControlHandler.validate_frame_data(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x30, 0x12]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x31, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xA1, 0x32, 0xCC)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0xBC, 0x34, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x90, 0x30, 0x17, 0xFE] + ([0xCC] * 59)),
    ])
    def test_validate_frame_data__invalid(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            CanFlowControlHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)


class TestAbstractFlowControlParametersGenerator:
    """Unit tests for 'AbstractFlowControlParametersGenerator' class."""

    def setup_method(self):
        self.mock_flow_control_parameters_generator = Mock(spec=AbstractFlowControlParametersGenerator)

    # __iter__

    def test_iter(self):
        assert (AbstractFlowControlParametersGenerator.__iter__(self.mock_flow_control_parameters_generator)
                == self.mock_flow_control_parameters_generator)


class TestDefaultFlowControlParametersGenerator:
    """Unit tests for 'DefaultFlowControlParametersGenerator' class."""

    def setup_method(self):
        self.mock_flow_control_parameters_generator = Mock(spec=AbstractFlowControlParametersGenerator)
        # patching
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_deepcopy = patch(f"{SCRIPT_LOCATION}.deepcopy")
        self.mock_deepcopy = self._patcher_deepcopy.start()

    def teardown_method(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_deepcopy.stop()

    # inheritance

    def test_inheritance(self):
        assert issubclass(DefaultFlowControlParametersGenerator, AbstractFlowControlParametersGenerator)

    # __init__

    @pytest.mark.parametrize("block_size, st_min, wait_count, repeat_wait", [
        (0, 0, 0, False),
        (0xFF, 0xFF, 1234, True)
    ])
    def test_init(self, block_size, st_min, wait_count, repeat_wait):
        DefaultFlowControlParametersGenerator.__init__(self.mock_flow_control_parameters_generator,
                                                       block_size, st_min, wait_count, repeat_wait)
        assert self.mock_flow_control_parameters_generator.block_size == block_size
        assert self.mock_flow_control_parameters_generator.st_min == st_min
        assert self.mock_flow_control_parameters_generator.wait_count == wait_count
        assert self.mock_flow_control_parameters_generator.repeat_wait == repeat_wait
        assert self.mock_flow_control_parameters_generator._remaining_wait is None

    # iter

    def test_iter__no_wait(self):
        self.mock_deepcopy.return_value.wait_count = 0
        iterator = DefaultFlowControlParametersGenerator.__iter__(self.mock_flow_control_parameters_generator)
        assert iterator == self.mock_deepcopy.return_value
        assert iterator._remaining_wait is None
        self.mock_deepcopy.assert_called_once_with(self.mock_flow_control_parameters_generator)

    @pytest.mark.parametrize("wait_count", [1, 6543])
    def test_iter__with_wait(self, wait_count):
        self.mock_deepcopy.return_value.wait_count = wait_count
        iterator = DefaultFlowControlParametersGenerator.__iter__(self.mock_flow_control_parameters_generator)
        assert iterator == self.mock_deepcopy.return_value
        assert iterator._remaining_wait == wait_count
        self.mock_deepcopy.assert_called_once_with(self.mock_flow_control_parameters_generator)

    # next

    @pytest.mark.parametrize("block_size, st_min", [
        (0, 0),
        (0xFF, 0xFF)
    ])
    def test_next__no_wait(self, block_size, st_min):
        self.mock_flow_control_parameters_generator._remaining_wait = None
        self.mock_flow_control_parameters_generator.block_size = block_size
        self.mock_flow_control_parameters_generator.st_min = st_min
        assert (DefaultFlowControlParametersGenerator.__next__(self.mock_flow_control_parameters_generator) ==
                (CanFlowStatus.ContinueToSend, block_size, st_min))
        assert self.mock_flow_control_parameters_generator._remaining_wait is None

    @pytest.mark.parametrize("block_size, st_min", [
        (0, 0),
        (0xFF, 0xFF)
    ])
    def test_next__wait_0__without_repeat(self, block_size, st_min):
        self.mock_flow_control_parameters_generator._remaining_wait = 0
        self.mock_flow_control_parameters_generator.repeat_wait = False
        self.mock_flow_control_parameters_generator.block_size = block_size
        self.mock_flow_control_parameters_generator.st_min = st_min
        assert (DefaultFlowControlParametersGenerator.__next__(self.mock_flow_control_parameters_generator) ==
                (CanFlowStatus.ContinueToSend, block_size, st_min))
        assert self.mock_flow_control_parameters_generator._remaining_wait == 0

    @pytest.mark.parametrize("block_size, st_min, wait_count", [
        (0, 0, 1),
        (0xFF, 0xFF, 54)
    ])
    def test_next__wait_0__with_repeat(self, block_size, st_min, wait_count):
        self.mock_flow_control_parameters_generator._remaining_wait = 0
        self.mock_flow_control_parameters_generator.repeat_wait = True
        self.mock_flow_control_parameters_generator.wait_count = wait_count
        self.mock_flow_control_parameters_generator.block_size = block_size
        self.mock_flow_control_parameters_generator.st_min = st_min
        assert (DefaultFlowControlParametersGenerator.__next__(self.mock_flow_control_parameters_generator) ==
                (CanFlowStatus.ContinueToSend, block_size, st_min))
        assert self.mock_flow_control_parameters_generator._remaining_wait == wait_count

    @pytest.mark.parametrize("remaining_wait", [1, 6543])
    def test_next__wait(self, remaining_wait):
        self.mock_flow_control_parameters_generator._remaining_wait = remaining_wait
        assert (DefaultFlowControlParametersGenerator.__next__(self.mock_flow_control_parameters_generator) ==
                (CanFlowStatus.Wait, None, None))
        assert self.mock_flow_control_parameters_generator._remaining_wait == remaining_wait - 1

    # block_size

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_block_size__get(self, value):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__block_size = value
        assert DefaultFlowControlParametersGenerator.block_size.fget(self.mock_flow_control_parameters_generator) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_flow_control_parameters_generator__set(self, value):
        DefaultFlowControlParametersGenerator.block_size.fset(self.mock_flow_control_parameters_generator, value)
        assert self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__block_size == value
        self.mock_validate_raw_byte.assert_called_once_with(value)

    # st_min

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_st_min__get(self, value):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__st_min = value
        assert DefaultFlowControlParametersGenerator.st_min.fget(self.mock_flow_control_parameters_generator) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_flow_control_parameters_generator__set(self, value):
        DefaultFlowControlParametersGenerator.st_min.fset(self.mock_flow_control_parameters_generator, value)
        assert self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__st_min == value
        self.mock_validate_raw_byte.assert_called_once_with(value)

    # wait_count

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_wait_count__get(self, value):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__wait_count = value
        assert DefaultFlowControlParametersGenerator.wait_count.fget(self.mock_flow_control_parameters_generator) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_parameters_generator__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            DefaultFlowControlParametersGenerator.wait_count.fset(self.mock_flow_control_parameters_generator, value)
        mock_isinstance.assert_called_once_with(value, int)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_parameters_generator__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_lt = Mock(return_value=True)
        mock_value = MagicMock(__lt__=mock_lt)
        with pytest.raises(ValueError):
            DefaultFlowControlParametersGenerator.wait_count.fset(self.mock_flow_control_parameters_generator, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)
        mock_lt.assert_called_once_with(0)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_parameters_generator__set(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_lt = Mock(return_value=False)
        mock_value = MagicMock(__lt__=mock_lt)
        DefaultFlowControlParametersGenerator.wait_count.fset(self.mock_flow_control_parameters_generator, mock_value)
        assert self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__wait_count == mock_value
        mock_isinstance.assert_called_once_with(mock_value, int)
        mock_lt.assert_called_once_with(0)
        
    # repeat_wait

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_repeat_wait__get(self, value):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__repeat_wait = value
        assert DefaultFlowControlParametersGenerator.repeat_wait.fget(self.mock_flow_control_parameters_generator) == value

    @patch(f"{SCRIPT_LOCATION}.bool")
    def test_flow_control_parameters_generator__set(self, mock_bool):
        mock_value = Mock()
        DefaultFlowControlParametersGenerator.repeat_wait.fset(self.mock_flow_control_parameters_generator, mock_value)
        assert self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__repeat_wait == mock_bool.return_value
        mock_bool.assert_called_once_with(mock_value)

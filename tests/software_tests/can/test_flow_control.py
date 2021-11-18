import pytest
from mock import patch, call

from uds.can.flow_control import CanSTminTranslator, CanFlowStatus, CanFlowControlHandler, \
    InconsistentArgumentsError, CanDlcHandler
from uds.can import CanAddressingFormat
from uds.utilities import ValidatedEnum, NibbleEnum


class TestCanFlowStatus:
    """Unit tests for 'CanFlowStatus' class."""

    def test_inheritance__validated_enum(self):
        assert issubclass(CanFlowStatus, ValidatedEnum)

    def test_inheritance__nibble_enum(self):
        assert issubclass(CanFlowStatus, NibbleEnum)


class TestCanSTmin:
    """Unit tests for 'CanSTmin' class."""

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

    SCRIPT_LOCATION = TestCanSTmin.SCRIPT_LOCATION

    def setup(self):
        self._patcher_validate_nibble = patch(f"{self.SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_encode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.encode_dlc")
        self.mock_encode_dlc = self._patcher_encode_dlc.start()
        self._patcher_decode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.decode_dlc")
        self.mock_decode_dlc = self._patcher_decode_dlc.start()
        self._patcher_get_min_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
        self.mock_get_min_dlc = self._patcher_get_min_dlc.start()
        self._patcher_encode_ai_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_validate_flow_status = patch(f"{self.SCRIPT_LOCATION}.CanFlowStatus.validate_member")
        self.mock_validate_flow_status = self._patcher_validate_flow_status.start()

    def teardown(self):
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
        (CanDlcHandler.MIN_DLC_DATA_PADDING, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_DLC_DATA_PADDING + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (3, [], [0x30, 0x12, 0x56]),
        (4, [0x5A], [0x31, 0x00, 0x00]),
        (8, [0xF0], [0x32, 0xCC, 0xCC]),
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
        assert isinstance(fc_frame_data, list)
        assert len(fc_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, flow_status, block_size, st_min", [
        (CanDlcHandler.MIN_DLC_DATA_PADDING, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_DLC_DATA_PADDING + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (3, [], [0x30, 0x12, 0x56]),
        (4, [0x5A], [0x31, 0x00, 0x00]),
        (8, [0xF0], [0x32, 0xCC, 0xCC]),
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
        assert isinstance(fc_frame_data, list)
        assert len(fc_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (CanDlcHandler.MIN_DLC_DATA_PADDING - 2, 0x66, 4, [], [0x30, 0x12, 0x56]),
        (CanDlcHandler.MIN_DLC_DATA_PADDING - 1, 0x99, 5, [0xFF], [0x31, 0x00, 0x00]),
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
        (CanDlcHandler.MIN_DLC_DATA_PADDING - 1, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_DLC_DATA_PADDING + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (3, [], [0x30, 0x12, 0x56]),
        (4, [0x5A], [0x31, 0x00, 0x00]),
        (8, [0xF0], [0x32, 0xCC, 0xCC]),
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
        assert isinstance(fc_frame_data, list)
        assert len(fc_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, flow_status, block_size, st_min", [
        (CanDlcHandler.MIN_DLC_DATA_PADDING - 1, 0x66, "some flow status", "some block size", "some STmin"),
        (CanDlcHandler.MIN_DLC_DATA_PADDING + 2, 0x99, CanFlowStatus.ContinueToSend, 0x00, 0xFF),
    ])
    @pytest.mark.parametrize("data_bytes_number, ai_data_bytes, fs_data_bytes", [
        (2, [], [0x30, 0x12, 0x56]),
        (1, [0x5A], [0x31]),
        (0, [0xF0], [0x32, 0xCC, 0xCC]),
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
        assert fs_data_bytes == [0x30 + flow_status, block_size, st_min]
        self.mock_validate_flow_status.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_has_calls([call(block_size), call(st_min)], any_order=True)

    @pytest.mark.parametrize("flow_status, filler_byte", [
        (CanFlowStatus.Overflow, 0x52),
        (CanFlowStatus.Wait, 0x99),
    ])
    def test_encode_valid_flow_status__fs_only(self, flow_status, filler_byte):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_valid_flow_status(flow_status=flow_status,
                                                                                               filler_byte=filler_byte)
        assert fs_data_bytes == [0x30 + flow_status, filler_byte, filler_byte]
        self.mock_validate_flow_status.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("block_size, st_min", [
        (None, 0x34),
        (0xF0, None),
        ("something", "something else"),
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
        assert fs_data_bytes == [0x30 + flow_status, block_size, st_min]
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
        assert fs_data_bytes == [0x30 + flow_status, block_size or st_min or 0]
        self.mock_validate_nibble.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_called_once()

    @pytest.mark.parametrize("flow_status", [0, 5, 15])
    def test_encode_any_flow_status__fs_only(self, flow_status):
        fs_data_bytes = CanFlowControlHandler._CanFlowControlHandler__encode_any_flow_status(flow_status=flow_status)
        assert fs_data_bytes == [0x30 + flow_status]
        self.mock_validate_nibble.assert_called_once_with(flow_status)
        self.mock_validate_raw_byte.assert_not_called()


@pytest.mark.integration
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
          "target_address": 0xA1}, [0x30, 0x00, 0xFF] + ([0x9B] * 61)),
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
          "block_size": 0xED,
          "st_min": 0xCB,
          "filler_byte": 0x99,
          "target_address": 0x9A,
          "address_extension": 0xFF}, [0xFF, 0x31, 0xED, 0xCB]),
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
          "target_address": 0xA1}, [0x3F] + ([0x9B] * 63)),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "flow_status": CanFlowStatus.Wait,
          "block_size": 0xFF,
          "st_min": 0x00,
          "dlc": 8,
          "filler_byte": 0x85,
          "target_address": 0xA1}, [0xA1, 0x31, 0xFF, 0x00, 0x85, 0x85, 0x85, 0x85]),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "flow_status": 5,
          "dlc": 2,
          "address_extension": 0x0B}, [0x0B, 0x35]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "flow_status": 3,
          "dlc": 3,
          "filler_byte": 0x99,
          "target_address": 0x9A,
          "address_extension": 0xFF}, [0xFF, 0x33, 0x99]),
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

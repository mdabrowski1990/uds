import pytest
from mock import MagicMock, Mock, call, patch

from uds.can.packet.flow_control import (
    BS_BYTE_POSITION,
    DEFAULT_FILLER_BYTE,
    FLOW_CONTROL_N_PCI,
    FS_BYTES_USED,
    ST_MIN_BYTE_POSITION,
    AbstractFlowControlParametersGenerator,
    CanAddressingFormat,
    CanDlcHandler,
    CanFlowStatus,
    CanSTminTranslator,
    DefaultFlowControlParametersGenerator,
    InconsistentArgumentsError,
    create_flow_control_data,
    encode_flow_status,
    extract_block_size,
    extract_flow_status,
    extract_st_min,
    generate_flow_control_data,
    generate_flow_status,
    get_flow_control_min_dlc,
    is_flow_control,
    validate_flow_control_data,
)
from uds.utilities import NibbleEnum, ValidatedEnum

SCRIPT_LOCATION = "uds.can.packet.flow_control"


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

    @pytest.mark.parametrize("raw_value", [0x80, 0xBA, 0xF0, 0xFA, 0xFF])
    def test_decode__unknown(self, raw_value):
        assert CanSTminTranslator.decode(raw_value) == CanSTminTranslator.MAX_STMIN_TIME
        self.mock_validate_raw_byte.assert_called_once_with(raw_value)
        self.mock_warn.assert_called_once()

    # encode

    @pytest.mark.parametrize("value", [Mock(), None])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_encode__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            CanSTminTranslator.encode(value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [CanSTminTranslator.MAX_VALUE_MS_RANGE + 1,
                                       -1,
                                       CanSTminTranslator.MIN_TIME_VALUE_100US_RANGE * 1.5])
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

    @pytest.mark.parametrize("value", [Mock(), None])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_time_value__wrong_type(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        assert CanSTminTranslator.is_time_value(value) is False
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value, is_ms_value, is_100us_value", [
        (52, True, False),
        (0.5, False, True),
        (0.123456, False, False),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSTminTranslator._is_ms_value")
    @patch(f"{SCRIPT_LOCATION}.CanSTminTranslator._is_100us_value")
    def test_is_time_value__valid(self, mock_is_100us_value, mock_is_ms_value,
                                  value, is_ms_value, is_100us_value):
        mock_is_100us_value.return_value = is_100us_value
        mock_is_ms_value.return_value = is_ms_value
        assert CanSTminTranslator.is_time_value(value) is (is_ms_value or is_100us_value)

    # _is_ms_value

    @pytest.mark.parametrize("value", [CanSTminTranslator.MIN_VALUE_MS_RANGE, 59.,
                                       CanSTminTranslator.MAX_VALUE_MS_RANGE])
    def test_is_ms_value__true(self, value):
        assert CanSTminTranslator._is_ms_value(value) is True

    @pytest.mark.parametrize("value", [-1, CanSTminTranslator.MAX_VALUE_MS_RANGE + 1, 25.99999])
    def test_is_ms_value__false(self, value):
        assert CanSTminTranslator._is_ms_value(value) is False

    # _is_100us_value

    @pytest.mark.parametrize("value", [CanSTminTranslator.MIN_TIME_VALUE_100US_RANGE, 0.5,
                                       CanSTminTranslator.MAX_TIME_VALUE_100US_RANGE])
    def test_is_100us_value__true(self, value):
        assert CanSTminTranslator._is_100us_value(value) is True

    @pytest.mark.parametrize("value", [0, CanSTminTranslator.MAX_TIME_VALUE_100US_RANGE + 0.1, 0.1234])
    def test_is_100us_value__false(self, value):
        assert CanSTminTranslator._is_100us_value(value) is False


@pytest.mark.integration
class TestCanSTminIntegration:
    """Integration tests for CanSTmin class."""

    @pytest.mark.parametrize("raw_value", [0x00, 0x12, 0x7F, 0xF1, 0xF4, 0xF9])
    def test_decode_and_encode(self, raw_value):
        time_value = CanSTminTranslator.decode(raw_value)
        assert CanSTminTranslator.encode(time_value) == raw_value

    @pytest.mark.parametrize("time_value", [0, 126, 127, 0.1, 0.2, 0.9])
    def test_encode_and_decode(self, time_value):
        raw_value = CanSTminTranslator.encode(time_value)
        assert CanSTminTranslator.decode(raw_value) == time_value


class TestCanFlowControl:
    """Unit tests for functions in CAN Flow Control module."""

    def setup_method(self):
        self._patcher_validate_nibble = patch(f"{SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_can_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler",
                                              Mock(MIN_BASE_UDS_DLC=CanDlcHandler.MIN_BASE_UDS_DLC))
        self.mock_can_dlc_handler = self._patcher_can_dlc_handler.start()
        self._patcher_can_addressing_information = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_addressing_information = self._patcher_can_addressing_information.start()
        self._patcher_can_flow_status = patch(f"{SCRIPT_LOCATION}.CanFlowStatus")
        self.mock_can_flow_status = self._patcher_can_flow_status.start()

    def teardown_method(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_warn.stop()
        self._patcher_can_dlc_handler.stop()
        self._patcher_can_addressing_information.stop()
        self._patcher_can_flow_status.stop()

    # is_flow_control

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number, expected_output", [
        (Mock(), [FLOW_CONTROL_N_PCI << 4, *range(7)], 0, True),
        (Mock(), [0xFF, (FLOW_CONTROL_N_PCI << 4) + 0xF, 0xFF, 0xFF], 1, True),
        (Mock(), [0xFF, (FLOW_CONTROL_N_PCI << 4) + 0xF, 0xFF, 0xFF], 0, False),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [(FLOW_CONTROL_N_PCI << 4), 0x00, 0xAA, 0xBB, 0xCC], 1, False),
    ])
    def test_is_flow_control(self, addressing_format, raw_frame_data,
                                   ai_data_bytes_number, expected_output):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert is_flow_control(addressing_format=addressing_format, raw_frame_data=raw_frame_data) is expected_output
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data, min_dlc, dlc", [
        (Mock(), MagicMock(), 5, 5),
        (CanAddressingFormat.EXTENDED_ADDRESSING, range(8), 3, CanDlcHandler.MIN_BASE_UDS_DLC),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_flow_status")
    @patch(f"{SCRIPT_LOCATION}.get_flow_control_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.is_flow_control")
    def test_validate_frame_data__valid(self, mock_is_flow_control, mock_get_flow_control_min_dlc,
                                        mock_extract_flow_status,
                                        addressing_format, raw_frame_data,
                                        min_dlc, dlc):
        mock_is_flow_control.return_value = True
        mock_get_flow_control_min_dlc.return_value = min_dlc
        self.mock_can_dlc_handler.encode_dlc.return_value = dlc
        assert validate_flow_control_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data) is None
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data, allow_empty=False)
        mock_is_flow_control.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_extract_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        mock_get_flow_control_min_dlc.assert_called_once_with(addressing_format=addressing_format)
        self.mock_can_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))

    @pytest.mark.parametrize("addressing_format, raw_frame_data, min_dlc, dlc", [
        (Mock(), MagicMock(), CanDlcHandler.MIN_BASE_UDS_DLC - 2, CanDlcHandler.MIN_BASE_UDS_DLC - 1),
        (CanAddressingFormat.EXTENDED_ADDRESSING, range(8), 6, 5),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_flow_status")
    @patch(f"{SCRIPT_LOCATION}.get_flow_control_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.is_flow_control")
    def test_validate_frame_data__inconsistent(self, mock_is_flow_control, mock_get_flow_control_min_dlc,
                                        mock_extract_flow_status,
                                        addressing_format, raw_frame_data,
                                        min_dlc, dlc):
        mock_is_flow_control.return_value = True
        mock_get_flow_control_min_dlc.return_value = min_dlc
        self.mock_can_dlc_handler.encode_dlc.return_value = dlc
        with pytest.raises(InconsistentArgumentsError):
            validate_flow_control_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data, allow_empty=False)
        mock_is_flow_control.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_extract_flow_status.assert_called_once_with(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        mock_get_flow_control_min_dlc.assert_called_once_with(addressing_format=addressing_format)
        self.mock_can_dlc_handler.encode_dlc.assert_called_once_with(len(raw_frame_data))

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (Mock(), MagicMock()),
        (CanAddressingFormat.EXTENDED_ADDRESSING, range(8)),
    ])
    @patch(f"{SCRIPT_LOCATION}.extract_flow_status")
    @patch(f"{SCRIPT_LOCATION}.get_flow_control_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.is_flow_control")
    def test_validate_frame_data__value_error(self, mock_is_flow_control, mock_get_flow_control_min_dlc,
                                              mock_extract_flow_status,
                                              addressing_format, raw_frame_data):
        mock_is_flow_control.return_value = False
        with pytest.raises(ValueError):
            validate_flow_control_data(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data, allow_empty=False)
        mock_is_flow_control.assert_called_once_with(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        mock_extract_flow_status.assert_not_called()
        mock_get_flow_control_min_dlc.assert_not_called()
        self.mock_can_dlc_handler.encode_dlc.assert_not_called()

    # create_flow_control_data

    @pytest.mark.parametrize("addressing_format, flow_status, ai_data_bytes, fs_data_bytes", [
        (Mock(), Mock(), bytearray(), bytearray([0x31])),
        (CanAddressingFormat.EXTENDED_ADDRESSING, CanFlowStatus.Overflow, bytearray([0x54]), bytearray([0x3F])),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_flow_control_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.encode_flow_status")
    def test_create_flow_control_data__mandatory_args(self, mock_encode_flow_status, mock_get_flow_control_min_dlc,
                                                      addressing_format, flow_status,
                                                      ai_data_bytes, fs_data_bytes):
        expected_output = ai_data_bytes + fs_data_bytes + bytearray([DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE])
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = len(expected_output)
        mock_encode_flow_status.return_value = fs_data_bytes
        assert create_flow_control_data(addressing_format=addressing_format,
                                        flow_status=flow_status) == expected_output
        self.mock_validate_raw_byte.assert_called_once_with(DEFAULT_FILLER_BYTE)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=None,
            address_extension=None)
        mock_get_flow_control_min_dlc.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(mock_get_flow_control_min_dlc.return_value)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status)

    @pytest.mark.parametrize("addressing_format, flow_status, block_size, st_min, dlc, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, fs_data_bytes, data_bytes_number", [
        (Mock(), Mock(), 0x00, 0xFF, CanDlcHandler.MIN_BASE_UDS_DLC, 0xA5, Mock(), Mock(),
         bytearray([0xA1]), bytearray([0x30]), 8),
        (CanAddressingFormat.NORMAL_ADDRESSING, CanFlowStatus.ContinueToSend, 0xFF, 0x12,
         CanDlcHandler.MAX_DLC_VALUE, 0x00, 0xE5, 0xD4,
         bytearray(), bytearray([0x31]), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_flow_control_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.encode_flow_status")
    def test_create_flow_control_data__all_args(self, mock_encode_flow_status, mock_get_flow_control_min_dlc,
                                                addressing_format, flow_status, block_size, st_min, dlc,
                                                filler_byte, target_address, address_extension,
                                                ai_data_bytes, fs_data_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_flow_status.return_value = fs_data_bytes
        expected_output = ai_data_bytes + fs_data_bytes + bytearray([block_size, st_min])
        while len(expected_output) < data_bytes_number:
            expected_output.append(filler_byte)
        assert create_flow_control_data(addressing_format=addressing_format,
                                        flow_status=flow_status,
                                        block_size=block_size,
                                        st_min=st_min,
                                        dlc=dlc,
                                        filler_byte=filler_byte,
                                        target_address=target_address,
                                        address_extension=address_extension) == expected_output
        self.mock_validate_raw_byte.assert_has_calls([call(filler_byte), call(block_size), call(st_min)],
                                                     any_order=True)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        mock_get_flow_control_min_dlc.assert_not_called()
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status)

    @pytest.mark.parametrize("addressing_format, flow_status, block_size, st_min, dlc, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, fs_data_bytes, data_bytes_number", [
        (Mock(), Mock(), 0x00, 0xFF, CanDlcHandler.MIN_BASE_UDS_DLC - 1, 0xA5, Mock(), Mock(),
         bytearray([0xA1]), bytearray([0x30]), 8),
        (CanAddressingFormat.NORMAL_ADDRESSING, CanFlowStatus.ContinueToSend, 0xFF, 0x12,
         CanDlcHandler.MAX_DLC_VALUE, 0x00, 0xE5, 0xD4,
         bytearray(), bytearray([0x31]), FS_BYTES_USED - 1),
    ])
    @patch(f"{SCRIPT_LOCATION}.get_flow_control_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.encode_flow_status")
    def test_create_flow_control_data__inconsistent(self, mock_encode_flow_status, mock_get_flow_control_min_dlc,
                                                addressing_format, flow_status, block_size, st_min, dlc,
                                                filler_byte, target_address, address_extension,
                                                ai_data_bytes, fs_data_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_encode_flow_status.return_value = fs_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            create_flow_control_data(addressing_format=addressing_format,
                                     flow_status=flow_status,
                                     block_size=block_size,
                                     st_min=st_min,
                                     dlc=dlc,
                                     filler_byte=filler_byte,
                                     target_address=target_address,
                                     address_extension=address_extension)
        self.mock_validate_raw_byte.assert_has_calls([call(filler_byte), call(block_size), call(st_min)],
                                                     any_order=True)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        mock_get_flow_control_min_dlc.assert_not_called()
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        mock_encode_flow_status.assert_called_once_with(flow_status=flow_status)

    # generate_flow_control_data

    @pytest.mark.parametrize("addressing_format, flow_status, dlc, ai_data_bytes, fs_data_bytes, data_bytes_number", [
        (Mock(), Mock(), Mock(), bytearray(), bytearray([0x3F]), 1),
        (CanAddressingFormat.NORMAL_ADDRESSING, CanFlowStatus.Wait, 0xF, bytearray([0x6B]), bytearray([0x30]), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_flow_status")
    def test_generate_flow_control_data__mandatory_args(self, mock_generate_flow_status,
                                                        addressing_format, flow_status, dlc,
                                                        ai_data_bytes, fs_data_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_generate_flow_status.return_value = fs_data_bytes
        expected_output = ai_data_bytes + fs_data_bytes
        while len(expected_output) < data_bytes_number:
            expected_output.append(DEFAULT_FILLER_BYTE)
        assert generate_flow_control_data(addressing_format=addressing_format,
                                          flow_status=flow_status,
                                          dlc=dlc) == expected_output
        self.mock_validate_raw_byte.assert_called_once_with(DEFAULT_FILLER_BYTE)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=None,
            address_extension=None)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        mock_generate_flow_status.assert_called_once_with(flow_status=flow_status)

    @pytest.mark.parametrize("addressing_format, flow_status, dlc, block_size, st_min, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, fs_data_bytes, data_bytes_number", [
        (Mock(), Mock(), Mock(), 0x5A, 0xBE, 0x97, Mock(), Mock(), bytearray(), bytearray([0x3F]), 3),
        (CanAddressingFormat.EXTENDED_ADDRESSING, 0xF, 0xF, 0xDE, 0x00, 0xAA, 0x92, 0x60, bytearray([0x71]),
         bytearray([0x30]), 64),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_flow_status")
    def test_generate_flow_control_data__all_args(self, mock_generate_flow_status,
                                                  addressing_format, flow_status, dlc, block_size, st_min, filler_byte,
                                                  target_address, address_extension,
                                                  ai_data_bytes, fs_data_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_generate_flow_status.return_value = fs_data_bytes
        expected_output = ai_data_bytes + fs_data_bytes + bytearray([block_size, st_min])
        while len(expected_output) < data_bytes_number:
            expected_output.append(filler_byte)
        assert generate_flow_control_data(addressing_format=addressing_format,
                                          flow_status=flow_status,
                                          dlc=dlc,
                                          block_size=block_size,
                                          st_min=st_min,
                                          filler_byte=filler_byte,
                                          target_address=target_address,
                                          address_extension=address_extension) == expected_output
        self.mock_validate_raw_byte.assert_has_calls([call(filler_byte), call(block_size), call(st_min)],
                                                     any_order=True)
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        mock_generate_flow_status.assert_called_once_with(flow_status=flow_status)

    @pytest.mark.parametrize("addressing_format, flow_status, dlc, block_size, st_min, filler_byte, target_address, "
                             "address_extension, ai_data_bytes, fs_data_bytes, data_bytes_number", [
        (Mock(), Mock(), Mock(), 0x5A, 0xBE, 0x97, Mock(), Mock(), bytearray(), bytearray([0x3F]), FS_BYTES_USED - 1),
        (Mock(), Mock(), Mock(), None, None, 0xAA, Mock(), Mock(), bytearray([0xBB]), bytearray([0x30]), 1),
    ])
    @patch(f"{SCRIPT_LOCATION}.generate_flow_status")
    def test_generate_flow_control_data__inconsistent(self, mock_generate_flow_status,
                                                      addressing_format, flow_status, dlc, block_size, st_min,
                                                      filler_byte,
                                                      target_address, address_extension,
                                                      ai_data_bytes, fs_data_bytes, data_bytes_number):
        self.mock_can_addressing_information.encode_ai_data_bytes.return_value = ai_data_bytes
        self.mock_can_dlc_handler.decode_dlc.return_value = data_bytes_number
        mock_generate_flow_status.return_value = fs_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            generate_flow_control_data(addressing_format=addressing_format,
                                       flow_status=flow_status,
                                       dlc=dlc,
                                       block_size=block_size,
                                       st_min=st_min,
                                       filler_byte=filler_byte,
                                       target_address=target_address,
                                       address_extension=address_extension)
        self.mock_validate_raw_byte.assert_called()
        self.mock_can_addressing_information.encode_ai_data_bytes.assert_called_once_with(
            addressing_format=addressing_format,
            target_address=target_address,
            address_extension=address_extension)
        self.mock_can_dlc_handler.decode_dlc.assert_called_once_with(dlc)
        mock_generate_flow_status.assert_called_once_with(flow_status=flow_status)

    # extract_flow_status

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number", [
        (Mock(), [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0], 0),
        (CanAddressingFormat.EXTENDED_ADDRESSING, bytearray([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0][::-1]), 1),
    ])
    def test_extract_flow_status(self, addressing_format, raw_frame_data, ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert extract_flow_status(addressing_format=addressing_format,
                                   raw_frame_data=raw_frame_data) == self.mock_can_flow_status.return_value
        self.mock_can_flow_status.assert_called_once_with(raw_frame_data[ai_data_bytes_number] & 0xF)

    # extract_block_size

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number", [
        (Mock(), [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0], 0),
        (CanAddressingFormat.EXTENDED_ADDRESSING, bytearray([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0][::-1]), 1),
    ])
    def test_extract_block_size(self, addressing_format, raw_frame_data, ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (extract_block_size(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
                == raw_frame_data[ai_data_bytes_number + BS_BYTE_POSITION])

    # extract_st_min

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes_number", [
        (Mock(), [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0], 0),
        (CanAddressingFormat.EXTENDED_ADDRESSING, bytearray([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0][::-1]), 1),
    ])
    def test_extract_st_min(self, addressing_format, raw_frame_data, ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert (extract_st_min(addressing_format=addressing_format, raw_frame_data=raw_frame_data)
                == raw_frame_data[ai_data_bytes_number + ST_MIN_BYTE_POSITION])

    # get_flow_control_min_dlc

    @pytest.mark.parametrize("addressing_format, ai_data_bytes_number", [
        (Mock(), 0),
        (CanAddressingFormat.EXTENDED_ADDRESSING, 1),
    ])
    def test_get_flow_control_min_dlc(self, addressing_format, ai_data_bytes_number):
        self.mock_can_addressing_information.get_ai_data_bytes_number.return_value = ai_data_bytes_number
        assert get_flow_control_min_dlc(addressing_format) == self.mock_can_dlc_handler.get_min_dlc.return_value
        self.mock_can_addressing_information.get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_can_dlc_handler.get_min_dlc.assert_called_once_with(ai_data_bytes_number + FS_BYTES_USED)

    # encode_flow_status

    @pytest.mark.parametrize("flow_status", [Mock(), CanFlowStatus.ContinueToSend])
    @patch(f"{SCRIPT_LOCATION}.generate_flow_status")
    def test_encode_flow_status(self, mock_generate_flow_status, flow_status):
        assert encode_flow_status(flow_status) == mock_generate_flow_status.return_value
        self.mock_can_flow_status.validate_member.assert_called_once_with(flow_status)
        mock_generate_flow_status.assert_called_once_with(flow_status)

    # generate_flow_status

    @pytest.mark.parametrize("flow_status", [0x0, 0x5, 0xF])
    def test_generate_flow_status(self, flow_status):
        assert generate_flow_status(flow_status=flow_status) == bytearray([0x30 + flow_status])
        self.mock_validate_nibble.assert_called_once_with(flow_status)


@pytest.mark.integration
class TestCanFlowControlIntegration:
    """Integration tests for functions in CAN Flow Control module."""

    # create_flow_control_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "flow_status": CanFlowStatus.Overflow}, bytearray([0x32, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE])),
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
    def test_create_flow_control_data(self, kwargs, expected_raw_frame_data):
        assert create_flow_control_data(**kwargs) == expected_raw_frame_data

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
    def test_create_flow_control_data__value_error(self, kwargs):
        with pytest.raises(ValueError):
            create_flow_control_data(**kwargs)

    # generate_flow_control_data

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
    def test_generate_flow_control_data(self, kwargs, expected_raw_frame_data):
        assert generate_flow_control_data(**kwargs) == expected_raw_frame_data

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
    def test_generate_flow_control_data__value_error(self, kwargs):
        with pytest.raises(ValueError):
            generate_flow_control_data(**kwargs)

    # validate_flow_control_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x30, 0x12, 0x34]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x31, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xA1, 0x32, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0xBC, 0x30, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x90, 0x30, 0x17, 0xFE] + ([0xCC] * 60)),
    ])
    def test_validate_frame_data(self, addressing_format, raw_frame_data):
        assert validate_flow_control_data(addressing_format=addressing_format,
                                          raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x30, 0x12]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x31, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xA1, 0x32, 0xCC)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0xBC, 0x34, 0xCC, 0xCC)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x90, 0x30, 0x17, 0xFE] + ([0xCC] * 59)),
    ])
    def test_validate_frame_data__value_error(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            validate_flow_control_data(addressing_format=addressing_format,
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
        (0, 0x55),
        (0xAA, 0x12)
    ])
    def test_next__no_wait(self, block_size, st_min):
        self.mock_flow_control_parameters_generator._remaining_wait = None
        self.mock_flow_control_parameters_generator.block_size = block_size
        self.mock_flow_control_parameters_generator.st_min = st_min
        assert (DefaultFlowControlParametersGenerator.__next__(self.mock_flow_control_parameters_generator) ==
                (CanFlowStatus.ContinueToSend, block_size, st_min))
        assert self.mock_flow_control_parameters_generator._remaining_wait is None

    @pytest.mark.parametrize("block_size, st_min", [
        (0, 0x55),
        (0xAA, 0x12)
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
        (0, 0x55, 1),
        (0xAA, 0x12, 54)
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

    def test_block_size__get(self):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__block_size = Mock()
        assert (DefaultFlowControlParametersGenerator.block_size.fget(self.mock_flow_control_parameters_generator)
                == self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__block_size)

    @pytest.mark.parametrize("value", [0x5A, Mock()])
    def test_block_size__set(self, value):
        DefaultFlowControlParametersGenerator.block_size.fset(self.mock_flow_control_parameters_generator, value)
        assert self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__block_size == value
        self.mock_validate_raw_byte.assert_called_once_with(value)

    # st_min

    def test_st_min__get(self):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__st_min = Mock()
        assert (DefaultFlowControlParametersGenerator.st_min.fget(self.mock_flow_control_parameters_generator)
                == self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__st_min)

    @pytest.mark.parametrize("value", [0x5A, Mock()])
    def test_st_min__set(self, value):
        DefaultFlowControlParametersGenerator.st_min.fset(self.mock_flow_control_parameters_generator, value)
        assert self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__st_min == value
        self.mock_validate_raw_byte.assert_called_once_with(value)

    # wait_count

    def test_wait_count__get(self):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__wait_count = Mock()
        assert (DefaultFlowControlParametersGenerator.wait_count.fget(self.mock_flow_control_parameters_generator)
                == self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__wait_count)

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_wait_count__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            DefaultFlowControlParametersGenerator.wait_count.fset(self.mock_flow_control_parameters_generator, value)
        mock_isinstance.assert_called_once_with(value, int)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_wait_count__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_lt = Mock(return_value=True)
        mock_value = MagicMock(__lt__=mock_lt)
        with pytest.raises(ValueError):
            DefaultFlowControlParametersGenerator.wait_count.fset(self.mock_flow_control_parameters_generator,
                                                                  mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)
        mock_lt.assert_called_once_with(0)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_wait_count__set__valid(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_lt = Mock(return_value=False)
        mock_value = MagicMock(__lt__=mock_lt)
        DefaultFlowControlParametersGenerator.wait_count.fset(self.mock_flow_control_parameters_generator, mock_value)
        assert (self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__wait_count
                == mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)
        mock_lt.assert_called_once_with(0)
        
    # repeat_wait

    def test_repeat_wait__get(self):
        self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__repeat_wait = Mock()
        assert (DefaultFlowControlParametersGenerator.repeat_wait.fget(self.mock_flow_control_parameters_generator)
                == self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__repeat_wait)

    @patch(f"{SCRIPT_LOCATION}.bool")
    def test_repeat_wait__set(self, mock_bool):
        mock_value = Mock()
        DefaultFlowControlParametersGenerator.repeat_wait.fset(self.mock_flow_control_parameters_generator, mock_value)
        assert (self.mock_flow_control_parameters_generator._DefaultFlowControlParametersGenerator__repeat_wait
                == mock_bool.return_value)
        mock_bool.assert_called_once_with(mock_value)


@pytest.mark.integration
class TestDefaultFlowControlParametersGeneratorIntegration:
    """Integration tests for DefaultFlowControlParametersGenerator"""

    @pytest.mark.parametrize("init_params, following_fc_params", [
        (
            {},
            [
                (CanFlowStatus.ContinueToSend, 0, 0),
                (CanFlowStatus.ContinueToSend, 0, 0),
                (CanFlowStatus.ContinueToSend, 0, 0)
            ]
        ),
        (
            {
                "block_size": 2,
                "st_min": 125,
                "wait_count": 2,
                "repeat_wait": False,
            },
            [
                (CanFlowStatus.Wait, None, None),
                (CanFlowStatus.Wait, None, None),
                (CanFlowStatus.ContinueToSend, 2, 125),
                (CanFlowStatus.ContinueToSend, 2, 125),
                (CanFlowStatus.ContinueToSend, 2, 125),
            ]
        ),
        (
            {
                "block_size": 13,
                "st_min": 241,
                "wait_count": 1,
                "repeat_wait": True,
            },
            [
                (CanFlowStatus.Wait, None, None),
                (CanFlowStatus.ContinueToSend, 13, 241),
                (CanFlowStatus.Wait, None, None),
                (CanFlowStatus.ContinueToSend, 13, 241),
                (CanFlowStatus.Wait, None, None),
                (CanFlowStatus.ContinueToSend, 13, 241),
            ]
        ),
    ])
    def test_generate_params(self, init_params, following_fc_params):
        flow_control_generator = DefaultFlowControlParametersGenerator(**init_params)
        flow_control_iterator = iter(flow_control_generator)
        for fc_params in following_fc_params:
            assert next(flow_control_iterator) == fc_params

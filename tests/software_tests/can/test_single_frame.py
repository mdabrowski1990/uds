import pytest
from mock import patch

from uds.can.single_frame import CanSingleFrameDataLengthHandler, \
    CanPacketType, CanAddressingFormat, InconsistentArgumentsError


class TestCanSingleFrameDataLengthHandler:
    """Tests for `CanSingleFrameDataLengthHandler` class."""

    SCRIPT_LOCATION = "uds.can.single_frame"

    def setup(self):
        self._patcher_validate_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_dlc = self._patcher_validate_dlc.start()
        self._patcher_encode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.encode")
        self.mock_encode_dlc = self._patcher_encode_dlc.start()
        self._patcher_decode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.decode")
        self.mock_decode_dlc = self._patcher_decode_dlc.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_int_to_bytes_list = patch(f"{self.SCRIPT_LOCATION}.int_to_bytes_list")
        self.mock_int_to_bytes_list = self._patcher_int_to_bytes_list.start()
        self._patcher_bytes_list_to_int = patch(f"{self.SCRIPT_LOCATION}.bytes_list_to_int")
        self.mock_bytes_list_to_int = self._patcher_bytes_list_to_int.start()
        self._patcher_validate_nibble = patch(f"{self.SCRIPT_LOCATION}.validate_nibble")
        self.mock_validate_nibble = self._patcher_validate_nibble.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown(self):
        self._patcher_validate_dlc.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_int_to_bytes_list.stop()
        self._patcher_bytes_list_to_int.stop()
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()

    # encode_sf_dl

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
    @pytest.mark.parametrize("valid_sf_dl, addressing_format", [
        (True, "some addressing format"),
        (False, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.validate_sf_dl")
    def test_encode_sf_dl__short(self, mock_validate_sf_dl, sf_dl, dlc, valid_sf_dl, addressing_format):
        assert CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl,
                                                            valid_sf_dl=valid_sf_dl,
                                                            addressing_format=addressing_format,
                                                            dlc=dlc) == self.mock_int_to_bytes_list.return_value
        self.mock_int_to_bytes_list.assert_called_once_with(
            int_value=sf_dl, list_size=CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED)
        self.mock_int_to_bytes_list.return_value.__getitem__.assert_called_once_with(0)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    valid_sf_dl=valid_sf_dl,
                                                    addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    @pytest.mark.parametrize("valid_sf_dl, addressing_format", [
        (True, "some addressing format"),
        (False, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.validate_sf_dl")
    def test_encode_sf_dl__long(self, mock_validate_sf_dl, sf_dl, dlc, valid_sf_dl, addressing_format):
        assert CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl,
                                                            valid_sf_dl=valid_sf_dl,
                                                            addressing_format=addressing_format,
                                                            dlc=dlc) == self.mock_int_to_bytes_list.return_value
        self.mock_int_to_bytes_list.assert_called_once_with(
            int_value=sf_dl, list_size=CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED)
        self.mock_int_to_bytes_list.return_value.__getitem__.assert_called_once_with(0)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    valid_sf_dl=valid_sf_dl,
                                                    addressing_format=addressing_format)

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(8)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("ai_data_bytes", [0, 1])
    @pytest.mark.parametrize("dlc", [CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_single_frame")
    def test_decode_sf_dl__short(self, mock_validate_validate_single_frame,
                                 addressing_format, raw_frame_data, ai_data_bytes, dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_encode_dlc.return_value = dlc
        assert CanSingleFrameDataLengthHandler.decode_sf_dl(addressing_format=addressing_format,
                                                            raw_frame_data=raw_frame_data) == self.mock_bytes_list_to_int.return_value
        sf_dl_data_bytes = list(raw_frame_data[ai_data_bytes:][:CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED])
        sf_dl_data_bytes[0] -= (CanPacketType.SINGLE_FRAME.value << 4)
        self.mock_bytes_list_to_int.assert_called_once_with(bytes_list=sf_dl_data_bytes)
        mock_validate_validate_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                            raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(8)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("ai_data_bytes", [0, 1])
    @pytest.mark.parametrize("dlc", [CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_single_frame")
    def test_decode_sf_dl__long(self, mock_validate_validate_single_frame,
                                addressing_format, raw_frame_data, ai_data_bytes, dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_encode_dlc.return_value = dlc
        assert CanSingleFrameDataLengthHandler.decode_sf_dl(addressing_format=addressing_format,
                                                            raw_frame_data=raw_frame_data) == self.mock_bytes_list_to_int.return_value
        sf_dl_data_bytes = list(raw_frame_data[ai_data_bytes:][:CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED])
        sf_dl_data_bytes[0] -= (CanPacketType.SINGLE_FRAME.value << 4)
        self.mock_bytes_list_to_int.assert_called_once_with(bytes_list=sf_dl_data_bytes)
        mock_validate_validate_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                            raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))

    # validate_sf_dl

    @pytest.mark.parametrize("sf_dl", ["some SF_DL", 6])
    @pytest.mark.parametrize("dlc", [0, 8, 9, 0xF])
    def test_validate_sf_dl__valid_loose_check(self, sf_dl, dlc):
        CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, valid_sf_dl=False)
        self.mock_validate_dlc.assert_called_once_with(dlc)
        if dlc <= CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            self.mock_validate_nibble.assert_called_once_with(sf_dl)
            self.mock_validate_raw_byte.assert_not_called()
        else:
            self.mock_validate_raw_byte.assert_called_once_with(sf_dl)
            self.mock_validate_nibble.assert_not_called()

    @pytest.mark.parametrize("sf_dl, dlc, frame_bytes_number", [
        (0, 6, 1),
        (2, 8, 8),
        (7, 8, 8),
        (13, 0xA, 15),
        (13, 0xF, 64),
        (62, 0xF, 64),
    ])
    def test_validate_sf_dl__valid_strict_check_without_addressing_format(self, sf_dl, dlc, frame_bytes_number):
        self.mock_decode_dlc.return_value = frame_bytes_number
        CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        if dlc <= CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            self.mock_validate_nibble.assert_called_once_with(sf_dl)
            self.mock_validate_raw_byte.assert_not_called()
        else:
            self.mock_validate_raw_byte.assert_called_once_with(sf_dl)
            self.mock_validate_nibble.assert_not_called()

    @pytest.mark.parametrize("sf_dl, dlc, frame_bytes_number, ai_data_bytes", [
        (0, 6, 1, 0),
        (2, 8, 8, 1),
        (6, 8, 8, 1),
        (13, 0xA, 15, 0),
        (13, 0xF, 64, 1),
        (61, 0xF, 64, 1),
    ])
    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    def test_validate_sf_dl__valid_strict_check_with_addressing_format(self, sf_dl, dlc, addressing_format,
                                                                       frame_bytes_number, ai_data_bytes):
        self.mock_decode_dlc.return_value = frame_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl,
                                                       dlc=dlc,
                                                       valid_sf_dl=True,
                                                       addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        if dlc <= CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            self.mock_validate_nibble.assert_called_once_with(sf_dl)
            self.mock_validate_raw_byte.assert_not_called()
        else:
            self.mock_validate_raw_byte.assert_called_once_with(sf_dl)
            self.mock_validate_nibble.assert_not_called()

    @pytest.mark.parametrize("sf_dl, dlc, frame_bytes_number", [
        (1, 6, 1),
        (8, 8, 8),
        (12, 8, 8),
        (12, 9, 12),
        (14, 0xA, 15),
        (16, 0xA, 15),
        (63, 0xF, 64),
    ])
    def test_validate_sf_dl__invalid_strict_without_addressing_format(self, sf_dl, dlc, frame_bytes_number):
        self.mock_decode_dlc.return_value = frame_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        if dlc <= CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            self.mock_validate_nibble.assert_called_once_with(sf_dl)
            self.mock_validate_raw_byte.assert_not_called()
        else:
            self.mock_validate_raw_byte.assert_called_once_with(sf_dl)
            self.mock_validate_nibble.assert_not_called()

    @pytest.mark.parametrize("sf_dl, dlc, frame_bytes_number, ai_data_bytes", [
        (1, 6, 1, 0),
        (8, 6, 1, 1),
        (7, 8, 8, 1),
        (8, 8, 8, 0),
        (14, 0xA, 15, 0),
        (62, 0xF, 64, 1),
        (128, 0xF, 64, 0),
    ])
    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    def test_validate_sf_dl__invalid_strict_with_addressing_format(self, sf_dl, dlc, addressing_format,
                                                                   frame_bytes_number, ai_data_bytes):
        self.mock_decode_dlc.return_value = frame_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl,
                                                           dlc=dlc,
                                                           valid_sf_dl=True,
                                                           addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        if dlc <= CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            self.mock_validate_nibble.assert_called_once_with(sf_dl)
            self.mock_validate_raw_byte.assert_not_called()
        else:
            self.mock_validate_raw_byte.assert_called_once_with(sf_dl)
            self.mock_validate_nibble.assert_not_called()


@pytest.mark.integration
class TestCanSingleFrameDataLengthHandlerIntegration:
    """Integration tests for `CanSingleFrameDataLengthHandler` class."""

    # encode_sf_dl

    @pytest.mark.parametrize("sf_dl, dlc, expected_sf_dl_data_bytes", [
        # short
        (0x0, 1, [0x00]),
        (0x8, 2, [0x08]),
        (0x9, 6, [0x09]),
        (0xF, 8, [0x0F]),
        # long
        (0x0, 0x9, [0x00, 0x00]),
        (0x8, 0xA, [0x00, 0x08]),
        (0x12, 0xD, [0x00, 0x12]),
        (0x3E, 0xF, [0x00, 0x3E]),
        (0xFF, 0xF, [0x00, 0xFF]),
    ])
    def test_encode_sf_dl(self, sf_dl, dlc, expected_sf_dl_data_bytes):
        assert CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl, dlc=dlc, valid_sf_dl=False) == expected_sf_dl_data_bytes

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data, expected_sf_dl", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, (0x01, 0x23), 1),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF], 1),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B], 5),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x0A, 0x00, 0x3D] + list(range(100, 161)), 0x3D),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xF0, 0x00, 0x0B] + list(range(50, 95)), 0xB),
    ])
    def test_decode_sf_dl(self, addressing_format, raw_frame_data, expected_sf_dl):
        assert CanSingleFrameDataLengthHandler.decode_sf_dl(addressing_format=addressing_format,
                                                            raw_frame_data=raw_frame_data) == expected_sf_dl

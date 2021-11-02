import pytest
from mock import patch

from uds.can.single_frame import CanSingleFrameHandler, _CanSingleFrameDataLengthHandler, _CanSingleFrameHandler, \
    CanPacketType, CanAddressingFormat, InconsistentArgumentsError, CanDlcHandler, DEFAULT_FILLER_BYTE


class TestCanSingleFrameHandler:
    """Tests for `CanSingleFrameHandler` class."""

    SCRIPT_LOCATION = "uds.can.single_frame"

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

        # self._patcher_get_ai_data_bytes_number = \
        #     patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        # self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        # self._patcher_int_to_bytes_list = patch(f"{self.SCRIPT_LOCATION}.int_to_bytes_list")
        # self.mock_int_to_bytes_list = self._patcher_int_to_bytes_list.start()
        # self._patcher_bytes_list_to_int = patch(f"{self.SCRIPT_LOCATION}.bytes_list_to_int")
        # self.mock_bytes_list_to_int = self._patcher_bytes_list_to_int.start()
        # self._patcher_validate_nibble = patch(f"{self.SCRIPT_LOCATION}.validate_nibble")
        # self.mock_validate_nibble = self._patcher_validate_nibble.start()

    def teardown(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_min_dlc.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()

        # self._patcher_validate_dlc.stop()
        # self._patcher_get_ai_data_bytes_number.stop()
        # self._patcher_int_to_bytes_list.stop()
        # self._patcher_bytes_list_to_int.stop()
        # self._patcher_validate_nibble.stop()

    # create_can_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.encode_sf_dl")
    def test_generate_can_frame_data__with_dlc(self, mock_encode_sf_dl,
                                               addressing_format, target_address, address_extension,
                                               payload, dlc, filler_byte, data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        sf_frame_data = CanSingleFrameHandler.create_can_frame_data(addressing_format=addressing_format,
                                                                    payload=payload,
                                                                    dlc=dlc,
                                                                    filler_byte=filler_byte,
                                                                    target_address=target_address,
                                                                    address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        assert isinstance(sf_frame_data, list)
        assert len(sf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_dlc")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.encode_sf_dl")
    def test_generate_can_frame_data__without_dlc(self, mock_encode_sf_dl, mock_get_dlc,
                                                  addressing_format, target_address, address_extension,
                                                  payload, dlc, filler_byte, data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        mock_get_dlc.return_value = dlc
        sf_frame_data = CanSingleFrameHandler.create_can_frame_data(addressing_format=addressing_format,
                                                                    payload=payload,
                                                                    dlc=None,
                                                                    filler_byte=filler_byte,
                                                                    target_address=target_address,
                                                                    address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_get_dlc.assert_called_once_with(addressing_format=addressing_format,
                                             payload_length=len(payload))
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        assert isinstance(sf_frame_data, list)
        assert len(sf_frame_data) == data_bytes_number

    # is_single_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_data_bytes", [
        ("some addressing", "some raw frame", [0x00]),
        ("some other addressing", "some other raw frame", [0x06]),
        ("Mixed", range(20), [0x00, 0x12]),
        ("Extended", [0x10, 0x20, 0x30], [0x0F, 0xED]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    def test_is_single_frame__true(self, mock_extract_sf_dl_data_bytes,
                                   addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        assert CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is True
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data, sf_dl_data_bytes", [
        ("some addressing", "some raw frame", [0x10]),
        ("some other addressing", "some other raw frame", [0x26]),
        ("Mixed", range(20), [0xF0, 0x12]),
        ("Extended", [0x10, 0x20, 0x30], [0x8F, 0xED]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.extract_sf_dl_data_bytes")
    def test_is_single_frame__false(self, mock_extract_sf_dl_data_bytes,
                                    addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        assert CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is False
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # get_dlc

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 0),
        (1, 7),
        (0, 15),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                             _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__short_dlc(self, mock_validate_payload_length,
                                                       addressing_format, payload_length, ai_data_bytes,
                                                       decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanSingleFrameHandler.get_dlc(addressing_format=addressing_format,
                                             payload_length=payload_length) == self.mock_get_min_dlc.return_value
        data_bytes_number = payload_length + _CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_once_with(data_bytes_number)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 0),
        (1, 7),
        (0, 15),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                             _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 5])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__long_dlc(self, mock_validate_payload_length,
                                                      addressing_format, payload_length, ai_data_bytes,
                                                      decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanSingleFrameHandler.get_dlc(addressing_format=addressing_format,
                                             payload_length=payload_length) == self.mock_get_min_dlc.return_value
        data_bytes_number = payload_length + _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_with(data_bytes_number)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)

    # encode_sf_dl

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.create_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_encode_sf_dl__short(self, mock_validate_sf_dl, mock_generate_sf_dl_data_bytes,
                                 sf_dl, dlc, addressing_format):
        assert CanSingleFrameHandler.encode_sf_dl(sf_dl=sf_dl,
                                                  addressing_format=addressing_format,
                                                  dlc=dlc) == mock_generate_sf_dl_data_bytes.return_value
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    addressing_format=addressing_format)
        mock_generate_sf_dl_data_bytes.assert_called_once_with(sf_dl_short=sf_dl)

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.create_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_encode_sf_dl__long(self, mock_validate_sf_dl, mock_generate_sf_dl_data_bytes,
                                sf_dl, dlc, addressing_format):
        assert CanSingleFrameHandler.encode_sf_dl(sf_dl=sf_dl,
                                                  addressing_format=addressing_format,
                                                  dlc=dlc) == mock_generate_sf_dl_data_bytes.return_value
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    addressing_format=addressing_format)
        mock_generate_sf_dl_data_bytes.assert_called_once_with(sf_dl_long=sf_dl)

    # create_sf_dl_data_bytes

    @pytest.mark.parametrize("sf_dl_short", [0, 7, 0xF])
    def test_create_sf_dl_data_bytes__short(self, sf_dl_short):
        assert CanSingleFrameHandler.create_sf_dl_data_bytes(sf_dl_short=sf_dl_short) == \
               [(CanPacketType.SINGLE_FRAME.value << 4) + sf_dl_short]
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("sf_dl_short", [0, 7, 0xF])
    @pytest.mark.parametrize("sf_dl_long", [0, 7, 0xF])
    def test_create_sf_dl_data_bytes__long(self, sf_dl_short, sf_dl_long):
        assert CanSingleFrameHandler.create_sf_dl_data_bytes(sf_dl_short=sf_dl_short, sf_dl_long=sf_dl_long) == \
               [(CanPacketType.SINGLE_FRAME.value << 4) + sf_dl_short, sf_dl_long]
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_called_once_with(sf_dl_long)


@pytest.mark.integration
class TestCanSingleFrameHandlerIntegration:
    """Integration tests for `CanSingleFrameHandler` class."""

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "payload": [0x3E]},
         [0x01, 0x3E]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": [0x3E],
          "dlc": 8,
          "target_address": 0xFF},
         [0x01, 0x3E] + ([DEFAULT_FILLER_BYTE] * 6)),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "payload": list(range(54)),
          "filler_byte": 0x66,
          "target_address": 0xF2},
         [0xF2, 0x00, 0x36] + list(range(54)) + ([0x66] * 7)),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
          "dlc": 8,
          "filler_byte": 0x66,
          "address_extension": 0x12},
         [0x12, 0x06, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01],
          "filler_byte": 0x99,
          "target_address": 0xF2,
          "address_extension": 0x12},
         [0x12, 0x00, 0x07, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01, 0x99, 0x99]),
    ])
    def test_generate_can_frame_data(self, kwargs, expected_raw_frame_data):
        assert CanSingleFrameHandler.create_can_frame_data(**kwargs) == expected_raw_frame_data


class _TestCanSingleFrameDataLengthHandler:
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
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()

    def teardown(self):
        self._patcher_validate_dlc.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_int_to_bytes_list.stop()
        self._patcher_bytes_list_to_int.stop()
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()

    # encode_sf_dl

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
    @pytest.mark.parametrize("valid_sf_dl, addressing_format", [
        (True, "some addressing format"),
        (False, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.validate_sf_dl")
    def test_encode_sf_dl__short(self, mock_validate_sf_dl, sf_dl, dlc, valid_sf_dl, addressing_format):
        assert _CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl,
                                                             valid_sf_dl=valid_sf_dl,
                                                             addressing_format=addressing_format,
                                                             dlc=dlc) == self.mock_int_to_bytes_list.return_value
        self.mock_int_to_bytes_list.assert_called_once_with(
            int_value=sf_dl, list_size=_CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED)
        self.mock_int_to_bytes_list.return_value.__getitem__.assert_called_once_with(0)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    valid_sf_dl=valid_sf_dl,
                                                    addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    @pytest.mark.parametrize("valid_sf_dl, addressing_format", [
        (True, "some addressing format"),
        (False, None),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.validate_sf_dl")
    def test_encode_sf_dl__long(self, mock_validate_sf_dl, sf_dl, dlc, valid_sf_dl, addressing_format):
        assert _CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl,
                                                             valid_sf_dl=valid_sf_dl,
                                                             addressing_format=addressing_format,
                                                             dlc=dlc) == self.mock_int_to_bytes_list.return_value
        self.mock_int_to_bytes_list.assert_called_once_with(
            int_value=sf_dl, list_size=_CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED)
        self.mock_int_to_bytes_list.return_value.__getitem__.assert_called_once_with(0)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    valid_sf_dl=valid_sf_dl,
                                                    addressing_format=addressing_format)

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(8)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("sf_dl_data_bytes", [[0x05], [0x10, 0x06], [0xfE]])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.extract_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_frame_data")
    def test_decode_sf_dl(self, mock_validate_frame_data, mock_extract_sf_dl_data_bytes,
                          addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        assert _CanSingleFrameDataLengthHandler.decode_sf_dl(addressing_format=addressing_format,
                                                             raw_frame_data=raw_frame_data) == self.mock_bytes_list_to_int.return_value
        mock_validate_frame_data.assert_called_once_with(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        sf_dl_data_bytes[0] ^= (CanPacketType.SINGLE_FRAME.value << 4)
        self.mock_bytes_list_to_int.assert_called_once_with(bytes_list=sf_dl_data_bytes)

    # extract_sf_dl_data_bytes

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        ("some addressing format", 0),
        ("another format", 1),
    ])
    @pytest.mark.parametrize("raw_frame_data", [range(10), range(10, 16)])
    @pytest.mark.parametrize("dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    def test_extract_sf_dl_data_bytes(self, addressing_format, raw_frame_data, dlc, ai_data_bytes):
        self.mock_encode_dlc.return_value = dlc
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        sf_dl_bytes = _CanSingleFrameDataLengthHandler.extract_sf_dl_data_bytes(addressing_format=addressing_format,
                                                                                raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        assert isinstance(sf_dl_bytes, list)
        if dlc <= _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            assert len(sf_dl_bytes) == _CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED
            assert sf_dl_bytes == list(raw_frame_data)[ai_data_bytes:][:_CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED]
        else:
            assert len(sf_dl_bytes) == _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED
            assert sf_dl_bytes == list(raw_frame_data)[ai_data_bytes:][:_CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED]

    # validate_sf_dl

    @pytest.mark.parametrize("sf_dl", ["some SF_DL", 6])
    @pytest.mark.parametrize("dlc", [0, 8, 9, 0xF])
    def test_validate_sf_dl__valid_loose_check(self, sf_dl, dlc):
        _CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, valid_sf_dl=False)
        self.mock_validate_dlc.assert_called_once_with(dlc)
        if dlc <= _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
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
        _CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        if dlc <= _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
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
        _CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl,
                                                        dlc=dlc,
                                                        valid_sf_dl=True,
                                                        addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        if dlc <= _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
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
            _CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        if dlc <= _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
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
            _CanSingleFrameDataLengthHandler.validate_sf_dl(sf_dl=sf_dl,
                                                            dlc=dlc,
                                                            valid_sf_dl=True,
                                                            addressing_format=addressing_format)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        if dlc <= _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL:
            self.mock_validate_nibble.assert_called_once_with(sf_dl)
            self.mock_validate_raw_byte.assert_not_called()
        else:
            self.mock_validate_raw_byte.assert_called_once_with(sf_dl)
            self.mock_validate_nibble.assert_not_called()

    # validate_sf_dl_data_bytes

    @pytest.mark.parametrize("dlc, sf_dl_bytes, sf_dl", [
        (2, [0x01], 1),
        (8, [0x06], 6),
        (9, [0x00, 0x12], 0x12),
        (15, [0x00, 0x3A], 0x3A),
    ])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.validate_sf_dl")
    def test_validate_sf_dl_data_bytes__valid(self, mock_validate_sf_dl,
                                              sf_dl_bytes, sf_dl, dlc, addressing_format):
        _CanSingleFrameDataLengthHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                                   dlc=dlc,
                                                                   addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("dlc, sf_dl_bytes", [
        (2, [0x00, 0x12]),
        (8, [0x00, 0x06]),
        (9, [0x0A]),
        (15, [0x0F]),
    ])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    def test_validate_sf_dl_data_bytes__invalid_length(self, sf_dl_bytes, dlc, addressing_format):
        with pytest.raises(InconsistentArgumentsError):
            _CanSingleFrameDataLengthHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                                       dlc=dlc,
                                                                       addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)

    @pytest.mark.parametrize("dlc, sf_dl_bytes", [
        (9, [0x01, 0x3E]),
        (0x10, [0x0A, 0x12]),
        (0xF, [0x0F, 0x02]),
    ])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    def test_validate_sf_dl_data_bytes__invalid_byte_zero(self, sf_dl_bytes, dlc, addressing_format):
        with pytest.raises(ValueError):
            _CanSingleFrameDataLengthHandler.validate_sf_dl_data_bytes(sf_dl_bytes=sf_dl_bytes,
                                                                       dlc=dlc,
                                                                       addressing_format=addressing_format)
        self.mock_validate_raw_bytes.assert_called_once_with(sf_dl_bytes)


@pytest.mark.integration
class _TestCanSingleFrameDataLengthHandlerIntegration:
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
        assert _CanSingleFrameDataLengthHandler.encode_sf_dl(sf_dl=sf_dl, dlc=dlc, valid_sf_dl=False) == expected_sf_dl_data_bytes

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data, expected_sf_dl", [
        (CanAddressingFormat.NORMAL_11BIT_ADDRESSING, (0x01, 0x23), 1),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF], 1),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B], 5),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x0A, 0x00, 0x3D] + list(range(100, 161)), 0x3D),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xF0, 0x00, 0x0B] + list(range(50, 95)), 0xB),
    ])
    def test_decode_sf_dl(self, addressing_format, raw_frame_data, expected_sf_dl):
        assert _CanSingleFrameDataLengthHandler.decode_sf_dl(addressing_format=addressing_format,
                                                             raw_frame_data=raw_frame_data) == expected_sf_dl


class _TestCanSingleFrameHandler:
    """Tests for `CanSingleFrameHandler` class."""

    SCRIPT_LOCATION = _TestCanSingleFrameDataLengthHandler.SCRIPT_LOCATION

    def setup(self):
        self._patcher_encode_sf_dl = patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.encode_sf_dl")
        self.mock_encode_sf_dl = self._patcher_encode_sf_dl.start()
        self._patcher_extract_sf_dl_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.extract_sf_dl_data_bytes")
        self.mock_extract_sf_dl_data_bytes = self._patcher_extract_sf_dl_data_bytes.start()
        self._patcher_validate_sf_dl_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameDataLengthHandler.validate_sf_dl_data_bytes")
        self.mock_validate_sf_dl_data_bytes = self._patcher_validate_sf_dl_data_bytes.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()
        self._patcher_generate_ai_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.generate_ai_data_bytes")
        self.mock_generate_ai_data_bytes = self._patcher_generate_ai_data_bytes.start()
        self._patcher_get_min_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.get_min_dlc")
        self.mock_get_min_dlc = self._patcher_get_min_dlc.start()
        self._patcher_decode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.decode")
        self.mock_decode_dlc = self._patcher_decode_dlc.start()
        self._patcher_encode_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.encode")
        self.mock_encode_dlc = self._patcher_encode_dlc.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_validate_raw_bytes = patch(f"{self.SCRIPT_LOCATION}.validate_raw_bytes")
        self.mock_validate_raw_bytes = self._patcher_validate_raw_bytes.start()

    def teardown(self):
        self._patcher_encode_sf_dl.stop()
        self._patcher_extract_sf_dl_data_bytes.stop()
        self._patcher_validate_sf_dl_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()
        self._patcher_generate_ai_data_bytes.stop()
        self._patcher_get_min_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()

    # generate_can_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    def test_generate_can_frame_data__with_dlc(self, addressing_format, target_address, address_extension,
                                               payload, dlc, filler_byte, data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_generate_ai_data_bytes.return_value = ai_bytes
        self.mock_encode_sf_dl.return_value = sf_dl_bytes
        sf_frame_data = _CanSingleFrameHandler.generate_can_frame_data(addressing_format=addressing_format,
                                                                       payload=payload,
                                                                       dlc=dlc,
                                                                       filler_byte=filler_byte,
                                                                       target_address=target_address,
                                                                       address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_generate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                                 target_address=target_address,
                                                                 address_extension=address_extension)
        self.mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                       dlc=dlc,
                                                       addressing_format=addressing_format)
        data_padding_index = len(ai_bytes) + len(sf_dl_bytes) + len(payload)
        assert isinstance(sf_frame_data, list)
        assert len(sf_frame_data) == data_bytes_number
        assert sf_frame_data[:data_padding_index] == list(ai_bytes) + list(sf_dl_bytes) + list(payload)
        assert all(padded_byte == filler_byte for padded_byte in sf_frame_data[data_padding_index:])

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_dlc")
    def test_generate_can_frame_data__without_dlc(self, mock_get_dlc,
                                                  addressing_format, target_address, address_extension,
                                                  payload, dlc, filler_byte, data_bytes_number, ai_bytes, sf_dl_bytes):
        mock_get_dlc.return_value = dlc
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_generate_ai_data_bytes.return_value = ai_bytes
        self.mock_encode_sf_dl.return_value = sf_dl_bytes
        sf_frame_data = _CanSingleFrameHandler.generate_can_frame_data(addressing_format=addressing_format,
                                                                       payload=payload,
                                                                       dlc=None,
                                                                       filler_byte=filler_byte,
                                                                       target_address=target_address,
                                                                       address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        mock_get_dlc.assert_called_once_with(addressing_format=addressing_format,
                                             payload_length=len(payload))
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_generate_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                                 target_address=target_address,
                                                                 address_extension=address_extension)
        self.mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                       dlc=dlc,
                                                       addressing_format=addressing_format)
        data_padding_index = len(ai_bytes) + len(sf_dl_bytes) + len(payload)
        assert isinstance(sf_frame_data, list)
        assert len(sf_frame_data) == data_bytes_number
        assert sf_frame_data[:data_padding_index] == list(ai_bytes) + list(sf_dl_bytes) + list(payload)
        assert all(padded_byte == filler_byte for padded_byte in sf_frame_data[data_padding_index:])

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data", ["some raw bbytes", range(6)])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__invalid(self, mock_is_single_frame, addressing_format, raw_frame_data):
        mock_is_single_frame.return_value = False
        with pytest.raises(ValueError):
            _CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                       raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data", ["some raw bbytes", range(6)])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__valid(self, mock_is_single_frame, addressing_format, raw_frame_data):
        mock_is_single_frame.return_value = True
        _CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                   raw_frame_data=raw_frame_data)
        mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        self.mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                                   raw_frame_data=raw_frame_data)
        self.mock_validate_sf_dl_data_bytes.assert_called_once_with(
            sf_dl_bytes=self.mock_extract_sf_dl_data_bytes.return_value,
            dlc=self.mock_encode_dlc.return_value,
            addressing_format=addressing_format)

    # is_single_frame

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes", [
        ("some addressing format", (0x01, 0x23, 0x45, 0x67, 0x89, 0xAB), 0),
        ("xyz", (0xAB, 0x05, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5), 1),
        ("another addressing format", [0xFF, 0x00, 0x25] + list(range(100, 161)), 1),
        ("abc", [0x00], 0),
    ])
    def test_is_single_frame__true(self, addressing_format, raw_frame_data, ai_data_bytes):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        assert _CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data) is True
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format, raw_frame_data, ai_data_bytes", [
        ("some addressing format", (0x11, 0x23, 0x45, 0x67, 0x89, 0xAB), 0),
        ("xyz", (0xAB, 0x25, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5), 1),
        ("another addressing format", [0xFF, 0x30, 0x25] + list(range(100, 161)), 1),
        ("abc", [0x00], 1),
    ])
    def test_is_single_frame__false(self, addressing_format, raw_frame_data, ai_data_bytes):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        assert _CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data) is False
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # get_dlc

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 0),
        (1, 7),
        (0, 15),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                             _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL - 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__short_dlc(self, mock_validate_payload_length,
                                                       addressing_format, payload_length, ai_data_bytes, decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert _CanSingleFrameHandler.get_dlc(addressing_format=addressing_format,
                                              payload_length=payload_length) == self.mock_get_min_dlc.return_value
        data_bytes_number = payload_length + _CanSingleFrameDataLengthHandler.SHORT_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_once_with(data_bytes_number)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 0),
        (1, 7),
        (0, 15),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [_CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                             _CanSingleFrameDataLengthHandler.MAX_DLC_VALUE_SHORT_SF_DL + 5])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__long_dlc(self, mock_validate_payload_length,
                                                      addressing_format, payload_length, ai_data_bytes, decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert _CanSingleFrameHandler.get_dlc(addressing_format=addressing_format,
                                              payload_length=payload_length) == self.mock_get_min_dlc.return_value
        data_bytes_number = payload_length + _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_with(data_bytes_number)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)

    # __validate_payload_length

    @pytest.mark.parametrize("payload_length", [None, 2.5, "wrong type"])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_validate_payload_length__type_error(self, payload_length, ai_data_bytes_number):
        with pytest.raises(TypeError):
            _CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(
                payload_length=payload_length, ai_data_bytes_number=ai_data_bytes_number)

    @pytest.mark.parametrize("payload_length", [-1, -2, -100])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_validate_payload_length__value_error(self, payload_length, ai_data_bytes_number):
        with pytest.raises(ValueError):
            _CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(
                payload_length=payload_length, ai_data_bytes_number=ai_data_bytes_number)

    @pytest.mark.parametrize("ai_data_bytes_number, payload_length", [
        (0, CanDlcHandler.MAX_DATA_BYTES_NUMBER - _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED + 1),
        (1, CanDlcHandler.MAX_DATA_BYTES_NUMBER - _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED),
        (2, CanDlcHandler.MAX_DATA_BYTES_NUMBER - _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED - 1),
        (0, CanDlcHandler.MAX_DATA_BYTES_NUMBER - _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED + 99),
    ])
    def test_validate_payload_length__inconsistent_arg_error(self, payload_length, ai_data_bytes_number):
        with pytest.raises(ValueError):
            _CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(
                payload_length=payload_length, ai_data_bytes_number=ai_data_bytes_number)

    @pytest.mark.parametrize("ai_data_bytes_number, payload_length", [
        (0, 0),
        (1, 0),
        (0, CanDlcHandler.MAX_DATA_BYTES_NUMBER - _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED),
        (1, CanDlcHandler.MAX_DATA_BYTES_NUMBER - _CanSingleFrameDataLengthHandler.LONG_SF_DL_BYTES_USED - 1),
    ])
    def test_validate_payload_length__valid(self, payload_length, ai_data_bytes_number):
        _CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
                                                                               ai_data_bytes_number=ai_data_bytes_number)


@pytest.mark.integration
class _TestCanSingleFrameHandlerIntegration:
    """Integration tests for `CanSingleFrameHandler` class."""

    # generate_can_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "payload": [0x3E]},
         [0x01, 0x3E]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": [0x3E],
          "dlc": 8,
          "target_address": 0xFF},
         [0x01, 0x3E] + ([DEFAULT_FILLER_BYTE] * 6)),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "payload": list(range(54)),
          "filler_byte": 0x66,
          "target_address": 0xF2},
         [0xF2, 0x00, 0x36] + list(range(54)) + ([0x66] * 7)),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
          "dlc": 8,
          "filler_byte": 0x66,
          "address_extension": 0x12},
         [0x12, 0x06, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01],
          "filler_byte": 0x99,
          "target_address": 0xF2,
          "address_extension": 0x12},
         [0x12, 0x00, 0x07, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01, 0x99, 0x99]),
    ])
    def test_generate_can_frame_data(self, kwargs, expected_raw_frame):
        assert _CanSingleFrameHandler.generate_can_frame_data(**kwargs) == expected_raw_frame

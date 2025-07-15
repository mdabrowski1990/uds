import pytest
from mock import patch

from uds.can import CanAddressingFormat
from uds.can.packet.single_frame import (
    DEFAULT_FILLER_BYTE,
    CanDlcHandler,
    CanSingleFrameHandler,
    InconsistentArgumentsError,
)

SCRIPT_LOCATION = "uds.addressing.single_frame"


class TestCanSingleFrameHandler:
    """Unit tests for `CanSingleFrameHandler` class."""

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
        self._patcher_validate_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_dlc = self._patcher_validate_dlc.start()
        self._patcher_encode_ai_data_bytes = \
            patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{SCRIPT_LOCATION}.CanAddressingInformation.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()

    def teardown_method(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_min_dlc.stop()
        self._patcher_validate_dlc.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()

    # create_valid_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        (CanDlcHandler.MIN_BASE_UDS_DLC, 0x66),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, bytearray(), bytearray([0xFA])),
        (range(50, 110), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl")
    def test_create_valid_frame_data__valid_with_dlc(self, mock_encode_sf_dl,
                                                     addressing_format, target_address, address_extension,
                                                     payload, dlc, filler_byte,
                                                     data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        sf_frame_data = CanSingleFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                      payload=payload,
                                                                      dlc=dlc,
                                                                      filler_byte=filler_byte,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        assert isinstance(sf_frame_data, bytearray)
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
        ([0x54], 2, bytearray(), bytearray([0xFA])),
        (range(50, 110), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl")
    def test_create_valid_frame_data__valid_without_dlc(self, mock_encode_sf_dl, mock_get_min_dlc,
                                                        addressing_format, target_address, address_extension,
                                                        payload, dlc, filler_byte, data_bytes_number, ai_bytes,
                                                        sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        mock_get_min_dlc.return_value = dlc
        sf_frame_data = CanSingleFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                      payload=payload,
                                                                      dlc=None,
                                                                      filler_byte=filler_byte,
                                                                      target_address=target_address,
                                                                      address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format,
                                                 payload_length=len(payload))
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)
        assert isinstance(sf_frame_data, bytearray)
        assert len(sf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("filler_byte", [0x66, 0x99])
    @pytest.mark.parametrize("dlc, payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        (CanDlcHandler.MIN_BASE_UDS_DLC - 1, range(60), 100, bytearray([0xFF]), bytearray([0x00, 0xFA])),
        (CanDlcHandler.MIN_BASE_UDS_DLC, [0x20, 0x30, 0x44], 3, bytearray(), bytearray([0x03])),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 1, range(20), 21, bytearray([0xAA]), bytearray([0x03])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl")
    def test_create_valid_frame_data__inconsistent_args(self, mock_encode_sf_dl,
                                                        addressing_format, target_address, address_extension,
                                                        payload, dlc, filler_byte,
                                                        data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_sf_dl.return_value = sf_dl_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                          payload=payload,
                                                          dlc=dlc,
                                                          filler_byte=filler_byte,
                                                          target_address=target_address,
                                                          address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_sf_dl.assert_called_once_with(sf_dl=len(payload),
                                                  dlc=dlc,
                                                  addressing_format=addressing_format)

    # create_any_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte", [
        ("some DLC", 0x66),
        (8, 0x99),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_bytes, sf_dl_bytes", [
        ([0x54], 2, bytearray(), bytearray([0xFA])),
        (range(50, 111), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
    ])
    @pytest.mark.parametrize("sf_dl_short, sf_dl_long", [
        (5, None),
        ("short", "long"),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl")
    def test_create_any_frame_data__valid(self, mock_encode_any_sf_dl,
                                          addressing_format, target_address, address_extension,
                                          payload, dlc, filler_byte, sf_dl_short, sf_dl_long,
                                          data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_any_sf_dl.return_value = sf_dl_bytes
        sf_frame_data = CanSingleFrameHandler.create_any_frame_data(addressing_format=addressing_format,
                                                                    payload=payload,
                                                                    dlc=dlc,
                                                                    sf_dl_short=sf_dl_short,
                                                                    sf_dl_long=sf_dl_long,
                                                                    filler_byte=filler_byte,
                                                                    target_address=target_address,
                                                                    address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_any_sf_dl.assert_called_once_with(sf_dl_short=sf_dl_short,
                                                      sf_dl_long=sf_dl_long)
        assert isinstance(sf_frame_data, bytearray)
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
        ([0x54], 2, bytearray([0x11]), bytearray([0xFA])),
        (range(50, 112), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
    ])
    @pytest.mark.parametrize("sf_dl_short, sf_dl_long", [
        (5, None),
        ("short", "long"),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl")
    def test_create_any_frame_data__inconsistent_args(self, mock_encode_any_sf_dl,
                                                      addressing_format, target_address, address_extension,
                                                      payload, dlc, filler_byte, sf_dl_short, sf_dl_long,
                                                      data_bytes_number, ai_bytes, sf_dl_bytes):
        self.mock_encode_ai_data_bytes.return_value = ai_bytes
        self.mock_decode_dlc.return_value = data_bytes_number
        mock_encode_any_sf_dl.return_value = sf_dl_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.create_any_frame_data(addressing_format=addressing_format,
                                                        payload=payload,
                                                        dlc=dlc,
                                                        sf_dl_short=sf_dl_short,
                                                        sf_dl_long=sf_dl_long,
                                                        filler_byte=filler_byte,
                                                        target_address=target_address,
                                                        address_extension=address_extension)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        mock_encode_any_sf_dl.assert_called_once_with(sf_dl_short=sf_dl_short,
                                                      sf_dl_long=sf_dl_long)

    # is_single_frame

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, ai_bytes_number", [
        ([0x01, 0xFE, 0xDC], 0),
        ([0xFE, 0x05, 0xDC, 0xBA, 0x98, 0x76, 0x54], 1),
    ])
    def test_is_single_frame__true(self, addressing_format, raw_frame_data, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is True
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, ai_bytes_number", [
        ([0x01, 0xFE, 0xDC], 1),
        ([0xFE, 0x15, 0xDC, 0xBA, 0x98, 0x76, 0x54], 1),
    ])
    def test_is_single_frame__false(self, addressing_format, raw_frame_data, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanSingleFrameHandler.is_single_frame(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data) is False
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # decode_payload

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, sf_dl, sf_dl_bytes_number, ai_bytes_number", [
        (range(8), 4, 1, 0),
        (tuple(range(10, 74)), 20, 2, 1),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.decode_sf_dl")
    def test_decode_payload(self, mock_decode_sf_dl, mock_get_sf_dl_bytes_number,
                            addressing_format, raw_frame_data,
                            sf_dl, sf_dl_bytes_number, ai_bytes_number):
        mock_decode_sf_dl.return_value = sf_dl
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        payload = CanSingleFrameHandler.decode_payload(addressing_format=addressing_format,
                                                       raw_frame_data=raw_frame_data)
        mock_decode_sf_dl.assert_called_once_with(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_called_once_with(self.mock_encode_dlc.return_value)
        assert isinstance(payload, bytearray)
        assert len(payload) == sf_dl
        assert payload == bytearray(raw_frame_data)[ai_bytes_number+sf_dl_bytes_number:][:sf_dl]

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(64)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("sf_dl", [1, 7])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
    def test_decode_sf_dl__valid_short(self, mock_extract_sf_dl_data_bytes,
                                       addressing_format, raw_frame_data, sf_dl):
        mock_extract_sf_dl_data_bytes.return_value = [(CanSingleFrameHandler.SINGLE_FRAME_N_PCI << 4) ^ sf_dl]
        assert CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data) == sf_dl
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(64)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("sf_dl", [8, 0x3E])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
    def test_decode_sf_dl__valid_long(self, mock_extract_sf_dl_data_bytes,
                                      addressing_format, raw_frame_data, sf_dl):
        mock_extract_sf_dl_data_bytes.return_value = [(CanSingleFrameHandler.SINGLE_FRAME_N_PCI << 4), sf_dl]
        assert CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data) == sf_dl
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [list(range(64)), (0x12, 0x34, 0x56)])
    @pytest.mark.parametrize("sf_dl_data_bytes", [[], [0x00, 0x00, 0x01]])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
    def test_decode_sf_dl__not_implemented(self, mock_extract_sf_dl_data_bytes,
                                           addressing_format, raw_frame_data, sf_dl_data_bytes):
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        with pytest.raises(NotImplementedError):
            CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                               raw_frame_data=raw_frame_data)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)

    # get_min_dlc

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (1, 7),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                             CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_min_dlc__short_dlc(self, mock_validate_payload_length,
                                    addressing_format, payload_length, ai_data_bytes,
                                    decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanSingleFrameHandler.get_min_dlc(addressing_format=addressing_format,
                                                 payload_length=payload_length) == self.mock_get_min_dlc.return_value
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)
        data_bytes_number = payload_length + CanSingleFrameHandler.SHORT_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_once_with(data_bytes_number)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (1, 7),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                             CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 5])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length")
    def test_get_can_frame_dlc_single_frame__long_dlc(self, mock_validate_payload_length,
                                                      addressing_format, payload_length, ai_data_bytes,
                                                      decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanSingleFrameHandler.get_min_dlc(addressing_format=addressing_format,
                                                 payload_length=payload_length) == self.mock_get_min_dlc.return_value
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_validate_payload_length.assert_called_once_with(ai_data_bytes_number=ai_data_bytes,
                                                             payload_length=payload_length)
        data_bytes_number = payload_length + CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_with(data_bytes_number)

    # get_max_payload_size

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("frame_data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number", [
        (10, 1, 1),
        (6, 0, 2),
        (64, 1, 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_get_max_payload_size__with_addressing_dlc(self, mock_get_sf_dl_bytes_number,
                                                       addressing_format, dlc,
                                                       frame_data_bytes_number, ai_data_bytes_number,
                                                       sf_dl_bytes_number):
        self.mock_decode_dlc.return_value = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        max_value = CanSingleFrameHandler.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)
        assert isinstance(max_value, int)
        assert max_value == frame_data_bytes_number - ai_data_bytes_number - sf_dl_bytes_number

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("frame_data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number", [
        (2, 1, 1),
        (1, 0, 2),
        (2, 1, 2),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_get_max_payload_size__too_short(self, mock_get_sf_dl_bytes_number,
                                             addressing_format, dlc,
                                             frame_data_bytes_number, ai_data_bytes_number, sf_dl_bytes_number):
        self.mock_decode_dlc.return_value = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_get_sf_dl_bytes_number.assert_called_once_with(dlc)

    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_get_max_payload_size__without_args(self, mock_get_sf_dl_bytes_number):
        max_value = CanSingleFrameHandler.get_max_payload_size()
        self.mock_decode_dlc.assert_not_called()
        self.mock_get_ai_data_bytes_number.assert_not_called()
        mock_get_sf_dl_bytes_number.assert_not_called()
        assert isinstance(max_value, int)
        assert max_value == CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED

    # get_sf_dl_bytes_number

    @pytest.mark.parametrize("dlc, expected_sf_dl_bytes_number", [
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 100, CanSingleFrameHandler.SHORT_SF_DL_BYTES_USED),
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL, CanSingleFrameHandler.SHORT_SF_DL_BYTES_USED),
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1, CanSingleFrameHandler.LONG_SF_DL_BYTES_USED),
        (CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 100, CanSingleFrameHandler.LONG_SF_DL_BYTES_USED),
    ])
    def test_get_sf_dl_bytes_number__short(self, dlc, expected_sf_dl_bytes_number):
        assert CanSingleFrameHandler.get_sf_dl_bytes_number(dlc) == expected_sf_dl_bytes_number
        self.mock_validate_dlc.assert_called_once_with(dlc)

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data, dlc, ai_bytes_number, sf_dl_data_bytes", [
        (list(range(8)), 8, 0, [0x07]),
        (list(range(64)), 10, 0, [0x00, 0x3E]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__valid(self, mock_is_single_frame, mock_extract_sf_dl_data_bytes,
                                        addressing_format, raw_frame_data,
                                        ai_bytes_number, sf_dl_data_bytes, dlc):
        mock_is_single_frame.return_value = True
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        self.mock_encode_dlc.return_value = dlc
        CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data", ["some raw bbytes", range(6)])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__invalid_type(self, mock_is_single_frame, addressing_format, raw_frame_data):
        mock_is_single_frame.return_value = False
        with pytest.raises(ValueError):
            CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("raw_frame_data, dlc, ai_bytes_number, sf_dl_data_bytes", [
        (list(range(7)), 8, 0, [0x07]),
        (list(range(9)), 9, 1, [0x00, 0x08]),
        (list(range(64)), 10, 0, [0x0A, 0x3F]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.is_single_frame")
    def test_validate_frame_data__sf_dl_bytes(self, mock_is_single_frame, mock_extract_sf_dl_data_bytes,
                                              addressing_format, raw_frame_data,
                                              ai_bytes_number, sf_dl_data_bytes, dlc):
        mock_is_single_frame.return_value = True
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        mock_extract_sf_dl_data_bytes.return_value = sf_dl_data_bytes
        self.mock_encode_dlc.return_value = dlc
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_single_frame.assert_called_once_with(addressing_format=addressing_format,
                                                     raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        mock_extract_sf_dl_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))

    # validate_sf_dl

    @pytest.mark.parametrize("sf_dl", ["some SF_DL", None, 5.])
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("dlc", "some addressing"),
        (8, None),
    ])
    def test_validate_sf_dl__type_error(self, sf_dl, dlc, addressing_format):
        with pytest.raises(TypeError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl", [0, -1, -6])
    @pytest.mark.parametrize("dlc, addressing_format", [
        ("dlc", "some addressing"),
        (8, None),
    ])
    def test_validate_sf_dl__value_error(self, sf_dl, dlc, addressing_format):
        with pytest.raises(ValueError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)

    @pytest.mark.parametrize("sf_dl, max_sf_dl", [
        (8, 7),
        (14, 9),
        (63, 62),
    ])
    @pytest.mark.parametrize("dlc", [8, 0xF])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_max_payload_size")
    def test_validate_sf_dl__inconsistent(self, mock_get_max_payload_size,
                                          sf_dl, dlc, addressing_format, max_sf_dl):
        mock_get_max_payload_size.return_value = max_sf_dl
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)  #
        mock_get_max_payload_size.assert_called_once_with(addressing_format=addressing_format, dlc=dlc)

    @pytest.mark.parametrize("sf_dl, max_sf_dl", [
        (8, 8),
        (14, 16),
        (62, 62),
    ])
    @pytest.mark.parametrize("dlc", [8, 0xF])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_max_payload_size")
    def test_validate_sf_dl__valid(self, mock_get_max_payload_size,
                                   sf_dl, dlc, addressing_format, max_sf_dl):
        mock_get_max_payload_size.return_value = max_sf_dl
        CanSingleFrameHandler.validate_sf_dl(sf_dl=sf_dl, dlc=dlc, addressing_format=addressing_format)
        mock_get_max_payload_size.assert_called_once_with(addressing_format=addressing_format, dlc=dlc)

    # __validate_payload_length

    @pytest.mark.parametrize("payload_length", [None, 6.5, "not a payload length"])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_validate_payload_length__type_error(self, payload_length, ai_data_bytes_number):
        with pytest.raises(TypeError):
            CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
                                                                                  ai_data_bytes_number=ai_data_bytes_number)

    @pytest.mark.parametrize("payload_length", [0, -1])
    @pytest.mark.parametrize("ai_data_bytes_number", [0, 1])
    def test_validate_payload_length__value_error(self, payload_length, ai_data_bytes_number):
        with pytest.raises(ValueError):
            CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
                                                                                  ai_data_bytes_number=ai_data_bytes_number)

    @pytest.mark.parametrize("payload_length, ai_data_bytes_number", [
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED, 1),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + 42, 1),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + 1, 0),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED + 5, 0),
    ])
    def test_validate_payload_length__inconsistency_error(self, payload_length, ai_data_bytes_number):
        with pytest.raises(InconsistentArgumentsError):
            CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
                                                                                  ai_data_bytes_number=ai_data_bytes_number)

    @pytest.mark.parametrize("payload_length, ai_data_bytes_number", [
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED - 1, 1),
        (CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanSingleFrameHandler.LONG_SF_DL_BYTES_USED, 0),
        (1, 0),
    ])
    def test_validate_payload_length__valid(self, payload_length, ai_data_bytes_number):
        CanSingleFrameHandler._CanSingleFrameHandler__validate_payload_length(payload_length=payload_length,
                                                                              ai_data_bytes_number=ai_data_bytes_number)

    # __extract_sf_dl_data_bytes

    @pytest.mark.parametrize("addressing_format, ai_data_bytes", [
        ("some addressing format", 0),
        ("another format", 1),
    ])
    @pytest.mark.parametrize("raw_frame_data", [range(10), range(10, 16)])
    @pytest.mark.parametrize("sf_dl_bytes_number", [1, 2])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_sf_dl_bytes_number")
    def test_extract_sf_dl_data_bytes(self, mock_get_sf_dl_bytes_number,
                                      addressing_format, raw_frame_data, sf_dl_bytes_number, ai_data_bytes):
        mock_get_sf_dl_bytes_number.return_value = sf_dl_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        sf_dl_bytes = CanSingleFrameHandler._CanSingleFrameHandler__extract_sf_dl_data_bytes(
            addressing_format=addressing_format, raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        self.mock_encode_dlc.assert_called_once_with(len(raw_frame_data))
        mock_get_sf_dl_bytes_number.assert_called_once_with(self.mock_encode_dlc.return_value)
        assert isinstance(sf_dl_bytes, bytearray)
        assert len(sf_dl_bytes) == sf_dl_bytes_number
        assert sf_dl_bytes == bytearray(raw_frame_data)[ai_data_bytes:][:sf_dl_bytes_number]

    # __encode_valid_sf_dl

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL,
                                     CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL - 1])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_encode_valid_sf_dl__short(self, mock_validate_sf_dl, mock_encode_any_sf_dl,
                                 sf_dl, dlc, addressing_format):
        assert CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl(
            sf_dl=sf_dl,
            addressing_format=addressing_format,
            dlc=dlc) == mock_encode_any_sf_dl.return_value
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    addressing_format=addressing_format)
        mock_encode_any_sf_dl.assert_called_once_with(sf_dl_short=sf_dl)

    @pytest.mark.parametrize("sf_dl", [0, 8, 0xF])
    @pytest.mark.parametrize("dlc", [CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 1,
                                     CanSingleFrameHandler.MAX_DLC_VALUE_SHORT_SF_DL + 2])
    @pytest.mark.parametrize("addressing_format", [None, "some addressing format"])
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl")
    @patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.validate_sf_dl")
    def test_encode_valid_sf_dl__long(self, mock_validate_sf_dl, mock_encode_any_sf_dl,
                                sf_dl, dlc, addressing_format):
        assert CanSingleFrameHandler._CanSingleFrameHandler__encode_valid_sf_dl(
            sf_dl=sf_dl,
            addressing_format=addressing_format,
            dlc=dlc) == mock_encode_any_sf_dl.return_value
        mock_validate_sf_dl.assert_called_once_with(sf_dl=sf_dl,
                                                    dlc=dlc,
                                                    addressing_format=addressing_format)
        mock_encode_any_sf_dl.assert_called_once_with(sf_dl_long=sf_dl)

    # __encode_any_sf_dl

    @pytest.mark.parametrize("sf_dl_short", [0, 7, 0xF])
    def test_encode_any_sf_dl__short(self, sf_dl_short):
        assert (CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl(sf_dl_short=sf_dl_short)
                == bytearray([(CanSingleFrameHandler.SINGLE_FRAME_N_PCI << 4) + sf_dl_short]))
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_not_called()

    @pytest.mark.parametrize("sf_dl_short", [0, 5, 0xF])
    @pytest.mark.parametrize("sf_dl_long", [0, 7, 0xF])
    def test_encode_any_sf_dl__long(self, sf_dl_short, sf_dl_long):
        assert (CanSingleFrameHandler._CanSingleFrameHandler__encode_any_sf_dl(sf_dl_short=sf_dl_short,
                                                                              sf_dl_long=sf_dl_long)
                == bytearray([(CanSingleFrameHandler.SINGLE_FRAME_N_PCI << 4) + sf_dl_short, sf_dl_long]))
        self.mock_validate_nibble.assert_called_once_with(sf_dl_short)
        self.mock_validate_raw_byte.assert_called_once_with(sf_dl_long)


@pytest.mark.integration
class TestCanSingleFrameHandlerIntegration:
    """Integration tests for `CanSingleFrameHandler` class."""

    # create_valid_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "payload": [0x3E]}, bytearray([0x01, 0x3E])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": [0x3E],
          "dlc": 8,
          "target_address": 0xFF}, bytearray([0x01, 0x3E] + ([DEFAULT_FILLER_BYTE] * 6))),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "payload": list(range(54)),
          "filler_byte": 0x66,
          "target_address": 0xF2}, bytearray([0xF2, 0x00, 0x36] + list(range(54)) + ([0x66] * 7))),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
          "dlc": 8,
          "filler_byte": 0x66,
          "address_extension": 0x12}, bytearray([0x12, 0x06, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01],
          "filler_byte": 0x99,
          "target_address": 0xF2,
          "address_extension": 0x12}, bytearray([0x12, 0x00, 0x07, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00, 0x01, 0x99, 0x99])),
    ])
    def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanSingleFrameHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "payload": b"\x3E",
         "dlc": 1},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": bytes(range(63))},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "payload": bytes(range(50, 112)),
         "target_address": 0xF2},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "payload": b"\xAB",
         "dlc": 7,
         "address_extension": 0x12},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "payload": [],
         "target_address": 0xF2,
         "address_extension": 0x12},
    ])
    def test_create_valid_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanSingleFrameHandler.create_valid_frame_data(**kwargs)

    # create_any_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "payload": [0x3E],
          "dlc": 2,
          "sf_dl_short": 0xF}, bytearray([0x0F, 0x3E])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": [0x3E],
          "dlc": 8,
          "target_address": 0xFF,
          "sf_dl_short": 0x0,
          "sf_dl_long": 0xAB}, bytearray([0x00, 0xAB, 0x3E] + ([DEFAULT_FILLER_BYTE] * 5))),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "payload": [],
          "dlc": 0xF,
          "filler_byte": 0x66,
          "target_address": 0xF2,
          "sf_dl_short": 0xE}, bytearray([0xF2, 0x0E] + ([0x66] * 62))),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "payload": [0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00],
          "dlc": 8,
          "filler_byte": 0x66,
          "address_extension": 0x12,
          "sf_dl_short": 0x5}, bytearray([0x12, 0x05, 0x9A, 0xB8, 0xC4, 0x67, 0x10, 0x00])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "payload": [0x9A, 0xB8],
          "dlc": 7,
          "filler_byte": 0x99,
          "target_address": 0xF2,
          "address_extension": 0x12,
          "sf_dl_short": 0x2}, bytearray([0x12, 0x02, 0x9A, 0xB8, 0x99, 0x99, 0x99])),
    ])
    def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanSingleFrameHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "payload": [0x3E],
         "dlc": 1,
         "sf_dl_short": 0xF},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": list(range(63)),
         "dlc": 0xF,
         "sf_dl_short": 0x0,
         "sf_dl_long": 0xAB},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "payload": [],
         "dlc": 0xF,
         "target_address": 0xF2,
         "sf_dl_short": 0x10},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "payload": list(range(5)),
         "dlc": 8,
         "address_extension": 0x12,
         "sf_dl_short": 0,
         "sf_dl_long": 0x100},
    ])
    def test_create_any_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanSingleFrameHandler.create_any_frame_data(**kwargs)

    # decode_sf_dl

    @pytest.mark.parametrize("addressing_format, raw_frame_data, expected_sf_dl", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x01, 0x3E), 1),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x00, 0x32] + list(range(20, 82)), 0x32),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x05, 0x04, 0x03, 0x02, 0x01, 0x00, 0xFF, 0xFE], 4),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x0A, 0x00, 0x3D] + list(range(100, 161)), 0x3D),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xDA, 0x00, 0x10] + list(range(21)), 0x10)
    ])
    def test_decode_sf_dl(self, addressing_format, raw_frame_data, expected_sf_dl):
        assert CanSingleFrameHandler.decode_sf_dl(addressing_format=addressing_format,
                                                  raw_frame_data=raw_frame_data) == expected_sf_dl

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x07, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x00, 0x3E] + list(range(0x10, 0x4E))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x00, 0x00, 0x01] + list(range(0x10, 0x4D))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x02, 0x01, 0xFF)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0x04, 0x00, 0x05] + list(range(100, 113))),
    ])
    def test_validate_frame_data__valid(self, addressing_format, raw_frame_data):
        assert CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                         raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x05, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, [0x00, 0x3F] + list(range(0x10, 0x4E))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x00, 0x01, 0x01] + list(range(0x10, 0x4D))),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, (0x02, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, [0xB0, 0x09] + list(range(100, 114))),
    ])
    def test_validate_frame_data__invalid(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            CanSingleFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)

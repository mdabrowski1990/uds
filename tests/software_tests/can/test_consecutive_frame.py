import pytest
from mock import patch

from uds.can.consecutive_frame import CanConsecutiveFrameHandler, \
    InconsistentArgumentsError, CanPacketType, CanAddressingFormat, DEFAULT_FILLER_BYTE


class TestCanConsecutiveFrameHandler:
    """Tests for `CanConsecutiveFrameHandler` class."""

    SCRIPT_LOCATION = "uds.can.consecutive_frame"

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
        self._patcher_encode_ai_data_bytes = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.encode_ai_data_bytes")
        self.mock_encode_ai_data_bytes = self._patcher_encode_ai_data_bytes.start()
        self._patcher_get_ai_data_bytes_number = \
            patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler.get_ai_data_bytes_number")
        self.mock_get_ai_data_bytes_number = self._patcher_get_ai_data_bytes_number.start()

    def teardown(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()

    # create_valid_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, sequence_number", [
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING, 0x66, "some sequence number"),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING + 2, 0x99, 0xF),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_valid_frame_data__valid_with_dlc(self, mock_encode_sn,
                                                     addressing_format, target_address, address_extension,
                                                     payload, sequence_number, dlc, filler_byte,
                                                     data_bytes_number, ai_data_bytes, sn_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_sn.return_value = sn_data_bytes
        cf_frame_data = CanConsecutiveFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                           target_address=target_address,
                                                                           address_extension=address_extension,
                                                                           payload=payload,
                                                                           sequence_number=sequence_number,
                                                                           dlc=dlc,
                                                                           filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_sn.assert_called_once_with(sequence_number=sequence_number)
        assert isinstance(cf_frame_data, list)
        assert len(cf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, sequence_number", [
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING, 0x66, "some sequence number"),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING + 2, 0x99, 0xF),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([0x3E], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.get_min_dlc")
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_valid_frame_data__valid_without_dlc(self, mock_encode_sn, mock_get_min_dlc,
                                                        addressing_format, target_address, address_extension,
                                                        payload, sequence_number, dlc, filler_byte,
                                                        data_bytes_number, ai_data_bytes, sn_data_bytes):
        mock_get_min_dlc.return_value = dlc
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_sn.return_value = sn_data_bytes
        cf_frame_data = CanConsecutiveFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                                           target_address=target_address,
                                                                           address_extension=address_extension,
                                                                           payload=payload,
                                                                           sequence_number=sequence_number,
                                                                           dlc=None,
                                                                           filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format,
                                                 payload_length=len(payload))
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_sn.assert_called_once_with(sequence_number=sequence_number)
        assert isinstance(cf_frame_data, list)
        assert len(cf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("filler_byte, sequence_number", [
        (0x66, "some sequence number"),
        (0x99, 0xF),
    ])
    @pytest.mark.parametrize("dlc, payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING - 1, range(60), 100, [0xFF], [0x00, 0xFA]),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING - 2, [0x3E], 7, [], [0x01]),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING, [0x20, 0x30, 0x44], 3, [], [0x03]),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING + 1, range(20), 21, [0xAA], [0x03]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_valid_frame_data__inconsistent_args(self, mock_encode_sn,
                                                        addressing_format, target_address, address_extension,
                                                        payload, sequence_number, dlc, filler_byte,
                                                        data_bytes_number, ai_data_bytes, sn_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_sn.return_value = sn_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanConsecutiveFrameHandler.create_valid_frame_data(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension,
                                                               payload=payload,
                                                               sequence_number=sequence_number,
                                                               dlc=dlc,
                                                               filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=False)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_sn.assert_called_once_with(sequence_number=sequence_number)

    # create_any_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, sequence_number", [
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING - 2, 0x66, "some sequence number"),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING + 2, 0x99, 0xF),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        ([0x54], 2, [], [0xFA]),
        ([], 8, [], [0x0C]),
        (range(50, 110), 64, [0x98], [0x12, 0x34]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_valid_frame_data__valid_with_dlc(self, mock_encode_sn,
                                                     addressing_format, target_address, address_extension,
                                                     payload, sequence_number, dlc, filler_byte,
                                                     data_bytes_number, ai_data_bytes, sn_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_sn.return_value = sn_data_bytes
        cf_frame_data = CanConsecutiveFrameHandler.create_any_frame_data(addressing_format=addressing_format,
                                                                         target_address=target_address,
                                                                         address_extension=address_extension,
                                                                         payload=payload,
                                                                         sequence_number=sequence_number,
                                                                         dlc=dlc,
                                                                         filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_sn.assert_called_once_with(sequence_number=sequence_number)
        assert isinstance(cf_frame_data, list)
        assert len(cf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("filler_byte, sequence_number", [
        (0x66, "some sequence number"),
        (0x99, 0xF),
    ])
    @pytest.mark.parametrize("dlc, payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING - 1, range(60), 62, [0xFF], [0x00, 0xFA]),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING + 1, range(20), 21, [0xAA], [0x03]),
        (CanConsecutiveFrameHandler.MIN_DLC_DATA_PADDING, [0x20, 0x30, 0x44], 3, [], [0x03]),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_valid_frame_data__inconsistent_args(self, mock_encode_sn,
                                                        addressing_format, target_address, address_extension,
                                                        payload, sequence_number, dlc, filler_byte,
                                                        data_bytes_number, ai_data_bytes, sn_data_bytes):
        self.mock_decode_dlc.return_value = data_bytes_number
        self.mock_encode_ai_data_bytes.return_value = ai_data_bytes
        mock_encode_sn.return_value = sn_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanConsecutiveFrameHandler.create_any_frame_data(addressing_format=addressing_format,
                                                             target_address=target_address,
                                                             address_extension=address_extension,
                                                             payload=payload,
                                                             sequence_number=sequence_number,
                                                             dlc=dlc,
                                                             filler_byte=filler_byte)
        self.mock_validate_raw_byte.assert_called_once_with(filler_byte)
        self.mock_validate_raw_bytes.assert_called_once_with(payload, allow_empty=True)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_encode_ai_data_bytes.assert_called_once_with(addressing_format=addressing_format,
                                                               target_address=target_address,
                                                               address_extension=address_extension)
        mock_encode_sn.assert_called_once_with(sequence_number=sequence_number)

    # __extract_sn_data_bytes

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data, ai_bytes_number, expected_output", [
        ([0x12, 0x34, 0x45, 0x67, 0x89], 0, [0x12]),
        ([0x12, 0x34, 0x45, 0x67, 0x89], 1, [0x34]),
        (range(30, 94), 0, [30]),
    ])
    def test_extract_sn_data_bytes(self, addressing_format, raw_frame_data, ai_bytes_number, expected_output):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__extract_sn_data_bytes(
            addressing_format=addressing_format, raw_frame_data=raw_frame_data) == expected_output
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # __encode_sn

    @pytest.mark.parametrize("sequence_number", [0, 5, 0xF])
    def test_encode_sn(self, sequence_number):
        assert CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn(sequence_number=sequence_number) \
               == [(CanPacketType.CONSECUTIVE_FRAME.value << 4) + sequence_number]
        self.mock_validate_nibble.assert_called_once_with(sequence_number)


@pytest.mark.integration
class TestCanSingleFrameHandlerIntegration:
    """Integration tests for `CanSingleFrameHandler` class."""

    # create_valid_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "payload": [0x9A],
          "sequence_number": 0}, [0x20, 0x9A]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": tuple(range(48)),
          "sequence_number": 0xF}, [0x2F] + list(range(48)) + (15 * [DEFAULT_FILLER_BYTE])),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "target_address": 0xF1,
          "dlc": 8,
          "payload": (0x92, 0xB8),
          "sequence_number": 0x5,
          "filler_byte": 0xD9}, [0xF1, 0x25, 0x92, 0xB8, 0xD9, 0xD9, 0xD9, 0xD9]),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "address_extension": 0xE8,
          "dlc": 9,
          "payload": list(range(10, 20)),
          "sequence_number": 0xB,
          "filler_byte": 0x99}, [0xE8, 0x2B] + list(range(10, 20))),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "target_address": 0xFE,
          "address_extension": 0xDC,
          "payload": tuple(range(50, 96)),
          "sequence_number": 0x1,
          "filler_byte": 0xD9}, [0xFE, 0x21] + list(range(50, 96))),
    ])
    def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanConsecutiveFrameHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "payload": [0x9A],
         "dlc": 1,
         "sequence_number": 0},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": [],
         "sequence_number": 0xF},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "target_address": 0xF1,
         "payload": [0x9A],
         "dlc": 8,
         "sequence_number": 0x10},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "address_extension": 0xE8,
         "payload": list(range(7)),
         "dlc": 8,
         "sequence_number": 0x10},
        {"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
         "target_address": 0xFE,
         "address_extension": 0xE8,
         "payload": tuple(range(50, 96)),
         "sequence_number": -1,
         "filler_byte": 0xD9}
    ])
    def test_create_valid_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.create_valid_frame_data(**kwargs)

    # create_any_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
          "payload": [],
          "dlc": 1,
          "sequence_number": 0}, [0x20]),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": (0xFE, 0xDC),
          "dlc": 5,
          "sequence_number": 0xF}, [0x2F, 0xFE, 0xDC, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE]),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "target_address": 0xF1,
          "payload": [],
          "dlc": 2,
          "sequence_number": 0xE,
          "filler_byte": 0xD9}, [0xF1, 0x2E]),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "address_extension": 0xE8,
          "payload": [],
          "dlc": 2,
          "sequence_number": 0x1}, [0xE8, 0x21]),
    ])
    def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanConsecutiveFrameHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
         "payload": [0x9A],
         "dlc": 1,
         "sequence_number": 0},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": [],
         "dlc": 8,
         "sequence_number": -1},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "target_address": 0xF1,
         "payload": [0x9A],
         "dlc": 8,
         "sequence_number": 0x10},
        {"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
         "address_extension": 0xE8,
         "payload": list(range(7)),
         "dlc": 8,
         "sequence_number": 0xE},
    ])
    def test_create_any_frame_data__invalid(self, kwargs):
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.create_any_frame_data(**kwargs)

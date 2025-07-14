import pytest
from mock import patch

from uds.addressing import CanAddressingFormat
from uds.can.packet.consecutive_frame import (
    DEFAULT_FILLER_BYTE,
    CanConsecutiveFrameHandler,
    CanDlcHandler,
    InconsistentArgumentsError,
)

SCRIPT_LOCATION = "uds.addressing.consecutive_frame"


class TestCanConsecutiveFrameHandler:
    """Unit tests for `CanConsecutiveFrameHandler` class."""

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

    def teardown_method(self):
        self._patcher_validate_nibble.stop()
        self._patcher_validate_raw_byte.stop()
        self._patcher_validate_raw_bytes.stop()
        self._patcher_encode_dlc.stop()
        self._patcher_decode_dlc.stop()
        self._patcher_get_min_dlc.stop()
        self._patcher_encode_ai_data_bytes.stop()
        self._patcher_get_ai_data_bytes_number.stop()

    # create_valid_frame_data

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, sequence_number", [
        (CanDlcHandler.MIN_BASE_UDS_DLC, 0x66, "some sequence number"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, 0xF),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        ([0x54], 2, bytearray(), bytearray([0xFA])),
        (range(50, 110), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
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
        assert isinstance(cf_frame_data, bytearray)
        assert len(cf_frame_data) == data_bytes_number

    @pytest.mark.parametrize("addressing_format, target_address, address_extension", [
        ("some format", "TA", "SA"),
        ("another format", None, None),
    ])
    @pytest.mark.parametrize("dlc, filler_byte, sequence_number", [
        (CanDlcHandler.MIN_BASE_UDS_DLC, 0x66, "some sequence number"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, 0xF),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        ([0x54], 2, bytearray(), bytearray([0xFA])),
        (range(50, 110), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
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
        assert isinstance(cf_frame_data, bytearray)
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
        (CanDlcHandler.MIN_BASE_UDS_DLC - 1, range(60), 100, bytearray([0xFF]), bytearray([0x00, 0xFA])),
        (CanDlcHandler.MIN_BASE_UDS_DLC - 2, [0x3E], 7, bytearray(), bytearray([0x01])),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 1, [0x20, 0x30, 0x44], 4, bytearray([0xAA]), bytearray([0x03])),
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
        (CanDlcHandler.MIN_BASE_UDS_DLC - 2, 0x66, "some sequence number"),
        (CanDlcHandler.MIN_BASE_UDS_DLC + 2, 0x99, 0xF),
    ])
    @pytest.mark.parametrize("payload, data_bytes_number, ai_data_bytes, sn_data_bytes", [
        ([], 8, bytearray(), bytearray([0x0C])),
        (range(50, 110), 64, bytearray([0x98]), bytearray([0x12, 0x34])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_any_frame_data__valid(self, mock_encode_sn,
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
        assert isinstance(cf_frame_data, bytearray)
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
        (CanDlcHandler.MIN_BASE_UDS_DLC - 1, range(60), 62, bytearray([0xFF]), bytearray([0x00, 0xFA])),
        (CanDlcHandler.MIN_BASE_UDS_DLC, [0x20, 0x30, 0x44], 3, bytearray(), bytearray([0x03])),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn")
    def test_create_any_frame_data__inconsistent_args(self, mock_encode_sn,
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

    # is_consecutive_frame

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, (0x2F, 0xFE, 0xDC, 0xBA, 0x98, 0x76)),
        (1, [0x01, 0x20] + list(range(46))),
    ])
    def test_is_consecutive_frame__true(self, addressing_format, raw_frame_data,
                                        ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanConsecutiveFrameHandler.is_consecutive_frame(addressing_format=addressing_format,
                                                               raw_frame_data=raw_frame_data) is True
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, (0x0F, 0xFE, 0xDC, 0xBA, 0x98, 0x76)),
        (1, [0x01, 0x10] + list(range(46))),
        (0, [0x35] + list(range(47))),
        (1, (0x13, 0xFE, 0x21)),
    ])
    def test_is_consecutive_frame__false(self, addressing_format, raw_frame_data, ai_bytes_number):
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        assert CanConsecutiveFrameHandler.is_consecutive_frame(addressing_format=addressing_format,
                                                               raw_frame_data=raw_frame_data) is False
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # decode_payload

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, [0x25] + list(range(47))),
        (1, (0x13, 0x2E, 0x21)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    def test_decode_payload(self, mock_is_consecutive_frame,
                            addressing_format, raw_frame_data, ai_bytes_number):
        mock_is_consecutive_frame.return_value = True
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        payload = CanConsecutiveFrameHandler.decode_payload(addressing_format=addressing_format,
                                                            raw_frame_data=raw_frame_data)
        assert isinstance(payload, bytearray)
        assert payload == bytearray(raw_frame_data)[ai_bytes_number + CanConsecutiveFrameHandler.SN_BYTES_USED:]
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [
        (0x2F, 0xFE, 0xDC, 0xBA, 0x98, 0x76),
        [0x01, 0x20] + list(range(46)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    def test_decode_payload__value_error(self, mock_is_consecutive_frame,
                                         addressing_format, raw_frame_data):
        mock_is_consecutive_frame.return_value = False
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.decode_payload(addressing_format=addressing_format,
                                                      raw_frame_data=raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_not_called()

    # decode_sequence_number

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("ai_bytes_number, raw_frame_data", [
        (0, [0x25] + list(range(47))),
        (1, (0x13, 0x2E, 0x21)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    def test_decode_sequence_number(self, mock_is_consecutive_frame,
                                    addressing_format, raw_frame_data, ai_bytes_number):
        mock_is_consecutive_frame.return_value = True
        self.mock_get_ai_data_bytes_number.return_value = ai_bytes_number
        sequence_number = CanConsecutiveFrameHandler.decode_sequence_number(addressing_format=addressing_format,
                                                                            raw_frame_data=raw_frame_data)
        assert isinstance(sequence_number, int)
        assert sequence_number == raw_frame_data[ai_bytes_number] & 0xF
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "another format"])
    @pytest.mark.parametrize("raw_frame_data", [
        (0x2F, 0xFE, 0xDC, 0xBA, 0x98, 0x76),
        [0x01, 0x20] + list(range(46)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    def test_decode_sequence_number__value_error(self, mock_is_consecutive_frame,
                                                 addressing_format, raw_frame_data):
        mock_is_consecutive_frame.return_value = False
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.decode_sequence_number(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        self.mock_get_ai_data_bytes_number.assert_not_called()

    # get_min_dlc

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (0, 1),
        (0, 62),
    ])
    @pytest.mark.parametrize("decoded_dlc", [8, 0xF])
    def test_get_min_dlc(self, addressing_format, payload_length, ai_data_bytes, decoded_dlc):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        self.mock_get_min_dlc.return_value = decoded_dlc
        assert CanConsecutiveFrameHandler.get_min_dlc(
            addressing_format=addressing_format, payload_length=payload_length) == self.mock_get_min_dlc.return_value
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        data_bytes_number = payload_length + CanConsecutiveFrameHandler.SN_BYTES_USED + ai_data_bytes
        self.mock_get_min_dlc.assert_called_once_with(data_bytes_number)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("payload_length", [None, "not a payload", 5.])
    def test_get_min_dlc__type_error(self, addressing_format, payload_length):
        with pytest.raises(TypeError):
            CanConsecutiveFrameHandler.get_min_dlc(addressing_format=addressing_format, payload_length=payload_length)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("payload_length", [0, 64])
    def test_get_min_dlc__value_error(self, addressing_format, payload_length):
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.get_min_dlc(addressing_format=addressing_format, payload_length=payload_length)

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("ai_data_bytes, payload_length", [
        (1, 63),
        (2, 62),
    ])
    def test_get_min_dlc__inconsistent_args(self, addressing_format, payload_length, ai_data_bytes):
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes
        with pytest.raises(InconsistentArgumentsError):
            CanConsecutiveFrameHandler.get_min_dlc(addressing_format=addressing_format, payload_length=payload_length)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    # get_max_payload_size

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("frame_data_bytes_number, ai_data_bytes_number", [
        (10, 1),
        (64, 1),
    ])
    def test_get_max_payload_size__with_addressing_dlc(self, addressing_format, dlc,
                                                       frame_data_bytes_number, ai_data_bytes_number):
        self.mock_decode_dlc.return_value = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        max_value = CanConsecutiveFrameHandler.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)
        assert isinstance(max_value, int)
        assert max_value == frame_data_bytes_number - ai_data_bytes_number - CanConsecutiveFrameHandler.SN_BYTES_USED

    @pytest.mark.parametrize("addressing_format", ["some addressing format", "something else"])
    @pytest.mark.parametrize("dlc", ["some DLC", 8])
    @pytest.mark.parametrize("frame_data_bytes_number, ai_data_bytes_number", [
        (1, 1),
        (0, 0),
    ])
    def test_get_max_payload_size__too_short(self, addressing_format, dlc,
                                             frame_data_bytes_number, ai_data_bytes_number):
        self.mock_decode_dlc.return_value = frame_data_bytes_number
        self.mock_get_ai_data_bytes_number.return_value = ai_data_bytes_number
        with pytest.raises(InconsistentArgumentsError):
            CanConsecutiveFrameHandler.get_max_payload_size(addressing_format=addressing_format, dlc=dlc)
        self.mock_decode_dlc.assert_called_once_with(dlc)
        self.mock_get_ai_data_bytes_number.assert_called_once_with(addressing_format)

    def test_get_max_payload_size__without_args(self):
        max_value = CanConsecutiveFrameHandler.get_max_payload_size()
        self.mock_decode_dlc.assert_not_called()
        self.mock_get_ai_data_bytes_number.assert_not_called()
        assert isinstance(max_value, int)
        assert max_value == CanDlcHandler.MAX_DATA_BYTES_NUMBER - CanConsecutiveFrameHandler.SN_BYTES_USED

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing format", "some raw frame data"),
        ("another format", range(5)),
    ])
    @pytest.mark.parametrize("min_dlc, decoded_dlc", [
        (8, 8),
        (13, 15),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.get_min_dlc")
    def test_validate_frame_data__valid(self, mock_get_min_dlc, mock_is_consecutive_frame,
                                        addressing_format, raw_frame_data,
                                        decoded_dlc, min_dlc):
        mock_is_consecutive_frame.return_value = True
        mock_get_min_dlc.return_value = min_dlc
        self.mock_encode_dlc.return_value = decoded_dlc
        CanConsecutiveFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                       raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format)

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing format", "some raw frame data"),
        ("another format", range(5)),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    def test_validate_frame_data__value_error(self, mock_is_consecutive_frame,
                                                      addressing_format, raw_frame_data):
        mock_is_consecutive_frame.return_value = False
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                           raw_frame_data=raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        ("some addressing format", "some raw frame data"),
        ("another format", range(5)),
    ])
    @pytest.mark.parametrize("min_dlc, decoded_dlc", [
        (1, 0),
        (15, 8),
    ])
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.is_consecutive_frame")
    @patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.get_min_dlc")
    def test_validate_frame_data__inconsistent_error(self, mock_get_min_dlc, mock_is_consecutive_frame,
                                                     addressing_format, raw_frame_data,
                                                     decoded_dlc, min_dlc):
        mock_is_consecutive_frame.return_value = True
        mock_get_min_dlc.return_value = min_dlc
        self.mock_encode_dlc.return_value = decoded_dlc
        with pytest.raises(InconsistentArgumentsError):
            CanConsecutiveFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                           raw_frame_data=raw_frame_data)
        self.mock_validate_raw_bytes.assert_called_once_with(raw_frame_data)
        mock_is_consecutive_frame.assert_called_once_with(addressing_format=addressing_format,
                                                          raw_frame_data=raw_frame_data)
        mock_get_min_dlc.assert_called_once_with(addressing_format=addressing_format)

    # __encode_sn

    @pytest.mark.parametrize("sequence_number", [0, 0xF])
    def test_encode_sn(self, sequence_number):
        assert CanConsecutiveFrameHandler._CanConsecutiveFrameHandler__encode_sn(sequence_number=sequence_number) \
               == bytearray([(CanConsecutiveFrameHandler.CONSECUTIVE_FRAME_N_PCI << 4) + sequence_number])
        self.mock_validate_nibble.assert_called_once_with(sequence_number)


@pytest.mark.integration
class TestCanSingleFrameHandlerIntegration:
    """Integration tests for `CanSingleFrameHandler` class."""

    # create_valid_frame_data

    @pytest.mark.parametrize("kwargs, expected_raw_frame_data", [
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "payload": b"\x9A",
          "sequence_number": 0}, bytearray([0x20, 0x9A])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": bytes(range(48)),
          "sequence_number": 0xF}, bytearray([0x2F] + list(range(48)) + (15 * [DEFAULT_FILLER_BYTE]))),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "target_address": 0xF1,
          "dlc": 8,
          "payload": b"\x92\xB8",
          "sequence_number": 0x5,
          "filler_byte": 0xD9}, bytearray([0xF1, 0x25, 0x92, 0xB8, 0xD9, 0xD9, 0xD9, 0xD9])),
        ({"addressing_format": CanAddressingFormat.MIXED_11BIT_ADDRESSING,
          "address_extension": 0xE8,
          "dlc": 9,
          "payload": bytes(range(10, 20)),
          "sequence_number": 0xB,
          "filler_byte": 0x99}, bytearray([0xE8, 0x2B] + list(range(10, 20)))),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "target_address": 0xFE,
          "address_extension": 0xDC,
          "payload": bytes(range(50, 96)),
          "sequence_number": 0x1,
          "filler_byte": 0xD9}, bytearray([0xDC, 0x21] + list(range(50, 96)))),
    ])
    def test_create_valid_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanConsecutiveFrameHandler.create_valid_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
         "payload": b"\x9A",
         "dlc": 1,
         "sequence_number": 0},
        {"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
         "payload": bytearray(),
         "sequence_number": 0xF},
        {"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
         "target_address": 0xF1,
         "payload": b"\x9A",
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
        ({"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
          "payload": [],
          "dlc": 1,
          "sequence_number": 0}, bytearray([0x20])),
        ({"addressing_format": CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
          "payload": (0xFE, 0xDC),
          "dlc": 5,
          "sequence_number": 0xF}, bytearray([0x2F, 0xFE, 0xDC, DEFAULT_FILLER_BYTE, DEFAULT_FILLER_BYTE])),
        ({"addressing_format": CanAddressingFormat.EXTENDED_ADDRESSING,
          "target_address": 0xF1,
          "payload": [],
          "dlc": 2,
          "sequence_number": 0xE,
          "filler_byte": 0xD9}, bytearray([0xF1, 0x2E])),
        ({"addressing_format": CanAddressingFormat.MIXED_29BIT_ADDRESSING,
          "address_extension": 0xE8,
          "payload": [],
          "dlc": 2,
          "sequence_number": 0x1}, bytearray([0xE8, 0x21])),
    ])
    def test_create_any_frame_data__valid(self, kwargs, expected_raw_frame_data):
        assert CanConsecutiveFrameHandler.create_any_frame_data(**kwargs) == expected_raw_frame_data

    @pytest.mark.parametrize("kwargs", [
        {"addressing_format": CanAddressingFormat.NORMAL_ADDRESSING,
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

    # validate_frame_data

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, (0x20, 0x12, 0x34, 0x45, 0x67, 0x89, 0x9A, 0xBC)),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, (0x2F, 0x2F)),
        (CanAddressingFormat.EXTENDED_ADDRESSING, (0xF0, 0x26, 0x00)),
        (CanAddressingFormat.MIXED_11BIT_ADDRESSING, [0x30, 0x21] + (46 * [0xFF])),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, (0x8B, 0x2E, 0x9B)),
    ])
    def test_validate_frame_data__valid(self, addressing_format, raw_frame_data):
        assert CanConsecutiveFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                              raw_frame_data=raw_frame_data) is None

    @pytest.mark.parametrize("addressing_format, raw_frame_data", [
        (CanAddressingFormat.NORMAL_ADDRESSING, [0x20]),
        (CanAddressingFormat.NORMAL_FIXED_ADDRESSING, tuple([0x2F] + ([0xFF] * 64))),
        (CanAddressingFormat.EXTENDED_ADDRESSING, [0x2F, 0x2F]),
        (CanAddressingFormat.MIXED_29BIT_ADDRESSING, (0x8B, 0x2E)),
    ])
    def test_validate_frame_data__invalid(self, addressing_format, raw_frame_data):
        with pytest.raises(ValueError):
            CanConsecutiveFrameHandler.validate_frame_data(addressing_format=addressing_format,
                                                           raw_frame_data=raw_frame_data)

import pytest
from mock import MagicMock, Mock, call, patch

from uds.can import (
    ExtendedCanAddressingInformation,
    Mixed11BitCanAddressingInformation,
    Mixed29BitCanAddressingInformation,
    Normal11BitCanAddressingInformation,
    NormalFixedCanAddressingInformation,
    CanFlowStatus
)
from uds.segmentation.can_segmenter import (
    DEFAULT_FILLER_BYTE,
    AbstractCanAddressingInformation,
    AddressingType,
    CanDlcHandler,
    CanFirstFrameHandler,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    CanSegmenter,
    SegmentationError,
    UdsMessage,
)

SCRIPT_LOCATION = "uds.segmentation.can_segmenter"


class TestCanSegmenter:
    """Unit tests for `CanSegmenter` class."""

    def setup_method(self):
        self.mock_can_segmenter = Mock(spec=CanSegmenter)
        self.mock_can_segmenter.addressing_information.AI_DATA_BYTES_NUMBER = 0
        # patching
        self._patcher_can_ai_class = patch(f"{SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_ai_class = self._patcher_can_ai_class.start()
        self._patcher_validate_dlc = patch(f"{SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_dlc = self._patcher_validate_dlc.start()
        self._patcher_is_initial_packet_type = patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
        self.mock_is_initial_packet_type = self._patcher_is_initial_packet_type.start()
        self._patcher_get_max_sf_payload_size \
            = patch(f"{SCRIPT_LOCATION}.CanSingleFrameHandler.get_max_payload_size")
        self.mock_get_max_sf_payload_size = self._patcher_get_max_sf_payload_size.start()
        self._patcher_get_ff_payload_size = patch(f"{SCRIPT_LOCATION}.CanFirstFrameHandler.get_payload_size")
        self.mock_get_ff_payload_size = self._patcher_get_ff_payload_size.start()
        self._patcher_get_max_cf_payload_size \
            = patch(f"{SCRIPT_LOCATION}.CanConsecutiveFrameHandler.get_max_payload_size")
        self.mock_get_max_cf_payload_size = self._patcher_get_max_cf_payload_size.start()
        self._patcher_can_packet_class = patch(f"{SCRIPT_LOCATION}.CanPacket")
        self.mock_can_packet_class = self._patcher_can_packet_class.start()
        self._patcher_uds_message_class = patch(f"{SCRIPT_LOCATION}.UdsMessage")
        self.mock_uds_message_class = self._patcher_uds_message_class.start()
        self._patcher_uds_message_record_class = patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
        self.mock_uds_message_record_class = self._patcher_uds_message_record_class.start()
        self._patcher_validate_raw_byte = patch(f"{SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown_method(self):
        self._patcher_can_ai_class.stop()
        self._patcher_validate_dlc.stop()
        self._patcher_is_initial_packet_type.stop()
        self._patcher_get_max_sf_payload_size.stop()
        self._patcher_get_ff_payload_size.stop()
        self._patcher_get_max_cf_payload_size.stop()
        self._patcher_can_packet_class.stop()
        self._patcher_uds_message_class.stop()
        self._patcher_uds_message_record_class.stop()
        self._patcher_validate_raw_byte.stop()

    # __init__

    @pytest.mark.parametrize("addressing_information", [
        "some addressing information",
        Mock()
    ])
    def test_init__mandatory_args(self, addressing_information):
        CanSegmenter.__init__(self=self.mock_can_segmenter,
                              addressing_information=addressing_information)
        assert self.mock_can_segmenter.addressing_information == addressing_information
        assert self.mock_can_segmenter.dlc == CanDlcHandler.MIN_BASE_UDS_DLC
        assert self.mock_can_segmenter.use_data_optimization is False
        assert self.mock_can_segmenter.filler_byte == DEFAULT_FILLER_BYTE

    @pytest.mark.parametrize("addressing_information, dlc, use_data_optimization, filler_byte", [
        ("some addressing info", "some dlc", "True or False", "filler"),
        (Mock(), Mock(), Mock(), Mock()),
    ])
    def test_init__all_args(self, addressing_information, dlc, use_data_optimization, filler_byte):
        CanSegmenter.__init__(self=self.mock_can_segmenter,
                              addressing_information=addressing_information,
                              dlc=dlc,
                              use_data_optimization=use_data_optimization,
                              filler_byte=filler_byte)
        assert self.mock_can_segmenter.addressing_information == addressing_information
        assert self.mock_can_segmenter.dlc == dlc
        assert self.mock_can_segmenter.use_data_optimization == use_data_optimization
        assert self.mock_can_segmenter.filler_byte == filler_byte

    # supported_packet_classes

    def test_supported_packet_class__get(self):
        assert CanSegmenter.supported_packet_class.fget(self.mock_can_segmenter) == self.mock_can_packet_class

    # supported_packet_record_class

    def test_supported_packet_record_class__get(self):
        assert CanSegmenter.supported_packet_record_class.fget(self.mock_can_segmenter) == CanPacketRecord

    # addressing_format

    def test_addressing_format__get(self):
        assert CanSegmenter.addressing_format.fget(self.mock_can_segmenter) \
               == self.mock_can_segmenter.addressing_information.addressing_format

    # rx_packets_physical_ai

    def test_rx_packets_physical_ai__get(self):
        assert CanSegmenter.rx_packets_physical_ai.fget(self.mock_can_segmenter) \
               == self.mock_can_segmenter.addressing_information.rx_packets_physical_ai

    # tx_packets_physical_ai

    def test_tx_packets_physical_ai__get(self):
        assert CanSegmenter.tx_packets_physical_ai.fget(self.mock_can_segmenter) \
               == self.mock_can_segmenter.addressing_information.tx_packets_physical_ai

    # rx_packets_functional_ai

    def test_rx_packets_functional_ai__get(self):
        assert CanSegmenter.rx_packets_functional_ai.fget(self.mock_can_segmenter) \
               == self.mock_can_segmenter.addressing_information.rx_packets_functional_ai

    # tx_packets_functional_ai

    def test_tx_packets_functional_ai__get(self):
        assert CanSegmenter.tx_packets_functional_ai.fget(self.mock_can_segmenter) \
               == self.mock_can_segmenter.addressing_information.tx_packets_functional_ai

    # addressing_information

    @pytest.mark.parametrize("value", ["some AI", Mock()])
    def test_addressing_information__get(self, value):
        self.mock_can_segmenter._CanSegmenter__addressing_information = value
        assert CanSegmenter.addressing_information.fget(self.mock_can_segmenter) \
               == self.mock_can_segmenter._CanSegmenter__addressing_information

    @pytest.mark.parametrize("value", [Mock(), "some value"])
    def test_addressing_information__set__type_error(self, value):
        with pytest.raises(TypeError):
            CanSegmenter.addressing_information.fset(self.mock_can_segmenter, value=value)

    @pytest.mark.parametrize("value", [Mock(spec=AbstractCanAddressingInformation),
                                       Mock(spec=Normal11BitCanAddressingInformation)])
    def test_addressing_information__set(self, value):
        CanSegmenter.addressing_information.fset(self.mock_can_segmenter, value=value)
        assert self.mock_can_segmenter._CanSegmenter__addressing_information == value

    # dlc

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_dlc__get(self, value):
        self.mock_can_segmenter._CanSegmenter__dlc = value
        assert CanSegmenter.dlc.fget(self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", [0, CanDlcHandler.MIN_BASE_UDS_DLC - 1])
    def test_dlc__set__value_error(self, value):
        with pytest.raises(ValueError):
            CanSegmenter.dlc.fset(self.mock_can_segmenter, value=value)
        self.mock_validate_dlc.assert_called_once_with(value)

    @pytest.mark.parametrize("value", [CanDlcHandler.MIN_BASE_UDS_DLC, CanDlcHandler.MIN_BASE_UDS_DLC + 1])
    def test_dlc__set(self, value):
        CanSegmenter.dlc.fset(self.mock_can_segmenter, value=value)
        self.mock_validate_dlc.assert_called_once_with(value)
        assert self.mock_can_segmenter._CanSegmenter__dlc == value

    # use_data_optimization

    @pytest.mark.parametrize("value", [False, True])
    def test_use_data_optimization__get(self, value):
        self.mock_can_segmenter._CanSegmenter__use_data_optimization = value
        assert CanSegmenter.use_data_optimization.fget(self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", [False, True, "something"])
    def test_use_data_optimization__set(self, value):
        CanSegmenter.use_data_optimization.fset(self.mock_can_segmenter, value=value)
        assert self.mock_can_segmenter._CanSegmenter__use_data_optimization == bool(value)

    # filler_byte

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_filler_byte__get(self, value):
        self.mock_can_segmenter._CanSegmenter__filler_byte = value
        assert CanSegmenter.filler_byte.fget(self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_filler_byte__set(self, value):
        CanSegmenter.filler_byte.fset(self.mock_can_segmenter, value=value)
        self.mock_validate_raw_byte.assert_called_once_with(value)
        assert self.mock_can_segmenter._CanSegmenter__filler_byte == value

    # __physical_segmentation

    @pytest.mark.parametrize("message_payload_size", [CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE + 1,
                                                      CanFirstFrameHandler.MAX_LONG_FF_DL_VALUE + 23])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_physical_segmentation__too_long(self, mock_len, message_payload_size):
        mock_len.return_value = message_payload_size
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.PHYSICAL)
        with pytest.raises(SegmentationError):
            CanSegmenter._CanSegmenter__physical_segmentation(self=self.mock_can_segmenter, message=mock_message)
        mock_len.assert_called_once_with(mock_message.payload)

    @pytest.mark.parametrize("message_payload_size, max_payload", [
        (2, 2),
        (60, 62)
    ])
    @pytest.mark.parametrize("physical_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_physical_segmentation__sf_with_data_optimization(self, mock_len,
                                                              message_payload_size, max_payload, physical_ai):
        mock_len.return_value = message_payload_size
        self.mock_get_max_sf_payload_size.return_value = max_payload
        self.mock_can_segmenter.use_data_optimization = True
        self.mock_can_segmenter.tx_packets_physical_ai = physical_ai
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.PHYSICAL)
        packets = CanSegmenter._CanSegmenter__physical_segmentation(self=self.mock_can_segmenter,
                                                                    message=mock_message)
        assert isinstance(packets, tuple)
        assert len(packets) == 1
        assert packets[0] == self.mock_can_packet_class.return_value
        self.mock_get_max_sf_payload_size.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format,
            dlc=self.mock_can_segmenter.dlc)
        mock_len.assert_called_once_with(mock_message.payload)
        self.mock_can_packet_class.assert_called_once_with(packet_type=CanPacketType.SINGLE_FRAME,
                                                           payload=mock_message.payload,
                                                           dlc=None,
                                                           filler_byte=self.mock_can_segmenter.filler_byte,
                                                           **physical_ai)

    @pytest.mark.parametrize("message_payload_size, max_payload", [
        (2, 2),
        (60, 62)
    ])
    @pytest.mark.parametrize("physical_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_physical_segmentation__sf_without_data_optimization(self, mock_len,
                                                                 message_payload_size, max_payload, physical_ai):
        mock_len.return_value = message_payload_size
        self.mock_get_max_sf_payload_size.return_value = max_payload
        self.mock_can_segmenter.use_data_optimization = False
        self.mock_can_segmenter.tx_packets_physical_ai = physical_ai
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.PHYSICAL)
        packets = CanSegmenter._CanSegmenter__physical_segmentation(self=self.mock_can_segmenter,
                                                                    message=mock_message)
        assert isinstance(packets, tuple)
        assert len(packets) == 1
        assert packets[0] == self.mock_can_packet_class.return_value
        self.mock_get_max_sf_payload_size.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format, dlc=self.mock_can_segmenter.dlc)
        mock_len.assert_called_once_with(mock_message.payload)
        self.mock_can_packet_class.assert_called_once_with(packet_type=CanPacketType.SINGLE_FRAME,
                                                           payload=mock_message.payload,
                                                           dlc=self.mock_can_segmenter.dlc,
                                                           filler_byte=self.mock_can_segmenter.filler_byte,
                                                           **physical_ai)

    @pytest.mark.parametrize("message_payload_size, max_payload, ff_size, cf_size", [
        (3, 2, 1, 2),
        (150, 7, 6, 7),
    ])
    @pytest.mark.parametrize("physical_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_physical_segmentation__ff_cf_with_data_optimization(self, mock_len, physical_ai,
                                                                 message_payload_size, max_payload, ff_size,
                                                                 cf_size):
        mock_len.return_value = message_payload_size
        self.mock_get_max_sf_payload_size.return_value = max_payload
        self.mock_get_ff_payload_size.return_value = ff_size
        self.mock_get_max_cf_payload_size.return_value = cf_size
        self.mock_can_segmenter.use_data_optimization = True
        self.mock_can_segmenter.tx_packets_physical_ai = physical_ai
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.PHYSICAL,
                            payload=range(message_payload_size))
        packets = CanSegmenter._CanSegmenter__physical_segmentation(self=self.mock_can_segmenter,
                                                                    message=mock_message)
        assert isinstance(packets, tuple)
        cf_number = (message_payload_size - ff_size + cf_size - 1) // cf_size
        assert len(packets) == 1 + cf_number
        self.mock_get_max_sf_payload_size.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format, dlc=self.mock_can_segmenter.dlc)
        mock_len.assert_called_once_with(mock_message.payload)
        last_cf_payload = (message_payload_size - ff_size) % cf_size
        if last_cf_payload == 0:
            last_cf_payload = cf_size
        ff_call = call(packet_type=CanPacketType.FIRST_FRAME,
                       payload=mock_message.payload[:ff_size],
                       dlc=self.mock_can_segmenter.dlc,
                       data_length=message_payload_size,
                       **physical_ai)
        cf_calls = []
        for cf_i in range(cf_number - 1):
            cf_payload_i_start = ff_size + cf_i * cf_size
            cf_payload_i_stop = cf_payload_i_start + cf_size
            cf_call = call(packet_type=CanPacketType.CONSECUTIVE_FRAME,
                           payload=mock_message.payload[cf_payload_i_start:cf_payload_i_stop],
                           sequence_number=(cf_i + 1) % 0x10,
                           dlc=self.mock_can_segmenter.dlc,
                           filler_byte=self.mock_can_segmenter.filler_byte,
                           **physical_ai)
            cf_calls.append(cf_call)
        last_cf_call = call(packet_type=CanPacketType.CONSECUTIVE_FRAME,
                            payload=mock_message.payload[-last_cf_payload:],
                            dlc=None,
                            filler_byte=self.mock_can_segmenter.filler_byte,
                            sequence_number=cf_number % 16,
                            **physical_ai)
        self.mock_can_packet_class.assert_has_calls([ff_call, *cf_calls, last_cf_call])

    # __functional_segmentation

    @pytest.mark.parametrize("message_payload_size, max_payload", [
        (2, 1),
        (60, 59)
    ])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_functional_segmentation__too_long(self, mock_len, message_payload_size, max_payload):
        mock_len.return_value = message_payload_size
        self.mock_get_max_sf_payload_size.return_value = max_payload
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.FUNCTIONAL)
        with pytest.raises(SegmentationError):
            CanSegmenter._CanSegmenter__functional_segmentation(self=self.mock_can_segmenter, message=mock_message)
        self.mock_get_max_sf_payload_size.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format, dlc=self.mock_can_segmenter.dlc)
        mock_len.assert_called_once_with(mock_message.payload)

    @pytest.mark.parametrize("message_payload_size, max_payload", [
        (2, 2),
        (60, 62)
    ])
    @pytest.mark.parametrize("functional_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_functional_segmentation__with_data_optimization(self, mock_len, message_payload_size, max_payload,
                                                             functional_ai):
        mock_len.return_value = message_payload_size
        self.mock_get_max_sf_payload_size.return_value = max_payload
        self.mock_can_segmenter.use_data_optimization = True
        self.mock_can_segmenter.tx_packets_functional_ai = functional_ai
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.FUNCTIONAL)
        packets = CanSegmenter._CanSegmenter__functional_segmentation(self=self.mock_can_segmenter,
                                                                      message=mock_message)
        assert isinstance(packets, tuple)
        assert len(packets) == 1
        assert packets[0] == self.mock_can_packet_class.return_value
        self.mock_get_max_sf_payload_size.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format, dlc=self.mock_can_segmenter.dlc)
        mock_len.assert_called_once_with(mock_message.payload)
        self.mock_can_packet_class.assert_called_once_with(packet_type=CanPacketType.SINGLE_FRAME,
                                                           payload=mock_message.payload,
                                                           dlc=None,
                                                           filler_byte=self.mock_can_segmenter.filler_byte,
                                                           **functional_ai)

    @pytest.mark.parametrize("message_payload_size, max_payload", [
        (2, 2),
        (60, 62)
    ])
    @pytest.mark.parametrize("functional_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_functional_segmentation__without_data_optimization(self, mock_len, message_payload_size, max_payload,
                                                                functional_ai):
        mock_len.return_value = message_payload_size
        self.mock_get_max_sf_payload_size.return_value = max_payload
        self.mock_can_segmenter.use_data_optimization = False
        self.mock_can_segmenter.tx_packets_functional_ai = functional_ai
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.FUNCTIONAL)
        packets = CanSegmenter._CanSegmenter__functional_segmentation(self=self.mock_can_segmenter,
                                                                      message=mock_message)
        assert isinstance(packets, tuple)
        assert len(packets) == 1
        assert packets[0] == self.mock_can_packet_class.return_value
        self.mock_get_max_sf_payload_size.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format, dlc=self.mock_can_segmenter.dlc)
        mock_len.assert_called_once_with(mock_message.payload)
        self.mock_can_packet_class.assert_called_once_with(packet_type=CanPacketType.SINGLE_FRAME,
                                                           payload=mock_message.payload,
                                                           dlc=self.mock_can_segmenter.dlc,
                                                           filler_byte=self.mock_can_segmenter.filler_byte,
                                                           **functional_ai)

    # is_input_packet

    @pytest.mark.parametrize("frame_can_id, frame_data", [
        ("some ID", "some data"),
        (Mock(), MagicMock()),
    ])
    def test_is_input_packet__decoding_error(self, frame_can_id, frame_data):
        self.mock_can_ai_class.decode_packet_ai.side_effect = ValueError
        assert CanSegmenter.is_input_packet(self.mock_can_segmenter, can_id=frame_can_id, data=frame_data) is None

    @pytest.mark.parametrize("frame_can_id, frame_data, decoded_ai", [
        ("some ID", "some data", {"a": 1, "b": 2}),
        (Mock(), MagicMock(), MagicMock()),
    ])
    def test_is_input_packet__physical(self, frame_can_id, frame_data, decoded_ai):
        self.mock_can_ai_class.decode_packet_ai.return_value = decoded_ai
        mock_eq_physical = Mock(return_value=True)
        self.mock_can_segmenter.rx_packets_physical_ai = MagicMock(__eq__=mock_eq_physical)
        self.mock_can_segmenter.rx_packets_functional_ai = MagicMock(__eq__=Mock(return_value=False))
        assert CanSegmenter.is_input_packet(self.mock_can_segmenter, can_id=frame_can_id, data=frame_data) \
               == AddressingType.PHYSICAL
        mock_eq_physical.assert_called_once()

    @pytest.mark.parametrize("frame_can_id, frame_data, decoded_ai", [
        ("some ID", "some data", {"a": 1, "b": 2}),
        (Mock(), MagicMock(), MagicMock()),
    ])
    def test_is_input_packet__functional(self, frame_can_id, frame_data, decoded_ai):
        self.mock_can_ai_class.decode_packet_ai.return_value = decoded_ai
        mock_eq_functional = Mock(return_value=True)
        self.mock_can_segmenter.rx_packets_physical_ai = MagicMock(__eq__=Mock(return_value=False))
        self.mock_can_segmenter.rx_packets_functional_ai = MagicMock(__eq__=mock_eq_functional)
        assert CanSegmenter.is_input_packet(self.mock_can_segmenter, can_id=frame_can_id, data=frame_data) \
               == AddressingType.FUNCTIONAL
        mock_eq_functional.assert_called_once()

    @pytest.mark.parametrize("frame_can_id, frame_data, decoded_ai", [
        ("some ID", "some data", {"a": 1, "b": 2}),
        (Mock(), MagicMock(), MagicMock()),
    ])
    def test_is_input_packet__no_match(self, frame_can_id, frame_data, decoded_ai):
        self.mock_can_ai_class.decode_packet_ai.return_value = decoded_ai
        mock_eq_physical = Mock(return_value=False)
        mock_eq_functional = Mock(return_value=False)
        self.mock_can_segmenter.rx_packets_physical_ai = MagicMock(__eq__=mock_eq_physical)
        self.mock_can_segmenter.rx_packets_functional_ai = MagicMock(__eq__=mock_eq_functional)
        assert CanSegmenter.is_input_packet(self.mock_can_segmenter, can_id=frame_can_id, data=frame_data) is None
        mock_eq_physical.assert_called_once()
        mock_eq_functional.assert_called_once()

    # is_desegmented_message

    @pytest.mark.parametrize("packets", ["some packets", range(4)])
    def test_is_desegmented_message__value_error(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = False
        with pytest.raises(ValueError):
            CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock(), Mock()),
    ])
    def test_is_desegmented_message__not_implemented_error(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.return_value = True
        with pytest.raises(NotImplementedError):
            CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock(), Mock()),
    ])
    def test_is_desegmented_message__false__not_initial_packet(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.return_value = False
        assert CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.SINGLE_FRAME)],
        [Mock(packet_type=CanPacketType.SINGLE_FRAME), Mock()],
        (Mock(packet_type=CanPacketType.SINGLE_FRAME), Mock(), Mock()),
    ])
    def test_is_desegmented_message__single_frame(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.return_value = True
        assert CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets) \
               is (len(packets) == 1)
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, payload=[]), Mock()],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, payload=range(5)), Mock(), Mock()),
    ])
    def test_is_desegmented_message__first_frame__multiple_initial_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.return_value = True
        assert CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packets[0].packet_type), call(packets[1].packet_type)])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=11, payload=range(4)), Mock(payload=range(6))],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=143, payload=[0xFF] * 10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_desegmented_message__first_frame__too_little_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=10, payload=range(4)), Mock(payload=range(6)),
         Mock(payload=None)],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=54, payload=[0xFF] * 10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_desegmented_message__first_frame__too_many_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=11, payload=range(4)), Mock(payload=range(7))],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=100, payload=[0xFF] * 10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_desegmented_message__first_frame__true(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence_type.return_value = True
        self.mock_is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_desegmented_message(self=self.mock_can_segmenter, packets=packets) is True
        self.mock_can_segmenter.is_supported_packets_sequence_type.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    # get_flow_control_packet

    @pytest.mark.parametrize("flow_status, block_size, st_min", [
        (Mock(), Mock(), Mock()),
        ("flow_status", "block_size", "st_min"),
    ])
    @pytest.mark.parametrize("physical_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    def test_get_flow_control_packet__data_optimization(self, flow_status, block_size, st_min, physical_ai):
        self.mock_can_segmenter.tx_packets_physical_ai = physical_ai
        self.mock_can_segmenter.use_data_optimization = True
        assert CanSegmenter.get_flow_control_packet(self=self.mock_can_segmenter, flow_status=flow_status,
                                                    block_size=block_size, st_min=st_min) \
               == self.mock_can_packet_class.return_value
        self.mock_can_packet_class.assert_called_once_with(packet_type=CanPacketType.FLOW_CONTROL,
                                                           dlc=None,
                                                           filler_byte=self.mock_can_segmenter.filler_byte,
                                                           flow_status=flow_status,
                                                           block_size=block_size,
                                                           st_min=st_min,
                                                           **physical_ai)

    @pytest.mark.parametrize("flow_status, block_size, st_min", [
        (Mock(), Mock(), Mock()),
        ("flow_status", "block_size", "st_min"),
    ])
    @pytest.mark.parametrize("physical_ai", [{"p1": 1, "p2": 2, "p3": 3}, {"abc": "something", "xyz": "else"}])
    def test_get_flow_control_packet__no_data_optimization(self, flow_status, block_size, st_min, physical_ai):
        self.mock_can_segmenter.tx_packets_physical_ai = physical_ai
        self.mock_can_segmenter.use_data_optimization = False
        assert CanSegmenter.get_flow_control_packet(self=self.mock_can_segmenter, flow_status=flow_status,
                                                    block_size=block_size, st_min=st_min) \
               == self.mock_can_packet_class.return_value
        self.mock_can_packet_class.assert_called_once_with(packet_type=CanPacketType.FLOW_CONTROL,
                                                           dlc=self.mock_can_segmenter.dlc,
                                                           filler_byte=self.mock_can_segmenter.filler_byte,
                                                           flow_status=flow_status,
                                                           block_size=block_size,
                                                           st_min=st_min,
                                                           **physical_ai)

    # desegmentation

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock()),
    ])
    def test_desegmentation__segmentation_error(self, packets):
        self.mock_can_segmenter.is_desegmented_message.return_value = False
        with pytest.raises(SegmentationError):
            CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_desegmented_message.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_desegmentation__not_implemented(self, mock_isinstance, packets):
        self.mock_can_segmenter.is_desegmented_message.return_value = True
        mock_isinstance.return_value = False
        with pytest.raises(NotImplementedError):
            CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_desegmented_message.assert_called_once_with(packets)
        mock_isinstance.assert_called()

    @pytest.mark.parametrize("packets", [
        [Mock(spec=CanPacketRecord)],
        (Mock(spec=CanPacketRecord), Mock(spec=CanPacketRecord)),
    ])
    def test_desegmentation__records(self, packets):
        self.mock_can_segmenter.is_desegmented_message.return_value = True
        assert CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets) \
               == self.mock_uds_message_record_class.return_value
        self.mock_can_segmenter.is_desegmented_message.assert_called_once_with(packets)
        self.mock_uds_message_record_class.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [
        [Mock(spec=CanPacket, packet_type=CanPacketType.SINGLE_FRAME)],
        (Mock(spec=CanPacket, packet_type=CanPacketType.SINGLE_FRAME),),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_desegmentation__definition__unsegmented_message(self, mock_isinstance, packets):
        self.mock_can_segmenter.is_desegmented_message.return_value = True
        mock_isinstance.side_effect = lambda value, types: types == self.mock_can_packet_class and isinstance(value, CanPacket)
        assert CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets) \
               == self.mock_uds_message_class.return_value
        self.mock_can_segmenter.is_desegmented_message.assert_called_once_with(packets)
        self.mock_uds_message_class.assert_called_once_with(payload=packets[0].payload,
                                                            addressing_type=packets[0].addressing_type)

    @pytest.mark.parametrize("packets", [
        [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, data_length=10, payload=range(4)),
         Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, payload=range(4, 10))],
        (Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, data_length=214, payload=list(range(0, 100, 2))),
         Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, payload=None),
         Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, payload=list(range(100, 162))),
         Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, payload=list(range(100, 162))),
         Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, payload=list(range(0, 124, 2)))),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_desegmentation__definitions__segmented_message(self, mock_isinstance, packets):
        self.mock_can_segmenter.is_desegmented_message.return_value = True
        mock_isinstance.side_effect = lambda value, types: types == self.mock_can_packet_class and isinstance(value, CanPacket)
        assert CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets) \
               == self.mock_uds_message_class.return_value
        self.mock_can_segmenter.is_desegmented_message.assert_called_once_with(packets)
        total_payload = []
        for packet in packets:
            if packet.payload is not None:
                total_payload.extend(packet.payload)
        self.mock_uds_message_class.assert_called_once_with(payload=total_payload[:packets[0].data_length],
                                                            addressing_type=packets[0].addressing_type)

    @pytest.mark.parametrize("packets", [
        [Mock(spec=CanPacket)],
        (Mock(spec=CanPacket), Mock(spec=CanPacket)),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_desegmentation__definitions__segmentation_error(self, mock_isinstance, packets):
        self.mock_can_segmenter.is_desegmented_message.return_value = True
        mock_isinstance.side_effect = lambda value, types: types == self.mock_can_packet_class and isinstance(value, CanPacket)
        with pytest.raises(SegmentationError):
            CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_desegmented_message.assert_called_once_with(packets)

    # segmentation

    @pytest.mark.parametrize("message", [Mock(), "not a message"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmentation__type_error(self, mock_isinstance, message):
        mock_isinstance.side_effect = lambda value, types: types == self.mock_uds_message_class and isinstance(value,
                                                                                                               UdsMessage)
        with pytest.raises(TypeError):
            CanSegmenter.segmentation(self=self.mock_can_segmenter, message=message)

    @pytest.mark.parametrize("message", [Mock(spec=UdsMessage, addressing_type=None),
                                         Mock(spec=UdsMessage, addressing_type="Something new")])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmentation__not_implemented_error(self, mock_isinstance, message):
        mock_isinstance.side_effect = lambda value, types: types == self.mock_uds_message_class and isinstance(value,
                                                                                                               UdsMessage)
        with pytest.raises(NotImplementedError):
            CanSegmenter.segmentation(self=self.mock_can_segmenter, message=message)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmentation__functional(self, mock_isinstance):
        mock_isinstance.side_effect = lambda value, types: types == self.mock_uds_message_class and isinstance(value,
                                                                                                               UdsMessage)
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.FUNCTIONAL)
        assert CanSegmenter.segmentation(self=self.mock_can_segmenter, message=mock_message) \
               == self.mock_can_segmenter._CanSegmenter__functional_segmentation.return_value
        self.mock_can_segmenter._CanSegmenter__functional_segmentation.assert_called_once_with(mock_message)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmentation__physical(self, mock_isinstance):
        mock_isinstance.side_effect = lambda value, types: types == self.mock_uds_message_class and isinstance(value,
                                                                                                               UdsMessage)
        mock_message = Mock(spec=UdsMessage, addressing_type=AddressingType.PHYSICAL)
        assert CanSegmenter.segmentation(self=self.mock_can_segmenter, message=mock_message) \
               == self.mock_can_segmenter._CanSegmenter__physical_segmentation.return_value
        self.mock_can_segmenter._CanSegmenter__physical_segmentation.assert_called_once_with(mock_message)


@pytest.mark.integration
class TestCanSegmenterIntegration:
    """Integration tests for `CanSegmenter` class."""

    @pytest.mark.parametrize("addressing_information, frame_can_id, frame_data", [
        (Normal11BitCanAddressingInformation(rx_physical={"can_id": 0x611},
                                             tx_physical={"can_id": 0x612},
                                             rx_functional={"can_id": 0x6FE},
                                             tx_functional={"can_id": 0x6FF}), 0x611, [0x10, 0x01]),
        (NormalFixedCanAddressingInformation(rx_physical={"can_id": 0x18DA1234, "target_address": 0x12, "source_address": 0x34},
                                             tx_physical={"can_id": 0x18DA3412, "target_address": 0x34, "source_address": 0x12},
                                             rx_functional={"can_id": 0x18DBF0E1, "target_address": 0xF0, "source_address": 0xE1},
                                             tx_functional={"can_id": 0x18DBE1F0}), 0x18DA1234, [0xAB, 0xCD, 0x12, 0xF5]),
        (ExtendedCanAddressingInformation(rx_physical={"can_id": 0x1234, "target_address": 0xF0},
                                          tx_physical={"can_id": 0x1234, "target_address": 0xE2,},
                                          rx_functional={"can_id": 0xFEDCBA, "target_address": 0xBB},
                                          tx_functional={"can_id": 0xFEDCBA, "target_address": 0x12}), 0x1234, [0xF0, *range(63)]),
        (Mixed11BitCanAddressingInformation(rx_physical={"can_id": 0x645, "address_extension": 0x01},
                                            tx_physical={"can_id": 0x646, "address_extension": 0xFE},
                                            rx_functional={"can_id": 0x6DE, "address_extension": 0x05},
                                            tx_functional={"can_id": 0x6DF, "address_extension": 0xFF}), 0x645, [0x01, 0x3E]),
        (Mixed29BitCanAddressingInformation(rx_physical={"can_id": 0x18CEC2D0, "address_extension": 0x52, "target_address": 0xC2, "source_address": 0xD0},
                                            tx_physical={"can_id": 0x18CED0C2, "address_extension": 0xD8, "target_address": 0xD0, "source_address": 0xC2},
                                            rx_functional={"can_id": 0x18CD7186, "address_extension": 0x05, "target_address": 0x71, "source_address": 0x86},
                                            tx_functional={"can_id": 0x18CD8671, "address_extension": 0xFF}), 0x18CEC2D0, [0x52, 0x3E]),
    ])
    def test_is_input_packet__physical(self, addressing_information, frame_can_id, frame_data):
        can_segmenter = CanSegmenter(addressing_information=addressing_information)
        assert can_segmenter.is_input_packet(can_id=frame_can_id, data=frame_data) is AddressingType.PHYSICAL

    @pytest.mark.parametrize("addressing_information, frame_can_id, frame_data", [
        (Normal11BitCanAddressingInformation(rx_physical={"can_id": 0x611},
                                             tx_physical={"can_id": 0x612},
                                             rx_functional={"can_id": 0x6FE},
                                             tx_functional={"can_id": 0x6FF}), 0x6FE, [0x10, 0x01]),
        (NormalFixedCanAddressingInformation(rx_physical={"can_id": 0x18DA1234, "target_address": 0x12, "source_address": 0x34},
                                             tx_physical={"can_id": 0x18DA3412, "target_address": 0x34, "source_address": 0x12},
                                             rx_functional={"can_id": 0x18DBF0E1, "target_address": 0xF0, "source_address": 0xE1},
                                             tx_functional={"can_id": 0x18DBE1F0}), 0x18DBF0E1, [0xAB, 0xCD, 0x12, 0xF5]),
        (ExtendedCanAddressingInformation(rx_physical={"can_id": 0x1234, "target_address": 0xF0},
                                          tx_physical={"can_id": 0x1234, "target_address": 0xE2,},
                                          rx_functional={"can_id": 0xFEDCBA, "target_address": 0xBB},
                                          tx_functional={"can_id": 0xFEDCBA, "target_address": 0x12}), 0xFEDCBA, [0xBB, *range(63)]),
        (Mixed11BitCanAddressingInformation(rx_physical={"can_id": 0x645, "address_extension": 0x01},
                                            tx_physical={"can_id": 0x646, "address_extension": 0xFE},
                                            rx_functional={"can_id": 0x6DE, "address_extension": 0x05},
                                            tx_functional={"can_id": 0x6DF, "address_extension": 0xFF}), 0x6DE, [0x05, 0x3E]),
        (Mixed29BitCanAddressingInformation(rx_physical={"can_id": 0x18CEC2D0, "address_extension": 0x52, "target_address": 0xC2, "source_address": 0xD0},
                                            tx_physical={"can_id": 0x18CED0C2, "address_extension": 0xD8, "target_address": 0xD0, "source_address": 0xC2},
                                            rx_functional={"can_id": 0x18CD7186, "address_extension": 0x05, "target_address": 0x71, "source_address": 0x86},
                                            tx_functional={"can_id": 0x18CD8671, "address_extension": 0xFF}), 0x18CD7186, [0x05, 0x3E]),
    ])
    def test_is_input_packet__functional(self, addressing_information, frame_can_id, frame_data):
        can_segmenter = CanSegmenter(addressing_information=addressing_information)
        assert can_segmenter.is_input_packet(can_id=frame_can_id, data=frame_data) is AddressingType.FUNCTIONAL

    @pytest.mark.parametrize("addressing_information, frame_can_id, frame_data", [
        (Normal11BitCanAddressingInformation(rx_physical={"can_id": 0x611},
                                             tx_physical={"can_id": 0x612},
                                             rx_functional={"can_id": 0x6FE},
                                             tx_functional={"can_id": 0x6FF}), 0x6FF, [0x10, 0x01]),
        (NormalFixedCanAddressingInformation(rx_physical={"can_id": 0x18DA1234, "target_address": 0x12, "source_address": 0x34},
                                             tx_physical={"can_id": 0x18DA3412, "target_address": 0x34, "source_address": 0x12},
                                             rx_functional={"can_id": 0x18DBF0E1, "target_address": 0xF0, "source_address": 0xE1},
                                             tx_functional={"can_id": 0x18DBE1F0}), 0x18DA3412, [0xAB, 0xCD, 0x12, 0xF5]),
        (ExtendedCanAddressingInformation(rx_physical={"can_id": 0x1234, "target_address": 0xF0},
                                          tx_physical={"can_id": 0x1234, "target_address": 0xE2,},
                                          rx_functional={"can_id": 0xFEDCBA, "target_address": 0xBB},
                                          tx_functional={"can_id": 0xFEDCBA, "target_address": 0x12}), 0xFEDCBA, [0xF0, *range(63)]),
        (Mixed11BitCanAddressingInformation(rx_physical={"can_id": 0x645, "address_extension": 0x01},
                                            tx_physical={"can_id": 0x646, "address_extension": 0xFE},
                                            rx_functional={"can_id": 0x6DE, "address_extension": 0x05},
                                            tx_functional={"can_id": 0x6DF, "address_extension": 0xFF}), 0x646, [0xFE, 0x3E]),
        (Mixed29BitCanAddressingInformation(rx_physical={"can_id": 0x18CEC2D0, "address_extension": 0x52, "target_address": 0xC2, "source_address": 0xD0},
                                            tx_physical={"can_id": 0x18CED0C2, "address_extension": 0xD8, "target_address": 0xD0, "source_address": 0xC2},
                                            rx_functional={"can_id": 0x18CD7186, "address_extension": 0x05, "target_address": 0x71, "source_address": 0x86},
                                            tx_functional={"can_id": 0x18CD8671, "address_extension": 0xFF}), 0x18CD7186, [0x52, 0x3E]),
    ])
    def test_is_input_packet__false(self, addressing_information, frame_can_id, frame_data):
        can_segmenter = CanSegmenter(addressing_information=addressing_information)
        assert can_segmenter.is_input_packet(can_id=frame_can_id, data=frame_data) is None

    @pytest.mark.parametrize("addressing_information", [
        Normal11BitCanAddressingInformation(rx_physical={"can_id": 0x611},
                                            tx_physical={"can_id": 0x612},
                                            rx_functional={"can_id": 0x6FE},
                                            tx_functional={"can_id": 0x6FF}),
        NormalFixedCanAddressingInformation(rx_physical={"can_id": 0x18DA1234, "target_address": 0x12, "source_address": 0x34},
                                            tx_physical={"can_id": 0x18DA3412, "target_address": 0x34, "source_address": 0x12},
                                            rx_functional={"can_id": 0x18DBF0E1, "target_address": 0xF0, "source_address": 0xE1},
                                            tx_functional={"can_id": 0x18DBE1F0}),
        ExtendedCanAddressingInformation(rx_physical={"can_id": 0x1234, "target_address": 0xF0},
                                         tx_physical={"can_id": 0x1234, "target_address": 0xE2,},
                                         rx_functional={"can_id": 0xFEDCBA, "target_address": 0xBB},
                                         tx_functional={"can_id": 0xFEDCBA, "target_address": 0x12}),
        Mixed11BitCanAddressingInformation(rx_physical={"can_id": 0x645, "address_extension": 0x01},
                                           tx_physical={"can_id": 0x646, "address_extension": 0xFE},
                                           rx_functional={"can_id": 0x6DE, "address_extension": 0x05},
                                           tx_functional={"can_id": 0x6DF, "address_extension": 0xFF}),
        Mixed29BitCanAddressingInformation(rx_physical={"can_id": 0x18CEC2D0, "address_extension": 0x52, "target_address": 0xC2, "source_address": 0xD0},
                                           tx_physical={"can_id": 0x18CED0C2, "address_extension": 0xD8, "target_address": 0xD0, "source_address": 0xC2},
                                           rx_functional={"can_id": 0x18CD7186, "address_extension": 0x05, "target_address": 0x71, "source_address": 0x86},
                                           tx_functional={"can_id": 0x18CD8671, "address_extension": 0xFF}),
    ])
    @pytest.mark.parametrize("flow_Status, block_size, st_min", [
        (CanFlowStatus.Overflow, None, None),
        (CanFlowStatus.Wait, None, None),
        (CanFlowStatus.ContinueToSend, 0x00, 0xFF),
        (CanFlowStatus.ContinueToSend, 0xFF, 0x00),
    ])
    def test_get_flow_control_packet(self, addressing_information, flow_Status, block_size, st_min):
        can_segmenter = CanSegmenter(addressing_information=addressing_information)
        flow_control = can_segmenter.get_flow_control_packet(flow_status=flow_Status, block_size=block_size, st_min=st_min)
        assert flow_control.addressing_format == addressing_information.addressing_format
        assert flow_control.addressing_type == AddressingType.PHYSICAL
        assert flow_control.packet_type == CanPacketType.FLOW_CONTROL
        assert flow_control.flow_status == flow_Status
        if flow_Status == CanFlowStatus.ContinueToSend:
            assert flow_control.block_size == block_size
            assert flow_control.st_min == st_min

    @pytest.mark.parametrize("uds_message", [
        UdsMessage(payload=bytearray([0x54]), addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=(0x3E, 0x00), addressing_type=AddressingType.FUNCTIONAL),
        UdsMessage(payload=[0x62] + list(range(0xFF)), addressing_type=AddressingType.PHYSICAL),
    ])
    def test_segmentation_desegmentation(self, example_can_segmenter, uds_message):
        segmented_packets = example_can_segmenter.segmentation(uds_message)
        assert example_can_segmenter.desegmentation(segmented_packets) == uds_message

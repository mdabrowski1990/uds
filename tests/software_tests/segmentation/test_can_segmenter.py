import pytest
from mock import Mock, patch, call

from uds.segmentation.can_segmenter import CanSegmenter, \
    CanDlcHandler, CanPacket, CanPacketRecord, CanPacketType, CanFirstFrameHandler, \
    AddressingType, UdsMessage, DEFAULT_FILLER_BYTE, SegmentationError


class TestCanSegmenter:
    """Unit tests for `CanSegmenter` class."""

    SCRIPT_LOCATION = "uds.segmentation.can_segmenter"

    def setup(self):
        self.mock_can_segmenter = Mock(spec=CanSegmenter)
        # patching
        self._patcher_can_addressing_format_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat")
        self.mock_can_addressing_format_class = self._patcher_can_addressing_format_class.start()
        self._patcher_can_ai_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformation")
        self.mock_can_ai_class = self._patcher_can_ai_class.start()
        self._patcher_validate_dlc = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler.validate_dlc")
        self.mock_validate_dlc = self._patcher_validate_dlc.start()
        self._patcher_is_initial_packet_type = patch(f"{self.SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
        self.mock_is_initial_packet_type = self._patcher_is_initial_packet_type.start()
        self._patcher_get_max_sf_payload_size \
            = patch(f"{self.SCRIPT_LOCATION}.CanSingleFrameHandler.get_max_payload_size")
        self.mock_get_max_sf_payload_size = self._patcher_get_max_sf_payload_size.start()
        self._patcher_get_ff_payload_size = patch(f"{self.SCRIPT_LOCATION}.CanFirstFrameHandler.get_payload_size")
        self.mock_get_ff_payload_size = self._patcher_get_ff_payload_size.start()
        self._patcher_get_max_cf_payload_size \
            = patch(f"{self.SCRIPT_LOCATION}.CanConsecutiveFrameHandler.get_max_payload_size")
        self.mock_get_max_cf_payload_size = self._patcher_get_max_cf_payload_size.start()
        self._patcher_can_packet_class = patch(f"{self.SCRIPT_LOCATION}.CanPacket")
        self.mock_can_packet_class = self._patcher_can_packet_class.start()
        self._patcher_uds_message_class = patch(f"{self.SCRIPT_LOCATION}.UdsMessage")
        self.mock_uds_message_class = self._patcher_uds_message_class.start()
        self._patcher_uds_message_record_class = patch(f"{self.SCRIPT_LOCATION}.UdsMessageRecord")
        self.mock_uds_message_record_class = self._patcher_uds_message_record_class.start()
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()

    def teardown(self):
        self._patcher_can_addressing_format_class.stop()
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

    @pytest.mark.parametrize("addressing_format, physical_ai, functional_ai", [
        ("some format", "Addressing Info1 ", "Addressing Info 2"),
        ("Normal", None, {}),
    ])
    def test_init__mandatory_args(self, addressing_format, physical_ai, functional_ai):
        CanSegmenter.__init__(self=self.mock_can_segmenter,
                              addressing_format=addressing_format,
                              physical_ai=physical_ai,
                              functional_ai=functional_ai)
        assert self.mock_can_segmenter._CanSegmenter__addressing_format \
               == self.mock_can_addressing_format_class.return_value
        assert self.mock_can_segmenter.physical_ai == physical_ai
        assert self.mock_can_segmenter.functional_ai == functional_ai
        assert self.mock_can_segmenter.dlc == CanDlcHandler.MIN_BASE_UDS_DLC
        assert self.mock_can_segmenter.use_data_optimization is False
        assert self.mock_can_segmenter.filler_byte == DEFAULT_FILLER_BYTE
        self.mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)
        self.mock_can_addressing_format_class.assert_called_once_with(addressing_format)

    @pytest.mark.parametrize("addressing_format, physical_ai, functional_ai, dlc, use_data_optimization, filler_byte", [
        ("some format", "Addressing Info1 ", "Addressing Info 2", "DLC", "whether tyo use data optimization", "filler"),
        ("Normal", None, {}, 0xF, False, 0x71),
    ])
    def test_init__all_args(self, addressing_format, physical_ai, functional_ai, dlc, use_data_optimization,
                            filler_byte):
        CanSegmenter.__init__(self=self.mock_can_segmenter,
                              addressing_format=addressing_format,
                              physical_ai=physical_ai,
                              functional_ai=functional_ai,
                              dlc=dlc,
                              use_data_optimization=use_data_optimization,
                              filler_byte=filler_byte)
        assert self.mock_can_segmenter._CanSegmenter__addressing_format \
               == self.mock_can_addressing_format_class.return_value
        assert self.mock_can_segmenter.physical_ai == physical_ai
        assert self.mock_can_segmenter.functional_ai == functional_ai
        assert self.mock_can_segmenter.dlc == dlc
        assert self.mock_can_segmenter.use_data_optimization == use_data_optimization
        assert self.mock_can_segmenter.filler_byte == filler_byte
        self.mock_can_addressing_format_class.validate_member.assert_called_once_with(addressing_format)
        self.mock_can_addressing_format_class.assert_called_once_with(addressing_format)

    # supported_packet_classes

    def test_supported_packet_classes__get(self):
        assert CanSegmenter.supported_packet_classes.fget(self.mock_can_segmenter) \
               == (self.mock_can_packet_class, CanPacketRecord)

    # addressing_format

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_addressing_format__get(self, value):
        self.mock_can_segmenter._CanSegmenter__addressing_format = value
        assert CanSegmenter.addressing_format.fget(self.mock_can_segmenter) == value

    # physical_ai

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_physical_ai__get(self, value):
        self.mock_can_segmenter._CanSegmenter__physical_ai = value
        assert CanSegmenter.physical_ai.fget(self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"arg1": "something", "arg2": "something else"}])
    def test_physical_ai__set(self, value):
        CanSegmenter.physical_ai.fset(self.mock_can_segmenter, value=value)
        self.mock_can_ai_class.validate_packet_ai.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format,
            addressing_type=AddressingType.PHYSICAL,
            **value)
        assert self.mock_can_segmenter._CanSegmenter__physical_ai \
               == self.mock_can_ai_class.validate_packet_ai.return_value

    # functional_ai

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_functional_ai__get(self, value):
        self.mock_can_segmenter._CanSegmenter__functional_ai = value
        assert CanSegmenter.functional_ai.fget(self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"arg1": "something", "arg2": "something else"}])
    def test_functional_ai__set(self, value):
        CanSegmenter.functional_ai.fset(self.mock_can_segmenter, value=value)
        self.mock_can_ai_class.validate_packet_ai.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format,
            addressing_type=AddressingType.FUNCTIONAL,
            **value)
        assert self.mock_can_segmenter._CanSegmenter__functional_ai \
               == self.mock_can_ai_class.validate_packet_ai.return_value

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

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_use_data_optimization__get(self, value):
        self.mock_can_segmenter._CanSegmenter__use_data_optimization = value
        assert CanSegmenter.use_data_optimization.fget(self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", ["something", 5.5])
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

    # desegmentation

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock()),
    ])
    def test_desegmentation__segmentation_error(self, packets):
        self.mock_can_segmenter.is_complete_packets_sequence.return_value = False
        with pytest.raises(SegmentationError):
            CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_desegmentation__not_implemented(self, mock_isinstance, packets):
        self.mock_can_segmenter.is_complete_packets_sequence.return_value = True
        mock_isinstance.return_value = False
        with pytest.raises(NotImplementedError):
            CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)
        mock_isinstance.assert_called()

    @pytest.mark.parametrize("packets", [
        [Mock(spec=CanPacketRecord)],
        (Mock(spec=CanPacketRecord), Mock(spec=CanPacketRecord)),
    ])
    def test_desegmentation__records(self, packets):
        self.mock_can_segmenter.is_complete_packets_sequence.return_value = True
        assert CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets) \
               == self.mock_uds_message_record_class.return_value
        self.mock_can_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)
        self.mock_uds_message_record_class.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [
        [Mock(spec=CanPacket, packet_type=CanPacketType.SINGLE_FRAME)],
        (Mock(spec=CanPacket, packet_type=CanPacketType.SINGLE_FRAME),),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_desegmentation__definition__unsegmented_message(self, mock_isinstance, packets):
        self.mock_can_segmenter.is_complete_packets_sequence.return_value = True
        mock_isinstance.side_effect = lambda value, types: types == self.mock_can_packet_class and isinstance(value,
                                                                                                              CanPacket)
        assert CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets) \
               == self.mock_uds_message_class.return_value
        self.mock_can_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)
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
        self.mock_can_segmenter.is_complete_packets_sequence.return_value = True
        mock_isinstance.side_effect = lambda value, types: types == self.mock_can_packet_class and isinstance(value,
                                                                                                              CanPacket)
        assert CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets) \
               == self.mock_uds_message_class.return_value
        self.mock_can_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)
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
        self.mock_can_segmenter.is_complete_packets_sequence.return_value = True
        mock_isinstance.side_effect = lambda value, types: types == self.mock_can_packet_class and isinstance(value,
                                                                                                              CanPacket)
        with pytest.raises(SegmentationError):
            CanSegmenter.desegmentation(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)

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

    # is_complete_packets_sequence

    @pytest.mark.parametrize("packets", ["some packets", range(4)])
    def test_is_complete_packets_sequence__value_error(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = False
        with pytest.raises(ValueError):
            CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__not_implemented_error(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.return_value = True
        with pytest.raises(NotImplementedError):
            CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__false__not_initial_packet(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.return_value = False
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.SINGLE_FRAME)],
        [Mock(packet_type=CanPacketType.SINGLE_FRAME), Mock()],
        (Mock(packet_type=CanPacketType.SINGLE_FRAME), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__single_frame(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.return_value = True
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) \
               is (len(packets) == 1)
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, payload=[]), Mock()],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, payload=range(5)), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__first_frame__multiple_initial_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.return_value = True
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packets[0].packet_type), call(packets[1].packet_type)])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=11, payload=range(4)), Mock(payload=range(6))],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=143, payload=[0xFF] * 10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_complete_packets_sequence__first_frame__too_little_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=10, payload=range(4)), Mock(payload=range(6)),
         Mock(payload=None)],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=54, payload=[0xFF] * 10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_complete_packets_sequence__first_frame__too_many_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=11, payload=range(4)), Mock(payload=range(7))],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=100, payload=[0xFF] * 10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_complete_packets_sequence__first_frame__true(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is True
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

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
        self.mock_can_segmenter.physical_ai = physical_ai
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
        self.mock_can_segmenter.physical_ai = physical_ai
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
        self.mock_can_segmenter.physical_ai = physical_ai
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
        self.mock_can_segmenter.functional_ai = functional_ai
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
        self.mock_can_segmenter.functional_ai = functional_ai
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


@pytest.mark.integration
class TestCanSegmenterIntegration:
    """Integration tests for `CanSegmenter` class."""

    @pytest.mark.parametrize("uds_message", [
        UdsMessage(payload=bytearray([0x54]), addressing_type=AddressingType.PHYSICAL),
        UdsMessage(payload=(0x3E, 0x00), addressing_type=AddressingType.FUNCTIONAL),
        UdsMessage(payload=[0x62] + list(range(0xFF)), addressing_type=AddressingType.PHYSICAL),
    ])
    def test_segmentation_desegmentation(self, example_can_segmenter, uds_message):
        segmented_packets = example_can_segmenter.segmentation(uds_message)
        assert example_can_segmenter.desegmentation(segmented_packets) == uds_message
import pytest
from mock import Mock, patch, call

from uds.segmentation.can_segmenter import CanSegmenter, \
    CanDlcHandler, CanAddressingInformationHandler, CanPacket, CanPacketRecord, CanPacketType, \
    AddressingType, UdsMessage, DEFAULT_FILLER_BYTE


class TestCanSegmenter:
    """Unit tests for `CanSegmenter` class."""

    SCRIPT_LOCATION = "uds.segmentation.can_segmenter"

    def setup(self):
        self.mock_can_segmenter = Mock(spec=CanSegmenter)
        mock_can_ai_handler_class = Mock(ADDRESSING_TYPE_NAME=CanAddressingInformationHandler.ADDRESSING_TYPE_NAME)
        mock_can_packet_type_class = Mock(SINGLE_FRAME=CanPacketType.SINGLE_FRAME,
                                          FIRST_FRAME=CanPacketType.FIRST_FRAME,
                                          CONSECUTIVE_FRAME=CanPacketType.CONSECUTIVE_FRAME,
                                          FLOW_CONTROL=CanPacketType.FLOW_CONTROL)
        # patching
        self._patcher_validate_raw_byte = patch(f"{self.SCRIPT_LOCATION}.validate_raw_byte")
        self.mock_validate_raw_byte = self._patcher_validate_raw_byte.start()
        self._patcher_addressing_type_class = patch(f"{self.SCRIPT_LOCATION}.AddressingType")
        self.mock_addressing_type_class = self._patcher_addressing_type_class.start()
        self._patcher_can_dlc_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler_class = self._patcher_can_dlc_handler_class.start()
        self._patcher_can_addressing_format_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingFormat")
        self.mock_can_addressing_format_class = self._patcher_can_addressing_format_class.start()
        self._patcher_can_ai_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanAddressingInformationHandler",
                                                   mock_can_ai_handler_class)
        self.mock_can_ai_handler_class = self._patcher_can_ai_handler_class.start()
        self._patcher_can_packet_type_class = patch(f"{self.SCRIPT_LOCATION}.CanPacketType", mock_can_packet_type_class)
        self.mock_can_packet_type_class = self._patcher_can_packet_type_class.start()

    def teardown(self):
        self._patcher_validate_raw_byte.stop()
        self._patcher_addressing_type_class.stop()
        self._patcher_can_dlc_handler_class.stop()
        self._patcher_can_addressing_format_class.stop()
        self._patcher_can_ai_handler_class.stop()
        self._patcher_can_packet_type_class.stop()

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
    def test_init__all_args(self, addressing_format, physical_ai, functional_ai, dlc, use_data_optimization, filler_byte):
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

    # addressing_format

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_addressing_format__get(self, value):
        self.mock_can_segmenter._CanSegmenter__addressing_format = value
        assert CanSegmenter.addressing_format.fget(self=self.mock_can_segmenter) == value

    # physical_ai

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_physical_ai__get(self, value):
        self.mock_can_segmenter._CanSegmenter__physical_ai = value
        assert CanSegmenter.physical_ai.fget(self=self.mock_can_segmenter) == value

    def test_physical_ai__set__none(self):
        CanSegmenter.physical_ai.fset(self=self.mock_can_segmenter, value=None)
        self.mock_can_ai_handler_class.validate_ai.assert_not_called()
        assert self.mock_can_segmenter._CanSegmenter__physical_ai is None

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"arg1": "something", "arg2": "something else"}])
    def test_physical_ai__set(self, value):
        CanSegmenter.physical_ai.fset(self=self.mock_can_segmenter, value=value)
        self.mock_can_ai_handler_class.validate_ai.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format,
            addressing_type=self.mock_addressing_type_class.PHYSICAL,
            **value)
        assert isinstance(self.mock_can_segmenter._CanSegmenter__physical_ai, dict)
        assert all([self.mock_can_segmenter._CanSegmenter__physical_ai[arg_name] == arg_value
                    for arg_name, arg_value in value.items()])
        assert self.mock_can_segmenter._CanSegmenter__physical_ai[self.mock_can_ai_handler_class.ADDRESSING_TYPE_NAME] \
               == self.mock_addressing_type_class.PHYSICAL

    # functional_ai

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_functional_ai__get(self, value):
        self.mock_can_segmenter._CanSegmenter__functional_ai = value
        assert CanSegmenter.functional_ai.fget(self=self.mock_can_segmenter) == value

    def test_functional_ai__set__none(self):
        CanSegmenter.functional_ai.fset(self=self.mock_can_segmenter, value=None)
        self.mock_can_ai_handler_class.validate_ai.assert_not_called()
        assert self.mock_can_segmenter._CanSegmenter__functional_ai is None

    @pytest.mark.parametrize("value", [{"a": 1, "b": 2}, {"arg1": "something", "arg2": "something else"}])
    def test_functional_ai__set(self, value):
        CanSegmenter.functional_ai.fset(self=self.mock_can_segmenter, value=value)
        self.mock_can_ai_handler_class.validate_ai.assert_called_once_with(
            addressing_format=self.mock_can_segmenter.addressing_format,
            addressing_type=self.mock_addressing_type_class.FUNCTIONAL,
            **value)
        assert isinstance(self.mock_can_segmenter._CanSegmenter__functional_ai, dict)
        assert all([self.mock_can_segmenter._CanSegmenter__functional_ai[arg_name] == arg_value
                    for arg_name, arg_value in value.items()])
        assert self.mock_can_segmenter._CanSegmenter__functional_ai[self.mock_can_ai_handler_class.ADDRESSING_TYPE_NAME] \
               == self.mock_addressing_type_class.FUNCTIONAL

    # dlc

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_dlc__get(self, value):
        self.mock_can_segmenter._CanSegmenter__dlc = value
        assert CanSegmenter.dlc.fget(self=self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_dlc__set(self, value):
        CanSegmenter.dlc.fset(self=self.mock_can_segmenter, value=value)
        self.mock_can_dlc_handler_class.validate_dlc.assert_called_once_with(value)
        assert self.mock_can_segmenter._CanSegmenter__dlc == value
        
    # use_data_optimization

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_use_data_optimization__get(self, value):
        self.mock_can_segmenter._CanSegmenter__use_data_optimization = value
        assert CanSegmenter.use_data_optimization.fget(self=self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_use_data_optimization__set(self, value):
        CanSegmenter.use_data_optimization.fset(self=self.mock_can_segmenter, value=value)
        assert self.mock_can_segmenter._CanSegmenter__use_data_optimization == bool(value)

    # filler_byte

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_filler_byte__get(self, value):
        self.mock_can_segmenter._CanSegmenter__filler_byte = value
        assert CanSegmenter.filler_byte.fget(self=self.mock_can_segmenter) == value

    @pytest.mark.parametrize("value", ["something", 5.5])
    def test_filler_byte__set(self, value):
        CanSegmenter.filler_byte.fset(self=self.mock_can_segmenter, value=value)
        self.mock_validate_raw_byte.assert_called_once_with(value)
        assert self.mock_can_segmenter._CanSegmenter__filler_byte == value

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
        self.mock_can_packet_type_class.is_initial_packet_type.return_value = True
        with pytest.raises(NotImplementedError):
            CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets)
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock()],
        (Mock(), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__false__not_initial_packet(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_can_packet_type_class.is_initial_packet_type.return_value = False
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.SINGLE_FRAME)],
        [Mock(packet_type=CanPacketType.SINGLE_FRAME), Mock()],
        (Mock(packet_type=CanPacketType.SINGLE_FRAME), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__single_frame(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_can_packet_type_class.is_initial_packet_type.return_value = True
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) \
               is (len(packets) == 1)
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_called_once_with(packets[0].packet_type)

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, payload=[]), Mock()],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, payload=range(5)), Mock(), Mock()),
    ])
    def test_is_complete_packets_sequence__first_frame__multiple_initial_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_can_packet_type_class.is_initial_packet_type.return_value = True
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_has_calls(
            [call(packets[0].packet_type), call(packets[1].packet_type)])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=11, payload=range(4)), Mock(payload=range(6))],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=143, payload=[0xFF]*10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_complete_packets_sequence__first_frame__too_little_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_can_packet_type_class.is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=10, payload=range(4)), Mock(payload=range(6)),
         Mock(payload=None)],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=54, payload=[0xFF]*10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_complete_packets_sequence__first_frame__too_many_packets(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_can_packet_type_class.is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is False
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])

    @pytest.mark.parametrize("packets", [
        [Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=11, payload=range(4)), Mock(payload=range(7))],
        (Mock(packet_type=CanPacketType.FIRST_FRAME, data_length=100, payload=[0xFF]*10), Mock(payload=None),
         Mock(payload=range(50, 100)), Mock(payload=range(150, 200))),
    ])
    def test_is_complete_packets_sequence__first_frame__true(self, packets):
        self.mock_can_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_can_packet_type_class.is_initial_packet_type.side_effect = [True] + (len(packets) - 1) * [False]
        assert CanSegmenter.is_complete_packets_sequence(self=self.mock_can_segmenter, packets=packets) is True
        self.mock_can_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_can_packet_type_class.is_initial_packet_type.assert_has_calls(
            [call(packet.packet_type) for packet in packets])


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

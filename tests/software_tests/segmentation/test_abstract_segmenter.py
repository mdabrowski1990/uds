import pytest
from mock import Mock, patch, MagicMock

from uds.segmentation.abstract_segmenter import AbstractSegmenter, SegmentationError, \
    UdsMessage, UdsMessageRecord
from uds.messages import AbstractUdsPacket, AbstractUdsPacketRecord


class TestAbstractSegmenter:
    """Tests for `AbstractSegmenter` class."""

    SCRIPT_PATH = "uds.segmentation.abstract_segmenter"

    def setup(self):
        self.mock_abstract_segmenter = Mock(spec=AbstractSegmenter)

    # is_supported_packet

    @pytest.mark.parametrize("result", [True, False])
    @pytest.mark.parametrize("value", [None, 5, "some value", Mock()])
    @patch(f"{SCRIPT_PATH}.isinstance")
    def test_is_supported_packet(self, mock_isinstance, value, result):
        mock_isinstance.return_value = result
        assert AbstractSegmenter.is_supported_packet(self=self.mock_abstract_segmenter, value=value) is result
        mock_isinstance.assert_called_once_with(value, self.mock_abstract_segmenter.supported_packet_classes)

    # is_supported_packets_sequence

    @pytest.mark.parametrize("value", [None, True, 1, Mock(), {1, 2, 3}])
    def test_is_supported_packets_sequence__false__invalid_type(self, value):
        assert AbstractSegmenter.is_supported_packets_sequence(self=self.mock_abstract_segmenter, value=value) is False
        self.mock_abstract_segmenter.is_supported_packet.assert_not_called()

    @pytest.mark.parametrize("value", [
        (1, 2, 3, 4),
        (1, 2.1, 3, 4.4),
        [2.2, 3.3, 4.4],
        [None, True, False],
        (True, False),
    ])
    def test_is_supported_packets_sequence__false__invalid_elements_type(self, value):
        self.mock_abstract_segmenter.is_supported_packet.return_value = False
        assert AbstractSegmenter.is_supported_packets_sequence(self=self.mock_abstract_segmenter, value=value) is False
        self.mock_abstract_segmenter.is_supported_packet.assert_called_once()

    @pytest.mark.parametrize("value", [
        (1, 2.1, 3, 4.4),
        [None, True, False],
    ])
    def test_is_supported_packets_sequence__false__more_element_types(self, value):
        self.mock_abstract_segmenter.is_supported_packet.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence(self=self.mock_abstract_segmenter, value=value) is False
        self.mock_abstract_segmenter.is_supported_packet.assert_called()

    def test_is_supported_packets_sequence__false__empty_sequence(self):
        self.mock_abstract_segmenter.is_supported_packet.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence(self=self.mock_abstract_segmenter, value=[]) is False

    @pytest.mark.parametrize("value", [
        (1, 2, 3, 4),
        [2.2, 3.3, 4.4],
        (True, False),
    ])
    def test_is_supported_packets_sequence__true(self, value):
        self.mock_abstract_segmenter.is_supported_packet.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence(self=self.mock_abstract_segmenter, value=value) is True
        self.mock_abstract_segmenter.is_supported_packet.assert_called()

    # get_consecutive_packets_number

    @pytest.mark.parametrize("packet", [Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacketRecord)])
    def test_get_consecutive_packets_number__value_error(self, packet):
        self.mock_abstract_segmenter.is_initial_packet.return_value = False
        with pytest.raises(ValueError):
            AbstractSegmenter.get_consecutive_packets_number(self=self.mock_abstract_segmenter, first_packet=packet)
        self.mock_abstract_segmenter.is_initial_packet.assert_called_once_with(packet)

    @pytest.mark.parametrize("packet", [Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacketRecord)])
    def test_get_consecutive_packets_number__valid(self, packet):
        self.mock_abstract_segmenter.is_initial_packet.return_value = True
        AbstractSegmenter.get_consecutive_packets_number(self=self.mock_abstract_segmenter, first_packet=packet)
        self.mock_abstract_segmenter.is_initial_packet.assert_called_once_with(packet)

    # is_following_packets_sequence

    @pytest.mark.parametrize("packets", [
        (1, 2, 3, 4),
        (1, 2.1, 3, 4.4),
        [2.2, 3.3, 4.4],
        [None, True, False],
        (True, False),
    ])
    def test_is_following_packets_sequence__value_error(self, packets):
        self.mock_abstract_segmenter.is_supported_packets_sequence.return_value = False
        with pytest.raises(ValueError):
            AbstractSegmenter.is_following_packets_sequence(self=self.mock_abstract_segmenter, packets=packets)
        self.mock_abstract_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_abstract_segmenter.is_initial_packet.assert_not_called()

    @pytest.mark.parametrize("packets", [
        (1, 2, 3, 4),
        (1, 2.1, 3, 4.4),
        [2.2, 3.3, 4.4],
        [None, True, False],
        (True, False),
    ])
    def test_is_following_packets_sequence__false(self, packets):
        self.mock_abstract_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_abstract_segmenter.is_initial_packet.return_value = False
        assert AbstractSegmenter.is_following_packets_sequence(self=self.mock_abstract_segmenter, packets=packets) is False
        self.mock_abstract_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_abstract_segmenter.is_initial_packet.assert_called_once_with(packets[0])

    @pytest.mark.parametrize("packets", [
        (1, 2, 3, 4),
        (1, 2.1, 3, 4.4),
        [2.2, 3.3, 4.4],
        [None, True, False],
        (True, False),
    ])
    def test_is_following_packets_sequence__valid(self, packets):
        self.mock_abstract_segmenter.is_supported_packets_sequence.return_value = True
        self.mock_abstract_segmenter.is_initial_packet.return_value = True
        assert AbstractSegmenter.is_following_packets_sequence(self=self.mock_abstract_segmenter, packets=packets) is None
        self.mock_abstract_segmenter.is_supported_packets_sequence.assert_called_once_with(packets)
        self.mock_abstract_segmenter.is_initial_packet.assert_called_once_with(packets[0])

    # is_complete_packets_sequence

    @pytest.mark.parametrize("packets", [
        (Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacket)),
        [Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord)],
    ])
    def test_is_complete_packets_sequence__not_a_sequence(self, packets):
        self.mock_abstract_segmenter.is_following_packets_sequence.return_value = False
        assert AbstractSegmenter.is_complete_packets_sequence(self=self.mock_abstract_segmenter, packets=packets) is False
        self.mock_abstract_segmenter.is_following_packets_sequence.assert_called_once_with(packets)
        self.mock_abstract_segmenter.get_consecutive_packets_number.assert_not_called()

    @pytest.mark.parametrize("packets", [
        (Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacket)),
        [Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord)],
    ])
    def test_is_complete_packets_sequence__invalid_packets_number(self, packets):
        mock_eq_false = MagicMock()
        mock_eq_false.__eq__.return_value = False
        self.mock_abstract_segmenter.is_following_packets_sequence.return_value = True
        self.mock_abstract_segmenter.get_consecutive_packets_number.return_value = mock_eq_false
        assert AbstractSegmenter.is_complete_packets_sequence(self=self.mock_abstract_segmenter, packets=packets) is False
        self.mock_abstract_segmenter.is_following_packets_sequence.assert_called_once_with(packets)
        self.mock_abstract_segmenter.get_consecutive_packets_number.assert_called_once_with(packets[0])
        mock_eq_false.__eq__.assert_called_once_with(len(packets))

    @pytest.mark.parametrize("packets", [
        (Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacket)),
        [Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord)],
    ])
    def test_is_complete_packets_sequence__true(self, packets):
        self.mock_abstract_segmenter.is_following_packets_sequence.return_value = True
        self.mock_abstract_segmenter.get_consecutive_packets_number.return_value = len(packets)
        assert AbstractSegmenter.is_complete_packets_sequence(self=self.mock_abstract_segmenter, packets=packets) is True
        self.mock_abstract_segmenter.is_following_packets_sequence.assert_called_once_with(packets)
        self.mock_abstract_segmenter.get_consecutive_packets_number.assert_called_once_with(packets[0])

    # segmentation

    @pytest.mark.parametrize("message", [None, False, Mock(spec=UdsMessageRecord), (0x1, 0x2, 0x3)])
    def test_segmentation__type_error(self, message):
        with pytest.raises(TypeError):
            AbstractSegmenter.segmentation(self=self.mock_abstract_segmenter, message=message)

    def test_segmentation__valid_input(self):
        AbstractSegmenter.segmentation(self=self.mock_abstract_segmenter, message=Mock(spec=UdsMessage))

    # desegmentation

    @pytest.mark.parametrize("packets", [None, "some packets", [1, 2, 3]])
    def test_desegmentation__segmentation_error(self, packets):
        self.mock_abstract_segmenter.is_complete_packets_sequence.return_value = False
        with pytest.raises(SegmentationError):
            AbstractSegmenter.desegmentation(self=self.mock_abstract_segmenter, packets=packets)
        self.mock_abstract_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)

    @pytest.mark.parametrize("packets", [None, "some packets", [1, 2, 3]])
    def test_desegmentation__valid_input(self, packets):
        self.mock_abstract_segmenter.is_complete_packets_sequence.return_value = True
        AbstractSegmenter.desegmentation(self=self.mock_abstract_segmenter, packets=packets)
        self.mock_abstract_segmenter.is_complete_packets_sequence.assert_called_once_with(packets)

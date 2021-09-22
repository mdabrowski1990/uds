import pytest
from mock import Mock

from uds.segmentation.abstract_segmenter import AbstractSegmenter, SegmentationError, \
    UdsMessage, UdsMessageRecord, AbstractUdsPacket, AbstractUdsPacketRecord


class TestAbstractSegmenter:

    def setup(self):
        self.mock_abstract_segmenter = Mock(spec=AbstractSegmenter)

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
        self.mock_abstract_segmenter.is_complete_packet_set = Mock(return_value=False)
        with pytest.raises(SegmentationError):
            AbstractSegmenter.desegmentation(self=self.mock_abstract_segmenter, packets=packets)
        self.mock_abstract_segmenter.is_complete_packet_set.assert_called_once_with(packets=packets)

    @pytest.mark.parametrize("packets", [None, "some packets", [1, 2, 3]])
    def test_desegmentation__valid_input(self, packets):
        self.mock_abstract_segmenter.is_complete_packet_set = Mock(return_value=True)
        AbstractSegmenter.desegmentation(self=self.mock_abstract_segmenter, packets=packets)
        self.mock_abstract_segmenter.is_complete_packet_set.assert_called_once_with(packets=packets)

    # is_complete_packet_set

    @pytest.mark.parametrize("packets", [None, False, 505, Mock(), "not packets"])
    def test_is_complete_packet_set__type_error(self, packets):
        with pytest.raises(TypeError):
            AbstractSegmenter.is_complete_packet_set(self=self.mock_abstract_segmenter, packets=packets)

    @pytest.mark.parametrize("packets", [
        (1, 2, 3, 4),
        [True, False],
        (None, ),
        [Mock(), Mock()],
        [Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacketRecord)],
        (Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacket)),
    ])
    def test_is_complete_packet_set__value_error(self, packets):
        with pytest.raises(ValueError):
            AbstractSegmenter.is_complete_packet_set(self=self.mock_abstract_segmenter, packets=packets)

    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacket)],
        [Mock(spec=AbstractUdsPacketRecord)],
        (Mock(spec=AbstractUdsPacketRecord), Mock(spec=AbstractUdsPacketRecord)),
        (Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacket)),
    ])
    def test_is_complete_packet_set__valid_input(self, packets):
        AbstractSegmenter.is_complete_packet_set(self=self.mock_abstract_segmenter, packets=packets)

    # is_first_packet

    @pytest.mark.parametrize("packet", [None, True, "not a packet", 232, Mock(), [0x1, 0x2, 0x3]])
    def test_is_first_packet__type_error(self, packet):
        with pytest.raises(TypeError):
            AbstractSegmenter.is_first_packet(self=self.mock_abstract_segmenter, packet=packet)

    @pytest.mark.parametrize("packet", [Mock(spec=AbstractUdsPacket), Mock(spec=AbstractUdsPacketRecord)])
    def test_is_first_packet__valid_input(self, packet):
        AbstractSegmenter.is_first_packet(self=self.mock_abstract_segmenter, packet=packet)

    # get_consecutive_packets_needed

    @pytest.mark.parametrize("packet", [None, True, "a packet", 6321, [0x1, 0x2, 0x3], Mock(spec=AbstractUdsPacket)])
    def test_get_consecutive_packets_needed__value_error(self, packet):
        self.mock_abstract_segmenter.is_first_packet.return_value = False
        with pytest.raises(ValueError):
            AbstractSegmenter.get_consecutive_packets_number(self=self.mock_abstract_segmenter, first_packet=packet)
        self.mock_abstract_segmenter.is_first_packet.assert_called_once_with(packet=packet)

    @pytest.mark.parametrize("packet", [None, True, "a packet", 6321, [0x1, 0x2, 0x3], Mock(spec=AbstractUdsPacket)])
    def test_get_consecutive_packets_needed__valid_input(self, packet):
        self.mock_abstract_segmenter.is_first_packet.return_value = True
        AbstractSegmenter.get_consecutive_packets_number(self=self.mock_abstract_segmenter, first_packet=packet)
        self.mock_abstract_segmenter.is_first_packet.assert_called_once_with(packet=packet)

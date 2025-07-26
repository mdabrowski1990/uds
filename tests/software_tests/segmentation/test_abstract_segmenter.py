import pytest
from mock import Mock, call, patch

from uds.segmentation.abstract_segmenter import AbstractSegmenter, Sequence

SCRIPT_LOCATION = "uds.segmentation.abstract_segmenter"


class TestAbstractSegmenter:
    """Unit tests for `AbstractSegmenter` class."""

    def setup_method(self):
        self.mock_abstract_segmenter = Mock(spec=AbstractSegmenter)

    # __init__

    @pytest.mark.parametrize("addressing_information", [Mock(), "some value"])
    def test_init(self, addressing_information):
        assert AbstractSegmenter.__init__(self.mock_abstract_segmenter,
                                          addressing_information=addressing_information) is None
        assert self.mock_abstract_segmenter.addressing_information == addressing_information

    # addressing_information

    def test_addressing_information__get(self):
        self.mock_abstract_segmenter._AbstractSegmenter__addressing_information = Mock()
        assert (AbstractSegmenter.addressing_information.fget(self.mock_abstract_segmenter)
                == self.mock_abstract_segmenter._AbstractSegmenter__addressing_information)

    @pytest.mark.parametrize("addressing_information", [Mock(), "some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_addressing_information__set(self, mock_isinstance,
                                         addressing_information):
        mock_isinstance.return_value = True
        assert AbstractSegmenter.addressing_information.fset(self.mock_abstract_segmenter,
                                                             addressing_information) is None
        assert self.mock_abstract_segmenter._AbstractSegmenter__addressing_information == addressing_information
        mock_isinstance.assert_called_once_with(addressing_information,
                                                self.mock_abstract_segmenter.supported_addressing_information_class)

    @pytest.mark.parametrize("addressing_information", [Mock(), "some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_addressing_information__set__type_error(self, mock_isinstance,
                                         addressing_information):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractSegmenter.addressing_information.fset(self.mock_abstract_segmenter, addressing_information)
        mock_isinstance.assert_called_once_with(addressing_information,
                                                self.mock_abstract_segmenter.supported_addressing_information_class)

    # is_supported_packet_type

    @pytest.mark.parametrize("value, result", [
        (Mock(), True),
        (Mock(), False),
        ("some packet", True),
        ("not a packet", False),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_supported_packet_type(self, mock_isinstance,
                                      value, result):
        mock_isinstance.return_value = result
        assert AbstractSegmenter.is_supported_packet_type(self=self.mock_abstract_segmenter, packet=value) is result
        mock_isinstance.assert_called_once_with(value, (self.mock_abstract_segmenter.supported_packet_class,
                                                        self.mock_abstract_segmenter.supported_packet_record_class))

    # is_supported_packets_sequence_type

    @pytest.mark.parametrize("value", [Mock(), "some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_supported_packets_sequence_type__false__not_sequence(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is False
        mock_isinstance.assert_called_once_with(value, Sequence)
        self.mock_abstract_segmenter.is_supported_packet_type.assert_not_called()

    @pytest.mark.parametrize("value", [range(10), "some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_supported_packets_sequence_type__false__not_packets(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = False
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is False
        mock_isinstance.assert_called_once_with(value, Sequence)
        self.mock_abstract_segmenter.is_supported_packet_type.assert_called_once()

    @pytest.mark.parametrize("value", [
        (1, 2.1, 3, 4.4),
        [None, True, False],
    ])
    def test_is_supported_packets_sequence_type__false__multiple_packet_types(self, value):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is False
        self.mock_abstract_segmenter.is_supported_packet_type.assert_called()

    def test_is_supported_packets_sequence_type__false__empty_sequence(self):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=[]) is False

    @pytest.mark.parametrize("value", [
        (1., 2.1, 4.4),
        [True, False],
    ])
    def test_is_supported_packets_sequence_type__true(self, value):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is True
        self.mock_abstract_segmenter.is_supported_packet_type.assert_has_calls(
            [call(element) for element in value], any_order=True)

    # is_input_packet

    @pytest.mark.parametrize("frame_attributes", [
        {"data": list(range(10)), "can_id": 0x7BF},
        {"data": list(range(100, 256)), "mac": "AB:CD:EF:98", "ip": "126.1.0.32"},
    ])
    def test_is_input_packet(self, frame_attributes):
        assert (AbstractSegmenter.is_input_packet(self.mock_abstract_segmenter, **frame_attributes)
                == self.mock_abstract_segmenter.addressing_information.is_input_packet.return_value)
        self.mock_abstract_segmenter.addressing_information.is_input_packet.assert_called_once_with(**frame_attributes)

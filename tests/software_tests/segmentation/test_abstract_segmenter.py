import pytest
from mock import Mock, patch

from uds.segmentation.abstract_segmenter import AbstractSegmenter


SCRIPT_PATH = "uds.segmentation.abstract_segmenter"


class TestAbstractSegmenter:
    """Unit tests for `AbstractSegmenter` class."""

    def setup_method(self):
        self.mock_abstract_segmenter = Mock(spec=AbstractSegmenter)

    # is_supported_packet_type

    @pytest.mark.parametrize("result", [True, False])
    @pytest.mark.parametrize("value", [None, 5, "some value", Mock()])
    @patch(f"{SCRIPT_PATH}.isinstance")
    def test_is_supported_packet_type(self, mock_isinstance, value, result):
        mock_isinstance.return_value = result
        assert AbstractSegmenter.is_supported_packet_type(self=self.mock_abstract_segmenter, packet=value) is result
        mock_isinstance.assert_called_once_with(value, (self.mock_abstract_segmenter.supported_packet_class,
                                                        self.mock_abstract_segmenter.supported_packet_record_class))

    # is_supported_packets_sequence_type

    @pytest.mark.parametrize("value", [None, True, 1, Mock(), {1, 2, 3}])
    def test_is_supported_packets_sequence_type__false__invalid_type(self, value):
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is False
        self.mock_abstract_segmenter.is_supported_packet_type.assert_not_called()

    @pytest.mark.parametrize("value", [
        (1, 2, 3, 4),
        (1, 2.1, 3, 4.4),
        [2.2, 3.3, 4.4],
        [None, True, False],
        (True, False),
    ])
    def test_is_supported_packets_sequence_type__false__invalid_elements_type(self, value):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = False
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is False
        self.mock_abstract_segmenter.is_supported_packet_type.assert_called_once()

    @pytest.mark.parametrize("value", [
        (1, 2.1, 3, 4.4),
        [None, True, False],
    ])
    def test_is_supported_packets_sequence_type__false__more_element_types(self, value):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is False
        self.mock_abstract_segmenter.is_supported_packet_type.assert_called()

    def test_is_supported_packets_sequence_type__false__empty_sequence(self):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=[]) is False

    @pytest.mark.parametrize("value", [
        (1, 2, 3, 4),
        [2.2, 3.3, 4.4],
        (True, False),
    ])
    def test_is_supported_packets_sequence_type__true(self, value):
        self.mock_abstract_segmenter.is_supported_packet_type.return_value = True
        assert AbstractSegmenter.is_supported_packets_sequence_type(self=self.mock_abstract_segmenter,
                                                                    packets=value) is True
        self.mock_abstract_segmenter.is_supported_packet_type.assert_called()

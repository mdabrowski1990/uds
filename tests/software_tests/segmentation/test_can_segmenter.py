import pytest
from mock import Mock, patch

from uds.segmentation.can_segmenter import CanSegmenter, \
    AddressingType, UdsMessage


class TestCanSegmenter:
    """Unit tests for `CanSegmenter` class."""

    def test_init(self):
        ...


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

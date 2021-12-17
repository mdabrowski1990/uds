import pytest
from mock import Mock

from uds.transport_interface.packet_queues import PacketsQueue, TimestampedPacketsQueue


class TestTimestampedPacketsQueue:
    """Unit tests for `TimestampedPacketsQueue` class."""

    def setup(self):
        self.mock_timestamped_packets_queue = Mock(spec=TimestampedPacketsQueue)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            TimestampedPacketsQueue.__init__(self=self.mock_timestamped_packets_queue, packet_class=Mock())

    # get_packet

    @pytest.mark.asyncio
    async def test_get_packet(self):
        with pytest.raises(NotImplementedError):
            await TimestampedPacketsQueue.get_packet(self=self.mock_timestamped_packets_queue)

    # put_packet

    @pytest.mark.asyncio
    async def test_put_packet(self):
        with pytest.raises(NotImplementedError):
            await TimestampedPacketsQueue.put_packet(self=self.mock_timestamped_packets_queue, packet=Mock())


class TestPacketsQueue:
    """Unit tests for `PacketsQueue` class."""

    def setup(self):
        self.mock_fifo_packets_queue = Mock(spec=PacketsQueue)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            PacketsQueue.__init__(self=self.mock_fifo_packets_queue, packet_class=Mock())

    # get_packet

    @pytest.mark.asyncio
    async def test_get_packet(self):
        with pytest.raises(NotImplementedError):
            await PacketsQueue.get_packet(self=self.mock_fifo_packets_queue)

    # put_packet

    @pytest.mark.asyncio
    async def test_put_packet(self):
        with pytest.raises(NotImplementedError):
            await PacketsQueue.put_packet(self=self.mock_fifo_packets_queue, packet=Mock())

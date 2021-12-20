import pytest
from mock import Mock, patch

from uds.transport_interface.packet_queues import PacketsQueue, TimestampedPacketsQueue


class TestTimestampedPacketsQueue:
    """Unit tests for `TimestampedPacketsQueue` class."""

    SCRIPT_LOCATION = "uds.transport_interface.packet_queues"

    def setup(self):
        self.mock_timestamped_packets_queue = Mock(spec=TimestampedPacketsQueue)
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()

    # __init__

    @pytest.mark.parametrize("packet_type", [Mock(), "something"])
    def test_init(self, packet_type):
        TimestampedPacketsQueue.__init__(self=self.mock_timestamped_packets_queue, packet_type=packet_type)
        self.mock_abstract_packets_queue_init.assert_called_once_with(packet_type=packet_type)

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

    SCRIPT_LOCATION = TestTimestampedPacketsQueue.SCRIPT_LOCATION

    def setup(self):
        self.mock_fifo_packets_queue = Mock(spec=PacketsQueue)
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()

    # __init__

    @pytest.mark.parametrize("packet_type", [Mock(), "something"])
    def test_init(self, packet_type):
        PacketsQueue.__init__(self=self.mock_fifo_packets_queue, packet_type=packet_type)
        self.mock_abstract_packets_queue_init.assert_called_once_with(packet_type=packet_type)

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


class TestTimestampedPacketsQueueIntegration:
    """Integration tests for `TimestampedPacketsQueue` class."""

    # TODO: put_packet (None) and immediately get_packet

    # TODO: put_packet (in future) and await for get_packet

    # TODO: block (when awaited)

    # TODO: clear


class TestPacketsQueueIntegration:
    """Integration tests for `PacketsQueue` class."""

    # TODO: await for get_packet and put_packet

    # TODO: multiple put_packet and get_packet in order

    # TODO: block (when awaited)

    # TODO: clear

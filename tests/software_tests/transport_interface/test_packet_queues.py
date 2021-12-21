import pytest
from mock import Mock, patch

import datetime
from uds.transport_interface.packet_queues import PacketsQueue, TimestampedPacketsQueue
from uds.packet import AbstractUdsPacketContainer


class TestTimestampedPacketsQueue:
    """Unit tests for `TimestampedPacketsQueue` class."""

    SCRIPT_LOCATION = "uds.transport_interface.packet_queues"

    def setup(self):
        self.mock_timestamped_packets_queue = Mock(spec=TimestampedPacketsQueue)
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()
        self._patcher_priority_queue_class = patch(f"{self.SCRIPT_LOCATION}.PriorityQueue")
        self.mock_priority_queue_class = self._patcher_priority_queue_class.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()
        self._patcher_priority_queue_class.stop()

    # __init__

    @pytest.mark.parametrize("packet_type", [Mock(), "something"])
    def test_init(self, packet_type):
        TimestampedPacketsQueue.__init__(self=self.mock_timestamped_packets_queue, packet_type=packet_type)
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__async_queue \
               == self.mock_priority_queue_class.return_value
        self.mock_abstract_packets_queue_init.assert_called_once_with(packet_type=packet_type)
        self.mock_priority_queue_class.assert_called_once_with()

    # _async_queue

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_async_queue__get(self, value):
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__async_queue = value
        assert TimestampedPacketsQueue._async_queue.fget(self.mock_timestamped_packets_queue) == value

    # get_packet

    @pytest.mark.asyncio
    async def test_get_packet(self):
        with pytest.raises(NotImplementedError):
            await TimestampedPacketsQueue.get_packet(self=self.mock_timestamped_packets_queue)

    # put_packet

    def test_put_packet(self):
        with pytest.raises(NotImplementedError):
            TimestampedPacketsQueue.put_packet(self=self.mock_timestamped_packets_queue, packet=Mock())


class TestPacketsQueue:
    """Unit tests for `PacketsQueue` class."""

    SCRIPT_LOCATION = TestTimestampedPacketsQueue.SCRIPT_LOCATION

    def setup(self):
        self.mock_fifo_packets_queue = Mock(spec=PacketsQueue)
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()
        self._patcher_queue_class = patch(f"{self.SCRIPT_LOCATION}.Queue")
        self.mock_queue_class = self._patcher_queue_class.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()
        self._patcher_queue_class.stop()

    # __init__

    @pytest.mark.parametrize("packet_type", [Mock(), "something"])
    def test_init(self, packet_type):
        PacketsQueue.__init__(self=self.mock_fifo_packets_queue, packet_type=packet_type)
        assert self.mock_fifo_packets_queue._PacketsQueue__async_queue == self.mock_queue_class.return_value
        self.mock_abstract_packets_queue_init.assert_called_once_with(packet_type=packet_type)
        self.mock_queue_class.assert_called_once_with()

    # _async_queue

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_async_queue__get(self, value):
        self.mock_fifo_packets_queue._PacketsQueue__async_queue = value
        assert PacketsQueue._async_queue.fget(self.mock_fifo_packets_queue) == value

    # get_packet

    @pytest.mark.asyncio
    async def test_get_packet(self):
        with pytest.raises(NotImplementedError):
            await PacketsQueue.get_packet(self=self.mock_fifo_packets_queue)

    # put_packet

    def test_put_packet(self):
        with pytest.raises(NotImplementedError):
            PacketsQueue.put_packet(self=self.mock_fifo_packets_queue, packet=Mock())


class TestTimestampedPacketsQueueIntegration:
    """Integration tests for `TimestampedPacketsQueue` class."""

    def setup(self):
        self.queue = TimestampedPacketsQueue(packet_type=AbstractUdsPacketContainer)

    # TODO: put_packet (None) and immediately get_packet

    # TODO: put_packet (in future) and await for get_packet

    # TODO: block (when awaited)

    @pytest.mark.parametrize("packets", [
        [(Mock(spec=AbstractUdsPacketContainer), None)],
        [(Mock(spec=AbstractUdsPacketContainer), None),
         (Mock(spec=AbstractUdsPacketContainer), datetime.datetime.now() + datetime.timedelta(seconds=23))],
    ])
    def test_clear(self, packets):
        for packet, timestamp in packets:
            self.queue.put_packet(packet=packet, timestamp=timestamp)
        assert self.queue.is_empty() is False and len(self.queue) == len(packets)
        self.queue.clear()
        assert self.queue.is_empty() is True and len(self.queue) == 0


class TestPacketsQueueIntegration:
    """Integration tests for `PacketsQueue` class."""

    def setup(self):
        self.queue = PacketsQueue(packet_type=AbstractUdsPacketContainer)

    # @pytest.mark.parametrize("packet_type", [AbstractUdsPacketContainer, AbstractUdsPacket, AbstractUdsPacketRecord])
    # def test_await_for_packet(self, packet_type):
    #     packet = Mock(spec=packet_type)
    #     queue = PacketsQueue(packet_type=packet_type)
    #     queue.put_packet(packet)
    #     future = queue.get_packet()

    # TODO: await for get_packet and put_packet

    # TODO: multiple put_packet and get_packet in order

    # TODO: block (when awaited)

    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacketContainer)],
        [Mock(spec=AbstractUdsPacketContainer)] * 10,
    ])
    def test_clear(self, packets):
        for packet in packets:
            self.queue.put_packet(packet=packet)
        assert self.queue.is_empty() is False and len(self.queue) == len(packets)
        self.queue.clear()
        assert self.queue.is_empty() is True and len(self.queue) == 0

import pytest
from mock import Mock, MagicMock, AsyncMock, patch

from time import perf_counter

from uds.transport_interface.packet_queues import PacketsQueue, TimestampedPacketsQueue
from uds.packet import AbstractUdsPacketContainer


class TestTimestampedPacketsQueue:
    """Unit tests for `TimestampedPacketsQueue` class."""

    SCRIPT_LOCATION = "uds.transport_interface.packet_queues"

    def setup(self):
        self.mock_timestamped_packets_queue = Mock(spec=TimestampedPacketsQueue,
                                                   _async_queue=MagicMock(get=AsyncMock(),
                                                                          put=AsyncMock(),
                                                                          join=AsyncMock()))
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()
        self._patcher_abstract_packets_queue_put_packet = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.put_packet")
        self.mock_abstract_packets_queue_put_packet = self._patcher_abstract_packets_queue_put_packet.start()
        self._patcher_priority_queue_class = patch(f"{self.SCRIPT_LOCATION}.PriorityQueue")
        self.mock_priority_queue_class = self._patcher_priority_queue_class.start()
        self._patcher_perf_counter = patch(f"{self.SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()
        self._patcher_abstract_packets_queue_put_packet.stop()
        self._patcher_priority_queue_class.stop()
        self._patcher_perf_counter.stop()

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

    @pytest.mark.parametrize("packet", [Mock(), "a packet"])
    def test_put_packet__without_timestamp(self, packet):
        assert TimestampedPacketsQueue.put_packet(self=self.mock_timestamped_packets_queue, packet=packet) is None
        self.mock_abstract_packets_queue_put_packet.assert_called_once_with(packet=packet)
        self.mock_timestamped_packets_queue._async_queue.put_nowait.assert_called_once_with(
            (self.mock_perf_counter.return_value, packet))
        self.mock_perf_counter.assert_called_once_with()

    @pytest.mark.parametrize("packet", [Mock(), "a packet"])
    @pytest.mark.parametrize("timestamp", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet__type_error(self, mock_isinstance, packet, timestamp):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TimestampedPacketsQueue.put_packet(self=self.mock_timestamped_packets_queue,
                                               packet=packet,
                                               timestamp=timestamp)
        mock_isinstance.assert_called_once_with(timestamp, float)
        self.mock_abstract_packets_queue_put_packet.assert_not_called()
        self.mock_timestamped_packets_queue._async_queue.put_nowait.assert_not_called()

    @pytest.mark.parametrize("packet", [Mock(), "a packet"])
    @pytest.mark.parametrize("timestamp", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet__with_timestamp(self, mock_isinstance, packet, timestamp):
        mock_isinstance.return_value = True
        assert TimestampedPacketsQueue.put_packet(self=self.mock_timestamped_packets_queue,
                                                  packet=packet,
                                                  timestamp=timestamp) is None
        mock_isinstance.assert_called_once_with(timestamp, float)
        self.mock_abstract_packets_queue_put_packet.assert_called_once_with(packet=packet)
        self.mock_timestamped_packets_queue._async_queue.put_nowait.assert_called_once_with((timestamp, packet))


class TestPacketsQueue:
    """Unit tests for `PacketsQueue` class."""

    SCRIPT_LOCATION = TestTimestampedPacketsQueue.SCRIPT_LOCATION

    def setup(self):
        self.mock_fifo_packets_queue = Mock(spec=PacketsQueue,
                                            _async_queue=MagicMock(get=AsyncMock(),
                                                                   put=AsyncMock(),
                                                                   join=AsyncMock()))
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()
        self._patcher_abstract_packets_queue_put_packet = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.put_packet")
        self.mock_abstract_packets_queue_put_packet = self._patcher_abstract_packets_queue_put_packet.start()
        self._patcher_queue_class = patch(f"{self.SCRIPT_LOCATION}.Queue")
        self.mock_queue_class = self._patcher_queue_class.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()
        self._patcher_abstract_packets_queue_put_packet.stop()
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
        packet = await PacketsQueue.get_packet(self=self.mock_fifo_packets_queue)
        assert packet == self.mock_fifo_packets_queue._async_queue.get.return_value

    # put_packet

    @pytest.mark.parametrize("packet", [Mock(), "a packet"])
    def test_put_packet(self, packet):
        assert PacketsQueue.put_packet(self=self.mock_fifo_packets_queue, packet=packet) is None
        self.mock_abstract_packets_queue_put_packet.assert_called_once_with(packet=packet)
        self.mock_fifo_packets_queue._async_queue.put_nowait.assert_called_once_with(packet)


class TestTimestampedPacketsQueueIntegration:
    """Integration tests for `TimestampedPacketsQueue` class."""

    ACCURACY = 0.000001

    def setup(self):
        self.queue = TimestampedPacketsQueue(packet_type=AbstractUdsPacketContainer)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacketContainer)],
        [Mock(spec=AbstractUdsPacketContainer), Mock(spec=AbstractUdsPacketContainer),
         Mock(spec=AbstractUdsPacketContainer), Mock(spec=AbstractUdsPacketContainer)]
    ])
    async def test_put_get_packets__without_timestamp(self, packets):
        for packet in packets:
            self.queue.put_packet(packet)
        for packet in packets:
            packet_from_queue = await self.queue.get_packet()
            assert packet_from_queue is packet

    @pytest.mark.asyncio
    @pytest.mark.parametrize("packets_with_timestamp", [
        [(perf_counter() + 20/1000, Mock(spec=AbstractUdsPacketContainer))],
        [(perf_counter() + 1, Mock(spec=AbstractUdsPacketContainer)),
         (perf_counter() + 613/1000, Mock(spec=AbstractUdsPacketContainer)),
         (perf_counter() + 10/1000, Mock(spec=AbstractUdsPacketContainer)),
         (perf_counter() + 955/1000, Mock(spec=AbstractUdsPacketContainer))]
    ])
    async def test_put_get_packets__with_timestamp(self, packets_with_timestamp):
        for timestamp, packet in packets_with_timestamp:
            self.queue.put_packet(packet=packet, timestamp=timestamp)
        for timestamp, packet in sorted(packets_with_timestamp):
            packet_from_queue = await self.queue.get_packet()
            assert packet_from_queue is packet
            now = perf_counter()
            assert now - self.ACCURACY <= timestamp <= now + self.ACCURACY

    @pytest.mark.parametrize("packets", [
        [(Mock(spec=AbstractUdsPacketContainer), None)],
        [(Mock(spec=AbstractUdsPacketContainer), None),
         (Mock(spec=AbstractUdsPacketContainer), perf_counter() + 23.123)],
    ])
    def test_clear(self, packets):
        for packet, timestamp in packets:
            self.queue.put_packet(packet=packet, timestamp=timestamp)
        assert self.queue.is_empty is False and len(self.queue) == len(packets)
        self.queue.clear()
        assert self.queue.is_empty is True and len(self.queue) == 0


class TestPacketsQueueIntegration:
    """Integration tests for `PacketsQueue` class."""

    def setup(self):
        self.queue = PacketsQueue(packet_type=AbstractUdsPacketContainer)

    # tests

    def test_empty(self):
        assert self.queue.is_empty is True
        assert len(self.queue) == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacketContainer)],
        [Mock(spec=AbstractUdsPacketContainer), Mock(spec=AbstractUdsPacketContainer),
         Mock(spec=AbstractUdsPacketContainer), Mock(spec=AbstractUdsPacketContainer)]
    ])
    async def test_put_get_packets(self, packets):
        # put packets to queue
        for packet in packets:
            self.queue.put_packet(packet)
        # check packets number
        assert self.queue.is_empty is False
        assert len(self.queue) == len(packets)
        # get packets from queue
        for packet in packets:
            packet_from_queue = await self.queue.get_packet()
            assert packet_from_queue is packet
        # check packets number
        assert self.queue.is_empty is True
        assert len(self.queue) == 0

    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacketContainer)],
        [Mock(spec=AbstractUdsPacketContainer)] * 10,
    ])
    def test_clear(self, packets):
        for packet in packets:
            self.queue.put_packet(packet=packet)
        assert self.queue.is_empty is False
        assert len(self.queue) == len(packets)
        self.queue.clear()
        assert self.queue.is_empty is True
        assert len(self.queue) == 0

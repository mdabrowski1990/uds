import pytest
from mock import Mock, MagicMock, AsyncMock, patch, call

from time import perf_counter
from copy import deepcopy

from uds.transport_interface.packet_queues import PacketsQueue, TimestampedPacketsQueue, \
    Event, PriorityQueue, Queue, AsyncioTimeoutError
from uds.packet import AbstractUdsPacketContainer


class TestTimestampedPacketsQueue:
    """Unit tests for `TimestampedPacketsQueue` class."""

    SCRIPT_LOCATION = "uds.transport_interface.packet_queues"

    def setup(self):
        self.mock_timestamped_packets_queue = Mock(spec=TimestampedPacketsQueue,
                                                   _TimestampedPacketsQueue__timestamps=MagicMock(spec=set),
                                                   _TimestampedPacketsQueue__event_packet_added=MagicMock(spec=Event,
                                                                                                          wait=AsyncMock()),
                                                   _async_queue=MagicMock(spec=PriorityQueue,
                                                                          get=AsyncMock(),
                                                                          put=AsyncMock(),
                                                                          join=AsyncMock()))
        # patching
        self._patcher_abstract_packets_queue_init = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.__init__")
        self.mock_abstract_packets_queue_init = self._patcher_abstract_packets_queue_init.start()
        self._patcher_abstract_packets_queue_put_packet = patch(f"{self.SCRIPT_LOCATION}.AbstractPacketsQueue.put_packet")
        self.mock_abstract_packets_queue_put_packet = self._patcher_abstract_packets_queue_put_packet.start()
        self._patcher_priority_queue_class = patch(f"{self.SCRIPT_LOCATION}.PriorityQueue")
        self.mock_priority_queue_class = self._patcher_priority_queue_class.start()
        self._patcher_event_class = patch(f"{self.SCRIPT_LOCATION}.Event")
        self.mock_event_class = self._patcher_event_class.start()
        self._patcher_wait_for = patch(f"{self.SCRIPT_LOCATION}.wait_for")
        self.mock_wait_for = self._patcher_wait_for.start()
        self._patcher_perf_counter = patch(f"{self.SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()

    def teardown(self):
        self._patcher_abstract_packets_queue_init.stop()
        self._patcher_abstract_packets_queue_put_packet.stop()
        self._patcher_priority_queue_class.stop()
        self._patcher_event_class.stop()
        self._patcher_wait_for.stop()
        self._patcher_perf_counter.stop()

    # __init__

    @pytest.mark.parametrize("packet_type", [Mock(), "something"])
    def test_init(self, packet_type):
        TimestampedPacketsQueue.__init__(self=self.mock_timestamped_packets_queue, packet_type=packet_type)
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__async_queue \
               == self.mock_priority_queue_class.return_value
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__event_packet_added \
               == self.mock_event_class.return_value
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps == set()
        self.mock_abstract_packets_queue_init.assert_called_once_with(packet_type=packet_type)
        self.mock_priority_queue_class.assert_called_once_with()

    # _async_queue

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_async_queue__get(self, value):
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__async_queue = value
        assert TimestampedPacketsQueue._async_queue.fget(self.mock_timestamped_packets_queue) == value

    # __await_lowest_timestamp

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_timestamp, timestamps", [
        (0, {0, 0.1}),
        (100, {43.123, 102, 150})
    ])
    async def test_await_lowest_timestamp__now(self, current_timestamp, timestamps):
        self.mock_perf_counter.return_value = current_timestamp
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps = deepcopy(timestamps)
        assert await TimestampedPacketsQueue._TimestampedPacketsQueue__await_lowest_timestamp(
            self=self.mock_timestamped_packets_queue) == min(timestamps)
        self.mock_perf_counter.assert_called_once_with()
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps == timestamps

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_timestamp, next_timestamp", [
        (0, 2.56789),
        (9654.4312965, 93921321.2315312),
    ])
    async def test_await_lowest_timestamp__await_packet(self, current_timestamp, next_timestamp):
        self.mock_perf_counter.side_effect = [current_timestamp, next_timestamp]
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps = set()
        self.mock_wait_for.side_effect = lambda *args, **kwargs: \
            self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps.add(next_timestamp)
        assert await TimestampedPacketsQueue._TimestampedPacketsQueue__await_lowest_timestamp(
            self=self.mock_timestamped_packets_queue) == next_timestamp
        self.mock_wait_for.assert_awaited_once()  # TODO: https://stackoverflow.com/questions/70448262/how-to-use-asyncmock-and-get-coroutines-futures-returned-from-call
        assert self.mock_wait_for.mock_calls[0].kwargs["timeout"] == float("inf")
        self.mock_perf_counter.assert_has_calls([call(), call()])
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps == {next_timestamp}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_timestamp, timestamps", [
        (0, {1, 0.1}),
        (100, {983221, 102, 150})
    ])
    async def test_await_lowest_timestamp__await_timestamp(self, current_timestamp, timestamps):
        self.mock_perf_counter.return_value = current_timestamp
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps = deepcopy(timestamps)
        self.mock_wait_for.side_effect = AsyncioTimeoutError
        assert await TimestampedPacketsQueue._TimestampedPacketsQueue__await_lowest_timestamp(
            self=self.mock_timestamped_packets_queue) == min(timestamps)
        self.mock_wait_for.assert_awaited_once()  # TODO: https://stackoverflow.com/questions/70448262/how-to-use-asyncmock-and-get-coroutines-futures-returned-from-call
        assert self.mock_wait_for.mock_calls[0].kwargs["timeout"] == min(timestamps) - current_timestamp
        self.mock_perf_counter.assert_called_once_with()
        assert self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps == timestamps

    # get_packet

    @pytest.mark.asyncio
    @pytest.mark.parametrize("packet_timestamp", [123.456, 0.91784])
    @pytest.mark.parametrize("packet", ["something", Mock()])
    async def test_get_packet(self, packet_timestamp, packet):
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__await_lowest_timestamp.return_value = packet_timestamp
        self.mock_timestamped_packets_queue._async_queue.get_nowait.return_value = [packet_timestamp, packet]
        assert await TimestampedPacketsQueue.get_packet(self=self.mock_timestamped_packets_queue) == packet
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__await_lowest_timestamp.assert_awaited_once_with()
        self.mock_timestamped_packets_queue._async_queue.get_nowait.assert_called_once_with()
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps.remove.assert_called_once_with(packet_timestamp)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("min_timestamp, packet_timestamp", [
        (1, 2),
        (9.5, 3.123),
    ])
    @pytest.mark.parametrize("packet", ["something", Mock()])
    async def test_get_packet__runtime_error(self, min_timestamp, packet_timestamp, packet):
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__await_lowest_timestamp.return_value = min_timestamp
        self.mock_timestamped_packets_queue._async_queue.get_nowait.return_value = [packet_timestamp, packet]
        with pytest.raises(RuntimeError):
            await TimestampedPacketsQueue.get_packet(self=self.mock_timestamped_packets_queue)
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__await_lowest_timestamp.assert_awaited_once_with()
        self.mock_timestamped_packets_queue._async_queue.get_nowait.assert_called_once_with()

    # put_packet

    @pytest.mark.parametrize("packet", [Mock(), "a packet"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet__without_timestamp(self, mock_isinstance, packet):
        timestamp = self.mock_perf_counter.return_value
        assert TimestampedPacketsQueue.put_packet(self=self.mock_timestamped_packets_queue, packet=packet) is None
        mock_isinstance.assert_not_called()
        self.mock_abstract_packets_queue_put_packet.assert_called_once_with(packet=packet)
        self.mock_timestamped_packets_queue._async_queue.put_nowait.assert_called_once_with((timestamp, packet))
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps.add.assert_called_once_with(timestamp)
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__event_packet_added.set.assert_called_once_with()

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
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps.add.assert_not_called()
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__event_packet_added.set.assert_not_called()

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
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__timestamps.add.assert_called_once_with(timestamp)
        self.mock_timestamped_packets_queue._TimestampedPacketsQueue__event_packet_added.set.assert_called_once_with()


class TestPacketsQueue:
    """Unit tests for `PacketsQueue` class."""

    SCRIPT_LOCATION = TestTimestampedPacketsQueue.SCRIPT_LOCATION

    def setup(self):
        self.mock_fifo_packets_queue = Mock(spec=PacketsQueue,
                                            _async_queue=MagicMock(spec=Queue,
                                                                   get=AsyncMock(),
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


@pytest.mark.intergration
class TestTimestampedPacketsQueueIntegration:
    """Integration tests for `TimestampedPacketsQueue` class."""

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
        [(0.0000001, Mock(spec=AbstractUdsPacketContainer))],
        [(0.0000001, Mock(spec=AbstractUdsPacketContainer)),
         (0.0000004, Mock(spec=AbstractUdsPacketContainer)),
         (0.0000003, Mock(spec=AbstractUdsPacketContainer)),
         (0.0000002, Mock(spec=AbstractUdsPacketContainer))],
    ])
    async def test_put_get_packets__with_timestamp(self, packets_with_timestamp):
        start_time = perf_counter()
        for offset, packet in packets_with_timestamp:
            self.queue.put_packet(packet=packet, timestamp=start_time+offset)
        for timestamp, packet in sorted(packets_with_timestamp):
            packet_from_queue = await self.queue.get_packet()
            assert packet_from_queue is packet

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


@pytest.mark.intergration
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

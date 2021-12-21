import pytest
from mock import Mock, MagicMock, AsyncMock, patch

import datetime
from uds.transport_interface.packet_queues import PacketsQueue, TimestampedPacketsQueue
from uds.packet import AbstractUdsPacketContainer


class TestTimestampedPacketsQueue:
    """Unit tests for `TimestampedPacketsQueue` class."""

    SCRIPT_LOCATION = "uds.transport_interface.packet_queues"

    def setup(self):
        self.mock_timestamped_packets_queue = Mock(spec=PacketsQueue,
                                                   _async_queue=MagicMock(get=AsyncMock(),
                                                                          put=AsyncMock(),
                                                                          join=AsyncMock()))
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
        self.mock_fifo_packets_queue = Mock(spec=PacketsQueue,
                                            _async_queue=MagicMock(get=AsyncMock(),
                                                                   put=AsyncMock(),
                                                                   join=AsyncMock()))
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
        packet = await PacketsQueue.get_packet(self=self.mock_fifo_packets_queue)
        assert packet == self.mock_queue_class._async_queue.get.return_value

    # put_packet

    @pytest.mark.parametrize("packet", [Mock(), "not a packet"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet__type_error(self, mock_isinstance, packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PacketsQueue.put_packet(self=self.mock_fifo_packets_queue, packet=packet)
        mock_isinstance.assert_called_once_with(packet, self.mock_fifo_packets_queue.packet_type)

    @pytest.mark.parametrize("packet", [Mock(), "a packet"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet(self, mock_isinstance, packet):
        mock_isinstance.return_value = True
        assert PacketsQueue.put_packet(self=self.mock_fifo_packets_queue, packet=packet) is None
        self.mock_fifo_packets_queue._async_queue.put_nowait.assert_called_once_with(packet)
        mock_isinstance.assert_called_once_with(packet, self.mock_fifo_packets_queue.packet_type)


class TestTimestampedPacketsQueueIntegration:
    """Integration tests for `TimestampedPacketsQueue` class."""

    def setup(self):
        self.queue = TimestampedPacketsQueue(packet_type=AbstractUdsPacketContainer)

    # TODO: put_packet (None) and immediately get_packet

    # TODO: put_packet (in future) and await for get_packet

    # TODO: block (when awaited)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacketContainer)],
        [Mock(spec=AbstractUdsPacketContainer), Mock(spec=AbstractUdsPacketContainer),
         Mock(spec=AbstractUdsPacketContainer), Mock(spec=AbstractUdsPacketContainer)]
    ])
    async def test_put_get_packets(self, packets):
        for packet in packets:
            self.queue.put_packet(packet)
        for packet in packets:
            packet_from_queue = await self.queue.get_packet()
            assert packet_from_queue is packet

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

    # TODO: block (when awaited)

    def test_empty(self):
        assert self.queue.is_empty() is True
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
        assert self.queue.is_empty() is False
        assert len(self.queue) == len(packets)
        # get packets from queue
        for packet in packets:
            packet_from_queue = await self.queue.get_packet()
            assert packet_from_queue is packet
        # check packets number
        assert self.queue.is_empty() is True
        assert len(self.queue) == 0

    @pytest.mark.parametrize("packets", [
        [Mock(spec=AbstractUdsPacketContainer)],
        [Mock(spec=AbstractUdsPacketContainer)] * 10,
    ])
    def test_clear(self, packets):
        for packet in packets:
            self.queue.put_packet(packet=packet)
        assert self.queue.is_empty() is False
        assert len(self.queue) == len(packets)
        self.queue.clear()
        assert self.queue.is_empty() is True
        assert len(self.queue) == 0

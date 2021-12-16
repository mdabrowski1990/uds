import pytest
from mock import Mock

from uds.transport_interface.packet_queue import AbstractPacketsQueue, PacketsQueue, TimestampedPacketsQueue


class TestAbstractPacketsQueue:
    """Unit tests for `AbstractPacketsQueue` class."""

    def setup(self):
        self.mock_abstract_packets_queue = Mock(spec=AbstractPacketsQueue)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.__init__(self=self.mock_abstract_packets_queue, packet_class=Mock())

    # __del__

    def test_del(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.__del__(self=self.mock_abstract_packets_queue)

    # __len__

    def test_len(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.__len__(self=self.mock_abstract_packets_queue)

    # is_empty

    def test_is_empty(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.is_empty(self=self.mock_abstract_packets_queue)

    # one_task_done

    def test_one_task_done(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.one_task_done(self=self.mock_abstract_packets_queue)

    # block

    def test_get_block(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.block(self=self.mock_abstract_packets_queue)

    # clear

    def test_get_clear(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.clear(self=self.mock_abstract_packets_queue)


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

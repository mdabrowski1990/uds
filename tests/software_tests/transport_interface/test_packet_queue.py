import pytest
from mock import Mock

from uds.transport_interface.packet_queue import ReceivedPacketsQueue


class TestReceivedPacketsQueue:
    """Unit tests for `ReceivedPacketsQueue class."""

    def setup(self):
        self.mock_received_packets_queue = Mock(spec=ReceivedPacketsQueue)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            ReceivedPacketsQueue.__init__(self=self.mock_received_packets_queue, packet_class=Mock())

    # __del__

    def test_del(self):
        with pytest.raises(NotImplementedError):
            ReceivedPacketsQueue.__del__(self=self.mock_received_packets_queue)

    # __len__

    def test_len(self):
        with pytest.raises(NotImplementedError):
            ReceivedPacketsQueue.__len__(self=self.mock_received_packets_queue)

    # is_empty

    def test_is_empty(self):
        with pytest.raises(NotImplementedError):
            ReceivedPacketsQueue.is_empty(self=self.mock_received_packets_queue)

    # packet_task_done

    def test_packet_task_done(self):
        with pytest.raises(NotImplementedError):
            ReceivedPacketsQueue.packet_task_done(self=self.mock_received_packets_queue)

    # get_packet

    @pytest.mark.asyncio
    async def test_get_packet(self):
        with pytest.raises(NotImplementedError):
            await ReceivedPacketsQueue.get_packet(self=self.mock_received_packets_queue)

    # put_packet

    @pytest.mark.asyncio
    async def test_put_packet(self):
        with pytest.raises(NotImplementedError):
            await ReceivedPacketsQueue.put_packet(self=self.mock_received_packets_queue, packet=Mock())

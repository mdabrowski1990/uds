import pytest
from mock import MagicMock, Mock, AsyncMock, patch, call

from uds.transport_interface.abstract_packet_queue import AbstractPacketsQueue, \
    AbstractUdsPacketContainer, QueueEmpty
from uds.packet import AbstractUdsPacket, AbstractUdsPacketRecord
from uds.message import UdsMessage


class TestAbstractPacketsQueue:
    """Unit tests for `AbstractPacketsQueue` class."""

    SCRIPT_LOCATION = "uds.transport_interface.abstract_packet_queue"

    def setup(self):
        self.mock_abstract_packets_queue = MagicMock(spec=AbstractPacketsQueue,
                                                     _async_queue=MagicMock(get=AsyncMock(),
                                                                            put=AsyncMock(),
                                                                            join=AsyncMock()))
        # patching
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown(self):
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("packet_type", [AbstractUdsPacketContainer, AbstractUdsPacket, AbstractUdsPacketRecord])
    def test_init(self, packet_type):
        assert AbstractPacketsQueue.__init__(self=self.mock_abstract_packets_queue, packet_type=packet_type) is None
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__packet_type == packet_type

    @pytest.mark.parametrize("packet_type", [None, Mock(spec=AbstractUdsPacketContainer)])
    def test_init__type_error(self, packet_type):
        with pytest.raises(TypeError):
            AbstractPacketsQueue.__init__(self=self.mock_abstract_packets_queue, packet_type=packet_type)

    @pytest.mark.parametrize("packet_type", [UdsMessage, type, int])
    def test_init__value_error(self, packet_type):
        with pytest.raises(ValueError):
            AbstractPacketsQueue.__init__(self=self.mock_abstract_packets_queue, packet_type=packet_type)

    # __len__

    def test_len(self):
        assert AbstractPacketsQueue.__len__(self=self.mock_abstract_packets_queue) \
               == self.mock_abstract_packets_queue._async_queue.qsize.return_value

    # packet_type

    @pytest.mark.parametrize("packet_type", [Mock(), "something"])
    def test_packet_type(self, packet_type):
        self.mock_abstract_packets_queue._AbstractPacketsQueue__packet_type = packet_type
        assert AbstractPacketsQueue.packet_type.fget(self.mock_abstract_packets_queue) == packet_type

    # is_empty

    def test_is_empty__true(self):
        self.mock_abstract_packets_queue.__len__.return_value = 0
        assert AbstractPacketsQueue.is_empty.fget(self.mock_abstract_packets_queue) is True

    @pytest.mark.parametrize("len_value", [1, 9321])
    def test_is_empty__false(self, len_value):
        self.mock_abstract_packets_queue.__len__.return_value = len_value
        assert AbstractPacketsQueue.is_empty.fget(self.mock_abstract_packets_queue) is False

    # mark_task_done

    def test_mark_task_done__value_error(self):
        self.mock_abstract_packets_queue._AbstractPacketsQueue__unfinished_tasks = 0
        with pytest.raises(ValueError):
            AbstractPacketsQueue.mark_task_done(self=self.mock_abstract_packets_queue)
        self.mock_abstract_packets_queue._async_queue.task_done.assert_not_called()

    @pytest.mark.parametrize("unfinished_tasks_number", [1, 100])
    def test_mark_task_done(self, unfinished_tasks_number):
        self.mock_abstract_packets_queue._AbstractPacketsQueue__unfinished_tasks = unfinished_tasks_number
        assert AbstractPacketsQueue.mark_task_done(self=self.mock_abstract_packets_queue) is None
        self.mock_abstract_packets_queue._async_queue.task_done.assert_called_once_with()
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__unfinished_tasks == unfinished_tasks_number - 1

    # clear

    @pytest.mark.parametrize("packets_number", [0, 1, 99])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_clear(self, mock_len, packets_number):
        mock_len.return_value = packets_number
        assert AbstractPacketsQueue.clear(self=self.mock_abstract_packets_queue) is None
        mock_len.assert_called_once_with(self.mock_abstract_packets_queue)
        self.mock_abstract_packets_queue._async_queue.get_nowait.assert_has_calls([call()] * packets_number)
        self.mock_abstract_packets_queue.mark_task_done.assert_has_calls([call()] * packets_number)

    @pytest.mark.parametrize("packets_number", [1, 99])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_clear__queue_empty(self, mock_len, packets_number):
        mock_len.return_value = packets_number
        self.mock_abstract_packets_queue._async_queue.get_nowait.side_effect = QueueEmpty
        assert AbstractPacketsQueue.clear(self=self.mock_abstract_packets_queue) is None
        self.mock_abstract_packets_queue._async_queue.get_nowait.assert_called_once()
        self.mock_warn.assert_called_once()
        self.mock_abstract_packets_queue.mark_task_done.assert_not_called()

    # await_handled

    @pytest.mark.asyncio
    async def test_await_handled(self):
        assert await AbstractPacketsQueue.await_handled(self=self.mock_abstract_packets_queue) is None
        self.mock_abstract_packets_queue._async_queue.join.assert_awaited_once_with()

    # put_packet

    @pytest.mark.parametrize("packet", ["some packet", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet__type_error(self, mock_isinstance, packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractPacketsQueue.put_packet(self=self.mock_abstract_packets_queue, packet=packet)
        mock_isinstance.assert_called_once_with(packet, self.mock_abstract_packets_queue.packet_type)

    @pytest.mark.parametrize("packet", ["some packet", Mock()])
    @pytest.mark.parametrize("unfinished_tasks", [0, 1, 99])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_packet(self, mock_isinstance, packet, unfinished_tasks):
        mock_isinstance.return_value = True
        self.mock_abstract_packets_queue._AbstractPacketsQueue__unfinished_tasks = unfinished_tasks
        assert AbstractPacketsQueue.put_packet(self=self.mock_abstract_packets_queue, packet=packet) is None
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__unfinished_tasks == unfinished_tasks + 1
        mock_isinstance.assert_called_once_with(packet, self.mock_abstract_packets_queue.packet_type)

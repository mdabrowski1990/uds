import pytest
from mock import MagicMock, Mock, AsyncMock, patch, call

from uds.transport_interface.abstract_packet_queue import AbstractPacketsQueue, \
    AbstractUdsPacketContainer
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

    # __init__

    @pytest.mark.parametrize("packet_type", [AbstractUdsPacketContainer, AbstractUdsPacket, AbstractUdsPacketRecord])
    def test_init(self, packet_type):
        AbstractPacketsQueue.__init__(self=self.mock_abstract_packets_queue, packet_type=packet_type)
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__packet_type == packet_type
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__is_blocked is False

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

    # is_blocked

    @pytest.mark.parametrize("value", [True, False])
    def test_is_blocked(self, value):
        self.mock_abstract_packets_queue._AbstractPacketsQueue__is_blocked = value
        assert AbstractPacketsQueue.is_blocked.fget(self.mock_abstract_packets_queue) == value

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

    # block

    def test_block__empty(self):
        self.mock_abstract_packets_queue.is_empty = True
        AbstractPacketsQueue.block(self=self.mock_abstract_packets_queue)
        with pytest.raises(AttributeError):  # value not set
            self.mock_abstract_packets_queue._AbstractPacketsQueue__is_blocked

    def test_block__nonempty(self):
        self.mock_abstract_packets_queue.is_empty = False
        AbstractPacketsQueue.block(self=self.mock_abstract_packets_queue)
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__is_blocked is True

    # clear

    @pytest.mark.parametrize("packets_number", [0, 1, 99])
    @patch(f"{SCRIPT_LOCATION}.len")
    def test_clear(self, mock_len, packets_number):
        mock_len.return_value = packets_number
        AbstractPacketsQueue.clear(self=self.mock_abstract_packets_queue)
        mock_len.assert_called_once_with(self.mock_abstract_packets_queue)
        self.mock_abstract_packets_queue.block.assert_called_once_with()
        self.mock_abstract_packets_queue._async_queue.get_nowait.assert_has_calls([call()] * packets_number)
        self.mock_abstract_packets_queue.mark_task_done.assert_has_calls([call()] * packets_number)
        assert self.mock_abstract_packets_queue._AbstractPacketsQueue__is_blocked is False

    # await_handled

    @pytest.mark.asyncio
    @pytest.mark.parametrize("block_new_packets", [True, False])
    async def test_await_handled(self, block_new_packets):
        await AbstractPacketsQueue.await_handled(self=self.mock_abstract_packets_queue,
                                                 block_new_packets=block_new_packets)
        self.mock_abstract_packets_queue._async_queue.join.assert_awaited_once_with()
        if block_new_packets:
            self.mock_abstract_packets_queue.block.assert_called_once_with()
        else:
            self.mock_abstract_packets_queue.block.assert_not_called()

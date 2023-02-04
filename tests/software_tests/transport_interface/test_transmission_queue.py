import pytest
from mock import AsyncMock, MagicMock, Mock, patch, call
from copy import deepcopy
from time import perf_counter

from uds.transport_interface.transmission_queue import TransmissionQueue, \
    UdsMessage, AbstractUdsPacket, QueueEmpty, Event, AsyncioTimeoutError, PriorityQueue


class TestTransmissionQueue:
    """Unit tests for 'TransmissionQueue' class."""

    SCRIPT_LOCATION = "uds.transport_interface.transmission_queue"

    def setup(self):
        self.mock_transmission_queue = Mock(spec=TransmissionQueue,
                                            _TransmissionQueue__timestamps=MagicMock(spec=set),
                                            _TransmissionQueue__event_pdu_added=MagicMock(spec=Event,
                                                                                          wait=AsyncMock()),
                                            _TransmissionQueue__async_queue=MagicMock(spec=PriorityQueue,
                                                                                      get=AsyncMock(),
                                                                                      put=AsyncMock(),
                                                                                      join=AsyncMock()))
        # patching
        self._patcher_priority_queue_class = patch(f"{self.SCRIPT_LOCATION}.PriorityQueue")
        self.mock_priority_queue_class = self._patcher_priority_queue_class.start()
        self._patcher_event_class = patch(f"{self.SCRIPT_LOCATION}.Event")
        self.mock_event_class = self._patcher_event_class.start()
        self._patcher_wait_for = patch(f"{self.SCRIPT_LOCATION}.wait_for")
        self.mock_wait_for = self._patcher_wait_for.start()
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_perf_counter = patch(f"{self.SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()

    def teardown(self):
        self._patcher_priority_queue_class.stop()
        self._patcher_event_class.stop()
        self._patcher_wait_for.stop()
        self._patcher_warn.stop()
        self._patcher_perf_counter.stop()

    # __init__

    @pytest.mark.parametrize("pdu_type", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    def test_init__type_error(self, mock_issubclass, pdu_type):
        mock_issubclass.return_value = False
        with pytest.raises(TypeError):
            TransmissionQueue.__init__(self=self.mock_transmission_queue, pdu_type=pdu_type)
        mock_issubclass.assert_called_once_with(pdu_type, (UdsMessage, AbstractUdsPacket))

    @pytest.mark.parametrize("pdu_type", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    def test_init__valid(self, mock_issubclass, pdu_type):
        mock_issubclass.return_value = True
        assert TransmissionQueue.__init__(self=self.mock_transmission_queue, pdu_type=pdu_type) is None
        mock_issubclass.assert_called_once_with(pdu_type, (UdsMessage, AbstractUdsPacket))
        self.mock_event_class.assert_called_once_with()
        assert self.mock_transmission_queue._TransmissionQueue__pdu_type == pdu_type
        assert self.mock_transmission_queue._TransmissionQueue__async_queue \
               == self.mock_priority_queue_class.return_value
        assert self.mock_transmission_queue._TransmissionQueue__event_pdu_added \
               == self.mock_event_class.return_value
        assert self.mock_transmission_queue._TransmissionQueue__timestamps == set()

    # __len__

    def test_len(self):
        mock_len = Mock()
        self.mock_transmission_queue._TransmissionQueue__async_queue = Mock(qsize=mock_len)
        assert TransmissionQueue.__len__(self=self.mock_transmission_queue) == mock_len.return_value

    # __pdu_ready

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_timestamp, timestamps", [
        (0, {0, 0.1}),
        (100, {43.123, 102, 150})
    ])
    async def test_pdu_ready__now(self, current_timestamp, timestamps):
        self.mock_perf_counter.return_value = current_timestamp
        self.mock_transmission_queue._TransmissionQueue__timestamps = deepcopy(timestamps)
        assert await TransmissionQueue._TransmissionQueue__pdu_ready(self=self.mock_transmission_queue) \
               == min(timestamps)
        self.mock_perf_counter.assert_called_once_with()
        assert self.mock_transmission_queue._TransmissionQueue__timestamps == timestamps

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_timestamp, next_timestamp", [
        (0, 2.56789),
        (9654.4312965, 93921321.2315312),
    ])
    async def test_pdu_ready__await_packet(self, current_timestamp, next_timestamp):
        self.mock_perf_counter.side_effect = [current_timestamp, next_timestamp]
        self.mock_transmission_queue._TransmissionQueue__timestamps = set()
        self.mock_wait_for.side_effect \
            = lambda *args, **kwargs: self.mock_transmission_queue._TransmissionQueue__timestamps.add(next_timestamp)
        assert await TransmissionQueue._TransmissionQueue__pdu_ready(self=self.mock_transmission_queue) \
               == next_timestamp
        self.mock_wait_for.assert_awaited_once()  # TODO: https://stackoverflow.com/questions/70448262/how-to-use-asyncmock-and-get-coroutines-futures-returned-from-call
        assert self.mock_wait_for.mock_calls[0].kwargs["timeout"] == float("inf")
        self.mock_perf_counter.assert_has_calls([call(), call()])
        assert self.mock_transmission_queue._TransmissionQueue__timestamps == {next_timestamp}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_timestamp, timestamps", [
        (0, {1, 0.1}),
        (100, {983221, 102, 150})
    ])
    async def test_pdu_ready__await_timestamp(self, current_timestamp, timestamps):
        self.mock_perf_counter.return_value = current_timestamp
        self.mock_transmission_queue._TransmissionQueue__timestamps = deepcopy(timestamps)
        self.mock_wait_for.side_effect = AsyncioTimeoutError
        assert await TransmissionQueue._TransmissionQueue__pdu_ready(self=self.mock_transmission_queue) \
               == min(timestamps)
        self.mock_wait_for.assert_awaited_once()  # TODO: https://stackoverflow.com/questions/70448262/how-to-use-asyncmock-and-get-coroutines-futures-returned-from-call
        assert self.mock_wait_for.mock_calls[0].kwargs["timeout"] == min(timestamps) - current_timestamp
        self.mock_perf_counter.assert_called_once_with()
        assert self.mock_transmission_queue._TransmissionQueue__timestamps == timestamps

    # pdu_type

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_pdu_type__get(self, value):
        self.mock_transmission_queue._TransmissionQueue__pdu_type = value
        assert TransmissionQueue.pdu_type.fget(self.mock_transmission_queue) == value

    # is_empty

    @pytest.mark.parametrize("value", [True, False])
    def test_is_empty(self, value):
        mock_eq = Mock(return_value=value)
        self.mock_transmission_queue.__len__ = Mock(return_value=MagicMock(__eq__=mock_eq))
        assert TransmissionQueue.is_empty.fget(self.mock_transmission_queue) is value
        mock_eq.assert_called_once_with(0)

    # mark_pdu_sent

    def test_mark_pdu_sent(self):
        mock_task_done = Mock()
        self.mock_transmission_queue._TransmissionQueue__async_queue = Mock(task_done=mock_task_done)
        assert TransmissionQueue.mark_pdu_sent(self=self.mock_transmission_queue) is None
        mock_task_done.assert_called_once_with()

    # clear

    @pytest.mark.parametrize("packets_number", [0, 1, 99])
    def test_clear(self, packets_number):
        self.mock_transmission_queue.__len__ = Mock(return_value=packets_number)
        mock_get_nowait = Mock()
        self.mock_transmission_queue._TransmissionQueue__async_queue = Mock(get_nowait=mock_get_nowait)
        assert TransmissionQueue.clear(self=self.mock_transmission_queue) is None
        self.mock_transmission_queue.__len__.assert_called_once_with()
        mock_get_nowait.assert_has_calls([call()] * packets_number)
        self.mock_warn.assert_not_called()
        self.mock_transmission_queue.mark_pdu_sent.assert_has_calls([call()] * packets_number)

    @pytest.mark.parametrize("packets_number", [1, 99])
    def test_clear__queue_empty(self, packets_number):
        self.mock_transmission_queue.__len__ = Mock(return_value=packets_number)
        mock_get_nowait = Mock(side_effect=QueueEmpty)
        self.mock_transmission_queue._TransmissionQueue__async_queue = Mock(get_nowait=mock_get_nowait)
        assert TransmissionQueue.clear(self=self.mock_transmission_queue) is None
        self.mock_transmission_queue.__len__.assert_called_once_with()
        mock_get_nowait.assert_called_once()
        self.mock_warn.assert_called_once()
        self.mock_transmission_queue.mark_pdu_sent.assert_not_called()

    # get_pdu

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pdu_timestamp", [123.456, 0.91784])
    @pytest.mark.parametrize("pdu", ["something", Mock()])
    async def test_get_pdu(self, pdu_timestamp, pdu):
        self.mock_transmission_queue._TransmissionQueue__pdu_ready.return_value = pdu_timestamp
        self.mock_transmission_queue._TransmissionQueue__async_queue.get_nowait.return_value = [pdu_timestamp, pdu]
        assert await TransmissionQueue.get_pdu(self=self.mock_transmission_queue) == pdu
        self.mock_transmission_queue._TransmissionQueue__pdu_ready.assert_awaited_once_with()
        self.mock_transmission_queue._TransmissionQueue__async_queue.get_nowait.assert_called_once_with()
        self.mock_transmission_queue._TransmissionQueue__timestamps.remove.assert_called_once_with(pdu_timestamp)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("min_timestamp, pdu_timestamp", [
        (1, 2),
        (9.5, 3.123),
    ])
    @pytest.mark.parametrize("pdu", ["something", Mock()])
    async def test_get_pdu__runtime_error(self, min_timestamp, pdu_timestamp, pdu):
        self.mock_transmission_queue._TransmissionQueue__pdu_ready.return_value = min_timestamp
        self.mock_transmission_queue._TransmissionQueue__async_queue.get_nowait.return_value = [pdu_timestamp, pdu]
        with pytest.raises(RuntimeError):
            await TransmissionQueue.get_pdu(self=self.mock_transmission_queue)
        self.mock_transmission_queue._TransmissionQueue__pdu_ready.assert_awaited_once_with()
        self.mock_transmission_queue._TransmissionQueue__async_queue.get_nowait.assert_called_once_with()

    # put_pdu

    @pytest.mark.parametrize("pdu", [Mock(), "a pdu"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_pdu__type_error__pdu(self, mock_isinstance, pdu):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TransmissionQueue.put_pdu(self=self.mock_transmission_queue, pdu=pdu)
        mock_isinstance.assert_called_once_with(pdu, self.mock_transmission_queue.pdu_type)

    @pytest.mark.parametrize("pdu, timestamp", [
        (Mock(), Mock()),
        ("a pdu", "some timestamp")
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_pdu__type_error__timestamp(self, mock_isinstance, pdu, timestamp):
        mock_isinstance.side_effect = [True, False]
        with pytest.raises(TypeError):
            TransmissionQueue.put_pdu(self=self.mock_transmission_queue,
                                      pdu=pdu,
                                      timestamp=timestamp)
        mock_isinstance.assert_has_calls([call(pdu, self.mock_transmission_queue.pdu_type),
                                          call(timestamp, float)])

    @pytest.mark.parametrize("pdu", [Mock(), "a pdu"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_pdu__without_timestamp(self, mock_isinstance, pdu):
        mock_isinstance.return_value = True
        timestamp = self.mock_perf_counter.return_value
        assert TransmissionQueue.put_pdu(self=self.mock_transmission_queue, pdu=pdu) is None
        mock_isinstance.assert_called_once_with(pdu, self.mock_transmission_queue.pdu_type)
        self.mock_transmission_queue._TransmissionQueue__async_queue.put_nowait.assert_called_once_with((timestamp, pdu))
        self.mock_transmission_queue._TransmissionQueue__timestamps.add.assert_called_once_with(timestamp)
        self.mock_transmission_queue._TransmissionQueue__event_pdu_added.set.assert_called_once_with()

    @pytest.mark.parametrize("pdu, timestamp", [
        (Mock(), Mock()),
        ("a pdu", "some timestamp")
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_pdu__with_timestamp(self, mock_isinstance, pdu, timestamp):
        mock_isinstance.return_value = True
        assert TransmissionQueue.put_pdu(self=self.mock_transmission_queue,
                                         pdu=pdu,
                                         timestamp=timestamp) is None
        mock_isinstance.assert_has_calls([call(pdu, self.mock_transmission_queue.pdu_type),
                                          call(timestamp, float)])
        self.mock_transmission_queue._TransmissionQueue__async_queue.put_nowait.assert_called_once_with((timestamp, pdu))
        self.mock_transmission_queue._TransmissionQueue__timestamps.add.assert_called_once_with(timestamp)
        self.mock_transmission_queue._TransmissionQueue__event_pdu_added.set.assert_called_once_with()


@pytest.mark.performance
class TestTransmissionQueuePerformance:

    def setup(self):
        self.transmission_queue = TransmissionQueue(AbstractUdsPacket)

    @pytest.mark.asyncio
    @pytest.mark.skip("Sometimes fails due to issues with async timing - TO BE IMPROVED")
    @pytest.mark.parametrize("delays", [
        (0.1, 0.2, 0.3, 0.4),
        (0.19, 0.01, 0.35, 0.3),
        (0.01, 0.02, 0.8, 0.05, 0.03, 0.07, 0.065, 0.015, 0.7, 0.123456)])
    async def test_put_and_get_pdu(self, delays):
        pdu_list = [Mock(spec=AbstractUdsPacket) for _ in delays]
        pdu_with_delays = list(zip(pdu_list, [perf_counter() + delay for delay in delays]))
        for pdu, timestamp in pdu_with_delays:
            self.transmission_queue.put_pdu(pdu=pdu, timestamp=timestamp)
        for expected_pdu, expected_timestamp in sorted(pdu_with_delays, key=lambda pair: pair[1]):
            assert await self.transmission_queue.get_pdu() == expected_pdu
            out_time = perf_counter()
            assert out_time >= expected_timestamp
            print(expected_timestamp, out_time, out_time - expected_timestamp)

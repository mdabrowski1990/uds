import pytest
from copy import deepcopy
from mock import AsyncMock, Mock, patch

from uds.transport_interface.records_queue import RecordsQueue, \
    UdsMessageRecord, AbstractUdsPacketRecord


class TestRecordsQueue:
    """Unit tests for 'RecordsQueue' class."""

    SCRIPT_LOCATION = "uds.transport_interface.records_queue"

    def setup(self):
        self.mock_records_queue = Mock(spec=RecordsQueue)
        # patching
        self._patcher_event_class = patch(f"{self.SCRIPT_LOCATION}.Event")
        self.mock_event_class = self._patcher_event_class.start()

    def teardown(self):
        self._patcher_event_class.stop()

    # __init__

    @pytest.mark.parametrize("records_type, history_size", [
        (Mock(), Mock()),
        ("some type", "some history size"),
    ])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__type_error__records_type(self, mock_isinstance, mock_issubclass, records_type, history_size):
        mock_isinstance.return_value = True
        mock_issubclass.return_value = False
        with pytest.raises(TypeError):
            RecordsQueue.__init__(self=self.mock_records_queue,
                                  records_type=records_type,
                                  history_size=history_size)
        mock_issubclass.assert_called_once_with(records_type, (UdsMessageRecord, AbstractUdsPacketRecord))

    @pytest.mark.parametrize("records_type, history_size", [
        (Mock(), Mock()),
        ("some type", "some history size"),
    ])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__type_error__history_size(self, mock_isinstance, mock_issubclass, records_type, history_size):
        mock_isinstance.return_value = False
        mock_issubclass.return_value = True
        with pytest.raises(TypeError):
            RecordsQueue.__init__(self=self.mock_records_queue,
                                  records_type=records_type,
                                  history_size=history_size)
        mock_isinstance.assert_called_once_with(history_size, int)

    @pytest.mark.parametrize("records_type", [Mock(), "some type"])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__value_error(self, mock_isinstance, mock_issubclass, records_type):
        mock_isinstance.return_value = True
        mock_issubclass.return_value = True
        mock_le = Mock(return_value=True)
        mock_history_size = Mock(__le__=mock_le)
        with pytest.raises(ValueError):
            RecordsQueue.__init__(self=self.mock_records_queue,
                                  records_type=records_type,
                                  history_size=mock_history_size)
        mock_isinstance.assert_called_once_with(mock_history_size, int)
        mock_issubclass.assert_called_once_with(records_type, (UdsMessageRecord, AbstractUdsPacketRecord))
        mock_le.assert_called_once_with(0)

    @pytest.mark.parametrize("records_type", [Mock(), "some type"])
    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__valid(self, mock_isinstance, mock_issubclass, records_type):
        mock_isinstance.return_value = True
        mock_issubclass.return_value = True
        mock_le = Mock(return_value=False)
        mock_history_size = Mock(__le__=mock_le)
        assert RecordsQueue.__init__(self=self.mock_records_queue,
                                     records_type=records_type,
                                     history_size=mock_history_size) is None
        mock_isinstance.assert_called_once_with(mock_history_size, int)
        mock_issubclass.assert_called_once_with(records_type, (UdsMessageRecord, AbstractUdsPacketRecord))
        mock_le.assert_called_once_with(0)
        self.mock_event_class.assert_called_once_with()
        assert self.mock_records_queue._RecordsQueue__records_type == records_type
        assert self.mock_records_queue._RecordsQueue__history_size == mock_history_size
        assert self.mock_records_queue._RecordsQueue__total_records_number == 0
        assert self.mock_records_queue._RecordsQueue__records_history == []
        assert self.mock_records_queue._RecordsQueue__event_new_record == self.mock_event_class.return_value

    # records_type

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_records_type__get(self, value):
        self.mock_records_queue._RecordsQueue__records_type = value
        assert RecordsQueue.records_type.fget(self.mock_records_queue) == value
        
    # history_size

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_history_size__get(self, value):
        self.mock_records_queue._RecordsQueue__history_size = value
        assert RecordsQueue.history_size.fget(self.mock_records_queue) == value
        
    # total_records_number

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_total_records_number__get(self, value):
        self.mock_records_queue._RecordsQueue__total_records_number = value
        assert RecordsQueue.total_records_number.fget(self.mock_records_queue) == value

    # records_history

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.tuple")
    def test_records_history__get(self, mock_tuple, value):
        self.mock_records_queue._RecordsQueue__records_history = value
        assert RecordsQueue.records_history.fget(self.mock_records_queue) == mock_tuple.return_value
        mock_tuple.assert_called_once_with(value)

    # clear_records_history

    def test_clear_records_history(self):
        assert RecordsQueue.clear_records_history(self.mock_records_queue) is None
        assert self.mock_records_queue._RecordsQueue__records_history == []
        assert self.mock_records_queue._RecordsQueue__total_records_number == 0

    # put_record

    @pytest.mark.parametrize("record", ["some record", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_record__type_error(self, mock_isinstance, record):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            RecordsQueue.put_record(self=self.mock_records_queue, record=record)
        mock_isinstance.assert_called_once_with(record, self.mock_records_queue.records_type)

    @pytest.mark.parametrize("records_history, history_size", [
        ([], 0),
        (list(range(10)), 15),
        (["record 1", "record 2"], 2),
    ])
    @pytest.mark.parametrize("record, total_records_number", [
        ("some record", 0),
        (Mock(), 12325),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_put_record__valid(self, mock_isinstance, record, total_records_number, records_history, history_size):
        mock_isinstance.return_value = True
        self.mock_records_queue._RecordsQueue__total_records_number = total_records_number
        self.mock_records_queue._RecordsQueue__records_history = deepcopy(records_history)
        self.mock_records_queue._RecordsQueue__event_new_record = Mock()
        self.mock_records_queue.history_size = history_size
        assert RecordsQueue.put_record(self=self.mock_records_queue, record=record) is None
        mock_isinstance.assert_called_once_with(record, self.mock_records_queue.records_type)
        self.mock_records_queue._RecordsQueue__event_new_record.set.assert_called_once_with()
        assert self.mock_records_queue._RecordsQueue__records_history == ([record] + records_history)[:history_size]
        assert self.mock_records_queue._RecordsQueue__total_records_number == total_records_number + 1

    # get_next_record

    @pytest.mark.asyncio
    @pytest.mark.parametrize("records_history", [
        (Mock(), ),
        tuple(range(100)),
    ])
    async def test_get_next_record(self, records_history):
        self.mock_records_queue.records_history = records_history
        self.mock_records_queue._RecordsQueue__event_new_record = Mock(wait=AsyncMock())
        assert await RecordsQueue.get_next_record(self=self.mock_records_queue) == records_history[0]
        self.mock_records_queue._RecordsQueue__event_new_record.clear.assert_called_once_with()
        self.mock_records_queue._RecordsQueue__event_new_record.wait.assert_awaited_once_with()

import pytest
from mock import Mock

from uds.transport_interface.abstract_packet_queue import AbstractPacketsQueue


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

    # mark_task_done

    def test_mark_task_done(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.mark_task_done(self=self.mock_abstract_packets_queue)

    # block

    def test_get_block(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.block(self=self.mock_abstract_packets_queue)

    # clear

    def test_get_clear(self):
        with pytest.raises(NotImplementedError):
            AbstractPacketsQueue.clear(self=self.mock_abstract_packets_queue)


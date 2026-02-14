from time import perf_counter, sleep

import pytest
from mock import MagicMock, Mock, call, patch

from uds.addressing import AddressingType
from uds.client import (
    NRC,
    AbstractTransportInterface,
    Client,
    Empty,
    Event,
    InconsistencyError,
    MessageTransmissionNotStartedError,
    ReassignmentError,
    RequestSID,
    ResponseSID,
    Thread,
    UdsMessage,
    UdsMessageRecord,
    Queue
)

SCRIPT_LOCATION = "uds.client"


class TestClient:
    """Unit tests for `Client` class."""

    def setup_method(self):
        self.mock_client = MagicMock(spec=Client,
                                     _Client__response_queue=Mock(),
                                     _Client__last_physical_response=Mock(),
                                     _Client__last_functional_response=Mock())
        # patching
        self._patcher_sleep = patch(f"{SCRIPT_LOCATION}.sleep")
        self.mock_sleep = self._patcher_sleep.start()
        self._patcher_min = patch(f"{SCRIPT_LOCATION}.min")
        self.mock_min = self._patcher_min.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_thread = patch(f"{SCRIPT_LOCATION}.Thread")
        self.mock_thread = self._patcher_thread.start()
        self._patcher_event = patch(f"{SCRIPT_LOCATION}.Event")
        self.mock_event = self._patcher_event.start()
        self._patcher_lock = patch(f"{SCRIPT_LOCATION}.Lock")
        self.mock_lock = self._patcher_lock.start()
        self._patcher_queue = patch(f"{SCRIPT_LOCATION}.Queue")
        self.mock_queue = self._patcher_queue.start()
        self._patcher_tester_present = patch(f"{SCRIPT_LOCATION}.TESTER_PRESENT")
        self.mock_tester_present = self._patcher_tester_present.start()
        self._patcher_validate_request_sid = patch(f"{SCRIPT_LOCATION}.RequestSID.validate_member")
        self.mock_validate_request_sid = self._patcher_validate_request_sid.start()

    def teardown_method(self):
        self._patcher_sleep.stop()
        self._patcher_min.stop()
        self._patcher_warn.stop()
        self._patcher_perf_counter.stop()
        self._patcher_thread.stop()
        self._patcher_event.stop()
        self._patcher_lock.stop()
        self._patcher_tester_present.stop()
        self._patcher_validate_request_sid.stop()

    # __init__

    @pytest.mark.parametrize("transport_interface", [Mock(), "Some transport interface"])
    def test_init__mandatory_args(self, transport_interface):
        assert Client.__init__(self.mock_client,
                               transport_interface=transport_interface) is None
        # measurements
        assert self.mock_client._Client__p2_client_measured is None
        assert self.mock_client._Client__p2_ext_client_measured is None
        assert self.mock_client._Client__p6_client_measured is None
        assert self.mock_client._Client__p6_ext_client_measured is None
        # defaults
        assert self.mock_client._Client__p2_client_timeout == self.mock_client.DEFAULT_P2_CLIENT_TIMEOUT
        assert self.mock_client._Client__p2_ext_client_timeout == self.mock_client.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        assert self.mock_client._Client__p3_client_physical == self.mock_client.DEFAULT_P3_CLIENT
        assert self.mock_client._Client__p3_client_functional == self.mock_client.DEFAULT_P3_CLIENT
        assert self.mock_client._Client__p6_client_timeout == self.mock_client.DEFAULT_P6_CLIENT_TIMEOUT
        assert self.mock_client._Client__p6_ext_client_timeout == self.mock_client.DEFAULT_P6_EXT_CLIENT_TIMEOUT
        assert self.mock_client._Client__s3_client == self.mock_client.DEFAULT_S3_CLIENT
        # assignment
        assert self.mock_client.transport_interface == transport_interface
        assert self.mock_client.p2_client_timeout == Client.DEFAULT_P2_CLIENT_TIMEOUT
        assert self.mock_client.p2_ext_client_timeout == Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        assert self.mock_client.p3_client_physical == Client.DEFAULT_P3_CLIENT
        assert self.mock_client.p3_client_functional == Client.DEFAULT_P3_CLIENT
        assert self.mock_client.p6_client_timeout == Client.DEFAULT_P6_CLIENT_TIMEOUT
        assert self.mock_client.p6_ext_client_timeout == Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT
        assert self.mock_client.s3_client == Client.DEFAULT_S3_CLIENT
        # internal attributes
        assert self.mock_client._Client__tester_present_task_event == self.mock_event.return_value
        assert self.mock_client._Client__tester_present_thread is None
        assert self.mock_client._Client__background_receiving_task_event == self.mock_event.return_value
        assert self.mock_client._Client__break_in_background_receiving_event == self.mock_event.return_value
        assert self.mock_client._Client__background_receiving_thread is None
        assert self.mock_client._Client__send_and_receive_not_in_progress_event == self.mock_event.return_value
        assert self.mock_client._Client__receiving_not_in_progress_event == self.mock_event.return_value
        assert self.mock_client._Client__transmission_not_in_progress_event == self.mock_event.return_value
        assert self.mock_client._Client__receiving_lock == self.mock_lock.return_value
        assert self.mock_client._Client__transmission_lock == self.mock_lock.return_value
        assert self.mock_client._Client__physical_transmission_lock == self.mock_lock.return_value
        assert self.mock_client._Client__functional_transmission_lock == self.mock_lock.return_value
        assert self.mock_client._Client__response_queue == self.mock_queue.return_value
        assert self.mock_client._Client__last_physical_request is None
        assert self.mock_client._Client__last_physical_response is None
        assert self.mock_client._Client__last_functional_request is None
        assert self.mock_client._Client__last_functional_response is None
        assert self.mock_client._Client__last_tester_present_requests == []

    @pytest.mark.parametrize("transport_interface, p2_client_timeout, p2_ext_client_timeout, "
                             "p3_client_physical, p3_client_functional, p6_client_timeout, p6_ext_client_timeout, "
                             "s3_client", [
        (Mock(), Mock(), Mock(), Mock(), Mock(),  Mock(), Mock() ,Mock()),
        ("TI", "P2Client", "P2*Client", "P3Client_Phys", "P3Client_Func", "P6Client", "P6*Client", "S3Client"),
    ])
    def test_init__all_args(self, transport_interface, p2_client_timeout, p2_ext_client_timeout,
                            p3_client_physical, p3_client_functional, p6_client_timeout, p6_ext_client_timeout,
                            s3_client):
        assert Client.__init__(self.mock_client,
                               transport_interface=transport_interface,
                               p2_client_timeout=p2_client_timeout,
                               p2_ext_client_timeout=p2_ext_client_timeout,
                               p3_client_physical=p3_client_physical,
                               p3_client_functional=p3_client_functional,
                               p6_client_timeout=p6_client_timeout,
                               p6_ext_client_timeout=p6_ext_client_timeout,
                               s3_client=s3_client) is None
        # measurements
        assert self.mock_client._Client__p2_client_measured is None
        assert self.mock_client._Client__p2_ext_client_measured is None
        assert self.mock_client._Client__p6_client_measured is None
        assert self.mock_client._Client__p6_ext_client_measured is None
        # defaults
        assert self.mock_client._Client__p2_client_timeout == self.mock_client.DEFAULT_P2_CLIENT_TIMEOUT
        assert self.mock_client._Client__p2_ext_client_timeout == self.mock_client.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        assert self.mock_client._Client__p3_client_physical == self.mock_client.DEFAULT_P3_CLIENT
        assert self.mock_client._Client__p3_client_functional == self.mock_client.DEFAULT_P3_CLIENT
        assert self.mock_client._Client__p6_client_timeout == self.mock_client.DEFAULT_P6_CLIENT_TIMEOUT
        assert self.mock_client._Client__p6_ext_client_timeout == self.mock_client.DEFAULT_P6_EXT_CLIENT_TIMEOUT
        assert self.mock_client._Client__s3_client == self.mock_client.DEFAULT_S3_CLIENT
        # assignment
        assert self.mock_client.transport_interface == transport_interface
        assert self.mock_client.p2_client_timeout == p2_client_timeout
        assert self.mock_client.p2_ext_client_timeout == p2_ext_client_timeout
        assert self.mock_client.p3_client_physical == p3_client_physical
        assert self.mock_client.p3_client_functional == p3_client_functional
        assert self.mock_client.p6_client_timeout == p6_client_timeout
        assert self.mock_client.p6_ext_client_timeout == p6_ext_client_timeout
        assert self.mock_client.s3_client == s3_client
        # internal attributes
        assert self.mock_client._Client__tester_present_task_event == self.mock_event.return_value
        assert self.mock_client._Client__tester_present_thread is None
        assert self.mock_client._Client__background_receiving_task_event == self.mock_event.return_value
        assert self.mock_client._Client__break_in_background_receiving_event == self.mock_event.return_value
        assert self.mock_client._Client__background_receiving_thread is None
        assert self.mock_client._Client__send_and_receive_not_in_progress_event == self.mock_event.return_value
        assert self.mock_client._Client__receiving_not_in_progress_event == self.mock_event.return_value
        assert self.mock_client._Client__transmission_not_in_progress_event == self.mock_event.return_value
        assert self.mock_client._Client__receiving_lock == self.mock_lock.return_value
        assert self.mock_client._Client__transmission_lock == self.mock_lock.return_value
        assert self.mock_client._Client__physical_transmission_lock == self.mock_lock.return_value
        assert self.mock_client._Client__functional_transmission_lock == self.mock_lock.return_value
        assert self.mock_client._Client__response_queue == self.mock_queue.return_value
        assert self.mock_client._Client__last_physical_request is None
        assert self.mock_client._Client__last_physical_response is None
        assert self.mock_client._Client__last_functional_request is None
        assert self.mock_client._Client__last_functional_response is None
        assert self.mock_client._Client__last_tester_present_requests == []

    # __del__

    @pytest.mark.parametrize("is_tester_present_sent, is_background_receiving", [
        (False, True),
        (True, False),
        (True, True),
    ])
    def test_del(self, is_tester_present_sent, is_background_receiving):
        self.mock_client.is_tester_present_sent = is_tester_present_sent
        self.mock_client.is_background_receiving = is_background_receiving
        assert Client.__del__(self.mock_client) is None
        if is_tester_present_sent:
            self.mock_client.stop_tester_present.assert_called_once_with()
        else:
            self.mock_client.stop_tester_present.assert_not_called()
        if is_background_receiving:
            self.mock_client.stop_background_receiving.assert_called_once_with()
        else:
            self.mock_client.stop_background_receiving.assert_not_called()

    # transport_interface

    def test_transport_interface__get(self):
        self.mock_client._Client__transport_interface = Mock()
        assert Client.transport_interface.fget(self.mock_client) == self.mock_client._Client__transport_interface

    @pytest.mark.parametrize("transport_interface", [Mock(), "Some transport interface"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_transport_interface__set__type_error(self, mock_isinstance, transport_interface):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.transport_interface.fset(self.mock_client, transport_interface)
        mock_isinstance.assert_called_once_with(transport_interface, AbstractTransportInterface)

    @pytest.mark.parametrize("transport_interface", [Mock(spec=AbstractTransportInterface),
                                                     MagicMock(spec=AbstractTransportInterface)])
    def test_transport_interface__set__reassignment_error(self, transport_interface):
        self.mock_client._Client__transport_interface = Mock()
        with pytest.raises(ReassignmentError):
            Client.transport_interface.fset(self.mock_client, transport_interface)

    @pytest.mark.parametrize("transport_interface", [Mock(spec=AbstractTransportInterface),
                                                     MagicMock(spec=AbstractTransportInterface)])
    def test_transport_interface__set__valid(self, transport_interface):
        assert Client.transport_interface.fset(self.mock_client, transport_interface) is None
        assert self.mock_client._Client__transport_interface == transport_interface

    # p2_client_timeout

    def test_p2_client_timeout__get(self):
        self.mock_client._Client__p2_client_timeout = Mock()
        assert Client.p2_client_timeout.fget(self.mock_client) == self.mock_client._Client__p2_client_timeout

    @pytest.mark.parametrize("p2_client_timeout", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_p2_client_timeout__set__type_error(self, mock_isinstance, p2_client_timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout)
        mock_isinstance.assert_called_once_with(p2_client_timeout, (int, float))

    @pytest.mark.parametrize("p2_client_timeout", [0, -0.01])
    def test_p2_client_timeout__set__value_error(self, p2_client_timeout):
        with pytest.raises(ValueError):
            Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout)

    @pytest.mark.parametrize("p2_client_timeout", [Client.DEFAULT_P2_CLIENT_TIMEOUT, 1])
    def test_p2_client_timeout__set__valid__no_warning(self, p2_client_timeout):
        self.mock_client.p3_client_physical = p2_client_timeout
        self.mock_client.p3_client_functional = p2_client_timeout
        self.mock_client.p6_client_timeout = p2_client_timeout
        assert Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout) is None
        assert self.mock_client._Client__p2_client_timeout == p2_client_timeout
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("p2_client_timeout", [Client.DEFAULT_P2_CLIENT_TIMEOUT, 1])
    def test_p2_client_timeout__set__valid__warn_p3_client_physical(self, p2_client_timeout):
        self.mock_client.p3_client_physical = p2_client_timeout - 0.1
        self.mock_client.p3_client_functional = p2_client_timeout + 1
        self.mock_client.p6_client_timeout = p2_client_timeout + 1
        assert Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout) is None
        assert self.mock_client._Client__p2_client_timeout == p2_client_timeout
        assert self.mock_client.p3_client_physical == p2_client_timeout
        assert self.mock_client.p3_client_functional > p2_client_timeout
        assert self.mock_client.p6_client_timeout > p2_client_timeout
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_client_timeout", [Client.DEFAULT_P2_CLIENT_TIMEOUT, 1])
    def test_p2_client_timeout__set__valid__warn_p3_client_functional(self, p2_client_timeout):
        self.mock_client.p3_client_physical = p2_client_timeout + 1
        self.mock_client.p3_client_functional = p2_client_timeout - 0.1
        self.mock_client.p6_client_timeout = p2_client_timeout + 1
        assert Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout) is None
        assert self.mock_client._Client__p2_client_timeout == p2_client_timeout
        assert self.mock_client.p3_client_physical > p2_client_timeout
        assert self.mock_client.p3_client_functional == p2_client_timeout
        assert self.mock_client.p6_client_timeout > p2_client_timeout
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_client_timeout", [Client.DEFAULT_P2_CLIENT_TIMEOUT, 1])
    def test_p2_client_timeout__set__valid__warn_p6_client_timeout(self, p2_client_timeout):
        self.mock_client.p3_client_physical = p2_client_timeout + 1
        self.mock_client.p3_client_functional = p2_client_timeout + 1
        self.mock_client.p6_client_timeout = p2_client_timeout - 0.1
        assert Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout) is None
        assert self.mock_client._Client__p2_client_timeout == p2_client_timeout
        assert self.mock_client.p3_client_physical > p2_client_timeout
        assert self.mock_client.p3_client_functional > p2_client_timeout
        assert self.mock_client.p6_client_timeout == p2_client_timeout
        self.mock_warn.assert_called_once()

    # p2_client_measured

    def test_p2_client_measured__get(self):
        self.mock_client._Client__p2_client_measured = Mock()
        assert Client.p2_client_measured.fget(self.mock_client) == self.mock_client._Client__p2_client_measured

    # p2_ext_client_timeout

    def test_p2_ext_client_timeout__get(self):
        self.mock_client._Client__p2_ext_client_timeout = Mock()
        assert Client.p2_ext_client_timeout.fget(self.mock_client) == self.mock_client._Client__p2_ext_client_timeout

    @pytest.mark.parametrize("p2_ext_client_timeout", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_p2_ext_client_timeout__set__type_error(self, mock_isinstance, p2_ext_client_timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.p2_ext_client_timeout.fset(self.mock_client, p2_ext_client_timeout)
        mock_isinstance.assert_called_once_with(p2_ext_client_timeout, (int, float))

    @pytest.mark.parametrize("p2_ext_client_timeout", [0, -0.01])
    def test_p2_ext_client_timeout__set__value_error(self, p2_ext_client_timeout):
        with pytest.raises(ValueError):
            Client.p2_ext_client_timeout.fset(self.mock_client, p2_ext_client_timeout)

    @pytest.mark.parametrize("p2_ext_client_timeout", [Client.DEFAULT_P2_CLIENT_TIMEOUT, 1])
    def test_p2_ext_client_timeout__set__valid__no_warning(self, p2_ext_client_timeout):
        self.mock_client.p6_ext_client_timeout = p2_ext_client_timeout
        assert Client.p2_ext_client_timeout.fset(self.mock_client, p2_ext_client_timeout) is None
        assert self.mock_client._Client__p2_ext_client_timeout == p2_ext_client_timeout
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("p2_ext_client_timeout", [Client.DEFAULT_P2_CLIENT_TIMEOUT, 1])
    def test_p2_ext_client_timeout__set__valid__warn_p6_ext_client_timeout(self, p2_ext_client_timeout):
        self.mock_client.p6_ext_client_timeout = p2_ext_client_timeout - 0.1
        assert Client.p2_ext_client_timeout.fset(self.mock_client, p2_ext_client_timeout) is None
        assert self.mock_client._Client__p2_ext_client_timeout == p2_ext_client_timeout
        assert self.mock_client.p6_ext_client_timeout == p2_ext_client_timeout
        self.mock_warn.assert_called_once()

    # p2_ext_client_measured

    def test_p2_ext_client_measured__get(self):
        self.mock_client._Client__p2_ext_client_measured = Mock()
        assert Client.p2_ext_client_measured.fget(self.mock_client) == self.mock_client._Client__p2_ext_client_measured

    # p3_client_physical

    def test_p3_client_physical__get(self):
        self.mock_client._Client__p3_client_physical = Mock()
        assert Client.p3_client_physical.fget(self.mock_client) == self.mock_client._Client__p3_client_physical

    @pytest.mark.parametrize("p3_client_physical", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_p3_client_physical__set__type_error(self, mock_isinstance, p3_client_physical):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.p3_client_physical.fset(self.mock_client, p3_client_physical)
        mock_isinstance.assert_called_once_with(p3_client_physical, (int, float))

    @pytest.mark.parametrize("p3_client_physical", [0, -0.01])
    def test_p3_client_physical__set__value_error(self, p3_client_physical):
        with pytest.raises(ValueError):
            Client.p3_client_physical.fset(self.mock_client, p3_client_physical)

    @pytest.mark.parametrize("p3_client_physical, p2_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT + 0.1),
        (49, 50),
    ])
    def test_p3_client_physical__set__inconsistent(self, p3_client_physical, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        with pytest.raises(InconsistencyError):
            Client.p3_client_physical.fset(self.mock_client, p3_client_physical)

    @pytest.mark.parametrize("p3_client_physical, p2_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P2_CLIENT_TIMEOUT),
        (123, 123),
    ])
    def test_p3_client_physical__set__valid__no_warning(self, p3_client_physical, p2_client_timeout):
        self.mock_client.s3_client = p3_client_physical
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client.p3_client_physical.fset(self.mock_client, p3_client_physical) is None
        assert self.mock_client._Client__p3_client_physical == p3_client_physical
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("p3_client_physical, p2_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P2_CLIENT_TIMEOUT),
        (123, 123),
    ])
    def test_p3_client_physical__set__valid__warn_s3_client(self, p3_client_physical, p2_client_timeout):
        self.mock_client.s3_client = p3_client_physical - 0.1
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client.p3_client_physical.fset(self.mock_client, p3_client_physical) is None
        assert self.mock_client._Client__p3_client_physical == p3_client_physical
        assert self.mock_client.s3_client == p3_client_physical
        self.mock_warn.assert_called_once()

    # p3_client_functional

    def test_p3_client_functional__get(self):
        self.mock_client._Client__p3_client_functional = Mock()
        assert Client.p3_client_functional.fget(self.mock_client) == self.mock_client._Client__p3_client_functional

    @pytest.mark.parametrize("p3_client_functional", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_p3_client_functional__set__type_error(self, mock_isinstance, p3_client_functional):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.p3_client_functional.fset(self.mock_client, p3_client_functional)
        mock_isinstance.assert_called_once_with(p3_client_functional, (int, float))

    @pytest.mark.parametrize("p3_client_functional", [0, -0.01])
    def test_p3_client_functional__set__value_error(self, p3_client_functional):
        with pytest.raises(ValueError):
            Client.p3_client_functional.fset(self.mock_client, p3_client_functional)

    @pytest.mark.parametrize("p3_client_functional, p2_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT + 0.1),
        (49, 50),
    ])
    def test_p3_client_functional__set__inconsistent(self, p3_client_functional, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        with pytest.raises(InconsistencyError):
            Client.p3_client_functional.fset(self.mock_client, p3_client_functional)

    @pytest.mark.parametrize("p3_client_functional, p2_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P2_CLIENT_TIMEOUT),
        (123, 123),
    ])
    def test_p3_client_functional__set__valid__no_warning(self, p3_client_functional, p2_client_timeout):
        self.mock_client.s3_client = p3_client_functional
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client.p3_client_functional.fset(self.mock_client, p3_client_functional) is None
        assert self.mock_client._Client__p3_client_functional == p3_client_functional
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("p3_client_functional, p2_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P2_CLIENT_TIMEOUT),
        (123, 123),
    ])
    def test_p3_client_functional__set__valid__warn_s3_client(self, p3_client_functional, p2_client_timeout):
        self.mock_client.s3_client = p3_client_functional - 0.1
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client.p3_client_functional.fset(self.mock_client, p3_client_functional) is None
        assert self.mock_client._Client__p3_client_functional == p3_client_functional
        assert self.mock_client.s3_client == p3_client_functional
        self.mock_warn.assert_called_once()

    # p6_client_timeout

    def test_p6_client_timeout__get(self):
        self.mock_client._Client__p6_client_timeout = Mock()
        assert Client.p6_client_timeout.fget(self.mock_client) == self.mock_client._Client__p6_client_timeout

    @pytest.mark.parametrize("p6_client_timeout", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_p6_client_timeout__set__type_error(self, mock_isinstance, p6_client_timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.p6_client_timeout.fset(self.mock_client, p6_client_timeout)
        mock_isinstance.assert_called_once_with(p6_client_timeout, (int, float))

    @pytest.mark.parametrize("p6_client_timeout", [0, -0.01])
    def test_p6_client_timeout__set__value_error(self, p6_client_timeout):
        with pytest.raises(ValueError):
            Client.p6_client_timeout.fset(self.mock_client, p6_client_timeout)

    @pytest.mark.parametrize("p6_client_timeout, p2_client_timeout", [
        (Client.DEFAULT_P6_CLIENT_TIMEOUT, Client.DEFAULT_P6_CLIENT_TIMEOUT + 0.1),
        (100, 101),
    ])
    def test_p6_client_timeout__set__inconsistent(self, p6_client_timeout, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        with pytest.raises(InconsistencyError):
            Client.p6_client_timeout.fset(self.mock_client, p6_client_timeout)

    @pytest.mark.parametrize("p6_client_timeout, p2_client_timeout", [
        (Client.DEFAULT_P6_CLIENT_TIMEOUT, Client.DEFAULT_P6_CLIENT_TIMEOUT),
        (100, 99),
    ])
    def test_p6_client_timeout__set__valid__no_warning(self, p6_client_timeout, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        self.mock_client.p6_ext_client_timeout = p6_client_timeout
        assert Client.p6_client_timeout.fset(self.mock_client, p6_client_timeout) is None
        assert self.mock_client._Client__p6_client_timeout == p6_client_timeout
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("p6_client_timeout", [Client.DEFAULT_P6_CLIENT_TIMEOUT, 12345])
    def test_p6_client_timeout__set__valid__warn_p6_ext_client_timeout(self, p6_client_timeout):
        self.mock_client.p2_client_timeout = p6_client_timeout
        self.mock_client.p6_ext_client_timeout = p6_client_timeout - 0.1
        assert Client.p6_client_timeout.fset(self.mock_client, p6_client_timeout) is None
        assert self.mock_client._Client__p6_client_timeout == p6_client_timeout
        assert self.mock_client.p6_ext_client_timeout == p6_client_timeout
        self.mock_warn.assert_called_once()

    # p6_client_measured

    def test_p6_client_measured__get(self):
        self.mock_client._Client__p6_client_measured = Mock()
        assert Client.p6_client_measured.fget(self.mock_client) == self.mock_client._Client__p6_client_measured

    # p6_ext_client_timeout

    def test_p6_ext_client_timeout__get(self):
        self.mock_client._Client__p6_ext_client_timeout = Mock()
        assert Client.p6_ext_client_timeout.fget(self.mock_client) == self.mock_client._Client__p6_ext_client_timeout

    @pytest.mark.parametrize("p6_ext_client_timeout", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_p6_ext_client_timeout__set__type_error(self, mock_isinstance, p6_ext_client_timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.p6_ext_client_timeout.fset(self.mock_client, p6_ext_client_timeout)
        mock_isinstance.assert_called_once_with(p6_ext_client_timeout, (int, float))

    @pytest.mark.parametrize("p6_ext_client_timeout", [0, -0.01])
    def test_p6_ext_client_timeout__set__value_error(self, p6_ext_client_timeout):
        with pytest.raises(ValueError):
            Client.p6_ext_client_timeout.fset(self.mock_client, p6_ext_client_timeout)

    @pytest.mark.parametrize("p6_ext_client_timeout, p2_ext_client_timeout, p6_client_timeout", [
        (Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT, Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT + 0.1,
         Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT),
        (1000, 50, 1001),
    ])
    def test_p6_ext_client_timeout__set__inconsistent(self, p6_ext_client_timeout,
                                                      p2_ext_client_timeout, p6_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        self.mock_client.p6_client_timeout = p6_client_timeout
        with pytest.raises(InconsistencyError):
            Client.p6_ext_client_timeout.fset(self.mock_client, p6_ext_client_timeout)

    @pytest.mark.parametrize("p6_ext_client_timeout, p2_ext_client_timeout, p6_client_timeout", [
        (Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT, Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT, Client.DEFAULT_P6_CLIENT_TIMEOUT),
        (Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT, Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT,
         Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT),
    ])
    def test_p6_ext_client_timeout__set__valid(self, p6_ext_client_timeout,
                                               p2_ext_client_timeout, p6_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client.p6_ext_client_timeout.fset(self.mock_client, p6_ext_client_timeout) is None
        assert self.mock_client._Client__p6_ext_client_timeout == p6_ext_client_timeout

    # p6_ext_client_measured

    def test_p6_ext_client_measured__get(self):
        self.mock_client._Client__p6_ext_client_measured = Mock()
        assert Client.p6_ext_client_measured.fget(self.mock_client) == self.mock_client._Client__p6_ext_client_measured

    # s3_client

    def test_s3_client__get(self):
        self.mock_client._Client__s3_client = Mock()
        assert Client.s3_client.fget(self.mock_client) == self.mock_client._Client__s3_client

    @pytest.mark.parametrize("s3_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_s3_client__set__type_error(self, mock_isinstance, s3_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.s3_client.fset(self.mock_client, s3_client)
        mock_isinstance.assert_called_once_with(s3_client, (int, float))

    @pytest.mark.parametrize("s3_client", [0, -0.01])
    def test_s3_client__set__value_error(self, s3_client):
        with pytest.raises(ValueError):
            Client.s3_client.fset(self.mock_client, s3_client)

    @pytest.mark.parametrize("s3_client, p3_client_physical, p3_client_functional", [
        (Client.DEFAULT_P3_CLIENT - 0.1, Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT),
        (249, 100, 250),
    ])
    def test_s3_client__set__inconsistent(self, s3_client, p3_client_physical, p3_client_functional):
        self.mock_client.p3_client_physical = p3_client_physical
        self.mock_client.p3_client_functional = p3_client_functional
        with pytest.raises(InconsistencyError):
            Client.s3_client.fset(self.mock_client, s3_client)

    @pytest.mark.parametrize("s3_client, p3_client_physical, p3_client_functional", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT),
        (500, 100, 250),
    ])
    def test_s3_client__set__valid(self, s3_client, p3_client_physical, p3_client_functional):
        self.mock_client.p3_client_physical = p3_client_physical
        self.mock_client.p3_client_functional = p3_client_functional
        assert Client.s3_client.fset(self.mock_client, s3_client) is None
        assert self.mock_client._Client__s3_client == s3_client

    # last_sent_tester_present_requests

    @pytest.mark.parametrize("last_tester_present_requests", [
        [Mock()],
        range(5),
    ])
    def test_last_sent_tester_present_requests(self, last_tester_present_requests):
        self.mock_client._Client__last_tester_present_requests = last_tester_present_requests
        assert Client.last_sent_tester_present_requests.fget(self.mock_client) == tuple(last_tester_present_requests)

    # last_sent_request

    @pytest.mark.parametrize("last_physical, last_functional, last_sent_request", [
        (None, None, None),
        (Mock(transmission_end_timestamp=1), None, "last_physical"),
        (None, Mock(transmission_end_timestamp=2), "last_functional"),
        (Mock(transmission_end_timestamp=3.5), Mock(transmission_end_timestamp=3.6), "last_functional"),
        (Mock(transmission_end_timestamp=3.8), Mock(transmission_end_timestamp=3.7), "last_physical"),
    ])
    def test_last_sent_request(self, last_physical, last_functional, last_sent_request):
        self.mock_client._Client__last_physical_request = last_physical
        self.mock_client._Client__last_functional_request = last_functional
        if last_sent_request is None:
            assert Client.last_sent_request.fget(self.mock_client) is None
        elif last_sent_request == "last_physical":
            assert Client.last_sent_request.fget(self.mock_client) is last_physical
        elif last_sent_request == "last_functional":
            assert Client.last_sent_request.fget(self.mock_client) is last_functional
        else:
            raise AssertionError

    # last_received_response

    @pytest.mark.parametrize("last_physical, last_functional, last_received_response", [
        (None, None, None),
        (Mock(transmission_end_timestamp=1), None, "last_physical"),
        (None, Mock(transmission_end_timestamp=2), "last_functional"),
        (Mock(transmission_end_timestamp=3.5), Mock(transmission_end_timestamp=3.6), "last_functional"),
        (Mock(transmission_end_timestamp=3.8), Mock(transmission_end_timestamp=3.7), "last_physical"),
    ])
    def test_last_received_response(self, last_physical, last_functional, last_received_response):
        self.mock_client._Client__last_physical_response = last_physical
        self.mock_client._Client__last_functional_response = last_functional
        if last_received_response is None:
            assert Client.last_received_response.fget(self.mock_client) is None
        elif last_received_response == "last_physical":
            assert Client.last_received_response.fget(self.mock_client) is last_physical
        elif last_received_response == "last_functional":
            assert Client.last_received_response.fget(self.mock_client) is last_functional
        else:
            raise AssertionError

    # is_background_receiving

    def test_is_background_receiving__true(self):
        self.mock_client._Client__background_receiving_task_event = Mock(is_set=Mock(return_value=True))
        assert Client.is_background_receiving.fget(self.mock_client) is True

    def test_is_background_receiving__false(self):
        self.mock_client._Client__background_receiving_task_event = Mock(is_set=Mock(return_value=False))
        assert Client.is_background_receiving.fget(self.mock_client) is False

    # is_tester_present_sent

    def test_is_tester_present_sent__true(self):
        self.mock_client._Client__tester_present_task_event = Mock(is_set=Mock(return_value=True))
        assert Client.is_tester_present_sent.fget(self.mock_client) is True

    def test_is_tester_present_sent__false(self):
        self.mock_client._Client__tester_present_task_event = Mock(is_set=Mock(return_value=False))
        assert Client.is_tester_present_sent.fget(self.mock_client) is False

    # is_ready_for_physical_transmission

    @pytest.mark.parametrize("transmission_not_in_progress, receiving_not_in_progress,"
                             "last_physical_request, last_physical_response,"
                             "p3_client_physical, perf_counter_value,"
                             "excepted_output", [
        (True, True, None, None, 100, 0, True),
        (False, True, None, None, 100, 0, False),
        (True, False, None, None, 100, 0, False),
        (True, True, Mock(transmission_end_timestamp=1.), None, 125, 1.125, False),
        (True, True, Mock(transmission_end_timestamp=1.), None, 125, 1.125001, True),
        (True, True, Mock(transmission_end_timestamp=5.6), None, 1000, 6.6, False),
        (True, True, Mock(transmission_end_timestamp=5.6), None, 1000, 6.60001, True),
        (True, True, Mock(transmission_end_timestamp=5.6), Mock(), 1000, 5.7, True),
    ])
    def test_is_ready_for_physical_transmission(self, transmission_not_in_progress,
                                                receiving_not_in_progress,
                                                last_physical_request,
                                                last_physical_response,
                                                p3_client_physical, perf_counter_value,
                                                excepted_output):
        self.mock_client._Client__transmission_not_in_progress_event = Mock(is_set=Mock(return_value=transmission_not_in_progress))
        self.mock_client._Client__receiving_not_in_progress_event = Mock(is_set=Mock(return_value=receiving_not_in_progress))
        self.mock_client._Client__last_physical_request = last_physical_request
        self.mock_client._Client__last_physical_response = last_physical_response
        self.mock_client.p3_client_physical = p3_client_physical
        self.mock_perf_counter.return_value = perf_counter_value
        assert Client.is_ready_for_physical_transmission.fget(self.mock_client) == excepted_output

    # is_ready_for_functional_transmission

    @pytest.mark.parametrize("transmission_not_in_progress, last_functional_request, p3_client_functional, "
                             "perf_counter_value, excepted_output", [
        (True, None, 100, 0, True),
        (False, None, 100, 0, False),
        (True, Mock(transmission_end_timestamp=1.), 125, 1.125, False),
        (True, Mock(transmission_end_timestamp=1.), 125, 1.125001, True),
        (True, Mock(transmission_end_timestamp=49.2), 65, 49.265, False),
        (True, Mock(transmission_end_timestamp=49.2), 65, 49.265001, True),
    ])
    def test_is_ready_for_functional_transmission(self, transmission_not_in_progress,
                                                last_functional_request,
                                                p3_client_functional, perf_counter_value,
                                                excepted_output):
        self.mock_client._Client__transmission_not_in_progress_event = Mock(is_set=Mock(return_value=transmission_not_in_progress))
        self.mock_client._Client__last_functional_request = last_functional_request
        self.mock_client.p3_client_functional = p3_client_functional
        self.mock_perf_counter.return_value = perf_counter_value
        assert Client.is_ready_for_functional_transmission.fget(self.mock_client) == excepted_output

    # __update_p2_client_measured

    @pytest.mark.parametrize("p2_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p2_client_measured__type_error(self, mock_isinstance, p2_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._Client__update_p2_client_measured(self.mock_client, p2_client)
        mock_isinstance.assert_called_once_with(p2_client, (int, float))

    @pytest.mark.parametrize("p2_client", [0, -0.01])
    def test_update_p2_client_measured__value_error(self, p2_client):
        with pytest.raises(ValueError):
            Client._Client__update_p2_client_measured(self.mock_client, p2_client)

    @pytest.mark.parametrize("p2_client_measured, p2_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p2_client_measured__valid__with_warning(self, p2_client_measured, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client._Client__update_p2_client_measured(self.mock_client, p2_client_measured) is None
        assert self.mock_client._Client__p2_client_measured == p2_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_client_measured, p2_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p2_client_measured__valid__without_warning(self, p2_client_measured, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client._Client__update_p2_client_measured(self.mock_client, p2_client_measured) is None
        assert self.mock_client._Client__p2_client_measured == p2_client_measured
        self.mock_warn.assert_not_called()

    # __update_p2_ext_client_measured

    def test_update_p2_ext_client_measured__runtime_error(self):
        with pytest.raises(RuntimeError):
            Client._Client__update_p2_ext_client_measured(self.mock_client)

    @pytest.mark.parametrize("p2_ext_client_measured_list", [
        [Mock()],
        [Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT, "Some time", Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT],
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p2_ext_client_measured__type_error(self, mock_isinstance, p2_ext_client_measured_list):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._Client__update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list)
        mock_isinstance.assert_called_with(p2_ext_client_measured_list[0], (int, float))

    @pytest.mark.parametrize("p2_ext_client_measured_list", [
        [0],
        [Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT, -0.01, Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT],
    ])
    def test_update_p2_ext_client_measured__value_error(self, p2_ext_client_measured_list):
        self.mock_client.p2_ext_client_timeout = Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        with pytest.raises(ValueError):
            Client._Client__update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list)

    @pytest.mark.parametrize("p2_ext_client_measured_list, p2_ext_client_timeout", [
        ([1.001], 1),
        ([100, 100.1, 25, 0.25], 100),
    ])
    def test_update_p2_ext_client_measured__valid__with_warning(self, p2_ext_client_measured_list,
                                                                p2_ext_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        assert Client._Client__update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list) is None
        assert self.mock_client._Client__p2_ext_client_measured == tuple(p2_ext_client_measured_list)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_ext_client_measured_list, p2_ext_client_timeout", [
        ([1], 1),
        ([0.00001, 22.75, 99.9999, 100], 100),
    ])
    def test_update_p2_ext_client_measured__valid__without_warning(self, p2_ext_client_measured_list,
                                                                   p2_ext_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        assert Client._Client__update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list) is None
        assert self.mock_client._Client__p2_ext_client_measured == tuple(p2_ext_client_measured_list)
        self.mock_warn.assert_not_called()

    # __update_p6_client_measured

    @pytest.mark.parametrize("p6_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p6_client_measured__type_error(self, mock_isinstance, p6_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._Client__update_p6_client_measured(self.mock_client, p6_client)
        mock_isinstance.assert_called_once_with(p6_client, (int, float))

    @pytest.mark.parametrize("p6_client", [0, -0.01])
    def test_update_p6_client_measured__value_error(self, p6_client):
        with pytest.raises(ValueError):
            Client._Client__update_p6_client_measured(self.mock_client, p6_client)

    @pytest.mark.parametrize("p6_client_measured, p6_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p6_client_measured__valid__with_warning(self, p6_client_measured, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client._Client__update_p6_client_measured(self.mock_client, p6_client_measured) is None
        assert self.mock_client._Client__p6_client_measured == p6_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p6_client_measured, p6_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p6_client_measured__valid__without_warning(self, p6_client_measured, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client._Client__update_p6_client_measured(self.mock_client, p6_client_measured) is None
        assert self.mock_client._Client__p6_client_measured == p6_client_measured
        self.mock_warn.assert_not_called()

    # __update_p6_ext_client_measured

    @pytest.mark.parametrize("p6_ext_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p6_ext_client_measured__type_error(self, mock_isinstance, p6_ext_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._Client__update_p6_ext_client_measured(self.mock_client, p6_ext_client)
        mock_isinstance.assert_called_once_with(p6_ext_client, (int, float))

    @pytest.mark.parametrize("p6_ext_client", [0, -0.01])
    def test_update_p6_ext_client_measured__value_error(self, p6_ext_client):
        with pytest.raises(ValueError):
            Client._Client__update_p6_ext_client_measured(self.mock_client, p6_ext_client)

    @pytest.mark.parametrize("p6_ext_client_measured, p6_ext_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p6_ext_client_measured__valid__with_warning(self, p6_ext_client_measured, p6_ext_client_timeout):
        self.mock_client.p6_ext_client_timeout = p6_ext_client_timeout
        assert Client._Client__update_p6_ext_client_measured(self.mock_client, p6_ext_client_measured) is None
        assert self.mock_client._Client__p6_ext_client_measured == p6_ext_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p6_ext_client_measured, p6_ext_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p6_ext_client_measured__valid__without_warning(self, p6_ext_client_measured, p6_ext_client_timeout):
        self.mock_client.p6_ext_client_timeout = p6_ext_client_timeout
        assert Client._Client__update_p6_ext_client_measured(self.mock_client, p6_ext_client_measured) is None
        assert self.mock_client._Client__p6_ext_client_measured == p6_ext_client_measured
        self.mock_warn.assert_not_called()

    # __receiving_task

    def test_receiving_task__stopped(self):
        self.mock_client.is_background_receiving = False
        assert Client._Client__receiving_task(self.mock_client, cycle=Mock()) is None
        self.mock_client.transport_interface.receive_message.assert_not_called()

    @pytest.mark.parametrize("cycle", [10])
    def test_receiving_task__send_and_receive_in_progress__no_message(self, cycle):
        def _stop_background_receiving(*_, **__):
            self.mock_client.is_background_receiving = False
            raise TimeoutError

        mock_send_and_receive_not_in_progress = Mock(return_value=False)
        mock_set_break_in_background_receiving = Mock()
        mock_clear_break_in_background_receiving = Mock()
        mock_wait = Mock()
        self.mock_client.is_background_receiving = True
        self.mock_client._Client__send_and_receive_not_in_progress_event = Mock(
            is_set=mock_send_and_receive_not_in_progress,
            wait=mock_wait)
        self.mock_client._Client__break_in_background_receiving_event = Mock(
            set=mock_set_break_in_background_receiving,
            clear=mock_clear_break_in_background_receiving)
        self.mock_client._receive_response.side_effect = _stop_background_receiving
        assert Client._Client__receiving_task(self.mock_client, cycle=cycle) is None
        self.mock_sleep.assert_called_once_with(cycle / 1000.)
        mock_send_and_receive_not_in_progress.assert_called_once_with()
        mock_set_break_in_background_receiving.assert_called_once_with()
        mock_wait.assert_called_once_with()
        mock_clear_break_in_background_receiving.assert_called_once_with()
        self.mock_client._receive_response.assert_called_once_with(start_timeout=cycle,
                                                                   end_timeout=self.mock_client.p6_ext_client_timeout)

    @pytest.mark.parametrize("cycle", [13])
    def test_receiving_task__received_message(self, cycle):
        mock_message = Mock()
        def _stop_background_receiving(*_, **__):
            self.mock_client.is_background_receiving = False
            return mock_message

        mock_send_and_receive_not_in_progress = Mock(return_value=True)
        self.mock_client.is_background_receiving = True
        self.mock_client._Client__send_and_receive_not_in_progress_event = Mock(
            is_set=mock_send_and_receive_not_in_progress)
        self.mock_client._receive_response.side_effect = _stop_background_receiving
        assert Client._Client__receiving_task(self.mock_client, cycle=cycle) is None
        self.mock_sleep.assert_called_once_with(cycle / 1000.)
        mock_send_and_receive_not_in_progress.assert_called_once_with()
        self.mock_client._receive_response.assert_called_once_with(start_timeout=cycle,
                                                                   end_timeout=self.mock_client.p6_ext_client_timeout)
        self.mock_client._Client__response_queue.put_nowait.assert_called_once_with(mock_message)


    # __send_tester_present_task

    # @pytest.mark.parametrize("cycle", [10, 321])
    # def test__receiving_task__no_message(self, cycle):
    #     mock_is_set = Mock(side_effect=[False, True])
    #     self.mock_client._Client__receiving_stop_event = Mock(spec=Event, is_set=mock_is_set)
    #     mock_is_waiting = Mock(return_value=False)
    #     self.mock_client._Client__receiving_break_event = Mock(spec=Event, wait=mock_is_waiting)
    #     self.mock_client.transport_interface.receive_message.side_effect = TimeoutError
    #     assert Client._Client__receiving_task(self.mock_client, cycle=cycle) is None
    #     self.mock_client.transport_interface.receive_message.assert_called_once_with(
    #         start_timeout=cycle,
    #         end_timeout=self.mock_client.p6_ext_client_timeout)
    #     self.mock_client._Client__response_queue.put_nowait.assert_not_called()
    #
    # @pytest.mark.parametrize("cycle", [10, 321])
    # def test__receiving_task__1_message(self, cycle):
    #     mock_message = Mock()
    #     mock_is_set = Mock(side_effect=[False, False, False, True])
    #     self.mock_client._Client__receiving_stop_event = Mock(spec=Event, is_set=mock_is_set)
    #     mock_is_waiting = Mock(return_value=False)
    #     self.mock_client._Client__receiving_break_event = Mock(spec=Event, wait=mock_is_waiting)
    #     self.mock_client.transport_interface.receive_message.side_effect = [TimeoutError, mock_message, TimeoutError]
    #     assert Client._Client__receiving_task(self.mock_client, cycle=cycle) is None
    #     assert self.mock_client.transport_interface.receive_message.call_count == 3
    #     self.mock_client._Client__response_queue.put_nowait.assert_called_once_with(mock_message)

























    # _update_measured_client_values

    @pytest.mark.parametrize("request_message, response_messages, p2_client, p6_client", [
        (Mock(spec=UdsMessageRecord,
              transmission_start_timestamp=0,
              transmission_end_timestamp=0.000500),
         (Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=0.014000,
               transmission_end_timestamp=0.015500), ),
         13.5,
         15),
        (Mock(spec=UdsMessageRecord,
              transmission_start_timestamp=17.917304,
              transmission_end_timestamp=17.919054),
         (Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=18.017804,
               transmission_end_timestamp=18.019054),),
         98.75,
         100),
    ])
    def test_update_measured_client_values__direct_response(self, request_message, response_messages,
                                                            p2_client, p6_client):
        assert Client._update_measured_client_values(self.mock_client,
                                                     request_record=request_message,
                                                     response_records=response_messages) is None
        self.mock_client._Client__update_p2_client_measured.assert_called_once_with(p2_client)
        self.mock_client._Client__update_p6_client_measured.assert_called_once_with(p6_client)
        self.mock_client._Client__update_p2_ext_client_measured.assert_not_called()
        self.mock_client._Client__update_p6_ext_client_measured.assert_not_called()
        self.mock_client.assert_not_called()

    @pytest.mark.parametrize("request_message, response_messages, p2_client, p2_ext_client, p6_ext_client", [
        (Mock(spec=UdsMessageRecord,
              transmission_start_timestamp=0,
              transmission_end_timestamp=0.000500),
         (Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=0.014000,
               transmission_end_timestamp=0.015500),
          Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=0.514000,
               transmission_end_timestamp=0.989000)),
         13.5,
         [973.5],
         988.5),
        (Mock(spec=UdsMessageRecord,
              transmission_start_timestamp=17.917304,
              transmission_end_timestamp=17.919054),
         (Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=18.017804,
               transmission_end_timestamp=18.019054),
          Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=18.698454,
               transmission_end_timestamp=18.701304),
          Mock(spec=UdsMessageRecord,
               transmission_start_timestamp=19.017804,
               transmission_end_timestamp=19.019054)),
         98.75,
         [682.25, 317.75],
         1100),
    ])
    def test_update_measured_client_values__delayed_response(self, request_message, response_messages,
                                                             p2_client, p2_ext_client, p6_ext_client):
        assert Client._update_measured_client_values(self.mock_client,
                                                     request_record=request_message,
                                                     response_records=response_messages) is None
        self.mock_client._Client__update_p2_client_measured.assert_called_once_with(p2_client)
        self.mock_client._Client__update_p2_ext_client_measured.assert_called_once_with(*p2_ext_client)
        self.mock_client._Client__update_p6_ext_client_measured.assert_called_once_with(p6_ext_client)
        self.mock_client._Client__update_p6_client_measured.assert_not_called()

    # _receive_response

    @pytest.mark.parametrize("sid, start_timeout, end_timeout, response_records", [
        (
            0x10,
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            [Mock(spec=UdsMessageRecord, payload=b"\x7F\x11\x78"),
             MessageTransmissionNotStartedError]
        ),
        (
            0x22,
            float("inf"),
            float("inf"),
            MessageTransmissionNotStartedError
        ),
    ])
    def test_receive_response__timeout(self, sid, start_timeout, end_timeout, response_records):
        self.mock_client.transport_interface.receive_message.side_effect = response_records
        assert Client._receive_response(self.mock_client,
                                        sid=sid,
                                        start_timeout=start_timeout,
                                        end_timeout=end_timeout) is None
        self.mock_client.transport_interface.receive_message.assert_called()

    @pytest.mark.parametrize("sid, start_timeout, end_timeout, response_record", [
        (
            0x10,
            MagicMock(__gt__=MagicMock(side_effect=[True, False]),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            Mock(spec=UdsMessageRecord, payload=b"\x7F\x11\x78"),
        ),
        (
            0x22,
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(side_effect=[True, False]),
                      __sub__=lambda this, other: this),
            Mock(spec=UdsMessageRecord, payload=b"\x50\x03\x00\x50\x12\x34"),
        ),
    ])
    def test_receive_response__one_other_response(self, sid, start_timeout, end_timeout, response_record):
        self.mock_client.transport_interface.receive_message.return_value = response_record
        assert Client._receive_response(self.mock_client,
                                        sid=sid,
                                        start_timeout=start_timeout,
                                        end_timeout=end_timeout) is None
        self.mock_client._Client__response_queue.put_nowait.assert_called_once_with(response_record)

    @pytest.mark.parametrize("sid, start_timeout, end_timeout, response_records", [
        (
            0x10,
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            [Mock(spec=UdsMessageRecord, payload=b"\x7F\x11\x78"),
             Mock(spec=UdsMessageRecord, payload=b"\x50\x03\x00\x50\x12\x34")]
        ),
        (
            0x22,
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            [   Mock(spec=UdsMessageRecord, payload=b"\x7F\x11\x78"),
                Mock(spec=UdsMessageRecord, payload=b"\x62\x12\x34\x56\x78\x9A\xBC\xDC\xEF\x0F")]
        ),
    ])
    def test_receive_response__positive_response(self, sid, start_timeout, end_timeout, response_records):
        self.mock_client.transport_interface.receive_message.side_effect = response_records
        assert Client._receive_response(self.mock_client,
                                        sid=sid,
                                        start_timeout=start_timeout,
                                        end_timeout=end_timeout) == response_records[-1]
        self.mock_client.transport_interface.receive_message.assert_called()

    @pytest.mark.parametrize("sid, start_timeout, end_timeout, response_records", [
        (
            0x10,
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            [Mock(spec=UdsMessageRecord, payload=b"\x54"),
             Mock(spec=UdsMessageRecord, payload=b"\x7F\x10\x22")]
        ),
        (
            0x22,
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            [Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x78")]
        ),
    ])
    def test_receive_response__negative_response(self, sid, start_timeout, end_timeout, response_records):
        self.mock_client.transport_interface.receive_message.side_effect = response_records
        assert Client._receive_response(self.mock_client,
                                        sid=sid,
                                        start_timeout=start_timeout,
                                        end_timeout=end_timeout) == response_records[-1]
        self.mock_client.transport_interface.receive_message.assert_called()



    # _send_tester_present_task

    def test_send_tester_present_task__send_2_then_wait(self):
        mock_tp = Mock()
        mock_is_set = Mock(return_value=False)
        mock_wait = Mock(side_effect=[False, True])
        self.mock_client._Client__tester_present_stop_event = Mock(spec=Event, is_set=mock_is_set, wait=mock_wait)
        assert Client.__send_tester_present_task(self.mock_client, tester_present_request=mock_tp) is None
        self.mock_client.transport_interface.send_message.assert_has_calls([call(mock_tp), call(mock_tp)])
        assert mock_is_set.call_count == 2
        assert mock_wait.call_count == 2

    def test_send_tester_present_task__stopped(self):
        mock_tp = Mock()
        mock_is_set = Mock(return_value=True)
        mock_wait = Mock()
        self.mock_client._Client__tester_present_stop_event = Mock(spec=Event, is_set=mock_is_set, wait=mock_wait)
        assert Client.__send_tester_present_task(self.mock_client, tester_present_request=mock_tp) is None
        self.mock_client.transport_interface.send_message.assert_not_called()
        mock_is_set.assert_called_once_with()
        mock_wait.assert_not_called()

    # is_response_pending_message

    @pytest.mark.parametrize("message, sid", [
        (Mock(), Mock())
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_response_pending_message__type_error(self, mock_isinstance, message, sid):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.is_response_pending_message(response_message=message, request_sid=sid)
        mock_isinstance.assert_called_once_with(message, (UdsMessage, UdsMessageRecord))

    @pytest.mark.parametrize("message, sid", [
        (Mock(spec=UdsMessageRecord, payload=b"\x7F\x13\x78"), 0x13),
        (Mock(spec=UdsMessageRecord, payload=(ResponseSID.NegativeResponse,
                                              RequestSID.ReadDTCInformation,
                                              NRC.RequestCorrectlyReceived_ResponsePending)),
         RequestSID.ReadDTCInformation),
    ])
    def test_is_response_pending_message__true(self, message, sid):
        self.mock_validate_request_sid.return_value = sid
        assert Client.is_response_pending_message(response_message=message, request_sid=sid) is True
        self.mock_validate_request_sid.assert_called_once_with(sid)

    @pytest.mark.parametrize("message, sid", [
        (Mock(spec=UdsMessageRecord, payload=b"\x7F\x13\x78"), 0x10),
        (Mock(spec=UdsMessageRecord, payload=b"\x7F\x10\x78\x78"), 0x10),
        (Mock(spec=UdsMessageRecord, payload=(RequestSID.ReadDTCInformation,
                                              RequestSID.ReadDTCInformation,
                                              NRC.RequestCorrectlyReceived_ResponsePending)),
         RequestSID.ReadDTCInformation),
    ])
    def test_is_response_pending_message__false(self, message, sid):
        self.mock_validate_request_sid.return_value = sid
        assert Client.is_response_pending_message(response_message=message, request_sid=sid) is False
        self.mock_validate_request_sid.assert_called_once_with(sid)

    # get_response

    @pytest.mark.parametrize("timeout", [Mock(), "not a timeout"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_response__type_error(self, mock_isinstance, timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client.get_response(self.mock_client, timeout=timeout)
        mock_isinstance.assert_called_once_with(timeout, (int, float))

    @pytest.mark.parametrize("timeout", [0, -0.043])
    def test_get_response__value_error(self, timeout):
        with pytest.raises(ValueError):
            Client.get_response(self.mock_client, timeout=timeout)

    @pytest.mark.parametrize("timeout", [1, 453.231])
    def test_get_response__empty(self, timeout):
        self.mock_client._Client__response_queue.get.side_effect = Empty
        assert Client.get_response(self.mock_client, timeout=timeout) is None
        self.mock_client._Client__response_queue.get.assert_called_once_with(timeout=None if timeout is None else timeout/1000.)

    @pytest.mark.parametrize("timeout", [None, 1])
    def test_get_response__response(self, timeout):
        assert (Client.get_response(self.mock_client, timeout=timeout)
                == self.mock_client._Client__response_queue.get.return_value)
        self.mock_client._Client__response_queue.get.assert_called_once_with(timeout=None if timeout is None else timeout/1000.)

    # get_response_no_wait

    def test_get_response_no_wait__empty(self):
        self.mock_client._Client__response_queue.get_nowait.side_effect = Empty
        assert Client.get_response_no_wait(self.mock_client) is None
        self.mock_client._Client__response_queue.get_nowait.assert_called_once_with()

    def test_get_response_no_wait__response(self):
        assert (Client.get_response_no_wait(self.mock_client)
                == self.mock_client._Client__response_queue.get_nowait.return_value)
        self.mock_client._Client__response_queue.get_nowait.assert_called_once_with()

    # clear_response_queue

    @pytest.mark.parametrize("queue_size", [0, 31])
    def test_clear_response_queue(self, queue_size):
        self.mock_client._Client__response_queue.qsize = Mock(return_value=queue_size)
        assert Client.clear_response_queue(self.mock_client) is None
        assert self.mock_client._Client__response_queue.get_nowait.call_count == queue_size

    # start_receiving

    @pytest.mark.parametrize("cycle", [Mock(), 234])
    def test_start_receiving__not_running(self, cycle):
        self.mock_client.is_background_receiving = False
        assert Client.start_background_receiving(self.mock_client, cycle=cycle) is None
        assert self.mock_client._Client__receiving_thread == self.mock_thread.return_value
        self.mock_thread.return_value.start.assert_called_once_with()
        self.mock_client._Client__receiving_stop_event.clear.assert_called_once_with()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("cycle", [Mock(), 234])
    def test_start_receiving__running(self, cycle):
        self.mock_client.is_background_receiving = True
        assert Client.start_background_receiving(self.mock_client, cycle=cycle) is None
        self.mock_thread.return_value.start.assert_not_called()
        self.mock_warn.assert_called_once()

    # stop_receiving

    def test_stop_receiving__running(self):
        self.mock_client.is_background_receiving = True
        mock_thread = Mock(spec=Thread)
        self.mock_client._Client__receiving_thread = mock_thread
        assert Client.stop_background_receiving(self.mock_client) is None
        assert self.mock_client._Client__receiving_thread is None
        self.mock_client._Client__receiving_stop_event.set.assert_called_once_with()
        mock_thread.join.assert_called_once_with()
        self.mock_warn.assert_not_called()

    def test_stop_receiving__not_running(self):
        self.mock_client.is_background_receiving = False
        assert Client.stop_background_receiving(self.mock_client) is None
        self.mock_warn.assert_called_once()

    # start_tester_present

    @pytest.mark.parametrize("addressing_type, sprmib", [
        (AddressingType.FUNCTIONAL, True),
        (AddressingType.PHYSICAL, False),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessage")
    def test_start_tester_present__start(self, mock_uds_message, addressing_type, sprmib):
        mock_event = Mock(spec=Event)
        self.mock_client.is_tester_present_sent = False
        self.mock_client._Client__tester_present_stop_event = mock_event
        self.mock_client._Client__tester_present_thread = None
        assert Client.start_tester_present(self.mock_client,
                                           addressing_type=addressing_type,
                                           sprmib=sprmib) is None
        assert self.mock_client._Client__tester_present_thread == self.mock_thread.return_value
        mock_event.clear.assert_called_once_with()
        self.mock_tester_present.encode_request.assert_called_once_with({
            "SubFunction": {
                "suppressPosRspMsgIndicationBit": sprmib,
                "zeroSubFunction": 0}
        })
        mock_uds_message.assert_called_once_with(payload=self.mock_tester_present.encode_request.return_value,
                                                 addressing_type=addressing_type)
        self.mock_thread.assert_called_once_with(target=self.mock_client._send_tester_present_task,
                                                 args=(mock_uds_message.return_value,),
                                                 daemon=True)
        self.mock_warn.assert_not_called()

    def test_start_tester_present__started(self):
        self.mock_client.is_tester_present_sent = True
        assert Client.start_tester_present(self.mock_client) is None
        self.mock_warn.assert_called_once()

    # stop_tester_present

    def test_stop_tester_present__stop(self):
        mock_thread = Mock(spec=Thread)
        mock_event = Mock(spec=Event)
        self.mock_client.is_tester_present_sent = True
        self.mock_client._Client__tester_present_thread = mock_thread
        self.mock_client._Client__tester_present_stop_event = mock_event
        assert Client.stop_tester_present(self.mock_client) is None
        assert self.mock_client._Client__tester_present_thread is None
        mock_event.set.assert_called_once_with()
        mock_thread.join.assert_called_once()
        self.mock_warn.assert_not_called()

    def test_stop_tester_present__stopped(self):
        self.mock_client.is_tester_present_sent = False
        assert Client.stop_tester_present(self.mock_client) is None
        self.mock_warn.assert_called_once()

    # send_request_receive_responses

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_send_request_receive_responses__type_error(self, mock_isinstance):
        mock_isinstance.return_value = False
        mock_request = Mock()
        with pytest.raises(TypeError):
            Client.send_request_receive_responses(self.mock_client, mock_request)
        mock_isinstance.assert_called_once_with(mock_request, UdsMessage)

    @pytest.mark.parametrize("request_message", [
        Mock(spec=UdsMessage, payload=b"\x10\x83"),
        Mock(spec=UdsMessage, payload=b"\x3E\x80"),
    ])
    def test_send_request_receive_responses__no_response(self, request_message):
        self.mock_client._receive_response.return_value = None
        self.mock_client.transport_interface.send_message.return_value = MagicMock(spec=UdsMessageRecord,
                                                                                   payload=request_message.payload)
        assert (Client.send_request_receive_responses(self.mock_client, request=request_message)
                == (self.mock_client.transport_interface.send_message.return_value, tuple()))
        self.mock_client._Client__receiving_not_in_progress.wait.assert_called_once()
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        self.mock_client._receive_response.assert_called_once()
        self.mock_client._update_measured_client_values.assert_not_called()

    @pytest.mark.parametrize("request_message", [
        Mock(spec=UdsMessage, payload=b"\x10\x83"),
        Mock(spec=UdsMessage, payload=b"\x3E\x80"),
    ])
    def test_send_request_receive_responses__timeout_error__p6(self, request_message):
        self.mock_client.transport_interface.send_message.return_value = MagicMock(spec=UdsMessageRecord,
                                                                                   payload=request_message.payload)
        self.mock_client._receive_response.side_effect = TimeoutError
        with pytest.raises(TimeoutError):
            Client.send_request_receive_responses(self.mock_client,
                                                  request=request_message)
        self.mock_client._Client__receiving_not_in_progress.wait.assert_called_once()
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        self.mock_client._receive_response.assert_called_once()

    @pytest.mark.parametrize("request_message, response_messages", [
        (
                Mock(spec=UdsMessage, payload=b"\x10\x03"),
                [Mock(spec=UdsMessageRecord, payload=b"\x7F\x10\x78"),
                 None],
        ),
        (
                Mock(spec=UdsMessage, payload=b"\x22\x12\x34"),
                [Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x78"),
                 Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x78"),
                 None],
        ),
    ])
    def test_send_request_receive_responses__timeout_error__p2_ext(self, request_message, response_messages):
        self.mock_client.transport_interface.send_message.return_value = MagicMock(spec=UdsMessageRecord,
                                                                                   payload=request_message.payload)
        self.mock_client._receive_response.side_effect = response_messages
        with pytest.raises(TimeoutError):
            Client.send_request_receive_responses(self.mock_client,
                                                  request=request_message)
        self.mock_client._Client__receiving_not_in_progress.wait.assert_called_once()
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        assert self.mock_client._receive_response.call_count == len(response_messages)

    @pytest.mark.parametrize("request_message, response_messages", [
        (
                Mock(spec=UdsMessage, payload=b"\x10\x03"),
                [Mock(spec=UdsMessageRecord, payload=b"\x7F\x10\x78"),
                 TimeoutError],
        ),
        (
                Mock(spec=UdsMessage, payload=b"\x22\x12\x34"),
                [Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x78"),
                 Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x78"),
                 TimeoutError],
        ),
    ])
    def test_send_request_receive_responses__timeout_error__p6_ext(self, request_message, response_messages):
        self.mock_client.transport_interface.send_message.return_value = MagicMock(spec=UdsMessageRecord,
                                                                                   payload=request_message.payload)
        self.mock_client._receive_response.side_effect = response_messages
        with pytest.raises(TimeoutError):
            Client.send_request_receive_responses(self.mock_client,
                                                  request=request_message)
        self.mock_client._Client__receiving_not_in_progress.wait.assert_called_once()
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        assert self.mock_client._receive_response.call_count == len(response_messages)

    @pytest.mark.parametrize("request_message, response_message", [
        (Mock(spec=UdsMessage, payload=b"\x10\x03"), Mock(payload=b"\x50\x03\x12\x34\x56\x78")),
        (Mock(spec=UdsMessage, payload=b"\x3E\x00"), Mock(payload=b"\x7E\x00")),
    ])
    def test_send_request_receive_responses__direct_response(self, request_message, response_message):
        request_record = MagicMock(spec=UdsMessageRecord, payload=request_message.payload)
        response_records = (response_message,)
        self.mock_client._receive_response.return_value = response_message
        self.mock_client.transport_interface.send_message.return_value = request_record
        self.mock_client.is_response_pending_message.return_value = False
        assert (Client.send_request_receive_responses(self.mock_client, request=request_message)
                == (request_record, response_records))
        self.mock_client._Client__receiving_not_in_progress.wait.assert_called_once()
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        self.mock_client._receive_response.assert_called_once()
        self.mock_client.is_response_pending_message.assert_called_once_with(
            message=response_message, request_sid=RequestSID(request_message.payload[0]))
        self.mock_client._update_measured_client_values.assert_called_once_with(
            request_record=request_record, response_records=list(response_records))

    @pytest.mark.parametrize("request_message, response_messages", [
        (Mock(spec=UdsMessage, payload=b"\x22\x12\x34"),
         (Mock(spec=UdsMessageRecord, payload=b"\x7F\x22\x78"),
          Mock(spec=UdsMessageRecord, payload=b"\x62\x12\x34\x00\xFF\x55\xAA"))),
        (Mock(spec=UdsMessage, payload=b"\x2E\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\xF0"),
         (Mock(spec=UdsMessageRecord, payload=b"\x7F\x2E\x78"),
          Mock(spec=UdsMessageRecord, payload=b"\x7F\x2E\x78"),
          Mock(spec=UdsMessageRecord, payload=b"\x7F\x2E\x78"),
          Mock(spec=UdsMessageRecord, payload=b"\x6E\xF0\xE1"))),
    ])
    def test_send_request_receive_responses__delayed_response(self, request_message, response_messages):
        request_record = MagicMock(spec=UdsMessageRecord, payload=request_message.payload)
        response_records = tuple([Mock(spec=UdsMessageRecord, payload=response_message.payload)
                                  for response_message in response_messages])
        self.mock_client._receive_response.side_effect = response_records
        self.mock_client.transport_interface.send_message.return_value = request_record
        self.mock_client.is_response_pending_message.side_effect \
            = lambda message, request_sid: message.payload != response_messages[-1].payload
        assert (Client.send_request_receive_responses(self.mock_client, request=request_message)
                == (request_record, response_records))
        self.mock_client._Client__receiving_not_in_progress.wait.assert_called_once()
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        assert self.mock_client._receive_response.call_count == len(response_records)
        self.mock_client._update_measured_client_values.assert_called_once_with(
            request_record=request_record, response_records=list(response_records))


@pytest.mark.performance
class TestClientPerformance:
    """Performance tests for `Client` class."""

    REPETITIONS = 100

    def setup_method(self):
        self.mock_client = MagicMock(spec=Client,
                                     _Client__response_queue=Queue())
        # patching
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_warn.stop()

    # _receive_response

    @pytest.mark.parametrize("start_timeout, end_timeout", [
        (10, 2000),
        (75, 75),
    ])
    def test_receive_response__start_timeout(self,
                                             performance_tolerance_ms, mean_performance_tolerance_ms,
                                             start_timeout, end_timeout):
        def _get_message(*_, **__):
            sleep(0.005)
            return MagicMock(payload=[MagicMock(__eq__=Mock(return_value=False))])

        self.mock_client.transport_interface.receive_message.side_effect = _get_message

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            assert Client._receive_response(self.mock_client,
                                            sid=MagicMock(),
                                            start_timeout=start_timeout,
                                            end_timeout=end_timeout) is None
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (start_timeout
                    <= execution_time_ms
                    <= start_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (start_timeout
                <= mean_execution_time_ms
                <= start_timeout + mean_performance_tolerance_ms)

    @pytest.mark.parametrize("start_timeout, end_timeout", [
        (2000, 10),
        (50, 50),
    ])
    def test_receive_response__end_timeout(self,
                                             performance_tolerance_ms, mean_performance_tolerance_ms,
                                             start_timeout, end_timeout):
        def _get_message(*_, **__):
            sleep(0.005)
            return MagicMock(payload=[MagicMock(__eq__=Mock(return_value=False))])

        self.mock_client.transport_interface.receive_message.side_effect = _get_message

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            assert Client._receive_response(self.mock_client,
                                            sid=MagicMock(),
                                            start_timeout=start_timeout,
                                            end_timeout=end_timeout) is None
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (end_timeout
                    <= execution_time_ms
                    <= end_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (end_timeout
                <= mean_execution_time_ms
                <= end_timeout + mean_performance_tolerance_ms)


@pytest.mark.integration
class TestClientIntegration:
    """Integration tests for `Client` class."""

    @pytest.mark.parametrize("kwargs, attributes", [
        (
            {
                "transport_interface": Mock(spec=AbstractTransportInterface)
            },
            {
                "p2_client_timeout": Client.DEFAULT_P2_CLIENT_TIMEOUT,
                "p2_client_measured": None,
                "p2_ext_client_timeout": Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT,
                "p2_ext_client_measured": None,
                "p6_client_timeout": Client.DEFAULT_P6_CLIENT_TIMEOUT,
                "p6_client_measured": None,
                "p6_ext_client_timeout": Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT,
                "p6_ext_client_measured": None,
                "s3_client": Client.DEFAULT_S3_CLIENT,
            }
        ),
        (
            {
                "transport_interface": Mock(spec=AbstractTransportInterface),
                "p2_client_timeout": 20,
                "p2_ext_client_timeout": 2000,
                "p6_client_timeout": 25,
                "p6_ext_client_timeout": 10000,
                "s3_client": 1500,
            },
            {
                "p2_client_timeout": 20,
                "p2_client_measured": None,
                "p2_ext_client_timeout": 2000,
                "p2_ext_client_measured": None,
                "p6_client_timeout": 25,
                "p6_client_measured": None,
                "p6_ext_client_timeout": 10000,
                "p6_ext_client_measured": None,
                "s3_client": 1500,
            }
        ),
    ])
    def test_init(self, kwargs, attributes):
        client = Client(**kwargs)
        for attr_name, attr_value in attributes.items():
            assert getattr(client, attr_name) == attr_value

    @pytest.mark.parametrize("kwargs", [
        {
            "transport_interface": Mock(spec=AbstractTransportInterface),
            "p2_client_timeout": 100,
            "p6_client_timeout": 95,
        },
        {
            "transport_interface": Mock(spec=AbstractTransportInterface),
            "p2_ext_client_timeout": 5000,
            "p6_ext_client_timeout": 4000,
        },
    ])
    def test_init__value_error(self, kwargs):
        with pytest.raises(ValueError):
            Client(**kwargs)

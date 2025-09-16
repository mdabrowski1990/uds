from datetime import datetime
from time import perf_counter, sleep

import pytest
from mock import MagicMock, Mock, call, patch

from uds.addressing import AddressingType
from uds.client import (
    NRC,
    AbstractTransportInterface,
    Client,
    Event,
    InconsistencyError,
    MessageTransmissionNotStartedError,
    ReassignmentError,
    RequestSID,
    ResponseSID,
    Thread,
    UdsMessage,
    UdsMessageRecord,
)

SCRIPT_LOCATION = "uds.client"


class TestClient:
    """Unit tests for `Client` class."""

    def setup_method(self):
        self.mock_client = MagicMock(spec=Client)
        # patching
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_time = patch(f"{SCRIPT_LOCATION}.time")
        self.mock_time = self._patcher_time.start()
        self._patcher_thread = patch(f"{SCRIPT_LOCATION}.Thread")
        self.mock_thread = self._patcher_thread.start()
        self._patcher_event = patch(f"{SCRIPT_LOCATION}.Event")
        self.mock_event = self._patcher_event.start()
        self._patcher_tester_present = patch(f"{SCRIPT_LOCATION}.TESTER_PRESENT")
        self.mock_tester_present = self._patcher_tester_present.start()
        self._patcher_validate_request_sid = patch(f"{SCRIPT_LOCATION}.RequestSID.validate_member")
        self.mock_validate_request_sid = self._patcher_validate_request_sid.start()

    def teardown_method(self):
        self._patcher_warn.stop()
        self._patcher_perf_counter.stop()
        self._patcher_time.stop()
        self._patcher_thread.stop()
        self._patcher_event.stop()
        self._patcher_tester_present.stop()
        self._patcher_validate_request_sid.stop()

    # __init__

    @pytest.mark.parametrize("transport_interface", [Mock(), "Some transport interface"])
    def test_init__mandatory_args(self, transport_interface):
        assert Client.__init__(self.mock_client,
                               transport_interface=transport_interface) is None
        assert self.mock_client.transport_interface == transport_interface
        assert self.mock_client.p2_client_timeout == Client.DEFAULT_P2_CLIENT_TIMEOUT
        assert self.mock_client.p2_ext_client_timeout == Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        assert self.mock_client.p6_client_timeout == Client.DEFAULT_P6_CLIENT_TIMEOUT
        assert self.mock_client.p6_ext_client_timeout == Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT
        assert self.mock_client.s3_client == Client.DEFAULT_S3_CLIENT
        assert self.mock_client._Client__p2_client_measured is None
        assert self.mock_client._Client__p2_ext_client_measured is None
        assert self.mock_client._Client__p6_client_measured is None
        assert self.mock_client._Client__p6_ext_client_measured is None
        assert self.mock_client._Client__tester_present_thread is None
        assert self.mock_client._Client__tester_present_stop_event == self.mock_event.return_value

    @pytest.mark.parametrize("transport_interface, p2_client_timeout, p2_ext_client_timeout, p6_client_timeout, "
                             "p6_ext_client_timeout, s3_client", [
        (Mock(), Mock(), Mock(), Mock(), Mock(),  Mock()),
        ("TI", "P2Client", "P2*Client", "P6Client", "P6*Client", "S3Client"),
    ])
    def test_init__all_args(self, transport_interface, p2_client_timeout, p2_ext_client_timeout, p6_client_timeout,
                            p6_ext_client_timeout, s3_client):
        assert Client.__init__(self.mock_client,
                               transport_interface=transport_interface,
                               p2_client_timeout=p2_client_timeout,
                               p2_ext_client_timeout=p2_ext_client_timeout,
                               p6_client_timeout=p6_client_timeout,
                               p6_ext_client_timeout=p6_ext_client_timeout,
                               s3_client=s3_client) is None
        assert self.mock_client.transport_interface == transport_interface
        assert self.mock_client.p2_client_timeout == p2_client_timeout
        assert self.mock_client.p2_ext_client_timeout == p2_ext_client_timeout
        assert self.mock_client.p6_client_timeout == p6_client_timeout
        assert self.mock_client.p6_ext_client_timeout == p6_ext_client_timeout
        assert self.mock_client.s3_client == s3_client
        assert self.mock_client._Client__p2_client_measured is None
        assert self.mock_client._Client__p2_ext_client_measured is None
        assert self.mock_client._Client__p6_client_measured is None
        assert self.mock_client._Client__p6_ext_client_measured is None
        assert self.mock_client._Client__tester_present_thread is None
        assert self.mock_client._Client__tester_present_stop_event == self.mock_event.return_value

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
    def test_p2_client_timeout__set__valid(self, p2_client_timeout):
        assert Client.p2_client_timeout.fset(self.mock_client, p2_client_timeout) is None
        assert self.mock_client._Client__p2_client_timeout == p2_client_timeout

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
    def test_p2_ext_client_timeout__set__valid(self, p2_ext_client_timeout):
        assert Client.p2_ext_client_timeout.fset(self.mock_client, p2_ext_client_timeout) is None
        assert self.mock_client._Client__p2_ext_client_timeout == p2_ext_client_timeout

    # p2_ext_client_measured

    def test_p2_ext_client_measured__get(self):
        self.mock_client._Client__p2_ext_client_measured = Mock()
        assert Client.p2_ext_client_measured.fget(self.mock_client) == self.mock_client._Client__p2_ext_client_measured

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
    def test_p6_client_timeout__set__valid(self, p6_client_timeout, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client.p6_client_timeout.fset(self.mock_client, p6_client_timeout) is None
        assert self.mock_client._Client__p6_client_timeout == p6_client_timeout

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

    @pytest.mark.parametrize("s3_client, p2_client_timeout", [
        (Client.DEFAULT_P2_CLIENT_TIMEOUT, Client.DEFAULT_P2_CLIENT_TIMEOUT + 0.1),
        (100, 101),
    ])
    def test_s3_client__set__inconsistent(self, s3_client, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        with pytest.raises(InconsistencyError):
            Client.s3_client.fset(self.mock_client, s3_client)

    @pytest.mark.parametrize("s3_client, p2_client_timeout", [
        (Client.DEFAULT_P2_CLIENT_TIMEOUT, Client.DEFAULT_P2_CLIENT_TIMEOUT),
        (500, 100),
    ])
    def test_s3_client__set__valid(self, s3_client, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client.s3_client.fset(self.mock_client, s3_client) is None
        assert self.mock_client._Client__s3_client == s3_client

    # _update_p2_client_measured

    @pytest.mark.parametrize("p2_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p2_client_measured__type_error(self, mock_isinstance, p2_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._update_p2_client_measured(self.mock_client, p2_client)
        mock_isinstance.assert_called_once_with(p2_client, (int, float))

    @pytest.mark.parametrize("p2_client", [0, -0.01])
    def test_update_p2_client_measured__value_error(self, p2_client):
        with pytest.raises(ValueError):
            Client._update_p2_client_measured(self.mock_client, p2_client)

    @pytest.mark.parametrize("p2_client_measured, p2_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p2_client_measured__valid__with_warning(self, p2_client_measured, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client._update_p2_client_measured(self.mock_client, p2_client_measured) is None
        assert self.mock_client._Client__p2_client_measured == p2_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_client_measured, p2_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p2_client_measured__valid__without_warning(self, p2_client_measured, p2_client_timeout):
        self.mock_client.p2_client_timeout = p2_client_timeout
        assert Client._update_p2_client_measured(self.mock_client, p2_client_measured) is None
        assert self.mock_client._Client__p2_client_measured == p2_client_measured
        self.mock_warn.assert_not_called()

    # _update_p2_ext_client_measured

    def test_update_p2_ext_client_measured__runtime_error(self):
        with pytest.raises(RuntimeError):
            Client._update_p2_ext_client_measured(self.mock_client)

    @pytest.mark.parametrize("p2_ext_client_measured_list", [
        [Mock()],
        [Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT, "Some time", Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT],
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p2_ext_client_measured__type_error(self, mock_isinstance, p2_ext_client_measured_list):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list)
        mock_isinstance.assert_called_with(p2_ext_client_measured_list[0], (int, float))

    @pytest.mark.parametrize("p2_ext_client_measured_list", [
        [0],
        [Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT, -0.01, Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT],
    ])
    def test_update_p2_ext_client_measured__value_error(self, p2_ext_client_measured_list):
        self.mock_client.p2_ext_client_timeout = Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        with pytest.raises(ValueError):
            Client._update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list)

    @pytest.mark.parametrize("p2_ext_client_measured_list, p2_ext_client_timeout", [
        ([1.001], 1),
        ([100, 100.1, 25, 0.25], 100),
    ])
    def test_update_p2_ext_client_measured__valid__with_warning(self, p2_ext_client_measured_list,
                                                                p2_ext_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        assert Client._update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list) is None
        assert self.mock_client._Client__p2_ext_client_measured == tuple(p2_ext_client_measured_list)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_ext_client_measured_list, p2_ext_client_timeout", [
        ([1], 1),
        ([0.00001, 22.75, 99.9999, 100], 100),
    ])
    def test_update_p2_ext_client_measured__valid__without_warning(self, p2_ext_client_measured_list,
                                                                   p2_ext_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        assert Client._update_p2_ext_client_measured(self.mock_client, *p2_ext_client_measured_list) is None
        assert self.mock_client._Client__p2_ext_client_measured == tuple(p2_ext_client_measured_list)
        self.mock_warn.assert_not_called()
        
    # _update_p6_client_measured

    @pytest.mark.parametrize("p6_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p6_client_measured__type_error(self, mock_isinstance, p6_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._update_p6_client_measured(self.mock_client, p6_client)
        mock_isinstance.assert_called_once_with(p6_client, (int, float))

    @pytest.mark.parametrize("p6_client", [0, -0.01])
    def test_update_p6_client_measured__value_error(self, p6_client):
        with pytest.raises(ValueError):
            Client._update_p6_client_measured(self.mock_client, p6_client)

    @pytest.mark.parametrize("p6_client_measured, p6_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p6_client_measured__valid__with_warning(self, p6_client_measured, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client._update_p6_client_measured(self.mock_client, p6_client_measured) is None
        assert self.mock_client._Client__p6_client_measured == p6_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p6_client_measured, p6_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p6_client_measured__valid__without_warning(self, p6_client_measured, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client._update_p6_client_measured(self.mock_client, p6_client_measured) is None
        assert self.mock_client._Client__p6_client_measured == p6_client_measured
        self.mock_warn.assert_not_called()
        
    # _update_p6_ext_client_measured

    @pytest.mark.parametrize("p6_ext_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p6_ext_client_measured__type_error(self, mock_isinstance, p6_ext_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._update_p6_ext_client_measured(self.mock_client, p6_ext_client)
        mock_isinstance.assert_called_once_with(p6_ext_client, (int, float))

    @pytest.mark.parametrize("p6_ext_client", [0, -0.01])
    def test_update_p6_ext_client_measured__value_error(self, p6_ext_client):
        with pytest.raises(ValueError):
            Client._update_p6_ext_client_measured(self.mock_client, p6_ext_client)

    @pytest.mark.parametrize("p6_ext_client_measured, p6_ext_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p6_ext_client_measured__valid__with_warning(self, p6_ext_client_measured, p6_ext_client_timeout):
        self.mock_client.p6_ext_client_timeout = p6_ext_client_timeout
        assert Client._update_p6_ext_client_measured(self.mock_client, p6_ext_client_measured) is None
        assert self.mock_client._Client__p6_ext_client_measured == p6_ext_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p6_ext_client_measured, p6_ext_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p6_ext_client_measured__valid__without_warning(self, p6_ext_client_measured, p6_ext_client_timeout):
        self.mock_client.p6_ext_client_timeout = p6_ext_client_timeout
        assert Client._update_p6_ext_client_measured(self.mock_client, p6_ext_client_measured) is None
        assert self.mock_client._Client__p6_ext_client_measured == p6_ext_client_measured
        self.mock_warn.assert_not_called()

    # _update_measured_client_values

    @pytest.mark.parametrize("request_message, response_messages, p2_client, p6_client", [
        (Mock(spec=UdsMessageRecord,
              transmission_start=datetime(2020, 1, 1, 12, 0, 0),
              transmission_end=datetime(2020, 1, 1, 12, 0, 0, 500)),
         (Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2020, 1, 1, 12, 0, 0, 14000),
               transmission_end=datetime(2020, 1, 1, 12, 0, 0, 15500)), ),
         13.5,
         15),
        (Mock(spec=UdsMessageRecord,
              transmission_start=datetime(2025, 8, 24, 19, 21, 17, 917304),
              transmission_end=datetime(2025, 8, 24, 19, 21, 17, 919054)),
         (Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2025, 8, 24, 19, 21, 18, 17804),
               transmission_end=datetime(2025, 8, 24, 19, 21, 18, 19054)),),
         98.75,
         100),
    ])
    def test_update_measured_client_values__direct_response(self, request_message, response_messages,
                                                            p2_client, p6_client):
        assert Client._update_measured_client_values(self.mock_client,
                                                     request_record=request_message,
                                                     response_records=response_messages) is None
        self.mock_client._update_p2_client_measured.assert_called_once_with(p2_client)
        self.mock_client._update_p6_client_measured.assert_called_once_with(p6_client)
        self.mock_client._update_p2_ext_client_measured.assert_not_called()
        self.mock_client._update_p6_ext_client_measured.assert_not_called()

    @pytest.mark.parametrize("request_message, response_messages, p2_client, p2_ext_client, p6_ext_client", [
        (Mock(spec=UdsMessageRecord,
              transmission_start=datetime(2020, 1, 1, 12, 0, 0),
              transmission_end=datetime(2020, 1, 1, 12, 0, 0, 500)),
         (Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2020, 1, 1, 12, 0, 0, 14000),
               transmission_end=datetime(2020, 1, 1, 12, 0, 0, 15500)),
          Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2020, 1, 1, 12, 0, 0, 514000),
               transmission_end=datetime(2020, 1, 1, 12, 0, 0, 989000))),
         13.5,
         [973.5],
         988.5),
        (Mock(spec=UdsMessageRecord,
              transmission_start=datetime(2025, 8, 24, 19, 21, 17, 917304),
              transmission_end=datetime(2025, 8, 24, 19, 21, 17, 919054)),
         (Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2025, 8, 24, 19, 21, 18, 17804),
               transmission_end=datetime(2025, 8, 24, 19, 21, 18, 19054)),
          Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2025, 8, 24, 19, 21, 18, 698454),
               transmission_end=datetime(2025, 8, 24, 19, 21, 18, 701304)),
          Mock(spec=UdsMessageRecord,
               transmission_start=datetime(2025, 8, 24, 19, 21, 19, 17804),
               transmission_end=datetime(2025, 8, 24, 19, 21, 19, 19054))),
         98.75,
         [682.25, 317.75],
         1100),
    ])
    def test_update_measured_client_values__delayed_response(self, request_message, response_messages,
                                                             p2_client, p2_ext_client, p6_ext_client):
        assert Client._update_measured_client_values(self.mock_client,
                                                     request_record=request_message,
                                                     response_records=response_messages) is None
        self.mock_client._update_p2_client_measured.assert_called_once_with(p2_client)
        self.mock_client._update_p2_ext_client_measured.assert_called_once_with(*p2_ext_client)
        self.mock_client._update_p6_ext_client_measured.assert_called_once_with(p6_ext_client)
        self.mock_client._update_p6_client_measured.assert_not_called()

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
            MagicMock(__gt__=Mock(return_value=True),
                      __sub__=lambda this, other: this),
            MagicMock(__gt__=Mock(return_value=False),
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
    def test_receive_response__no_response(self, sid, start_timeout, end_timeout, response_record):
        self.mock_client.transport_interface.receive_message.return_value = response_record
        assert Client._receive_response(self.mock_client,
                                        sid=sid,
                                        start_timeout=start_timeout,
                                        end_timeout=end_timeout) is None

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
            [Mock(spec=UdsMessageRecord, payload=b"\x62\x12\x34\x56\x78\x9A\xBC\xDC\xEF\x0F")]
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

    # _send_tester_present

    def test_send_tester_present__send_2_then_wait(self):
        mock_tp = Mock()
        mock_is_set = Mock(return_value=False)
        mock_wait = Mock(side_effect=[False, True])
        self.mock_client._Client__tester_present_stop_event = Mock(spec=Event, is_set=mock_is_set, wait=mock_wait)
        assert Client._send_tester_present(self.mock_client, tester_present_message=mock_tp) is None
        self.mock_client.transport_interface.send_message.assert_has_calls([call(mock_tp), call(mock_tp)])
        assert mock_is_set.call_count == 2
        assert mock_wait.call_count == 2

    def test_send_tester_present__stopped(self):
        mock_tp = Mock()
        mock_is_set = Mock(return_value=True)
        mock_wait = Mock()
        self.mock_client._Client__tester_present_stop_event = Mock(spec=Event, is_set=mock_is_set, wait=mock_wait)
        assert Client._send_tester_present(self.mock_client, tester_present_message=mock_tp) is None
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
            Client.is_response_pending_message(message=message, request_sid=sid)
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
        assert Client.is_response_pending_message(message=message, request_sid=sid) is True
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
        assert Client.is_response_pending_message(message=message, request_sid=sid) is False
        self.mock_validate_request_sid.assert_called_once_with(sid)

    # start_tester_present

    @pytest.mark.parametrize("addressing_type, sprmib", [
        (AddressingType.FUNCTIONAL, True),
        (AddressingType.PHYSICAL, False),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessage")
    def test_start_tester_present__start(self, mock_uds_message, addressing_type, sprmib):
        mock_event = Mock(spec=Event)
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
        self.mock_thread.assert_called_once_with(target=self.mock_client._send_tester_present,
                                                 args=(mock_uds_message.return_value,),
                                                 daemon=True)
        self.mock_warn.assert_not_called()

    def test_start_tester_present__started(self):
        self.mock_client._Client__tester_present_thread = Mock(spec=Thread)
        assert Client.start_tester_present(self.mock_client) is None
        self.mock_warn.assert_called_once()

    # stop_tester_present

    def test_stop_tester_present__stop(self):
        mock_thread = Mock(spec=Thread)
        mock_event =  Mock(spec=Event)
        self.mock_client._Client__tester_present_thread = mock_thread
        self.mock_client._Client__tester_present_stop_event = mock_event
        assert Client.stop_tester_present(self.mock_client) is None
        assert self.mock_client._Client__tester_present_thread is None
        mock_event.set.assert_called_once_with()
        mock_thread.join.assert_called_once()
        self.mock_warn.assert_not_called()

    def test_stop_tester_present__stopped(self):
        self.mock_client._Client__tester_present_thread = None
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
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        assert self.mock_client._receive_response.call_count == len(response_messages)

    @pytest.mark.parametrize("request_message, response_message", [
        (Mock(spec=UdsMessage, payload=b"\x10\x03"), Mock(payload=b"\x50\x03\x12\x34\x56\x78")),
        (Mock(spec=UdsMessage, payload=b"\x3E\x00"), Mock(payload=b"\x7E\x00")),
    ])
    def test_send_request_receive_responses__direct_response(self, request_message, response_message):
        request_record = MagicMock(spec=UdsMessageRecord, payload=request_message.payload)
        response_records = (response_message, )
        self.mock_client._receive_response.return_value = response_message
        self.mock_client.transport_interface.send_message.return_value = request_record
        self.mock_client.is_response_pending_message.return_value = False
        assert (Client.send_request_receive_responses(self.mock_client, request=request_message)
                == (request_record, response_records))
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
        self.mock_client.transport_interface.send_message.assert_called_once_with(request_message)
        assert self.mock_client._receive_response.call_count == len(response_records)
        self.mock_client._update_measured_client_values.assert_called_once_with(
            request_record=request_record, response_records=list(response_records))
            
    # get_response
    
    def test_get_response(self):
        with pytest.raises(NotImplementedError):
            Client.get_response(self.mock_client)

    # get_response_no_wait
    
    def test_get_response_no_wait(self):
        with pytest.raises(NotImplementedError):
            Client.get_response_no_wait(self.mock_client)

    # clear_response_queue

    def test_clear_response_queue(self):
        with pytest.raises(NotImplementedError):
            Client.clear_response_queue(self.mock_client)


@pytest.mark.performance
class TestClientPerformance:
    """Performance tests for `Client` class."""

    REPETITIONS = 100

    def setup_method(self):
        self.mock_client = MagicMock(spec=Client)
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

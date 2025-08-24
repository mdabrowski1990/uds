from unittest.mock import MagicMock

import pytest
from mock import Mock, patch

from uds.client import AbstractTransportInterface, Client, InconsistencyError, ReassignmentError

SCRIPT_LOCATION = "uds.client"


class TestClient:
    """Unit tests for `Client` class."""

    def setup_method(self):
        self.mock_client = Mock(spec=Client)
        # patching
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_warn.stop()

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

    @pytest.mark.parametrize("s3_client, p6_client_timeout", [
        (Client.DEFAULT_P6_CLIENT_TIMEOUT, Client.DEFAULT_P6_CLIENT_TIMEOUT + 0.1),
        (100, 101),
    ])
    def test_s3_client__set__inconsistent(self, s3_client, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        with pytest.raises(InconsistencyError):
            Client.s3_client.fset(self.mock_client, s3_client)

    @pytest.mark.parametrize("s3_client, p6_client_timeout", [
        (Client.DEFAULT_S3_CLIENT, Client.DEFAULT_P6_CLIENT_TIMEOUT),
        (100, 100),
    ])
    def test_s3_client__set__valid(self, s3_client, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
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

    @pytest.mark.parametrize("p2_ext_client", [Mock(), "Some time"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_p2_ext_client_measured__type_error(self, mock_isinstance, p2_ext_client):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            Client._update_p2_ext_client_measured(self.mock_client, p2_ext_client)
        mock_isinstance.assert_called_once_with(p2_ext_client, (int, float))

    @pytest.mark.parametrize("p2_ext_client", [0, -0.01])
    def test_update_p2_ext_client_measured__value_error(self, p2_ext_client):
        with pytest.raises(ValueError):
            Client._update_p2_ext_client_measured(self.mock_client, p2_ext_client)

    @pytest.mark.parametrize("p2_ext_client_measured, p2_ext_client_timeout", [
        (1.001, 1),
        (100.1, 100),
    ])
    def test_update_p2_ext_client_measured__valid__with_warning(self, p2_ext_client_measured, p2_ext_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        assert Client._update_p2_ext_client_measured(self.mock_client, p2_ext_client_measured) is None
        assert self.mock_client._Client__p2_ext_client_measured == p2_ext_client_measured
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_ext_client_measured, p2_ext_client_timeout", [
        (0.001, 1),
        (100, 100),
    ])
    def test_update_p2_ext_client_measured__valid__without_warning(self, p2_ext_client_measured, p2_ext_client_timeout):
        self.mock_client.p2_ext_client_timeout = p2_ext_client_timeout
        assert Client._update_p2_ext_client_measured(self.mock_client, p2_ext_client_measured) is None
        assert self.mock_client._Client__p2_ext_client_measured == p2_ext_client_measured
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

    # _receive_response

    # TODO: tests

    # is_response_pending_message

    # TODO: tests

    # start_tester_present

    def test_start_tester_present(self):
        with pytest.raises(NotImplementedError):
            Client.start_tester_present(self.mock_client)

    # stop_tester_present

    def test_stop_tester_present(self):
        with pytest.raises(NotImplementedError):
            Client.stop_tester_present(self.mock_client)
            
    # send_request_receive_responses

    # TODO: tests
            
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

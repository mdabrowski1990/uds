from unittest.mock import MagicMock

import pytest
from mock import Mock, patch

from uds.client import AbstractTransportInterface, Client, InconsistencyError, ReassignmentError

SCRIPT_LOCATION = "uds.client"


class TestClient:

    def setup_method(self):
        self.mock_client = Mock(spec=Client)

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
        assert self.mock_client.p3_client_physical == Client.DEFAULT_P3_CLIENT
        assert self.mock_client.p3_client_functional == Client.DEFAULT_P3_CLIENT
        assert self.mock_client.s3_client == Client.DEFAULT_S3_CLIENT
        assert self.mock_client._Client__p2_client_measured is None
        assert self.mock_client._Client__p2_ext_client_measured is None
        assert self.mock_client._Client__p6_client_measured is None
        assert self.mock_client._Client__p6_ext_client_measured is None

    @pytest.mark.parametrize("transport_interface, p2_client_timeout, p2_ext_client_timeout, p6_client_timeout, "
                             "p6_ext_client_timeout, p3_client_physical, p3_client_functional, s3_client", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
        ("TI", "P2Client", "P2*Client", "P6Client", "P6*Client", "P3Client_phys", "P3Client_func", "S3Client"),
    ])
    def test_init__all_args(self, transport_interface, p2_client_timeout, p2_ext_client_timeout, p6_client_timeout,
                            p6_ext_client_timeout, p3_client_physical, p3_client_functional, s3_client):
        assert Client.__init__(self.mock_client,
                               transport_interface=transport_interface,
                               p2_client_timeout=p2_client_timeout,
                               p2_ext_client_timeout=p2_ext_client_timeout,
                               p6_client_timeout=p6_client_timeout,
                               p6_ext_client_timeout=p6_ext_client_timeout,
                               p3_client_physical=p3_client_physical,
                               p3_client_functional=p3_client_functional,
                               s3_client=s3_client) is None
        assert self.mock_client.transport_interface == transport_interface
        assert self.mock_client.p2_client_timeout == p2_client_timeout
        assert self.mock_client.p2_ext_client_timeout == p2_ext_client_timeout
        assert self.mock_client.p6_client_timeout == p6_client_timeout
        assert self.mock_client.p6_ext_client_timeout == p6_ext_client_timeout
        assert self.mock_client.p3_client_physical == p3_client_physical
        assert self.mock_client.p3_client_functional == p3_client_functional
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

    @pytest.mark.parametrize("p3_client_physical, p6_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT + 0.1),
        (100, 101),
    ])
    def test_p3_client_physical__set__inconsistent(self, p3_client_physical, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        with pytest.raises(InconsistencyError):
            Client.p3_client_physical.fset(self.mock_client, p3_client_physical)

    @pytest.mark.parametrize("p3_client_physical, p6_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT),
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P6_CLIENT_TIMEOUT),
    ])
    def test_p3_client_physical__set__valid(self, p3_client_physical, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client.p3_client_physical.fset(self.mock_client, p3_client_physical) is None
        assert self.mock_client._Client__p3_client_physical == p3_client_physical

    # p3_client_functional

    def test_p3_p3_client_functional__get(self):
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

    @pytest.mark.parametrize("p3_client_functional, p6_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT + 0.1),
        (100, 101),
    ])
    def test_p3_client_functional__set__inconsistent(self, p3_client_functional, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        with pytest.raises(InconsistencyError):
            Client.p3_client_functional.fset(self.mock_client, p3_client_functional)

    @pytest.mark.parametrize("p3_client_functional, p6_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT),
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P6_CLIENT_TIMEOUT),
    ])
    def test_p3_client_functional__set__valid(self, p3_client_functional, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client.p3_client_functional.fset(self.mock_client, p3_client_functional) is None
        assert self.mock_client._Client__p3_client_functional == p3_client_functional

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
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT + 0.1),
        (100, 101),
    ])
    def test_s3_client__set__inconsistent(self, s3_client, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        with pytest.raises(InconsistencyError):
            Client.s3_client.fset(self.mock_client, s3_client)

    @pytest.mark.parametrize("s3_client, p6_client_timeout", [
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P3_CLIENT),
        (Client.DEFAULT_P3_CLIENT, Client.DEFAULT_P6_CLIENT_TIMEOUT),
    ])
    def test_s3_client__set__valid(self, s3_client, p6_client_timeout):
        self.mock_client.p6_client_timeout = p6_client_timeout
        assert Client.s3_client.fset(self.mock_client, s3_client) is None
        assert self.mock_client._Client__s3_client == s3_client
        
    # start_tester_present

    def test_start_tester_present(self):
        with pytest.raises(NotImplementedError):
            Client.start_tester_present(self.mock_client)

    # stop_tester_present

    def test_stop_tester_present(self):
        with pytest.raises(NotImplementedError):
            Client.stop_tester_present(self.mock_client)
            
    # send_request_receive_responses

    def test_send_request_receive_responses(self):
        with pytest.raises(NotImplementedError):
            Client.send_request_receive_responses(self.mock_client, Mock())
            
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

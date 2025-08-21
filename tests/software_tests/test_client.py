import pytest
from mock import Mock

from uds.client import Client


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
        with pytest.raises(NotImplementedError):
            Client.transport_interface.fget(self.mock_client)

    # p2_client_timeout

    def test_p2_client_timeout__get(self):
        with pytest.raises(NotImplementedError):
            Client.p2_client_timeout.fget(self.mock_client)
            
    def test_p2_client_timeout__set(self):
        with pytest.raises(NotImplementedError):
            Client.p2_client_timeout.fset(self.mock_client, Mock())

    # p2_client_measured

    def test_p2_client_measured__get(self):
        with pytest.raises(NotImplementedError):
            Client.p2_client_measured.fget(self.mock_client)

    # p6_client_timeout

    def test_p6_client_timeout__get(self):
        with pytest.raises(NotImplementedError):
            Client.p6_client_timeout.fget(self.mock_client)

    def test_p6_client_timeout__set(self):
        with pytest.raises(NotImplementedError):
            Client.p6_client_timeout.fset(self.mock_client, Mock())
            
    # p6_client_measured

    def test_p6_client_measured__get(self):
        with pytest.raises(NotImplementedError):
            Client.p6_client_measured.fget(self.mock_client)

    # p2_ext_client_timeout

    def test_p2_ext_client_timeout__get(self):
        with pytest.raises(NotImplementedError):
            Client.p2_ext_client_timeout.fget(self.mock_client)

    def test_p2_ext_client_timeout__set(self):
        with pytest.raises(NotImplementedError):
            Client.p2_ext_client_timeout.fset(self.mock_client, Mock())

    # p2_ext_client_measured

    def test_p2_ext_client_measured__get(self):
        with pytest.raises(NotImplementedError):
            Client.p2_ext_client_measured.fget(self.mock_client)

    # p6_ext_client_timeout

    def test_p6_ext_client_timeout__get(self):
        with pytest.raises(NotImplementedError):
            Client.p6_ext_client_timeout.fget(self.mock_client)

    def test_p6_ext_client_timeout__set(self):
        with pytest.raises(NotImplementedError):
            Client.p6_ext_client_timeout.fset(self.mock_client, Mock())

    # p6_ext_client_measured

    def test_p6_ext_client_measured__get(self):
        with pytest.raises(NotImplementedError):
            Client.p6_ext_client_measured.fget(self.mock_client)
            
    # p3_client_physical

    def test_p3_client_physical__get(self):
        with pytest.raises(NotImplementedError):
            Client.p3_client_physical.fget(self.mock_client)

    def test_p3_client_physical__set(self):
        with pytest.raises(NotImplementedError):
            Client.p3_client_physical.fset(self.mock_client, Mock())

    # p3_client_functional

    def test_p3_p3_client_functional__get(self):
        with pytest.raises(NotImplementedError):
            Client.p3_client_functional.fget(self.mock_client)

    def test_p3_p3_client_functional__set(self):
        with pytest.raises(NotImplementedError):
            Client.p3_client_functional.fset(self.mock_client, Mock())

    # s3_client

    def test_s3_client__get(self):
        with pytest.raises(NotImplementedError):
            Client.s3_client.fget(self.mock_client)

    def test_s3_client__set(self):
        with pytest.raises(NotImplementedError):
            Client.s3_client.fset(self.mock_client, Mock())

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

import pytest
from mock import Mock

from uds.client import Client


class TestClient:

    def setup_method(self):
        self.mock_client = Mock(spec=Client)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            Client.__init__(self.mock_client, Mock())

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

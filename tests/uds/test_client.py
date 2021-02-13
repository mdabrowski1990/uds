import pytest
from mock import Mock

from uds import Client


class TestClient:
    """Test for Client class."""

    def setup(self):
        self.mock_client__tp_interface = Mock()
        self.mock_client = Mock(spec=Client, _Client__tp_interface=self.mock_client__tp_interface)

    @pytest.mark.parametrize("tp_interface", ["any", 1])
    def test_init(self, tp_interface):
        Client.__init__(self=self.mock_client, tp_interface=tp_interface)
        assert self.mock_client._Client__tp_interface == tp_interface

    @pytest.mark.parametrize("uds_request", ["some request", [0x10, 0x01]])
    @pytest.mark.parametrize("addressing", ["physical", "functional", "broadcast"])
    def test_send_request(self, uds_request, addressing):
        assert Client.send_request(self=self.mock_client, request=uds_request, addressing=addressing) is None
        self.mock_client__tp_interface.send_request.assert_called_once_with(request=uds_request, addressing=addressing)

    @pytest.mark.parametrize("last_request", [None, "some request"])
    def test_get_last_sent_request(self, last_request):
        self.mock_client__tp_interface.get_last_sent_message = Mock(return_value=last_request)
        assert Client.get_last_sent_request(self.mock_client) == last_request
        self.mock_client__tp_interface.get_last_sent_message.assert_called_once_with()

    @pytest.mark.parametrize("response_messages", [[], ["response 1", "response 2"]])
    def test_get_response_messages(self, response_messages):
        self.mock_client__tp_interface.get_response_messages = Mock(return_value=response_messages)
        assert Client.get_response_messages(self=self.mock_client) == response_messages
        self.mock_client__tp_interface.get_response_messages.assert_called_once_with()

    @pytest.mark.parametrize("addressing", ["physical", "functional", "broadcast"])
    @pytest.mark.parametrize("suppress_response", [True, False])
    def test_start_tester_present(self, addressing, suppress_response):
        assert Client.start_tester_present(self=self.mock_client, addressing=addressing,
                                           suppress_response=suppress_response) is None
        self.mock_client__tp_interface.start_tester_present.assert_called_once_with(
            addressing=addressing, suppress_response=suppress_response)

    def test_stop_tester_present(self):
        assert Client.stop_tester_present(self=self.mock_client) is None
        self.mock_client__tp_interface.stop_tester_present.assert_called_once_with()

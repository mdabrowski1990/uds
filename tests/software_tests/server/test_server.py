import pytest
from mock import Mock, patch

from uds.transport_interface import TransportInterfaceServer
from uds.server import ResponseManager
from uds.server.server import Server


class TestServer:
    """Tests for `Server` class."""

    def setup(self):
        self.mock_server = Mock(spec=Server)

    # __init __

    @pytest.mark.parametrize("transport_interface", ["transport interface", Mock(spec=TransportInterfaceServer)])
    @pytest.mark.parametrize("response_manager", ["response manager", Mock(spec=ResponseManager)])
    @pytest.mark.parametrize("p2_server, p2_server_max, p4_server", [
        (0, 50, 40),
        (50, 55, 200),
        (1, 100, None),
    ])
    @pytest.mark.parametrize("p2ext_server, p2ext_server_max", [
        (990, 1000),
        (459, 499)
    ])
    def test_init__valid(self, transport_interface, response_manager, p2_server, p2_server_max, p2ext_server,
                         p2ext_server_max, p4_server):
        Server.__init__(self=self.mock_server, transport_interface=transport_interface, response_manager=response_manager,
                        p2_server=p2_server, p2_server_max=p2_server_max, p2ext_server=p2ext_server,
                        p2ext_server_max=p2ext_server_max, p4_server=p4_server)
        assert self.mock_server._Server__transport_interface == transport_interface
        assert self.mock_server.response_manager == response_manager
        assert self.mock_server.p2_server == p2_server
        assert self.mock_server.p2_server_max == p2_server_max
        assert self.mock_server.p2ext_server == p2ext_server
        assert self.mock_server.p2ext_server_max == p2ext_server_max
        assert self.mock_server.p4_server == p4_server
        self.mock_server._Server__validate_transport_interface.assert_called_once_with(transport_interface=transport_interface)

    # __validate_transport_interface

    @pytest.mark.parametrize("transport_interface", [Mock(spec=TransportInterfaceServer)])
    def test_validate_transport_interface__valid(self, transport_interface):
        assert Server._Server__validate_transport_interface(transport_interface=transport_interface) is None

    @pytest.mark.parametrize("transport_interface", [None, 1, False, "no interface"])
    def test_validate_transport_interface__invalid_type(self, transport_interface):
        with pytest.raises(TypeError):
            Server._Server__validate_transport_interface(transport_interface=transport_interface)

    # response_manager

    @pytest.mark.parametrize("response_manager", [None, Mock(), "response_manager"])
    def test_response_manager__get(self, response_manager):
        self.mock_server._Server__response_manager = response_manager
        assert Server.response_manager.fget(self=self.mock_server) is response_manager

    @pytest.mark.parametrize("response_manager", [None, 1, False, "response manager"])
    def test_response_manager__set_invalid_type(self, response_manager):
        with pytest.raises(TypeError):
            Server.response_manager.fset(self=self.mock_server, value=response_manager)

    @pytest.mark.parametrize("response_manager", [
        Mock(spec=ResponseManager),
        ResponseManager(response_rules=[], server_states=[])
    ])
    def test_response_manager__set_valid(self, response_manager):
        Server.response_manager.fset(self=self.mock_server, value=response_manager)
        assert self.mock_server._Server__response_manager == response_manager

    # p2_server

    @pytest.mark.parametrize("p2_server", [None, Mock(), "p2_server", 0, 5.4])
    def test_p2_server__get(self, p2_server):
        self.mock_server._Server__p2_server = p2_server
        assert Server.p2_server.fget(self=self.mock_server) is p2_server

    @pytest.mark.parametrize("p2_server", [None, "p2_server", {}])
    def test_p2_server__set_invalid_type(self, p2_server):
        with pytest.raises(TypeError):
            Server.p2_server.fset(self=self.mock_server, value=p2_server)

    @pytest.mark.parametrize("p2_server_min, p2_server, p2_server_max", [
        [10, 9, 11],
        [10, 9.99, 11],
        [10, 11.01, 11],
        [10, 12, 11],
        [0, -1, 50],
        [0, -0.01, 50],
        [0, 50.01, 50],
        [0, 51, 50],
    ])
    def test_p2_server__set_invalid_value(self, p2_server_min, p2_server, p2_server_max):
        self.mock_server.p2_server_max = p2_server_max
        self.mock_server._Server__P2_SERVER_MIN = p2_server_min
        with pytest.raises(ValueError):
            Server.p2_server.fset(self=self.mock_server, value=p2_server)

    @pytest.mark.parametrize("p2_server_min, p2_server, p2_server_max", [
        [10, 10, 11],
        [10, 11, 11],
        [10, 10.5, 11],
        [10, 10., 11],
        [10, 11., 11],
        [0, 0, 50],
        [0, 50, 50],
        [0, 50., 50],
        [0, 0., 50],
        [0, 32.2312, 50],
    ])
    def test_p2_server__set_valid(self, p2_server_min, p2_server, p2_server_max):
        self.mock_server.p2_server_max = p2_server_max
        self.mock_server._Server__P2_SERVER_MIN = p2_server_min
        Server.p2_server.fset(self=self.mock_server, value=p2_server)
        assert self.mock_server._Server__p2_server == p2_server

    # p2_server_max

    @pytest.mark.parametrize("p2_server_max", [None, Mock(), "p2_server", 0, 5.4])
    def test_p2_server_max__get(self, p2_server_max):
        self.mock_server._Server__p2_server_max = p2_server_max
        assert Server.p2_server_max.fget(self=self.mock_server) is p2_server_max

    @pytest.mark.parametrize("p2_server_max", [None, "p2_server_max", {}])
    def test_p2_server_max__set_invalid_type(self, p2_server_max):
        with pytest.raises(TypeError):
            Server.p2_server_max.fset(self=self.mock_server, value=p2_server_max)

    @pytest.mark.parametrize("p2_server_min, p2_server_max", [
        [10, 10],
        [10, 10.],
        [0, 0],
        [0, 0.],
        [0, -0.00001],
        [0, -1],
        [321, 321],
        [321, 320.99999],
        [321, 10]
    ])
    def test_p2_server_max__set_invalid_value(self, p2_server_min, p2_server_max):
        self.mock_server._Server__P2_SERVER_MIN = p2_server_min
        with pytest.raises(ValueError):
            Server.p2_server_max.fset(self=self.mock_server, value=p2_server_max)

    @pytest.mark.parametrize("p2_server_min, p2_server_max", [
        [10, 11],
        [10, 10.01],
        [0, 1],
        [0, 0.01],
        [0, 100],
        [321, 500],
        [321, 321.431]
    ])
    def test_p2_server_max__set_valid(self, p2_server_min, p2_server_max):
        self.mock_server._Server__P2_SERVER_MIN = p2_server_min
        Server.p2_server_max.fset(self=self.mock_server, value=p2_server_max)
        assert self.mock_server._Server__p2_server_max == p2_server_max

    # p2ext_server

    @pytest.mark.parametrize("p2ext_server", [None, Mock(), "p2ext_server", 0, 5.4])
    def test_p2ext_server__get(self, p2ext_server):
        self.mock_server._Server__p2ext_server = p2ext_server
        assert Server.p2ext_server.fget(self=self.mock_server) is p2ext_server

    @pytest.mark.parametrize("p2ext_server", [None, "p2ext_server", {}])
    def test_p2ext_server__set_invalid_type(self, p2ext_server):
        with pytest.raises(TypeError):
            Server.p2ext_server.fset(self=self.mock_server, value=p2ext_server)

    @pytest.mark.parametrize("p2ext_server_min, p2ext_server, p2ext_server_max", [
        [10, 9, 11],
        [10, 9.99, 11],
        [10, 11.01, 11],
        [10, 12, 11],
        [0, -1, 50],
        [0, -0.01, 50],
        [0, 50.01, 50],
        [0, 51, 50],
    ])
    def test_p2ext_server__set_invalid_value(self, p2ext_server_min, p2ext_server, p2ext_server_max):
        self.mock_server.p2ext_server_max = p2ext_server_max
        self.mock_server._Server__P2EXT_SERVER_MIN = p2ext_server_min
        with pytest.raises(ValueError):
            Server.p2ext_server.fset(self=self.mock_server, value=p2ext_server)

    @pytest.mark.parametrize("p2ext_server_min, p2ext_server, p2ext_server_max", [
        [10, 10, 11],
        [10, 11, 11],
        [10, 10.5, 11],
        [10, 10., 11],
        [10, 11., 11],
        [0, 0, 50],
        [0, 50, 50],
        [0, 50., 50],
        [0, 0., 50],
        [0, 32.2312, 50],
    ])
    def test_p2ext_server__set_valid(self, p2ext_server_min, p2ext_server, p2ext_server_max):
        self.mock_server.p2ext_server_max = p2ext_server_max
        self.mock_server._Server__P2EXT_SERVER_MIN = p2ext_server_min
        Server.p2ext_server.fset(self=self.mock_server, value=p2ext_server)
        assert self.mock_server._Server__p2ext_server == p2ext_server

    # p2ext_server_max

    @pytest.mark.parametrize("p2ext_server_max", [None, Mock(), "p2ext_server_max", 0, 5.4])
    def test_p2ext_server_max__get(self, p2ext_server_max):
        self.mock_server._Server__p2ext_server_max = p2ext_server_max
        assert Server.p2ext_server_max.fget(self=self.mock_server) is p2ext_server_max

    @pytest.mark.parametrize("p2ext_server_max", [None, "p2ext_server_max", {}])
    def test_p2ext_server_max__set_invalid_type(self, p2ext_server_max):
        with pytest.raises(TypeError):
            Server.p2ext_server_max.fset(self=self.mock_server, value=p2ext_server_max)

    @pytest.mark.parametrize("p2ext_server_min, p2ext_server_max", [
        [10, 10],
        [10, 10.],
        [0, 0],
        [0, 0.],
        [0, -0.00001],
        [0, -1],
        [321, 321],
        [321, 320.99999],
        [321, 10]
    ])
    def test_p2ext_server_max__set_invalid_value(self, p2ext_server_min, p2ext_server_max):
        self.mock_server._Server__P2EXT_SERVER_MIN = p2ext_server_min
        with pytest.raises(ValueError):
            Server.p2ext_server_max.fset(self=self.mock_server, value=p2ext_server_max)

    @pytest.mark.parametrize("p2ext_server_min, p2ext_server_max", [
        [10, 11],
        [10, 10.01],
        [0, 1],
        [0, 0.01],
        [0, 100],
        [321, 500],
        [321, 321.431]
    ])
    def test_p2ext_server_max__set_valid(self, p2ext_server_min, p2ext_server_max):
        self.mock_server._Server__P2EXT_SERVER_MIN = p2ext_server_min
        Server.p2ext_server_max.fset(self=self.mock_server, value=p2ext_server_max)
        assert self.mock_server._Server__p2ext_server_max == p2ext_server_max

    # p4_server

    @pytest.mark.parametrize("p4_server", [Mock(), "p4_server", 0, 5.4])
    def test_p4_server__get(self, p4_server):
        self.mock_server._Server__p4_server = p4_server
        assert Server.p4_server.fget(self=self.mock_server) is p4_server

    @pytest.mark.parametrize("p2_server", [Mock(), "p4_server", 0, 5.4])
    def test_p4_server__get_when_none(self, p2_server):
        self.mock_server._Server__p4_server = None
        self.mock_server.p2_server = p2_server
        assert Server.p4_server.fget(self=self.mock_server) is p2_server

    @pytest.mark.parametrize("p4_server", ["p4_server", {}])
    def test_p4_server__set_invalid_type(self, p4_server):
        with pytest.raises(TypeError):
            Server.p4_server.fset(self=self.mock_server, value=p4_server)

    @pytest.mark.parametrize("p4_server_min, p4_server", [
        [10, 9],
        [10, 9.99],
        [10, 0],
        [92, 91],
        [92, 91.99],
        [92, 65],
        [92, -1],
    ])
    def test_p4_server__set_invalid_value(self, p4_server_min, p4_server):
        self.mock_server.p4_server_min = p4_server_min
        with pytest.raises(ValueError):
            Server.p4_server.fset(self=self.mock_server, value=p4_server)

    @pytest.mark.parametrize("p4_server_min, p4_server", [
        [10, 10],
        [10, 10.],
        [10, 10.01],
        [10, 65],
        [92, 92],
        [92, 92.01],
        [92, 4586],
        [92, None],
        [10, None],
    ])
    def test_p4_server__set_valid(self, p4_server_min, p4_server):
        self.mock_server.p4_server_min = p4_server_min
        Server.p4_server.fset(self=self.mock_server, value=p4_server)
        assert self.mock_server._Server__p4_server == p4_server

    # p4_server

    @pytest.mark.parametrize("p2_server", [0, 43.2, 35])
    def test_p4_server_min(self, p2_server):
        self.mock_server.p2_server = p2_server
        assert Server.p4_server_min.fget(self=self.mock_server) == p2_server

# TODO: integration tests for Server.__init__ to make sure values are set in proper order

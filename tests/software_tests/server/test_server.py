import pytest
from mock import Mock, patch

from uds.server.server import Server, ServerSimulationError, ResponseManager, TransportInterfaceServer, UdsResponse, \
    AddressingType, UdsRequest


class TestServer:
    """Tests for `Server` class."""

    SOURCE_SCRIPT_LOCATION = "uds.server.server"

    def setup(self):
        def timedelta_side_effect(milliseconds):
            return milliseconds

        self.mock_server = Mock(spec=Server)
        # patching
        self._patcher_warn = patch(f"{self.SOURCE_SCRIPT_LOCATION}.warn")
        self._patcher_datetime = patch(f"{self.SOURCE_SCRIPT_LOCATION}.datetime")
        self._patcher_timedelta = patch(f"{self.SOURCE_SCRIPT_LOCATION}.timedelta")
        self.mock_warn = self._patcher_warn.start()
        self.mock_datetime = self._patcher_datetime.start()
        self.mock_timedelta = self._patcher_timedelta.start()
        self.mock_timedelta.side_effect = timedelta_side_effect

    def teardown(self):
        self._patcher_warn.stop()
        self._patcher_datetime.stop()
        self._patcher_timedelta.stop()

    # __init __

    @pytest.mark.parametrize("transport_interface", ["transport interface", Mock(spec=TransportInterfaceServer)])
    @pytest.mark.parametrize("response_manager", ["response manager", Mock(spec=ResponseManager)])
    @pytest.mark.parametrize("p2_server, p2_server_max, p4_server, p4_server_max", [
        (0, 50, 40, 6000),
        (50, 55, 200, 1000),
        (1, 100, None, 100),
    ])
    @pytest.mark.parametrize("p2ext_server, p2ext_server_max", [
        (990, 1000),
        (459, 499)
    ])
    def test_init__valid(self, transport_interface, response_manager, p2_server, p2_server_max, p2ext_server,
                         p2ext_server_max, p4_server, p4_server_max):
        Server.__init__(self=self.mock_server, transport_interface=transport_interface, response_manager=response_manager,
                        p2_server=p2_server, p2_server_max=p2_server_max, p2ext_server=p2ext_server,
                        p2ext_server_max=p2ext_server_max, p4_server=p4_server, p4_server_max=p4_server_max)
        assert self.mock_server._Server__transport_interface == transport_interface
        assert self.mock_server.response_manager == response_manager
        assert self.mock_server.p2_server == p2_server
        assert self.mock_server.p2_server_max == p2_server_max
        assert self.mock_server.p2ext_server == p2ext_server
        assert self.mock_server.p2ext_server_max == p2ext_server_max
        assert self.mock_server.p4_server == p4_server
        assert self.mock_server.p4_server_max == p4_server_max
        self.mock_server._Server__validate_transport_interface.assert_called_once_with(transport_interface=transport_interface)

    # transport_interface

    @pytest.mark.parametrize("transport_interface", [Mock(spec=TransportInterfaceServer)])
    def test_validate_transport_interface__valid(self, transport_interface):
        assert Server._Server__validate_transport_interface(transport_interface=transport_interface) is None

    @pytest.mark.parametrize("transport_interface", [None, 1, False, "no interface"])
    def test_validate_transport_interface__invalid_type(self, transport_interface):
        with pytest.raises(TypeError):
            Server._Server__validate_transport_interface(transport_interface=transport_interface)

    @pytest.mark.parametrize("transport_interface", [None, Mock(), "transport_interface"])
    def test_transport_interface__get(self, transport_interface):
        self.mock_server._Server__transport_interface = transport_interface
        assert Server.transport_interface.fget(self=self.mock_server) == transport_interface

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

    # p2_server_min

    @pytest.mark.parametrize("p2_server_min", [None, Mock(), "p2_server_min", 0, 5.4])
    def test_p2_server_min__get(self, p2_server_min):
        self.mock_server._Server__P2_SERVER_MIN = p2_server_min
        assert Server.p2_server_min.fget(self=self.mock_server) is p2_server_min

    # p2_server_max

    @pytest.mark.parametrize("p2_server_max", [None, Mock(), "p2_server_max", 0, 5.4])
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
        self.mock_server.p2_server_min = p2_server_min
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
        self.mock_server.p2_server_min = p2_server_min
        self.mock_server.p2_server = p2_server_min
        self.mock_server.p2_server_max = p2_server_max
        Server.p2_server_max.fset(self=self.mock_server, value=p2_server_max)
        assert self.mock_server._Server__p2_server_max == p2_server_max

    @pytest.mark.parametrize("p2_server, p2_server_max", [
        (50, 49),
        (50, 49.9),
        (100, 99),
        (100, 99.0),
        (100, 50)
    ])
    def test_p2_server_max__set_lower_than_p2_server(self, p2_server, p2_server_max):
        self.mock_server.p2_server_min = 0
        self.mock_server.p2_server = p2_server
        self.mock_server.p2_server_max = p2_server_max
        Server.p2_server_max.fset(self=self.mock_server, value=p2_server_max)
        assert self.mock_server.p2_server == p2_server_max
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_server, p2_server_max", [
        (50, 50),
        (50, 50.),
        (50, 51),
        (100, 100),
        (100, 100.1),
        (100, 143.5)
    ])
    def test_p2_server_max__set_greater_equal_than_p2_server(self, p2_server, p2_server_max):
        self.mock_server.p2_server_min = 0
        self.mock_server.p2_server = p2_server
        self.mock_server.p2_server_max = p2_server_max
        Server.p2_server_max.fset(self=self.mock_server, value=p2_server_max)
        assert self.mock_server.p2_server == p2_server
        self.mock_warn.assert_not_called()

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
        [10, 10, 11],
        [10, 9.99, 11],
        [10, 10., 11],
        [10, 11.01, 11],
        [10, 12, 11],
        [0, 0, 50],
        [0, -0.01, 50],
        [0, 50.01, 50],
        [0, 51, 50],
    ])
    def test_p2_server__set_invalid_value(self, p2_server_min, p2_server, p2_server_max):
        self.mock_server.p2_server_max = p2_server_max
        self.mock_server.p2_server_min = p2_server_min
        with pytest.raises(ValueError):
            Server.p2_server.fset(self=self.mock_server, value=p2_server)

    @pytest.mark.parametrize("p2_server_min, p2_server, p2_server_max", [
        [10, 11, 11],
        [10, 10.5, 11],
        [10, 10.1, 11],
        [10, 11., 11],
        [0, 1, 50],
        [0, 50, 50],
        [0, 50., 50],
        [0, 0.1, 50],
        [0, 32.2312, 50],
    ])
    def test_p2_server__set_valid(self, p2_server_min, p2_server, p2_server_max):
        self.mock_server.p2_server_max = p2_server_max
        self.mock_server.p2_server_min = p2_server_min
        self.mock_server.p4_server = float("inf")
        self.mock_server.p4_server_min = p2_server
        Server.p2_server.fset(self=self.mock_server, value=p2_server)
        assert self.mock_server._Server__p2_server == p2_server

    @pytest.mark.parametrize("p2_server, p4_server", [
        (50, 30),
        (31, 30),
        (30.1, 30),
        (49.6, 49.5),
        (50, 49.5),
    ])
    def test_p2_server__set_greater_than_p4_server(self, p2_server, p4_server):
        self.mock_server.p2_server_min = p2_server-1
        self.mock_server.p2_server_max = p2_server+1
        self.mock_server.p4_server = p4_server
        self.mock_server.p4_server_min = p2_server
        Server.p2_server.fset(self=self.mock_server, value=p2_server)
        assert self.mock_server.p4_server is None
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2_server, p4_server", [
        (30, 30),
        (30., 30),
        (29.9, 30),
        (29, 30),
        (49.5, 49.5),
        (49, 49.5),
    ])
    def test_p2_server__set_less_equal_than_p4_server(self, p2_server, p4_server):
        self.mock_server.p2_server_min = p2_server-1
        self.mock_server.p2_server_max = p2_server+1
        self.mock_server.p4_server = p4_server
        self.mock_server.p4_server_min = p2_server
        Server.p2_server.fset(self=self.mock_server, value=p2_server)
        assert self.mock_server.p4_server == p4_server
        self.mock_warn.assert_not_called()

    # p2ext_server_min

    @pytest.mark.parametrize("p2ext_server_min", [None, Mock(), "p2ext_server_min", 0, 5.4])
    def test_p2ext_server_min__get(self, p2ext_server_min):
        self.mock_server._Server__P2EXT_SERVER_MIN = p2ext_server_min
        assert Server.p2ext_server_min.fget(self=self.mock_server) is p2ext_server_min

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
        self.mock_server.p2ext_server_min = p2ext_server_min
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
        self.mock_server.p2ext_server_min = p2ext_server_min
        self.mock_server.p2ext_server = p2ext_server_min
        self.mock_server.p2ext_server_max = p2ext_server_max
        Server.p2ext_server_max.fset(self=self.mock_server, value=p2ext_server_max)
        assert self.mock_server._Server__p2ext_server_max == p2ext_server_max

    @pytest.mark.parametrize("p2ext_server, p2ext_server_max", [
        (50, 49),
        (50, 49.9),
        (100, 99),
        (100, 99.0),
        (100, 50)
    ])
    def test_p2ext_server_max__set_lower_than_p2ext_server(self, p2ext_server, p2ext_server_max):
        self.mock_server.p2ext_server_min = 0
        self.mock_server.p2ext_server = p2ext_server
        self.mock_server.p2ext_server_max = p2ext_server_max
        Server.p2ext_server_max.fset(self=self.mock_server, value=p2ext_server_max)
        assert self.mock_server.p2ext_server == p2ext_server_max
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p2ext_server, p2ext_server_max", [
        (50, 50),
        (50, 50.),
        (50, 51),
        (100, 100),
        (100, 100.1),
        (100, 143.5)
    ])
    def test_p2ext_server_max__set_greater_equal_than_p2ext_server(self, p2ext_server, p2ext_server_max):
        self.mock_server.p2ext_server_min = 0
        self.mock_server.p2ext_server = p2ext_server
        self.mock_server.p2ext_server_max = p2ext_server_max
        Server.p2ext_server_max.fset(self=self.mock_server, value=p2ext_server_max)
        assert self.mock_server.p2ext_server == p2ext_server
        self.mock_warn.assert_not_called()

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
        [10, 10, 11],
        [10, 9.99, 11],
        [10, 10., 11],
        [10, 11.01, 11],
        [10, 12, 11],
        [0, 0, 50],
        [0, -0.01, 50],
        [0, 50.01, 50],
        [0, 51, 50],
    ])
    def test_p2ext_server__set_invalid_value(self, p2ext_server_min, p2ext_server, p2ext_server_max):
        self.mock_server.p2ext_server_max = p2ext_server_max
        self.mock_server.p2ext_server_min = p2ext_server_min
        with pytest.raises(ValueError):
            Server.p2ext_server.fset(self=self.mock_server, value=p2ext_server)

    @pytest.mark.parametrize("p2ext_server_min, p2ext_server, p2ext_server_max", [
        [10, 11, 11],
        [10, 10.5, 11],
        [10, 10.1, 11],
        [10, 11., 11],
        [0, 1, 50],
        [0, 50, 50],
        [0, 50., 50],
        [0, 0.1, 50],
        [0, 32.2312, 50],
    ])
    def test_p2ext_server__set_valid(self, p2ext_server_min, p2ext_server, p2ext_server_max):
        self.mock_server.p2ext_server_max = p2ext_server_max
        self.mock_server.p2ext_server_min = p2ext_server_min
        Server.p2ext_server.fset(self=self.mock_server, value=p2ext_server)
        assert self.mock_server._Server__p2ext_server == p2ext_server

    # p4_server_min

    @pytest.mark.parametrize("p2_server", [0, 43.2, 35])
    def test_p4_server_min__get(self, p2_server):
        self.mock_server.p2_server = p2_server
        assert Server.p4_server_min.fget(self=self.mock_server) == p2_server

    # p4_server_max

    @pytest.mark.parametrize("p4_server_max", [Mock(), "p4_server_max", 0, 5.4])
    def test_p4_server_max__get(self, p4_server_max):
        self.mock_server._Server__p4_server_max = p4_server_max
        assert Server.p4_server_max.fget(self=self.mock_server) == p4_server_max

    @pytest.mark.parametrize("p2_server_max", [Mock(), 0, 5.4])
    def test_p4_server_max__get_when_none(self, p2_server_max):
        self.mock_server._Server__p4_server_max = None
        self.mock_server.p2_server_max = p2_server_max
        assert Server.p4_server_max.fget(self=self.mock_server) is p2_server_max

    @pytest.mark.parametrize("p4_server_max", ["p4_server_max", {}])
    def test_p4_server_max__set_invalid_type(self, p4_server_max):
        with pytest.raises(TypeError):
            Server.p4_server_max.fset(self=self.mock_server, value=p4_server_max)

    @pytest.mark.parametrize("p2_server_max, p4_server_max", [
        [10, 9],
        [10, 9.99],
        [10, 0],
        [92, 91],
        [92, 91.99],
        [92, 65],
        [92, -1],
    ])
    def test_p4_server_max__set_invalid_value(self, p2_server_max, p4_server_max):
        self.mock_server.p2_server_max = p2_server_max
        with pytest.raises(ValueError):
            Server.p4_server_max.fset(self=self.mock_server, value=p4_server_max)

    @pytest.mark.parametrize("p2_server_max, p4_server_max", [
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
    def test_p4_server_max__set_valid(self, p2_server_max, p4_server_max):
        self.mock_server.p2_server_max = p2_server_max
        self.mock_server.p4_server = 0
        self.mock_server.p4_server_max = 1
        Server.p4_server_max.fset(self=self.mock_server, value=p4_server_max)
        assert self.mock_server._Server__p4_server_max == p4_server_max

    @pytest.mark.parametrize("p4_server, p4_server_max", [
        (50, 49),
        (50, 49.9),
        (100, 99),
        (100, 99.0),
        (100, 50)
    ])
    def test_p4_server_max__set_lower_than_p4_server(self, p4_server, p4_server_max):
        self.mock_server.p4_server = p4_server
        self.mock_server.p2_server_max = 0
        self.mock_server.p4_server_max = p4_server_max
        Server.p4_server_max.fset(self=self.mock_server, value=p4_server_max)
        assert self.mock_server.p4_server == p4_server_max
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("p4_server, p4_server_max", [
        (50, 50),
        (50, 50.),
        (50, 51),
        (100, 100),
        (100, 100.1),
        (100, 143.5)
    ])
    def test_p4_server_max__set_greater_equal_than_p4_server(self, p4_server, p4_server_max):
        self.mock_server.p4_server = p4_server
        self.mock_server.p2_server_max = 0
        self.mock_server.p4_server_max = p4_server_max
        Server.p4_server_max.fset(self=self.mock_server, value=p4_server_max)
        assert self.mock_server.p4_server == p4_server
        self.mock_warn.assert_not_called()

    # p4_server

    @pytest.mark.parametrize("p4_server", [Mock(), "p4_server", 0, 5.4])
    def test_p4_server__get(self, p4_server):
        self.mock_server._Server__p4_server = p4_server
        assert Server.p4_server.fget(self=self.mock_server) is p4_server

    @pytest.mark.parametrize("p2_server", [Mock(), 0, 5.4])
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

    @pytest.mark.parametrize("p4_server_min, p4_server, p4_server_max", [
        [10, 10, 100],
        [10, 10., 50],
        [10, 10.01, 11.],
        [10, 65, 65],
        [92, 92, 100],
        [92, 92.01, 100],
        [92, 4586, 4586],
        [92, None, 100],
        [10, None, 50],
    ])
    def test_p4_server__set_valid(self, p4_server_min, p4_server, p4_server_max):
        self.mock_server.p4_server_min = p4_server_min
        self.mock_server.p4_server_max = p4_server_max
        Server.p4_server.fset(self=self.mock_server, value=p4_server)
        assert self.mock_server._Server__p4_server == p4_server

    # create_response_pending_message

    @pytest.mark.parametrize("request_sid", [0x10, 0x11, 0x22, 0x31, 0x85])
    @pytest.mark.parametrize("addressing", [None] + list(AddressingType))
    def test_create_response_pending_message(self, request_sid, addressing):
        message = Server.create_response_pending_message(request_sid=request_sid, addressing=addressing)
        assert isinstance(message, UdsResponse)
        assert len(message.raw_message) == 3
        assert message.raw_message[0] == 0x7F
        assert message.raw_message[1] == request_sid
        assert message.raw_message[2] == 0x78
        assert message.addressing == addressing

    # _create_response_plan

    def test_create_response_plan__no_response(self, example_uds_request):
        self.mock_server.response_manager.create_response = Mock(return_value=None)
        assert Server._create_response_plan(self=self.mock_server, request=example_uds_request) is None
        self.mock_server.response_manager.create_response.assert_called_once_with(request=example_uds_request)

    @pytest.mark.parametrize("p2_server", [10, 49.5, 50])
    def test_create_response_plan__single_response(self, p2_server, example_uds_request_raw_data):
        mock_time_transmission_end = Mock()
        mock_add = Mock()
        mock_time_transmission_end.__add__ = mock_add
        mock_uds_request = Mock(spec=UdsRequest, raw_message=example_uds_request_raw_data,
                                time_transmission_end=mock_time_transmission_end)
        self.mock_server.p4_server = self.mock_server.p2_server = p2_server
        response_timetable = Server._create_response_plan(self=self.mock_server, request=mock_uds_request)
        assert isinstance(response_timetable, list)
        assert len(response_timetable) == 1
        assert response_timetable[0] == \
               (self.mock_server.response_manager.create_response.return_value, mock_add.return_value)

    @pytest.mark.parametrize("p2_server, p2ext_server, p4_server, response_pending_number", [
        (50, 900, 51, 1),
        (50, 900, 950, 1),
        (50, 900, 951, 2),
        (100, 800, 1700, 2),
        (100, 800, 1701, 3),
    ])
    def test_create_response_plan__with_response_pending(self, p2_server, p2ext_server, p4_server, response_pending_number,
                                                         example_uds_request_raw_data, example_addressing_type):
        mock_uds_request = Mock(spec=UdsRequest, raw_message=example_uds_request_raw_data,
                                addressing=example_addressing_type, time_transmission_end=0)
        self.mock_server.p2_server = p2_server
        self.mock_server.p2ext_server = p2ext_server
        self.mock_server.p4_server = p4_server
        response_timetable = Server._create_response_plan(self=self.mock_server, request=mock_uds_request)
        assert isinstance(response_timetable, list)
        assert len(response_timetable) == response_pending_number + 1
        assert all([message == self.mock_server.create_response_pending_message.return_value
                    for message, planned_time in response_timetable[:response_pending_number]])
        assert response_timetable[-1][0] == self.mock_server.response_manager.create_response.return_value
        self.mock_server.create_response_pending_message.assert_called_once_with(
            request_sid=example_uds_request_raw_data[0], addressing=example_addressing_type)

    # _schedule_response

    @pytest.mark.parametrize("time_now, response_timetable", [
        (1, [(Mock(), 0)]),
        (0.1, [(Mock(), 0), (Mock(), 1)]),
        (100, [(Mock(), 99.9), (Mock(), 0)]),
        (100, [(Mock(), 99)])
    ])
    def test_schedule_response__time_exceeded(self, time_now, response_timetable):
        self.mock_datetime.now = Mock(return_value=time_now)
        with pytest.raises(ServerSimulationError):
            Server._schedule_response(self=self.mock_server, response_timetable=response_timetable)

    # @pytest.mark.parametrize("time_now, response_timetable", [
    # ])
    # def test_schedule_response__time_exceeded(self, time_now, response_timetable):
    #     self.mock_datetime.now = Mock(return_value=time_now)
    #     assert Server._schedule_response(self=self.mock_server, response_timetable=response_timetable) is None

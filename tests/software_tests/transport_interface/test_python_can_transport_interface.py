import pytest
from mock import Mock, patch

from uds.transport_interface.python_can_transport_interface import PyCanTransportInterface, \
    BusABC, AbstractTransportInterface
from uds.can import CanAddressingInformation, CanAddressingFormat


class TestPyCanTransportInterface:
    """Unit tests for `PyCanTransportInterface` class."""

    SCRIPT_LOCATION = "uds.transport_interface.python_can_transport_interface"

    def setup(self):
        self.mock_can_transport_interface = Mock(spec=PyCanTransportInterface)
        # patching
        self._patcher_abstract_can_ti_init = patch(f"{self.SCRIPT_LOCATION}.AbstractCanTransportInterface.__init__")
        self.mock_abstract_can_ti_init = self._patcher_abstract_can_ti_init.start()

    def teardown(self):
        self._patcher_abstract_can_ti_init.stop()

    # __init__

    @pytest.mark.parametrize("can_bus_manager, addressing_information", [
        ("can_bus_manager", "addressing_information"),
        (Mock(), Mock())
    ])
    def test_init__default_args(self, can_bus_manager, addressing_information):
        PyCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                         can_bus_manager=can_bus_manager,
                                         addressing_information=addressing_information)
        self.mock_abstract_can_ti_init.assert_called_once_with(
            can_bus_manager=can_bus_manager,
            addressing_information=addressing_information,
            packet_records_number=AbstractTransportInterface.DEFAULT_PACKET_RECORDS_NUMBER,
            message_records_number=AbstractTransportInterface.DEFAULT_MESSAGE_RECORDS_NUMBER)
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_cr_measured is None

    @pytest.mark.parametrize("can_bus_manager, addressing_information", [
        ("can_bus_manager", "addressing_information"),
        (Mock(), Mock())
    ])
    @pytest.mark.parametrize("packet_records_number, message_records_number, kwargs", [
        (1, 2, {"a": Mock(), "b": Mock()}),
        (Mock(), Mock(), {"param1": Mock(), "param2": Mock(), "something_else": Mock()}),
    ])
    def test_init__all_args(self, can_bus_manager, addressing_information,
                            packet_records_number, message_records_number, kwargs):
        PyCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                         can_bus_manager=can_bus_manager,
                                         addressing_information=addressing_information,
                                         packet_records_number=packet_records_number,
                                         message_records_number=message_records_number,
                                         **kwargs)
        self.mock_abstract_can_ti_init.assert_called_once_with(
            can_bus_manager=can_bus_manager,
            addressing_information=addressing_information,
            packet_records_number=packet_records_number,
            message_records_number=message_records_number,
            **kwargs)
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_cr_measured is None

    # n_as_measured

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_as_measured(self, value):
        self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured = value
        assert PyCanTransportInterface.n_as_measured.fget(self.mock_can_transport_interface) == value

    # n_as_measured

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_ar_measured(self, value):
        self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured = value
        assert PyCanTransportInterface.n_ar_measured.fget(self.mock_can_transport_interface) == value
            
    # n_bs_measured

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_bs_measured(self, value):
        self.mock_can_transport_interface._PyCanTransportInterface__n_bs_measured = value
        assert PyCanTransportInterface.n_bs_measured.fget(self.mock_can_transport_interface) == value
            
    # n_cr_measured

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_cr_measured(self, value):
        self.mock_can_transport_interface._PyCanTransportInterface__n_cr_measured = value
        assert PyCanTransportInterface.n_cr_measured.fget(self.mock_can_transport_interface) == value
            
    # is_supported_bus_manager

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_supported_bus_manager(self, mock_isinstance, value):
        assert PyCanTransportInterface.is_supported_bus_manager(value) == mock_isinstance.return_value
        mock_isinstance.assert_called_once_with(value, BusABC)

    # send_packet

    # def test_send_packet(self):
    #     with pytest.raises(NotImplementedError):
    #         PyCanTransportInterface.send_packet(self=self.mock_can_transport_interface, packet=Mock())

    # send_message

    def test_send_message(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.send_message(self=self.mock_can_transport_interface, message=Mock())

    # receive_packet

    # def test_receive_packet(self):
    #     with pytest.raises(NotImplementedError):
    #         PyCanTransportInterface.receive_packet(self=self.mock_can_transport_interface, timeout=Mock())

    # receive_message

    def test_receive_message(self):
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.receive_message(self=self.mock_can_transport_interface, timeout=Mock())


class TestPyCanTransportInterfaceIntegration:
    """Integration tests for `PyCanTransportInterface` class."""

    @pytest.mark.parametrize("init_kwargs", [
        {
            "can_bus_manager": Mock(spec=BusABC),
            "addressing_information": CanAddressingInformation(
                addressing_format=CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                rx_physical={"can_id": 0x641},
                tx_physical={"can_id": 0x642},
                rx_functional={"can_id": 0x6FE},
                tx_functional={"can_id": 0x6FF},
            ),
        }
    ])
    def test_init(self, init_kwargs):
        py_can_ti = PyCanTransportInterface(**init_kwargs)
        assert py_can_ti.n_as_measured is None
        assert py_can_ti.n_ar_measured is None
        assert py_can_ti.n_bs_measured is None
        assert py_can_ti.n_cr_measured is None

import pytest
from mock import MagicMock, Mock, patch

from uds.transport_interface.abstract_can_transport_interface import AbstractCanTransportInterface, \
    AbstractCanAddressingInformation, Iterable


class TestAbstractCanTransportInterface:
    """Unit tests for `AbstractCanTransportInterface` class."""

    SCRIPT_LOCATION = "uds.transport_interface.abstract_can_transport_interface"

    def setup(self):
        self.mock_can_transport_interface = Mock(spec=AbstractCanTransportInterface,
                                                 DEFAULT_FLOW_CONTROL_ARGS=AbstractCanTransportInterface.DEFAULT_FLOW_CONTROL_ARGS)
        # patching
        self._patcher_abstract_transport_interface_init \
            = patch(f"{self.SCRIPT_LOCATION}.AbstractTransportInterface.__init__")
        self.mock_abstract_transport_interface_init = self._patcher_abstract_transport_interface_init.start()
        self._patcher_can_segmenter_class = patch(f"{self.SCRIPT_LOCATION}.CanSegmenter")
        self.mock_can_segmenter_class = self._patcher_can_segmenter_class.start()
        self._patcher_can_packet_class = patch(f"{self.SCRIPT_LOCATION}.CanPacket")
        self.mock_can_packet_class = self._patcher_can_packet_class.start()
        self._patcher_warn = patch(f"{self.SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown(self):
        self._patcher_abstract_transport_interface_init.stop()
        self._patcher_can_segmenter_class.stop()
        self._patcher_can_packet_class.stop()
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("can_bus_manager, packet_records_number, message_records_number, addressing_information", [
        ("can_bus_manager", "packet_records_number", "message_records_number", "addressing_information"),
        (Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__type_error(self, mock_isinstance,
                              can_bus_manager, packet_records_number, message_records_number, addressing_information):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                                   can_bus_manager=can_bus_manager,
                                                   packet_records_number=packet_records_number,
                                                   message_records_number=message_records_number,
                                                   addressing_information=addressing_information)
        mock_isinstance.assert_called_once_with(addressing_information, AbstractCanAddressingInformation)

    @pytest.mark.parametrize("can_bus_manager, packet_records_number, message_records_number, addressing_information", [
        ("can_bus_manager", "packet_records_number", "message_records_number", Mock(tx_packets_physical_ai={})),
        (Mock(), Mock(), Mock(), Mock(tx_packets_physical_ai={"arg1": 1, "arg2": 2})),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__valid_mandatory_args(self, mock_isinstance,
                                        can_bus_manager, packet_records_number, message_records_number,
                                        addressing_information):
        mock_isinstance.return_value = True
        AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                               can_bus_manager=can_bus_manager,
                                               packet_records_number=packet_records_number,
                                               message_records_number=message_records_number,
                                               addressing_information=addressing_information)
        mock_isinstance.assert_called_once_with(addressing_information, AbstractCanAddressingInformation)
        self.mock_abstract_transport_interface_init.assert_called_once_with(
            bus_manager=can_bus_manager,
            packet_records_number=packet_records_number,
            message_records_number=message_records_number)
        self.mock_can_segmenter_class.assert_called_once_with(
            addressing_format=addressing_information.addressing_format,
            physical_ai=addressing_information.tx_packets_physical_ai,
            functional_ai=addressing_information.tx_packets_functional_ai)
        self.mock_can_packet_class.assert_called_once_with(
            dlc=None if self.mock_can_transport_interface.use_data_optimization else self.mock_can_transport_interface.dlc,
            filler_byte=self.mock_can_transport_interface.filler_byte,
            **addressing_information.tx_packets_physical_ai,
            **self.mock_can_transport_interface.DEFAULT_FLOW_CONTROL_ARGS)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__addressing_information \
               == addressing_information
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter \
               == self.mock_can_segmenter_class.return_value
        assert self.mock_can_transport_interface.flow_control_generator == self.mock_can_packet_class.return_value
        assert self.mock_can_transport_interface.n_as_timeout == self.mock_can_transport_interface.N_AS_TIMEOUT
        assert self.mock_can_transport_interface.n_ar_timeout == self.mock_can_transport_interface.N_AR_TIMEOUT
        assert self.mock_can_transport_interface.n_bs_timeout == self.mock_can_transport_interface.N_BS_TIMEOUT
        assert self.mock_can_transport_interface.n_br == self.mock_can_transport_interface.DEFAULT_N_BR
        assert self.mock_can_transport_interface.n_cs == self.mock_can_transport_interface.DEFAULT_N_CS
        assert self.mock_can_transport_interface.n_cr_timeout == self.mock_can_transport_interface.N_CR_TIMEOUT

    @pytest.mark.parametrize("can_bus_manager, packet_records_number, message_records_number, addressing_information", [
        ("can_bus_manager", "packet_records_number", "message_records_number", Mock(tx_packets_physical_ai={})),
        (Mock(), Mock(), Mock(), Mock(tx_packets_physical_ai={"arg1": 1, "arg2": 2})),
    ])
    @pytest.mark.parametrize("n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout, "
                             "dlc, use_data_optimization, filler_byte, flow_control_generator", [
        ("n_as_timeout", "n_ar_timeout", "n_bs_timeout", "n_br", "n_cs", "n_cr_timeout", "dlc", "use_data_optimization",
         "filler_byte", "flow_control_generator"),
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__valid_all_args(self, mock_isinstance,
                                  can_bus_manager, packet_records_number, message_records_number,
                                  addressing_information, n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs,
                                  n_cr_timeout, dlc, use_data_optimization, filler_byte, flow_control_generator):
        mock_isinstance.return_value = True
        AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                               can_bus_manager=can_bus_manager,
                                               packet_records_number=packet_records_number,
                                               message_records_number=message_records_number,
                                               addressing_information=addressing_information,
                                               n_as_timeout=n_as_timeout,
                                               n_ar_timeout=n_ar_timeout,
                                               n_bs_timeout=n_bs_timeout,
                                               n_br=n_br,
                                               n_cs=n_cs,
                                               n_cr_timeout=n_cr_timeout,
                                               dlc=dlc,
                                               use_data_optimization=use_data_optimization,
                                               filler_byte=filler_byte,
                                               flow_control_generator=flow_control_generator)
        mock_isinstance.assert_called_once_with(addressing_information, AbstractCanAddressingInformation)
        self.mock_abstract_transport_interface_init.assert_called_once_with(
            bus_manager=can_bus_manager,
            packet_records_number=packet_records_number,
            message_records_number=message_records_number)
        self.mock_can_segmenter_class.assert_called_once_with(
            addressing_format=addressing_information.addressing_format,
            physical_ai=addressing_information.tx_packets_physical_ai,
            functional_ai=addressing_information.tx_packets_functional_ai,
            dlc=dlc,
            use_data_optimization=use_data_optimization,
            filler_byte=filler_byte)
        self.mock_can_packet_class.assert_not_called()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__addressing_information \
               == addressing_information
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter \
               == self.mock_can_segmenter_class.return_value
        assert self.mock_can_transport_interface.flow_control_generator == flow_control_generator
        assert self.mock_can_transport_interface.n_as_timeout == n_as_timeout
        assert self.mock_can_transport_interface.n_ar_timeout == n_ar_timeout
        assert self.mock_can_transport_interface.n_bs_timeout == n_bs_timeout
        assert self.mock_can_transport_interface.n_br == n_br
        assert self.mock_can_transport_interface.n_cs == n_cs
        assert self.mock_can_transport_interface.n_cr_timeout == n_cr_timeout

    # segmenter

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_segmenter(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter = value
        assert AbstractCanTransportInterface.segmenter.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter

    # n_as

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_as_timeout__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout = value
        assert AbstractCanTransportInterface.n_as_timeout.fget(self.mock_can_transport_interface) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_as_timeout__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_as_timeout__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le)
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_as_timeout__set__valid_with_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AS_TIMEOUT)
        self.mock_warn.assert_called_once()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout == mock_value

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_as_timeout__set__valid_without_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AS_TIMEOUT)
        self.mock_warn.assert_not_called()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout == mock_value

    # n_ar

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_ar_timeout__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout = value
        assert AbstractCanTransportInterface.n_ar_timeout.fget(self.mock_can_transport_interface) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_ar_timeout__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_ar_timeout__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le)
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_ar_timeout__set__valid_with_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AR_TIMEOUT)
        self.mock_warn.assert_called_once()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout == mock_value

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_ar_timeout__set__valid_without_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AR_TIMEOUT)
        self.mock_warn.assert_not_called()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout == mock_value
            
    # n_bs

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_bs_timeout__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout = value
        assert AbstractCanTransportInterface.n_bs_timeout.fget(self.mock_can_transport_interface) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_bs_timeout__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_bs_timeout__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le)
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_bs_timeout__set__valid_with_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_BS_TIMEOUT)
        self.mock_warn.assert_called_once()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout == mock_value

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_bs_timeout__set__valid_without_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_BS_TIMEOUT)
        self.mock_warn.assert_not_called()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout == mock_value
            
    # n_br

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_br__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_br = value
        assert AbstractCanTransportInterface.n_br.fget(self.mock_can_transport_interface) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_br__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.n_br.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value, max_value", [
        (-0.00000001, 100),
        (-1, 900),
        (901, 900.5),
        (450.1, 450),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_br__set__value_error(self, mock_isinstance, value, max_value):
        mock_isinstance.return_value = True
        self.mock_can_transport_interface.n_br_max = max_value
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_br.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value, max_value", [
        (99, 100),
        (899.99, 900),
        (45.59, 900.5),
        (0, 450),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_br__set__valid(self, mock_isinstance, value, max_value):
        mock_isinstance.return_value = True
        self.mock_can_transport_interface.n_br_max = max_value
        AbstractCanTransportInterface.n_br.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_br == value

    @pytest.mark.parametrize("n_bs_timeout, n_ar_measured", [
        (1000, 10),
        (965.43, 12.45),
    ])
    def test_n_br_max__n_ar_measured(self, n_bs_timeout, n_ar_measured):
        self.mock_can_transport_interface.n_bs_timeout = n_bs_timeout
        self.mock_can_transport_interface.n_ar_measured = n_ar_measured
        assert AbstractCanTransportInterface.n_br_max.fget(self.mock_can_transport_interface) \
               == 0.9 * n_bs_timeout - n_ar_measured

    @pytest.mark.parametrize("n_bs_timeout", [1000, 965.43])
    def test_n_br_max__n_ar_not_measured(self, n_bs_timeout):
        self.mock_can_transport_interface.n_bs_timeout = n_bs_timeout
        self.mock_can_transport_interface.n_ar_measured = None
        assert AbstractCanTransportInterface.n_br_max.fget(self.mock_can_transport_interface) \
               == 0.9 * n_bs_timeout

    # n_cs

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_cs__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs = value
        assert AbstractCanTransportInterface.n_cs.fget(self.mock_can_transport_interface) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cs__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value, max_value", [
        (-0.00000001, 100),
        (-1, 900),
        (901, 900.5),
        (450.1, 450),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cs__set__value_error(self, mock_isinstance, value, max_value):
        mock_isinstance.return_value = True
        self.mock_can_transport_interface.n_cs_max = max_value
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value, max_value", [
        (99, 100),
        (899.99, 900),
        (45.59, 900.5),
        (0, 450),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cs__set__valid(self, mock_isinstance, value, max_value):
        mock_isinstance.return_value = True
        self.mock_can_transport_interface.n_cs_max = max_value
        AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs == value

    def test_n_cs__set__none(self):
        AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, None)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs is None

    @pytest.mark.parametrize("n_cr_timeout, n_as_measured", [
        (1000, 10),
        (965.43, 12.45),
    ])
    def test_n_cs_max__n_as_measured(self, n_cr_timeout, n_as_measured):
        self.mock_can_transport_interface.n_cr_timeout = n_cr_timeout
        self.mock_can_transport_interface.n_as_measured = n_as_measured
        assert AbstractCanTransportInterface.n_cs_max.fget(self.mock_can_transport_interface) \
               == 0.9 * n_cr_timeout - n_as_measured

    @pytest.mark.parametrize("n_cr_timeout", [1000, 965.43])
    def test_n_cs_max__n_as_not_measured(self, n_cr_timeout):
        self.mock_can_transport_interface.n_cr_timeout = n_cr_timeout
        self.mock_can_transport_interface.n_as_measured = None
        assert AbstractCanTransportInterface.n_cs_max.fget(self.mock_can_transport_interface) \
               == 0.9 * n_cr_timeout
            
    # n_cr

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_n_cr_timeout__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout = value
        assert AbstractCanTransportInterface.n_cr_timeout.fget(self.mock_can_transport_interface) == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cr_timeout__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cr_timeout__set__value_error(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le)
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cr_timeout__set__valid_with_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_CR_TIMEOUT)
        self.mock_warn.assert_called_once()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout == mock_value

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_cr_timeout__set__valid_without_warn(self, mock_isinstance):
        mock_isinstance.return_value = True
        mock_le = Mock(return_value=False)
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__le__=mock_le, __ne__=mock_ne)
        AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, (int, float))
        mock_le.assert_called_once_with(0)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_CR_TIMEOUT)
        self.mock_warn.assert_not_called()
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout == mock_value

    # addressing_information

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_addressing_information(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__addressing_information = value
        assert AbstractCanTransportInterface.addressing_information.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface._AbstractCanTransportInterface__addressing_information

    # dlc

    def test_dlc__get(self):
        assert AbstractCanTransportInterface.dlc.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface.segmenter.dlc

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_dlc__set(self, value):
        AbstractCanTransportInterface.dlc.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface.segmenter.dlc == value
            
    # use_data_optimization

    def test_use_data_optimization__get(self):
        assert AbstractCanTransportInterface.use_data_optimization.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface.segmenter.use_data_optimization

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_use_data_optimization__set(self, value):
        AbstractCanTransportInterface.use_data_optimization.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface.segmenter.use_data_optimization == value
            
    # filler_byte

    def test_filler_byte__get(self):
        assert AbstractCanTransportInterface.filler_byte.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface.segmenter.filler_byte

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_filler_byte__set(self, value):
        AbstractCanTransportInterface.filler_byte.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface.segmenter.filler_byte == value

    # flow_control_generator

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_flow_control_generator__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_generator = value
        assert AbstractCanTransportInterface.flow_control_generator.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_generator

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_generator__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.flow_control_generator.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (self.mock_can_packet_class, Iterable))

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_generator__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        AbstractCanTransportInterface.flow_control_generator.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (self.mock_can_packet_class, Iterable))
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_generator == value
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_iterator is None

    # _get_flow_control

    @pytest.mark.parametrize("is_first", [True, False])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_flow_control__packet(self, mock_isinstance, is_first):
        mock_isinstance.return_value = True
        assert AbstractCanTransportInterface._get_flow_control(self=self.mock_can_transport_interface,
                                                               is_first=is_first) \
               == self.mock_can_transport_interface.flow_control_generator
        mock_isinstance.assert_called_once_with(self.mock_can_transport_interface.flow_control_generator,
                                                self.mock_can_packet_class)

    @patch(f"{SCRIPT_LOCATION}.iter")
    @patch(f"{SCRIPT_LOCATION}.next")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_flow_control__generator__first(self, mock_isinstance, mock_next, mock_iter):
        mock_isinstance.return_value = False
        assert AbstractCanTransportInterface._get_flow_control(self=self.mock_can_transport_interface,
                                                               is_first=True) \
               == mock_next.return_value
        mock_isinstance.assert_called_once_with(self.mock_can_transport_interface.flow_control_generator,
                                                self.mock_can_packet_class)
        mock_iter.assert_called_once_with(self.mock_can_transport_interface.flow_control_generator)
        mock_next.assert_called_once_with(
            self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_iterator)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_iterator \
               == mock_iter.return_value

    @patch(f"{SCRIPT_LOCATION}.iter")
    @patch(f"{SCRIPT_LOCATION}.next")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_get_flow_control__generator__following(self, mock_isinstance, mock_next, mock_iter):
        mock_isinstance.return_value = False
        self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_iterator = Mock()
        assert AbstractCanTransportInterface._get_flow_control(self=self.mock_can_transport_interface,
                                                               is_first=False) \
               == mock_next.return_value
        mock_isinstance.assert_called_once_with(self.mock_can_transport_interface.flow_control_generator,
                                                self.mock_can_packet_class)
        mock_iter.assert_not_called()
        mock_next.assert_called_once_with(
            self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_iterator)

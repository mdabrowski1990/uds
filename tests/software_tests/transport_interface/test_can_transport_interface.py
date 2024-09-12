from random import randint

import pytest
from mock import AsyncMock, MagicMock, Mock, patch

from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.transmission_attributes import AddressingType
from uds.transport_interface.can_transport_interface import (
    AbstractCanAddressingInformation,
    AbstractCanTransportInterface,
    AbstractFlowControlParametersGenerator,
    BusABC,
    CanPacket,
    CanPacketType,
    DefaultFlowControlParametersGenerator,
    PyCanTransportInterface,
    TransmissionDirection,
    UdsMessage,
    UdsMessageRecord,
)

SCRIPT_LOCATION = "uds.transport_interface.can_transport_interface"


class TestAbstractCanTransportInterface:
    """Unit tests for `AbstractCanTransportInterface` class."""

    def setup_method(self):
        self.mock_can_transport_interface = Mock(spec=AbstractCanTransportInterface)
        # patching
        self._patcher_abstract_transport_interface_init \
            = patch(f"{SCRIPT_LOCATION}.AbstractTransportInterface.__init__")
        self.mock_abstract_transport_interface_init = self._patcher_abstract_transport_interface_init.start()
        self._patcher_can_segmenter_class = patch(f"{SCRIPT_LOCATION}.CanSegmenter")
        self.mock_can_segmenter_class = self._patcher_can_segmenter_class.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_abstract_transport_interface_init.stop()
        self._patcher_can_segmenter_class.stop()
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("can_bus_manager, addressing_information", [
        ("can_bus_manager", "addressing_information"),
        (Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__type_error(self, mock_isinstance,
                              can_bus_manager, addressing_information):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                                   can_bus_manager=can_bus_manager,
                                                   addressing_information=addressing_information)
        mock_isinstance.assert_called_once_with(addressing_information, AbstractCanAddressingInformation)

    @pytest.mark.parametrize("can_bus_manager, addressing_information", [
        ("can_bus_manager", "some addressing information"),
        (Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__valid_mandatory_args(self, mock_isinstance,
                                        can_bus_manager, addressing_information):
        mock_isinstance.return_value = True
        AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                               can_bus_manager=can_bus_manager,
                                               addressing_information=addressing_information)
        mock_isinstance.assert_called_once_with(addressing_information, AbstractCanAddressingInformation)
        self.mock_abstract_transport_interface_init.assert_called_once_with(bus_manager=can_bus_manager)
        self.mock_can_segmenter_class.assert_called_once_with(addressing_information=addressing_information)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__addressing_information \
               == addressing_information
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter \
               == self.mock_can_segmenter_class.return_value
        assert self.mock_can_transport_interface.n_as_timeout == self.mock_can_transport_interface.N_AS_TIMEOUT
        assert self.mock_can_transport_interface.n_ar_timeout == self.mock_can_transport_interface.N_AR_TIMEOUT
        assert self.mock_can_transport_interface.n_bs_timeout == self.mock_can_transport_interface.N_BS_TIMEOUT
        assert self.mock_can_transport_interface.n_br == self.mock_can_transport_interface.DEFAULT_N_BR
        assert self.mock_can_transport_interface.n_cs == self.mock_can_transport_interface.DEFAULT_N_CS
        assert self.mock_can_transport_interface.n_cr_timeout == self.mock_can_transport_interface.N_CR_TIMEOUT
        assert (self.mock_can_transport_interface.flow_control_parameters_generator
                == self.mock_can_transport_interface.DEFAULT_FLOW_CONTROL_PARAMETERS)

    @pytest.mark.parametrize("can_bus_manager, addressing_information", [
        ("can_bus_manager", "addressing_information"),
        (Mock(), Mock()),
    ])
    @pytest.mark.parametrize("n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout, "
                             "dlc, use_data_optimization, filler_byte, flow_control_parameters_generator", [
        ("n_as_timeout", "n_ar_timeout", "n_bs_timeout", "n_br", "n_cs", "n_cr_timeout", "dlc", "use_data_optimization",
         "filler_byte", "flow_control_parameters_generator"),
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_init__valid_all_args(self, mock_isinstance,
                                  can_bus_manager, addressing_information,
                                  n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout,
                                  dlc, use_data_optimization, filler_byte, flow_control_parameters_generator):
        mock_isinstance.return_value = True
        AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                               can_bus_manager=can_bus_manager,
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
                                               flow_control_parameters_generator=flow_control_parameters_generator)
        mock_isinstance.assert_called_once_with(addressing_information, AbstractCanAddressingInformation)
        self.mock_abstract_transport_interface_init.assert_called_once_with(bus_manager=can_bus_manager)
        self.mock_can_segmenter_class.assert_called_once_with(
            addressing_information=addressing_information,
            dlc=dlc,
            use_data_optimization=use_data_optimization,
            filler_byte=filler_byte)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__addressing_information \
               == addressing_information
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter \
               == self.mock_can_segmenter_class.return_value
        assert self.mock_can_transport_interface.n_as_timeout == n_as_timeout
        assert self.mock_can_transport_interface.n_ar_timeout == n_ar_timeout
        assert self.mock_can_transport_interface.n_bs_timeout == n_bs_timeout
        assert self.mock_can_transport_interface.n_br == n_br
        assert self.mock_can_transport_interface.n_cs == n_cs
        assert self.mock_can_transport_interface.n_cr_timeout == n_cr_timeout
        assert self.mock_can_transport_interface.flow_control_parameters_generator == flow_control_parameters_generator

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

    # flow_control_parameters_generator

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_flow_control_parameters_generator__get(self, value):
        self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_parameters_generator = value
        assert AbstractCanTransportInterface.flow_control_parameters_generator.fget(self.mock_can_transport_interface) \
               == value

    @pytest.mark.parametrize("value", [Mock(spec=AbstractFlowControlParametersGenerator),
                                       Mock(spec=DefaultFlowControlParametersGenerator)])
    def test_flow_control_parameters_generator__set(self, value):
        AbstractCanTransportInterface.flow_control_parameters_generator.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_parameters_generator == value

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_flow_control_parameters_generator__set__type_error(self, value):
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.flow_control_parameters_generator.fset(self.mock_can_transport_interface, value)


class TestPyCanTransportInterface:
    """Unit tests for `PyCanTransportInterface` class."""

    def setup_method(self):
        self.mock_can_transport_interface = MagicMock(spec=PyCanTransportInterface)
        # patching
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_wait_for = patch(f"{SCRIPT_LOCATION}.wait_for", AsyncMock(side_effect=lambda *args, **kwargs: args[0]))
        self.mock_wait_for = self._patcher_wait_for.start()
        self._patcher_time = patch(f"{SCRIPT_LOCATION}.time")
        self.mock_time = self._patcher_time.start()
        self._patcher_datetime = patch(f"{SCRIPT_LOCATION}.datetime")
        self.mock_datetime = self._patcher_datetime.start()
        self._patcher_abstract_can_ti_init = patch(f"{SCRIPT_LOCATION}.AbstractCanTransportInterface.__init__")
        self.mock_abstract_can_ti_init = self._patcher_abstract_can_ti_init.start()
        self._patcher_uds_message = patch(f"{SCRIPT_LOCATION}.UdsMessage")
        self.mock_uds_message = self._patcher_uds_message.start()
        self._patcher_uds_message_record = patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
        self.mock_uds_message_record = self._patcher_uds_message_record.start()
        self._patcher_can_id_handler = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler = self._patcher_can_id_handler.start()
        self._patcher_can_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler = self._patcher_can_dlc_handler.start()
        self._patcher_can_packet_record = patch(f"{SCRIPT_LOCATION}.CanPacketRecord")
        self.mock_can_packet_record = self._patcher_can_packet_record.start()
        self._patcher_notifier = patch(f"{SCRIPT_LOCATION}.Notifier")
        self.mock_notifier = self._patcher_notifier.start()
        self._patcher_message = patch(f"{SCRIPT_LOCATION}.Message")
        self.mock_message = self._patcher_message.start()

    def teardown_method(self):
        self._patcher_warn.stop()
        self._patcher_wait_for.stop()
        self._patcher_time.stop()
        self._patcher_datetime.stop()
        self._patcher_abstract_can_ti_init.stop()
        self._patcher_uds_message.stop()
        self._patcher_uds_message_record.stop()
        self._patcher_can_id_handler.stop()
        self._patcher_can_dlc_handler.stop()
        self._patcher_can_packet_record.stop()
        self._patcher_notifier.stop()
        self._patcher_message.stop()

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
            addressing_information=addressing_information)
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_cr_measured is None

    @pytest.mark.parametrize("can_bus_manager, addressing_information", [
        ("can_bus_manager", "addressing_information"),
        (Mock(), Mock())
    ])
    @pytest.mark.parametrize("kwargs", [
        {"a": Mock(), "b": Mock()},
        {"param1": Mock(), "param2": Mock(), "something_else": Mock()},
    ])
    def test_init__all_args(self, can_bus_manager, addressing_information, kwargs):
        PyCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                         can_bus_manager=can_bus_manager,
                                         addressing_information=addressing_information,
                                         **kwargs)
        self.mock_abstract_can_ti_init.assert_called_once_with(can_bus_manager=can_bus_manager,
                                                               addressing_information=addressing_information,
                                                               **kwargs)
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__n_cr_measured is None

    # __del__

    def test_del(self):
        assert PyCanTransportInterface.__del__(self.mock_can_transport_interface) is None
        self.mock_can_transport_interface._teardown_notifier.assert_called_once_with(suppress_warning=True)
        self.mock_can_transport_interface._teardown_async_notifier.assert_called_once_with(suppress_warning=True)

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

    # _teardown_notifier

    def test_teardown_notifier__no_notifier(self):
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = None
        assert PyCanTransportInterface._teardown_notifier(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        self.mock_warn.assert_not_called()

    def test_teardown_notifier__notifier(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = mock_notifier
        assert PyCanTransportInterface._teardown_notifier(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_teardown_notifier__notifier_with_suppressed_warning(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = mock_notifier
        assert PyCanTransportInterface._teardown_notifier(self.mock_can_transport_interface, suppress_warning=True) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_not_called()

    # _teardown_async_notifier

    def test_teardown_async_notifier__no_notifier(self):
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = None
        assert PyCanTransportInterface._teardown_async_notifier(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        self.mock_warn.assert_not_called()

    def test_teardown_async_notifier__notifier(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = mock_notifier
        assert PyCanTransportInterface._teardown_async_notifier(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_teardown_async_notifier__notifier_with_suppressed_warning(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = mock_notifier
        assert PyCanTransportInterface._teardown_async_notifier(self.mock_can_transport_interface, suppress_warning=True) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_not_called()

    # _setup_notifier

    def test_setup_notifier__no_notifier(self):
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = None
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock()
        assert PyCanTransportInterface._setup_notifier(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.bus_manager,
            listeners=[self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_can_transport_interface._teardown_async_notifier.assert_called_once_with()

    def test_setup_notifier__notifier_exists(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = mock_notifier
        assert PyCanTransportInterface._setup_notifier(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier == mock_notifier
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface._teardown_async_notifier.assert_called_once_with()

    # _setup_async_notifier

    @pytest.mark.parametrize("loop", ["some loop", Mock()])
    def test_setup_async_notifier__no_notifier(self, loop):
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = None
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock()
        assert PyCanTransportInterface._setup_async_notifier(self.mock_can_transport_interface, loop=loop) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.bus_manager,
            listeners=[self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=loop)
        self.mock_can_transport_interface._teardown_notifier.assert_called_once_with()

    @pytest.mark.parametrize("loop", ["some loop", Mock()])
    def test_setup_async_notifier__notifier_exists(self, loop):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = mock_notifier
        assert PyCanTransportInterface._setup_async_notifier(self.mock_can_transport_interface, loop=loop) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier == mock_notifier
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface._teardown_notifier.assert_called_once_with()

    # clear_frames_buffers

    @pytest.mark.parametrize("sync_queue_size", [0, 1, 7])
    @pytest.mark.parametrize("async_queue_size", [0, 1, 43])
    def test_clear_frames_buffers(self, sync_queue_size, async_queue_size):
        mock_sync_queue = Mock(qsize=Mock(return_value=sync_queue_size))
        mock_async_queue = Mock(qsize=Mock(return_value=async_queue_size))
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(buffer=mock_sync_queue)
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(buffer=mock_async_queue)
        assert PyCanTransportInterface.clear_frames_buffers(self.mock_can_transport_interface) is None
        mock_sync_queue.qsize.assert_called_once_with()
        mock_async_queue.qsize.assert_called_once_with()
        assert mock_sync_queue.get_nowait.call_count == sync_queue_size
        assert mock_async_queue.get_nowait.call_count == async_queue_size

    # is_supported_bus_manager

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_supported_bus_manager(self, mock_isinstance, value):
        assert PyCanTransportInterface.is_supported_bus_manager(value) == mock_isinstance.return_value
        mock_isinstance.assert_called_once_with(value, BusABC)

    # send_packet

    @pytest.mark.parametrize("packet", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_send_packet__type_error(self, mock_isinstance, packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PyCanTransportInterface.send_packet(self.mock_can_transport_interface, packet)
        mock_isinstance.assert_called_once_with(packet, CanPacket)

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=(0x12, 0x34)),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=tuple(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=tuple(range(64, 128))),
    ])
    def test_send_packet__timeout(self, packet):
        mock_get_message = Mock(return_value=MagicMock(arbitration_id=packet.can_id,
                                                       data=packet.raw_frame_data,
                                                       is_rx=True,
                                                       timestamp=MagicMock(__lt__=Mock(return_value=False))))
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured = None
        self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured = None
        self.mock_can_transport_interface.n_ar_timeout = self.mock_can_transport_interface.n_as_timeout \
            = MagicMock(__truediv__=lambda this, other: this,
                        __div__=lambda this, other: this,
                        __sub__=lambda this, other: this,
                        __le__=Mock(return_value=True))
        with pytest.raises(TimeoutError):
            PyCanTransportInterface.send_packet(self.mock_can_transport_interface, packet)
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_message.assert_called_once_with(arbitration_id=packet.can_id,
                                                  is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                                                  data=packet.raw_frame_data,
                                                  is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value)
        self.mock_can_transport_interface.bus_manager.send.assert_called_once_with(self.mock_message.return_value)

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=(0x12, 0x34)),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=tuple(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=tuple(range(64, 128))),
    ])
    def test_send_packet(self, packet):
        mock_get_message = Mock(return_value=MagicMock(arbitration_id=packet.can_id,
                                                       data=packet.raw_frame_data,
                                                       is_rx=True,
                                                       timestamp=MagicMock(__lt__=Mock(return_value=False))))
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured = None
        self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured = None
        self.mock_can_transport_interface.n_ar_timeout = self.mock_can_transport_interface.n_as_timeout \
            = MagicMock(__truediv__=lambda this, other: this,
                        __div__=lambda this, other: this,
                        __sub__=lambda this, other: this,
                        __le__=Mock(return_value=False))
        assert PyCanTransportInterface.send_packet(self.mock_can_transport_interface, packet) \
               == self.mock_can_packet_record.return_value
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_message.assert_called_once_with(arbitration_id=packet.can_id,
                                                  is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                                                  data=packet.raw_frame_data,
                                                  is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value)
        self.mock_can_transport_interface.bus_manager.send.assert_called_once_with(self.mock_message.return_value)
        self.mock_datetime.fromtimestamp.assert_called_once_with(mock_get_message.return_value.timestamp)
        self.mock_can_packet_record.assert_called_once_with(frame=mock_get_message.return_value,
                                                            direction=TransmissionDirection.TRANSMITTED,
                                                            addressing_type=packet.addressing_type,
                                                            addressing_format=packet.addressing_format,
                                                            transmission_time=self.mock_datetime.fromtimestamp.return_value)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is None
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured \
                   == mock_get_message.return_value.timestamp.__sub__.return_value
            mock_get_message.return_value.timestamp.__sub__.assert_called_once_with(self.mock_time.return_value)
        else:
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured \
                   == mock_get_message.return_value.timestamp.__sub__.return_value
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None
            mock_get_message.return_value.timestamp.__sub__.assert_called_once_with(self.mock_time.return_value)

    # receive_packet

    @pytest.mark.parametrize("timeout", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_packet__type_error(self, mock_isinstance, timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
        mock_isinstance.assert_called_once_with(timeout, (int, float))

    @pytest.mark.parametrize("timeout", [0, -654])
    def test_receive_packet__value_error(self, timeout):
        with pytest.raises(ValueError):
            PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    def test_receive_packet__timeout_error__no_message(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __rsub__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock(return_value=None)
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
        mock_get_message.assert_called_once()

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    def test_receive_packet__timeout_error__out_of_time(self, timeout):
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __rsub__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
        mock_is_timeout_reached.assert_called_once_with(0)

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    def test_receive_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT \
            = MagicMock(__sub__=lambda this, other: this,
                        __rsub__=lambda this, other: this,
                        __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(get_message=mock_get_message)
        assert PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout) \
               == self.mock_can_packet_record.return_value
        self.mock_datetime.fromtimestamp.assert_called_once_with(mock_get_message.return_value.timestamp)
        self.mock_can_transport_interface.segmenter.is_input_packet.assert_called_once_with(
            can_id=mock_get_message.return_value.arbitration_id,
            data=mock_get_message.return_value.data)
        self.mock_can_packet_record.assert_called_once_with(
            frame=mock_get_message.return_value,
            direction=TransmissionDirection.RECEIVED,
            addressing_type=self.mock_can_transport_interface.segmenter.is_input_packet.return_value,
            addressing_format=self.mock_can_transport_interface.segmenter.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value)

    # async_send_packet

    @pytest.mark.parametrize("packet", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_send_packet__type_error(self, mock_isinstance, packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            await PyCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet)
        mock_isinstance.assert_called_once_with(packet, CanPacket)

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=(0x12, 0x34)),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=tuple(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=tuple(range(64, 128))),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet(self, packet):
        mock_get_message = Mock(return_value=MagicMock(arbitration_id=packet.can_id,
                                                       data=packet.raw_frame_data,
                                                       is_rx=True,
                                                       timestamp=MagicMock(__lt__=Mock(return_value=False))))
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured = None
        self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured = None
        assert await PyCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet) \
               == self.mock_can_packet_record.return_value
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_message.assert_called_once_with(arbitration_id=packet.can_id,
                                                  is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                                                  data=packet.raw_frame_data,
                                                  is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value)
        self.mock_can_transport_interface.bus_manager.send.assert_called_once_with(self.mock_message.return_value)
        self.mock_datetime.fromtimestamp.assert_called_once_with(mock_get_message.return_value.timestamp)
        self.mock_can_packet_record.assert_called_once_with(frame=mock_get_message.return_value,
                                                            direction=TransmissionDirection.TRANSMITTED,
                                                            addressing_type=packet.addressing_type,
                                                            addressing_format=packet.addressing_format,
                                                            transmission_time=self.mock_datetime.fromtimestamp.return_value)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is None
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured \
                   == mock_get_message.return_value.timestamp.__sub__.return_value
            mock_get_message.return_value.timestamp.__sub__.assert_called_once_with(self.mock_time.return_value)
        else:
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured \
                   == mock_get_message.return_value.timestamp.__sub__.return_value
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None
            mock_get_message.return_value.timestamp.__sub__.assert_called_once_with(self.mock_time.return_value)

    # async_receive_packet

    @pytest.mark.parametrize("timeout", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_packet__type_error(self, mock_isinstance, timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            await PyCanTransportInterface.async_receive_packet(self.mock_can_transport_interface, timeout)
        mock_isinstance.assert_called_once_with(timeout, (int, float))

    @pytest.mark.parametrize("timeout", [0, -654])
    @pytest.mark.asyncio
    async def test_async_receive_packet__value_error(self, timeout):
        with pytest.raises(ValueError):
            await PyCanTransportInterface.async_receive_packet(self.mock_can_transport_interface, timeout)

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_packet__timeout(self, timeout):
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __rsub__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            await PyCanTransportInterface.async_receive_packet(self.mock_can_transport_interface, timeout)
        mock_is_timeout_reached.assert_called_once_with(0)

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __rsub__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(get_message=mock_get_message)
        assert await PyCanTransportInterface.async_receive_packet(self.mock_can_transport_interface, timeout) \
               == self.mock_can_packet_record.return_value
        self.mock_datetime.fromtimestamp.assert_called_once_with(mock_get_message.return_value.timestamp)
        self.mock_can_transport_interface.segmenter.is_input_packet.assert_called_once_with(
            can_id=mock_get_message.return_value.arbitration_id,
            data=mock_get_message.return_value.data)
        self.mock_can_packet_record.assert_called_once_with(
            frame=mock_get_message.return_value,
            direction=TransmissionDirection.RECEIVED,
            addressing_type=self.mock_can_transport_interface.segmenter.is_input_packet.return_value,
            addressing_format=self.mock_can_transport_interface.segmenter.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value)

    # send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    def test_send_message__single_frame(self, message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        assert PyCanTransportInterface.send_message(self.mock_can_transport_interface,
                                                    message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(mock_segmented_message[0])
        self.mock_uds_message_record.assert_called_once_with((self.mock_can_transport_interface.send_packet.return_value, ))

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets(self, message):
        mock_segmented_message = [Mock(spec=CanPacket) for _ in range(randint(2, 20))]
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)

    # async_send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__single_frame(self, message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        assert await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface, message) \
               == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_send_packet.assert_called_once_with(mock_segmented_message[0], loop=None)
        self.mock_uds_message_record.assert_called_once_with((self.mock_can_transport_interface.async_send_packet.return_value, ))

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets(self, message):
        mock_segmented_message = [Mock(spec=CanPacket) for _ in range(randint(2, 20))]
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)


@pytest.mark.integration
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
                tx_functional={"can_id": 0x6FF}),
        },
        {
            "can_bus_manager": Mock(spec=BusABC),
            "addressing_information": CanAddressingInformation(
                addressing_format=CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                tx_physical={"target_address": 0x1B, "source_address": 0xFF, "address_extension": 0x87},
                rx_physical={"target_address": 0xFF, "source_address": 0x1B, "address_extension": 0x87},
                tx_functional={"target_address": 0xAC, "source_address": 0xFE, "address_extension": 0xFF},
                rx_functional={"target_address": 0xFE, "source_address": 0xAC, "address_extension": 0xFF}),
            "n_as_timeout": 0.1,
            "n_ar_timeout": 987,
            "n_bs_timeout": 43,
            "n_br": 5.3,
            "n_cs": 0.92,
            "n_cr_timeout": 98.32,
        },
    ])
    def test_init(self, init_kwargs):
        py_can_ti = PyCanTransportInterface(**init_kwargs)
        assert py_can_ti.bus_manager == init_kwargs["can_bus_manager"]
        assert py_can_ti.addressing_information == init_kwargs["addressing_information"]
        assert py_can_ti.n_as_measured is None
        assert py_can_ti.n_ar_measured is None
        assert py_can_ti.n_bs_measured is None
        assert py_can_ti.n_cr_measured is None
        assert py_can_ti.n_as_timeout == init_kwargs.get("n_as_timeout", AbstractCanTransportInterface.N_AS_TIMEOUT)
        assert py_can_ti.n_ar_timeout == init_kwargs.get("n_ar_timeout", AbstractCanTransportInterface.N_AR_TIMEOUT)
        assert py_can_ti.n_bs_timeout == init_kwargs.get("n_bs_timeout", AbstractCanTransportInterface.N_BS_TIMEOUT)
        assert py_can_ti.n_br == init_kwargs.get("n_br", AbstractCanTransportInterface.DEFAULT_N_BR)
        assert py_can_ti.n_cs == init_kwargs.get("n_cs", AbstractCanTransportInterface.DEFAULT_N_CS)
        assert py_can_ti.n_cr_timeout == init_kwargs.get("n_cr_timeout", AbstractCanTransportInterface.N_CR_TIMEOUT)

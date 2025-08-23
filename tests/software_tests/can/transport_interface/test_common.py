from datetime import datetime

import pytest
from mock import MagicMock, Mock, patch

from uds.can import CanPacketRecord
from uds.can.transport_interface.common import (
    AbstractCanAddressingInformation,
    AbstractCanTransportInterface,
    AbstractFlowControlParametersGenerator,
    CanPacketType,
    TransmissionDirection,
    UdsMessageRecord,
)

SCRIPT_LOCATION = "uds.can.transport_interface.common"


class TestAbstractCanTransportInterface:
    """Unit tests for `AbstractCanTransportInterface` class."""

    def setup_method(self):
        self.mock_can_transport_interface = Mock(spec=AbstractCanTransportInterface)
        # patching
        self._patcher_abstract_transport_interface_init \
            = patch(f"{SCRIPT_LOCATION}.AbstractTransportInterface.__init__")
        self.mock_abstract_transport_interface_init = self._patcher_abstract_transport_interface_init.start()
        self._patcher_can_segmenter = patch(f"{SCRIPT_LOCATION}.CanSegmenter")
        self.mock_can_segmenter = self._patcher_can_segmenter.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()

    def teardown_method(self):
        self._patcher_abstract_transport_interface_init.stop()
        self._patcher_can_segmenter.stop()
        self._patcher_warn.stop()

    # __init__

    @pytest.mark.parametrize("network_manager, addressing_information", [
        (Mock(), Mock()),
        ("some network manger for CAN bus", Mock(spec=AbstractCanAddressingInformation)),
    ])
    def test_init__mandatory_args(self, network_manager, addressing_information):
        assert AbstractCanTransportInterface.__init__(self.mock_can_transport_interface,
                                                      network_manager=network_manager,
                                                      addressing_information=addressing_information) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured is None
        assert self.mock_can_transport_interface.n_as_timeout == AbstractCanTransportInterface.N_AS_TIMEOUT
        assert self.mock_can_transport_interface.n_ar_timeout == AbstractCanTransportInterface.N_AR_TIMEOUT
        assert self.mock_can_transport_interface.n_bs_timeout == AbstractCanTransportInterface.N_BS_TIMEOUT
        assert self.mock_can_transport_interface.n_br == AbstractCanTransportInterface.DEFAULT_N_BR
        assert self.mock_can_transport_interface.n_cs == AbstractCanTransportInterface.DEFAULT_N_CS
        assert self.mock_can_transport_interface.n_cr_timeout == AbstractCanTransportInterface.N_CR_TIMEOUT
        assert (self.mock_can_transport_interface.flow_control_parameters_generator
                == AbstractCanTransportInterface.DEFAULT_FLOW_CONTROL_PARAMETERS)
        self.mock_can_transport_interface.segmenter = self.mock_can_segmenter.return_value
        self.mock_abstract_transport_interface_init.assert_called_once_with(network_manager=network_manager,
                                                                            network_manager_receives_own_frames=True)
        self.mock_can_segmenter.assert_called_once_with(addressing_information=addressing_information)

    @pytest.mark.parametrize("network_manager, addressing_information, network_manager_receives_own_frames, "
                             "n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout, "
                             "flow_control_parameters_generator, segmenter_configuration", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), {"a": 1, "bc": 2, "def_xyz": Mock()})
    ])
    def test_init__all_args(self, network_manager, addressing_information, network_manager_receives_own_frames,
                            n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout,
                            flow_control_parameters_generator, segmenter_configuration):
        assert AbstractCanTransportInterface.__init__(
            self.mock_can_transport_interface,
            network_manager=network_manager,
            addressing_information=addressing_information,
            network_manager_receives_own_frames=network_manager_receives_own_frames,
            n_as_timeout=n_as_timeout,
            n_ar_timeout=n_ar_timeout,
            n_bs_timeout=n_bs_timeout,
            n_br=n_br,
            n_cs=n_cs,
            n_cr_timeout=n_cr_timeout,
            flow_control_parameters_generator=flow_control_parameters_generator,
            **segmenter_configuration) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured is None
        assert self.mock_can_transport_interface.n_as_timeout == n_as_timeout
        assert self.mock_can_transport_interface.n_ar_timeout == n_ar_timeout
        assert self.mock_can_transport_interface.n_bs_timeout == n_bs_timeout
        assert self.mock_can_transport_interface.n_br == n_br
        assert self.mock_can_transport_interface.n_cs == n_cs
        assert self.mock_can_transport_interface.n_cr_timeout == n_cr_timeout
        assert (self.mock_can_transport_interface.flow_control_parameters_generator
                == flow_control_parameters_generator)
        self.mock_can_transport_interface.segmenter = self.mock_can_segmenter.return_value
        self.mock_abstract_transport_interface_init.assert_called_once_with(
            network_manager=network_manager,
            network_manager_receives_own_frames=network_manager_receives_own_frames)
        self.mock_can_segmenter.assert_called_once_with(addressing_information=addressing_information,
                                                        **segmenter_configuration)

    # segmenter

    def test_segmenter__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter = Mock()
        assert (AbstractCanTransportInterface.segmenter.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter)

    @pytest.mark.parametrize("value", [Mock(), "CAN Segmenter"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmenter__set(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert AbstractCanTransportInterface.segmenter.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter == value
        mock_isinstance.assert_called_once_with(value, self.mock_can_segmenter)

    @pytest.mark.parametrize("value", [Mock(), "CAN Segmenter"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmenter__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.segmenter.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, self.mock_can_segmenter)

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

    def test_flow_control_parameters_generator__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_parameters_generator = Mock()
        assert (AbstractCanTransportInterface.flow_control_parameters_generator.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_parameters_generator)

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_parameters_generator__set(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert AbstractCanTransportInterface.flow_control_parameters_generator.fset(self.mock_can_transport_interface,
                                                                                    value) is None
        assert (self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_parameters_generator
                == value)
        mock_isinstance.assert_called_once_with(value, AbstractFlowControlParametersGenerator)

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_parameters_generator__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.flow_control_parameters_generator.fset(self.mock_can_transport_interface,
                                                                                 value)
        mock_isinstance.assert_called_once_with(value, AbstractFlowControlParametersGenerator)

    # n_as

    def test_n_as_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout = Mock()
        assert (AbstractCanTransportInterface.n_as_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout)

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
    def test_n_as_timeout__set__warning(self, mock_isinstance):
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
    def test_n_as_timeout__set__no_warning(self, mock_isinstance):
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

    def test_n_as_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured = Mock()
        assert (AbstractCanTransportInterface.n_as_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured)

    # n_ar

    def test_n_ar_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout = Mock()
        assert (AbstractCanTransportInterface.n_ar_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout)

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
    def test_n_ar_timeout__set__warning(self, mock_isinstance):
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
    def test_n_ar_timeout__set__no_warning(self, mock_isinstance):
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

    def test_n_ar_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured = Mock()
        assert (AbstractCanTransportInterface.n_ar_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured)

    # n_bs

    def test_n_bs_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout = Mock()
        assert (AbstractCanTransportInterface.n_bs_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout)

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
    def test_n_bs_timeout__set__warning(self, mock_isinstance):
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
    def test_n_bs_timeout__set__no_warning(self, mock_isinstance):
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

    def test_n_bs_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured = Mock()
        assert (AbstractCanTransportInterface.n_bs_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured)

    # n_br

    def test_n_br__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_br = Mock()
        assert (AbstractCanTransportInterface.n_br.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_br)

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
        (0, 450),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_n_br__set(self, mock_isinstance, value, max_value):
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
        assert (AbstractCanTransportInterface.n_br_max.fget(self.mock_can_transport_interface)
                == 0.9 * n_bs_timeout - n_ar_measured)

    @pytest.mark.parametrize("n_bs_timeout", [1000, 965.43])
    def test_n_br_max__n_ar_not_measured(self, n_bs_timeout):
        self.mock_can_transport_interface.n_bs_timeout = n_bs_timeout
        self.mock_can_transport_interface.n_ar_measured = None
        assert (AbstractCanTransportInterface.n_br_max.fget(self.mock_can_transport_interface)
                == 0.9 * n_bs_timeout)

    # n_cs

    def test_n_cs__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs = Mock()
        assert (AbstractCanTransportInterface.n_cs.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs)

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
        assert (AbstractCanTransportInterface.n_cs_max.fget(self.mock_can_transport_interface)
                == 0.9 * n_cr_timeout - n_as_measured)

    @pytest.mark.parametrize("n_cr_timeout", [1000, 965.43])
    def test_n_cs_max__n_as_not_measured(self, n_cr_timeout):
        self.mock_can_transport_interface.n_cr_timeout = n_cr_timeout
        self.mock_can_transport_interface.n_as_measured = None
        assert (AbstractCanTransportInterface.n_cs_max.fget(self.mock_can_transport_interface)
                == 0.9 * n_cr_timeout)

    # n_cr

    def test_n_cr_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout = Mock()
        assert (AbstractCanTransportInterface.n_cr_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout)

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

    def test_n_cr_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured = Mock()
        assert (AbstractCanTransportInterface.n_cr_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured)

    # _update_n_ar_measured

    @pytest.mark.parametrize("value", [Mock(), "some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_ar_measured__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface._update_n_ar_measured(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [-1, -0.0001])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_ar_measured__value_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            AbstractCanTransportInterface._update_n_ar_measured(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [0, AbstractCanTransportInterface.N_AR_TIMEOUT])
    def test_update_n_ar_measured__no_warning(self, value):
        self.mock_can_transport_interface.n_ar_timeout = AbstractCanTransportInterface.N_AR_TIMEOUT
        assert AbstractCanTransportInterface._update_n_ar_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured == value
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("value, n_ar_timeout", [
        (AbstractCanTransportInterface.N_AR_TIMEOUT + 1, AbstractCanTransportInterface.N_AR_TIMEOUT),
        (AbstractCanTransportInterface.N_AR_TIMEOUT - 1, AbstractCanTransportInterface.N_AR_TIMEOUT // 2),
    ])
    def test_update_n_ar_measured__warning(self, value, n_ar_timeout):
        self.mock_can_transport_interface.n_ar_timeout = n_ar_timeout
        assert AbstractCanTransportInterface._update_n_ar_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured == value
        self.mock_warn.assert_called_once()
        
    # _update_n_as_measured

    @pytest.mark.parametrize("value", [Mock(), "some value"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_as_measured__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface._update_n_as_measured(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [-1, -0.0001])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_as_measured__value_error(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            AbstractCanTransportInterface._update_n_as_measured(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [0, AbstractCanTransportInterface.N_AS_TIMEOUT])
    def test_update_n_as_measured__no_warning(self, value):
        self.mock_can_transport_interface.n_as_timeout = AbstractCanTransportInterface.N_AS_TIMEOUT
        assert AbstractCanTransportInterface._update_n_as_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured == value
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("value, n_as_timeout", [
        (AbstractCanTransportInterface.N_AS_TIMEOUT + 1, AbstractCanTransportInterface.N_AS_TIMEOUT),
        (AbstractCanTransportInterface.N_AS_TIMEOUT - 1, AbstractCanTransportInterface.N_AS_TIMEOUT // 2),
    ])
    def test_update_n_as_measured__warning(self, value, n_as_timeout):
        self.mock_can_transport_interface.n_as_timeout = n_as_timeout
        assert AbstractCanTransportInterface._update_n_as_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured == value
        self.mock_warn.assert_called_once()

    # _update_n_bs_measured

    @pytest.mark.parametrize("message_record", [
        Mock(), "not a message"
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_bs_measured__type_error(self, mock_isinstance, message_record):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface._update_n_bs_measured(self.mock_can_transport_interface,
                                                                message_record=message_record)
        mock_isinstance.assert_called_once_with(message_record, UdsMessageRecord)

    @pytest.mark.parametrize("message_record", [
        Mock(direction=TransmissionDirection.RECEIVED), Mock(direction="not transmitted")
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_bs_measured__value_error(self, mock_isinstance, message_record):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            AbstractCanTransportInterface._update_n_bs_measured(self.mock_can_transport_interface,
                                                                message_record=message_record)
        mock_isinstance.assert_called_once_with(message_record, UdsMessageRecord)

    def test_update_n_bs_measured__1_record(self):
        mock_message_record = Mock(spec=UdsMessageRecord,
                                   direction=TransmissionDirection.TRANSMITTED,
                                   packets_records=(Mock(spec=CanPacketRecord),))
        assert AbstractCanTransportInterface._update_n_bs_measured(self.mock_can_transport_interface,
                                                                   message_record=mock_message_record) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured is None

    @pytest.mark.parametrize("message_record, expected_n_bs_measurements", [
        (Mock(spec=UdsMessageRecord, direction=TransmissionDirection.TRANSMITTED, packets_records=(
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME,
                     transmission_time=datetime(year=1234, month=1, day=2)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=1234, month=1, day=2, microsecond=1000)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=1234, month=1, day=2, microsecond=3000)))),
         (1,)),
        (Mock(spec=UdsMessageRecord, direction=TransmissionDirection.TRANSMITTED, packets_records=(
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=12,
                                                microsecond=987654)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=154)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=57000)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=58954)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=58955)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=868955)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=14,
                                                microsecond=955)),
        )),
         (12.5, 56.846, 0.001)),
    ])
    def test_update_n_bs_measured__multiple_records(self, message_record, expected_n_bs_measurements):
        assert AbstractCanTransportInterface._update_n_bs_measured(self.mock_can_transport_interface,
                                                                   message_record=message_record) is None
        assert (self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured
                == expected_n_bs_measurements)

    # _update_n_cr_measured

    @pytest.mark.parametrize("message_record", [
        Mock(), "not a message"
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_cr_measured__type_error(self, mock_isinstance, message_record):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface._update_n_cr_measured(self.mock_can_transport_interface,
                                                                message_record=message_record)
        mock_isinstance.assert_called_once_with(message_record, UdsMessageRecord)

    @pytest.mark.parametrize("message_record", [
        Mock(direction=TransmissionDirection.TRANSMITTED), Mock(direction="not received")
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_update_n_cr_measured__value_error(self, mock_isinstance, message_record):
        mock_isinstance.return_value = True
        with pytest.raises(ValueError):
            AbstractCanTransportInterface._update_n_cr_measured(self.mock_can_transport_interface,
                                                                message_record=message_record)
        mock_isinstance.assert_called_once_with(message_record, UdsMessageRecord)

    def test_update_n_cr_measured__1_record(self):
        mock_message_record = Mock(spec=UdsMessageRecord,
                                   direction=TransmissionDirection.RECEIVED,
                                   packets_records=(Mock(spec=CanPacketRecord),))
        assert AbstractCanTransportInterface._update_n_cr_measured(self.mock_can_transport_interface,
                                                                   message_record=mock_message_record) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured is None

    @pytest.mark.parametrize("message, expected_n_cr_measurements", [
        (Mock(spec=UdsMessageRecord, direction=TransmissionDirection.RECEIVED, packets_records=(
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME,
                     transmission_time=datetime(year=1234, month=1, day=2)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=1234, month=1, day=2, microsecond=1000)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=1234, month=1, day=2, microsecond=3000)))),
         (2,)),
        (Mock(spec=UdsMessageRecord, direction=TransmissionDirection.RECEIVED, packets_records=(
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=12,
                                                microsecond=987654)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=154)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=57000)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=58954)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=58955)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=13,
                                                microsecond=868955)),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_time=datetime(year=2024, month=9, day=22, hour=14, minute=43, second=14,
                                                microsecond=955)),
        )),
         (1.954, 810.0, 132)),
    ])
    def test_update_n_cr_measured__multiple_records(self, message, expected_n_cr_measurements):
        assert AbstractCanTransportInterface._update_n_cr_measured(self.mock_can_transport_interface,
                                                                   message_record=message) is None
        assert (self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured
                == expected_n_cr_measurements)

    # clear_measurements

    def test_clear_measurements(self):
        assert AbstractCanTransportInterface.clear_measurements(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured is None

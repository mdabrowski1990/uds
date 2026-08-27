from random import randint

import pytest
from mock import MagicMock, Mock, call, patch

from uds.addressing import AddressingType
from uds.can import CanPacketRecord
from uds.can.transport_interface.common import (
    AbstractCanAddressingInformation,
    AbstractCanTransportInterface,
    AbstractEventLoop,
    AbstractFlowControlParametersGenerator,
    CanFlowStatus,
    CanPacket,
    CanPacketType,
    CanVersion,
    MessageTransmissionNotStartedError,
    TransmissionDirection,
    UdsMessage,
    UdsMessageRecord,
    async_sleep,
    perf_counter,
    sleep,
)

SCRIPT_LOCATION = "uds.can.transport_interface.common"


class TestAbstractCanTransportInterface:
    """Unit tests for `AbstractCanTransportInterface` class."""

    def setup_method(self):
        self.mock_can_transport_interface = Mock(spec=AbstractCanTransportInterface,
                                                 flow_control_parameters_generator=MagicMock())
        # patching
        self._patcher_abstract_transport_interface_init \
            = patch(f"{SCRIPT_LOCATION}.AbstractTransportInterface.__init__")
        self.mock_abstract_transport_interface_init = self._patcher_abstract_transport_interface_init.start()
        self._patcher_uds_message = patch(f"{SCRIPT_LOCATION}.UdsMessage")
        self.mock_uds_message = self._patcher_uds_message.start()
        self._patcher_validate_can_version = patch(f"{SCRIPT_LOCATION}.CanVersion.validate_member")
        self.mock_validate_can_version = self._patcher_validate_can_version.start()
        self._patcher_can_segmenter = patch(f"{SCRIPT_LOCATION}.CanSegmenter")
        self.mock_can_segmenter = self._patcher_can_segmenter.start()
        self._patcher_can_st_min_handler = patch(f"{SCRIPT_LOCATION}.CanSTminTranslator")
        self.mock_can_st_min_handler = self._patcher_can_st_min_handler.start()
        self._patcher_can_packet_type_is_initial_packet_type \
            = patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
        self.mock_can_packet_type_is_initial_packet_type = self._patcher_can_packet_type_is_initial_packet_type.start()
        self._patcher_min = patch(f"{SCRIPT_LOCATION}.min")
        self.mock_min = self._patcher_min.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_sleep = patch(f"{SCRIPT_LOCATION}.sleep")
        self.mock_sleep = self._patcher_sleep.start()
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_async_sleep = patch(f"{SCRIPT_LOCATION}.async_sleep")
        self.mock_async_sleep = self._patcher_async_sleep.start()
        self._patcher_get_running_loop = patch(f"{SCRIPT_LOCATION}.get_running_loop")
        self.mock_get_running_loop = self._patcher_get_running_loop.start()
        self._patcher_validate_time = patch(f"{SCRIPT_LOCATION}.validate_time")
        self.mock_validate_time = self._patcher_validate_time.start()
        self._patcher_validate_timeout = patch(f"{SCRIPT_LOCATION}.validate_timeout")
        self.mock_validate_timeout = self._patcher_validate_timeout.start()

    def teardown_method(self):
        self._patcher_abstract_transport_interface_init.stop()
        self._patcher_uds_message.stop()
        self._patcher_validate_can_version.stop()
        self._patcher_can_segmenter.stop()
        self._patcher_can_st_min_handler.stop()
        self._patcher_can_packet_type_is_initial_packet_type.stop()
        self._patcher_min.stop()
        self._patcher_warn.stop()
        self._patcher_sleep.stop()
        self._patcher_perf_counter.stop()
        self._patcher_async_sleep.stop()
        self._patcher_get_running_loop.stop()
        self._patcher_validate_time.stop()
        self._patcher_validate_timeout.stop()

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
        assert self.mock_can_transport_interface.can_version == CanVersion.CLASSIC_CAN
        assert self.mock_can_transport_interface.bitrate_switch == False
        self.mock_can_transport_interface.segmenter = self.mock_can_segmenter.return_value
        self.mock_abstract_transport_interface_init.assert_called_once_with(network_manager=network_manager)
        self.mock_can_segmenter.assert_called_once_with(addressing_information=addressing_information)

    @pytest.mark.parametrize("network_manager, addressing_information, "
                             "n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout, "
                             "flow_control_parameters_generator, can_version, bitrate_switch, segmenter_configuration", [
        (Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(),
         {"a": 1, "bc": 2, "def_xyz": Mock()})
    ])
    def test_init__all_args(self, network_manager, addressing_information,
                            n_as_timeout, n_ar_timeout, n_bs_timeout, n_br, n_cs, n_cr_timeout,
                            flow_control_parameters_generator, can_version, bitrate_switch, segmenter_configuration):
        assert AbstractCanTransportInterface.__init__(
            self.mock_can_transport_interface,
            network_manager=network_manager,
            addressing_information=addressing_information,
            n_as_timeout=n_as_timeout,
            n_ar_timeout=n_ar_timeout,
            n_bs_timeout=n_bs_timeout,
            n_br=n_br,
            n_cs=n_cs,
            n_cr_timeout=n_cr_timeout,
            flow_control_parameters_generator=flow_control_parameters_generator,
            can_version=can_version,
            bitrate_switch=bitrate_switch,
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
        assert self.mock_can_transport_interface.can_version == can_version
        assert self.mock_can_transport_interface.bitrate_switch == bitrate_switch
        self.mock_can_transport_interface.segmenter = self.mock_can_segmenter.return_value
        self.mock_abstract_transport_interface_init.assert_called_once_with(network_manager=network_manager)
        self.mock_can_segmenter.assert_called_once_with(addressing_information=addressing_information,
                                                        **segmenter_configuration)

    # segmenter

    def test_segmenter__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter = Mock()
        assert (AbstractCanTransportInterface.segmenter.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter)

    @pytest.mark.parametrize("value", [Mock(), "CAN Segmenter"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmenter__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.segmenter.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, self.mock_can_segmenter)

    @pytest.mark.parametrize("value", [Mock(), "CAN Segmenter"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_segmenter__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert AbstractCanTransportInterface.segmenter.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__segmenter == value
        mock_isinstance.assert_called_once_with(value, self.mock_can_segmenter)

    # can_version

    def test_can_version__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__can_version = Mock()
        assert AbstractCanTransportInterface.can_version.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface._AbstractCanTransportInterface__can_version

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_can_version__set(self, value):
        AbstractCanTransportInterface.can_version.fset(self.mock_can_transport_interface, value)
        assert (self.mock_can_transport_interface._AbstractCanTransportInterface__can_version
                == self.mock_validate_can_version.return_value)
        self.mock_validate_can_version.assert_called_once_with(value)

    # bitrate_switch
    
    def test_bitrate_switch__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__bitrate_switch = Mock()
        assert AbstractCanTransportInterface.bitrate_switch.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface._AbstractCanTransportInterface__bitrate_switch

    @pytest.mark.parametrize("value", [True, False, 1, 0])
    def test_bitrate_switch__set(self, value):
        AbstractCanTransportInterface.bitrate_switch.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__bitrate_switch == bool(value)

    # dlc

    def test_dlc__get(self):
        assert AbstractCanTransportInterface.dlc.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface.segmenter.dlc

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_dlc__set(self, value):
        AbstractCanTransportInterface.dlc.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface.segmenter.dlc == value

    # min_dlc

    def test_min_dlc__get(self):
        assert AbstractCanTransportInterface.min_dlc.fget(self.mock_can_transport_interface) \
               == self.mock_can_transport_interface.segmenter.min_dlc

    @pytest.mark.parametrize("value", ["something", Mock()])
    def test_min_dlc__set(self, value):
        AbstractCanTransportInterface.min_dlc.fset(self.mock_can_transport_interface, value)
        assert self.mock_can_transport_interface.segmenter.min_dlc == value

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
    def test_flow_control_parameters_generator__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanTransportInterface.flow_control_parameters_generator.fset(self.mock_can_transport_interface,
                                                                                 value)
        mock_isinstance.assert_called_once_with(value, AbstractFlowControlParametersGenerator)

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_flow_control_parameters_generator__set__valid(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert AbstractCanTransportInterface.flow_control_parameters_generator.fset(self.mock_can_transport_interface,
                                                                                    value) is None
        assert (self.mock_can_transport_interface._AbstractCanTransportInterface__flow_control_parameters_generator
                == value)
        mock_isinstance.assert_called_once_with(value, AbstractFlowControlParametersGenerator)

    # n_as

    def test_n_as_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout = Mock()
        assert (AbstractCanTransportInterface.n_as_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout)

    def test_n_as_timeout__set__valid_with_warning(self):
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AS_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_n_as_timeout__set__valid_without_warning(self):
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AS_TIMEOUT)
        self.mock_warn.assert_not_called()

    def test_n_as_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured = Mock()
        assert (AbstractCanTransportInterface.n_as_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured)

    # n_ar

    def test_n_ar_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout = Mock()
        assert (AbstractCanTransportInterface.n_ar_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout)

    def test_n_ar_timeout__set__valid_with_warning(self):
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AR_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_n_ar_timeout__set__valid_without_warning(self):
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_AR_TIMEOUT)
        self.mock_warn.assert_not_called()

    def test_n_ar_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured = Mock()
        assert (AbstractCanTransportInterface.n_ar_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured)

    # n_bs

    def test_n_bs_timeout__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout = Mock()
        assert (AbstractCanTransportInterface.n_bs_timeout.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout)

    def test_n_bs_timeout__set__valid_with_warning(self):
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_BS_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_n_bs_timeout__set__valid_without_warning(self):
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_BS_TIMEOUT)
        self.mock_warn.assert_not_called()

    def test_n_bs_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured = Mock()
        assert (AbstractCanTransportInterface.n_bs_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_bs_measured)

    # n_br

    def test_n_br__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_br = Mock()
        assert (AbstractCanTransportInterface.n_br.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_br)


    @pytest.mark.parametrize("value, max_value", [
        (901, 900.5),
        (450.1, 450),
    ])
    def test_n_br__set__value_error(self,value, max_value):
        self.mock_can_transport_interface.n_br_max = max_value
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_br.fset(self.mock_can_transport_interface, value)
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)

    @pytest.mark.parametrize("value, max_value", [
        (899.99, 900),
        (0, 450),
    ])
    def test_n_br__set__valid(self, value, max_value):
        self.mock_can_transport_interface.n_br_max = max_value
        assert AbstractCanTransportInterface.n_br.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_br == value
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)

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

    @pytest.mark.parametrize("value, max_value", [
        (901, 900.5),
        (450.1, 450),
    ])
    def test_n_cs__set__value_error(self, value, max_value):
        self.mock_can_transport_interface.n_cs_max = max_value
        with pytest.raises(ValueError):
            AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, value)
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)

    @pytest.mark.parametrize("value, max_value", [
        (899.99, 900),
        (0, 450),
    ])
    def test_n_cs__set__valid(self, value, max_value):
        self.mock_can_transport_interface.n_cs_max = max_value
        assert AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs == value
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)

    def test_n_cs__set__none(self):
        assert AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, None) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cs is None
        self.mock_validate_time.assert_not_called()

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

    def test_n_cr_timeout__set__valid_with_warning(self):
        mock_ne = Mock(return_value=True)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_CR_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_n_cr_timeout__set__valid_without_warning(self):
        mock_ne = Mock(return_value=False)
        mock_value = MagicMock(__ne__=mock_ne)
        assert AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, mock_value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_timeout == mock_value
        self.mock_validate_time.assert_called_once_with(mock_value, accept_zero=False)
        mock_ne.assert_called_once_with(self.mock_can_transport_interface.N_CR_TIMEOUT)
        self.mock_warn.assert_not_called()

    def test_n_cr_measured__get(self):
        self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured = Mock()
        assert (AbstractCanTransportInterface.n_cr_measured.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._AbstractCanTransportInterface__n_cr_measured)

    # _update_n_ar_measured

    @pytest.mark.parametrize("value", [0, AbstractCanTransportInterface.N_AR_TIMEOUT])
    def test_update_n_ar_measured__valid_without_warning(self, value):
        self.mock_can_transport_interface.n_ar_timeout = AbstractCanTransportInterface.N_AR_TIMEOUT
        assert AbstractCanTransportInterface._update_n_ar_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured == value
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("value, n_ar_timeout", [
        (AbstractCanTransportInterface.N_AR_TIMEOUT + 1, AbstractCanTransportInterface.N_AR_TIMEOUT),
        (AbstractCanTransportInterface.N_AR_TIMEOUT - 1, AbstractCanTransportInterface.N_AR_TIMEOUT // 2),
    ])
    def test_update_n_ar_measured__valid_with_warning(self, value, n_ar_timeout):
        self.mock_can_transport_interface.n_ar_timeout = n_ar_timeout
        assert AbstractCanTransportInterface._update_n_ar_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_ar_measured == value
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)
        self.mock_warn.assert_called_once()
        
    # _update_n_as_measured

    @pytest.mark.parametrize("value", [0, AbstractCanTransportInterface.N_AS_TIMEOUT])
    def test_update_n_as_measured__valid_without_warning(self, value):
        self.mock_can_transport_interface.n_as_timeout = AbstractCanTransportInterface.N_AS_TIMEOUT
        assert AbstractCanTransportInterface._update_n_as_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured == value
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("value, n_as_timeout", [
        (AbstractCanTransportInterface.N_AS_TIMEOUT + 1, AbstractCanTransportInterface.N_AS_TIMEOUT),
        (AbstractCanTransportInterface.N_AS_TIMEOUT - 1, AbstractCanTransportInterface.N_AS_TIMEOUT // 2),
    ])
    def test_update_n_as_measured__valid_with_warning(self, value, n_as_timeout):
        self.mock_can_transport_interface.n_as_timeout = n_as_timeout
        assert AbstractCanTransportInterface._update_n_as_measured(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._AbstractCanTransportInterface__n_as_measured == value
        self.mock_validate_time.assert_called_once_with(value, accept_zero=True)
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
                     transmission_timestamp=0.000),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=0.001),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=0.002))),
         (1,)),
        (Mock(spec=UdsMessageRecord, direction=TransmissionDirection.TRANSMITTED, packets_records=(
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME,
                     transmission_timestamp=1.234),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=1.5675),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=2.111),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=2.222),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=2.234),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=2.567),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=2.999),
        )),
         (333.5, 543.5, 12)),
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
                     transmission_timestamp=0.1),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=0.2),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=0.4))),
         (200,)),
        (Mock(spec=UdsMessageRecord, direction=TransmissionDirection.RECEIVED, packets_records=(
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME,
                     transmission_timestamp=0.123456),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=0.789012),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=0.345678),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=0.901234),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.FLOW_CONTROL,
                     transmission_timestamp=1.111111),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=1.223344),
                Mock(spec=CanPacketRecord, packet_type=CanPacketType.CONSECUTIVE_FRAME,
                     transmission_timestamp=1.5566772),
        )),
         (555.556, 112.233, 333.333)),
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

    # _send_cf_packets_block

    @pytest.mark.parametrize("packets, delay", [
        ([Mock(spec=CanPacket), Mock(spec=CanPacket)], 0),
        ([Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)], 12.34),
    ])
    def test_send_cf_packets_block(self, packets, delay):
        mock_fc_timestamp_gt = Mock(return_value=False)
        mock_cf_timestamp_gt = Mock(return_value=True)
        mock_fc_transmission_timestamp = MagicMock(__add__=lambda this, other: this,
                                                   __sub__=lambda this, other: this,
                                                   __gt__=mock_fc_timestamp_gt)
        mock_cf_transmission_timestamp = MagicMock(__add__=lambda this, other: this,
                                                   __sub__=lambda this, other: this,
                                                   __gt__=mock_cf_timestamp_gt)
        packet_records = tuple(MagicMock(spec=CanPacketRecord,
                                         transmission_timestamp=mock_cf_transmission_timestamp)
                               for _ in packets)
        self.mock_can_transport_interface.send_packet.side_effect = packet_records
        assert (AbstractCanTransportInterface._send_cf_packets_block
                (self.mock_can_transport_interface,
                 cf_packets_block=packets,
                 fc_transmission_timestamp=mock_fc_transmission_timestamp,
                 delay=delay) == packet_records)
        self.mock_can_transport_interface.send_packet.assert_has_calls(
            [call(packet) for packet in packets], any_order=False)
        mock_fc_timestamp_gt.assert_called_once_with(0)
        mock_cf_timestamp_gt.assert_has_calls([call(0)] * len(packets[1:]))
        self.mock_sleep.assert_called()
        self.mock_async_sleep.assert_not_called()

    # _async_send_cf_packets_block

    @pytest.mark.parametrize("packets, delay", [
        ([Mock(spec=CanPacket), Mock(spec=CanPacket)], 0),
        ([Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)], 12.34),
    ])
    @pytest.mark.asyncio
    async def test_async_send_cf_packets_block(self, packets, delay):
        mock_loop = Mock()
        mock_fc_timestamp_gt = Mock(return_value=False)
        mock_cf_timestamp_gt = Mock(return_value=True)
        mock_fc_transmission_timestamp = MagicMock(__add__=lambda this, other: this,
                                                   __sub__=lambda this, other: this,
                                                   __gt__=mock_fc_timestamp_gt)
        mock_cf_transmission_timestamp = MagicMock(__add__=lambda this, other: this,
                                                   __sub__=lambda this, other: this,
                                                   __gt__=mock_cf_timestamp_gt)
        packet_records = tuple(MagicMock(spec=CanPacketRecord,
                                         transmission_timestamp=mock_cf_transmission_timestamp)
                               for _ in packets)
        self.mock_can_transport_interface.async_send_packet.side_effect = packet_records
        assert await AbstractCanTransportInterface._async_send_cf_packets_block(
            self.mock_can_transport_interface,
            cf_packets_block=packets,
            delay=delay,
            fc_transmission_timestamp=mock_fc_transmission_timestamp,
            loop=mock_loop) == packet_records
        self.mock_can_transport_interface.async_send_packet.assert_has_calls(
            [call(packet, loop=mock_loop) for packet in packets], any_order=False)
        mock_fc_timestamp_gt.assert_called_once_with(0)
        mock_cf_timestamp_gt.assert_has_calls([call(0)] * len(packets[1:]))
        self.mock_sleep.assert_not_called()
        self.mock_async_sleep.assert_called()

# _receive_cf_packets_block

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (Mock(), Mock(), 1, MagicMock(__sub__=lambda this, other: this,
                                      __mul__=lambda this, other: this,
                                      __le__=Mock(return_value=False))),
        (Mock(), Mock(), 987, None),
    ])
    def test_receive_cf_packets_block__timeout__n_cr(self, sequence_number, block_size,
                                                     remaining_data_length, timestamp_end):
        mock_is_n_cr_timeout_reached = Mock(side_effect=(False, True))
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=Mock(return_value=False))
        self.mock_can_transport_interface.n_cr_timeout = MagicMock(__sub__=lambda this, other: this,
                                                                   __add__=lambda this, other: this,
                                                                   __mul__=lambda this, other: this,
                                                                   __le__=mock_is_n_cr_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        with pytest.raises(TimeoutError):
            AbstractCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                  sequence_number=sequence_number,
                                                                  block_size=block_size,
                                                                  remaining_data_length=remaining_data_length,
                                                                  timestamp_end=timestamp_end)
        assert mock_is_n_cr_timeout_reached.call_count == 2
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(timeout=self.mock_min.return_value)
        self.mock_can_transport_interface._message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (Mock(), Mock(), 1, MagicMock(__sub__=lambda this, other: this,
                                      __mul__=lambda this, other: this,
                                      __le__=Mock(return_value=True))),
        (Mock(), Mock(), 987, MagicMock(__sub__=lambda this, other: this,
                                        __mul__=lambda this, other: this,
                                        __le__=Mock(side_effect=(False, True)))),
    ])
    def test_receive_cf_packets_block__timeout__end(self, sequence_number, block_size,
                                                    remaining_data_length, timestamp_end):
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        with pytest.raises(TimeoutError):
            AbstractCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                  sequence_number=sequence_number,
                                                                  block_size=block_size,
                                                                  remaining_data_length=remaining_data_length,
                                                                  timestamp_end=timestamp_end)
        self.mock_can_transport_interface._message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (Mock(), Mock(), 1, MagicMock(__sub__=lambda this, other: this,
                                      __mul__=lambda this, other: this,
                                      __le__=Mock(return_value=False))),
        (Mock(), Mock(), 987, None),
    ])
    def test_receive_cf_packets_block__initial_packet(self, sequence_number, block_size,
                                                      remaining_data_length, timestamp_end):
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (AbstractCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                      sequence_number=sequence_number,
                                                                      block_size=block_size,
                                                                      remaining_data_length=remaining_data_length,
                                                                      timestamp_end=timestamp_end)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_min.return_value)
        self.mock_can_packet_type_is_initial_packet_type.assert_called_once_with(
            self.mock_can_transport_interface.receive_packet.return_value.packet_type)
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value,
            timestamp_end=timestamp_end)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (1, 1, 1, MagicMock(__sub__=lambda this, other: this,
                            __mul__=lambda this, other: this,
                            __le__=Mock(return_value=False))),
        (13, 5, 987, None),
    ])
    def test_receive_cf_packets_block__cf_block(self, sequence_number, block_size, remaining_data_length,
                                                timestamp_end):
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        packet_sequence = [
            Mock(spec=CanPacketRecord,
                 packet_type=CanPacketType.CONSECUTIVE_FRAME,
                 sequence_number=(sequence_number + i) & 0xF,
                 payload=[])
            for i in range(block_size)
        ]
        self.mock_can_transport_interface.receive_packet.side_effect = packet_sequence[:]
        assert (AbstractCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                      sequence_number=sequence_number,
                                                                      block_size=block_size,
                                                                      remaining_data_length=remaining_data_length,
                                                                      timestamp_end=timestamp_end)
                == tuple(packet_sequence))
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            [call(timeout=self.mock_min.return_value)] * block_size)
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([
            call(packet.packet_type) for packet in packet_sequence])
        self.mock_can_transport_interface._message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, remaining_data_length, payload, timestamp_end", [
        (1, 1, [0x12], MagicMock(__sub__=lambda this, other: this,
                                 __mul__=lambda this, other: this,
                                 __le__=Mock(return_value=False))),
        (13, 987, [*range(100, 162)], None),
    ])
    def test_receive_cf_packets_block__remaining_payload(self, sequence_number, remaining_data_length, payload,
                                                         timestamp_end):
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        packet_sequence = [
            Mock(spec=CanPacketRecord,
                 packet_type=CanPacketType.CONSECUTIVE_FRAME,
                 sequence_number=(sequence_number + i) & 0xF,
                 payload=payload)
            for i in range(remaining_data_length // len(payload) + bool(remaining_data_length % len(payload)))
        ]
        self.mock_can_transport_interface.receive_packet.side_effect = packet_sequence[:]
        assert (AbstractCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                      sequence_number=sequence_number,
                                                                      block_size=0,
                                                                      remaining_data_length=remaining_data_length,
                                                                      timestamp_end=timestamp_end)
                == tuple(packet_sequence))
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            [call(timeout=self.mock_min.return_value)] * len(packet_sequence))
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([
            call(packet.packet_type) for packet in packet_sequence])
        self.mock_can_transport_interface._message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    # _async_receive_cf_packets_block

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (Mock(), Mock(), 1, MagicMock(__sub__=lambda this, other: this,
                                      __mul__=lambda this, other: this,
                                      __le__=Mock(return_value=False))),
        (Mock(), Mock(), 987, None),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__timeout__n_cr(self, sequence_number, block_size,
                                                                 remaining_data_length, timestamp_end):
        mock_loop = Mock()
        mock_is_n_cr_timeout_reached = Mock(side_effect=(False, True))
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=Mock(return_value=False))
        self.mock_can_transport_interface.n_cr_timeout = MagicMock(__sub__=lambda this, other: this,
                                                                   __add__=lambda this, other: this,
                                                                   __mul__=lambda this, other: this,
                                                                   __le__=mock_is_n_cr_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        with pytest.raises(TimeoutError):
            await AbstractCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
                                                                              sequence_number=sequence_number,
                                                                              block_size=block_size,
                                                                              remaining_data_length=remaining_data_length,
                                                                              timestamp_end=timestamp_end,
                                                                              loop=mock_loop)
        assert mock_is_n_cr_timeout_reached.call_count == 2
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_min.return_value,
            loop=mock_loop)
        self.mock_can_transport_interface._async_message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (Mock(), Mock(), 1, MagicMock(__sub__=lambda this, other: this,
                                      __mul__=lambda this, other: this,
                                      __le__=Mock(return_value=True))),
        (Mock(), Mock(), 987, MagicMock(__sub__=lambda this, other: this,
                                        __mul__=lambda this, other: this,
                                        __le__=Mock(side_effect=(False, True)))),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__timeout__end(self, sequence_number, block_size,
                                                                remaining_data_length, timestamp_end):
        mock_loop = Mock()
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        with pytest.raises(TimeoutError):
            await AbstractCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
                                                                              sequence_number=sequence_number,
                                                                              block_size=block_size,
                                                                              remaining_data_length=remaining_data_length,
                                                                              timestamp_end=timestamp_end,
                                                                              loop=mock_loop)
        self.mock_can_transport_interface._async_message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (Mock(), Mock(), 1, MagicMock(__sub__=lambda this, other: this,
                                      __mul__=lambda this, other: this,
                                      __le__=Mock(return_value=False))),
        (Mock(), Mock(), 987, None),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__initial_packet(self, sequence_number, block_size,
                                                                  remaining_data_length, timestamp_end):
        mock_loop = Mock()
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (await AbstractCanTransportInterface._async_receive_cf_packets_block(
            self.mock_can_transport_interface,
            sequence_number=sequence_number,
            block_size=block_size,
            remaining_data_length=remaining_data_length,
            timestamp_end=timestamp_end,
            loop=mock_loop)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_min.return_value,
            loop=mock_loop)
        self.mock_can_packet_type_is_initial_packet_type.assert_called_once_with(
            self.mock_can_transport_interface.async_receive_packet.return_value.packet_type)
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value,
            timestamp_end=timestamp_end,
            loop=mock_loop)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length, timestamp_end", [
        (1, 1, 1, MagicMock(__sub__=lambda this, other: this,
                            __mul__=lambda this, other: this,
                            __le__=Mock(return_value=False))),
        (13, 5, 987, None),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__cf_block(self, sequence_number, block_size,
                                                            remaining_data_length, timestamp_end):
        mock_loop = Mock()
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        packet_sequence = [
            Mock(spec=CanPacketRecord,
                 packet_type=CanPacketType.CONSECUTIVE_FRAME,
                 sequence_number=(sequence_number + i) & 0xF,
                 payload=[])
            for i in range(block_size)
        ]
        self.mock_can_transport_interface.async_receive_packet.side_effect = packet_sequence[:]
        assert (await AbstractCanTransportInterface._async_receive_cf_packets_block(
            self.mock_can_transport_interface,
            sequence_number=sequence_number,
            block_size=block_size,
            remaining_data_length=remaining_data_length,
            timestamp_end=timestamp_end,
            loop=mock_loop) == tuple(packet_sequence))
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            [call(timeout=self.mock_min.return_value,
                  loop=mock_loop)] * block_size)
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([call(packet.packet_type)
                                                                           for packet in packet_sequence])
        self.mock_can_transport_interface._async_message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, remaining_data_length, payload, timestamp_end", [
        (1, 1, [0x12], MagicMock(__sub__=lambda this, other: this,
                                 __mul__=lambda this, other: this,
                                 __le__=Mock(return_value=False))),
        (13, 987, [*range(100, 162)], None),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__remaining_payload(self, sequence_number, remaining_data_length,
                                                                     payload, timestamp_end):
        mock_loop = Mock()
        self.mock_perf_counter.return_value = self.mock_can_transport_interface.n_cr_timeout = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=Mock(return_value=False))
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        packet_sequence = [
            Mock(spec=CanPacketRecord,
                 packet_type=CanPacketType.CONSECUTIVE_FRAME,
                 sequence_number=(sequence_number + i) & 0xF,
                 payload=payload)
            for i in range(remaining_data_length // len(payload) + bool(remaining_data_length % len(payload)))
        ]
        self.mock_can_transport_interface.async_receive_packet.side_effect = packet_sequence[:]
        assert (await AbstractCanTransportInterface._async_receive_cf_packets_block(
            self.mock_can_transport_interface,
            sequence_number=sequence_number,
            block_size=0,
            remaining_data_length=remaining_data_length,
            timestamp_end=timestamp_end,
            loop=mock_loop) == tuple(packet_sequence))
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            [call(timeout=self.mock_min.return_value,
                  loop=mock_loop)] * len(packet_sequence))
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([call(packet.packet_type)
                                                                           for packet in packet_sequence])
        self.mock_can_transport_interface._async_message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()
        
    # _receive_consecutive_frames

    def test_receive_consecutive_frames__timeout(self):
        mock_is_timeout_reached = Mock(return_value=True)
        mock_timestamp_end = MagicMock(__sub__=lambda this, other: this,
                                       __mul__=lambda this, other: this,
                                       __lt__=mock_is_timeout_reached)
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                transmission_time=Mock(timestamp=MagicMock()))
        with pytest.raises(TimeoutError):
            AbstractCanTransportInterface._receive_consecutive_frames(self.mock_can_transport_interface,
                                                                    first_frame=mock_first_frame,
                                                                    timestamp_end=mock_timestamp_end)
        self.mock_can_transport_interface.receive_packet.assert_not_called()
        self.mock_can_transport_interface.send_packet.assert_not_called()

    @pytest.mark.parametrize("timestamp_end", [MagicMock(__sub__=lambda this, other: this,
                                                         __mul__=lambda this, other: this,
                                                         __lt__=Mock(return_value=False)),
                                               None])
    def test_receive_consecutive_frames__new_message_interrupted(self, timestamp_end):
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                transmission_time=Mock(timestamp=MagicMock()))
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=True))
        assert (AbstractCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                        first_frame=mock_first_frame,
                                                                        timestamp_end=timestamp_end)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value,
            timestamp_end=timestamp_end)
        self.mock_can_transport_interface.receive_packet.assert_called_once()
        self.mock_can_transport_interface.send_packet.assert_not_called()
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("timestamp_end", [MagicMock(__sub__=lambda this, other: this,
                                                         __mul__=lambda this, other: this,
                                                         __lt__=Mock(return_value=False)),
                                               None])
    def test_receive_consecutive_frames__overflow(self, timestamp_end):
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                transmission_time=Mock(timestamp=MagicMock()))
        self.mock_can_transport_interface.flow_control_parameters_generator = [(CanFlowStatus.Overflow, None, None)]
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=False))
        with pytest.raises(OverflowError):
            AbstractCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                    first_frame=mock_first_frame,
                                                                    timestamp_end=timestamp_end)
        self.mock_can_transport_interface.receive_packet.assert_not_called()
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_called_once_with(
            flow_status=CanFlowStatus.Overflow,
            block_size=None,
            st_min=None)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(
            self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("block_size, st_min, timestamp_end", [
        (0, 127, None),
        (Mock(), Mock(), MagicMock(__sub__=lambda this, other: this,
                                   __mul__=lambda this, other: this,
                                   __lt__=Mock(return_value=False)))
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_consecutive_frames__wait_then_receive_message(self, mock_isinstance, mock_uds_message_record,
                                                                   block_size, st_min, timestamp_end):
        mock_isinstance.return_value = True
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                data_length=MagicMock())
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.Wait, None, None),
            (CanFlowStatus.ContinueToSend, block_size, st_min)]
        self.mock_can_transport_interface.receive_packet.side_effect = TimeoutError
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=True))
        assert (AbstractCanTransportInterface._receive_consecutive_frames(self.mock_can_transport_interface,
                                                                        first_frame=mock_first_frame,
                                                                        timestamp_end=timestamp_end)
                == self.mock_can_transport_interface._receive_cf_packets_block.return_value)
        assert self.mock_can_transport_interface.receive_packet.call_count == 2
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_has_calls(
            [call(flow_status=CanFlowStatus.Wait, block_size=None, st_min=None),
             call(flow_status=CanFlowStatus.ContinueToSend, block_size=block_size, st_min=st_min)])
        self.mock_can_transport_interface.send_packet.assert_has_calls(
            [call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value),
             call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value)],
            any_order=True)
        self.mock_can_transport_interface._receive_cf_packets_block.assert_called_once()
        mock_isinstance.assert_called_once_with(
            self.mock_can_transport_interface._receive_cf_packets_block.return_value,
            mock_uds_message_record)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize(
        "data_length, ff_payload, cf_blocks, sequence_numbers, remaining_data_lengths, timestamp_end", [
            (8, [0x12, 0x34], [[Mock(spec=CanPacketRecord, payload=[0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])]], [1], [6],
             None),
            (68, [0x98],
             [[Mock(spec=CanPacketRecord, payload=list(range(60, 67)), sequence_number=2 * i + j + (i % 3 == 0))
               for j in range(1 + i)] for i in range(4)], [1, 2, 4, 7], [67, 60, 46, 25],
             MagicMock(__sub__=lambda this, other: this,
                       __mul__=lambda this, other: this,
                       __lt__=Mock(return_value=False))),
        ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_consecutive_frames__cf_received(self, mock_isinstance, mock_uds_message_record,
                                                     data_length, ff_payload, cf_blocks,
                                                     sequence_numbers, remaining_data_lengths, timestamp_end):
        mock_st_min = Mock()
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=ff_payload,
                                data_length=data_length)
        mock_isinstance.return_value = False
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=True))
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.ContinueToSend, len(cf_block), mock_st_min) for cf_block in cf_blocks]
        self.mock_can_transport_interface._receive_cf_packets_block.side_effect = cf_blocks
        assert (AbstractCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                        first_frame=mock_first_frame,
                                                                        timestamp_end=timestamp_end)
                == mock_uds_message_record.return_value)
        assert self.mock_can_transport_interface.receive_packet.call_count == len(cf_blocks)
        self.mock_can_transport_interface._receive_cf_packets_block.assert_has_calls(
            [call(sequence_number=sequence_numbers[i],
                  block_size=len(cf_block),
                  remaining_data_length=remaining_data_lengths[i],
                  timestamp_end=timestamp_end)
             for i, cf_block in enumerate(cf_blocks)])
        all_packets = [mock_first_frame]
        for cf_block in cf_blocks:
            all_packets.append(self.mock_can_transport_interface.send_packet.return_value)
            all_packets.extend(cf_block)
        mock_uds_message_record.assert_called_once_with(all_packets)
        mock_isinstance.assert_called()
        self.mock_warn.assert_not_called()

    # _async_receive_consecutive_frames

    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__timeout(self):
        mock_loop = Mock()
        mock_is_timeout_reached = Mock(return_value=True)
        mock_timestamp_end = MagicMock(__sub__=lambda this, other: this,
                                       __mul__=lambda this, other: this,
                                       __lt__=mock_is_timeout_reached)
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                transmission_time=Mock(timestamp=MagicMock()))
        with pytest.raises(TimeoutError):
            await AbstractCanTransportInterface._async_receive_consecutive_frames(self.mock_can_transport_interface,
                                                                                first_frame=mock_first_frame,
                                                                                timestamp_end=mock_timestamp_end,
                                                                                loop=mock_loop)
        self.mock_can_transport_interface.async_receive_packet.assert_not_called()
        self.mock_can_transport_interface.async_send_packet.assert_not_called()

    @pytest.mark.parametrize("timestamp_end", [MagicMock(__sub__=lambda this, other: this,
                                                         __mul__=lambda this, other: this,
                                                         __lt__=Mock(return_value=False)),
                                               None])
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__new_message_interrupted(self, timestamp_end):
        mock_loop = Mock()
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                transmission_time=Mock(timestamp=MagicMock()))
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=True))
        assert (await AbstractCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                    first_frame=mock_first_frame,
                                                                                    timestamp_end=timestamp_end,
                                                                                    loop=mock_loop)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value,
            timestamp_end=timestamp_end,
            loop=mock_loop)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once()
        self.mock_can_transport_interface.async_send_packet.assert_not_called()
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("timestamp_end", [MagicMock(__sub__=lambda this, other: this,
                                                         __mul__=lambda this, other: this,
                                                         __lt__=Mock(return_value=False)),
                                               None])
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__overflow(self, timestamp_end):
        mock_loop = Mock()
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                transmission_time=Mock(timestamp=MagicMock()))
        self.mock_can_transport_interface.flow_control_parameters_generator = [(CanFlowStatus.Overflow, None, None)]
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=False))
        with pytest.raises(OverflowError):
            await AbstractCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                first_frame=mock_first_frame,
                                                                                timestamp_end=timestamp_end,
                                                                                loop=mock_loop)
        self.mock_can_transport_interface.async_receive_packet.assert_not_called()
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_called_once_with(
            flow_status=CanFlowStatus.Overflow,
            block_size=None,
            st_min=None)
        self.mock_can_transport_interface.async_send_packet.assert_called_once_with(
            self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value,
            loop=mock_loop)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("block_size, st_min, timestamp_end", [
        (0, 127, None),
        (Mock(), Mock(), MagicMock(__sub__=lambda this, other: this,
                                   __mul__=lambda this, other: this,
                                   __lt__=Mock(return_value=False)))
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__wait_then_receive_message(self, mock_isinstance, mock_uds_message_record,
                                                                               block_size, st_min, timestamp_end):
        mock_loop = Mock()
        mock_isinstance.return_value = True
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=[],
                                data_length=MagicMock())
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.Wait, None, None),
            (CanFlowStatus.ContinueToSend, block_size, st_min)]
        self.mock_can_transport_interface.async_receive_packet.side_effect = TimeoutError
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=True))
        assert (await AbstractCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                    first_frame=mock_first_frame,
                                                                                    timestamp_end=timestamp_end,
                                                                                    loop=mock_loop)
                == self.mock_can_transport_interface._async_receive_cf_packets_block.return_value)
        assert self.mock_can_transport_interface.async_receive_packet.call_count == 2
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_has_calls(
            [call(flow_status=CanFlowStatus.Wait, block_size=None, st_min=None),
             call(flow_status=CanFlowStatus.ContinueToSend, block_size=block_size, st_min=st_min)])
        self.mock_can_transport_interface.async_send_packet.assert_has_calls(
            [call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value, loop=mock_loop),
             call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value, loop=mock_loop)],
            any_order=True)
        self.mock_can_transport_interface._async_receive_cf_packets_block.assert_called_once()
        mock_isinstance.assert_called_once_with(
            self.mock_can_transport_interface._async_receive_cf_packets_block.return_value,
            mock_uds_message_record)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize(
        "data_length, ff_payload, cf_blocks, sequence_numbers, remaining_data_lengths, timestamp_end", [
            (8, [0x12, 0x34], [[Mock(spec=CanPacketRecord, payload=[0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])]], [1], [6],
             None),
            (68, [0x98],
             [[Mock(spec=CanPacketRecord, payload=list(range(60, 67)), sequence_number=2 * i + j + (i % 3 == 0))
               for j in range(1 + i)] for i in range(4)], [1, 2, 4, 7], [67, 60, 46, 25],
             MagicMock(__sub__=lambda this, other: this,
                       __mul__=lambda this, other: this,
                       __lt__=Mock(return_value=False))),
        ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__cf_received(self, mock_isinstance, mock_uds_message_record,
                                                                 data_length, ff_payload, cf_blocks,
                                                                 sequence_numbers, remaining_data_lengths,
                                                                 timestamp_end):
        mock_loop = Mock()
        mock_st_min = Mock()
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=ff_payload,
                                data_length=data_length)
        mock_isinstance.return_value = False
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.n_br = MagicMock(__sub__=lambda this, other: this,
                                                           __gt__=Mock(return_value=True))
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.ContinueToSend, len(cf_block), mock_st_min) for cf_block in cf_blocks]
        self.mock_can_transport_interface._async_receive_cf_packets_block.side_effect = cf_blocks
        assert (await AbstractCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                    first_frame=mock_first_frame,
                                                                                    timestamp_end=timestamp_end,
                                                                                    loop=mock_loop)
                == mock_uds_message_record.return_value)
        assert self.mock_can_transport_interface.async_receive_packet.call_count == len(cf_blocks)
        self.mock_can_transport_interface._async_receive_cf_packets_block.assert_has_calls(
            [call(sequence_number=sequence_numbers[i],
                  block_size=len(cf_block),
                  remaining_data_length=remaining_data_lengths[i],
                  timestamp_end=timestamp_end,
                  loop=mock_loop) for i, cf_block in enumerate(cf_blocks)])
        all_packets = [mock_first_frame]
        for cf_block in cf_blocks:
            all_packets.append(self.mock_can_transport_interface.async_send_packet.return_value)
            all_packets.extend(cf_block)
        mock_uds_message_record.assert_called_once_with(all_packets)
        mock_isinstance.assert_called()
        self.mock_warn.assert_not_called()
        
    # _message_receive_start

    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    def test_message_receive_start__sf(self, mock_uds_message_record):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        assert (AbstractCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                                   initial_packet=mock_packet,
                                                                   timestamp_end=Mock())
                == mock_uds_message_record.return_value)
        mock_uds_message_record.assert_called_once_with([mock_packet])

    def test_message_receive_start__ff(self):
        mock_timestamp_end = Mock()
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME)
        assert (AbstractCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                                   initial_packet=mock_packet,
                                                                   timestamp_end=mock_timestamp_end)
                == self.mock_can_transport_interface._receive_consecutive_frames.return_value)
        self.mock_can_transport_interface._receive_consecutive_frames.assert_called_once_with(
            first_frame=mock_packet,
            timestamp_end=mock_timestamp_end)

    @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, None])
    def test_message_receive_start__other(self, packet_type):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=packet_type)
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                               initial_packet=mock_packet,
                                                               timestamp_end=Mock())

    # _async_message_receive_start

    @pytest.mark.asyncio
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    async def test_async_message_receive_start__sf(self, mock_uds_message_record):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        assert (await AbstractCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                               initial_packet=mock_packet,
                                                                               timestamp_end=Mock(),
                                                                               loop=Mock())
                == mock_uds_message_record.return_value)
        mock_uds_message_record.assert_called_once_with([mock_packet])

    @pytest.mark.asyncio
    async def test_async_message_receive_start__ff(self):
        mock_loop = Mock()
        mock_timestamp_end = Mock()
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME)
        assert (await AbstractCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                               initial_packet=mock_packet,
                                                                               timestamp_end=mock_timestamp_end,
                                                                               loop=mock_loop)
                == self.mock_can_transport_interface._async_receive_consecutive_frames.return_value)
        self.mock_can_transport_interface._async_receive_consecutive_frames.assert_called_once_with(
            first_frame=mock_packet,
            timestamp_end=mock_timestamp_end,
            loop=mock_loop)

    @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, None])
    @pytest.mark.asyncio
    async def test_async_message_receive_start__other(self, packet_type):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=packet_type)
        with pytest.raises(NotImplementedError):
            await AbstractCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                           initial_packet=mock_packet,
                                                                           timestamp_end=Mock(),
                                                                           loop=Mock())

    # send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    def test_send_message__single_frame(self, mock_uds_message_record,
                                        message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        assert AbstractCanTransportInterface.send_message(self.mock_can_transport_interface,
                                                        message) == mock_uds_message_record.return_value
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(mock_segmented_message[0])
        mock_uds_message_record.assert_called_once_with(
            [self.mock_can_transport_interface.send_packet.return_value])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message, st_min", [
        (MagicMock(spec=UdsMessage,
                   payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
                   addressing_type=AddressingType.PHYSICAL),
         0x00),
        (MagicMock(spec=UdsMessage,
                   payload=[0x3E, 0x80],
                   addressing_type=AddressingType.PHYSICAL),
         0xFF),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    def test_send_message__multiple_packets__st_min__block_size_0(self, mock_uds_message_record,
                                                                  message, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        self.mock_can_transport_interface.n_cs = None
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0,
                                        st_min=st_min)
        self.mock_can_transport_interface._wait_for_flow_control = Mock(return_value=mock_flow_control_record)
        mock_sent_packet_records = [Mock(spec=CanPacketRecord)] * 20
        self.mock_can_transport_interface._send_cf_packets_block.return_value = mock_sent_packet_records
        assert (AbstractCanTransportInterface.send_message(self.mock_can_transport_interface, message)
                == mock_uds_message_record.return_value)
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_called_once_with(
            timeout_timestamp=mock_add_ff_timestamp.return_value)
        self.mock_can_transport_interface._send_cf_packets_block.assert_called_once_with(
            cf_packets_block=mock_segmented_message[1:],
            delay=self.mock_can_st_min_handler.decode.return_value,
            fc_transmission_timestamp=mock_flow_control_record.transmission_timestamp)
        self.mock_can_st_min_handler.decode.assert_called_once_with(st_min)
        mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record,
            *mock_sent_packet_records
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message, n_cs, st_min", [
        (Mock(spec=UdsMessage,
              payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
              addressing_type=AddressingType.PHYSICAL),
         0, 0xFF),
        (Mock(spec=UdsMessage,
              payload=[0x3E, 0x80],
              addressing_type=AddressingType.PHYSICAL),
         5, 0x00),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    def test_send_message__multiple_packets__n_cs__block_size_1(self, mock_uds_message_record,
                                                                message, n_cs, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        self.mock_can_transport_interface.n_cs = n_cs
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=1,
                                        st_min=st_min)
        self.mock_can_transport_interface._wait_for_flow_control = Mock(return_value=mock_flow_control_record)
        mock_add_cf_timestamp = Mock()
        mock_sent_packet_record = Mock(spec=CanPacketRecord, transmission_timestamp=MagicMock(__add__=mock_add_cf_timestamp))
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert (AbstractCanTransportInterface.send_message(self.mock_can_transport_interface, message)
                == mock_uds_message_record.return_value)
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_has_calls(
            [call(timeout_timestamp=mock_add_ff_timestamp.return_value)] + [
                call(timeout_timestamp=mock_add_cf_timestamp.return_value)
                for _ in mock_segmented_message[1:-1]
            ],
            any_order=False)
        self.mock_can_transport_interface._send_cf_packets_block.assert_has_calls([
            call(cf_packets_block=[packet],
                 delay=n_cs,
                 fc_transmission_timestamp=mock_flow_control_record.transmission_timestamp)
            for packet in mock_segmented_message[1:]],
            any_order=False)
        self.mock_can_st_min_handler.decode.assert_not_called()
        mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            *([mock_flow_control_record, mock_sent_packet_record] * len(mock_segmented_message[1:]))
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    def test_send_message__multiple_packets__wait(self, mock_uds_message_record,
                                                  message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        mock_add_fc_timestamp = Mock()
        mock_flow_control_record_wait = Mock(spec=CanPacketRecord,
                                             packet_type=CanPacketType.FLOW_CONTROL,
                                             flow_status=CanFlowStatus.Wait,
                                             transmission_timestamp=MagicMock(__add__=mock_add_fc_timestamp))
        mock_flow_control_record_continue = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.ContinueToSend,
                                                 block_size=0)
        self.mock_can_transport_interface._wait_for_flow_control.side_effect = [mock_flow_control_record_wait,
                                                                                mock_flow_control_record_continue]
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert (AbstractCanTransportInterface.send_message(self.mock_can_transport_interface, message)
                == mock_uds_message_record.return_value)
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_has_calls(
            [call(timeout_timestamp=mock_add_ff_timestamp.return_value),
             call(timeout_timestamp=mock_add_fc_timestamp.return_value)],
            any_order=False)
        mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record_wait,
            mock_flow_control_record_continue,
            mock_sent_packet_record
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__overflow(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.Overflow)
        self.mock_can_transport_interface._wait_for_flow_control.return_value = mock_flow_control_record_overflow
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        with pytest.raises(OverflowError):
            AbstractCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_called_once_with(
            timeout_timestamp=mock_add_ff_timestamp.return_value)
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__unknown_flow_status(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        mock_flow_control_record_unknown = Mock(spec=CanPacketRecord,
                                                packet_type=CanPacketType.FLOW_CONTROL,
                                                flow_status=Mock())
        self.mock_can_transport_interface._wait_for_flow_control.return_value = mock_flow_control_record_unknown
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_called_once_with(
            timeout_timestamp=mock_add_ff_timestamp.return_value)
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    # async_send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @pytest.mark.asyncio
    async def test_async_send_message__single_frame(self, mock_uds_message_record,
                                                    message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        assert await AbstractCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                    message) == mock_uds_message_record.return_value
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_send_packet.assert_called_once_with(
            mock_segmented_message[0], loop=self.mock_get_running_loop.return_value)
        mock_uds_message_record.assert_called_once_with(
            [self.mock_can_transport_interface.async_send_packet.return_value])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message, st_min", [
        (Mock(spec=UdsMessage,
              payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
              addressing_type=AddressingType.PHYSICAL),
         0x00),
        (Mock(spec=UdsMessage,
              payload=[0x3E, 0x80],
              addressing_type=AddressingType.PHYSICAL),
         0xFF),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__st_min__block_size_0(self, mock_uds_message_record,
                                                                              message, st_min):
        mock_loop = Mock(spec=AbstractEventLoop)
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.async_send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        self.mock_can_transport_interface.n_cs = None
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0,
                                        st_min=st_min)
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value = mock_flow_control_record
        mock_sent_packet_records = [Mock(spec=CanPacketRecord)] * 20
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = mock_sent_packet_records
        assert (await AbstractCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                     message=message,
                                                                     loop=mock_loop)
                == mock_uds_message_record.return_value)
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            mock_loop)
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_called_once_with(
            timeout_timestamp=mock_add_ff_timestamp.return_value)
        self.mock_can_transport_interface._async_send_cf_packets_block.assert_called_once_with(
            cf_packets_block=mock_segmented_message[1:],
            delay=self.mock_can_st_min_handler.decode.return_value,
            fc_transmission_timestamp=mock_flow_control_record.transmission_timestamp,
            loop=mock_loop)
        self.mock_can_st_min_handler.decode.assert_called_once_with(st_min)
        mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record,
            *mock_sent_packet_records
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message, n_cs, st_min", [
        (Mock(spec=UdsMessage,
              payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
              addressing_type=AddressingType.PHYSICAL),
         0, 0xFF),
        (Mock(spec=UdsMessage,
              payload=[0x3E, 0x80],
              addressing_type=AddressingType.PHYSICAL),
         5, 0x00),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__n_cs__block_size_1(self, mock_uds_message_record,
                                                                            message, n_cs, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.async_send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        self.mock_can_transport_interface.n_cs = n_cs
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=1,
                                        st_min=st_min)
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value = mock_flow_control_record
        mock_add_cf_timestamp = Mock()
        mock_sent_packet_record = Mock(spec=CanPacketRecord, transmission_timestamp=MagicMock(__add__=mock_add_cf_timestamp))
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await AbstractCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                    message) == mock_uds_message_record.return_value
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_has_calls(
            [call(timeout_timestamp=mock_add_ff_timestamp.return_value)] + [
                call(timeout_timestamp=mock_add_cf_timestamp.return_value)
                for _ in mock_segmented_message[1:-1]
            ],
            any_order=False)
        self.mock_can_transport_interface._async_send_cf_packets_block.assert_has_calls([
            call(cf_packets_block=[packet],
                 delay=n_cs,
                 fc_transmission_timestamp=mock_flow_control_record.transmission_timestamp,
                 loop=self.mock_get_running_loop.return_value) for packet in mock_segmented_message[1:]],
            any_order=False)
        self.mock_can_st_min_handler.decode.assert_not_called()
        mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            *([mock_flow_control_record, mock_sent_packet_record] * len(mock_segmented_message[1:]))
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    @patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__wait(self, mock_uds_message_record,
                                                              message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.async_send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        mock_add_fc_timestamp = Mock()
        mock_flow_control_record_wait = Mock(spec=CanPacketRecord,
                                             packet_type=CanPacketType.FLOW_CONTROL,
                                             flow_status=CanFlowStatus.Wait,
                                             transmission_timestamp=MagicMock(__add__=mock_add_fc_timestamp))
        mock_flow_control_record_continue = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.ContinueToSend,
                                                 block_size=0)
        self.mock_can_transport_interface._async_wait_for_flow_control.side_effect = [
            mock_flow_control_record_wait, mock_flow_control_record_continue]
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await AbstractCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                    message) == mock_uds_message_record.return_value
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_has_calls(
            [call(timeout_timestamp=mock_add_ff_timestamp.return_value),
             call(timeout_timestamp=mock_add_fc_timestamp.return_value)],
            any_order=False)
        mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record_wait,
            mock_flow_control_record_continue,
            mock_sent_packet_record
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__overflow(self, message):
        mock_loop = Mock(spec=AbstractEventLoop)
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.async_send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.Overflow)
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value = mock_flow_control_record_overflow
        with pytest.raises(OverflowError):
            await AbstractCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                   message=message,
                                                                   loop=mock_loop)
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            mock_loop)
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_called_once_with(
            timeout_timestamp=mock_add_ff_timestamp.return_value)
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__unknown_flow_status(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value = mock_segmented_message
        self.mock_can_transport_interface.n_bs_timeout = MagicMock(__div__=Mock())
        mock_add_ff_timestamp = Mock()
        self.mock_can_transport_interface.async_send_packet.return_value.transmission_timestamp = MagicMock(__add__=mock_add_ff_timestamp)
        mock_flow_control_record_unknown = Mock(spec=CanPacketRecord,
                                                packet_type=CanPacketType.FLOW_CONTROL,
                                                flow_status=Mock())
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value = mock_flow_control_record_unknown
        with pytest.raises(NotImplementedError):
            await AbstractCanTransportInterface.async_send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_flow_control_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_called_once_with(
            timeout_timestamp=mock_add_ff_timestamp.return_value)
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    # receive_message

    @pytest.mark.parametrize("start_timeout", [0.001, 123.456])
    def test_receive_message__timeout_error__no_time(self, start_timeout):
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        with pytest.raises(MessageTransmissionNotStartedError):
            AbstractCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                        start_timeout=start_timeout)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.receive_packet.assert_not_called()

    @pytest.mark.parametrize("start_timeout", [0.001, 123.456])
    def test_receive_message__timeout_error__no_packet(self, start_timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_transport_interface.receive_packet.side_effect = TimeoutError
        with pytest.raises(MessageTransmissionNotStartedError):
            AbstractCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                        start_timeout=start_timeout)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.receive_packet.assert_called_once()

    @pytest.mark.parametrize("start_timeout, end_timeout", [
        (None, 123.456),
        (65.201, None),
        (987, 654),
    ])
    def test_receive_message__initial_packet(self, start_timeout, end_timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (AbstractCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                            start_timeout=start_timeout,
                                                            end_timeout=end_timeout)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value,
            timestamp_end=None if end_timeout is None else self.mock_perf_counter.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called_once()
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("start_timeout, end_timeout", [
        (None, 123.456),
        (65.201, None),
        (987, 654),
    ])
    def test_receive_message__cf_then_initial_packet(self, start_timeout, end_timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.side_effect = [False, True]
        assert (AbstractCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                            start_timeout=start_timeout,
                                                            end_timeout=end_timeout)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value,
            timestamp_end=None if end_timeout is None else self.mock_perf_counter.return_value)
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            calls=[call(timeout=None if start_timeout is None else self.mock_perf_counter.return_value),
                   call(timeout=None if start_timeout is None else self.mock_perf_counter.return_value)]
        )
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_warn.assert_called_once()

    # async_receive_message

    @pytest.mark.parametrize("start_timeout", [0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_message__timeout_error__no_time(self, start_timeout):
        mock_loop = Mock(spec=AbstractEventLoop)
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        with pytest.raises(MessageTransmissionNotStartedError):
            await AbstractCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                    start_timeout=start_timeout,
                                                                    loop=mock_loop)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            loop=mock_loop)
        self.mock_can_transport_interface.async_receive_packet.assert_not_called()

    @pytest.mark.parametrize("start_timeout", [0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_message__timeout_error__no_packet(self, start_timeout):
        mock_loop = Mock(spec=AbstractEventLoop)
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_transport_interface.async_receive_packet.side_effect = TimeoutError
        with pytest.raises(MessageTransmissionNotStartedError):
            await AbstractCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                    start_timeout=start_timeout,
                                                                    loop=mock_loop)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            loop=mock_loop)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once()

    @pytest.mark.parametrize("start_timeout, end_timeout", [
        (None, 123.456),
        (65.201, None),
        (987, 654),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__initial_packet(self, start_timeout, end_timeout):
        mock_loop = Mock(spec=AbstractEventLoop)
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (await AbstractCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                        start_timeout=start_timeout,
                                                                        end_timeout=end_timeout,
                                                                        loop=mock_loop)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            loop=mock_loop)
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value,
            timestamp_end=None if end_timeout is None else self.mock_perf_counter.return_value,
            loop=mock_loop)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("start_timeout, end_timeout", [
        (None, 123.456),
        (65.201, None),
        (987, 654),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_message__cf_then_initial_packet(self, start_timeout, end_timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.side_effect = [False, True]
        assert (await AbstractCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                        start_timeout=start_timeout,
                                                                        end_timeout=end_timeout,
                                                                        loop=None)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value,
            timestamp_end=None if end_timeout is None else self.mock_perf_counter.return_value,
            loop=self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            calls=[call(timeout=None if start_timeout is None else self.mock_perf_counter.return_value,
                        loop=self.mock_get_running_loop.return_value),
                   call(timeout=None if start_timeout is None else self.mock_perf_counter.return_value,
                        loop=self.mock_get_running_loop.return_value)]
        )
        self.mock_warn.assert_called_once()


@pytest.mark.performance
class TestAbstractCanTransportInterfacePerformance:
    """Performance tests for `AbstractCanTransportInterface` class."""

    REPETITIONS = 100

    def setup_method(self):
        self.mock_can_transport_interface = MagicMock(spec=AbstractCanTransportInterface)
        self._patcher_get_running_loop = patch(f"{SCRIPT_LOCATION}.get_running_loop")
        self.mock_get_running_loop = self._patcher_get_running_loop.start()

    def teardown_method(self):
        self._patcher_get_running_loop.stop()

    # receive_message

    @pytest.mark.parametrize("start_timeout", [10, 75])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
    def test_receive_message__start_timeout(self, mock_is_initial_packet_type,
                                            performance_tolerance_ms, mean_performance_tolerance_ms,
                                            start_timeout):
        def _get_packet_record(*_, **__):
            sleep(0.005)
            return Mock(spec=CanPacketRecord)

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.receive_packet.side_effect = _get_packet_record

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                AbstractCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                              start_timeout=start_timeout)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (start_timeout
                    <= execution_time_ms
                    <= start_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (start_timeout
                <= mean_execution_time_ms
                <= start_timeout + mean_performance_tolerance_ms)

    # async_receive_message

    @pytest.mark.parametrize("start_timeout", [10, 75])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
    @pytest.mark.asyncio
    async def test_async_receive_message__start_timeout(self, mock_is_initial_packet_type,
                                                        performance_tolerance_ms, mean_performance_tolerance_ms,
                                                        start_timeout):
        async def _get_packet_record(*_, **__):
            await async_sleep(0.005)
            return Mock(spec=CanPacketRecord)

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.async_receive_packet.side_effect = _get_packet_record

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(MessageTransmissionNotStartedError):
                await AbstractCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                          start_timeout=start_timeout)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (start_timeout
                    <= execution_time_ms
                    <= start_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (start_timeout
                <= mean_execution_time_ms
                <= start_timeout + mean_performance_tolerance_ms)

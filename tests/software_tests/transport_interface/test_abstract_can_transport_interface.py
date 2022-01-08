import pytest
from mock import Mock, patch

from uds.transport_interface.abstract_can_transport_interface import AbstractCanTransportInterface,\
    DEFAULT_PACKET_RECORDS_STORED, DEFAULT_MESSAGE_RECORDS_STORED,\
    DEFAULT_FLOW_CONTROL_ARGS, N_AS_TIMEOUT, N_AR_TIMEOUT, N_BS_TIMEOUT, N_CR_TIMEOUT


class TestAbstractCanTransportInterface:
    """Unit tests for `AbstractCanTransportInterface` class."""

    SCRIPT_LOCATION = "uds.transport_interface.abstract_can_transport_interface"

    def setup(self):
        self.mock_can_transport_interface = Mock(spec=AbstractCanTransportInterface)
        # patching
        self._patcher_abstract_ti_init = patch(f"{self.SCRIPT_LOCATION}.AbstractTransportInterface.__init__")
        self.mock_abstract_ti_init = self._patcher_abstract_ti_init.start()
        self._patcher_can_segmenter_class = patch(f"{self.SCRIPT_LOCATION}.CanSegmenter")
        self.mock_can_segmenter_class = self._patcher_can_segmenter_class.start()
        self._patcher_can_packet_class = patch(f"{self.SCRIPT_LOCATION}.CanPacket")
        self.mock_can_packet_class = self._patcher_can_packet_class.start()
        self._patcher_packet_queue_class = patch(f"{self.SCRIPT_LOCATION}.PacketsQueue")
        self.mock_packet_queue_class = self._patcher_packet_queue_class.start()
        self._patcher_timestamped_packet_queue_class = patch(f"{self.SCRIPT_LOCATION}.TimestampedPacketsQueue")
        self.mock_timestamped_packet_queue_class = self._patcher_timestamped_packet_queue_class.start()

    def teardown(self):
        self._patcher_abstract_ti_init.stop()
        self._patcher_can_segmenter_class.stop()
        self._patcher_can_packet_class.stop()
        self._patcher_packet_queue_class.stop()
        self._patcher_timestamped_packet_queue_class.stop()

    # __init__

    def test_init__valid(self, can_bus_manager, addressing_format, physical_ai, functional_ai,
                         records_args, segmenter_args, other_can_args):
        AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                               can_bus_manager=can_bus_manager,
                                               addressing_format=addressing_format,
                                               physical_ai=physical_ai,
                                               functional_ai=functional_ai,
                                               **records_args,
                                               **segmenter_args,
                                               **other_can_args)
        self.mock_abstract_ti_init.assert_called_once_with(
            bus_manager=can_bus_manager,
            max_packet_records_stored=records_args.get("max_packet_records_stored", DEFAULT_PACKET_RECORDS_STORED),
            max_message_records_stored=records_args.get("max_message_records_stored", DEFAULT_MESSAGE_RECORDS_STORED))
        self.mock_can_segmenter_class.assert_called_once_with(addressing_format=addressing_format,
                                                              physical_ai=physical_ai,
                                                              functional_ai=functional_ai,
                                                              **segmenter_args)
        assert self.mock_can_transport_interface.__segmenter == self.mock_can_segmenter_class.return_value
        assert self.mock_can_transport_interface.__input_packets_queue == self.mock_packet_queue_class.return_value
        assert self.mock_can_transport_interface.__output_packet_queue == self.mock_timestamped_packet_queue_class.return_value
        assert self.mock_can_transport_interface.n_as_timeout == other_can_args.get("n_as_timeout", N_AS_TIMEOUT)
        assert self.mock_can_transport_interface.n_ar_timeout == other_can_args.get("n_ar_timeout", N_AR_TIMEOUT)
        assert self.mock_can_transport_interface.n_bs_timeout == other_can_args.get("n_bs_timeout", N_BS_TIMEOUT)
        assert self.mock_can_transport_interface.n_cr_timeout == other_can_args.get("n_cr_timeout", N_CR_TIMEOUT)
        if "flow_control_generator" in other_can_args:
            assert self.mock_can_transport_interface.flow_control_generator == other_can_args["flow_control_generator"]
        else:
            self.mock_can_packet_class.assert_called_once_with(
                dlc=self.mock_can_transport_interface.dlc,
                use_data_optimization=self.mock_can_transport_interface.use_data_optimization,
                filler_byte=self.mock_can_transport_interface.filler_byte,
                **DEFAULT_FLOW_CONTROL_ARGS,
                **self.mock_can_transport_interface.physical_ai)
            assert self.mock_can_transport_interface.flow_control_generator == self.mock_can_packet_class.return_value

    # segmenter

    def test_segmenter(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.segmenter.fget(self.mock_can_transport_interface)

    # _input_packets_queue

    def test_input_packets_queue(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface._input_packets_queue.fget(self.mock_can_transport_interface)

    # _output_packet_queue

    def test_output_packet_queue(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface._output_packet_queue.fget(self.mock_can_transport_interface)

    # n_as

    def test_n_as_timeout__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_as_timeout.fget(self.mock_can_transport_interface)

    def test_n_as_timeout__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_as_timeout.fset(self.mock_can_transport_interface, Mock())
            
    # n_ar

    def test_n_ar_timeout__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_ar_timeout.fget(self.mock_can_transport_interface)

    def test_n_ar_timeout__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_ar_timeout.fset(self.mock_can_transport_interface, Mock())
            
    # n_bs

    def test_n_bs_timeout__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_bs_timeout.fget(self.mock_can_transport_interface)

    def test_n_bs_timeout__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_bs_timeout.fset(self.mock_can_transport_interface, Mock())
            
    # n_br

    def test_n_br__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_br.fget(self.mock_can_transport_interface)

    def test_n_br__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_br.fset(self.mock_can_transport_interface, Mock())

    def test_n_br_max(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_br_max.fget(self.mock_can_transport_interface)
            
    # n_cs

    def test_n_cs__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_cs.fget(self.mock_can_transport_interface)

    def test_n_cs__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_cs.fset(self.mock_can_transport_interface, Mock())

    def test_n_cs_max(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_cs_max.fget(self.mock_can_transport_interface)
            
    # n_cr

    def test_n_cr_timeout__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_cr_timeout.fget(self.mock_can_transport_interface)

    def test_n_cr_timeout__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.n_cr_timeout.fset(self.mock_can_transport_interface, Mock())

    # addressing_format

    def test_addressing_format__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.addressing_format.fget(self.mock_can_transport_interface)

    # physical_ai

    def test_physical_ai__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.physical_ai.fget(self.mock_can_transport_interface)

    def test_physical_ai__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.physical_ai.fset(self.mock_can_transport_interface, Mock())
            
    # functional_ai

    def test_functional_ai__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.functional_ai.fget(self.mock_can_transport_interface)

    def test_functional_ai__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.functional_ai.fset(self.mock_can_transport_interface, Mock())

    # dlc

    def test_dlc__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.dlc.fget(self.mock_can_transport_interface)

    def test_dlc__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.dlc.fset(self.mock_can_transport_interface, Mock())
            
    # use_data_optimization

    def test_use_data_optimization__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.use_data_optimization.fget(self.mock_can_transport_interface)

    def test_use_data_optimization__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.use_data_optimization.fset(self.mock_can_transport_interface, Mock())
            
    # filler_byte

    def test_filler_byte__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.filler_byte.fget(self.mock_can_transport_interface)

    def test_filler_byte__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.filler_byte.fset(self.mock_can_transport_interface, Mock())

    # flow_control_generator

    def test_flow_control_generator__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.flow_control_generator.fget(self.mock_can_transport_interface)

    def test_flow_control_generator__set(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.flow_control_generator.fset(self.mock_can_transport_interface, Mock())

    # _get_flow_control

    def test_get_flow_control(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface._get_flow_control(self=self.mock_can_transport_interface, is_first=Mock())

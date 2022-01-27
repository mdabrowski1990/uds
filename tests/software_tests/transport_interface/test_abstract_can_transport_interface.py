import pytest
from mock import Mock

from uds.transport_interface.abstract_can_transport_interface import AbstractCanTransportInterface


class TestAbstractCanTransportInterface:
    """Unit tests for `AbstractCanTransportInterface` class."""

    def setup(self):
        self.mock_can_transport_interface = Mock(spec=AbstractCanTransportInterface)

    # __init__

    def test_init(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                                   can_bus_manager=Mock(),
                                                   max_packet_records_stored=Mock(),
                                                   max_message_records_stored=Mock(),
                                                   addressing_information=Mock())

    # segmenter

    def test_segmenter(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.segmenter.fget(self.mock_can_transport_interface)

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

    # addressing_information

    def test_addressing_information__get(self):
        with pytest.raises(NotImplementedError):
            AbstractCanTransportInterface.addressing_information.fget(self.mock_can_transport_interface)

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

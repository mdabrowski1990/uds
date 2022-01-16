import pytest
from mock import Mock, MagicMock, patch, call

from uds.can.entity_addressing_information import AbstractCanEntityAI, CanEntityNormal11bitAI,\
    CanAddressingFormat, AbstractCanPacketContainer, AddressingType


class TestAbstractCanEntityAI:
    """Unit tests for `AbstractCanEntityAI` class."""

    SCRIPT_LOCATION = "uds.can.entity_addressing_information"

    def setup(self):
        self.mock_can_entity_ai = Mock(spec=AbstractCanEntityAI)

    # __init__

    @pytest.mark.parametrize("physical_ai, functional_ai", [
        ({"arg1": "some value", "arg2": "some other value"}, {"a": None, "b": 1}),
        ({"foo": "Bar"}, {"xyz": "abc", "ghi": 321}),
    ])
    def test_init(self, physical_ai, functional_ai):
        AbstractCanEntityAI.__init__(self=self.mock_can_entity_ai, physical_ai=physical_ai, functional_ai=functional_ai)
        self.mock_can_entity_ai.set_physical_ai.assert_called_once_with(**physical_ai)
        self.mock_can_entity_ai.set_functional_ai.assert_called_once_with(**functional_ai)

    # is_packet_targeting_entity

    @pytest.mark.parametrize("can_packet", [Mock(), "something"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_packet_targeting_entity__type_error(self, mock_isinstance, can_packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            AbstractCanEntityAI.is_packet_targeting_entity(self=self.mock_can_entity_ai, can_packet=can_packet)
        mock_isinstance.assert_called_once_with(can_packet, AbstractCanPacketContainer)

    @pytest.mark.parametrize("can_packet", [Mock(), Mock(addressing_type="something")])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_packet_targeting_entity__not_implemented_error(self, mock_isinstance, can_packet):
        mock_isinstance.return_value = True
        with pytest.raises(NotImplementedError):
            AbstractCanEntityAI.is_packet_targeting_entity(self=self.mock_can_entity_ai, can_packet=can_packet)
        mock_isinstance.assert_called_once_with(can_packet, AbstractCanPacketContainer)

    @pytest.mark.parametrize("can_packet", [Mock(addressing_type=AddressingType.PHYSICAL),
                                            Mock(addressing_type=AddressingType.FUNCTIONAL)])
    @pytest.mark.parametrize("ai_params_names", [
        ("arg1", "arg2", "arg3"),
        ("can_id", "target_address"),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_packet_targeting_entity__true(self, mock_isinstance, can_packet, ai_params_names):
        mock_isinstance.return_value = True
        mock_ne = Mock(return_value=False)
        if can_packet.addressing_type == AddressingType.PHYSICAL:
            self.mock_can_entity_ai.receiving_physical_ai = {param_name: MagicMock(__ne__=mock_ne)
                                                             for param_name in ai_params_names}
        elif can_packet.addressing_type == AddressingType.FUNCTIONAL:
            self.mock_can_entity_ai.receiving_functional_ai = {param_name: MagicMock(__ne__=mock_ne)
                                                               for param_name in ai_params_names}
        assert AbstractCanEntityAI.is_packet_targeting_entity(self=self.mock_can_entity_ai,
                                                              can_packet=can_packet) is True
        mock_isinstance.assert_called_once_with(can_packet, AbstractCanPacketContainer)
        mock_ne.assert_has_calls([call(getattr(can_packet, param_name)) for param_name in ai_params_names],
                                 any_order=True)

    @pytest.mark.parametrize("can_packet", [Mock(addressing_type=AddressingType.PHYSICAL),
                                            Mock(addressing_type=AddressingType.FUNCTIONAL)])
    @pytest.mark.parametrize("ai_params_names", [
        ("arg1", "arg2", "arg3"),
        ("can_id", "target_address"),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_packet_targeting_entity__false(self, mock_isinstance, can_packet, ai_params_names):
        mock_isinstance.return_value = True
        mock_ne = Mock(return_value=True)
        if can_packet.addressing_type == AddressingType.PHYSICAL:
            self.mock_can_entity_ai.receiving_physical_ai = {param_name: MagicMock(__ne__=mock_ne)
                                                             for param_name in ai_params_names}
        elif can_packet.addressing_type == AddressingType.FUNCTIONAL:
            self.mock_can_entity_ai.receiving_functional_ai = {param_name: MagicMock(__ne__=mock_ne)
                                                               for param_name in ai_params_names}
        assert AbstractCanEntityAI.is_packet_targeting_entity(self=self.mock_can_entity_ai,
                                                              can_packet=can_packet) is False
        mock_isinstance.assert_called_once_with(can_packet, AbstractCanPacketContainer)
        mock_ne.assert_called_once()


class TestCanEntityNormal11bitAI:
    """Unit tests for `CanEntityNormal11bitAI` class."""

    SCRIPT_LOCATION = TestAbstractCanEntityAI.SCRIPT_LOCATION

    def setup(self):
        self.mock_can_entity_ai = Mock(spec=CanEntityNormal11bitAI)
        # patching
        self._patcher_can_id_handler_class = patch(f"{self.SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler_class = self._patcher_can_id_handler_class.start()
        self._patcher_abstract_can_entity_ai_init = patch(f"{self.SCRIPT_LOCATION}.AbstractCanEntityAI.__init__")
        self.mock_abstract_can_entity_ai_init = self._patcher_abstract_can_entity_ai_init.start()

    def teardown(self):
        self._patcher_can_id_handler_class.stop()
        self._patcher_abstract_can_entity_ai_init.stop()

    # __init__

    @pytest.mark.parametrize("physical_ai, functional_ai", [
        ({"arg1": "some value", "arg2": "some other value"}, {"a": None, "b": 1}),
        ({"foo": "Bar"}, {"xyz": "abc", "ghi": 321}),
    ])
    def test_init(self, physical_ai, functional_ai):
        CanEntityNormal11bitAI.__init__(self=self.mock_can_entity_ai,
                                        physical_ai=physical_ai,
                                        functional_ai=functional_ai)
        self.mock_abstract_can_entity_ai_init.assert_called_once_with(physical_ai=physical_ai,
                                                                      functional_ai=functional_ai)
        assert self.mock_can_entity_ai._CanEntityNormal11bitAI__physical_rx_can_id is None
        assert self.mock_can_entity_ai._CanEntityNormal11bitAI__physical_tx_can_id is None
        assert self.mock_can_entity_ai._CanEntityNormal11bitAI__functional_rx_can_id is None
        assert self.mock_can_entity_ai._CanEntityNormal11bitAI__functional_tx_can_id is None

    # set_physical_ai

    @pytest.mark.parametrize("can_entity_ai, rx_can_id, tx_can_id", [
        (Mock(spec=CanEntityNormal11bitAI,
              _CanEntityNormal11bitAI__physical_rx_can_id=0x1,
              _CanEntityNormal11bitAI__physical_tx_can_id=0x2,
              _CanEntityNormal11bitAI__functional_rx_can_id=0x124,
              _CanEntityNormal11bitAI__functional_tx_can_id=0x122),
         0x123, 0x456),
        (Mock(spec=CanEntityNormal11bitAI,
              _CanEntityNormal11bitAI__physical_rx_can_id=0xA1,
              _CanEntityNormal11bitAI__physical_tx_can_id=0xB2,
              _CanEntityNormal11bitAI__functional_rx_can_id=0xB1,
              _CanEntityNormal11bitAI__functional_tx_can_id=0xB3),
         0xA1, 0xB2),
    ])
    def test_set_physical_ai__valid(self, can_entity_ai, rx_can_id, tx_can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = True
        assert CanEntityNormal11bitAI.set_physical_ai(self=can_entity_ai,
                                                      rx_can_id=rx_can_id,
                                                      tx_can_id=tx_can_id) is None
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_has_calls(
            [call(rx_can_id), call(tx_can_id)], any_order=True)
        assert can_entity_ai._CanEntityNormal11bitAI__physical_rx_can_id == rx_can_id
        assert can_entity_ai._CanEntityNormal11bitAI__physical_tx_can_id == tx_can_id

    @pytest.mark.parametrize("rx_can_id, tx_can_id", [
        ("some", "thing"),
        (123, 456),
    ])
    @pytest.mark.parametrize("check_results", [
        [False, True],
        [True, False],
    ])
    def test_set_physical_ai__invalid_value(self, rx_can_id, tx_can_id, check_results):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.side_effect = check_results
        with pytest.raises(ValueError):
            CanEntityNormal11bitAI.set_physical_ai(self=self.mock_can_entity_ai,
                                                   rx_can_id=rx_can_id,
                                                   tx_can_id=tx_can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_called()

    @pytest.mark.parametrize("can_entity_ai, rx_can_id, tx_can_id", [
        (Mock(spec=CanEntityNormal11bitAI,
              _CanEntityNormal11bitAI__physical_rx_can_id=None,
              _CanEntityNormal11bitAI__physical_tx_can_id=None,
              _CanEntityNormal11bitAI__functional_rx_can_id=0x123,
              _CanEntityNormal11bitAI__functional_tx_can_id=None),
         0x123, 0x456),
        (Mock(spec=CanEntityNormal11bitAI,
              _CanEntityNormal11bitAI__physical_rx_can_id=None,
              _CanEntityNormal11bitAI__physical_tx_can_id=None,
              _CanEntityNormal11bitAI__functional_rx_can_id=None,
              _CanEntityNormal11bitAI__functional_tx_can_id=0xB2),
         0xA1, 0xB2),
    ])
    def test_set_physical_ai__repeated_value(self, can_entity_ai, rx_can_id, tx_can_id):
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.return_value = True
        with pytest.raises(ValueError):
            CanEntityNormal11bitAI.set_physical_ai(self=can_entity_ai,
                                                   rx_can_id=rx_can_id,
                                                   tx_can_id=tx_can_id)
        self.mock_can_id_handler_class.is_normal_11bit_addressed_can_id.assert_has_calls(
            [call(rx_can_id), call(tx_can_id)], any_order=True)

    # set_functional_ai

    # TODO

    # addressing_format

    def test_addressing_format(self):
        assert CanEntityNormal11bitAI.addressing_format.fget(self.mock_can_entity_ai) \
               == CanAddressingFormat.NORMAL_11BIT_ADDRESSING

from asyncio import get_running_loop
from asyncio import sleep as asyncio_sleep
from datetime import datetime
from time import perf_counter, sleep

import pytest
from mock import AsyncMock, MagicMock, Mock, call, patch

from can import Bus
from can.interfaces.kvaser import KvaserBus
from can.interfaces.vector import VectorBus
from can.interfaces.virtual import VirtualBus
from uds.addressing import AddressingType
from uds.can import DEFAULT_FILLER_BYTE, CanAddressingInformation, DefaultFlowControlParametersGenerator
from uds.can.transport_interface.python_can import (
    AbstractCanTransportInterface,
    AbstractEventLoop,
    AsyncBufferedReader,
    BufferedReader,
    BusABC,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    Notifier,
    PythonCanTransportInterface,
    TransmissionDirection,
)

SCRIPT_LOCATION = "uds.can.transport_interface.python_can"


class TestPythonCanTransportInterface:
    """Unit tests for `PythonCanTransportInterface` class."""

    def setup_method(self):
        self.mock_can_transport_interface = MagicMock(
            spec=PythonCanTransportInterface,
            _MIN_NOTIFIER_TIMEOUT=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT,
            _PythonCanTransportInterface__rx_frames_buffer=Mock(),
            _PythonCanTransportInterface__tx_frames_buffer=Mock(),
            _PythonCanTransportInterface__fc_frames_buffer=Mock(),
            _PythonCanTransportInterface__async_rx_frames_buffer=Mock(),
            _PythonCanTransportInterface__async_tx_frames_buffer=Mock(),
            _PythonCanTransportInterface__async_fc_frames_buffer=Mock())
        # patching
        self._patcher_can_packet_record = patch(f"{SCRIPT_LOCATION}.CanPacketRecord")
        self.mock_can_packet_record = self._patcher_can_packet_record.start()
        self._patcher_can_id_handler = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler = self._patcher_can_id_handler.start()
        self._patcher_can_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler = self._patcher_can_dlc_handler.start()
        self._patcher_abstract_can_ti_init = patch(f"{SCRIPT_LOCATION}.AbstractCanTransportInterface.__init__")
        self.mock_abstract_can_ti_init = self._patcher_abstract_can_ti_init.start()
        self._patcher_buffered_reader = patch(f"{SCRIPT_LOCATION}.BufferedReader")
        self.mock_buffered_reader = self._patcher_buffered_reader.start()
        self._patcher_async_buffered_reader = patch(f"{SCRIPT_LOCATION}.AsyncBufferedReader")
        self.mock_async_buffered_reader = self._patcher_async_buffered_reader.start()
        self._patcher_notifier = patch(f"{SCRIPT_LOCATION}.Notifier")
        self.mock_notifier = self._patcher_notifier.start()
        self._patcher_python_can_frame = patch(f"{SCRIPT_LOCATION}.PythonCanFrame")
        self.mock_python_can_frame = self._patcher_python_can_frame.start()
        self._patcher_validate_timeout = patch(f"{SCRIPT_LOCATION}.validate_timeout")
        self.mock_validate_timeout = self._patcher_validate_timeout.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_datetime = patch(f"{SCRIPT_LOCATION}.datetime")
        self.mock_datetime = self._patcher_datetime.start()
        self._patcher_get_running_loop = patch(f"{SCRIPT_LOCATION}.get_running_loop")
        self.mock_get_running_loop = self._patcher_get_running_loop.start()
        self._patcher_async_timeout = patch(f"{SCRIPT_LOCATION}.async_timeout")
        self.mock_async_timeout = self._patcher_async_timeout.start()

    def teardown_method(self):
        self._patcher_can_packet_record.stop()
        self._patcher_can_id_handler.stop()
        self._patcher_can_dlc_handler.stop()
        self._patcher_abstract_can_ti_init.stop()
        self._patcher_buffered_reader.stop()
        self._patcher_async_buffered_reader.stop()
        self._patcher_notifier.stop()
        self._patcher_python_can_frame.stop()
        self._patcher_validate_timeout.stop()
        self._patcher_warn.stop()
        self._patcher_perf_counter.stop()
        self._patcher_datetime.stop()
        self._patcher_get_running_loop.stop()
        self._patcher_async_timeout.stop()

    # __init__

    @pytest.mark.parametrize("network_manager, addressing_information, configuration_params", [
        (
                Mock(),
                Mock(),
                {}
        ),
        (
                Mock(spec=BusABC),
                Mock(spec=CanAddressingInformation),
                {"param1": Mock(), "param2": Mock(), "dlc": 8}
        ),
    ])
    def test_init__mandatory_args(self, network_manager, addressing_information, configuration_params):
        assert PythonCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                                    network_manager=network_manager,
                                                    addressing_information=addressing_information,
                                                    **configuration_params) is None
        assert self.mock_can_transport_interface.notifier is None
        assert self.mock_can_transport_interface.async_notifier is None
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        self.mock_abstract_can_ti_init.assert_called_once_with(
            network_manager=network_manager,
            addressing_information=addressing_information,
            **configuration_params)
        self.mock_buffered_reader.assert_has_calls([call(), call(), call()])
        self.mock_async_buffered_reader.assert_has_calls([call(), call(), call()])

    @pytest.mark.parametrize("network_manager, addressing_information, notifier, async_notifier, "
                             "configuration_params", [
                                 (
                                         Mock(),
                                         Mock(),
                                         Mock(),
                                         Mock(),
                                         {}
                                 ),
                                 (
                                         Mock(spec=BusABC),
                                         Mock(spec=CanAddressingInformation),
                                         Mock(spec=Notifier),
                                         Mock(spec=Notifier),
                                         {"param1": Mock(), "param2": Mock(), "dlc": 8}
                                 ),
                             ])
    def test_init__all_args(self, network_manager, addressing_information, notifier, async_notifier,
                            configuration_params):
        assert PythonCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                                    network_manager=network_manager,
                                                    addressing_information=addressing_information,
                                                    notifier=notifier,
                                                    async_notifier=async_notifier,
                                                    **configuration_params) is None
        assert self.mock_can_transport_interface.notifier == notifier
        assert self.mock_can_transport_interface.async_notifier == async_notifier
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        self.mock_abstract_can_ti_init.assert_called_once_with(
            network_manager=network_manager,
            addressing_information=addressing_information,
            **configuration_params)
        assert self.mock_buffered_reader.call_count == 3
        assert self.mock_async_buffered_reader.call_count == 3

    # __del__

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.__del__")
    def test_del(self, mock_parent_del):
        assert PythonCanTransportInterface.__del__(self.mock_can_transport_interface) is None
        self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer.stop.assert_called_once_with()
        mock_parent_del.assert_called_once_with()

    # network_manager

    @patch("uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.network_manager")
    def test_network_manager__get(self, mock_network_manager):
        assert (PythonCanTransportInterface.network_manager.fget(self.mock_can_transport_interface)
                == mock_network_manager)

    def test_network_manager__set(self):
        mock_value = Mock()
        self.mock_can_transport_interface.__dict__["backend"] = Mock()
        assert PythonCanTransportInterface.network_manager.fset(self.mock_can_transport_interface, mock_value) is None
        assert "backend" not in self.mock_can_transport_interface.__dict__

    # backed

    def test_backed__get__runtime_error(self):
        self.mock_can_transport_interface.network_manager = Mock(spec=BusABC)
        with pytest.raises(RuntimeError):
            PythonCanTransportInterface.backend.__get__(self.mock_can_transport_interface)

    @pytest.mark.parametrize("cls, name", [
        (KvaserBus, "kvaser"),
        (VectorBus, "vector"),
        (VirtualBus, "virtual"),
    ])
    def test_backed__get__valid(self, cls, name):
        self.mock_can_transport_interface.network_manager = Mock(spec=cls)
        assert PythonCanTransportInterface.backend.__get__(self.mock_can_transport_interface) == name

    # notifier

    def test_notifier__get(self):
        self.mock_can_transport_interface._PythonCanTransportInterface__notifier = Mock()
        assert (PythonCanTransportInterface.notifier.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._PythonCanTransportInterface__notifier)

    @pytest.mark.parametrize("value", [Mock(), "CAN Segmenter"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_notifier__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PythonCanTransportInterface.notifier.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, self.mock_notifier)

    def test_notifier__set__valid__none(self):
        assert PythonCanTransportInterface.notifier.fset(self.mock_can_transport_interface, None) is None
        assert self.mock_can_transport_interface._PythonCanTransportInterface__notifier is None

    @pytest.mark.parametrize("value", [Mock(spec=Notifier,
                                            timeout=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT + 0.01),
                                       Mock(spec=Notifier,
                                            timeout=2 * PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT)])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_notifier__set__valid__with_warning(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert PythonCanTransportInterface.notifier.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._PythonCanTransportInterface__notifier == value
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__notifier.timeout
                == PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT)
        mock_isinstance.assert_called_once_with(value, self.mock_notifier)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("value", [Mock(spec=Notifier,
                                            timeout=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT),
                                       Mock(spec=Notifier,
                                            timeout=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT - 0.01)])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_notifier__set__valid__without_warning(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert PythonCanTransportInterface.notifier.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._PythonCanTransportInterface__notifier == value
        mock_isinstance.assert_called_once_with(value, self.mock_notifier)
        self.mock_warn.assert_not_called()

    # async_notifier

    def test_async_notifier__get(self):
        self.mock_can_transport_interface._PythonCanTransportInterface__async_notifier = Mock()
        assert (PythonCanTransportInterface.async_notifier.fget(self.mock_can_transport_interface)
                == self.mock_can_transport_interface._PythonCanTransportInterface__async_notifier)

    @pytest.mark.parametrize("value", [Mock(), "CAN Segmenter"])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_async_notifier__set__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PythonCanTransportInterface.async_notifier.fset(self.mock_can_transport_interface, value)
        mock_isinstance.assert_called_once_with(value, self.mock_notifier)

    def test_async_notifier__set__valid__none(self):
        assert PythonCanTransportInterface.async_notifier.fset(self.mock_can_transport_interface, None) is None
        assert self.mock_can_transport_interface._PythonCanTransportInterface__async_notifier is None

    @pytest.mark.parametrize("value", [Mock(spec=Notifier,
                                            timeout=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT + 0.01),
                                       Mock(spec=Notifier,
                                            timeout=2 * PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT)])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_async_notifier__set__valid__with_warning(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert PythonCanTransportInterface.async_notifier.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._PythonCanTransportInterface__async_notifier == value
        assert (self.mock_can_transport_interface._PythonCanTransportInterface__async_notifier.timeout
                == PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT)
        mock_isinstance.assert_called_once_with(value, self.mock_notifier)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("value", [Mock(spec=Notifier,
                                            timeout=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT),
                                       Mock(spec=Notifier,
                                            timeout=PythonCanTransportInterface._MIN_NOTIFIER_TIMEOUT - 0.01)])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_async_notifier__set__valid__without_warning(self, mock_isinstance, value):
        mock_isinstance.return_value = True
        assert PythonCanTransportInterface.async_notifier.fset(self.mock_can_transport_interface, value) is None
        assert self.mock_can_transport_interface._PythonCanTransportInterface__async_notifier == value
        mock_isinstance.assert_called_once_with(value, self.mock_notifier)
        self.mock_warn.assert_not_called()

    # is_sync_active

    def test_is_sync_active__get__true(self):
        mock_bus = Mock()
        mock_rx_buffer = Mock(is_stopped=False)
        mock_tx_buffer = Mock(is_stopped=False)
        mock_fc_buffer = Mock(is_stopped=False)
        self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer = mock_rx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer = mock_tx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer = mock_fc_buffer
        self.mock_can_transport_interface.network_manager = mock_bus
        self.mock_can_transport_interface.notifier = Mock(
            stopped=False,
            _bus_list=[mock_bus],
            listeners=[mock_rx_buffer, mock_tx_buffer, mock_fc_buffer])
        assert PythonCanTransportInterface.is_sync_active.fget(self.mock_can_transport_interface) is True

    def test_is_sync_active__get__false__no_notifier(self):
        self.mock_can_transport_interface.notifier = None
        assert PythonCanTransportInterface.is_sync_active.fget(self.mock_can_transport_interface) is False

    def test_is_sync_active__get__false__wrong_bus(self):
        mock_rx_buffer = Mock(is_stopped=False)
        mock_tx_buffer = Mock(is_stopped=False)
        mock_fc_buffer = Mock(is_stopped=False)
        self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer = mock_rx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer = mock_tx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer = mock_fc_buffer
        self.mock_can_transport_interface.notifier = Mock(
            stopped=False,
            _bus_list=[Mock()],
            listeners=[mock_rx_buffer, mock_tx_buffer, mock_fc_buffer])
        assert PythonCanTransportInterface.is_sync_active.fget(self.mock_can_transport_interface) is False

    @pytest.mark.parametrize("notifier, rx_buffer, tx_buffer, fc_buffer", [
        (Mock(stopped=True), Mock(is_stopped=False), Mock(is_stopped=False), Mock(is_stopped=False)),
        (Mock(stopped=False), Mock(is_stopped=True), Mock(is_stopped=False), Mock(is_stopped=False)),
        (Mock(stopped=False), Mock(is_stopped=False), Mock(is_stopped=True), Mock(is_stopped=False)),
        (Mock(stopped=False), Mock(is_stopped=False), Mock(is_stopped=False), Mock(is_stopped=True)),
    ])
    def test_is_sync_active__get__false__stopped(self, notifier, rx_buffer, tx_buffer, fc_buffer):
        notifier._bus_list = [self.mock_can_transport_interface.network_manager, Mock()]
        notifier.listeners = [rx_buffer, tx_buffer, fc_buffer]
        self.mock_can_transport_interface.notifier = notifier
        self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer = rx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer = tx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer = fc_buffer
        assert PythonCanTransportInterface.is_sync_active.fget(self.mock_can_transport_interface) is False

    # is_async_active

    def test_is_async_active__get__true(self):
        mock_bus = Mock()
        mock_rx_buffer = Mock(is_stopped=False)
        mock_tx_buffer = Mock(is_stopped=False)
        mock_fc_buffer = Mock(is_stopped=False)
        self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer = mock_rx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer = mock_tx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer = mock_fc_buffer
        self.mock_can_transport_interface.network_manager = mock_bus
        self.mock_can_transport_interface.async_notifier = Mock(
            stopped=False,
            _bus_list=[mock_bus],
            listeners=[mock_rx_buffer, mock_tx_buffer, mock_fc_buffer])
        assert PythonCanTransportInterface.is_async_active.fget(self.mock_can_transport_interface) is True

    def test_is_async_active__get__false__no_notifier(self):
        self.mock_can_transport_interface.notifier = None
        assert PythonCanTransportInterface.is_async_active.fget(self.mock_can_transport_interface) is False

    def test_is_async_active__get__false__wrong_bus(self):
        mock_rx_buffer = Mock(is_stopped=False)
        mock_tx_buffer = Mock(is_stopped=False)
        mock_fc_buffer = Mock(is_stopped=False)
        self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer = mock_rx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer = mock_tx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer = mock_fc_buffer
        self.mock_can_transport_interface.async_notifier = Mock(
            stopped=False,
            _bus_list=[Mock()],
            listeners=[mock_rx_buffer, mock_tx_buffer, mock_fc_buffer])
        assert PythonCanTransportInterface.is_async_active.fget(self.mock_can_transport_interface) is False

    @pytest.mark.parametrize("notifier, rx_buffer, tx_buffer, fc_buffer", [
        (Mock(stopped=True), Mock(is_stopped=False), Mock(is_stopped=False), Mock(is_stopped=False)),
        (Mock(stopped=False), Mock(is_stopped=True), Mock(is_stopped=False), Mock(is_stopped=False)),
        (Mock(stopped=False), Mock(is_stopped=False), Mock(is_stopped=True), Mock(is_stopped=False)),
        (Mock(stopped=False), Mock(is_stopped=False), Mock(is_stopped=False), Mock(is_stopped=True)),
    ])
    def test_is_async_active__get__false__stopped(self, notifier, rx_buffer, tx_buffer, fc_buffer):
        notifier._bus_list = [self.mock_can_transport_interface.network_manager, Mock()]
        notifier.listeners = [rx_buffer, tx_buffer, fc_buffer]
        self.mock_can_transport_interface.async_notifier = notifier
        self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer = rx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer = tx_buffer
        self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer = fc_buffer
        assert PythonCanTransportInterface.is_async_active.fget(self.mock_can_transport_interface) is False

    # setup_sync

    def test_setup_sync__no_notifier(self):
        self.mock_notifier.return_value = Mock(
            spec=Notifier,
            _bus_list=[self.mock_can_transport_interface.network_manager],
            listeners=[
                self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
                self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer,
                self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT
        )
        self.mock_can_transport_interface.notifier = None
        assert PythonCanTransportInterface.setup_sync(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface.notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_can_transport_interface.teardown_async.assert_called_once_with()
        self.mock_can_transport_interface.notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.notifier.add_listener.assert_not_called()

    def test_setup_sync__stopped_notifier(self):
        self.mock_notifier.return_value = Mock(
            spec=Notifier,
            _bus_list=[self.mock_can_transport_interface.network_manager],
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT
        )
        self.mock_can_transport_interface.notifier = Mock(
            spec=Notifier,
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=True
        )
        assert PythonCanTransportInterface.setup_sync(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface.notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_can_transport_interface.teardown_async.assert_called_once_with()
        self.mock_can_transport_interface.notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.notifier.add_listener.assert_not_called()

    def test_setup_sync__notifier_without_listeners(self):
        mock_notifier = Mock(
            spec=Notifier,
            _bus_list=[Mock(), self.mock_can_transport_interface.network_manager],
            listeners=[],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=False
        )
        self.mock_can_transport_interface.notifier = mock_notifier
        assert PythonCanTransportInterface.setup_sync(
            self.mock_can_transport_interface) is None
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface.teardown_async.assert_called_once_with()
        self.mock_can_transport_interface.notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.notifier.add_listener.assert_has_calls([
            call(self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer),
            call(self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer),
            call(self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer),
        ], any_order=True)

    def test_setup_sync__notifier_without_bus(self):
        mock_notifier = Mock(
            spec=Notifier,
            _bus_list=[],
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer
                       ],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=False
        )
        self.mock_can_transport_interface.notifier = mock_notifier
        assert PythonCanTransportInterface.setup_sync(
            self.mock_can_transport_interface) is None
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface.teardown_async.assert_called_once_with()
        self.mock_can_transport_interface.notifier.add_bus.assert_called_once_with(
            self.mock_can_transport_interface.network_manager)
        self.mock_can_transport_interface.notifier.add_listener.assert_not_called()

    # setup_async

    def test_setup_async__no_notifier(self):
        mock_loop = Mock()
        self.mock_notifier.return_value = Mock(
            spec=Notifier,
            _bus_list=[self.mock_can_transport_interface.network_manager],
            listeners=[self.mock_async_buffered_reader.return_value,
                       self.mock_async_buffered_reader.return_value,
                       self.mock_async_buffered_reader.return_value],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            _loop=mock_loop,
        )
        self.mock_can_transport_interface.async_notifier = None
        assert PythonCanTransportInterface.setup_async(
            self.mock_can_transport_interface,
            loop=mock_loop) is None
        assert self.mock_can_transport_interface.async_notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=mock_loop)
        self.mock_can_transport_interface.teardown_sync.assert_called_once_with()
        self.mock_can_transport_interface.async_notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.async_notifier.add_listener.assert_not_called()

    def test_setup_async__stopped_notifier(self):
        mock_loop = Mock()
        self.mock_notifier.return_value = Mock(
            spec=Notifier,
            _bus_list=[self.mock_can_transport_interface.network_manager],
            listeners=[self.mock_async_buffered_reader.return_value,
                       self.mock_async_buffered_reader.return_value,
                       self.mock_async_buffered_reader.return_value],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=self.mock_get_running_loop.return_value
        )
        self.mock_can_transport_interface.async_notifier = Mock(
            spec=Notifier,
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=True,
            _loop=mock_loop,
        )
        assert PythonCanTransportInterface.setup_async(
            self.mock_can_transport_interface,
            loop=mock_loop) is None
        assert self.mock_can_transport_interface.async_notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=mock_loop)
        self.mock_can_transport_interface.teardown_sync.assert_called_once_with()
        self.mock_can_transport_interface.async_notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.async_notifier.add_listener.assert_not_called()

    def test_setup_async__another_loop_in_notifier(self):
        mock_loop = Mock()
        self.mock_notifier.return_value = Mock(
            spec=Notifier,
            _bus_list=[self.mock_can_transport_interface.network_manager],
            listeners=[self.mock_async_buffered_reader.return_value,
                       self.mock_async_buffered_reader.return_value,
                       self.mock_async_buffered_reader.return_value],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=self.mock_get_running_loop.return_value
        )
        self.mock_can_transport_interface.async_notifier = Mock(
            spec=Notifier,
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=False,
            _loop=Mock(),
        )
        assert PythonCanTransportInterface.setup_async(
            self.mock_can_transport_interface,
            loop=mock_loop) is None
        assert self.mock_can_transport_interface.async_notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer,
                       self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=mock_loop)
        self.mock_can_transport_interface.teardown_sync.assert_called_once_with()
        self.mock_can_transport_interface.async_notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.async_notifier.add_listener.assert_not_called()

    def test_setup_async__notifier_without_listeners(self):
        mock_loop = Mock()
        mock_notifier = Mock(
            spec=Notifier,
            _bus_list=[self.mock_can_transport_interface.network_manager, Mock()],
            listeners=[],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=False,
            _loop=mock_loop,
        )
        self.mock_can_transport_interface.async_notifier = mock_notifier
        assert PythonCanTransportInterface.setup_async(
            self.mock_can_transport_interface,
            loop=mock_loop) is None
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface.teardown_sync.assert_called_once_with()
        self.mock_can_transport_interface.async_notifier.add_bus.assert_not_called()
        self.mock_can_transport_interface.async_notifier.add_listener.assert_has_calls([
            call(self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer),
            call(self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer),
            call(self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer),
        ], any_order=True)

    def test_setup_async__notifier_without_bus(self):
        mock_loop = Mock()
        mock_notifier = Mock(
            spec=Notifier,
            _bus_list=[],
            listeners=[
                self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
                self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer,
                self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer
            ],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            stopped=False,
            _loop=mock_loop,
        )
        self.mock_can_transport_interface.async_notifier = mock_notifier
        assert PythonCanTransportInterface.setup_async(
            self.mock_can_transport_interface,
            loop=mock_loop) is None
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface.teardown_sync.assert_called_once_with()
        self.mock_can_transport_interface.async_notifier.add_bus.assert_called_once_with(
            self.mock_can_transport_interface.network_manager)
        self.mock_can_transport_interface.async_notifier.add_listener.assert_not_called()

    # teardown_sync

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.teardown_sync")
    def test_teardown_sync__no_notifier(self, mock_teardown_sync):
        self.mock_can_transport_interface.notifier = None
        assert PythonCanTransportInterface.teardown_sync(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface.notifier is None
        mock_teardown_sync.assert_called_once_with(suppress_warning=False)
        self.mock_warn.assert_not_called()

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.teardown_sync")
    def test_teardown_sync__notifier(self, mock_teardown_sync):
        mock_notifier = Mock()
        self.mock_can_transport_interface.notifier = mock_notifier
        assert PythonCanTransportInterface.teardown_sync(self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface.notifier is None
        mock_notifier.stop.assert_called_once_with()
        mock_teardown_sync.assert_called_once_with(suppress_warning=False)
        self.mock_warn.assert_called_once()

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.teardown_sync")
    def test_teardown_sync__notifier_with_suppressed_warning(self, mock_teardown_sync):
        mock_notifier = Mock()
        self.mock_can_transport_interface.notifier = mock_notifier
        assert PythonCanTransportInterface.teardown_sync(
            self.mock_can_transport_interface, suppress_warning=True) is None
        assert self.mock_can_transport_interface.notifier is None
        mock_teardown_sync.assert_called_once_with(suppress_warning=True)
        mock_notifier.stop.assert_called_once_with()
        self.mock_warn.assert_not_called()

    # teardown_async

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.teardown_async")
    def test_teardown_async__no_notifier(self, mock_teardown_async):
        self.mock_can_transport_interface.async_notifier = None
        assert PythonCanTransportInterface.teardown_async(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface.async_notifier is None
        mock_teardown_async.assert_called_once_with(suppress_warning=False)
        self.mock_warn.assert_not_called()

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.teardown_async")
    def test_teardown_async__notifier(self, mock_teardown_async):
        mock_notifier = Mock()
        self.mock_can_transport_interface.async_notifier = mock_notifier
        assert PythonCanTransportInterface.teardown_async(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface.async_notifier is None
        mock_teardown_async.assert_called_once_with(suppress_warning=False)
        mock_notifier.stop.assert_called_once_with()
        self.mock_warn.assert_called_once()

    @patch(f"uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.teardown_async")
    def test_teardown_async__notifier_with_suppressed_warning(self, mock_teardown_async):
        mock_notifier = Mock()
        self.mock_can_transport_interface.async_notifier = mock_notifier
        assert PythonCanTransportInterface.teardown_async(
            self.mock_can_transport_interface, suppress_warning=True) is None
        assert self.mock_can_transport_interface.async_notifier is None
        mock_teardown_async.assert_called_once_with(suppress_warning=True)
        mock_notifier.stop.assert_called_once_with()
        self.mock_warn.assert_not_called()

    # _wait_for_flow_control

    @pytest.mark.parametrize("packet_records", [
        [Mock(spec=CanPacketRecord, addressing_type=Mock(), packet_type=Mock()),
         Mock(spec=CanPacketRecord, addressing_type=Mock(), packet_type=CanPacketType.FLOW_CONTROL),
         Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=Mock()),
         Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=CanPacketType.FLOW_CONTROL)],
        [Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=CanPacketType.FLOW_CONTROL)]
    ])
    def test_wait_for_flow_control(self, packet_records):
        self.mock_can_transport_interface._wait_for_rx_packet.side_effect = packet_records
        assert (PythonCanTransportInterface._wait_for_flow_control(
            self.mock_can_transport_interface,
            timeout_timestamp=MagicMock()) == packet_records[-1])

    # _async_wait_for_flow_control

    @pytest.mark.parametrize("packet_records", [
        [Mock(spec=CanPacketRecord, addressing_type=Mock(), packet_type=Mock()),
         Mock(spec=CanPacketRecord, addressing_type=Mock(), packet_type=CanPacketType.FLOW_CONTROL),
         Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=Mock()),
         Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=CanPacketType.FLOW_CONTROL)],
        [Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=CanPacketType.FLOW_CONTROL)]
    ])
    @pytest.mark.asyncio
    async def test_async_wait_for_flow_control(self, packet_records):
        self.mock_can_transport_interface._async_wait_for_rx_packet.side_effect = packet_records
        assert (await PythonCanTransportInterface._async_wait_for_flow_control(
            self.mock_can_transport_interface,
            timeout_timestamp=MagicMock()) == packet_records[-1])

    # _wait_for_rx_packet

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    def test_wait_for_rx_packet__timeout_error(self, timeout):
        mock_is_timeout_reached = Mock(side_effect=[False, True])
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        mock_get_message = Mock(return_value=None)
        mock_frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            PythonCanTransportInterface._wait_for_rx_packet(self.mock_can_transport_interface,
                                                            buffer=mock_frames_buffer,
                                                            timeout=timeout)
        mock_get_message.assert_called_once()
        assert mock_is_timeout_reached.call_count == 2

    @pytest.mark.parametrize("timeout", [None, 123.456])
    def test_wait_for_rx_packet__wall_time_timestamp(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        mock_frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = [self.mock_can_transport_interface.backend]
        assert (PythonCanTransportInterface._wait_for_rx_packet(self.mock_can_transport_interface,
                                                                buffer=mock_frames_buffer,
                                                                timeout=timeout)
                == self.mock_can_packet_record.return_value)
        self.mock_datetime.fromtimestamp.assert_called_once_with(mock_get_message.return_value.timestamp)
        self.mock_can_transport_interface.addressing_information.is_input_packet.assert_called_once_with(
            can_id=mock_get_message.return_value.arbitration_id,
            raw_frame_data=mock_get_message.return_value.data)
        self.mock_can_packet_record.assert_called_once_with(
            frame=mock_get_message.return_value,
            direction=TransmissionDirection.RECEIVED,
            addressing_type=self.mock_can_transport_interface.addressing_information.is_input_packet.return_value,
            addressing_format=self.mock_can_transport_interface.segmenter.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=mock_get_message.return_value.timestamp)

    @pytest.mark.parametrize("timeout", [None, 0.001])
    def test_wait_for_rx_packet__other_timestamp(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        mock_frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = []
        assert (PythonCanTransportInterface._wait_for_rx_packet(self.mock_can_transport_interface,
                                                                buffer=mock_frames_buffer,
                                                                timeout=timeout)
                == self.mock_can_packet_record.return_value)
        self.mock_datetime.now.assert_called_once_with()
        self.mock_can_transport_interface.addressing_information.is_input_packet.assert_called_once_with(
            can_id=mock_get_message.return_value.arbitration_id,
            raw_frame_data=mock_get_message.return_value.data)
        self.mock_can_packet_record.assert_called_once_with(
            frame=mock_get_message.return_value,
            direction=TransmissionDirection.RECEIVED,
            addressing_type=self.mock_can_transport_interface.addressing_information.is_input_packet.return_value,
            addressing_format=self.mock_can_transport_interface.segmenter.addressing_format,
            transmission_time=self.mock_datetime.now.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=mock_get_message.return_value.timestamp)

    # _async_wait_for_rx_packet

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_wait_for_rx_packet__timeout_error(self, timeout):
        mock_is_timeout_reached = Mock(side_effect=[False, True])
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        self.mock_can_transport_interface.addressing_information.is_input_packet.return_value = None
        with pytest.raises(TimeoutError):
            await PythonCanTransportInterface._async_wait_for_rx_packet(self.mock_can_transport_interface,
                                                                        buffer=Mock(get_message=Mock(side_effect=TimeoutError)),
                                                                        timeout=timeout)
        self.mock_can_transport_interface.addressing_information.is_input_packet.assert_not_called()
        assert mock_is_timeout_reached.call_count == 2

    @pytest.mark.parametrize("timeout", [None, 123.456])
    @pytest.mark.asyncio
    async def test_async_wait_for_rx_packet__wall_time_timestamp(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        mock_buffer = Mock(get_message=AsyncMock())
        self.mock_perf_counter.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=mock_is_timeout_reached)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = [self.mock_can_transport_interface.backend]
        assert (await PythonCanTransportInterface._async_wait_for_rx_packet(self.mock_can_transport_interface,
                                                                            buffer=mock_buffer,
                                                                            timeout=timeout)
                == self.mock_can_packet_record.return_value)
        mock_frame = mock_buffer.get_message.return_value
        self.mock_datetime.fromtimestamp.assert_called_once_with(mock_frame.timestamp)
        self.mock_can_transport_interface.addressing_information.is_input_packet.assert_called_once_with(
            can_id=mock_frame.arbitration_id,
            raw_frame_data=mock_frame.data)
        self.mock_can_packet_record.assert_called_once_with(
            frame=mock_frame,
            direction=TransmissionDirection.RECEIVED,
            addressing_type=self.mock_can_transport_interface.addressing_information.is_input_packet.return_value,
            addressing_format=self.mock_can_transport_interface.segmenter.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=mock_frame.timestamp)

    @pytest.mark.parametrize("timeout", [None, 0.001])
    @pytest.mark.asyncio
    async def test_async_wait_for_rx_packet__other_timestamp(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        mock_buffer = Mock(get_message=AsyncMock())
        self.mock_perf_counter.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=mock_is_timeout_reached)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = []
        assert (await PythonCanTransportInterface._async_wait_for_rx_packet(self.mock_can_transport_interface,
                                                                            buffer=mock_buffer,
                                                                            timeout=timeout)
                == self.mock_can_packet_record.return_value)
        mock_frame = mock_buffer.get_message.return_value
        self.mock_datetime.now.assert_called_once_with()
        self.mock_can_transport_interface.addressing_information.is_input_packet.assert_called_once_with(
            can_id=mock_frame.arbitration_id,
            raw_frame_data=mock_frame.data)
        self.mock_can_packet_record.assert_called_once_with(
            frame=mock_frame,
            direction=TransmissionDirection.RECEIVED,
            addressing_type=self.mock_can_transport_interface.addressing_information.is_input_packet.return_value,
            addressing_format=self.mock_can_transport_interface.segmenter.addressing_format,
            transmission_time=self.mock_datetime.now.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=mock_frame.timestamp)

    # _wait_for_tx_frame

    def test_wait_for_tx_frame__timeout(self):
        mock_is_timeout_reached = Mock(return_value=True)
        mock_timestamp = MagicMock(__sub__=lambda this, other: this,
                                    __add__=lambda this, other: this,
                                    __mul__=lambda this, other: this,
                                    __le__=mock_is_timeout_reached)
        with pytest.raises(TimeoutError):
            PythonCanTransportInterface._wait_for_tx_frame(self.mock_can_transport_interface,
                                                           buffer=Mock(),
                                                           frame=Mock(),
                                                           timestamp=mock_timestamp)
        mock_is_timeout_reached.assert_called_once()

    @pytest.mark.parametrize("can_frame, observed_can_frame", [
        (Mock(arbitration_id=0x123, data=[0x00, 0xFF]),
         Mock(arbitration_id=0x123, data=[0x00, 0xFF], is_rx=True)),
        (Mock(arbitration_id=1, data=(0x52, 0xFF, 0xC0)),
         Mock(arbitration_id=2, data=(0x52, 0xFF, 0xC0), is_rx=False)),
        (Mock(arbitration_id=0x7DF, data=[1, 2, 3, 4]),
         Mock(arbitration_id=0x7DF, data=[5, 6, 7, 8], is_rx=False)),
    ])
    def test_wait_for_tx_frame__other_then_timeout(self, can_frame, observed_can_frame):
        mock_buffer = Mock(get_message=Mock(return_value=observed_can_frame))
        mock_is_timeout_reached = Mock(side_effect=[False, True])
        mock_timestamp = MagicMock(__sub__=lambda this, other: this,
                                    __add__=lambda this, other: this,
                                    __mul__=lambda this, other: this,
                                    __le__=mock_is_timeout_reached)
        with pytest.raises(TimeoutError):
            PythonCanTransportInterface._wait_for_tx_frame(self.mock_can_transport_interface,
                                                           buffer=mock_buffer,
                                                           frame=can_frame,
                                                           timestamp=mock_timestamp)
        assert mock_is_timeout_reached.call_count == 2
        mock_buffer.get_message.assert_called_once()

    @pytest.mark.parametrize("can_frame, observed_can_frame", [
        (Mock(arbitration_id=0x123, data=[0x00, 0xFF]),
         Mock(arbitration_id=0x123, data=[0x00, 0xFF], is_rx=False)),
        (Mock(arbitration_id=0xF6B26, data=[0x12, 0x34, 0x56, 0x78, 0x9A]),
         Mock(arbitration_id=0xF6B26, data=[0x12, 0x34, 0x56, 0x78, 0x9A], is_rx=False)),
    ])
    def test_wait_for_tx_frame__valid(self, can_frame, observed_can_frame):
        mock_buffer = Mock(get_message=Mock(return_value=observed_can_frame))
        mock_is_timeout_reached = Mock(return_value=False)
        mock_timestamp = MagicMock(__sub__=lambda this, other: this,
                                    __add__=lambda this, other: this,
                                    __mul__=lambda this, other: this,
                                    __le__=mock_is_timeout_reached)
        assert PythonCanTransportInterface._wait_for_tx_frame(self.mock_can_transport_interface,
                                                              buffer=mock_buffer,
                                                              frame=can_frame,
                                                              timestamp=mock_timestamp) == observed_can_frame
        assert mock_is_timeout_reached.call_count == 1
        mock_buffer.get_message.assert_called_once()

    # _async_wait_for_tx_frame

    @pytest.mark.asyncio
    async def test_async_wait_for_tx_frame__timeout(self):
        mock_is_timeout_reached = Mock(return_value=True)
        mock_timestamp = MagicMock(__sub__=lambda this, other: this,
                                   __add__=lambda this, other: this,
                                   __mul__=lambda this, other: this,
                                   __le__=mock_is_timeout_reached)
        with pytest.raises(TimeoutError):
            await PythonCanTransportInterface._async_wait_for_tx_frame(self.mock_can_transport_interface,
                                                                       buffer=Mock(),
                                                                       frame=Mock(),
                                                                       timestamp=mock_timestamp)
        mock_is_timeout_reached.assert_called_once()

    @pytest.mark.parametrize("can_frame, observed_can_frame", [
        (Mock(arbitration_id=0x123, data=[0x00, 0xFF]),
         Mock(arbitration_id=0x123, data=[0x00, 0xFF], is_rx=True)),
        (Mock(arbitration_id=1, data=(0x52, 0xFF, 0xC0)),
         Mock(arbitration_id=2, data=(0x52, 0xFF, 0xC0), is_rx=False)),
        (Mock(arbitration_id=0x7DF, data=[1, 2, 3, 4]),
         Mock(arbitration_id=0x7DF, data=[5, 6, 7, 8], is_rx=False)),
    ])
    @pytest.mark.asyncio
    async def test_async_wait_for_tx_frame__other_then_timeout(self, can_frame, observed_can_frame):
        mock_is_timeout_reached = Mock(side_effect=[False, True])
        mock_timestamp = MagicMock(__sub__=lambda this, other: this,
                                   __add__=lambda this, other: this,
                                   __mul__=lambda this, other: this,
                                   __le__=mock_is_timeout_reached)
        with pytest.raises(TimeoutError):
            await PythonCanTransportInterface._async_wait_for_tx_frame(
                self.mock_can_transport_interface,
                buffer=Mock(get_message=AsyncMock(return_value=observed_can_frame)),
                frame=can_frame,
                timestamp=mock_timestamp)
        assert mock_is_timeout_reached.call_count == 2

    @pytest.mark.parametrize("can_frame, observed_can_frame", [
        (Mock(arbitration_id=0x123, data=[0x00, 0xFF]),
         Mock(arbitration_id=0x123, data=[0x00, 0xFF], is_rx=False, timestamp=100.111)),
        (Mock(arbitration_id=0xF6B26, data=[0x12, 0x34, 0x56, 0x78, 0x9A]),
         Mock(arbitration_id=0xF6B26, data=[0x12, 0x34, 0x56, 0x78, 0x9A], is_rx=False, timestamp=100.211)),
    ])
    @pytest.mark.asyncio
    async def test_async_wait_for_tx_frame__valid(self, can_frame, observed_can_frame):
        mock_is_timeout_reached = Mock(return_value=False)
        mock_timestamp = MagicMock(__sub__=lambda this, other: this,
                                   __add__=lambda this, other: this,
                                   __mul__=lambda this, other: this,
                                   __le__=mock_is_timeout_reached)
        mock_buffer = Mock(get_message=AsyncMock(return_value=observed_can_frame))
        assert await PythonCanTransportInterface._async_wait_for_tx_frame(
            self.mock_can_transport_interface,
            buffer=mock_buffer,
            frame=can_frame,
            timestamp=mock_timestamp) == observed_can_frame
        assert mock_is_timeout_reached.call_count == 1

    # clear_received_frame_buffers

    @pytest.mark.parametrize("async_queue_size, sync_queue_size", [
        (0, 0),
        (1, 25),
        (69, 3),
    ])
    def test_clear_received_frame_buffers(self, sync_queue_size, async_queue_size):
        sync_get_nowait = Mock()
        async_get_nowait = Mock()
        mock_sync_queue = Mock(empty=Mock(side_effect=[False] * sync_queue_size + [True]),
                               get_nowait=sync_get_nowait)
        mock_async_queue = Mock(empty=Mock(side_effect=[False] * async_queue_size + [True]),
                                get_nowait=async_get_nowait)
        self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer = Mock(buffer=mock_sync_queue)
        self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer = Mock(
            buffer=mock_async_queue)
        assert PythonCanTransportInterface.clear_received_frame_buffers(self.mock_can_transport_interface) is None
        assert sync_get_nowait.call_count == sync_queue_size
        assert async_get_nowait.call_count == async_queue_size

    # clear_transmitted_frame_buffers

    @pytest.mark.parametrize("async_queue_size, sync_queue_size", [
        (0, 0),
        (1, 25),
        (69, 3),
    ])
    def test_clear_transmitted_frame_buffers(self, sync_queue_size, async_queue_size):
        sync_get_nowait = Mock()
        async_get_nowait = Mock()
        mock_sync_queue = Mock(empty=Mock(side_effect=[False] * sync_queue_size + [True]),
                               get_nowait=sync_get_nowait)
        mock_async_queue = Mock(empty=Mock(side_effect=[False] * async_queue_size + [True]),
                                get_nowait=async_get_nowait)
        self.mock_can_transport_interface._PythonCanTransportInterface__tx_frames_buffer = Mock(buffer=mock_sync_queue)
        self.mock_can_transport_interface._PythonCanTransportInterface__async_tx_frames_buffer = Mock(
            buffer=mock_async_queue)
        assert PythonCanTransportInterface.clear_transmitted_frame_buffers(self.mock_can_transport_interface) is None
        assert mock_sync_queue.get_nowait.call_count == sync_queue_size
        assert mock_async_queue.get_nowait.call_count == async_queue_size

    # clear_flow_control_frame_buffers

    @pytest.mark.parametrize("async_queue_size, sync_queue_size", [
        (0, 0),
        (1, 25),
        (69, 3),
    ])
    def test_clear_flow_control_frame_buffers(self, sync_queue_size, async_queue_size):
        sync_get_nowait = Mock()
        async_get_nowait = Mock()
        mock_sync_queue = Mock(empty=Mock(side_effect=[False] * sync_queue_size + [True]),
                               get_nowait=sync_get_nowait)
        mock_async_queue = Mock(empty=Mock(side_effect=[False] * async_queue_size + [True]),
                                get_nowait=async_get_nowait)
        self.mock_can_transport_interface._PythonCanTransportInterface__fc_frames_buffer = Mock(buffer=mock_sync_queue)
        self.mock_can_transport_interface._PythonCanTransportInterface__async_fc_frames_buffer = Mock(
            buffer=mock_async_queue)
        assert PythonCanTransportInterface.clear_flow_control_frame_buffers(self.mock_can_transport_interface) is None
        assert mock_sync_queue.get_nowait.call_count == sync_queue_size
        assert mock_async_queue.get_nowait.call_count == async_queue_size

    # is_supported_network_manager

    @pytest.mark.parametrize("value", ["something", Mock(spec=BusABC)])
    def test_is_supported_network_manager__false(self, value):
        assert PythonCanTransportInterface.is_supported_network_manager(value) is False

    @pytest.mark.parametrize("value", [Mock(spec=KvaserBus), Mock(spec=VectorBus), Mock(spec=VirtualBus)])
    def test_is_supported_network_manager__true(self, value):
        assert PythonCanTransportInterface.is_supported_network_manager(value) is True

    # send_packet

    @pytest.mark.parametrize("packet", ["something", MagicMock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_send_packet__type_error(self, mock_isinstance, packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PythonCanTransportInterface.send_packet(self.mock_can_transport_interface, packet)
        mock_isinstance.assert_called_once_with(packet, CanPacket)

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    def test_send_packet__observed(self, packet):
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            timeout = self.mock_can_transport_interface.n_ar_timeout / 1000.
        else:
            timeout = self.mock_can_transport_interface.n_as_timeout / 1000.
        sent_can_frame = self.mock_can_transport_interface._wait_for_tx_frame.return_value
        mock_is_wall_time_used = Mock(return_value=True)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = MagicMock(
            __contains__=mock_is_wall_time_used)
        assert (PythonCanTransportInterface.send_packet(self.mock_can_transport_interface, packet)
                == self.mock_can_packet_record.return_value)
        self.mock_can_transport_interface.clear_transmitted_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_python_can_frame.assert_called_once_with(
            arbitration_id=packet.can_id,
            is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
            data=packet.raw_frame_data,
            is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value,
            bitrate_switch=self.mock_can_transport_interface.bitrate_switch,
            is_rx=False,
            is_error_frame=False,
            is_remote_frame=False)
        self.mock_can_transport_interface.network_manager.send.assert_called_once_with(
            msg=self.mock_python_can_frame.return_value,
            timeout=timeout)
        mock_is_wall_time_used.assert_called_once_with(self.mock_can_transport_interface.backend)
        self.mock_datetime.fromtimestamp.assert_called_once_with(sent_can_frame.timestamp)
        self.mock_can_packet_record.assert_called_once_with(
            frame=sent_can_frame,
            direction=TransmissionDirection.TRANSMITTED,
            addressing_type=packet.addressing_type,
            addressing_format=packet.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=sent_can_frame.timestamp)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            self.mock_can_transport_interface._update_n_ar_measured.assert_called_once()
            self.mock_can_transport_interface._update_n_as_measured.assert_not_called()
        else:
            self.mock_can_transport_interface._update_n_ar_measured.assert_not_called()
            self.mock_can_transport_interface._update_n_as_measured.assert_called_once()

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    def test_send_packet__not_observed(self, packet):
        self.mock_can_transport_interface._wait_for_tx_frame.side_effect = TimeoutError
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            timeout = self.mock_can_transport_interface.n_ar_timeout / 1000.
        else:
            timeout = self.mock_can_transport_interface.n_as_timeout / 1000.
        sent_can_frame = self.mock_python_can_frame.return_value
        mock_is_wall_time_used = Mock(return_value=False)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = MagicMock(
            __contains__=mock_is_wall_time_used)
        assert (PythonCanTransportInterface.send_packet(self.mock_can_transport_interface, packet)
                == self.mock_can_packet_record.return_value)
        self.mock_can_transport_interface.clear_transmitted_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_python_can_frame.assert_has_calls([
            call(arbitration_id=packet.can_id,
                 is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                 data=packet.raw_frame_data,
                 is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value,
                 bitrate_switch=self.mock_can_transport_interface.bitrate_switch,
                 is_rx=False,
                 is_error_frame=False,
                 is_remote_frame=False),
            call(arbitration_id=self.mock_python_can_frame.return_value.arbitration_id,
                 is_extended_id=self.mock_python_can_frame.return_value.is_extended_id,
                 data=self.mock_python_can_frame.return_value.data,
                 bitrate_switch=self.mock_python_can_frame.return_value.bitrate_switch,
                 is_fd=self.mock_python_can_frame.return_value.is_fd,
                 is_rx=False,
                 is_error_frame=False,
                 is_remote_frame=False,
                 timestamp=self.mock_can_transport_interface.time_sync.perf_counter_to_time.return_value)],
            any_order=False)
        self.mock_can_transport_interface.network_manager.send.assert_called_once_with(
            msg=self.mock_python_can_frame.return_value,
            timeout=timeout)
        self.mock_datetime.fromtimestamp.assert_called_once_with(
            self.mock_can_transport_interface.time_sync.perf_counter_to_time.return_value)
        self.mock_can_packet_record.assert_called_once_with(
            frame=sent_can_frame,
            direction=TransmissionDirection.TRANSMITTED,
            addressing_type=packet.addressing_type,
            addressing_format=packet.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=sent_can_frame.timestamp)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            self.mock_can_transport_interface._update_n_ar_measured.assert_called_once()
            self.mock_can_transport_interface._update_n_as_measured.assert_not_called()
        else:
            self.mock_can_transport_interface._update_n_ar_measured.assert_not_called()
            self.mock_can_transport_interface._update_n_as_measured.assert_called_once()

    # async_send_packet

    @pytest.mark.parametrize("packet", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_send_packet__type_error(self, mock_isinstance, packet):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            await PythonCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet)
        mock_isinstance.assert_called_once_with(packet, CanPacket)

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet__observed(self, packet):
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            timeout = self.mock_can_transport_interface.n_ar_timeout / 1000.
        else:
            timeout = self.mock_can_transport_interface.n_as_timeout / 1000.
        sent_can_frame = self.mock_can_transport_interface._async_wait_for_tx_frame.return_value
        mock_is_wall_time_used = Mock(return_value=True)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = MagicMock(
            __contains__=mock_is_wall_time_used)
        assert (await PythonCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet)
                == self.mock_can_packet_record.return_value)
        self.mock_can_transport_interface.clear_transmitted_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            loop=self.mock_get_running_loop.return_value)
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_python_can_frame.assert_called_once_with(
            arbitration_id=packet.can_id,
            is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
            data=packet.raw_frame_data,
            is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value,
            bitrate_switch=self.mock_can_transport_interface.bitrate_switch,
            is_rx=False,
            is_error_frame=False,
            is_remote_frame=False)
        self.mock_can_transport_interface.network_manager.send.assert_called_once_with(
            msg=self.mock_python_can_frame.return_value,
            timeout=timeout)
        mock_is_wall_time_used.assert_called_once_with(self.mock_can_transport_interface.backend)
        self.mock_datetime.fromtimestamp.assert_called_once_with(sent_can_frame.timestamp)
        self.mock_can_packet_record.assert_called_once_with(
            frame=sent_can_frame,
            direction=TransmissionDirection.TRANSMITTED,
            addressing_type=packet.addressing_type,
            addressing_format=packet.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=sent_can_frame.timestamp)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            self.mock_can_transport_interface._update_n_ar_measured.assert_called_once()
            self.mock_can_transport_interface._update_n_as_measured.assert_not_called()
        else:
            self.mock_can_transport_interface._update_n_ar_measured.assert_not_called()
            self.mock_can_transport_interface._update_n_as_measured.assert_called_once()

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet__not_observed(self, packet):
        self.mock_can_transport_interface._async_wait_for_tx_frame.side_effect = TimeoutError
        mock_loop = Mock(spec=AbstractEventLoop)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            timeout = self.mock_can_transport_interface.n_ar_timeout / 1000.
        else:
            timeout = self.mock_can_transport_interface.n_as_timeout / 1000.
        sent_can_frame = self.mock_python_can_frame.return_value
        mock_is_wall_time_used = Mock(return_value=False)
        self.mock_can_transport_interface._INTERFACES_USING_WALL_TIME_TIMESTAMPS = MagicMock(
            __contains__=mock_is_wall_time_used)
        assert (await PythonCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet, loop=mock_loop)
                == self.mock_can_packet_record.return_value)
        self.mock_can_transport_interface.clear_transmitted_frame_buffers.assert_called_once_with()
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            loop=mock_loop)
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_python_can_frame.assert_has_calls([
            call(arbitration_id=packet.can_id,
                 is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                 data=packet.raw_frame_data,
                 is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value,
                 bitrate_switch=self.mock_can_transport_interface.bitrate_switch,
                 is_rx=False,
                 is_error_frame=False,
                 is_remote_frame=False),
            call(arbitration_id=self.mock_python_can_frame.return_value.arbitration_id,
                 is_extended_id=self.mock_python_can_frame.return_value.is_extended_id,
                 data=self.mock_python_can_frame.return_value.data,
                 bitrate_switch=self.mock_python_can_frame.return_value.bitrate_switch,
                 is_fd=self.mock_python_can_frame.return_value.is_fd,
                 is_rx=False,
                 is_error_frame=False,
                 is_remote_frame=False,
                 timestamp=self.mock_can_transport_interface.time_sync.perf_counter_to_time.return_value)],
            any_order=False)
        self.mock_can_transport_interface.network_manager.send.assert_called_once_with(
            msg=self.mock_python_can_frame.return_value,
            timeout=timeout)
        self.mock_datetime.fromtimestamp.assert_called_once_with(
            self.mock_can_transport_interface.time_sync.perf_counter_to_time.return_value)
        self.mock_can_packet_record.assert_called_once_with(
            frame=sent_can_frame,
            direction=TransmissionDirection.TRANSMITTED,
            addressing_type=packet.addressing_type,
            addressing_format=packet.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value,
            transmission_timestamp=self.mock_perf_counter.return_value,
            transmission_native_timestamp=sent_can_frame.timestamp)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            self.mock_can_transport_interface._update_n_ar_measured.assert_called_once()
            self.mock_can_transport_interface._update_n_as_measured.assert_not_called()
        else:
            self.mock_can_transport_interface._update_n_ar_measured.assert_not_called()
            self.mock_can_transport_interface._update_n_as_measured.assert_called_once()

    # receive_packet

    @pytest.mark.parametrize("timeout", [Mock(), 123.456])
    def test_receive_packet(self, timeout):
        assert (PythonCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
                == self.mock_can_transport_interface._wait_for_rx_packet.return_value)
        self.mock_validate_timeout.assert_called_once_with(timeout)
        self.mock_can_transport_interface._wait_for_rx_packet.assert_called_once_with(
            buffer=self.mock_can_transport_interface._PythonCanTransportInterface__rx_frames_buffer,
            timeout=timeout)
        self.mock_can_transport_interface.setup_sync.assert_called_once_with()
        self.mock_can_transport_interface.setup_async.assert_not_called()

    # async_receive_packet

    @pytest.mark.parametrize("timeout, loop", [
        (Mock(), None),
        (123.456, Mock(spec=AbstractEventLoop)),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet(self, timeout, loop):
        assert (await PythonCanTransportInterface.async_receive_packet(self.mock_can_transport_interface,
                                                                       timeout=timeout,
                                                                       loop=loop)
                == self.mock_can_transport_interface._async_wait_for_rx_packet.return_value)
        self.mock_validate_timeout.assert_called_once_with(timeout)
        self.mock_can_transport_interface._async_wait_for_rx_packet.assert_called_once_with(
            buffer=self.mock_can_transport_interface._PythonCanTransportInterface__async_rx_frames_buffer,
            timeout=timeout)
        self.mock_can_transport_interface.setup_sync.assert_not_called()
        self.mock_can_transport_interface.setup_async.assert_called_once_with(
            loop=loop if loop is not None else self.mock_get_running_loop.return_value)


@pytest.mark.performance
class TestPythonCanTransportInterfacePerformance:
    """Performance tests for `PythonCanTransportInterface` class."""

    REPETITIONS = 100

    def setup_method(self):
        self.mock_can_transport_interface = MagicMock(spec=PythonCanTransportInterface,
                                                      _PythonCanTransportInterface__rx_frames_buffer=Mock(),
                                                      _PythonCanTransportInterface__fc_frames_buffer=Mock(),
                                                      _PythonCanTransportInterface__async_rx_frames_buffer=Mock(),
                                                      _PythonCanTransportInterface__async_fc_frames_buffer=Mock())
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_get_running_loop = patch(f"{SCRIPT_LOCATION}.get_running_loop")
        self.mock_get_running_loop = self._patcher_get_running_loop.start()
        self._patcher_datetime = patch(f"{SCRIPT_LOCATION}.datetime")
        self.mock_datetime = self._patcher_datetime.start()
        self._pather_can_packet_record = patch(f"{SCRIPT_LOCATION}.CanPacketRecord")
        self.mock_can_packet_record = self._pather_can_packet_record.start()

    def teardown_method(self):
        self._patcher_warn.stop()
        self._patcher_get_running_loop.stop()
        self._patcher_datetime.stop()
        self._pather_can_packet_record.stop()

    # _wait_for_rx_packet

    @pytest.mark.parametrize("timeout", [10, 75])
    def test_wait_for_rx_packet__timeout(self,
                                         performance_tolerance_ms, mean_performance_tolerance_ms,
                                         timeout):
        def _get_message(*_, **__):
            sleep(0.005)
            return Mock()

        mock_buffer = Mock(spec=BufferedReader,
                           get_message=_get_message)
        self.mock_can_transport_interface.addressing_information.is_input_packet.return_value = None

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                PythonCanTransportInterface._wait_for_rx_packet(self.mock_can_transport_interface,
                                                                buffer=mock_buffer,
                                                                timeout=timeout)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (timeout
                    <= execution_time_ms
                    <= timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (timeout
                <= mean_execution_time_ms
                <= timeout + mean_performance_tolerance_ms)

    # _async_wait_for_rx_packet

    @pytest.mark.parametrize("timeout", [10, 75])
    @pytest.mark.asyncio
    async def test_async_wait_for_rx_packet__timeout(self,
                                                     performance_tolerance_ms, mean_performance_tolerance_ms,
                                                     timeout):
        async def _get_message(*_, **__):
            await asyncio_sleep(0.005)
            return Mock()

        mock_buffer = Mock(spec=AsyncBufferedReader,
                           get_message=_get_message)
        self.mock_can_transport_interface.addressing_information.is_input_packet.return_value = None

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                await PythonCanTransportInterface._async_wait_for_rx_packet(self.mock_can_transport_interface,
                                                                            buffer=mock_buffer,
                                                                            timeout=timeout)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (timeout
                    <= execution_time_ms
                    <= timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (timeout
                <= mean_execution_time_ms
                <= timeout + mean_performance_tolerance_ms)

    # _receive_cf_packets_block

    @pytest.mark.parametrize("n_cr_timeout", [10, 75])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
    def test_receive_cf_packets_block__n_cr_timeout(self, mock_is_initial_packet_type,
                                                    performance_tolerance_ms, mean_performance_tolerance_ms,
                                                    n_cr_timeout):
        def _get_packet_record(*_, **__):
            sleep(0.005)
            return Mock(spec=CanPacketRecord,
                        packet_type=Mock())

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.receive_packet.side_effect = _get_packet_record
        self.mock_can_transport_interface.n_cr_timeout = n_cr_timeout

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                PythonCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                      sequence_number=Mock(),
                                                                      block_size=float("inf"),
                                                                      remaining_data_length=float("inf"),
                                                                      timestamp_end=None)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (n_cr_timeout
                    <= execution_time_ms
                    <= n_cr_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (n_cr_timeout
                <= mean_execution_time_ms
                <= n_cr_timeout + mean_performance_tolerance_ms)

    @pytest.mark.parametrize("timeout_end", [10, 75])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
    def test_receive_cf_packets_block__end_timeout(self, mock_is_initial_packet_type,
                                                   performance_tolerance_ms, mean_performance_tolerance_ms,
                                                   timeout_end):
        current_sn = 0

        def _get_packet_record(*_, **__):
            nonlocal current_sn
            current_sn = (current_sn + 1) & 0xF
            sleep(0.005)
            return Mock(spec=CanPacketRecord,
                        packet_type=CanPacketType.CONSECUTIVE_FRAME,
                        sequence_number=current_sn,
                        payload=[0x12])

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.receive_packet.side_effect = _get_packet_record
        self.mock_can_transport_interface.n_cr_timeout = 1000
        sequence_number = 1

        diff_times = []
        for _ in range(self.REPETITIONS):
            current_sn = 0
            timestamp_end = perf_counter() + timeout_end / 1000.
            with pytest.raises(TimeoutError):
                PythonCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                      sequence_number=sequence_number,
                                                                      block_size=float("inf"),
                                                                      remaining_data_length=float("inf"),
                                                                      timestamp_end=timestamp_end)
            timestamp_after = perf_counter()
            diff_times.append(abs(timestamp_after - timestamp_end) * 1000.)
            assert (timestamp_end
                    <= timestamp_after
                    <= timestamp_end + performance_tolerance_ms / 1000.)

        mean_diff_time_ms = sum(diff_times) / len(diff_times)
        assert (0
                <= mean_diff_time_ms
                <= mean_performance_tolerance_ms)

    # _async_receive_cf_packets_block

    @pytest.mark.parametrize("n_cr_timeout", [10, 75])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__n_cr_timeout(self, mock_is_initial_packet_type,
                                                                performance_tolerance_ms, mean_performance_tolerance_ms,
                                                                n_cr_timeout):
        async def _get_packet_record(*_, **__):
            await asyncio_sleep(0.005)
            return Mock(spec=CanPacketRecord,
                        packet_type=Mock())

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.async_receive_packet.side_effect = _get_packet_record
        self.mock_can_transport_interface.n_cr_timeout = n_cr_timeout
        mock_loop = Mock()

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                await PythonCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
                                                                                  sequence_number=Mock(),
                                                                                  block_size=float("inf"),
                                                                                  remaining_data_length=float("inf"),
                                                                                  timestamp_end=None,
                                                                                  loop=mock_loop)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (n_cr_timeout
                    <= execution_time_ms
                    <= n_cr_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (n_cr_timeout
                <= mean_execution_time_ms
                <= n_cr_timeout + mean_performance_tolerance_ms)

    @pytest.mark.parametrize("timeout_end", [10, 75])
    @patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__end_timeout(self, mock_is_initial_packet_type,
                                                               performance_tolerance_ms, mean_performance_tolerance_ms,
                                                               timeout_end):
        current_sn = 0

        async def _get_packet_record(*_, **__):
            nonlocal current_sn
            current_sn = (current_sn + 1) & 0xF
            await asyncio_sleep(0.005)
            return Mock(spec=CanPacketRecord,
                        packet_type=CanPacketType.CONSECUTIVE_FRAME,
                        sequence_number=current_sn,
                        payload=[0x12])

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.async_receive_packet.side_effect = _get_packet_record
        self.mock_can_transport_interface.n_cr_timeout = 1000
        sequence_number = 1
        mock_loop = Mock()

        diff_times = []
        for _ in range(self.REPETITIONS):
            current_sn = 0
            timestamp_end = perf_counter() + timeout_end / 1000.
            with pytest.raises(TimeoutError):
                await PythonCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
                                                                                  sequence_number=sequence_number,
                                                                                  block_size=float("inf"),
                                                                                  remaining_data_length=float("inf"),
                                                                                  timestamp_end=timestamp_end,
                                                                                  loop=mock_loop)
            timestamp_after = perf_counter()
            diff_times.append(abs(timestamp_after - timestamp_end) * 1000.)
            assert (timestamp_end
                    <= timestamp_after
                    <= timestamp_end + performance_tolerance_ms / 1000.)

        mean_diff_time_ms = sum(diff_times) / len(diff_times)
        assert (0
                <= mean_diff_time_ms
                <= mean_performance_tolerance_ms)

    # _receive_consecutive_frames

    @pytest.mark.parametrize("end_timeout", [10, 75])
    def test_receive_consecutive_frames__end_timeout(self, end_timeout,
                                                     performance_tolerance_ms, mean_performance_tolerance_ms):
        current_sn = 0

        def _get_packet_record(*_, **__):
            nonlocal current_sn
            current_sn = (current_sn + 1) & 0xF
            sleep(0.005)
            return [Mock(spec=CanPacketRecord,
                         packet_type=CanPacketType.CONSECUTIVE_FRAME,
                         sequence_number=current_sn,
                         transmission_time=datetime.now(),
                         transmission_timestamp=perf_counter(),
                         payload=[0x12])]

        mock_first_frame = MagicMock(spec=CanPacketRecord,
                                     data_length=float("inf"),
                                     payload=[],
                                     transmission_time=datetime.now(),
                                     transmission_timestamp=perf_counter())
        self.mock_can_transport_interface.receive_packet.side_effect = TimeoutError
        self.mock_can_transport_interface.flow_control_parameters_generator = DefaultFlowControlParametersGenerator(
            block_size=1,
            st_min=1)
        self.mock_can_transport_interface._receive_cf_packets_block.side_effect = _get_packet_record
        self.mock_can_transport_interface.n_br = 1000

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                PythonCanTransportInterface._receive_consecutive_frames(
                    self.mock_can_transport_interface,
                    first_frame=mock_first_frame,
                    timestamp_end=timestamp_before + end_timeout / 1000.)
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (end_timeout
                    <= execution_time_ms
                    <= end_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (end_timeout
                <= mean_execution_time_ms
                <= end_timeout + mean_performance_tolerance_ms)

    # _async_receive_consecutive_frames

    @pytest.mark.parametrize("end_timeout", [10, 75])
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__end_timeout(self, end_timeout,
                                                                 performance_tolerance_ms,
                                                                 mean_performance_tolerance_ms):
        current_sn = 0

        async def _get_packet_record(*_, **__):
            nonlocal current_sn
            current_sn = (current_sn + 1) & 0xF
            await asyncio_sleep(0.005)
            return [Mock(spec=CanPacketRecord,
                         packet_type=CanPacketType.CONSECUTIVE_FRAME,
                         sequence_number=current_sn,
                         transmission_time=datetime.now(),
                         transmission_timestamp=perf_counter(),
                         payload=[0x12])]

        mock_first_frame = MagicMock(spec=CanPacketRecord,
                                     data_length=float("inf"),
                                     payload=[],
                                     transmission_time=datetime.now(),
                                     transmission_timestamp=perf_counter())
        self.mock_can_transport_interface.async_receive_packet.side_effect = TimeoutError
        self.mock_can_transport_interface.flow_control_parameters_generator = DefaultFlowControlParametersGenerator(
            block_size=1,
            st_min=1)
        self.mock_can_transport_interface._async_receive_cf_packets_block.side_effect = _get_packet_record
        self.mock_can_transport_interface.n_br = 1000

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(TimeoutError):
                await PythonCanTransportInterface._async_receive_consecutive_frames(
                    self.mock_can_transport_interface,
                    first_frame=mock_first_frame,
                    timestamp_end=timestamp_before + end_timeout / 1000.,
                    loop=get_running_loop())
            timestamp_after = perf_counter()
            execution_time_ms = (timestamp_after - timestamp_before) * 1000.
            execution_times.append(execution_time_ms)
            assert (end_timeout
                    <= execution_time_ms
                    <= end_timeout + performance_tolerance_ms)

        mean_execution_time_ms = sum(execution_times) / len(execution_times)
        assert (end_timeout
                <= mean_execution_time_ms
                <= end_timeout + mean_performance_tolerance_ms)


@pytest.mark.integration
class TestPythonCanTransportInterfaceIntegration:
    """Integration tests for `PythonCanTransportInterface` class."""

    # __init__

    @pytest.mark.parametrize("init_kwargs", [
        {
            "network_manager": Bus("test1", interface="virtual"),
        },
        {
            "network_manager": Bus("test2", interface="virtual"),
            "n_as_timeout": 0.1,
            "n_ar_timeout": 987,
            "n_bs_timeout": 43,
            "n_cr_timeout": 98.32,
            "n_br": 5.3,
            "n_cs": 0.92,
            "use_data_optimization": True,
            "filler_byte": 0x00,
            "flow_control_parameters_generator": DefaultFlowControlParametersGenerator(block_size=10,
                                                                                       st_min=50,
                                                                                       wait_count=1,
                                                                                       repeat_wait=True)
        },
    ])
    def test_init(self, init_kwargs, example_can_addressing_information):
        py_can_ti = PythonCanTransportInterface(**init_kwargs, addressing_information=example_can_addressing_information)
        assert py_can_ti.network_manager == init_kwargs["network_manager"]
        assert py_can_ti.addressing_information == example_can_addressing_information
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
        assert py_can_ti.use_data_optimization == init_kwargs.get("use_data_optimization", False)
        assert py_can_ti.filler_byte == init_kwargs.get("filler_byte", DEFAULT_FILLER_BYTE)
        assert (py_can_ti.flow_control_parameters_generator
                == init_kwargs.get("flow_control_parameters_generator",
                                   AbstractCanTransportInterface.DEFAULT_FLOW_CONTROL_PARAMETERS))

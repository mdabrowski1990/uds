from asyncio import get_running_loop
from asyncio import sleep as asyncio_sleep
from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from datetime import datetime
from random import randint
from time import perf_counter, sleep

import pytest
from mock import AsyncMock, MagicMock, Mock, call, patch

from can import Bus
from uds.addressing import AddressingType
from uds.can import DEFAULT_FILLER_BYTE, CanAddressingInformation, DefaultFlowControlParametersGenerator
from uds.can.transport_interface.python_can import (
    AbstractCanTransportInterface,
    AbstractEventLoop,
    AsyncBufferedReader,
    BufferedReader,
    BusABC,
    CanFlowStatus,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    MessageTransmissionNotStartedError,
    PyCanTransportInterface,
    TransmissionDirection,
    UdsMessage,
)

SCRIPT_LOCATION = "uds.can.transport_interface.python_can"


class TestPyCanTransportInterface:
    """Unit tests for `PyCanTransportInterface` class."""

    def setup_method(self):
        self.mock_can_transport_interface = MagicMock(spec=PyCanTransportInterface,
                                                      _PyCanTransportInterface__rx_frames_buffer=Mock(),
                                                      _PyCanTransportInterface__tx_frames_buffer=Mock(),
                                                      _PyCanTransportInterface__async_rx_frames_buffer=Mock(),
                                                      _PyCanTransportInterface__async_tx_frames_buffer=Mock())
        # patching
        self._patcher_uds_message = patch(f"{SCRIPT_LOCATION}.UdsMessage")
        self.mock_uds_message = self._patcher_uds_message.start()
        self._patcher_uds_message_record = patch(f"{SCRIPT_LOCATION}.UdsMessageRecord")
        self.mock_uds_message_record = self._patcher_uds_message_record.start()
        self._patcher_can_packet_record = patch(f"{SCRIPT_LOCATION}.CanPacketRecord")
        self.mock_can_packet_record = self._patcher_can_packet_record.start()
        self._patcher_can_id_handler = patch(f"{SCRIPT_LOCATION}.CanIdHandler")
        self.mock_can_id_handler = self._patcher_can_id_handler.start()
        self._patcher_can_dlc_handler = patch(f"{SCRIPT_LOCATION}.CanDlcHandler")
        self.mock_can_dlc_handler = self._patcher_can_dlc_handler.start()
        self._patcher_can_st_min_handler = patch(f"{SCRIPT_LOCATION}.CanSTminTranslator")
        self.mock_can_st_min_handler = self._patcher_can_st_min_handler.start()
        self._patcher_abstract_can_ti_init = patch(f"{SCRIPT_LOCATION}.AbstractCanTransportInterface.__init__")
        self.mock_abstract_can_ti_init = self._patcher_abstract_can_ti_init.start()
        self._patcher_can_packet_type_is_initial_packet_type \
            = patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
        self.mock_can_packet_type_is_initial_packet_type = self._patcher_can_packet_type_is_initial_packet_type.start()
        self._patcher_buffered_reader = patch(f"{SCRIPT_LOCATION}.BufferedReader")
        self.mock_buffered_reader = self._patcher_buffered_reader.start()
        self._patcher_async_buffered_reader = patch(f"{SCRIPT_LOCATION}.AsyncBufferedReader")
        self.mock_async_buffered_reader = self._patcher_async_buffered_reader.start()
        self._patcher_notifier = patch(f"{SCRIPT_LOCATION}.Notifier")
        self.mock_notifier = self._patcher_notifier.start()
        self._patcher_python_can_message = patch(f"{SCRIPT_LOCATION}.PythonCanMessage")
        self.mock_python_can_message = self._patcher_python_can_message.start()
        self._patcher_min = patch(f"{SCRIPT_LOCATION}.min")
        self.mock_min = self._patcher_min.start()
        self._patcher_warn = patch(f"{SCRIPT_LOCATION}.warn")
        self.mock_warn = self._patcher_warn.start()
        self._patcher_time = patch(f"{SCRIPT_LOCATION}.time")
        self.mock_time = self._patcher_time.start()
        self._patcher_perf_counter = patch(f"{SCRIPT_LOCATION}.perf_counter")
        self.mock_perf_counter = self._patcher_perf_counter.start()
        self._patcher_datetime = patch(f"{SCRIPT_LOCATION}.datetime")
        self.mock_datetime = self._patcher_datetime.start()
        self._patcher_sleep = patch(f"{SCRIPT_LOCATION}.sleep")
        self.mock_sleep = self._patcher_sleep.start()
        self._patcher_async_sleep = patch(f"{SCRIPT_LOCATION}.async_sleep")
        self.mock_async_sleep = self._patcher_async_sleep.start()
        self._patcher_wait_for = patch(f"{SCRIPT_LOCATION}.wait_for",
                                       AsyncMock(side_effect=lambda *args, **kwargs: args[0]))
        self.mock_wait_for = self._patcher_wait_for.start()
        self._patcher_get_running_loop = patch(f"{SCRIPT_LOCATION}.get_running_loop")
        self.mock_get_running_loop = self._patcher_get_running_loop.start()

    def teardown_method(self):
        self._patcher_uds_message.stop()
        self._patcher_uds_message_record.stop()
        self._patcher_can_packet_record.stop()
        self._patcher_can_id_handler.stop()
        self._patcher_can_dlc_handler.stop()
        self._patcher_can_st_min_handler.stop()
        self._patcher_abstract_can_ti_init.stop()
        self._patcher_can_packet_type_is_initial_packet_type.stop()
        self._patcher_buffered_reader.stop()
        self._patcher_async_buffered_reader.stop()
        self._patcher_notifier.stop()
        self._patcher_python_can_message.stop()
        self._patcher_min.stop()
        self._patcher_warn.stop()
        self._patcher_time.stop()
        self._patcher_perf_counter.stop()
        self._patcher_datetime.stop()
        self._patcher_sleep.stop()
        self._patcher_async_sleep.stop()
        self._patcher_wait_for.stop()
        self._patcher_get_running_loop.stop()

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
    def test_init(self, network_manager, addressing_information, configuration_params):
        assert PyCanTransportInterface.__init__(self=self.mock_can_transport_interface,
                                                network_manager=network_manager,
                                                addressing_information=addressing_information,
                                                **configuration_params) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        assert (self.mock_can_transport_interface._PyCanTransportInterface__rx_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PyCanTransportInterface__async_rx_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PyCanTransportInterface__tx_frames_buffer
                == self.mock_buffered_reader.return_value)
        assert (self.mock_can_transport_interface._PyCanTransportInterface__async_tx_frames_buffer
                == self.mock_async_buffered_reader.return_value)
        self.mock_abstract_can_ti_init.assert_called_once_with(
            network_manager=network_manager,
            addressing_information=addressing_information,
            **configuration_params)
        self.mock_buffered_reader.assert_has_calls([call(), call()])
        self.mock_async_buffered_reader.assert_has_calls([call(), call()])

    # __del__

    def test_del(self):
        assert PyCanTransportInterface.__del__(self.mock_can_transport_interface) is None
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_notifier.assert_called_once_with(
            suppress_warning=True)
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_async_notifier.assert_called_once_with(
            suppress_warning=True)
        self.mock_can_transport_interface._PyCanTransportInterface__rx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PyCanTransportInterface__async_rx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PyCanTransportInterface__tx_frames_buffer.stop.assert_called_once_with()
        self.mock_can_transport_interface._PyCanTransportInterface__async_tx_frames_buffer.stop.assert_called_once_with()

    # __teardown_notifier

    def test_teardown_notifier__no_notifier(self):
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = None
        assert PyCanTransportInterface._PyCanTransportInterface__teardown_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        self.mock_warn.assert_not_called()

    def test_teardown_notifier__notifier(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = mock_notifier
        assert PyCanTransportInterface._PyCanTransportInterface__teardown_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_teardown_notifier__notifier_with_suppressed_warning(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = mock_notifier
        assert PyCanTransportInterface._PyCanTransportInterface__teardown_notifier(
            self.mock_can_transport_interface, suppress_warning=True) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_not_called()

    # __teardown_async_notifier

    def test_teardown_async_notifier__no_notifier(self):
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = None
        assert PyCanTransportInterface._PyCanTransportInterface__teardown_async_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        self.mock_warn.assert_not_called()

    def test_teardown_async_notifier__notifier(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = mock_notifier
        assert PyCanTransportInterface._PyCanTransportInterface__teardown_async_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_called_once()

    def test_teardown_async_notifier__notifier_with_suppressed_warning(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = mock_notifier
        assert PyCanTransportInterface._PyCanTransportInterface__teardown_async_notifier(
            self.mock_can_transport_interface, suppress_warning=True) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier is None
        mock_notifier.stop.assert_called_once_with(self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_warn.assert_not_called()

    # __setup_notifier

    def test_setup_notifier__no_notifier(self):
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = None
        assert PyCanTransportInterface._PyCanTransportInterface__setup_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PyCanTransportInterface__rx_frames_buffer,
                       self.mock_can_transport_interface._PyCanTransportInterface__tx_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT)
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_async_notifier.assert_called_once_with()

    def test_setup_notifier__notifier_exists(self):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__notifier = mock_notifier
        assert PyCanTransportInterface._PyCanTransportInterface__setup_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier == mock_notifier
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_async_notifier.assert_called_once_with()

    # __setup_async_notifier

    @pytest.mark.parametrize("loop", ["some loop", Mock()])
    def test_setup_async_notifier__no_notifier(self, loop):
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = None
        assert PyCanTransportInterface._PyCanTransportInterface__setup_async_notifier(
            self.mock_can_transport_interface, loop=loop) is None
        assert (self.mock_can_transport_interface._PyCanTransportInterface__async_notifier
                == self.mock_notifier.return_value)
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.network_manager,
            listeners=[self.mock_can_transport_interface._PyCanTransportInterface__async_rx_frames_buffer,
                       self.mock_can_transport_interface._PyCanTransportInterface__async_tx_frames_buffer],
            timeout=self.mock_can_transport_interface._MIN_NOTIFIER_TIMEOUT,
            loop=loop)
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_notifier.assert_called_once_with()

    @pytest.mark.parametrize("loop", ["some loop", Mock()])
    def test_setup_async_notifier__notifier_exists(self, loop):
        mock_notifier = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_notifier = mock_notifier
        assert PyCanTransportInterface._PyCanTransportInterface__setup_async_notifier(
            self.mock_can_transport_interface, loop=loop) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier == mock_notifier
        self.mock_notifier.assert_not_called()
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_notifier.assert_called_once_with()

    # __validate_timeout

    @pytest.mark.parametrize("value", ["some value", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_validate_timeout__type_error(self, mock_isinstance, value):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PyCanTransportInterface._PyCanTransportInterface__validate_timeout(value)
        mock_isinstance.assert_called_once_with(value, (int, float))

    @pytest.mark.parametrize("value", [0, -0.231])
    def test_validate_timeout__value_error(self, value):
        with pytest.raises(ValueError):
            PyCanTransportInterface._PyCanTransportInterface__validate_timeout(value)

    @pytest.mark.parametrize("value", [None, 0.1, 543])
    def test_validate_timeout__valid(self, value):
        assert PyCanTransportInterface._PyCanTransportInterface__validate_timeout(value) is None

    # _send_cf_packets_block

    @pytest.mark.parametrize("packets, delay", [
        ([Mock(spec=CanPacket), Mock(spec=CanPacket)], 0),
        ([Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)], 12.34),
    ])
    def test_send_cf_packets_block(self, packets, delay):
        mock_fc_timestamp_gt = Mock(return_value=False)
        mock_cf_timestamp_gt = Mock(return_value=True)
        mock_fc_timestamp = MagicMock(__add__=lambda this, other: this,
                                      __sub__=lambda this, other: this,
                                      __gt__=mock_fc_timestamp_gt)
        mock_cf_timestamp = MagicMock(__add__=lambda this, other: this,
                                      __sub__=lambda this, other: this,
                                      __gt__=mock_cf_timestamp_gt)
        mock_fc_transmission_time = Mock(timestamp=Mock(return_value=mock_fc_timestamp))
        packet_records = tuple(MagicMock(spec=CanPacketRecord,
                                         transmission_time=Mock(timestamp=Mock(return_value=mock_cf_timestamp)))
                               for _ in packets)
        self.mock_can_transport_interface.send_packet.side_effect = packet_records
        assert PyCanTransportInterface._send_cf_packets_block(self.mock_can_transport_interface,
                                                              cf_packets_block=packets,
                                                              fc_transmission_time=mock_fc_transmission_time,
                                                              delay=delay) == packet_records
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
        mock_fc_timestamp = MagicMock(__add__=lambda this, other: this,
                                      __sub__=lambda this, other: this,
                                      __gt__=mock_fc_timestamp_gt)
        mock_cf_timestamp = MagicMock(__add__=lambda this, other: this,
                                      __sub__=lambda this, other: this,
                                      __gt__=mock_cf_timestamp_gt)
        mock_fc_transmission_time = Mock(timestamp=Mock(return_value=mock_fc_timestamp))
        packet_records = tuple(MagicMock(spec=CanPacketRecord,
                                         transmission_time=Mock(timestamp=Mock(return_value=mock_cf_timestamp)))
                               for _ in packets)
        self.mock_can_transport_interface.async_send_packet.side_effect = packet_records
        assert await PyCanTransportInterface._async_send_cf_packets_block(self.mock_can_transport_interface,
                                                                          cf_packets_block=packets,
                                                                          delay=delay,
                                                                          fc_transmission_time=mock_fc_transmission_time,
                                                                          loop=mock_loop) == packet_records
        self.mock_can_transport_interface.async_send_packet.assert_has_calls(
            [call(packet, loop=mock_loop) for packet in packets], any_order=False)
        mock_fc_timestamp_gt.assert_called_once_with(0)
        mock_cf_timestamp_gt.assert_has_calls([call(0)] * len(packets[1:]))
        self.mock_sleep.assert_not_called()
        self.mock_async_sleep.assert_called()

    # _wait_for_flow_control

    @pytest.mark.parametrize("packet_records", [
        [Mock(spec=CanPacketRecord, addressing_type=Mock(), packet_type=Mock()),
         Mock(spec=CanPacketRecord, addressing_type=Mock(), packet_type=CanPacketType.FLOW_CONTROL),
         Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=Mock()),
         Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=CanPacketType.FLOW_CONTROL)],
        [Mock(spec=CanPacketRecord, addressing_type=AddressingType.PHYSICAL, packet_type=CanPacketType.FLOW_CONTROL)]
    ])
    def test_wait_for_flow_control(self, packet_records):
        self.mock_can_transport_interface._wait_for_packet.side_effect = packet_records
        assert (PyCanTransportInterface._wait_for_flow_control(self.mock_can_transport_interface,
                                                               last_packet_transmission_time=MagicMock())
                == packet_records[-1])

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
        self.mock_can_transport_interface._async_wait_for_packet.side_effect = packet_records
        assert (await PyCanTransportInterface._async_wait_for_flow_control(self.mock_can_transport_interface,
                                                                           last_packet_transmission_time=MagicMock())
                == packet_records[-1])

    # _wait_for_packet

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    def test_wait_for_packet__timeout_error(self, timeout):
        mock_is_timeout_reached = Mock(side_effect=[False, True])
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        mock_get_message = Mock(return_value=None)
        mock_frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            PyCanTransportInterface._wait_for_packet(self.mock_can_transport_interface,
                                                     buffer=mock_frames_buffer,
                                                     timeout=timeout)
        mock_get_message.assert_called_once()
        assert mock_is_timeout_reached.call_count == 2

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    def test_wait_for_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        mock_frames_buffer = Mock(get_message=mock_get_message)
        assert (PyCanTransportInterface._wait_for_packet(self.mock_can_transport_interface,
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
            transmission_time=self.mock_datetime.fromtimestamp.return_value)

    # _async_wait_for_packet

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_wait_for_packet__timeout_error(self, timeout):
        mock_is_timeout_reached = Mock(side_effect=[False, True])
        self.mock_perf_counter.return_value = MagicMock(__sub__=lambda this, other: this,
                                                        __add__=lambda this, other: this,
                                                        __mul__=lambda this, other: this,
                                                        __le__=mock_is_timeout_reached)
        mock_get_message = Mock(side_effect=AsyncioTimeoutError)
        mock_frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            await PyCanTransportInterface._async_wait_for_packet(self.mock_can_transport_interface,
                                                                 buffer=mock_frames_buffer,
                                                                 timeout=timeout)
        mock_get_message.assert_called_once_with()
        assert mock_is_timeout_reached.call_count == 2

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_wait_for_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_perf_counter.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT = MagicMock(
            __sub__=lambda this, other: this,
            __add__=lambda this, other: this,
            __mul__=lambda this, other: this,
            __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        mock_frames_buffer = Mock(get_message=mock_get_message)
        assert (await PyCanTransportInterface._async_wait_for_packet(self.mock_can_transport_interface,
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
            transmission_time=self.mock_datetime.fromtimestamp.return_value)

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
            PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
            PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
        assert (PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
    def test_receive_cf_packets_block__cf_block(self, sequence_number, block_size, remaining_data_length, timestamp_end):
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
        assert (PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
        assert (PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
            await PyCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
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
            await PyCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
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
        assert (await PyCanTransportInterface._async_receive_cf_packets_block(
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
        assert (await PyCanTransportInterface._async_receive_cf_packets_block(
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
        assert (await PyCanTransportInterface._async_receive_cf_packets_block(
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
            PyCanTransportInterface._receive_consecutive_frames(self.mock_can_transport_interface,
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
        assert (PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
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
            PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
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
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_consecutive_frames__wait_then_receive_message(self, mock_isinstance, block_size, st_min,
                                                                   timestamp_end):
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
        assert (PyCanTransportInterface._receive_consecutive_frames(self.mock_can_transport_interface,
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
            self.mock_uds_message_record)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("data_length, ff_payload, cf_blocks, sequence_numbers, remaining_data_lengths, timestamp_end", [
        (8, [0x12, 0x34], [[Mock(spec=CanPacketRecord, payload=[0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])]], [1], [6], None),
        (68, [0x98], [[Mock(spec=CanPacketRecord, payload=list(range(60, 67)), sequence_number=2 * i + j + (i % 3 == 0))
                       for j in range(1 + i)] for i in range(4)], [1, 2, 4, 7], [67, 60, 46, 25],
         MagicMock(__sub__=lambda this, other: this,
                   __mul__=lambda this, other: this,
                   __lt__=Mock(return_value=False))),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_consecutive_frames__cf_received(self, mock_isinstance,
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
        assert (PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                    first_frame=mock_first_frame,
                                                                    timestamp_end=timestamp_end)
                == self.mock_uds_message_record.return_value)
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
        self.mock_uds_message_record.assert_called_once_with(all_packets)
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
            await PyCanTransportInterface._async_receive_consecutive_frames(self.mock_can_transport_interface,
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
        assert (await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
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
            await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
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
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__wait_then_receive_message(self, mock_isinstance,
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
        assert (await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
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
            self.mock_uds_message_record)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("data_length, ff_payload, cf_blocks, sequence_numbers, remaining_data_lengths, timestamp_end", [
        (8, [0x12, 0x34], [[Mock(spec=CanPacketRecord, payload=[0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])]], [1], [6], None),
        (68, [0x98], [[Mock(spec=CanPacketRecord, payload=list(range(60, 67)), sequence_number=2 * i + j + (i % 3 == 0))
                       for j in range(1 + i)] for i in range(4)], [1, 2, 4, 7], [67, 60, 46, 25],
         MagicMock(__sub__=lambda this, other: this,
                   __mul__=lambda this, other: this,
                   __lt__=Mock(return_value=False))),
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__cf_received(self, mock_isinstance,
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
        assert (await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                first_frame=mock_first_frame,
                                                                                timestamp_end=timestamp_end,
                                                                                loop=mock_loop)
                == self.mock_uds_message_record.return_value)
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
        self.mock_uds_message_record.assert_called_once_with(all_packets)
        mock_isinstance.assert_called()
        self.mock_warn.assert_not_called()

    # _message_receive_start

    def test_message_receive_start__sf(self):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        assert (PyCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                               initial_packet=mock_packet,
                                                               timestamp_end=Mock())
                == self.mock_uds_message_record.return_value)
        self.mock_uds_message_record.assert_called_once_with([mock_packet])

    def test_message_receive_start__ff(self):
        mock_timestamp_end = Mock()
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME)
        assert (PyCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
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
            PyCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                           initial_packet=mock_packet,
                                                           timestamp_end=Mock())

    # _async_message_receive_start

    @pytest.mark.asyncio
    async def test_async_message_receive_start__sf(self):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        assert (await PyCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                           initial_packet=mock_packet,
                                                                           timestamp_end=Mock(),
                                                                           loop=Mock())
                == self.mock_uds_message_record.return_value)
        self.mock_uds_message_record.assert_called_once_with([mock_packet])

    @pytest.mark.asyncio
    async def test_async_message_receive_start__ff(self):
        mock_loop = Mock()
        mock_timestamp_end = Mock()
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME)
        assert (await PyCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
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
            await PyCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                       initial_packet=mock_packet,
                                                                       timestamp_end=Mock(),
                                                                       loop=Mock())

    # clear_rx_frames_buffers

    @pytest.mark.parametrize("async_queue_size, sync_queue_size", [
        (0, 0),
        (1, 25),
        (69, 3),
    ])
    def test_clear_rx_frames_buffers(self, sync_queue_size, async_queue_size):
        mock_sync_queue = Mock(qsize=Mock(return_value=sync_queue_size))
        mock_async_queue = Mock(qsize=Mock(return_value=async_queue_size))
        self.mock_can_transport_interface._PyCanTransportInterface__rx_frames_buffer = Mock(buffer=mock_sync_queue)
        self.mock_can_transport_interface._PyCanTransportInterface__async_rx_frames_buffer = Mock(buffer=mock_async_queue)
        assert PyCanTransportInterface.clear_rx_frames_buffers(self.mock_can_transport_interface) is None
        mock_sync_queue.qsize.assert_called_once_with()
        mock_async_queue.qsize.assert_called_once_with()
        assert mock_sync_queue.get_nowait.call_count == sync_queue_size
        assert mock_async_queue.get_nowait.call_count == async_queue_size

    # clear_tx_frames_buffers

    @pytest.mark.parametrize("async_queue_size, sync_queue_size", [
        (0, 0),
        (1, 25),
        (69, 3),
    ])
    def test_clear_tx_frames_buffers(self, sync_queue_size, async_queue_size):
        mock_sync_queue = Mock(qsize=Mock(return_value=sync_queue_size))
        mock_async_queue = Mock(qsize=Mock(return_value=async_queue_size))
        self.mock_can_transport_interface._PyCanTransportInterface__tx_frames_buffer = Mock(buffer=mock_sync_queue)
        self.mock_can_transport_interface._PyCanTransportInterface__async_tx_frames_buffer = Mock(buffer=mock_async_queue)
        assert PyCanTransportInterface.clear_tx_frames_buffers(self.mock_can_transport_interface) is None
        mock_sync_queue.qsize.assert_called_once_with()
        mock_async_queue.qsize.assert_called_once_with()
        assert mock_sync_queue.get_nowait.call_count == sync_queue_size
        assert mock_async_queue.get_nowait.call_count == async_queue_size

    # is_supported_network_manager

    @pytest.mark.parametrize("value", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_is_supported_network_manager(self, mock_isinstance, value):
        assert PyCanTransportInterface.is_supported_network_manager(value) == mock_isinstance.return_value
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
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    def test_send_packet(self, packet):
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            timeout = self.mock_can_transport_interface.n_ar_timeout / 1000.
        else:
            timeout = self.mock_can_transport_interface.n_as_timeout / 1000.
        sent_can_frame = self.mock_python_can_message.return_value
        assert (PyCanTransportInterface.send_packet(self.mock_can_transport_interface, packet)
                == self.mock_can_packet_record.return_value)
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_python_can_message.assert_has_calls([
            call(arbitration_id=packet.can_id,
                 is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                 data=packet.raw_frame_data,
                 is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value,
                 is_rx=False,
                 is_error_frame=False,
                 is_remote_frame=False),
            call(arbitration_id=self.mock_python_can_message.return_value.arbitration_id,
                 is_extended_id=self.mock_python_can_message.return_value.is_extended_id,
                 data=self.mock_python_can_message.return_value.data,
                 is_fd=self.mock_python_can_message.return_value.is_fd,
                 is_rx=False,
                 is_error_frame=False,
                 is_remote_frame=False,
                 timestamp=self.mock_time.return_value)],
            any_order=False)
        self.mock_can_transport_interface.network_manager.send.assert_called_once_with(
            msg=self.mock_python_can_message.return_value, timeout=timeout)
        self.mock_datetime.fromtimestamp.assert_called_once_with(sent_can_frame.timestamp)
        self.mock_can_packet_record.assert_called_once_with(
            frame=sent_can_frame,
            direction=TransmissionDirection.TRANSMITTED,
            addressing_type=packet.addressing_type,
            addressing_format=packet.addressing_format,
            transmission_time=self.mock_datetime.fromtimestamp.return_value)
        if packet.packet_type == CanPacketType.FLOW_CONTROL:
            self.mock_can_transport_interface._update_n_ar_measured.assert_called_once()
            self.mock_can_transport_interface._update_n_as_measured.assert_not_called()
        else:
            self.mock_can_transport_interface._update_n_ar_measured.assert_not_called()
            self.mock_can_transport_interface._update_n_as_measured.assert_called_once()

    # async_send_packet

    @pytest.mark.parametrize("packet", ["something", Mock()])
    @pytest.mark.asyncio
    async def test_async_send_packet(self, packet):
        assert (await PyCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet)
                == self.mock_can_transport_interface.send_packet.return_value)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(packet=packet)

    # receive_packet

    @pytest.mark.parametrize("timeout", [Mock(), 123.456])
    def test_receive_packet(self, timeout):
        assert (PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
                == self.mock_can_transport_interface._wait_for_packet.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_called_once_with(timeout)
        self.mock_can_transport_interface._wait_for_packet.assert_called_once_with(
            buffer=self.mock_can_transport_interface._PyCanTransportInterface__rx_frames_buffer,
            timeout=timeout)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_not_called()

    # async_receive_packet

    @pytest.mark.parametrize("timeout, loop", [
        (Mock(), None),
        (123.456, Mock(spec=AbstractEventLoop)),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_packet(self, timeout, loop):
        assert (await PyCanTransportInterface.async_receive_packet(self.mock_can_transport_interface,
                                                                   timeout=timeout,
                                                                   loop=loop)
                == self.mock_can_transport_interface._async_wait_for_packet.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_called_once_with(timeout)
        self.mock_can_transport_interface._async_wait_for_packet.assert_called_once_with(
            buffer=self.mock_can_transport_interface._PyCanTransportInterface__async_rx_frames_buffer,
            timeout=timeout)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_not_called()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            loop=loop if loop is not None else self.mock_get_running_loop.return_value)

    # send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    def test_send_message__single_frame(self, message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        assert PyCanTransportInterface.send_message(self.mock_can_transport_interface,
                                                    message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(mock_segmented_message[0])
        self.mock_uds_message_record.assert_called_once_with(
            [self.mock_can_transport_interface.send_packet.return_value])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

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
    def test_send_message__multiple_packets__st_min__block_size_0(self, message, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        self.mock_can_transport_interface.n_cs = None
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0,
                                        st_min=st_min)
        self.mock_can_transport_interface._wait_for_flow_control = Mock(return_value=mock_flow_control_record)
        mock_sent_packet_records = [Mock(spec=CanPacketRecord)] * 20
        self.mock_can_transport_interface._send_cf_packets_block.return_value = mock_sent_packet_records
        assert (PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
                == self.mock_uds_message_record.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_called_once_with(
            last_packet_transmission_time=self.mock_can_transport_interface.send_packet.return_value.transmission_time)
        self.mock_can_transport_interface._send_cf_packets_block.assert_called_once_with(
            cf_packets_block=mock_segmented_message[1:],
            delay=self.mock_can_st_min_handler.decode.return_value,
            fc_transmission_time=mock_flow_control_record.transmission_time)
        self.mock_can_st_min_handler.decode.assert_called_once_with(st_min)
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record,
            *mock_sent_packet_records
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

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
    def test_send_message__multiple_packets__n_cs__block_size_1(self, message, n_cs, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        self.mock_can_transport_interface.n_cs = n_cs
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=1,
                                        st_min=st_min)
        self.mock_can_transport_interface._wait_for_flow_control = Mock(return_value=mock_flow_control_record)
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert (PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
                == self.mock_uds_message_record.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_has_calls(
            [call(last_packet_transmission_time=self.mock_can_transport_interface.send_packet.return_value.transmission_time)]
            + [call(last_packet_transmission_time=mock_sent_packet_record.transmission_time)
               for _ in mock_segmented_message[1:-1]],
            any_order=False)
        self.mock_can_transport_interface._send_cf_packets_block.assert_has_calls([
            call(cf_packets_block=[packet],
                 delay=n_cs,
                 fc_transmission_time=mock_flow_control_record.transmission_time)
            for packet in mock_segmented_message[1:]],
        any_order=False)
        self.mock_can_st_min_handler.decode.assert_not_called()
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            *([mock_flow_control_record, mock_sent_packet_record]*len(mock_segmented_message[1:]))
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__wait(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        mock_flow_control_record_wait = Mock(spec=CanPacketRecord,
                                             packet_type=CanPacketType.FLOW_CONTROL,
                                             flow_status=CanFlowStatus.Wait)
        mock_flow_control_record_continue = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.ContinueToSend,
                                                 block_size=0)
        self.mock_can_transport_interface._wait_for_flow_control.side_effect = [mock_flow_control_record_wait,
                                                                                mock_flow_control_record_continue]
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert (PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
                == self.mock_uds_message_record.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_has_calls([
            call(last_packet_transmission_time=self.mock_can_transport_interface.send_packet.return_value.transmission_time),
            call(last_packet_transmission_time=mock_flow_control_record_wait.transmission_time)],
        any_order=False)
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record_wait,
            mock_flow_control_record_continue,
            mock_sent_packet_record
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

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
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.Overflow)
        self.mock_can_transport_interface._wait_for_flow_control.return_value = mock_flow_control_record_overflow
        with pytest.raises(OverflowError):
            PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_called_once_with(
            last_packet_transmission_time=self.mock_can_transport_interface.send_packet.return_value.transmission_time)
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
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        mock_flow_control_record_unknown = Mock(spec=CanPacketRecord,
                                                packet_type=CanPacketType.FLOW_CONTROL,
                                                flow_status=Mock())
        self.mock_can_transport_interface._wait_for_flow_control.return_value = mock_flow_control_record_unknown
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._wait_for_flow_control.assert_called_once_with(
            last_packet_transmission_time=self.mock_can_transport_interface.send_packet.return_value.transmission_time)
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    # async_send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__single_frame(self, message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        assert await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_send_packet.assert_called_once_with(
            mock_segmented_message[0], loop=self.mock_get_running_loop.return_value)
        self.mock_uds_message_record.assert_called_once_with(
            [self.mock_can_transport_interface.async_send_packet.return_value])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

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
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__st_min__block_size_0(self, message, st_min):
        mock_loop = Mock(spec=AbstractEventLoop)
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        self.mock_can_transport_interface.n_cs = None
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0,
                                        st_min=st_min)
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value=mock_flow_control_record
        mock_sent_packet_records = [Mock(spec=CanPacketRecord)] * 20
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = mock_sent_packet_records
        assert (await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                 message=message,
                                                                 loop=mock_loop)
                == self.mock_uds_message_record.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            mock_loop)
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_called_once_with(
            last_packet_transmission_time=self.mock_can_transport_interface.async_send_packet.return_value.transmission_time)
        self.mock_can_transport_interface._async_send_cf_packets_block.assert_called_once_with(
            cf_packets_block=mock_segmented_message[1:],
            delay=self.mock_can_st_min_handler.decode.return_value,
            fc_transmission_time=mock_flow_control_record.transmission_time,
            loop=mock_loop)
        self.mock_can_st_min_handler.decode.assert_called_once_with(st_min)
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record,
            *mock_sent_packet_records
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

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
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__n_cs__block_size_1(self, message, n_cs, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        self.mock_can_transport_interface.n_cs = n_cs
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=1,
                                        st_min=st_min)
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value=mock_flow_control_record
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_has_calls(
            [call(last_packet_transmission_time=self.mock_can_transport_interface.async_send_packet.return_value.transmission_time)]
            + [call(last_packet_transmission_time=mock_sent_packet_record.transmission_time)
               for _ in mock_segmented_message[1:-1]], any_order=False)
        self.mock_can_transport_interface._async_send_cf_packets_block.assert_has_calls([
            call(cf_packets_block=[packet],
                 delay=n_cs,
                 fc_transmission_time=mock_flow_control_record.transmission_time,
                 loop=self.mock_get_running_loop.return_value) for packet in mock_segmented_message[1:]],
        any_order=False)
        self.mock_can_st_min_handler.decode.assert_not_called()
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            *([mock_flow_control_record, mock_sent_packet_record]*len(mock_segmented_message[1:]))
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage,
             payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88],
             addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage,
             payload=[0x3E, 0x80],
             addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__wait(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        mock_flow_control_record_wait = Mock(spec=CanPacketRecord,
                                             packet_type=CanPacketType.FLOW_CONTROL,
                                             flow_status=CanFlowStatus.Wait)
        mock_flow_control_record_continue = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.ContinueToSend,
                                                 block_size=0)
        self.mock_can_transport_interface._async_wait_for_flow_control.side_effect = [
            mock_flow_control_record_wait, mock_flow_control_record_continue]
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                                message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_has_calls(
            [call(last_packet_transmission_time=self.mock_can_transport_interface.async_send_packet.return_value.transmission_time),
             call(last_packet_transmission_time=mock_flow_control_record_wait.transmission_time)],
            any_order=False)
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record_wait,
            mock_flow_control_record_continue,
            mock_sent_packet_record
        ])
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

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
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.Overflow)
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value = mock_flow_control_record_overflow
        with pytest.raises(OverflowError):
            await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface,
                                                             message=message,
                                                             loop=mock_loop)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            mock_loop)
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_called_once_with(
            last_packet_transmission_time=self.mock_can_transport_interface.async_send_packet.return_value.transmission_time)
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
        self.mock_can_transport_interface.segmenter.segmentation.return_value=mock_segmented_message
        mock_flow_control_record_unknown = Mock(spec=CanPacketRecord,
                                                packet_type=CanPacketType.FLOW_CONTROL,
                                                flow_status=Mock())
        self.mock_can_transport_interface._async_wait_for_flow_control.return_value=mock_flow_control_record_unknown
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
            self.mock_get_running_loop.return_value)
        self.mock_can_transport_interface.clear_tx_frames_buffers.assert_called_once_with()
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface._async_wait_for_flow_control.assert_called_once_with(
            last_packet_transmission_time=self.mock_can_transport_interface.async_send_packet.return_value.transmission_time)
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
            PyCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                    start_timeout=start_timeout)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
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
            PyCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                    start_timeout=start_timeout)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
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
        assert (PyCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                        start_timeout=start_timeout,
                                                        end_timeout=end_timeout)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value,
            timestamp_end=None if end_timeout is None else self.mock_perf_counter.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called_once()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
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
        assert (PyCanTransportInterface.receive_message(self.mock_can_transport_interface,
                                                        start_timeout=start_timeout,
                                                        end_timeout=end_timeout)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value,
            timestamp_end=None if end_timeout is None else self.mock_perf_counter.return_value)
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            calls=[call(timeout=None if start_timeout is None else self.mock_perf_counter.return_value),
                   call(timeout=None if start_timeout is None else self.mock_perf_counter.return_value)]
        )
        self.mock_can_transport_interface._PyCanTransportInterface__setup_notifier.assert_called_once_with()
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
            await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                start_timeout=start_timeout,
                                                                loop=mock_loop)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
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
            await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                start_timeout=start_timeout,
                                                                loop=mock_loop)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(None)])
        mock_is_timeout_reached.assert_called_once()
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
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
        assert (await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                    start_timeout=start_timeout,
                                                                    end_timeout=end_timeout,
                                                                    loop=mock_loop)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
            call(start_timeout),
            call(end_timeout)])
        self.mock_can_transport_interface._PyCanTransportInterface__setup_async_notifier.assert_called_once_with(
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
        assert (await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
                                                                    start_timeout=start_timeout,
                                                                    end_timeout=end_timeout,
                                                                    loop=None)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface._PyCanTransportInterface__validate_timeout.assert_has_calls([
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
class TestPyCanTransportInterfacePerformance:

    REPETITIONS = 100

    def setup_method(self):
        self.mock_can_transport_interface = MagicMock(spec=PyCanTransportInterface,
                                                      _PyCanTransportInterface__rx_frames_buffer=Mock(),
                                                      _PyCanTransportInterface__tx_frames_buffer=Mock(),
                                                      _PyCanTransportInterface__async_rx_frames_buffer=Mock(),
                                                      _PyCanTransportInterface__async_tx_frames_buffer=Mock())
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

    # _wait_for_packet

    @pytest.mark.parametrize("timeout", [10, 75])
    def test_wait_for_packet__timeout(self,
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
                PyCanTransportInterface._wait_for_packet(self.mock_can_transport_interface,
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

    # _async_wait_for_packet

    @pytest.mark.parametrize("timeout", [10, 75])
    @pytest.mark.asyncio
    async def test_async_wait_for_packet__timeout(self,
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
                await PyCanTransportInterface._async_wait_for_packet(self.mock_can_transport_interface,
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
                PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
                PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
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
                await PyCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
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
                await PyCanTransportInterface._async_receive_cf_packets_block(self.mock_can_transport_interface,
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
                         payload=[0x12])]

        mock_first_frame = MagicMock(spec=CanPacketRecord,
                                     data_length=float("inf"),
                                     payload=[],
                                     transmission_time=datetime.now())
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
                PyCanTransportInterface._receive_consecutive_frames(
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
            sleep(0.005)
            return [Mock(spec=CanPacketRecord,
                         packet_type=CanPacketType.CONSECUTIVE_FRAME,
                         sequence_number=current_sn,
                         transmission_time=datetime.now(),
                         payload=[0x12])]

        mock_first_frame = MagicMock(spec=CanPacketRecord,
                                     data_length=float("inf"),
                                     payload=[],
                                     transmission_time=datetime.now())
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
                await PyCanTransportInterface._async_receive_consecutive_frames(
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
                PyCanTransportInterface.receive_message(self.mock_can_transport_interface,
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
            await asyncio_sleep(0.005)
            return Mock(spec=CanPacketRecord)

        mock_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.async_receive_packet.side_effect = _get_packet_record

        execution_times = []
        for _ in range(self.REPETITIONS):
            timestamp_before = perf_counter()
            with pytest.raises(MessageTransmissionNotStartedError):
                await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface,
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


@pytest.mark.integration
class TestPyCanTransportInterfaceIntegration:
    """Integration tests for `PyCanTransportInterface` class."""

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
        py_can_ti = PyCanTransportInterface(**init_kwargs, addressing_information=example_can_addressing_information)
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

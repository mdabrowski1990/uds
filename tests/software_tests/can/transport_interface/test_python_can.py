from random import choice, randint

import pytest
from mock import AsyncMock, MagicMock, Mock, call, patch

from uds.can import CanAddressingFormat, CanAddressingInformation
from uds.can.transport_interface.python_can import (
    AbstractCanTransportInterface,
    BusABC,
    CanFlowStatus,
    CanPacket,
    CanPacketRecord,
    CanPacketType,
    PyCanTransportInterface,
    TransmissionDirection,
    UdsMessage,
)
from uds.transmission_attributes import AddressingType

SCRIPT_LOCATION = "uds.transport_interface.addressing.python_can"


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
        self._patcher_can_st_min_handler = patch(f"{SCRIPT_LOCATION}.CanSTminTranslator")
        self.mock_can_st_min_handler = self._patcher_can_st_min_handler.start()
        self._patcher_can_packet_record = patch(f"{SCRIPT_LOCATION}.CanPacketRecord")
        self.mock_can_packet_record = self._patcher_can_packet_record.start()
        self._patcher_can_packet_type_is_initial_packet_type = patch(f"{SCRIPT_LOCATION}.CanPacketType.is_initial_packet_type")
        self.mock_can_packet_type_is_initial_packet_type = self._patcher_can_packet_type_is_initial_packet_type.start()
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
        self._patcher_can_st_min_handler.stop()
        self._patcher_can_packet_record.stop()
        self._patcher_can_packet_type_is_initial_packet_type.stop()
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

    # __del__

    def test_del(self):
        assert PyCanTransportInterface.__del__(self.mock_can_transport_interface) is None
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_notifier.assert_called_once_with(
            suppress_warning=True)
        self.mock_can_transport_interface._PyCanTransportInterface__teardown_async_notifier.assert_called_once_with(
            suppress_warning=True)

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
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock()
        assert PyCanTransportInterface._PyCanTransportInterface__setup_notifier(
            self.mock_can_transport_interface) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.bus_manager,
            listeners=[self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer],
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
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock()
        assert PyCanTransportInterface._PyCanTransportInterface__setup_async_notifier(
            self.mock_can_transport_interface, loop=loop) is None
        assert self.mock_can_transport_interface._PyCanTransportInterface__async_notifier == self.mock_notifier.return_value
        self.mock_notifier.assert_called_once_with(
            bus=self.mock_can_transport_interface.bus_manager,
            listeners=[self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer],
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

    # _send_cf_packets_block

    @pytest.mark.parametrize("packets", [
        (Mock(spec=CanPacket), Mock(spec=CanPacket)),
        (Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)),
    ])
    @pytest.mark.parametrize("delay", [0, 12.34])
    def test_send_cf_packets_block(self, packets, delay):
        called = 0

        def once_true_once_false(*args):
            nonlocal called
            called += 1
            return called % 2

        mock_lt = Mock(side_effect=once_true_once_false)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __lt__=mock_lt)
        self.mock_can_transport_interface.receive_packet.side_effect = TimeoutError
        packet_records = PyCanTransportInterface._send_cf_packets_block(self=self.mock_can_transport_interface,
                                                                        cf_packets_block=packets, delay=delay)
        assert isinstance(packet_records, tuple)
        assert all(packet_record == self.mock_can_transport_interface.send_packet.return_value
                   for packet_record in packet_records)
        self.mock_can_transport_interface.send_packet.assert_has_calls(calls=[call(packet) for packet in packets])
        self.mock_can_transport_interface.receive_packet.assert_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("packets", [
        (Mock(spec=CanPacket), Mock(spec=CanPacket)),
        (Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)),
    ])
    @pytest.mark.parametrize("delay", [0, 12.34])
    def test_send_cf_packets_block__unexpected_packet(self, packets, delay):
        called = 0

        def once_true_once_false(*args):
            nonlocal called
            called += 1
            return called % 2

        mock_lt = Mock(side_effect=once_true_once_false)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __lt__=mock_lt)
        mock_received_packet_records = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface.receive_packet.return_value = mock_received_packet_records
        packet_records = PyCanTransportInterface._send_cf_packets_block(self=self.mock_can_transport_interface,
                                                                        cf_packets_block=packets, delay=delay)
        assert isinstance(packet_records, tuple)
        assert all(packet_record == self.mock_can_transport_interface.send_packet.return_value
                   for packet_record in packet_records)
        self.mock_can_transport_interface.send_packet.assert_has_calls(calls=[call(packet) for packet in packets])
        self.mock_can_transport_interface.receive_packet.assert_called()
        self.mock_warn.assert_called()

    # _async_send_cf_packets_block

    @pytest.mark.parametrize("packets", [
        (Mock(spec=CanPacket), Mock(spec=CanPacket)),
        (Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)),
    ])
    @pytest.mark.parametrize("delay", [0, 12.34])
    @pytest.mark.asyncio
    async def test_async_send_cf_packets_block(self, packets, delay):
        called = 0

        def once_true_once_false(*args):
            nonlocal called
            called += 1
            return called % 2

        mock_lt = Mock(side_effect=once_true_once_false)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __lt__=mock_lt)
        self.mock_can_transport_interface.async_receive_packet.side_effect = TimeoutError
        packet_records = await PyCanTransportInterface._async_send_cf_packets_block(
            self=self.mock_can_transport_interface, cf_packets_block=packets, delay=delay)
        assert isinstance(packet_records, tuple)
        assert all(packet_record == self.mock_can_transport_interface.async_send_packet.return_value
                   for packet_record in packet_records)
        self.mock_can_transport_interface.async_send_packet.assert_has_calls(
            calls=[call(packet, loop=None) for packet in packets])
        self.mock_can_transport_interface.async_receive_packet.assert_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("packets", [
        (Mock(spec=CanPacket), Mock(spec=CanPacket)),
        (Mock(spec=CanPacket), Mock(spec=CanPacket), Mock(spec=CanPacket)),
    ])
    @pytest.mark.parametrize("delay", [0, 1234])
    @pytest.mark.asyncio
    async def test_async_send_cf_packets_block__unexpected_packet(self, packets, delay):
        called = 0

        def once_true_once_false(*args):
            nonlocal called
            called += 1
            return called % 2

        mock_lt = Mock(side_effect=once_true_once_false)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __lt__=mock_lt)
        mock_received_packet_records = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface.async_receive_packet.return_value = mock_received_packet_records
        packet_records = await PyCanTransportInterface._async_send_cf_packets_block(
            self=self.mock_can_transport_interface, cf_packets_block=packets, delay=delay)
        assert isinstance(packet_records, tuple)
        assert all(packet_record == self.mock_can_transport_interface.async_send_packet.return_value
                   for packet_record in packet_records)
        self.mock_can_transport_interface.async_send_packet.assert_has_calls(
            calls=[call(packet, loop=None) for packet in packets])
        self.mock_can_transport_interface.async_receive_packet.assert_called()
        self.mock_warn.assert_called()

    # _message_receive_start

    def test_message_receive_start__sf(self):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        assert (PyCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                               initial_packet=mock_packet)
                == self.mock_uds_message_record.return_value)
        self.mock_uds_message_record.assert_called_once_with([mock_packet])

    def test_message_receive_start__ff(self):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME)
        assert (PyCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                               initial_packet=mock_packet)
                == self.mock_can_transport_interface._receive_consecutive_frames.return_value)
        self.mock_can_transport_interface._receive_consecutive_frames.assert_called_once_with(first_frame=mock_packet)

    @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, None, "Other"])
    def test_message_receive_start__other(self, packet_type):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=packet_type)
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface._message_receive_start(self.mock_can_transport_interface,
                                                           initial_packet=mock_packet)

    # _async_message_receive_start

    @pytest.mark.asyncio
    async def test_async_message_receive_start__sf(self):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        assert (await PyCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                           initial_packet=mock_packet)
                == self.mock_uds_message_record.return_value)
        self.mock_uds_message_record.assert_called_once_with([mock_packet])

    @pytest.mark.asyncio
    async def test_async_message_receive_start__ff(self):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME)
        assert (await PyCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                           initial_packet=mock_packet)
                == self.mock_can_transport_interface._async_receive_consecutive_frames.return_value)
        self.mock_can_transport_interface._async_receive_consecutive_frames.assert_called_once_with(
            first_frame=mock_packet, loop=None)

    @pytest.mark.parametrize("packet_type", [CanPacketType.CONSECUTIVE_FRAME, None, "Other"])
    @pytest.mark.asyncio
    async def test_async_message_receive_start__other(self, packet_type):
        mock_packet = Mock(spec=CanPacketRecord, packet_type=packet_type)
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface._async_message_receive_start(self.mock_can_transport_interface,
                                                                       initial_packet=mock_packet)

    # _receive_cf_packets_block

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length", [
        (Mock(), Mock(), 1),
        (Mock(), Mock(), 987),
    ])
    def test_receive_cf_packets_block__initial_packet(self, sequence_number, block_size, remaining_data_length):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                  sequence_number=sequence_number,
                                                                  block_size=block_size,
                                                                  remaining_data_length=remaining_data_length)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_cr_timeout)
        self.mock_can_packet_type_is_initial_packet_type.assert_called_once_with(
            self.mock_can_transport_interface.receive_packet.return_value.packet_type)
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length", [
        (Mock(), Mock(), 1),
        (Mock(), Mock(), 987),
    ])
    def test_receive_cf_packets_block__unrelated_then_initial_packet(self, sequence_number, block_size,
                                                                     remaining_data_length):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
        self.mock_can_packet_type_is_initial_packet_type.side_effect = (False, True)
        assert (PyCanTransportInterface._receive_cf_packets_block(self.mock_can_transport_interface,
                                                                  sequence_number=sequence_number,
                                                                  block_size=block_size,
                                                                  remaining_data_length=remaining_data_length)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called()
        assert self.mock_can_transport_interface.receive_packet.call_count == 2
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls(calls=[
            call(self.mock_can_transport_interface.receive_packet.return_value.packet_type),
            call(self.mock_can_transport_interface.receive_packet.return_value.packet_type)])
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value)
        self.mock_warn.assert_called()
        assert self.mock_warn.call_count == 2

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length", [
        (1, 1, 1),
        (13, 5, 987),
    ])
    def test_receive_cf_packets_block__cf_block(self, sequence_number, block_size, remaining_data_length):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
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
                                                                  remaining_data_length=remaining_data_length)
                == tuple(packet_sequence))
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_cr_timeout)] * block_size)
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([
            call(packet.packet_type) for packet in packet_sequence])
        self.mock_can_transport_interface._message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, remaining_data_length, payload", [
        (1, 1, [0x12]),
        (13, 987, [*range(100, 162)]),
    ])
    def test_receive_cf_packets_block__remaining_payload(self, sequence_number, remaining_data_length, payload):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
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
                                                                  remaining_data_length=remaining_data_length)
                == tuple(packet_sequence))
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_cr_timeout)] * len(packet_sequence))
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([
            call(packet.packet_type) for packet in packet_sequence])
        self.mock_can_transport_interface._message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    # _async_receive_cf_packets_block

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length", [
        (Mock(), Mock(), 1),
        (Mock(), Mock(), 987),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__initial_packet(self, sequence_number, block_size,
                                                                  remaining_data_length):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (await PyCanTransportInterface._async_receive_cf_packets_block(
            self.mock_can_transport_interface,
            sequence_number=sequence_number,
            block_size=block_size,
            remaining_data_length=remaining_data_length)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_cr_timeout, loop=None)
        self.mock_can_packet_type_is_initial_packet_type.assert_called_once_with(
            self.mock_can_transport_interface.async_receive_packet.return_value.packet_type)
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value, loop=None)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length", [
        (Mock(), Mock(), 1),
        (Mock(), Mock(), 987),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__unrelated_then_initial_packet(self, sequence_number, block_size,
                                                                                 remaining_data_length):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
        self.mock_can_packet_type_is_initial_packet_type.side_effect = (False, True)
        assert (await PyCanTransportInterface._async_receive_cf_packets_block(
            self.mock_can_transport_interface,
            sequence_number=sequence_number,
            block_size=block_size,
            remaining_data_length=remaining_data_length)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface.async_receive_packet.assert_called()
        assert self.mock_can_transport_interface.async_receive_packet.call_count == 2
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls(calls=[
            call(self.mock_can_transport_interface.async_receive_packet.return_value.packet_type),
            call(self.mock_can_transport_interface.async_receive_packet.return_value.packet_type)])
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value, loop=None)
        self.mock_warn.assert_called()
        assert self.mock_warn.call_count == 2

    @pytest.mark.parametrize("sequence_number, block_size, remaining_data_length", [
        (1, 1, 1),
        (13, 5, 987),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__cf_block(self, sequence_number, block_size, remaining_data_length):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
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
            remaining_data_length=remaining_data_length) == tuple(packet_sequence))
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_cr_timeout, loop=None)] * block_size)
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([
            call(packet.packet_type) for packet in packet_sequence])
        self.mock_can_transport_interface._async_message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("sequence_number, remaining_data_length, payload", [
        (1, 1, [0x12]),
        (13, 987, [*range(100, 162)]),
    ])
    @pytest.mark.asyncio
    async def test_async_receive_cf_packets_block__remaining_payload(self, sequence_number, remaining_data_length,
                                                                     payload):
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this)
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
            remaining_data_length=remaining_data_length)
                == tuple(packet_sequence))
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_cr_timeout, loop=None)] * len(packet_sequence))
        self.mock_can_packet_type_is_initial_packet_type.assert_has_calls([
            call(packet.packet_type) for packet in packet_sequence])
        self.mock_can_transport_interface._async_message_receive_start.assert_not_called()
        self.mock_warn.assert_not_called()

    # _receive_consecutive_frames

    def test_receive_consecutive_frames__new_message_interrupted(self):
        mock_first_frame = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME, payload=[])
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                    first_frame=mock_first_frame)
                == self.mock_can_transport_interface._message_receive_start.return_value)
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_br)
        self.mock_can_transport_interface.send_packet.assert_not_called()
        self.mock_warn.assert_called_once()

    def test_receive_consecutive_frames__packet_interrupted_then_overflow(self):
        mock_first_frame = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME, payload=[])
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.flow_control_parameters_generator = [(CanFlowStatus.Overflow, None, None)]
        with pytest.raises(OverflowError):
            PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                first_frame=mock_first_frame)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_br)
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_called_once_with(
            flow_status=CanFlowStatus.Overflow, block_size=None, st_min=None)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(
            self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("block_size, st_min", [
        (0, 127),
        (Mock(), Mock())
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_consecutive_frames__wait_then_receive_message(self, mock_isinstance, block_size, st_min):
        mock_first_frame = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME, payload=[], data_length=MagicMock())
        self.mock_can_transport_interface.receive_packet.side_effect = choice((TimeoutError, ValueError))
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.Wait, None, None), (CanFlowStatus.ContinueToSend, block_size, st_min)]
        mock_isinstance.return_value = True
        assert (PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                    first_frame=mock_first_frame)
                == self.mock_can_transport_interface._receive_cf_packets_block.return_value)
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_br), call(timeout=self.mock_can_transport_interface.n_br)])
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_has_calls(
            [call(flow_status=CanFlowStatus.Wait, block_size=None, st_min=None),
             call(flow_status=CanFlowStatus.ContinueToSend, block_size=block_size, st_min=st_min)])
        self.mock_can_transport_interface.send_packet.assert_has_calls(
            [call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value),
             call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value)])
        self.mock_can_transport_interface._receive_cf_packets_block.assert_called_once_with(
            sequence_number=1,
            block_size=block_size,
            remaining_data_length=mock_first_frame.data_length.__sub__.return_value)
        mock_isinstance.assert_called_once_with(
            self.mock_can_transport_interface._receive_cf_packets_block.return_value, self.mock_uds_message_record)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("data_length, ff_payload, cf_blocks, sequence_numbers, remaining_data_lengths", [
        (8, [0x12, 0x34], [[Mock(spec=CanPacketRecord, payload=[0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])]], [1], [6]),
        (68, [0x98], [[Mock(spec=CanPacketRecord, payload=list(range(60, 67)), sequence_number=2*i + j + (i%3 == 0)) for j in range(1+i)] for i in range(4)],
         [1, 2, 4, 7], [67, 60, 46, 25])
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_consecutive_frames__cf_received(self, mock_isinstance,
                                                     data_length, ff_payload, cf_blocks,
                                                     sequence_numbers, remaining_data_lengths):
        mock_st_min = Mock()
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=ff_payload,
                                data_length=data_length)
        self.mock_can_transport_interface.receive_packet.side_effect = choice((TimeoutError, ValueError))
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.ContinueToSend, len(cf_block), mock_st_min) for cf_block in cf_blocks]
        mock_isinstance.return_value = False
        self.mock_can_transport_interface._receive_cf_packets_block.side_effect = cf_blocks
        assert (PyCanTransportInterface._receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                    first_frame=mock_first_frame)
                == self.mock_uds_message_record.return_value)
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_br) for _ in cf_blocks])
        self.mock_can_transport_interface._receive_cf_packets_block.assert_has_calls(
            [call(sequence_number=sequence_numbers[i],
                  block_size=len(cf_block),
                  remaining_data_length=remaining_data_lengths[i]) for i, cf_block in enumerate(cf_blocks)])
        all_packets = [mock_first_frame]
        for cf_block in cf_blocks:
            all_packets.append(self.mock_can_transport_interface.send_packet.return_value)
            all_packets.extend(cf_block)
        self.mock_uds_message_record.assert_called_once_with(all_packets)
        mock_isinstance.assert_called()
        self.mock_warn.assert_not_called()

    # _async_receive_consecutive_frames

    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__new_message_interrupted(self):
        mock_first_frame = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME, payload=[])
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert (await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                first_frame=mock_first_frame)
                == self.mock_can_transport_interface._async_message_receive_start.return_value)
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value, loop=None)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_br, loop=None)
        self.mock_can_transport_interface.async_send_packet.assert_not_called()
        self.mock_warn.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__packet_interrupted_then_overflow(self):
        mock_first_frame = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME, payload=[])
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        self.mock_can_transport_interface.flow_control_parameters_generator = [(CanFlowStatus.Overflow, None, None)]
        with pytest.raises(OverflowError):
            await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                            first_frame=mock_first_frame)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_br, loop=None)
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_called_once_with(
            flow_status=CanFlowStatus.Overflow, block_size=None, st_min=None)
        self.mock_can_transport_interface.async_send_packet.assert_called_once_with(
            self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value, loop=None)
        self.mock_warn.assert_called_once()

    @pytest.mark.parametrize("block_size, st_min", [
        (0, 127),
        (Mock(), Mock())
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__wait_then_receive_message(self, mock_isinstance, block_size, st_min):
        mock_first_frame = Mock(spec=CanPacketRecord, packet_type=CanPacketType.FIRST_FRAME, payload=[], data_length=MagicMock())
        self.mock_can_transport_interface.async_receive_packet.side_effect = choice((TimeoutError, ValueError))
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.Wait, None, None), (CanFlowStatus.ContinueToSend, block_size, st_min)]
        mock_isinstance.return_value = True
        assert (await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                first_frame=mock_first_frame)
                == self.mock_can_transport_interface._async_receive_cf_packets_block.return_value)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_br, loop=None),
             call(timeout=self.mock_can_transport_interface.n_br, loop=None)])
        self.mock_can_transport_interface.segmenter.get_flow_control_packet.assert_has_calls(
            [call(flow_status=CanFlowStatus.Wait, block_size=None, st_min=None),
             call(flow_status=CanFlowStatus.ContinueToSend, block_size=block_size, st_min=st_min)])
        self.mock_can_transport_interface.async_send_packet.assert_has_calls(
            [call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value, loop=None),
             call(self.mock_can_transport_interface.segmenter.get_flow_control_packet.return_value, loop=None)])
        self.mock_can_transport_interface._async_receive_cf_packets_block.assert_called_once_with(
            sequence_number=1,
            block_size=block_size,
            remaining_data_length=mock_first_frame.data_length.__sub__.return_value,
            loop=None)
        mock_isinstance.assert_called_once_with(
            self.mock_can_transport_interface._async_receive_cf_packets_block.return_value, self.mock_uds_message_record)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("data_length, ff_payload, cf_blocks, sequence_numbers, remaining_data_lengths", [
        (8, [0x12, 0x34], [[Mock(spec=CanPacketRecord, payload=[0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])]], [1], [6]),
        (68, [0x98], [[Mock(spec=CanPacketRecord, payload=list(range(60, 67)), sequence_number=2*i + j + (i%3 == 0)) for j in range(1+i)] for i in range(4)],
         [1, 2, 4, 7], [67, 60, 46, 25])
    ])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_consecutive_frames__cf_received(self, mock_isinstance,
                                                                 data_length, ff_payload, cf_blocks,
                                                                 sequence_numbers, remaining_data_lengths):
        mock_st_min = Mock()
        mock_first_frame = Mock(spec=CanPacketRecord,
                                packet_type=CanPacketType.FIRST_FRAME,
                                payload=ff_payload,
                                data_length=data_length)
        self.mock_can_transport_interface.async_receive_packet.side_effect = choice((TimeoutError, ValueError))
        self.mock_can_transport_interface.flow_control_parameters_generator = [
            (CanFlowStatus.ContinueToSend, len(cf_block), mock_st_min) for cf_block in cf_blocks]
        mock_isinstance.return_value = False
        self.mock_can_transport_interface._async_receive_cf_packets_block.side_effect = cf_blocks
        assert (await PyCanTransportInterface._async_receive_consecutive_frames(self=self.mock_can_transport_interface,
                                                                                first_frame=mock_first_frame)
                == self.mock_uds_message_record.return_value)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            [call(timeout=self.mock_can_transport_interface.n_br, loop=None) for _ in cf_blocks])
        self.mock_can_transport_interface._async_receive_cf_packets_block.assert_has_calls(
            [call(sequence_number=sequence_numbers[i],
                  block_size=len(cf_block),
                  remaining_data_length=remaining_data_lengths[i],
                  loop=None) for i, cf_block in enumerate(cf_blocks)])
        all_packets = [mock_first_frame]
        for cf_block in cf_blocks:
            all_packets.append(self.mock_can_transport_interface.async_send_packet.return_value)
            all_packets.extend(cf_block)
        self.mock_uds_message_record.assert_called_once_with(all_packets)
        mock_isinstance.assert_called()
        self.mock_warn.assert_not_called()

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
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    def test_send_packet(self, packet):
        mock_get_message = Mock(return_value=MagicMock(arbitration_id=packet.can_id,
                                                       data=packet.raw_frame_data,
                                                       is_rx=True))
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
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is not None
        else:
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is not None
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None

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
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet__timeout(self, packet):
        mock_get_message = Mock(return_value=MagicMock(arbitration_id=packet.can_id,
                                                       data=packet.raw_frame_data,
                                                       is_rx=True))
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured = None
        self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured = None
        self.mock_can_transport_interface.n_ar_timeout = self.mock_can_transport_interface.n_as_timeout \
            = MagicMock(__truediv__=lambda this, other: this,
                        __div__=lambda this, other: this,
                        __sub__=lambda this, other: this,
                        __le__=Mock(return_value=True))
        with pytest.raises(TimeoutError):
            await PyCanTransportInterface.async_send_packet(self.mock_can_transport_interface, packet)
        self.mock_can_id_handler.is_extended_can_id.assert_called_once_with(packet.can_id)
        self.mock_can_dlc_handler.is_can_fd_specific_dlc.assert_called_once_with(packet.dlc)
        self.mock_message.assert_called_once_with(arbitration_id=packet.can_id,
                                                  is_extended_id=self.mock_can_id_handler.is_extended_can_id.return_value,
                                                  data=packet.raw_frame_data,
                                                  is_fd=self.mock_can_dlc_handler.is_can_fd_specific_dlc.return_value)
        self.mock_can_transport_interface.bus_manager.send.assert_called_once_with(self.mock_message.return_value)

    @pytest.mark.parametrize("packet", [
        Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME, raw_frame_data=b"\x12\x34"),
        Mock(spec=CanPacket, packet_type=CanPacketType.FLOW_CONTROL, raw_frame_data=bytes(range(8))),
        Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME, raw_frame_data=bytes(range(64, 128))),
    ])
    @pytest.mark.asyncio
    async def test_async_send_packet(self, packet):
        mock_get_message = Mock(return_value=MagicMock(arbitration_id=packet.can_id,
                                                       data=packet.raw_frame_data,
                                                       is_rx=True))
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(get_message=mock_get_message)
        self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured = None
        self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured = None
        self.mock_can_transport_interface.n_ar_timeout = self.mock_can_transport_interface.n_as_timeout \
            = MagicMock(__truediv__=lambda this, other: this,
                        __div__=lambda this, other: this,
                        __sub__=lambda this, other: this,
                        __le__=Mock(return_value=False))
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
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is not None
        else:
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_as_measured is not None
            assert self.mock_can_transport_interface._PyCanTransportInterface__n_ar_measured is None

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
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock(return_value=None)
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(
            get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
        mock_get_message.assert_called_once()

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    def test_receive_packet__timeout_error__out_of_time(self, timeout):
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(
            get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            PyCanTransportInterface.receive_packet(self.mock_can_transport_interface, timeout)
        mock_is_timeout_reached.assert_called_once_with(self.mock_time.return_value)

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    def test_receive_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = self.mock_can_transport_interface._MAX_LISTENER_TIMEOUT \
            = MagicMock(__sub__=lambda this, other: this,
                        __add__=lambda this, other: this,
                        __mul__=lambda this, other: this,
                        __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__frames_buffer = Mock(
            get_message=mock_get_message)
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
            addressing_format=self.mock_can_transport_interface.segmenter.ADDRESSING_FORMAT,
            transmission_time=self.mock_datetime.fromtimestamp.return_value)

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
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_get_message = Mock()
        self.mock_can_transport_interface._PyCanTransportInterface__async_frames_buffer = Mock(get_message=mock_get_message)
        with pytest.raises(TimeoutError):
            await PyCanTransportInterface.async_receive_packet(self.mock_can_transport_interface, timeout)
        mock_is_timeout_reached.assert_called_once_with(self.mock_time.return_value)

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
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
            addressing_format=self.mock_can_transport_interface.segmenter.ADDRESSING_FORMAT,
            transmission_time=self.mock_datetime.fromtimestamp.return_value)

    # send_message

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.FUNCTIONAL),
    ])
    def test_send_message__single_frame(self, message):
        mock_segmented_message = [Mock(spec=CanPacket)]
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        assert PyCanTransportInterface.send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.send_packet.assert_called_once_with(mock_segmented_message[0])
        self.mock_uds_message_record.assert_called_once_with([self.mock_can_transport_interface.send_packet.return_value])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("st_min", [0x00, 0xFF])
    def test_send_message__multiple_packets__st_min__block_size_0(self, message, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        self.mock_can_transport_interface.n_cs = None
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0,
                                        st_min=st_min)
        self.mock_can_transport_interface.receive_packet = Mock(return_value=mock_flow_control_record)
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert PyCanTransportInterface.send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_bs_timeout)
        self.mock_can_transport_interface._send_cf_packets_block.assert_called_once_with(
            cf_packets_block=mock_segmented_message[1:],
            delay=self.mock_can_st_min_handler.decode.return_value)
        self.mock_can_st_min_handler.decode.assert_called_once_with(st_min)
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record,
            mock_sent_packet_record
        ])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("n_cs, st_min", [
        (0, 0xFF),
        (5, 0x00),
    ])
    def test_send_message__multiple_packets__n_cs__block_size_1(self, message, n_cs, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message[:])
        self.mock_can_transport_interface.n_cs = n_cs
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=1,
                                        st_min=st_min)
        self.mock_can_transport_interface.receive_packet = Mock(return_value=mock_flow_control_record)
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert PyCanTransportInterface.send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.receive_packet.assert_has_calls([
            call(timeout=self.mock_can_transport_interface.n_bs_timeout) for _ in mock_segmented_message[1:]
        ])
        self.mock_can_transport_interface._send_cf_packets_block.assert_has_calls([
            call(cf_packets_block=[packet], delay=n_cs) for packet in mock_segmented_message[1:]
        ])
        self.mock_can_st_min_handler.decode.assert_not_called()
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            *([mock_flow_control_record, mock_sent_packet_record]*len(mock_segmented_message[1:]))
        ])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__wait(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record_wait = Mock(spec=CanPacketRecord,
                                             packet_type=CanPacketType.FLOW_CONTROL,
                                             flow_status=CanFlowStatus.Wait)
        mock_flow_control_record_continue = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.ContinueToSend,
                                                 block_size=0)
        self.mock_can_transport_interface.receive_packet = Mock(
            side_effect=[mock_flow_control_record_wait, mock_flow_control_record_continue])
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert PyCanTransportInterface.send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.receive_packet.assert_has_calls([
            call(timeout=self.mock_can_transport_interface.n_bs_timeout),
            call(timeout=self.mock_can_transport_interface.n_bs_timeout)
        ])
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record_wait,
            mock_flow_control_record_continue,
            mock_sent_packet_record
        ])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__unexpected_packet(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0)
        mock_interrupting_record = Mock(spec=CanPacketRecord,
                                        packet_type=Mock())
        self.mock_can_transport_interface.receive_packet = Mock(
            side_effect=[mock_interrupting_record, mock_flow_control_record])
        self.mock_can_packet_type_is_initial_packet_type.return_value = False
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert PyCanTransportInterface.send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.receive_packet.assert_has_calls([
            call(timeout=self.mock_can_transport_interface.n_bs_timeout),
            call(timeout=self.mock_can_transport_interface.n_bs_timeout)
        ])
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.send_packet.return_value,
            mock_flow_control_record,
            mock_sent_packet_record
        ])
        self.mock_warn.assert_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__overflow(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.Overflow)
        self.mock_can_transport_interface.receive_packet = Mock(return_value=mock_flow_control_record_overflow)
        with pytest.raises(OverflowError):
            PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_bs_timeout)
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    def test_send_message__multiple_packets__unknown_flow_status(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=Mock())
        self.mock_can_transport_interface.receive_packet = Mock(return_value=mock_flow_control_record_overflow)
        with pytest.raises(NotImplementedError):
            PyCanTransportInterface.send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_bs_timeout)
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

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
        self.mock_uds_message_record.assert_called_once_with([self.mock_can_transport_interface.async_send_packet.return_value])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("st_min", [0x00, 0xFF])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__st_min__block_size_0(self, message, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        self.mock_can_transport_interface.n_cs = None
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0,
                                        st_min=st_min)
        self.mock_can_transport_interface.async_receive_packet = AsyncMock(return_value=mock_flow_control_record)
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await PyCanTransportInterface.async_send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None)
        self.mock_can_transport_interface._async_send_cf_packets_block.assert_called_once_with(
            cf_packets_block=mock_segmented_message[1:],
            delay=self.mock_can_st_min_handler.decode.return_value,
            loop=None)
        self.mock_can_st_min_handler.decode.assert_called_once_with(st_min)
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record,
            mock_sent_packet_record
        ])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("n_cs, st_min", [
        (0, 0xFF),
        (5, 0x00),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__n_cs__block_size_1(self, message, n_cs, st_min):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message[:])
        self.mock_can_transport_interface.n_cs = n_cs
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=1,
                                        st_min=st_min)
        self.mock_can_transport_interface.async_receive_packet = AsyncMock(return_value=mock_flow_control_record)
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await PyCanTransportInterface.async_send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls([
            call(timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None) for _ in mock_segmented_message[1:]
        ])
        self.mock_can_transport_interface._async_send_cf_packets_block.assert_has_calls([
            call(cf_packets_block=[packet], delay=n_cs, loop=None) for packet in mock_segmented_message[1:]
        ])
        self.mock_can_st_min_handler.decode.assert_not_called()
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            *([mock_flow_control_record, mock_sent_packet_record]*len(mock_segmented_message[1:]))
        ])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__wait(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record_wait = Mock(spec=CanPacketRecord,
                                             packet_type=CanPacketType.FLOW_CONTROL,
                                             flow_status=CanFlowStatus.Wait)
        mock_flow_control_record_continue = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.ContinueToSend,
                                                 block_size=0)
        self.mock_can_transport_interface.async_receive_packet = AsyncMock(
            side_effect=[mock_flow_control_record_wait, mock_flow_control_record_continue])
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await PyCanTransportInterface.async_send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls([
            call(timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None),
            call(timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None)
        ])
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record_wait,
            mock_flow_control_record_continue,
            mock_sent_packet_record
        ])
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__unexpected_packet(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record = Mock(spec=CanPacketRecord,
                                        packet_type=CanPacketType.FLOW_CONTROL,
                                        flow_status=CanFlowStatus.ContinueToSend,
                                        block_size=0)
        mock_interrupting_record = Mock(spec=CanPacketRecord,
                                        packet_type=Mock())
        self.mock_can_transport_interface.async_receive_packet = AsyncMock(
            side_effect=[mock_interrupting_record, mock_flow_control_record])
        mock_sent_packet_record = Mock(spec=CanPacketRecord)
        self.mock_can_transport_interface._async_send_cf_packets_block.return_value = [mock_sent_packet_record]
        assert await PyCanTransportInterface.async_send_message(
            self.mock_can_transport_interface, message) == self.mock_uds_message_record.return_value
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls([
            call(timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None),
            call(timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None)
        ])
        self.mock_uds_message_record.assert_called_once_with([
            self.mock_can_transport_interface.async_send_packet.return_value,
            mock_flow_control_record,
            mock_sent_packet_record
        ])
        self.mock_warn.assert_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_called_once_with(
            self.mock_uds_message_record.return_value)

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__overflow(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=CanFlowStatus.Overflow)
        self.mock_can_transport_interface.async_receive_packet = AsyncMock(
            return_value=mock_flow_control_record_overflow)
        with pytest.raises(OverflowError):
            await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None)
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    @pytest.mark.parametrize("message", [
        Mock(spec=UdsMessage, payload=[0x22, 0xF1, 0x86, 0xF1, 0x87, 0xF1, 0x88], addressing_type=AddressingType.PHYSICAL),
        Mock(spec=UdsMessage, payload=[0x3E, 0x80], addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.asyncio
    async def test_async_send_message__multiple_packets__unknown_flow_status(self, message):
        mock_segmented_message = [Mock(spec=CanPacket, packet_type=CanPacketType.FIRST_FRAME)]
        mock_segmented_message.extend([Mock(spec=CanPacket, packet_type=CanPacketType.CONSECUTIVE_FRAME)
                                       for _ in range(randint(1, 20))])
        self.mock_can_transport_interface.segmenter.segmentation = Mock(return_value=mock_segmented_message)
        mock_flow_control_record_overflow = Mock(spec=CanPacketRecord,
                                                 packet_type=CanPacketType.FLOW_CONTROL,
                                                 flow_status=Mock())
        self.mock_can_transport_interface.async_receive_packet = AsyncMock(
            return_value=mock_flow_control_record_overflow)
        with pytest.raises(NotImplementedError):
            await PyCanTransportInterface.async_send_message(self.mock_can_transport_interface, message)
        self.mock_can_transport_interface.segmenter.segmentation.assert_called_once_with(message)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=self.mock_can_transport_interface.n_bs_timeout, loop=None)
        self.mock_warn.assert_not_called()
        self.mock_can_transport_interface._update_n_bs_measured.assert_not_called()

    # receive_message

    @pytest.mark.parametrize("timeout", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_receive_message__type_error(self, mock_isinstance, timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            PyCanTransportInterface.receive_message(self.mock_can_transport_interface, timeout)
        mock_isinstance.assert_called_once_with(timeout, (int, float))

    @pytest.mark.parametrize("timeout", [0, -654])
    def test_receive_message__value_error(self, timeout):
        with pytest.raises(ValueError):
            PyCanTransportInterface.receive_message(self.mock_can_transport_interface, timeout)

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    def test_receive_message__timeout_error(self, timeout):
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_received_packet_record = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        self.mock_can_transport_interface.receive_packet.return_value = mock_received_packet_record
        with pytest.raises(TimeoutError):
            PyCanTransportInterface.receive_message(self.mock_can_transport_interface, timeout)
        mock_is_timeout_reached.assert_called_once()

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    def test_receive_message__initial_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert PyCanTransportInterface.receive_message(self.mock_can_transport_interface, timeout) \
            == self.mock_can_transport_interface._message_receive_start.return_value
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value)
        self.mock_can_transport_interface.receive_packet.assert_called_once_with(
            timeout=None if timeout is None else self.mock_time.return_value)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    def test_receive_message__cf_then_initial_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.side_effect = [False, True]
        assert PyCanTransportInterface.receive_message(self.mock_can_transport_interface, timeout) \
            == self.mock_can_transport_interface._message_receive_start.return_value
        self.mock_can_transport_interface._message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.receive_packet.return_value)
        self.mock_can_transport_interface.receive_packet.assert_has_calls(
            calls=[call(timeout=None if timeout is None else self.mock_time.return_value),
                   call(timeout=None if timeout is None else self.mock_time.return_value)]
        )
        self.mock_warn.assert_called_once()

    # async_receive_message

    @pytest.mark.parametrize("timeout", ["something", Mock()])
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    @pytest.mark.asyncio
    async def test_async_receive_message__type_error(self, mock_isinstance, timeout):
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface, timeout)
        mock_isinstance.assert_called_once_with(timeout, (int, float))

    @pytest.mark.parametrize("timeout", [0, -654])
    @pytest.mark.asyncio
    async def test_async_receive_message__value_error(self, timeout):
        with pytest.raises(ValueError):
            await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface, timeout)

    @pytest.mark.parametrize("timeout", [0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_message__timeout_error(self, timeout):
        mock_is_timeout_reached = Mock(return_value=True)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        mock_received_packet_record = Mock(spec=CanPacketRecord, packet_type=CanPacketType.SINGLE_FRAME)
        self.mock_can_transport_interface.receive_packet.return_value = mock_received_packet_record
        with pytest.raises(TimeoutError):
            await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface, timeout)
        mock_is_timeout_reached.assert_called_once()

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_message__initial_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.return_value = True
        assert await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface, timeout) \
            == self.mock_can_transport_interface._async_message_receive_start.return_value
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value, loop=None)
        self.mock_can_transport_interface.async_receive_packet.assert_called_once_with(
            timeout=None if timeout is None else self.mock_time.return_value, loop=None)
        self.mock_warn.assert_not_called()

    @pytest.mark.parametrize("timeout", [None, 0.001, 123.456])
    @pytest.mark.asyncio
    async def test_async_receive_message__cf_then_initial_packet(self, timeout):
        mock_is_timeout_reached = Mock(return_value=False)
        self.mock_time.return_value = MagicMock(__sub__=lambda this, other: this,
                                                __add__=lambda this, other: this,
                                                __mul__=lambda this, other: this,
                                                __le__=mock_is_timeout_reached)
        self.mock_can_packet_type_is_initial_packet_type.side_effect = [False, True]
        assert await PyCanTransportInterface.async_receive_message(self.mock_can_transport_interface, timeout) \
            == self.mock_can_transport_interface._async_message_receive_start.return_value
        self.mock_can_transport_interface._async_message_receive_start.assert_called_once_with(
            initial_packet=self.mock_can_transport_interface.async_receive_packet.return_value, loop=None)
        self.mock_can_transport_interface.async_receive_packet.assert_has_calls(
            calls=[call(timeout=None if timeout is None else self.mock_time.return_value, loop=None),
                   call(timeout=None if timeout is None else self.mock_time.return_value, loop=None)]
        )
        self.mock_warn.assert_called_once()


@pytest.mark.integration
class TestPyCanTransportInterfaceIntegration:
    """Integration tests for `PyCanTransportInterface` class."""

    @pytest.mark.parametrize("init_kwargs", [
        {
            "can_bus_manager": Mock(spec=BusABC),
            "addressing_information": CanAddressingInformation(
                addressing_format=CanAddressingFormat.NORMAL_ADDRESSING,
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
        fc_param_iter = iter(py_can_ti.flow_control_parameters_generator)
        for _ in range(5):
            assert next(fc_param_iter) == (CanFlowStatus.ContinueToSend, 0, 0)

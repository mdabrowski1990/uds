__all__ = ['BaseSystemTests']

import asyncio
from abc import ABC
from threading import Timer
from typing import List, Optional

from uds.message import UdsMessage, UdsMessageRecord
from uds.packet import AbstractPacket, AbstractPacketRecord
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import TimeMillisecondsAlias


class BaseSystemTests(ABC):
    """Base implementation for all system tests suites."""

    MAKE_TIMING_CHECKS: bool = True
    TASK_TIMING_TOLERANCE: TimeMillisecondsAlias = 20
    TIMESTAMP_TOLERANCE: TimeMillisecondsAlias = 1

    sent_message: Optional[UdsMessageRecord]
    received_message: Optional[UdsMessageRecord]
    sent_packet: Optional[AbstractPacketRecord]
    _timers: List[Timer]

    def setup_method(self):
        """
        Common setup:
        - define common variables
        """
        self.sent_message: Optional[UdsMessageRecord] = None
        self.received_message: Optional[UdsMessageRecord] = None
        self.sent_packet: Optional[AbstractPacketRecord] = None
        self._timers: List[Timer] = []

    def teardown_method(self):
        """
        Common teardown:
        - finish and kill all open tasks
        """
        for _timer in self._timers:
            _timer.cancel()
        if self._timers:
            for _timer in self._timers:
                _timer.join(self.TASK_TIMING_TOLERANCE / 1000.)
                del _timer
            self._timers = []

    def send_packet(self,
                    transport_interface: AbstractTransportInterface,
                    packet: AbstractPacket,
                    delay: TimeMillisecondsAlias) -> Timer:
        """
        Send a packet over Transport Interface.

        .. note:: The result (packet record) will be available be in `self.sent_packet` attribute.

        :param transport_interface: Transport Interface to use for transmission.
        :param packet: Packet to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Timer object with scheduled task.
        """

        def _send_packet():
            self.sent_packet = transport_interface.send_packet(packet)

        timer = Timer(interval=delay/1000., function=_send_packet)
        self._timers.append(timer)
        timer.start()
        return timer

    @staticmethod
    async def async_send_packet(transport_interface: AbstractTransportInterface,
                                packet: AbstractPacket,
                                delay: TimeMillisecondsAlias) -> AbstractPacketRecord:
        """
        Send a packet asynchronously over Transport Interface.

        :param transport_interface: Transport Interface to use for transmission.
        :param packet: Packet to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Future CAN packet record.
        """
        await asyncio.sleep(delay / 1000.)
        return await transport_interface.async_send_packet(packet=packet)

    def receive_message(self,
                        transport_interface: AbstractTransportInterface,
                        start_timeout: Optional[TimeMillisecondsAlias],
                        end_timeout: Optional[TimeMillisecondsAlias],
                        delay: TimeMillisecondsAlias) -> Timer:
        """
        Receive UDS message over Transport Interface.

        .. note:: The result (UDS message record) will be available be in `self.sent_message` attribute.

        :param transport_interface: Transport Interface to use for transmission.
        :param start_timeout: Maximal time (in milliseconds) to wait for UDS message transmission to start.
        :param end_timeout: Maximal time (in milliseconds) to wait for UDS message transmission to finish.
        :param delay: Time [ms] after which the reception will be started.

        :return: Timer object with scheduled task.
        """

        def _receive_message():
            self.received_message = transport_interface.receive_message(start_timeout=start_timeout,
                                                                        end_timeout=end_timeout)

        timer = Timer(interval=delay/1000., function=_receive_message)
        self._timers.append(timer)
        timer.start()
        return timer

    def send_message(self,
                     transport_interface: AbstractTransportInterface,
                     message: UdsMessage,
                     delay: TimeMillisecondsAlias) -> Timer:
        """
        Send UDS message over Transport Interface.

        .. note:: The result (UDS message record) will be available be in `self.sent_message` attribute.

        :param transport_interface: Transport Interface to use for transmission.
        :param message: UDS message to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Timer object with scheduled task.
        """

        def _send_message():
            self.sent_message = transport_interface.send_message(message)

        timer = Timer(interval=delay/1000., function=_send_message)
        self._timers.append(timer)
        timer.start()
        return timer

    @staticmethod
    async def async_send_message(transport_interface: AbstractTransportInterface,
                                 message: UdsMessage,
                                 delay: TimeMillisecondsAlias) -> UdsMessageRecord:
        """
        Send UDS message asynchronously over Transport Interface.

        :param transport_interface: Transport Interface to use for transmission.
        :param message: UDS message to send.
        :param delay: Time [ms] after which the transmission will be started.

        :return: Future UDS message record.
        """
        await asyncio.sleep(delay / 1000.)
        return await transport_interface.async_send_message(message=message)

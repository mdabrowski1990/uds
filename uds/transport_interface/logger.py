"""Logger implementation for Transport Interfaces."""

__all__ = ["TransportLogger"]

import functools
from copy import copy
from inspect import iscoroutinefunction
from logging import INFO, getLogger
from typing import Any, Awaitable, Callable, Optional, Type, Union

from uds.message import UdsMessageRecord
from uds.packet import AbstractPacketRecord

from .abstract_transport_interface import AbstractTransportInterface


class TransportLogger:
    """Configurable logger for Transport Interface objects."""

    TransportInterfaceAlias = Union[AbstractTransportInterface, Type[AbstractTransportInterface]]
    """Alias of Transport Interface (either class or instance)."""
    MessageMethodAlias = Callable[[Any], Union[UdsMessageRecord, Awaitable[UdsMessageRecord]]]
    """Alias of transmitting/receiving UDS Message method."""
    PacketMethodAlias = Callable[[Any], Union[AbstractPacketRecord, Awaitable[AbstractPacketRecord]]]
    """Alias of transmitting/receiving Packet method."""

    def __init__(self,
                 *,
                 logger_name: Optional[str] = None,
                 message_logging_level: Optional[int] = INFO,
                 packet_logging_level: Optional[int] = INFO,
                 log_sending: bool = True,
                 log_receiving: bool = True,
                 message_log_format: str = "{record}",
                 packet_log_format: str = "{record}") -> None:
        """
        Configure transport logging.

        :param message_logging_level: Logging level to use for UDS Messages logging.
        :param packet_logging_level: Logging level to use for Packets logging.
        :param log_receiving: Whether to log received messages/packets.
        :param message_log_format: Log messages format for UDS Messages.
            It has to be defined as a str on which format method would be called with record parameter.
        :param packet_log_format: Log messages format for Packets.
            It has to be defined as a str on which format method would be called with record parameter.
        """
        self.__logger = getLogger(logger_name)
        self.message_logging_level = message_logging_level
        self.packet_logging_level = packet_logging_level
        self.log_sending = log_sending
        self.log_receiving = log_receiving
        self.message_log_format = message_log_format
        self.packet_log_format = packet_log_format

    def __call__(self, transport_interface: TransportInterfaceAlias) -> TransportInterfaceAlias:
        """Decorate Transport Interface."""
        if isinstance(transport_interface, AbstractTransportInterface):
            return self._decorate_instance(transport_interface)
        if isinstance(transport_interface, type) and issubclass(transport_interface, AbstractTransportInterface):
            return self._decorate_class(transport_interface)
        raise TypeError("Provided value is not an instance neither subclass of AbstractTransportInterface. "
                        f"Actual type: {type(transport_interface)}.")

    def _decorate_class(self, cls: Type[AbstractTransportInterface]) -> Type[AbstractTransportInterface]:
        """Decorate Transport Interface class."""
        attributes_to_overwrite = {}
        if self.log_sending:
            if self.message_logging_level is not None:
                attributes_to_overwrite["send_message"] = self._decorate_message_method(cls.send_message)
                attributes_to_overwrite["async_send_message"] = self._decorate_message_method(cls.async_send_message)
            if self.packet_logging_level is not None:
                attributes_to_overwrite["send_packet"] =  self._decorate_packet_method(cls.send_packet)
                attributes_to_overwrite["async_send_packet"] = self._decorate_packet_method(cls.async_send_packet)
        if self.log_receiving:
            if self.message_logging_level is not None:
                attributes_to_overwrite["receive_message"] = self._decorate_message_method(cls.receive_message)
                attributes_to_overwrite["async_receive_message"] = self._decorate_message_method(cls.async_receive_message)
            if self.packet_logging_level is not None:
                attributes_to_overwrite["receive_packet"] = self._decorate_packet_method(cls.receive_packet)
                attributes_to_overwrite["async_receive_packet"] = self._decorate_packet_method(cls.async_receive_packet)
        return type(f"{cls.__name__}WithLogger", (cls,), attributes_to_overwrite)

    def _decorate_instance(self, instance: AbstractTransportInterface) -> AbstractTransportInterface:
        """Decorate Transport Interface instance."""
        cls = instance.__class__
        decorated = copy(instance)
        if self.log_sending:
            if self.message_logging_level is not None:
                decorated.send_message = self._decorate_message_method(cls.send_message).__get__(decorated, cls)
                decorated.async_send_message = self._decorate_message_method(cls.async_send_message).__get__(decorated, cls)
            if self.packet_logging_level is not None:
                decorated.send_packet =  self._decorate_packet_method(cls.send_packet).__get__(decorated, cls)
                decorated.async_send_packet = self._decorate_packet_method(cls.async_send_packet).__get__(decorated, cls)
        if self.log_receiving:
            if self.message_logging_level is not None:
                decorated.receive_message = self._decorate_message_method(cls.receive_message).__get__(decorated, cls)
                decorated.async_receive_message = self._decorate_message_method(cls.async_receive_message).__get__(decorated, cls)
            if self.packet_logging_level is not None:
                decorated.receive_packet = self._decorate_packet_method(cls.receive_packet).__get__(decorated, cls)
                decorated.async_receive_packet = self._decorate_packet_method(cls.async_receive_packet).__get__(decorated, cls)
        return decorated

    def _decorate_message_method(self, method: MessageMethodAlias) -> MessageMethodAlias:
        """Decorate method that either transmits or receives UDS Message."""
        if iscoroutinefunction(method):
            @functools.wraps(method)
            async def decorated_method(*args: Any, **kwargs: Any) -> UdsMessageRecord:
                message_record = await method(*args, **kwargs)
                self.log_message(message_record)
                return message_record
        else:
            @functools.wraps(method)
            def decorated_method(*args: Any, **kwargs: Any) -> UdsMessageRecord:
                message_record = method(*args, **kwargs)
                self.log_message(message_record)
                return message_record
        return decorated_method

    def _decorate_packet_method(self, method: PacketMethodAlias) -> PacketMethodAlias:
        """Decorate method that either transmits or receives Packet."""
        if iscoroutinefunction(method):
            @functools.wraps(method)
            async def decorated_method(*args: Any, **kwargs: Any) -> AbstractPacketRecord:
                packet_record = await method(*args, **kwargs)
                self.log_packet(packet_record)
                return packet_record
        else:
            @functools.wraps(method)
            def decorated_method(*args: Any, **kwargs: Any) -> AbstractPacketRecord:
                packet_record = method(*args, **kwargs)
                self.log_packet(packet_record)
                return packet_record
        return decorated_method

    def log_message(self, record: UdsMessageRecord) -> None:
        """Log a message after receiving/transmitting UDS Message."""
        self.__logger.log(level=self.message_logging_level,
                          msg=self.message_log_format.format(record=record))

    def log_packet(self, record: AbstractPacketRecord):
        """Log a message after receiving/transmitting Packet."""
        self.__logger.log(level=self.packet_logging_level,
                          msg=self.packet_log_format.format(record=record))

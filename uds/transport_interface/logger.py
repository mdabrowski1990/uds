"""Logger implementation for Transport Interfaces."""

__all__ = ["TransportLogger"]

from copy import copy
from functools import wraps
from inspect import iscoroutinefunction
from logging import INFO, Logger, getLogger
from typing import Any, Callable, Optional, Type, Union

from uds.message import UdsMessageRecord
from uds.packet import AbstractPacketRecord

from .abstract_transport_interface import AbstractTransportInterface


class TransportLogger:
    """Configurable logger for Transport Interface objects."""

    TransportInterfaceAlias = Union[AbstractTransportInterface, Type[AbstractTransportInterface]]
    """Alias of Transport Interface (either class or instance)."""

    DEFAULT_LOG_FORMAT: str = "{record.direction.name} {record}"

    def __init__(self,
                 *,
                 logger_name: Optional[str] = None,
                 message_logging_level: Optional[int] = INFO,
                 packet_logging_level: Optional[int] = INFO,
                 log_sending: bool = True,
                 log_receiving: bool = True,
                 message_log_format: str = DEFAULT_LOG_FORMAT,
                 packet_log_format: str = DEFAULT_LOG_FORMAT) -> None:
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

    @property
    def logger(self) -> Logger:
        """Get configured Logger (from logging package)."""
        return self.__logger

    @property
    def message_logging_level(self) -> Optional[int]:
        """Get logging level to use for UDS Messages logging."""
        return self.__message_logging_level

    @message_logging_level.setter
    def message_logging_level(self, value: Optional[int]) -> None:
        """
        Set logging level to use for UDS Messages logging.

        :param value: Either log level to use or None if UDS Messages are not supposed to be logged.

        :raise TypeError: Provided value is not None neither int type.
        """
        if value is not None and not isinstance(value, int):
            raise TypeError(f"Provided value is not None neither int type. Actual type: {type(value)}.")
        self.__message_logging_level = value

    @property
    def packet_logging_level(self) -> Optional[int]:
        """Get logging level to use for Packets logging."""
        return self.__packet_logging_level

    @packet_logging_level.setter
    def packet_logging_level(self, value: Optional[int]) -> None:
        """
        Set logging level to use for Packets logging.

        :param value: Either log level to use or None if Packets are not supposed to be logged.

        :raise TypeError: Provided value is not None neither int type.
        """
        if value is not None and not isinstance(value, int):
            raise TypeError(f"Provided value is not None neither int type. Actual type: {type(value)}.")
        self.__packet_logging_level = value

    @property
    def log_sending(self) -> bool:
        """Get information whether outgoing traffic shall be logged."""
        return self.__log_sending

    @log_sending.setter
    def log_sending(self, value: bool) -> None:
        """Set whether outgoing traffic shall be logged."""
        self.__log_sending = bool(value)

    @property
    def log_receiving(self) -> bool:
        """Get information whether incoming traffic shall be logged."""
        return self.__log_receiving

    @log_receiving.setter
    def log_receiving(self, value: bool) -> None:
        """Set whether outgoing traffic shall be logged."""
        self.__log_receiving = bool(value)

    @property
    def message_log_format(self) -> str:
        """Get log messages format for UDS Messages."""
        return self.__message_log_format

    @message_log_format.setter
    def message_log_format(self, value: str) -> None:
        """
        Set log messages format for UDS Messages.

        :param value: Value to set.
            It has to be defined as a str on which format method would be called with record parameter.

        :raise TypeError: Provided value is not str type.
        """
        if not isinstance(value, str):
            raise TypeError(f"Provided value is not str type. Actual type: {type(value)}.")
        self.__message_log_format = value

    @property
    def packet_log_format(self) -> str:
        """Get log messages format for Packets."""
        return self.__packet_log_format

    @packet_log_format.setter
    def packet_log_format(self, value: str) -> None:
        """
        Set log messages format for Packets.

        :param value: Value to set.
            It has to be defined as a str on which format method would be called with record parameter.

        :raise TypeError: Provided value is not str type.
        """
        if not isinstance(value, str):
            raise TypeError(f"Provided value is not str type. Actual type: {type(value)}.")
        self.__packet_log_format = value

    def _decorate_class(self, cls: Type[AbstractTransportInterface]) -> Type[AbstractTransportInterface]:
        """Decorate Transport Interface class."""
        attributes_to_overwrite = {}
        if self.log_sending:
            if self.message_logging_level is not None:
                attributes_to_overwrite["send_message"] = self._decorate_message_method(cls.send_message)
                attributes_to_overwrite["async_send_message"] = self._decorate_message_method(cls.async_send_message)
            if self.packet_logging_level is not None:
                attributes_to_overwrite["send_packet"] = self._decorate_packet_method(cls.send_packet)
                attributes_to_overwrite["async_send_packet"] = self._decorate_packet_method(cls.async_send_packet)
        if self.log_receiving:
            if self.message_logging_level is not None:
                attributes_to_overwrite["receive_message"] = self._decorate_message_method(cls.receive_message)
                attributes_to_overwrite["async_receive_message"] \
                    = self._decorate_message_method(cls.async_receive_message)
            if self.packet_logging_level is not None:
                attributes_to_overwrite["receive_packet"] = self._decorate_packet_method(cls.receive_packet)
                attributes_to_overwrite["async_receive_packet"] = self._decorate_packet_method(cls.async_receive_packet)
        return type(f"{cls.__name__}WithLogger", (cls,), attributes_to_overwrite)

    def _decorate_instance(self, instance: AbstractTransportInterface) -> AbstractTransportInterface:
        """Decorate Transport Interface instance."""
        # pylint: disable=too-many-function-args
        cls = instance.__class__
        decorated = copy(instance)
        if self.log_sending:
            if self.message_logging_level is not None:
                setattr(decorated,
                        "send_message",
                        self._decorate_message_method(cls.send_message).__get__(decorated, cls))
                setattr(decorated,
                        "async_send_message",
                        self._decorate_message_method(cls.async_send_message).__get__(decorated, cls))
            if self.packet_logging_level is not None:
                setattr(decorated,
                        "send_packet",
                        self._decorate_packet_method(cls.send_packet).__get__(decorated, cls))
                setattr(decorated,
                        "async_send_packet",
                        self._decorate_packet_method(cls.async_send_packet).__get__(decorated, cls))
        if self.log_receiving:
            if self.message_logging_level is not None:
                setattr(decorated,
                        "receive_message",
                        self._decorate_message_method(cls.receive_message).__get__(decorated, cls))
                setattr(decorated,
                        "async_receive_message",
                        self._decorate_message_method(cls.async_receive_message).__get__(decorated, cls))
            if self.packet_logging_level is not None:
                setattr(decorated,
                        "receive_packet",
                        self._decorate_packet_method(cls.receive_packet).__get__(decorated, cls))
                setattr(decorated,
                        "async_receive_packet",
                        self._decorate_packet_method(cls.async_receive_packet).__get__(decorated, cls))
        return decorated

    def _decorate_message_method(self, method: Callable) -> Callable:  # type: ignore
        """Decorate method that either transmits or receives UDS Message."""
        if iscoroutinefunction(method):
            @wraps(method)
            async def decorated_method(*args: Any, **kwargs: Any) -> UdsMessageRecord:
                message_record: UdsMessageRecord = await method(*args, **kwargs)
                self.log_message(message_record)
                return message_record
        else:
            @wraps(method)
            def decorated_method(*args: Any, **kwargs: Any) -> UdsMessageRecord:
                message_record: UdsMessageRecord = method(*args, **kwargs)
                self.log_message(message_record)
                return message_record
        return decorated_method

    def _decorate_packet_method(self, method: Callable) -> Callable:  # type: ignore
        """Decorate method that either transmits or receives Packet."""
        if iscoroutinefunction(method):
            @wraps(method)
            async def decorated_method(*args: Any, **kwargs: Any) -> AbstractPacketRecord:
                packet_record: AbstractPacketRecord = await method(*args, **kwargs)
                self.log_packet(packet_record)
                return packet_record
        else:
            @wraps(method)
            def decorated_method(*args: Any, **kwargs: Any) -> AbstractPacketRecord:
                packet_record: AbstractPacketRecord = method(*args, **kwargs)
                self.log_packet(packet_record)
                return packet_record
        return decorated_method

    def log_message(self, record: UdsMessageRecord) -> None:
        """Log a message after receiving/transmitting UDS Message."""
        if self.message_logging_level is not None:
            self.logger.log(level=self.message_logging_level,
                            msg=self.message_log_format.format(record=record))

    def log_packet(self, record: AbstractPacketRecord) -> None:
        """Log a message after receiving/transmitting Packet."""
        if self.packet_logging_level is not None:
            self.logger.log(level=self.packet_logging_level,
                            msg=self.packet_log_format.format(record=record))

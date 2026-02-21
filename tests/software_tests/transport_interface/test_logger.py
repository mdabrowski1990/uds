import pytest
from mock import AsyncMock, MagicMock, Mock, call, patch

from uds.transport_interface.logger import (
    INFO,
    AbstractPacketRecord,
    AbstractTransportInterface,
    TransportLogger,
    UdsMessageRecord,
)

SCRIPT_LOCATION = "uds.transport_interface.logger"


class TestTransportLogger:
    """Unit tests for `TransportLogger` class."""

    def setup_method(self):
        self.mock_transport_logger = Mock(spec=TransportLogger,
                                          DECORATED_CLASS_NAME_SUFFIX=TransportLogger.DECORATED_CLASS_NAME_SUFFIX)
        # patching
        self._patcher_get_logger = patch(f"{SCRIPT_LOCATION}.getLogger")
        self.mock_get_logger = self._patcher_get_logger.start()
        self._patcher_copy = patch(f"{SCRIPT_LOCATION}.copy")
        self.mock_copy = self._patcher_copy.start()

    def teardown_method(self):
        self._patcher_get_logger.stop()
        self._patcher_copy.stop()

    # __init__

    def test_init__mandatory(self):
        assert TransportLogger.__init__(self.mock_transport_logger) is None
        assert self.mock_transport_logger._TransportLogger__logger == self.mock_get_logger.return_value
        assert self.mock_transport_logger.message_logging_level == INFO
        assert self.mock_transport_logger.packet_logging_level == INFO
        assert self.mock_transport_logger.log_sending is True
        assert self.mock_transport_logger.log_receiving is True
        assert self.mock_transport_logger.message_log_format == TransportLogger.DEFAULT_LOG_FORMAT
        assert self.mock_transport_logger.packet_log_format == TransportLogger.DEFAULT_LOG_FORMAT
        self.mock_get_logger.assert_called_once_with(None)

    @pytest.mark.parametrize("logger_name, message_logging_level, packet_logging_level, log_sending, log_receiving, "
                             "message_log_format, packet_log_format", [
        (Mock(), Mock() ,Mock() ,Mock() ,Mock(), Mock(), Mock()),
        ("logger_name", "message_logging_level", "packet_logging_level", "log_sending", "log_receiving",
         "message_log_format", "packet_log_format"),
    ])
    def test_init__all(self, logger_name, message_logging_level, packet_logging_level, log_sending, log_receiving,
                       message_log_format, packet_log_format):
        assert TransportLogger.__init__(self.mock_transport_logger,
                                        logger_name=logger_name,
                                        message_logging_level=message_logging_level,
                                        packet_logging_level=packet_logging_level,
                                        log_sending=log_sending,
                                        log_receiving=log_receiving,
                                        message_log_format=message_log_format,
                                        packet_log_format=packet_log_format) is None
        assert self.mock_transport_logger._TransportLogger__logger == self.mock_get_logger.return_value
        assert self.mock_transport_logger.message_logging_level == message_logging_level
        assert self.mock_transport_logger.packet_logging_level == packet_logging_level
        assert self.mock_transport_logger.log_sending == log_sending
        assert self.mock_transport_logger.log_receiving == log_receiving
        assert self.mock_transport_logger.message_log_format == message_log_format
        assert self.mock_transport_logger.packet_log_format == packet_log_format
        self.mock_get_logger.assert_called_once_with(logger_name)

    # __call__

    @patch(f"{SCRIPT_LOCATION}.issubclass")
    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_call__type_error(self, mock_isinstance, mock_issubclass):
        mock_transport_interface = Mock()
        mock_isinstance.return_value = False
        mock_issubclass.return_value = False
        with pytest.raises(TypeError):
            TransportLogger.__call__(self.mock_transport_logger, mock_transport_interface)

    def test_call__instance(self):
        mock_transport_interface_instance = Mock(spec=AbstractTransportInterface)
        assert (TransportLogger.__call__(self.mock_transport_logger, mock_transport_interface_instance)
                == self.mock_transport_logger._decorate_instance.return_value)
        self.mock_transport_logger._decorate_instance.assert_called_once_with(mock_transport_interface_instance)
        self.mock_transport_logger._decorate_class.assert_not_called()

    def test_call__class(self):
        class MockTransportInterfaceClass(AbstractTransportInterface):
            ...

        assert (TransportLogger.__call__(self.mock_transport_logger, MockTransportInterfaceClass)
                == self.mock_transport_logger._decorate_class.return_value)
        self.mock_transport_logger._decorate_instance.assert_not_called()
        self.mock_transport_logger._decorate_class.assert_called_once_with(MockTransportInterfaceClass)

    # logger

    def test_logger__get(self):
        self.mock_transport_logger._TransportLogger__logger = Mock()
        assert (TransportLogger.logger.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__logger)

    # message_logging_level

    def test_message_logging_level__get(self):
        self.mock_transport_logger._TransportLogger__message_logging_level = Mock()
        assert (TransportLogger.message_logging_level.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__message_logging_level)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_message_logging_level__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TransportLogger.message_logging_level.fset(self.mock_transport_logger, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)

    @pytest.mark.parametrize("value", [None, INFO])
    def test_message_logging_level__set__valid(self, value):
        assert TransportLogger.message_logging_level.fset(self.mock_transport_logger, value) is None
        assert self.mock_transport_logger._TransportLogger__message_logging_level == value

    # packet_logging_level

    def test_packet_logging_level__get(self):
        self.mock_transport_logger._TransportLogger__packet_logging_level = Mock()
        assert (TransportLogger.packet_logging_level.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__packet_logging_level)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_packet_logging_level__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TransportLogger.packet_logging_level.fset(self.mock_transport_logger, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, int)

    @pytest.mark.parametrize("value", [None, INFO])
    def test_packet_logging_level__set__valid(self, value):
        assert TransportLogger.packet_logging_level.fset(self.mock_transport_logger, value) is None
        assert self.mock_transport_logger._TransportLogger__packet_logging_level == value

    # log_sending

    def test_log_sending__get(self):
        self.mock_transport_logger._TransportLogger__log_sending = Mock()
        assert (TransportLogger.log_sending.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__log_sending)

    @patch(f"{SCRIPT_LOCATION}.bool")
    def test_log_sending__set(self, mock_bool):
        mock_value = Mock()
        assert TransportLogger.log_sending.fset(self.mock_transport_logger, mock_value) is None
        assert self.mock_transport_logger._TransportLogger__log_sending == mock_bool.return_value
        mock_bool.assert_called_once_with(mock_value)

    # log_receiving

    def test_log_receiving__get(self):
        self.mock_transport_logger._TransportLogger__log_receiving = Mock()
        assert (TransportLogger.log_receiving.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__log_receiving)

    @patch(f"{SCRIPT_LOCATION}.bool")
    def test_log_receiving__set(self, mock_bool):
        mock_value = Mock()
        assert TransportLogger.log_receiving.fset(self.mock_transport_logger, mock_value) is None
        assert self.mock_transport_logger._TransportLogger__log_receiving == mock_bool.return_value
        mock_bool.assert_called_once_with(mock_value)
        
    # message_log_format

    def test_message_log_format__get(self):
        self.mock_transport_logger._TransportLogger__message_log_format = Mock()
        assert (TransportLogger.message_log_format.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__message_log_format)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_message_log_format__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TransportLogger.message_log_format.fset(self.mock_transport_logger, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)

    @pytest.mark.parametrize("value", [TransportLogger.DEFAULT_LOG_FORMAT, "Message: {record}"])
    def test_message_log_format__set__valid(self, value):
        assert TransportLogger.message_log_format.fset(self.mock_transport_logger, value) is None
        assert self.mock_transport_logger._TransportLogger__message_log_format == value
        
    # packet_log_format

    def test_packet_log_format__get(self):
        self.mock_transport_logger._TransportLogger__packet_log_format = Mock()
        assert (TransportLogger.packet_log_format.fget(self.mock_transport_logger)
                == self.mock_transport_logger._TransportLogger__packet_log_format)

    @patch(f"{SCRIPT_LOCATION}.isinstance")
    def test_packet_log_format__set__type_error(self, mock_isinstance):
        mock_value = Mock()
        mock_isinstance.return_value = False
        with pytest.raises(TypeError):
            TransportLogger.packet_log_format.fset(self.mock_transport_logger, mock_value)
        mock_isinstance.assert_called_once_with(mock_value, str)

    @pytest.mark.parametrize("value", [TransportLogger.DEFAULT_LOG_FORMAT, "Packet: {record}"])
    def test_packet_log_format__set__valid(self, value):
        assert TransportLogger.packet_log_format.fset(self.mock_transport_logger, value) is None
        assert self.mock_transport_logger._TransportLogger__packet_log_format == value

    # _decorate_class

    @pytest.mark.parametrize("name, log_sending, log_receiving, message_logging_level, packet_logging_level", [
        ("AbstractTransportInterface", False, False, None, None),
        ("PyCanTransportInterface", True, False, 10, None),
        ("EthernetTransportInterface", True, False, None, INFO),
        ("AbstractCanTransportInterface", False, True, None, 1),
        ("CustomTransportInterface", False, True, 2, None),
        ("SomeClass", True, True, 0, 0),
    ])
    @patch(f"{SCRIPT_LOCATION}.type")
    def test_decorate_class(self, mock_type, name,
                            log_sending, log_receiving, message_logging_level, packet_logging_level):
        mock_class = MagicMock(__name__=name)
        self.mock_transport_logger.log_sending = log_sending
        self.mock_transport_logger.log_receiving = log_receiving
        self.mock_transport_logger.message_logging_level = message_logging_level
        self.mock_transport_logger.packet_logging_level = packet_logging_level
        decorated_methods = {}
        if log_sending and message_logging_level is not None:
            decorated_methods["send_message"] = self.mock_transport_logger._decorate_message_method.return_value
            decorated_methods["async_send_message"] = self.mock_transport_logger._decorate_message_method.return_value
        if log_sending and packet_logging_level is not None:
            decorated_methods["send_packet"] = self.mock_transport_logger._decorate_packet_method.return_value
            decorated_methods["async_send_packet"] = self.mock_transport_logger._decorate_packet_method.return_value
        if log_receiving and message_logging_level is not None:
            decorated_methods["receive_message"] = self.mock_transport_logger._decorate_message_method.return_value
            decorated_methods["async_receive_message"] = self.mock_transport_logger._decorate_message_method.return_value
        if log_receiving and packet_logging_level is not None:
            decorated_methods["receive_packet"] = self.mock_transport_logger._decorate_packet_method.return_value
            decorated_methods["async_receive_packet"] = self.mock_transport_logger._decorate_packet_method.return_value
        assert TransportLogger._decorate_class(self.mock_transport_logger, mock_class) == mock_type.return_value
        mock_type.assert_called_once_with(name + self.mock_transport_logger.DECORATED_CLASS_NAME_SUFFIX,
                                          (mock_class,),
                                          decorated_methods)

    # _decorate_instance

    @pytest.mark.parametrize("log_sending, log_receiving, message_logging_level, packet_logging_level", [
        (False, False, None, None),
        (True, False, 10, None),
        (True, False, None, INFO),
        (False, True, None, 1),
        (False, True, 2, None),
        (True, True, 0, 0),
    ])
    @patch(f"{SCRIPT_LOCATION}.setattr")
    def test_decorate_instance(self, mock_setattr,
                               log_sending, log_receiving, message_logging_level, packet_logging_level):
        mock_class = Mock()
        mock_instance = MagicMock(__class__=mock_class)
        self.mock_transport_logger.log_sending = log_sending
        self.mock_transport_logger.log_receiving = log_receiving
        self.mock_transport_logger.message_logging_level = message_logging_level
        self.mock_transport_logger.packet_logging_level = packet_logging_level
        self.mock_transport_logger._decorate_message_method = Mock(return_value=MagicMock(__get__=Mock()))
        self.mock_transport_logger._decorate_packet_method = Mock(return_value=MagicMock(__get__=Mock()))
        calls = []
        if log_sending and message_logging_level is not None:
            calls.append(call(self.mock_copy.return_value,
                              "send_message",
                              self.mock_transport_logger._decorate_message_method.return_value.__get__.return_value))
            calls.append(call(self.mock_copy.return_value,
                              "async_send_message",
                              self.mock_transport_logger._decorate_message_method.return_value.__get__.return_value))
        if log_sending and packet_logging_level is not None:
            calls.append(call(self.mock_copy.return_value,
                              "send_packet",
                              self.mock_transport_logger._decorate_packet_method.return_value.__get__.return_value))
            calls.append(call(self.mock_copy.return_value,
                              "async_send_packet",
                              self.mock_transport_logger._decorate_packet_method.return_value.__get__.return_value))
        if log_receiving and message_logging_level is not None:
            calls.append(call(self.mock_copy.return_value,
                              "receive_message",
                              self.mock_transport_logger._decorate_message_method.return_value.__get__.return_value))
            calls.append(call(self.mock_copy.return_value,
                              "async_receive_message",
                              self.mock_transport_logger._decorate_message_method.return_value.__get__.return_value))
        if log_receiving and packet_logging_level is not None:
            calls.append(call(self.mock_copy.return_value,
                              "receive_packet",
                              self.mock_transport_logger._decorate_packet_method.return_value.__get__.return_value))
            calls.append(call(self.mock_copy.return_value,
                              "async_receive_packet",
                              self.mock_transport_logger._decorate_packet_method.return_value.__get__.return_value))
        assert (TransportLogger._decorate_instance(self.mock_transport_logger, mock_instance)
                == self.mock_copy.return_value)
        mock_setattr.assert_has_calls(calls,
                                      any_order=True)

    # _decorate_message_method

    @pytest.mark.parametrize("method", [Mock(), AsyncMock()])
    @patch(f"{SCRIPT_LOCATION}.wraps")
    def test_decorate_message_method(self, mock_wraps, method):
        assert (TransportLogger._decorate_message_method(self.mock_transport_logger, method)
                == mock_wraps.return_value.return_value)
        mock_wraps.assert_called_once_with(method)

    @pytest.mark.parametrize("method, args, kwargs", [
        (Mock(spec=AbstractTransportInterface).send_message, (None, "some arg"), {"a": 1, "kwarg_arg": Mock()}),
        (Mock(spec=AbstractTransportInterface).receive_message, (), {"param_1": "value_1", "param_2": "value_2"}),
    ])
    def test_decorate_message_method__sync_decorated_method(self, method, args, kwargs):
        decorated_method = TransportLogger._decorate_message_method(self.mock_transport_logger, method)
        assert decorated_method(*args, **kwargs) == method.return_value
        method.assert_called_once_with(*args, **kwargs)
        self.mock_transport_logger.log_message.assert_called_once_with(method.return_value)

    @pytest.mark.parametrize("method, args, kwargs", [
        (AsyncMock(spec=AbstractTransportInterface).async_send_message, (None, "some arg"), {"a": 1, "kwarg_arg": Mock()}),
        (AsyncMock(spec=AbstractTransportInterface).async_receive_message, (), {"param_1": "value_1", "param_2": "value_2"}),
    ])
    @pytest.mark.asyncio
    async def test_decorate_message_method__async_decorated_method(self, method, args, kwargs):
        decorated_method = TransportLogger._decorate_message_method(self.mock_transport_logger, method)
        assert await decorated_method(*args, **kwargs) == method.return_value
        method.assert_called_once_with(*args, **kwargs)
        self.mock_transport_logger.log_message.assert_called_once_with(method.return_value)

    # _decorate_packet_method

    @pytest.mark.parametrize("method", [Mock(), AsyncMock()])
    @patch(f"{SCRIPT_LOCATION}.wraps")
    def test_decorate_packet_method(self, mock_wraps, method):
        assert (TransportLogger._decorate_packet_method(self.mock_transport_logger, method)
                == mock_wraps.return_value.return_value)
        mock_wraps.assert_called_once_with(method)

    @pytest.mark.parametrize("method, args, kwargs", [
        (Mock(spec=AbstractTransportInterface).send_packet, (None, "some arg"), {"a": 1, "kwarg_arg": Mock()}),
        (Mock(spec=AbstractTransportInterface).receive_packet, (), {"param_1": "value_1", "param_2": "value_2"}),
    ])
    def test_decorate_packet_method__sync_decorated_method(self, method, args, kwargs):
        decorated_method = TransportLogger._decorate_packet_method(self.mock_transport_logger, method)
        assert decorated_method(*args, **kwargs) == method.return_value
        method.assert_called_once_with(*args, **kwargs)
        self.mock_transport_logger.log_packet.assert_called_once_with(method.return_value)

    @pytest.mark.parametrize("method, args, kwargs", [
        (AsyncMock(spec=AbstractTransportInterface).async_send_packet, (None, "some arg"), {"a": 1, "kwarg_arg": Mock()}),
        (AsyncMock(spec=AbstractTransportInterface).async_receive_packet, (), {"param_1": "value_1", "param_2": "value_2"}),
    ])
    @pytest.mark.asyncio
    async def test_decorate_packet_method__async_decorated_method(self, method, args, kwargs):
        decorated_method = TransportLogger._decorate_packet_method(self.mock_transport_logger, method)
        assert await decorated_method(*args, **kwargs) == method.return_value
        method.assert_called_once_with(*args, **kwargs)
        self.mock_transport_logger.log_packet.assert_called_once_with(method.return_value)

    # log_message

    @pytest.mark.parametrize("level, record", [
        (0, Mock(spec=UdsMessageRecord)),
        (INFO, Mock(spec=UdsMessageRecord)),
    ])
    def test_log_message__log(self, level, record):
        self.mock_transport_logger.message_logging_level = level
        assert TransportLogger.log_message(self.mock_transport_logger, record) is None
        self.mock_transport_logger.logger.log.assert_called_once_with(
            level=level,
            msg=self.mock_transport_logger.message_log_format.format.return_value)
        self.mock_transport_logger.message_log_format.format.assert_called_once_with(record=record)

    def test_log_message__no_log(self):
        self.mock_transport_logger.message_logging_level = None
        assert TransportLogger.log_message(self.mock_transport_logger, Mock(spec=UdsMessageRecord)) is None
        self.mock_transport_logger.logger.log.assert_not_called()
        self.mock_transport_logger.message_log_format.format.assert_not_called()

    # log_packet
    
    @pytest.mark.parametrize("level, record", [
        (0, Mock(spec=AbstractPacketRecord)),
        (INFO, Mock(spec=AbstractPacketRecord)),
    ])
    def test_log_packet__log(self, level, record):
        self.mock_transport_logger.packet_logging_level = level
        assert TransportLogger.log_packet(self.mock_transport_logger, record) is None
        self.mock_transport_logger.logger.log.assert_called_once_with(
            level=level,
            msg=self.mock_transport_logger.packet_log_format.format.return_value)
        self.mock_transport_logger.packet_log_format.format.assert_called_once_with(record=record)

    def test_log_packet__no_log(self):
        self.mock_transport_logger.packet_logging_level = None
        assert TransportLogger.log_packet(self.mock_transport_logger, Mock(spec=AbstractPacketRecord)) is None
        self.mock_transport_logger.logger.log.assert_not_called()
        self.mock_transport_logger.message_log_format.format.assert_not_called()

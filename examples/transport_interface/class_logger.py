"""Configure logger for class of Transport Interface."""

import logging

from uds.transport_interface import AbstractTransportInterface, TransportLogger


# configure your logging
# https://docs.python.org/3/library/logging.html
logger = logging.getLogger("UDS")  # example logger name
logger.setLevel(logging.DEBUG)  # example logging level
# optionally configure logging to file
file_handler = logging.FileHandler(filename="uds.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
# optionally configure logging to python console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# configure your logger
# https://uds.readthedocs.io/en/stable/pages/user_guide/logging.html#configuration
transport_logger = TransportLogger(logger_name="UDS",  # the same name as previously configured logger
                                   message_logging_level=logging.INFO,
                                   packet_logging_level=logging.DEBUG,
                                   log_sending=True,
                                   log_receiving=True)

# activate your logger
# https://uds.readthedocs.io/en/stable/pages/user_guide/logging.html#decorating-transport-interface-class
@transport_logger
class CustomTransportInterface(AbstractTransportInterface):
    ...  # TODO: implement your interface class

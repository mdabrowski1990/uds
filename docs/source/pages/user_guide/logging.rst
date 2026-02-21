Communication Logging
=====================
UDS communication logging utilities are provided in :mod:`uds.transport_interface.logger` module.


TransportLogger
---------------
:class:`~uds.transport_interface.logger.TransportLogger` is the recommended implementation
of the communication logging feature.
The logger works by wrapping transport interface methods responsible for sending and receiving
:ref:`UDS Messages <knowledge-base-diagnostic-message>` and :ref:`Packets <knowledge-base-packet>`.

This logger integrates with the built-in
`logging <https://docs.python.org/3/library/logging.html>`_ module.

Thanks to the modular package design, custom logging implementations can easily be inserted
between existing communication layers.

.. seealso:: `Python logging documentation <https://docs.python.org/3/library/logging.html>`_

Attributes:

- :attr:`~uds.transport_interface.logger.TransportLogger.logger`
- :attr:`~uds.transport_interface.logger.TransportLogger.message_logging_level`
- :attr:`~uds.transport_interface.logger.TransportLogger.packet_logging_level`
- :attr:`~uds.transport_interface.logger.TransportLogger.log_sending`
- :attr:`~uds.transport_interface.logger.TransportLogger.log_receiving`
- :attr:`~uds.transport_interface.logger.TransportLogger.message_log_format`
- :attr:`~uds.transport_interface.logger.TransportLogger.packet_log_format`


Configuration
`````````````

Upon :class:`~uds.transport_interface.logger.TransportLogger` object creation, the user can configure how the logger
behaves during the communication.

**Example code:**

.. code-block::  python

  import logging
  from uds.transport_interface import TransportLogger

  # create example Transport Logger
  transport_logger = TransportLogger(
      logger_name="UDS",
      message_logging_level=logging.INFO,
      packet_logging_level=logging.DEBUG,
      log_sending=True,
      log_receiving=True,
      message_log_format="{record.direction.name} {record.addressing_type.name} {record.payload}",
      packet_log_format="{record.direction.name} {record}")

  transport_logger.log_sending = False  # do not log outgoing communication
  transport_logger.packet_logging_level = None  # do not log packets


Activation
``````````
There are two ways to activate the logger:

- `Decorating Transport Interface class`_
- `Decorating Transport Interface instance`_


Decorating Transport Interface class
''''''''''''''''''''''''''''''''''''
Transport Logger activation is possible by decorating Transport Interface class.
This is the recommended (and most Pythonic) approach when implementing custom transport interfaces.

**Example code:**

.. code-block::  python

  from uds.transport_interface import AbstractTransportInterface, TransportLogger

  # let's assume that we have `transport_logger` already configured
  transport_logger: TransportLogger

  @transport_logger
  class MyTransportInterface(AbstractTransportInterface):
      ...  # TODO: custom implementation


It is also possible to decorate existing Transport Interfaces.

**Example code:**

.. code-block::  python

  from uds.transport_interface import TransportLogger
  from uds.can import PyCanTransportInterface

  # let's assume that we have `transport_logger` already configured
  transport_logger: TransportLogger

  PyCanTransportInterfaceWithLogging = transport_logger(PyCanTransportInterface)


Decorating Transport Interface instance
'''''''''''''''''''''''''''''''''''''''
Another option is to decorate an already existing transport interface instance.

**Example code:**

.. code-block::  python

  from uds.transport_interface import AbstractTransportInterface, TransportLogger

  # let's assume that we have `transport_interface` already configured
  transport_interface: AbstractTransportInterface

  # let's assume that we have `transport_logger` already configured
  transport_logger: TransportLogger

  # add logging to the transport_interface
  transport_interface_with_logger = transport_logger(transport_interface)


Customization
`````````````
The easiest way to create your own transport logger is to inherit after
:class:`~uds.transport_interface.logger.TransportLogger` class and add your own features.
This is also the easiest way to define more advanced or custom logging messages.

**Example code:**

.. code-block::  python

  from uds.transport_interface import TransportLogger
  from uds.addressing import TransmissionDirection
  from uds.message import UdsMessageRecord
  from uds.utilities import bytes_to_hex

  class MyTransportLogger(TransportLogger):

      def log_message(self, record: UdsMessageRecord) -> None:
          """Log a message after receiving/transmitting UDS Message."""
          if self.message_logging_level is not None:
              if record.direction == TransmissionDirection.TRANSMITTED:
                  message = f"Transmitted message with payload: {bytes_to_hex(record.payload)}"
              else:
                  message = f"Received message with payload: {bytes_to_hex(record.payload)}"
              self.logger.log(level=self.message_logging_level,
                              msg=message)

CAN Transport Interfaces
========================
The implementation for Transport Interfaces that can be used with CAN bus is located in
:mod:`uds.transport_interface.can_transport_interface` module.


Common
------
Common implementation for all all CAN Transport Interfaces is included in
:class:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface`.

.. warning:: A **user shall not use**
    :class:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface` **directly**,
    but one is able (and encouraged) to use
    :class:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface`
    implementation on any of its children classes.


Configuration
`````````````
CAN bus specific configuration is set upon calling
:meth:`uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.__init__` method.
The following configuration parameters are set then:

- Addressing Information of this CAN node - attribute
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.addressing_information`
- driver for a CAN bus interface - attribute
  :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.bus_manager`
- timing parameters (:ref:`N_Br <knowledge-base-can-n-br>`, :ref:`N_Cs <knowledge-base-can-n-cs>`) - attributes
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_br` and
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_cs`
- communication timeout parameters (:ref:`N_As <knowledge-base-can-n-as>`, :ref:`N_Ar <knowledge-base-can-n-ar>`,
  :ref:`N_Bs <knowledge-base-can-n-bs>`, :ref:`N_Cr <knowledge-base-can-n-cr>`) - attributes
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_as_timeout`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_ar_timeout`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_bs_timeout` and
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_cr_timeout`
- UDS message segmentation parameters (:ref:`base DLC of a CAN frame <knowledge-base-can-data-field>`,
  flag whether to use :ref:`data optimization for CAN frame <knowledge-base-can-data-optimization>`,
  and the value to use for :ref:`CAN frame data padding <knowledge-base-can-frame-data-padding>`) - attributes
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.dlc`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.use_data_optimization`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.filler_byte`,
- Flow Control generator - attribute
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.flow_control_parameters_generator`

Most of these attributes (all except
:attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.addressing_information`)
can be changed after object is created.


Python-CAN
----------
Class :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` contains
the implementation of CAN Transport Interface that uses `python-can <https://python-can.readthedocs.io>`_ package for
receiving and transmitting CAN frames.

.. note:: Right now only half-duplex communication is implemented.

    The matter is further explained in
    :ref:`handling unexpected CAN packets arrivals <knowledge-base-can-unexpected-packet-arrival>` chapter.


Configuration
`````````````
Configuration is set upon calling
:meth:`uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.__init__` method and from
the user perspective it does not provide any additional features to common_ implementation provided by
:meth:`uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.__init__`.

**Example code:**

.. code-block::  python

    import uds
    from can import Bus

    # define example python-can bus interface (https://python-can.readthedocs.io/en/stable/bus.html#bus-api)
    python_can_interface = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)

    # define Addressing Information for a CAN Node
    can_node_addressing_information = uds.can.CanAddressingInformation(
        addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})

    # configure CAN Transport Interface for this CAN Node
    can_transport_interface = uds.transport_interface.PyCanTransportInterface(
        can_bus_manager=python_can_interface,
        addressing_information=can_node_addressing_information,
        n_as_timeout=50,
        n_ar_timeout=900,
        n_bs_timeout=50,
        n_br=10,
        n_cs=0,
        n_cr_timeout = 900,
        dlc=0xF,
        use_data_optimization=True,
        filler_byte=0x55,
        flow_control_parameters_generator=uds.can.DefaultFlowControlParametersGenerator(st_min=0,
                                                                                        block_size=5,
                                                                                        wait_count=0,
                                                                                        repeat_wait=False))

    # change CAN Transport Interface configuration
    can_transport_interface.n_as_timeout = uds.transport_interface.PyCanTransportInterface.N_AS_TIMEOUT
    can_transport_interface.n_ar_timeout = uds.transport_interface.PyCanTransportInterface.N_AR_TIMEOUT
    can_transport_interface.n_bs_timeout = uds.transport_interface.PyCanTransportInterface.N_BS_TIMEOUT
    can_transport_interface.n_br = uds.transport_interface.PyCanTransportInterface.DEFAULT_N_BR
    can_transport_interface.n_cs = uds.transport_interface.PyCanTransportInterface.DEFAULT_N_CS
    can_transport_interface.n_cr_timeout = uds.transport_interface.PyCanTransportInterface.N_CR_TIMEOUT
    can_transport_interface.dlc = 8
    can_transport_interface.use_data_optimization = False
    can_transport_interface.filler_byte = 0xAA
    can_transport_interface.flow_control_parameters_generator = uds.can.DefaultFlowControlParametersGenerator(
        st_min=100,
        block_size=15,
        wait_count=1,
        repeat_wait=True)


Synchronous communication
`````````````````````````
.. warning:: Synchronous and asynchronous implementation shall not be mixed, therefore for transmitting and receiving
    UDS Messages and CAN Packets use either:

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_packet`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_packet`

    or

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_packet`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

.. seealso:: :ref:`Examples for python-can Transport Interface <examples-python-can>`

Send Message
''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # send UDS Message and receive UDS message record with historic information about the transmission
    message_record = can_transport_interface.send_message(message)


Receive Message
'''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive an UDS message with timeout set to 1000 ms
    message_record = can_transport_interface.receive_message(timeout=1000)



Send Packet
'''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_packet`
method to send CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # segment the message to create a CAN packet
    can_packet = can_transport_interface.segmenter.segmentation(message)[0]

    # send CAN packet and receive CAN packet record with historic information about the transmission and the transmitted CAN packet
    can_packet_record = can_transport_interface.send_packet(can_packet)

Receive Packet
''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_packet`
method to receive CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive a CAN packet with timeout set to 1000 ms
    can_packet_record = can_transport_interface.receive_packet(timeout=1000)


Asynchronous communication
``````````````````````````
.. warning:: Synchronous and asynchronous implementation shall not be mixed, therefore for transmitting and receiving
    UDS Messages and CAN Packets use either:

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_packet`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_packet`

    or

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_packet`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

.. seealso:: :ref:`Examples for python-can Transport Interface <examples-python-can>`

.. note:: In all examples, only a coroutine code was presented. If you need a manual how to run an asynchronous code,
    visit https://docs.python.org/3/library/asyncio-runner.html#running-an-asyncio-program.

Send Message
''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # send UDS Message and receive UDS message record with historic information about the transmission
    message_record = await can_transport_interface.async_send_message(message)

Receive Message
'''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive an UDS message with timeout set to 1000 ms
    message_record = await can_transport_interface.async_receive_message(timeout=1000)

Send Packet
'''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_packet`
method to send CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # segment the message to create a CAN packet
    can_packet = can_transport_interface.segmenter.segmentation(message)[0]

    # send CAN packet and receive CAN packet record with historic information about the transmission and the transmitted CAN packet
    can_packet_record = await can_transport_interface.async_send_packet(can_packet)

Receive Packet
''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_packet`
method to receive CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive a CAN packet with timeout set to 1000 ms
    can_packet_record = await can_transport_interface.async_receive_packet(timeout=1000)


UDS over CAN
============
This part of documentation explain how to use this package to communicate using
:ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol.
The implementation is located in :mod:`uds.can` module.

.. note:: You might :ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol separately from UDS.


Addressing
----------




Frame
-----


Packet
------


Segmentation
------------



Transport Interface
-------------------









TODO




CAN Transport Interface
-----------------------
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
        addressing_format=uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
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
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`

    or

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

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
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
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
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`
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
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`

    or

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

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
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
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
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`
method to receive CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive a CAN packet with timeout set to 1000 ms
    can_packet_record = await can_transport_interface.async_receive_packet(timeout=1000)


















CanSegmenter
------------
:class:`~uds.segmentation.can_segmenter.CanSegmenter` handles segmentation process specific for CAN bus.

Following functionalities are provided by :class:`~uds.segmentation.can_segmenter.CanSegmenter`:

- Configuration of the segmenter:

  As a user, you are able to configure :class:`~uds.segmentation.can_segmenter.CanSegmenter` parameters which determines
  the addressing (Addressing Format and Addressing Information of input and output CAN packets) and the content
  (e.g. Filler Byte value and whether to use CAN Frame Data Optimization) of CAN packets.

  **Example code:**

    .. code-block::  python

        import uds

        # define Addressing Information for a CAN Node
        can_node_addressing_information = uds.can.CanAddressingInformation(
            addressing_format=uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
            tx_physical={"can_id": 0x611},
            rx_physical={"can_id": 0x612},
            tx_functional={"can_id": 0x6FF},
            rx_functional={"can_id": 0x6FE})

        # configure CAN Segmenter for this CAN Node
        can_segmenter = uds.segmentation.CanSegmenter(addressing_information=can_node_addressing_information,
                                                      dlc=8,
                                                      use_data_optimization=False,
                                                      filler_byte=0xFF)

        # change CAN Segmenter configuration
        can_segmenter.addressing_information = uds.can.CanAddressingInformation(
            uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
            tx_physical={"can_id": 0x612},
            rx_physical={"can_id": 0x611},
            tx_functional={"can_id": 0x6FE},
            rx_functional={"can_id": 0x6FF})
        can_segmenter.dlc=0xF
        can_segmenter.use_data_optimization = True
        can_segmenter.filler_byte = 0xAA


- Diagnostic message segmentation:

  As a user, you are able to :ref:`segment diagnostic messages <knowledge-base-message-segmentation>`
  (objects of :class:`~uds.message.uds_message.UdsMessage` class) into CAN packets
  (objects for :class:`~uds.can.packet.can_packet.CanPacket` class).

  **Example code:**

    .. code-block::  python

        # let's assume that we have `can_segmenter` already configured as presented in configuration example above

        # define diagnostic message to segment
        uds_message_1 = uds.message.UdsMessage(payload=[0x3E, 0x00],
                                               addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL)
        uds_message_2 = uds.message.UdsMessage(payload=[0x62, 0x10, 0x00] + [0x20]*100,
                                               addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL)

        # use preconfigured segmenter to segment the diagnostic messages
        can_packets_1 = can_segmenter.segmentation(uds_message_1)  # output: Single Frame
        can_packets_2 = can_segmenter.segmentation(uds_message_2)  # output: First Frame with Consecutive Frame(s)

  .. note:: It is impossible to segment functionally addressed diagnostic message into First Frame and Consecutive Frame(s)
      as such result is considered incorrect according to :ref:`UDS ISO Standards <knowledge-base-uds-standards>`.


- CAN packets desegmentation:

  As a user, you are able to :ref:`desegment CAN packets <knowledge-base-packets-desegmentation>`
  (either objects of :class:`~uds.can.packet.can_packet.CanPacket` or
  :class:`~uds.can.packet.can_packet_record.CanPacketRecord` class)
  into diagnostic messages (either objects of :class:`~uds.message.uds_message.UdsMessage` or
  :class:`~uds.message.uds_message.UdsMessageRecord` class).

  **Example code:**

    .. code-block::  python

        # let's assume that we have `can_segmenter` already configured as presented in configuration example above

        # define CAN packets to desegment
        can_packets_1 = [
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.SINGLE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL,
                                 can_id=0x6A5,
                                 target_address=0x0C,
                                 payload=[0x3E, 0x80])
        ]
        can_packets_2 = [
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.FIRST_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 dlc=8,
                                 data_length=15,
                                 payload=[0x62, 0x10, 0x00] + 3*[0x20]),
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.CONSECUTIVE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 dlc=8,
                                 sequence_number=1,
                                 payload=7*[0x20]),
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.CONSECUTIVE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 sequence_number=1,
                                 payload=2 * [0x20],
                                 filler_byte=0x99)
        ]

        # use preconfigured segmenter to desegment the CAN packets
        uds_message_1 = can_segmenter.desegmentation(can_packets_1)
        uds_message_2 = can_segmenter.desegmentation(can_packets_2)

    .. warning:: Desegmentation performs only sanity check of CAN packets content, therefore some inconsistencies
        with Diagnostic on CAN standard might be silently accepted as long as a message can be unambiguously decoded
        out of provided CAN packets.

    .. note:: Desegmentation can be performed for any CAN packets (not only those targeting this CAN Node) in any format.

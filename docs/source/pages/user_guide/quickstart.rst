Quickstart
==========
This section introduces the essential steps to start working with the package.

- `Installation`_
- `Define Addressing Information`_
- `Create Transport Interface`_
- `Working with Transport Interface`_
- `Working with Client`_

.. seealso:: :ref:`Code Examples <examples>`


Installation
------------
.. role:: shell(code)
  :language: shell

:shell:`pip install -U py-uds`

.. seealso:: :ref:`Installation Guide <installation>`


Define Addressing Information
-----------------------------
This step depends on the network type used.

Example for CAN:

  .. code-block::  python

    import uds

    # configure Addressing Information
    can_ai = uds.can.addressing.NormalCanAddressingInformation(
        rx_physical_params={"can_id": 0x7E8},
        tx_physical_params={"can_id": 0x7E0},
        rx_functional_params={"can_id": 0x7E8},
        tx_functional_params={"can_id": 0x7DF})

.. seealso:: :ref:`CAN Addressing Information definition <implementation-can-addressing-information>` and
  :ref:`Abstract Addressing Information implementation <implementation-abstract-addressing-information>`


Create Transport Interface
--------------------------
This step depends on the network type and network manager used.

Example for CAN and `python-can <https://python-can.readthedocs.io>`_:

  .. code-block::  python

    from can import Bus
    import uds

    # let's assume Addressing Information object is created
    can_ai: uds.can.addressing.NormalCanAddressingInformation

    # configure Bus object (python-can) for CAN communication
    can_bus = Bus(
        interface="kvaser",
        channel=0,
        receive_own_messages=True,
        bitrate=500_000,
        fd=True,
        data_bitrate=4_000_000)

    # create Transport Interface object
    transport_interface = uds.can.PyCanTransportInterface(
        network_manager=can_bus,
        addressing_information=can_ai)

.. seealso:: :ref:`python-can Transport Interface <implementation-can-python-can-transport-interface>` and
  :ref:`Abstract Transport Interface implementation <implementation-abstract-transport-interface>`


Working with Transport Interface
--------------------------------
*This step is optional.*

It is recommended when you want to **work on the packet or message level**
(layers 3 and 4 of :ref:`OSI model <knowledge-base-osi-model>`).


Send and Receive Packets
````````````````````````
This step depends on the network type used.

Example for CAN:

  .. code-block::  python

    import uds

    # let's assume Transport Interface and Addressing Information objects are created
    can_ai: uds.can.addressing.NormalCanAddressingInformation
    transport_interface: uds.can.PyCanTransportInterface

    # define example packet to send (depends on network type - example for CAN bus)
    sf = uds.can.CanPacket(packet_type=uds.can.CanPacketType.SINGLE_FRAME,
                           payload=[0x3E, 0x00],
                           **can_ai.tx_functional_params)

    # send a packet
    sent_packet_record = transport_interface.send_packet(sf)

    # receive a packet
    received_packet_record = transport_interface.receive_packet(timeout=None)  # no timeout


.. seealso:: :ref:`Packet implementation <implementation-packet>` and
  :ref:`CAN Packet implementation <implementation-can-packet>`


Send and Receive Messages
`````````````````````````
Use the Transport Interface to exchange complete diagnostic messages.

Example:

  .. code-block::  python

    # let's assume Transport Interface object is created
    transport_interface: uds.transport_interface.AbstractTransportInterface

    # define example message to send
    uds_message = uds.message.UdsMessage(payload=[0x10, 0x03],
                                         addressing_type=uds.addressing.AddressingType.PHYSICAL)

    # send a message
    sent_message_record = transport_interface.send_message(uds_message)

    # receive a message
    received_message_record = transport_interface.receive_message(timeout=1000)  # timeout in [ms]


.. seealso:: :ref:`Diagnostic Message implementation <implementation-diagnostic-message>`


Working with Client
-------------------
*This step is optional.*

If you decided to use Client implementation.


Configuration
`````````````
:ref:`Client <knowledge-base-client>` configuration.

Example:

  .. code-block::  python

    import uds

    # let's assume Transport Interface object is created
    transport_interface: uds.transport_interface.AbstractTransportInterface

    # define a client
    client = uds.client.Client(transport_interface=transport_interface)


.. seealso:: :ref:`Client implementation <implementation-client>`


Send Request and Receive Responses
``````````````````````````````````
Send a request message as a client and collect all responses, including any negative responses with
:ref:`NRC <knowledge-base-nrc>` Response Pending (0x78) and the final response.

Example:

  .. code-block::  python

    import uds

    # let's assume Client object is created
    client: uds.client.Client

    # define an example request message
    request = uds.message.UdsMessage(payload=[0x14, 0xFF, 0xFF, 0xFF],
                                     addressing_type=uds.addressing.AddressingType.PHYSICAL)

    # send request and receive all responses
    request_record, responses_records = client.send_request_receive_responses(request)

.. seealso:: :ref:`Diagnostic Message implementation <implementation-diagnostic-message>`


Periodic Tester Present
```````````````````````
Periodically send :ref:`TesterPresent <knowledge-base-service-tester-present>` messages to maintain
the diagnostic session.

Example:

  .. code-block::  python

    import uds

    # let's assume Client object is created
    client: uds.client.Client

    # start sending TesterPresent messages periodically
    client.start_tester_present()

    # stop sending TesterPresent messages periodically
    client.stop_tester_present()


Collecting Response Messages
````````````````````````````
Use a background task to collect all response messages sent to the client when no request message was sent.
Useful for :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>`,
:ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>`,
or collecting responses for periodic :ref:`TesterPresent <knowledge-base-service-tester-present>` messages.

Example:

  .. code-block::  python

    import uds

    # let's assume Client object is created
    client: uds.client.Client

    # start collecting all response messages sent to client
    client.start_receiving()

    # wait for a response message
    response_message_record = client.get_response()

    # get a response message immediately
    response_message_record = client.get_response_no_wait()

    # stop collecting response messages
    client.stop_receiving()

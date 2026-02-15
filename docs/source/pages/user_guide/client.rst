.. _implementation-client:

Client
======
This section describes the :ref:`Client <knowledge-base-client>` implementation,
provided in the :mod:`uds.client` module.
The main entry point is the :class:`~uds.client.Client` class.

Attributes:

- :attr:`~uds.client.Client.DEFAULT_P2_CLIENT_TIMEOUT` - default :ref:`P2Client <knowledge-base-p2-client>` timeout
- :attr:`~uds.client.Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT` - default :ref:`P2*Client <knowledge-base-p2*-client>`
  timeout
- :attr:`~uds.client.Client.DEFAULT_P3_CLIENT` - default :ref:`P3Client <knowledge-base-p3-client>` value
- :attr:`~uds.client.Client.DEFAULT_P6_CLIENT_TIMEOUT` - default :ref:`P6Client <knowledge-base-p6-client>` timeout
- :attr:`~uds.client.Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT` - default :ref:`P6*Client <knowledge-base-p6*-client>`
  timeout
- :attr:`~uds.client.Client.DEFAULT_S3_CLIENT` - default :ref:`S3Client <knowledge-base-s3-client>` value
- :attr:`~uds.client.Client.DEFAULT_RECEIVING_TASK_CYCLE` - default cycle used by `Background Receiving`_
- :attr:`~uds.client.Client.tester_present_storage_size` - number of Tester Present request records stored
- :attr:`~uds.client.Client.transport_interface` - transport interface in use
- :attr:`~uds.client.Client.p2_client_timeout` - configured :ref:`P2Client <knowledge-base-p2-client>` timeout
- :attr:`~uds.client.Client.p2_client_measured` - last measured :ref:`P2Client <knowledge-base-p2-client>` value
- :attr:`~uds.client.Client.p2_ext_client_timeout` - configured :ref:`P2*Client <knowledge-base-p2*-client>` timeout
- :attr:`~uds.client.Client.p2_ext_client_measured` - last measured :ref:`P2*Client <knowledge-base-p2*-client>` value
- :attr:`~uds.client.Client.p3_client_physical` - configured :ref:`P2Client_Phys <knowledge-base-p3-client-phys>` value
- :attr:`~uds.client.Client.p3_client_functional` - configured :ref:`P2Client_Func <knowledge-base-p3-client-func>` value
- :attr:`~uds.client.Client.p6_client_timeout` - configured :ref:`P6Client <knowledge-base-p6-client>` timeout
- :attr:`~uds.client.Client.p6_client_measured` - last measured :ref:`P6Client <knowledge-base-p6-client>` value
- :attr:`~uds.client.Client.p6_ext_client_timeout` - configured :ref:`P6*Client <knowledge-base-p6*-client>` timeout
- :attr:`~uds.client.Client.p6_ext_client_measured` - last measured :ref:`P6*Client <knowledge-base-p6*-client>` value
- :attr:`~uds.client.Client.s3_client` - configured :ref:`S3Client <knowledge-base-s3-client>` value
- :attr:`~uds.client.Client.last_sent_tester_present_requests` - the last sent few (number equal to
  :attr:`~uds.client.Client.tester_present_storage_size`) Tester Present request records
- :attr:`~uds.client.Client.last_sent_request` - the last transmitted request message
- :attr:`~uds.client.Client.last_received_response` - the final response to :attr:`~uds.client.Client.last_sent_request`
- :attr:`~uds.client.Client.is_background_receiving` - whether `Background Receiving`_ is on
- :attr:`~uds.client.Client.is_tester_present_sent` - whether `Tester Present`_ is sent periodically
- :attr:`~uds.client.Client.is_ready_for_physical_transmission` - whether Client is ready for transmitting
  physically addressed request message
- :attr:`~uds.client.Client.is_ready_for_functional_transmission` - whether Client is ready for transmitting
  functionally addressed request message

Methods:

- :meth:`~uds.client.Client.__init__` - create and configure the :ref:`Client <knowledge-base-client>`
- :meth:`~uds.client.Client.__del__` - clean up and stop background tasks safely
- :meth:`~uds.client.Client.is_response_pending_message` - check if a message is a negative response
  with Response Pending (0x78) :ref:`NRC <knowledge-base-nrc>`
- :meth:`~uds.client.Client.is_response_to_request` - check if a message is a response to provided request message
- :meth:`~uds.client.Client.wait_till_ready_for_physical_transmission` - wait till Client is ready for
  transmitting physically addressed request
- :meth:`~uds.client.Client.wait_till_ready_for_functional_transmission` - wait till Client is ready for
  transmitting functionally addressed request
- :meth:`~uds.client.Client.wait_till_ready_for_transmission` - wait till Client is ready for
  transmitting given request message
- :meth:`~uds.client.Client.get_response` - wait for the next response collected by `Background Receiving`_
- :meth:`~uds.client.Client.get_response_no_wait` - get the next response collected by `Background Receiving`_
  without waiting
- :meth:`~uds.client.Client.clear_response_queue` - clear messages collected so far by `Background Receiving`_
- :meth:`~uds.client.Client.start_tester_present` - start sending Tester Present messages periodically
- :meth:`~uds.client.Client.stop_tester_present` - stop sending Tester Present messages periodically
- :meth:`~uds.client.Client.start_background_receiving` - turn `Background Receiving`_ on and start collecting response
- :meth:`~uds.client.Client.stop_background_receiving` - turn `Background Receiving`_ off and stop collecting response
- :meth:`~uds.client.Client.send_request_receive_responses` - send request message and collect all responses till
  the final one


Configuration
-------------
The :ref:`Client <knowledge-base-client>` is configured during :class:`~uds.client.Client` object creation.
The following arguments can be provided:

- :ref:`transport_interface <implementation-abstract-transport-interface>`
- :ref:`P2Client <knowledge-base-p2-client>` timeout value
- :ref:`P2*Client <knowledge-base-p2*-client>` timeout value
- :ref:`P3Client_Phys <knowledge-base-p3-client-phys>` value
- :ref:`P3Client_Func <knowledge-base-p3-client-func>` value
- :ref:`P6Client <knowledge-base-p6-client>` timeout value
- :ref:`P6*Client <knowledge-base-p6*-client>` timeout value
- :ref:`S3Client <knowledge-base-s3-client>` value

**Example code:**

  .. code-block::  python

    import uds

    # assume Transport Interface object exists
    transport_interface: uds.transport_interface.AbstractTransportInterface

    # configure Client object
    client = uds.client.Client(transport_interface=transport_interface,  # Transport Interface used
                               p2_client_timeout=50,  # custom value of P2Client timeout
                               p2_ext_client_timeout=5000,  # custom value of P2*Client timeout
                               p3_client_physical=250,  # custom value of P3Client_Phys
                               p3_client_functional=500,  # custom value of P3Client_Func
                               p6_client_timeout=1000,  # custom value of P6Client timeout
                               p6_ext_client_timeout=10000,  # custom value of P6*Client timeout
                               s3_client=1000)  # custom value of S3Client


Sending Requests and Receiving Responses
----------------------------------------
:meth:`~uds.client.Client.send_request_receive_responses` can be used to send a request message and collect
all responses, including Negative Responses with :ref:`NRC <knowledge-base-nrc>` Response Pending (0x78) and
the final response.

**Example code:**

  .. code-block::  python

    import uds

    # assume Client object exists
    client: uds.client.Client

    # define an example request message
    request = uds.message.UdsMessage(payload=[0x14, 0xFF, 0xFF, 0xFF],
                                     addressing_type=uds.addressing.AddressingType.PHYSICAL)

    # send request and receive all responses
    request_record, responses_records = client.send_request_receive_responses(request)


Tester Present
--------------
Manage periodic :ref:`TesterPresent <knowledge-base-service-tester-present>` messages with:

- :meth:`~uds.client.Client.start_tester_present` - start sending Tester Present messages periodically
- :meth:`~uds.client.Client.stop_tester_present` - stop sending Tester Present messages periodically

Period used for transmission is controlled by :attr:`~uds.client.Client.s3_client`.

:attr:`~uds.client.Client.is_tester_present_sent` indicates whether Tester Present cyclic sending is currently active.

:attr:`~uds.client.Client.last_sent_tester_present_requests` contains Tester Present request messages records that were
sent by periodic Tester Present task.

**Example code:**

  .. code-block::  python

    # assume Client object exists
    client: uds.client.Client

    # set period for Tester Present messages
    client.s3_client = 1000  # ms

    # start sending Tester Present Messages periodically
    client.start_tester_present(addressing_type=uds.addressing.AddressingType.PHYSICAL,  # Addressing Type to use
                                sprmib=False)  # whether to set Suppress Positive Response Message Indication Bit

    # stop sending Tester Present Messages periodically
    client.stop_tester_present()


Background Receiving
--------------------
Use this feature to receive response messages sent to :ref:`Client <knowledge-base-client>` such as asynchronous
responses not directly tied to a single request (e.g. :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>`,
:ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>`).

Methods:

- :meth:`~uds.client.Client.start_background_receiving` - start collecting responses
- :meth:`~uds.client.Client.stop_background_receiving` - stop collecting responses
- :meth:`~uds.client.Client.get_response` - get the next response (waits if none are available)
- :meth:`~uds.client.Client.get_response_no_wait` - get the next response immediately (returns None if none
  are available)
- :meth:`~uds.client.Client.clear_response_queue` - clear queue with response messages

:attr:`~uds.client.Client.is_background_receiving` indicates whether responses are currently being collected.

**Example code:**

  .. code-block::  python

    # assume Client object exists
    client: uds.client.Client
    # assume some request message object exists
    some_request: uds.message.UdsMessage

    # clear messages queue before receiving any messages
    client.clear_response_queue()

    # start collecting responses
    client.start_background_receiving()

    # you might send requests while collecting responses is active
    client.send_request_receive_responses(some_request)

    # get the next collected response with a timeout
    client.get_response(timeout=1000)  # ms

    # get next response immediately
    client.get_response_no_wait()

    # stop collecting responses
    client.stop_background_receiving()

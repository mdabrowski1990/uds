.. _implementation-client:

Client
======
This section explains :ref:`Client <knowledge-base-client>` implementation.
The implementation is provided in :mod:`uds.client` module with :class:`~uds.client.Client` class as
the main entry point.

Attributes:

- :attr:`~uds.client.Client.DEFAULT_P2_CLIENT_TIMEOUT` - default value of :ref:`P2Client <knowledge-base-p2-client>`
  timeout
- :attr:`~uds.client.Client.DEFAULT_P6_CLIENT_TIMEOUT` - default value of :ref:`P6Client <knowledge-base-p6-client>`
  timeout
- :attr:`~uds.client.Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT` - default value of
  :ref:`P2*Client <knowledge-base-p2*-client>` timeout
- :attr:`~uds.client.Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT` - default value of
  :ref:`P6*Client <knowledge-base-p6*-client>` timeout
- :attr:`~uds.client.Client.DEFAULT_S3_CLIENT` - default :ref:`S3Client <knowledge-base-s3-client>` value
- :attr:`~uds.client.Client.DEFAULT_RECEIVING_TASK_CYCLE` - default value used by `Background Receiving`_
- :attr:`~uds.client.Client.transport_interface` - Transport Interface used
- :attr:`~uds.client.Client.p2_client_timeout` - :ref:`P2Client <knowledge-base-p2-client>` timeout value
- :attr:`~uds.client.Client.p2_client_measured` - the last measured value of :ref:`P2Client <knowledge-base-p2-client>`
- :attr:`~uds.client.Client.p2_ext_client_timeout` - :ref:`P2*Client <knowledge-base-p2*-client>` timeout value
- :attr:`~uds.client.Client.p2_ext_client_measured` - the last measured value of
  :ref:`P2*Client <knowledge-base-p2*-client>`
- :attr:`~uds.client.Client.p6_client_timeout` - :ref:`P6Client <knowledge-base-p6-client>` timeout value
- :attr:`~uds.client.Client.p6_client_measured` - the last measured value of :ref:`P6Client <knowledge-base-p6-client>`
- :attr:`~uds.client.Client.p6_ext_client_timeout` - :ref:`P6*Client <knowledge-base-p6*-client>` timeout value
- :attr:`~uds.client.Client.p6_ext_client_measured` - the last measured value of
  :ref:`P6*Client <knowledge-base-p6*-client>`
- :attr:`~uds.client.Client.s3_client` - :ref:`S3Client <knowledge-base-s3-client>` value
- :attr:`~uds.client.Client.is_receiving` - whether `Background Receiving`_ is on

Methods:

- :meth:`~uds.client.Client.__init__` - configure :ref:`Client <knowledge-base-client>`
- :meth:`~uds.client.Client.__del__` - close threads safely
- :meth:`~uds.client.Client.is_response_pending_message` - check whether a message is a negative response
  with Response Pending (0x78) :ref:`NRC <knowledge-base-nrc>`
- :meth:`~uds.client.Client.get_response` - wait for the next response collected by `Background Receiving`_
- :meth:`~uds.client.Client.get_response_no_wait` - get the next response collected by `Background Receiving`_
  without waiting
- :meth:`~uds.client.Client.clear_response_queue` - clear messages collected so far by `Background Receiving`_
- :meth:`~uds.client.Client.start_receiving` - start collecting responses
- :meth:`~uds.client.Client.stop_receiving` - stop collecting responses
- :meth:`~uds.client.Client.start_tester_present` - start sending Tester Present messages periodically
- :meth:`~uds.client.Client.stop_tester_present` - stop sending Tester Present messages periodically
- :meth:`~uds.client.Client.send_request_receive_responses` - send request message and collect all responses till
  the final one


Configuration
-------------
Configuration of :ref:`Client <knowledge-base-client>` is done at :class:`~uds.client.Client` object creation.
The following arguments can be provided:

- :ref:`transport_interface <implementation-abstract-transport-interface>`
- :ref:`P2Client <knowledge-base-p2-client>` timeout value
- :ref:`P2*Client <knowledge-base-p2*-client>` timeout value
- :ref:`P6Client <knowledge-base-p6-client>` timeout value
- :ref:`P6*Client <knowledge-base-p6*-client>` timeout value
- :ref:`S3Client <knowledge-base-s3-client>` value

**Example code:**

  .. code-block::  python

    import uds

    # let's assume Transport Interface object is already created
    transport_interface: uds.transport_interface.AbstractTransportInterface

    # configure Client object
    client = uds.client.Client(transport_interface=transport_interface,  # Transport Interface used
                               p2_client_timeout=50,  # custom value of P2Client timeout,
                               p2_ext_client_timeout=5000,  # custom value of P2*Client timeout,
                               p6_client_timeout=1000,  # custom value of P6Client timeout,
                               p6_ext_client_timeout=10000,  # custom value of P6*Client timeout,
                               s3_client=1000)  # custom value of S3Client


Sending Requests and Receiving Responses
----------------------------------------
:meth:`~uds.client.Client.send_request_receive_responses` can be used to send a request message and collect
all responses, including Negative Responses with :ref:`NRC <knowledge-base-nrc>` Response Pending (0x78) and
the final response.

**Example code:**

  .. code-block::  python

    import uds

    # let's assume Client object is already created
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

Period used for transmission is controlled by :attr:`~uds.client.Client.s3_client` value.

**Example code:**

  .. code-block::  python

    # let's assume Client object is already created
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

- :meth:`~uds.client.Client.start_receiving` - start collecting responses
- :meth:`~uds.client.Client.stop_receiving` - stop collecting responses
- :meth:`~uds.client.Client.get_response` - get response, wait if no response stored
- :meth:`~uds.client.Client.get_response_no_wait` - get response, do not wait

**Example code:**

  .. code-block::  python

    # let's assume Client object is already created
    client: uds.client.Client
    # let's assume some request message is already created
    some_request: uds.message.UdsMessage

    # start collecting responses
    client.start_receiving()

    # you might send requests while collecting responses is active
    client.send_request_receive_responses(some_request)

    # get the next collected response with a timeout
    client.get_response(timeout=1000)

    # get next response immediately
    client.get_response_no_wait()

    # stop collecting responses
    client.stop_receiving()

UDS Time Parameters
===================


Session Parameters
------------------


.. _knowledge-base-s3-client:

S3 :sub:`Client`
````````````````
On the client side, the S3\ :sub:`Client` parameter defines the time interval for sending cyclical
:ref:`Tester Present <knowledge-base-service-tester-present>` request messages.
This ensures that the server(s) the client communicates with do not exit the current diagnostic session
due to inactivity.

Default value:
  2000 ms

Minimum value:
  P2\ :sub:`Client`

Maximum value:
  S3\ :sub:`Server`


.. _knowledge-base-s3-server:

S3\ :sub:`Server`
`````````````````
On the server side, the S3\ :sub:`Server` parameter defines the inactivity time (without any request messages)
after which the server shall exit the current diagnostic session and return to Default Session.

S3\ :sub:`Server` = 5000 ms


Network Delays
--------------

△P2
```
△P2 is the sum of delays affecting P2 timing parameters in UDS. It consists of:

- △P2 :sub:`request` – maximum delay from sending a request message to receiving it at the server
- △P2 :sub:`response` – maximum delay from sending a response message to receiving it at the client

△P2 = △P2\ :sub:`request` + △P2\ :sub:`response`


△P6
```
△P6 is the sum of delays affecting P6 timing parameters in UDS. It consists of:

- △P6 :sub:`request` – maximum delay from sending a request message to receiving it at the server
  (△P6 :sub:`request` = △P2 :sub:`request`)
- △P6 :sub:`response` – maximum delay from the start of response transmission to full reception at the client

△P6 = △P6\ :sub:`request` + △P6\ :sub:`response`


Client Side Parameters
----------------------


.. _knowledge-base-p2-client:

P2\ :sub:`Client`
`````````````````
P2\ :sub:`Client` is the time on the client side from transmitting a request until the start of the first
response message (positive or negative, or *Response Pending* NRC 0x78).

Timeout value:
  P2\ :sub:`Server_max` + △P2 (or greater)

Error handling:
  If P2\ :sub:`Client` timeout is exceeded, then the reception of
  the :ref:`response message <knowledge-base-response-message>` shall be aborted.


.. _knowledge-base-p2*-client:

P2*\ :sub:`Client`
``````````````````
P2*\ :sub:`Client` is the time on the client side after receiving a *Response Pending* negative response (NRC 0x78)
until the next response is received.

Timeout value:
  P2*\ :sub:`Server_max` + △P2\ :sub:`response` (or greater)

Error handling:
  If P2*\ :sub:`Client` timeout is exceeded, then the reception of
  the :ref:`response message <knowledge-base-response-message>` shall be aborted.


.. _knowledge-base-p3-client:
.. _knowledge-base-p3-client-phys:

P3\ :sub:`Client_Phys`
``````````````````````
P3\ :sub:`Client_Phys` is the time on the client side after sending a
:ref:`physically addressed <knowledge-base-physical-addressing>` request message that does **not** require a response.
If the server does respond, this timer does not apply.

Minimum value:
  P2\ :sub:`Server_max` + △P2

  P2\ :sub:`Client`

Performance requirement:
  The client shall assume that the addressed server has received and successfully processed the request,
  if no response was received within P3\ :sub:`Client_Phys` time.
  The client might proceed with sending a following request.


.. _knowledge-base-p3-client-func:

P3\ :sub:`Client_Func`
``````````````````````
P3\ :sub:`Client_Func` is the waiting time on the client side after sending a
:ref:`functionally addressed <knowledge-base-functional-addressing>` request message that does not require a response.
If the server does respond, this timer does not apply.

Minimum value:
  P2\ :sub:`Server_max` + △P2

  P2\ :sub:`Client`

Performance requirement:
  The client shall assume that all addressed servers have received and successfully processed the request,
  if no response was received within P3\ :sub:`Client_Func` time.
  The client might proceed with sending a following request.


.. _knowledge-base-p6-client:

P6\ :sub:`Client`
`````````````````
P6\ :sub:`Client` is the time from transmitting a request until the end of the first (and final)
response message transmission.
If one or more *Response Pending* messages are sent, then P6*\ :sub:`Client` applies instead.

Timeout value:
  P2\ :sub:`Server_max` + △P6 (or greater)

Error handling:
  If P6\ :sub:`Client` timeout is exceeded, then the reception of
  the :ref:`response message <knowledge-base-response-message>` shall be aborted.


.. _knowledge-base-p6*-client:

P6*\ :sub:`Client`
``````````````````
P6*\ :sub:`Client` is the time from transmitting a request until the end of the final response message,
when one or more *Response Pending* negative responses were sent before the final answer.
If the final response is sent immediately, P6\ :sub:`Client` applies.

Timeout value:
  P2*\ :sub:`Server_max` + △P6 (or greater)

Error handling:
  If P6*\ :sub:`Client` timeout is exceeded, then the reception of
  the :ref:`response message <knowledge-base-response-message>` shall be aborted.


Server Side Parameters
----------------------


.. _knowledge-base-p2-server:

P2\ :sub:`Server`
`````````````````
P2\ :sub:`Server` is the time after which the server sends the first response (either positive or negative)
after receiving a request message.

Minimum value:
  0

Maximum value:
  specific for the server
  default: 50 ms

Performance requirement:
  The server shall send a response (assuming the request requires one) within P2\ :sub:`Server`.
  If the final response is not yet available, the server shall send a negative response with
  :ref:`NRC <knowledge-base-nrc>` Response Pending (0x78).


.. _knowledge-base-p2*-server:

P2*\ :sub:`Server`
``````````````````
P2*\ :sub:`Server` is the additional time allowed for the server to send the final response after issuing
a Response Pending (NRC 0x78).

Minimum value:
  0

Maximum value:
  specific for the server
  default: 5000 ms

Performance requirement:
  After sending a negative response with :ref:`NRC <knowledge-base-nrc>` Response Pending (0x78),
  the server shall provide the next response within P2*\ :sub:`Server`.
  If the final response is still not available, the server shall send another Response Pending (0x78).


.. _knowledge-base-p4-server:

P4\ :sub:`Server`
`````````````````
P4\ :sub:`Server` is the total time from receiving a request until sending the final response.
If the server sends Response Pending messages, P2*\ :sub:`Server` applies between intermediate responses,
but the final response must still be sent within the overall P4\ :sub:`Server` limit.

Minimum value:
  P2\ :sub:`Server`

Maximum value:
  specific for the server

Performance requirement:
  The server shall send the final response within P4\ :sub:`Server` after receiving the request.
  If the final response is still not available when this time expires, the server shall abort
  the :ref:`response message <knowledge-base-response-message>` transmission.

.. _knowledge-base-addressing:

Addressing
==========
In UDS communication, addressing determines participants (sender and one or more receivers).

We distinguish following addressing types:

- `Physical Addressing`_
- `Functional Addressing`_


.. _knowledge-base-physical-addressing:

Physical Addressing
-------------------
Physical addressing is used in communication between one client and one server.
When physically addressed messages are sent, the direct (point-to-point) communication between the client and
the server takes place. The server shall respond to a physically addressed request unless the request contains
information that a response is not required (further explained in
`response behaviour to physically addressed request`_ section).

.. note:: You do not need a direct physical connection between a client and a server to have physically addressed
  communication as all messages shall be routed to a target of each message.


Response behaviour to physically addressed request
``````````````````````````````````````````````````
Expected server behaviour in case of receiving physically addressed request message with SubFunction parameter:

+----------------------------------+----------------------------------------------------------------+-----------------------------------------------+-------------------------------------------------------------------------------------------------------------+
|        **Client request**        |                      **Server capability**                     |              **Server response**              |                                                 **Comment**                                                 |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+                                                                                                             |
| **Addressing** |    **SPRMIB**   | **SID supported** | **SF supported** | **DataParam supported** |      **Message**      |        **NRC**        |                                                                                                             |
+================+=================+===================+==================+=========================+=======================+=======================+=============================================================================================================+
|    physical    | False (bit = 0) |        YES        |        YES       |        At least 1       |   Positive Response   |          ---          |                          Server supports the requests and sends positive response.                          |
|                |                 |                   |                  +-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |        At least 1       |   Negative Response   |        NRC = XX       | Server sends negative response because an error occurred processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |           None          |                       |       NRC = ROOR      |                                Server sends negative response with NRC 0x31.                                |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                       |  NRC = SNS or SNSIAS  |                            Server sends negative response with NRC 0x11 or 0x7F.                            |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                       | NRC = SFNS or SFNSIAS |                            Server sends negative response with NRC 0x12 or 0x7E.                            |
|                +-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |  True (bit = 1) |        YES        |        YES       |        At least 1       |      No Response      |          ---          |                                       Server does not send a response.                                      |
|                |                 |                   |                  +-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |        At least 1       |   Negative Response   |        NRC = XX       |         Server sends negative response because an error occurred during request message processing.         |
|                |                 |                   |                  +-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |           None          |                       |       NRC = ROOR      |                                Server sends negative response with NRC 0x31.                                |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                       |  NRC = SNS or SNSIAS  |                            Server sends negative response with NRC 0x11 or 0x7F.                            |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                       | NRC = SFNS or SFNSIAS |                            Server sends negative response with NRC 0x12 or 0x7E.                            |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+

Expected server behaviour in case of receiving physically addressed request message without SubFunction parameter:

+--------------------+---------------------------------------------+-----------------------------------------+-------------------------------------------------------------------------------------------------------------+
| **Client request** |            **Server capability**            |           **Server response**           |                                                 **Comment**                                                 |
+--------------------+-------------------+-------------------------+-------------------+---------------------+                                                                                                             |
|   **Addressing**   | **SID supported** | **DataParam supported** |    **Message**    |       **NRC**       |                                                                                                             |
+====================+===================+=========================+===================+=====================+=============================================================================================================+
|      physical      |        YES        |           All           | Positive Response |         ---         |                          Server supports the requests and sends positive response.                          |
|                    |                   +-------------------------+                   +---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |        At least 1       |                   |         ---         |                          Server supports the requests and sends positive response.                          |
|                    |                   +-------------------------+-------------------+---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |        At least 1       | Negative Response |       NRC = XX      | Server sends negative response because an error occurred processing the data parameters of request message. |
|                    |                   +-------------------------+                   +---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |           None          |                   |      NRC = ROOR     |                                Server sends negative response with NRC 0x31.                                |
|                    +-------------------+-------------------------+                   +---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |         NO        |           ---           |                   | NRC = SNS or SNSIAS |                             Server sends negative response with NRC 0x11 or 0x7F                            |
+--------------------+-------------------+-------------------------+-------------------+---------------------+-------------------------------------------------------------------------------------------------------------+

where:

- SPRMIB - flag informing whether Suppress Positive Response Message Indication Bit is set in the received request
  message
- SID supported - flag informing whether Service Identifier in the received request message is supported by the server
- SF supported - flag informing whether SubFunction in the received request message is supported by the server
- DataParam supported - information on whether values of data parameters (e.g. DIDs, RIDs, DTCStatusMask)
  in the received request message are supported by the server
- NRC - :ref:`Negative Response Code <knowledge-base-nrc>`
- ROOR - NRC 0x31 (requestOutOfRange)
- SNS - NRC 0x11 (serviceNotSupported)
- SNSIAS - NRC 0x7F (serviceNotSupportedInActiveSession)
- SFNS - NRC 0x12 (SubFunctionNotSupported)
- SFNSIAS - NRC 0x7E (SubFunctionNotSupportedInActiveSession)
- XX - NRC code that is supported by the server and suitable to the current situation (e.g. NRC 0x21 busyRepeatRequest
  if server is currently overloaded and cannot process next request message)


.. _knowledge-base-functional-addressing:

Functional Addressing
---------------------
Functional addressing is used to send messages to multiple servers (ECUs) in the network.
When functionally addressed messages are sent, a one-to-many communication between a client and servers (ECUs)
takes place. A server shall only respond to certain functionally addressed requests (further explained in
`response behaviour to functionally addressed request`_ chapter.

.. note:: Some types of buses (e.g. LIN) might also support broadcast communication which slightly change expected
  server behaviour. When broadcast communication is used, then a server response is never expected by a client.


Response behaviour to functionally addressed request
````````````````````````````````````````````````````
Expected server behaviour in case of receiving functionally addressed request message with SubFunction parameter:

+----------------------------------+----------------------------------------------------------------+------------------------------+-------------------------------------------------------------------------------------------------------------+
|        **Client request**        |                      **Server capability**                     |      **Server response**     |                                                 **Comment**                                                 |
+----------------+-----------------+-------------------+------------------+-------------------------+-------------------+----------+                                                                                                             |
| **Addressing** |    **SPRMIB**   | **SID supported** | **SF supported** | **DataParam supported** |    **Message**    |  **NRC** |                                                                                                             |
+----------------+-----------------+-------------------+------------------+-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|   functional   | False (bit = 0) |        YES        |        YES       |        At least 1       | Positive Response |    ---   |                          Server supports the requests and sends positive response.                          |
|                |                 |                   |                  +-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |        At least 1       | Negative Response | NRC = XX | Server sends negative response because an error occurred processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |           None          |    No Response    |    ---   |                                       Server does not send a response.                                      |
|                |                 +-------------------+------------------+-------------------------+                   +----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                   |    ---   |                                       Server does not send a response.                                      |
|                |                 +-------------------+------------------+-------------------------+                   +----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                   |    ---   |                                       Server does not send a response.                                      |
|                +-----------------+-------------------+------------------+-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                |  True (bit = 1) |        YES        |        YES       |        At least 1       |    No Response    |    ---   |                                       Server does not send a response.                                      |
|                |                 |                   |                  +-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |        At least 1       | Negative Response | NRC = XX | Server sends negative response because an error occurred processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |           None          |    No Response    |    ---   |                                       Server does not send a response.                                      |
|                |                 +-------------------+------------------+-------------------------+                   +----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                   |    ---   |                                       Server does not send a response.                                      |
|                |                 +-------------------+------------------+-------------------------+                   +----------+-------------------------------------------------------------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                   |    ---   |                                       Server does not send a response.                                      |
+----------------+-----------------+-------------------+------------------+-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+

Expected server behaviour in case of receiving functionally addressed request message without SubFunction parameter:

+--------------------+---------------------------------------------+------------------------------+-------------------------------------------------------------------------------------------------------------+
| **Client request** |            **Server capability**            |      **Server response**     |                                                 **Comment**                                                 |
+--------------------+-------------------+-------------------------+-------------------+----------+                                                                                                             |
|   **Addressing**   | **SID supported** | **DataParam supported** |    **Message**    |  **NRC** |                                                                                                             |
+--------------------+-------------------+-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|     functional     |        YES        |           All           | Positive Response |    ---   |                          Server supports the requests and sends positive response.                          |
|                    |                   +-------------------------+                   +----------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |        At least 1       |                   |    ---   |                          Server supports the requests and sends positive response.                          |
|                    |                   +-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |        At least 1       | Negative Response | NRC = XX | Server sends negative response because an error occurred processing the data parameters of request message. |
|                    |                   +-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |           None          |    No Response    |    ---   |                                       Server does not send a response.                                      |
|                    +-------------------+-------------------------+                   +----------+-------------------------------------------------------------------------------------------------------------+
|                    |         NO        |           ---           |                   |    ---   |                                       Server does not send a response.                                      |
+--------------------+-------------------+-------------------------+-------------------+----------+-------------------------------------------------------------------------------------------------------------+

where:

- SPRMIB - flag informing whether Suppress Positive Response Message Indication Bit is set in the received request
  message
- SID supported - flag informing whether Service Identifier in the received request message is supported by the server
- SF supported - flag informing whether SubFunction in the received request message is supported by the server
- DataParam supported - information whether values of data parameters (e.g. DIDs, RIDs, DTCStatusMask) in the received
  request message are supported by the server
- NRC - :ref:`Negative Response Code <knowledge-base-nrc>`
- XX - NRC code that is supported by the server and suitable to the current situation (e.g. NRC 0x21 busyRepeatRequest
  if server is currently overloaded and cannot process next request message)

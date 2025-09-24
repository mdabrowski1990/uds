.. _knowledge-base-addressing:

Addressing
==========
In UDS communication, addressing determines the participants involved in a message exchange, specifying the sender
and one or more receivers.

The following addressing types are defined:

- `Physical Addressing`_
- `Functional Addressing`_


.. _knowledge-base-physical-addressing:

Physical Addressing
-------------------
Physical addressing is used for communication between a single client and a single server.
Messages are transmitted directly (point-to-point) between the client and the server.
The server shall respond to a physically addressed request message unless the request message explicitly indicates that
no response is required.

.. note:: A direct physical connection is not required for physically addressed communication.
  Messages may be routed through gateways to reach the intended server.


Response behaviour to physically addressed request
``````````````````````````````````````````````````
Expected server behaviour when receiving a physically addressed request message containing a SubFunction parameter:

+----------------------------------+----------------------------------------------------------------+-----------------------------------------------+----------------------------------------------------------+
|        **Client request**        |                      **Server capability**                     |              **Server response**              |                        **Comment**                       |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+                                                          |
| **Addressing** |    **SPRMIB**   | **SID supported** | **SF supported** | **DataParam supported** |      **Message**      |        **NRC**        |                                                          |
+================+=================+===================+==================+=========================+=======================+=======================+==========================================================+
|    physical    | False (bit = 0) |        YES        |        YES       |        At least 1       |   Positive Response   |          ---          | Server supports the request and sends positive response. |
|                |                 |                   |                  +-------------------------+-----------------------+-----------------------+----------------------------------------------------------+
|                |                 |                   |                  |        At least 1       |   Negative Response   |        NRC = XX       | Server sends negative response because an error occurred |
|                |                 |                   |                  |                         |                       |                       |                                                          |
|                |                 |                   |                  |                         |                       |                       | while processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+                       +-----------------------+----------------------------------------------------------+
|                |                 |                   |                  |           None          |                       |       NRC = ROOR      |       Server sends negative response with NRC 0x31.      |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+----------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                       |  NRC = SNS or SNSIAS  |   Server sends negative response with NRC 0x11 or 0x7F.  |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+----------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                       | NRC = SFNS or SFNSIAS |   Server sends negative response with NRC 0x12 or 0x7E.  |
|                +-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+----------------------------------------------------------+
|                |  True (bit = 1) |        YES        |        YES       |        At least 1       |      No Response      |          ---          |             Server does not send a response.             |
|                |                 |                   |                  +-------------------------+-----------------------+-----------------------+----------------------------------------------------------+
|                |                 |                   |                  |        At least 1       |   Negative Response   |        NRC = XX       | Server sends negative response because an error occurred |
|                |                 |                   |                  |                         |                       |                       |                                                          |
|                |                 |                   |                  |                         |                       |                       | during request message processing.                       |
|                |                 |                   |                  +-------------------------+                       +-----------------------+----------------------------------------------------------+
|                |                 |                   |                  |           None          |                       |       NRC = ROOR      |       Server sends negative response with NRC 0x31.      |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+----------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                       |  NRC = SNS or SNSIAS  |   Server sends negative response with NRC 0x11 or 0x7F.  |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+----------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                       | NRC = SFNS or SFNSIAS |   Server sends negative response with NRC 0x12 or 0x7E.  |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+----------------------------------------------------------+

Expected server behaviour when receiving a physically addressed request message without a SubFunction parameter:

+--------------------+---------------------------------------------+-----------------------------------------+----------------------------------------------------------+
| **Client request** |            **Server capability**            |           **Server response**           |                        **Comment**                       |
+--------------------+-------------------+-------------------------+-------------------+---------------------+                                                          |
|   **Addressing**   | **SID supported** | **DataParam supported** |    **Message**    |       **NRC**       |                                                          |
+====================+===================+=========================+===================+=====================+==========================================================+
|      physical      |        YES        |           All           | Positive Response |         ---         | Server supports the request and sends positive response. |
|                    |                   +-------------------------+                   +---------------------+----------------------------------------------------------+
|                    |                   |        At least 1       |                   |         ---         | Server supports the request and sends positive response. |
|                    |                   +-------------------------+-------------------+---------------------+----------------------------------------------------------+
|                    |                   |        At least 1       | Negative Response |       NRC = XX      | Server sends negative response because an error occurred |
|                    |                   |                         |                   |                     |                                                          |
|                    |                   |                         |                   |                     | while processing the data parameters of request message. |
|                    |                   +-------------------------+                   +---------------------+----------------------------------------------------------+
|                    |                   |           None          |                   |      NRC = ROOR     |       Server sends negative response with NRC 0x31.      |
|                    +-------------------+-------------------------+                   +---------------------+----------------------------------------------------------+
|                    |         NO        |           ---           |                   | NRC = SNS or SNSIAS |   Server sends negative response with NRC 0x11 or 0x7F   |
+--------------------+-------------------+-------------------------+-------------------+---------------------+----------------------------------------------------------+

where:

- SPRMIB - indicates whether the Suppress Positive Response Message Indication Bit is set in the received request message
- SID supported - indicates whether the Service Identifier in the received request message is supported by the server
- SF supported - indicates whether the SubFunction in the received request message is supported
- DataParam supported - indicates whether the values of data parameters (e.g., DIDs, RIDs, DTCStatusMask)
  in the request are supported
- NRC - :ref:`Negative Response Code <knowledge-base-nrc>`
- ROOR - NRC 0x31 (requestOutOfRange)
- SNS - NRC 0x11 (serviceNotSupported)
- SNSIAS - NRC 0x7F (serviceNotSupportedInActiveSession)
- SFNS - NRC 0x12 (SubFunctionNotSupported)
- SFNSIAS - NRC 0x7E (SubFunctionNotSupportedInActiveSession)
- XX - server-specific NRC suitable for the current situation (e.g., 0x21 busyRepeatRequest if the server is
  temporarily unable to process a request message)


.. _knowledge-base-functional-addressing:

Functional Addressing
---------------------
Functional addressing is used to send messages to multiple servers (ECUs) simultaneously.
In this mode, a one-to-many communication occurs between a client and multiple servers.
Servers respond only to specific functionally addressed request messages.

.. note:: Certain bus types (e.g., LIN) support broadcast communication, which slightly alters the expected
  server behaviour.
  In such cases, servers do not have to respond to broadcast messages, and the client does not expect a response.


Response behaviour to functionally addressed request
````````````````````````````````````````````````````
Expected server behaviour when receiving a functionally addressed request message containing a SubFunction parameter:

+----------------------------------+----------------------------------------------------------------+------------------------------+----------------------------------------------------------+
|        **Client request**        |                      **Server capability**                     |      **Server response**     |                        **Comment**                       |
+----------------+-----------------+-------------------+------------------+-------------------------+-------------------+----------+                                                          |
| **Addressing** |    **SPRMIB**   | **SID supported** | **SF supported** | **DataParam supported** |    **Message**    |  **NRC** |                                                          |
+================+=================+===================+==================+=========================+===================+==========+==========================================================+
|   functional   | False (bit = 0) |        YES        |        YES       |        At least 1       | Positive Response |    ---   | Server supports the request and sends positive response. |
|                |                 |                   |                  +-------------------------+-------------------+----------+----------------------------------------------------------+
|                |                 |                   |                  |        At least 1       | Negative Response | NRC = XX | Server sends negative response because an error occurred |
|                |                 |                   |                  |                         |                   |          |                                                          |
|                |                 |                   |                  |                         |                   |          | while processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+-------------------+----------+----------------------------------------------------------+
|                |                 |                   |                  |           None          |    No Response    |    ---   |             Server does not send a response.             |
|                |                 +-------------------+------------------+-------------------------+                   +----------+----------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                   |    ---   |             Server does not send a response.             |
|                |                 +-------------------+------------------+-------------------------+                   +----------+----------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                   |    ---   |             Server does not send a response.             |
|                +-----------------+-------------------+------------------+-------------------------+-------------------+----------+----------------------------------------------------------+
|                |  True (bit = 1) |        YES        |        YES       |        At least 1       |    No Response    |    ---   |             Server does not send a response.             |
|                |                 |                   |                  +-------------------------+-------------------+----------+----------------------------------------------------------+
|                |                 |                   |                  |        At least 1       | Negative Response | NRC = XX | Server sends negative response because an error occurred |
|                |                 |                   |                  |                         |                   |          |                                                          |
|                |                 |                   |                  |                         |                   |          | while processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+-------------------+----------+----------------------------------------------------------+
|                |                 |                   |                  |           None          |    No Response    |    ---   |             Server does not send a response.             |
|                |                 +-------------------+------------------+-------------------------+                   +----------+----------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                   |    ---   |             Server does not send a response.             |
|                |                 +-------------------+------------------+-------------------------+                   +----------+----------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                   |    ---   |             Server does not send a response.             |
+----------------+-----------------+-------------------+------------------+-------------------------+-------------------+----------+----------------------------------------------------------+

Expected server behaviour when receiving a functionally addressed request message without a SubFunction parameter:

+--------------------+---------------------------------------------+------------------------------+----------------------------------------------------------+
| **Client request** |            **Server capability**            |      **Server response**     |                        **Comment**                       |
+--------------------+-------------------+-------------------------+-------------------+----------+                                                          |
|   **Addressing**   | **SID supported** | **DataParam supported** |    **Message**    |  **NRC** |                                                          |
+====================+===================+=========================+===================+==========+==========================================================+
|     functional     |        YES        |           All           | Positive Response |    ---   | Server supports the request and sends positive response. |
|                    |                   +-------------------------+                   +----------+----------------------------------------------------------+
|                    |                   |        At least 1       |                   |    ---   | Server supports the request and sends positive response. |
|                    |                   +-------------------------+-------------------+----------+----------------------------------------------------------+
|                    |                   |        At least 1       | Negative Response | NRC = XX | Server sends negative response because an error occurred |
|                    |                   |                         |                   |          |                                                          |
|                    |                   |                         |                   |          | while processing the data parameters of request message. |
|                    |                   +-------------------------+-------------------+----------+----------------------------------------------------------+
|                    |                   |           None          |    No Response    |    ---   |             Server does not send a response.             |
|                    +-------------------+-------------------------+                   +----------+----------------------------------------------------------+
|                    |         NO        |           ---           |                   |    ---   |             Server does not send a response.             |
+--------------------+-------------------+-------------------------+-------------------+----------+----------------------------------------------------------+

where:

- SPRMIB - indicates whether the Suppress Positive Response Message Indication Bit is set in the received request message
- SID supported - indicates whether the Service Identifier in the received request message is supported by the server
- SF supported - indicates whether the SubFunction in the received request message is supported
- DataParam supported - indicates whether the values of data parameters (e.g., DIDs, RIDs, DTCStatusMask)
  in the request message are supported
- NRC - :ref:`Negative Response Code <knowledge-base-nrc>`
- XX - server-specific NRC suitable for the current situation (e.g., 0x21 busyRepeatRequest if the server is
  temporarily unable to process a request message)

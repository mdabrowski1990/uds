UDS Knowledge Base
==================
If you are not an UDS expert, this part of documentation is created for you. It is meant to provide a technical support
for every user of `UDS package <https://github.com/mdabrowski1990/uds>`_ so you can better understand the code, but also
UDS protocol itself.


Client
------

Server
------


Data Flow
---------
UDS communication is always initiated by a client_ who sends a diagnostic request to a network that it is connected to.
The client_ might not be directly connected to a desired recipient(s) of the request, therefore some servers might be
forced to act as gateways and transmit the request to another network(s) to which they are connected. Server_ decision
(whether to redirect the request to another vehicle sub-network or not) depends on a target(s) of the request i.e.
server_ shall transmit the request in the sub-network if at least on ECU in this sub-network is the target of
the request.

.. figure:: ../diagrams/KnowledgeBase-Gateway_request.png
    :alt: Gateway - request
    :figclass: align-center

    Diagnostic request routing in example vehicle networks.

    In this example all ECUs in the vehicle are the targets of the request - functionally addressed request was sent.


Each server_ which was the recipient of the request, might decide to send a response back to the nearest client_
(the one which transmitted the request in this sub-network). Then, the client_ shall act as the gateway again and
redirect the response back until it reaches the request message originator (Diagnostic Tester).

.. figure:: ../diagrams/KnowledgeBase-Gateway_response.png
    :alt: Gateway - response
    :figclass: align-center

    Diagnostic responses routing in example vehicle networks.

    In this example all ECUs in the vehicle responds to the request.


Both examples that were presented above, uses terminology like *'diagnostic message'*, *'diagnostic request'* and
*'diagnostic response'* that were not previously explained.

- `diagnostic message`_ - also called 'diagnostic service' or Application Protocol Data Unit (A_PDU)
-


.. figure:: ../diagrams/KnowledgeBase-PDUs.png
    :alt: UDS PDUs
    :figclass: align-center
    :width: 20000


Diagnostic Message
``````````````````


Addressing
''''''''''
Addressing determines model of UDS communication.

We distinguish following addressing types:
 - Physical_
 - Functional_


Physical
........
Physical addressing is used to send a dedicated message to a certain server (ECU).
When physically addressed messages are sent, the direct (point-to-point) communication between the client and
the server takes place. The server shall respond to physically addressed request unless the request contains
an information that response is not required (further explained in`response behaviour to physically addressed request`_
chapter).

NOTE: You do not need a direct physical connection between the client and the server to have physically addressed
communication as all messages shall be routed to a target of each message.

Response behaviour to physically addressed request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Expected server behaviour in case of receiving physically addressed request message with SubFunction parameter:

+----------------------------------+----------------------------------------------------------------+-----------------------------------------------+-------------------------------------------------------------------------------------------------------------+
|        **Client request**        |                      **Server capability**                     |              **Server response**              |                                                 **Comment**                                                 |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+                                                                                                             |
| **Addressing** |    **SPRMIB**   | **SID supported** | **SF supported** | **DataParam supported** |      **Message**      |        **NRC**        |                                                                                                             |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|    physical    | False (bit = 0) |        YES        |        YES       |        At least 1       |   Positive Response   |          ---          |                          Server supports the requests and sends positive response.                          |
|                |                 |                   |                  +-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |        At least 1       |   Negative Response   |        NRC = XX       | Server sends negative response because an error occurred processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |           None          |                       |       NRC = ROOR      |                                Servers sends negative response with NRC 0x31.                               |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                       |  NRC = SNS or SNSIAS  |                            Servers sends negative response with NRC 0x11 or 0x7F.                           |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                       | NRC = SFNS or SFNSIAS |                            Servers sends negative response with NRC 0x12 or 0x7E.                           |
|                +-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |  True (bit = 1) |        YES        |        YES       |        At least 1       |      No Response      |          ---          |                                       Server does not send a response.                                      |
|                |                 |                   |                  +-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |        At least 1       |   Negative Response   |        NRC = XX       | Server sends negative response because an error occurred processing the data parameters of request message. |
|                |                 |                   |                  +-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |                   |                  |           None          |                       |       NRC = ROOR      |                                Servers sends negative response with NRC 0x31.                               |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |         NO        |        ---       |           ---           |                       |  NRC = SNS or SNSIAS  |                            Servers sends negative response with NRC 0x11 or 0x7F.                           |
|                |                 +-------------------+------------------+-------------------------+                       +-----------------------+-------------------------------------------------------------------------------------------------------------+
|                |                 |        YES        |        NO        |           ---           |                       | NRC = SFNS or SFNSIAS |                            Servers sends negative response with NRC 0x12 or 0x7E.                           |
+----------------+-----------------+-------------------+------------------+-------------------------+-----------------------+-----------------------+-------------------------------------------------------------------------------------------------------------+

Expected server behaviour in case of receiving physically addressed request message without SubFunction parameter:

+--------------------+---------------------------------------------+-----------------------------------------+-------------------------------------------------------------------------------------------------------------+
| **Client request** |            **Server capability**            |           **Server response**           |                                                 **Comment**                                                 |
+--------------------+-------------------+-------------------------+-------------------+---------------------+                                                                                                             |
|   **Addressing**   | **SID supported** | **DataParam supported** |    **Message**    |       **NRC**       |                                                                                                             |
+--------------------+-------------------+-------------------------+-------------------+---------------------+-------------------------------------------------------------------------------------------------------------+
|      physical      |        YES        |           All           | Positive Response |         ---         |                          Server supports the requests and sends positive response.                          |
|                    |                   +-------------------------+                   +---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |        At least 1       |                   |         ---         |                          Server supports the requests and sends positive response.                          |
|                    |                   +-------------------------+-------------------+---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |        At least 1       | Negative Response |       NRC = XX      | Server sends negative response because an error occurred processing the data parameters of request message. |
|                    |                   +-------------------------+                   +---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |                   |           None          |                   |      NRC = ROOR     |                                Servers sends negative response with NRC 0x31.                               |
|                    +-------------------+-------------------------+                   +---------------------+-------------------------------------------------------------------------------------------------------------+
|                    |         NO        |           ---           |                   | NRC = SNS or SNSIAS |                            Servers sends negative response with NRC 0x11 or 0x7F                            |
+--------------------+-------------------+-------------------------+-------------------+---------------------+-------------------------------------------------------------------------------------------------------------+


Explanation:
 - SPRMIB - flag informing whether Suppress Positive Response Message Indication Bit is set in the received request
   message
 - SID supported - flag informing whether Service Identifier in the received request message is supported by the server
 - SF supported - flag informing whether SubFunction in the received request message is supported by the server
 - DataParam supported - information whether values of data parameters (e.g. DIDs, RIDs, DTCStatusMask) in the received
   request message are supported by the server
 - NRC - Negative Response Code
 - ROOR - NRC 0x31 (requestOutOfRange)
 - SNS - NRC 0x11 (serviceNotSupported)
 - SNSIAS - NRC 0x7F (serviceNotSupportedInActiveSession)
 - SFNS - NRC 0x12 (SubFunctionNotSupported)
 - SFNSIAS - NRC 0x7E (SubFunctionNotSupportedInActiveSession)
 - XX - NRC code that is supported by the server and suitable to the current situation (e.g. NRC 0x21 busyRepeatRequest
   if server is currently overloaded and cannot process next request message)


Functional
..........
Functional addressing is used to send messages to multiple servers (ECUs) in the network.
When functionally addressed messages are sent, the one to many communication between the client and
the servers (ECUs) takes place. The server shall only respond to certain requests (further explained in
`response behaviour to functionally addressed request`_ chapter.

NOTE: Some types of buses (e.g. LIN) might also support broadcast communication which is very similar to functionally
addressed. The only difference is that a server response is never expected by the client during broadcast communication.

Response behaviour to functionally addressed request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

Explanation:
 - SPRMIB - flag informing whether Suppress Positive Response Message Indication Bit is set in the received request
   message
 - SID supported - flag informing whether Service Identifier in the received request message is supported by the server
 - SF supported - flag informing whether SubFunction in the received request message is supported by the server
 - DataParam supported - information whether values of data parameters (e.g. DIDs, RIDs, DTCStatusMask) in the received
   request message are supported by the server
 - NRC - Negative Response Code
 - XX - NRC code that is supported by the server and suitable to the current situation (e.g. NRC 0x21 busyRepeatRequest
   if server is currently overloaded and cannot process next request message)


Segmentation
````````````

UDS Packet
''''''''''''''''''''''''''
UDS packet is also called Network Protocol Data Unit (N_PDU). It is created during segmentation_ of a
`diagnostic message`_. Each `diagnostic message`_ consists of at least one N_PDU. There are some packets (N_PDUs) which
does not carry any `diagnostic message`_ data as they are used to manage the flow of other packets (N_PDUs).

UDS packet (N_PDU) consists of following fields:
 - `Network Address Information`_ (N_AI) - packet addressing
 - `Network Protocol Control Information`_ (N_PCI) - packet type
 - `Network Data Field`_ (N_Data) - packet date


Network Address Information
...........................
Network Address Information (N_AI) contains address information which identifies the recipient(s) and the sender
between whom data exchange takes place. It also describes communication model (e.g. whether response is required)
for the message.


Network Protocol Control Information
....................................
Network Protocol Control Information (N_PCI) identifies the type of `UDS packet`_ (Network Protocol Data Unit).
Supported N_PCIs and theirs values interpretation are bus specific.


Network Data Field
..................
Network Data Field (N_Data) carries `diagnostic message`_ data. It might be an entire `diagnostic message`_ data (if
`diagnostic message`_ fits into one packet) or just a part (a single packet) of it (if `segmentation`_ had to be
used to divide `diagnostic message`_ into smaller parts).

UDS Knowledge Base
==================
If you are not an UDS expert, this part of documentation is created for you. It is meant to provide a technical support
for every user of `UDS package <https://github.com/mdabrowski1990/uds>`_ so you can better understand the code, but also
UDS protocol itself.


Client
------
TODO DURING `CLIENT EPIC <https://github.com/mdabrowski1990/uds/milestone/8>`_


Server
------
TODO DURING `SERVER EPIC <https://github.com/mdabrowski1990/uds/milestone/7>`_


Diagnostic Message
------------------
If we only consider the top layer of OSI Model (layer 7 - Application), then the messages that are exchanged by
clients and servers during UDS communication would be called 'Application Protocol Data Units' (A_PDU),
'diagnostic messages' or 'UDS messages'.

There are two types of diagnostic messages:
 - `diagnostic request`_ - a message transmitted by a client
 - `diagnostic response`_ - a message transmitted by a server


UDS communication is always initiated by a client_ who sends a `diagnostic request`_ to a network that it is connected to.
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


To better understand 'diagnostic message' terminology, we need to know how these messages are actually transmitted
(what entities carry the message on other layers of OSI model). This is presented in the figure below:

.. figure:: ../diagrams/KnowledgeBase-PDUs.png
    :alt: UDS PDUs
    :figclass: align-center
    :width: 100%

    UDS Protocol Data Units on different layers of OSI Model.

We distinguish (in UDS package implementation) following entities on different layers of UDS OSI model, that take part in UDS communication:
 - `Diagnostic message`_ - also called 'Application Protocol Data Unit' (A_PDU)
 - `UDS packet`_ - also called 'Network Protocol Data Unit' (N_PDU). UDS packets types and transmission rules are
    bus specific.
 - `Frame <https://en.wikipedia.org/wiki/Frame_(networking)>`_ - the smallest piece of information exchanged by nodes
   in a bus network


Diagnostic Request
``````````````````
TODO


Diagnostic Response
```````````````````
TODO


Service Identifier
``````````````````
Service Identifies (SID) is one byte integer located in the first byte of Application Data (A_Data) in the
`diagnostic message`_. SID identifies whether the message is `diagnostic request`_ or `diagnostic response`_, but also
the service that the message carries. Services are used to execute special function in the on-board ECUs.

List of all Service Identifier (SID) values and their application:
 - 0x00 - not applicable, reserved by ISO 14229-1
 - 0x01-0x0F - ISO 15031-5/SAE J1979 specific services
 - 0x10 - `DiagnosticSessionControl`_ service request
 - 0x11 - `ECUReset`_ service request
 - 0x12-0x13 - reserved by ISO 14229-1
 - 0x14 - `ClearDiagnosticInformation`_ service request
 - 0x15-0x18 - reserved by ISO 14229-1
 - 0x19 - `ReadDTCInformation`_ service request
 - 0x1A-0x21 - reserved by ISO 14229-1
 - 0x22 - `ReadDataByIdentifier`_ service request
 - 0x23 - `ReadMemoryByAddress`_ service request
 - 0x24 - `ReadScalingDataByIdentifier`_ service request
 - 0x25-0x26 - reserved by ISO 14229-1
 - 0x27 - `SecurityAccess`_ service request
 - 0x28 - `CommunicationControl`_ service request
 - 0x29 - `Authentication`_ service request
 - 0x2A - `ReadDataByPeriodicIdentifier`_ service request
 - 0x2B - reserved by ISO 14229-1
 - 0x2C - `DynamicallyDefineDataIdentifier`_ service request
 - 0x2D - reserved by ISO 14229-1
 - 0x2E - `WriteDataByIdentifier`_ service request
 - 0x2F - `InputOutputControlByIdentifier`_ service request
 - 0x30 - reserved by ISO 14229-1
 - 0x31 - `RoutineControl`_ service request
 - 0x32-0x23 - reserved by ISO 14229-1
 - 0x34 - `RequestDownload`_ service request
 - 0x35 - `RequestUpload`_ service request
 - 0x36 - `TransferData`_ service request
 - 0x37 - `RequestTransferExit`_ service request
 - 0x38 - `RequestFileTransfer`_ service request
 - 0x39-0x3C - reserved by ISO 14229-1
 - 0x3D - `WriteMemoryByAddress`_ service request
 - 0x3E - `TesterPresent`_ service request
 - 0x3F - not applicable, reserved by ISO 14229-1
 - 0x40 - not applicable, reserved by ISO 14229-1
 - 0x41-0x4F - ISO 15031-5/SAE J1979 specific services
 - 0x50 - positive response to `DiagnosticSessionControl`_ service
 - 0x51 - positive response to `ECUReset`_ service
 - 0x52-0x53 - reserved by ISO 14229-1
 - 0x54 - positive response to `ClearDiagnosticInformation`_ service
 - 0x55-0x58 - reserved by ISO 14229-1
 - 0x59 - positive response to `ReadDTCInformation`_ service
 - 0x5A-0x61 - reserved by ISO 14229-1
 - 0x62 - positive response to `ReadDataByIdentifier`_ service
 - 0x63 - positive response to `ReadMemoryByAddress`_ service
 - 0x64 - positive response to `ReadScalingDataByIdentifier`_ service
 - 0x63-0x66 - reserved by ISO 14229-1
 - 0x67 - positive response to `SecurityAccess`_ service
 - 0x68 - positive response to `CommunicationControl`_ service
 - 0x69 - positive response to `Authentication`_ service
 - 0x6A - positive response to `ReadDataByPeriodicIdentifier`_ service
 - 0x6B - reserved by ISO 14229-1
 - 0x6C - positive response to `DynamicallyDefineDataIdentifier`_ service
 - 0x6D - reserved by ISO 14229-1
 - 0x6E - positive response to `WriteDataByIdentifier`_ service
 - 0x6F - positive response to `InputOutputControlByIdentifier`_ service
 - 0x70 - reserved by ISO 14229-1
 - 0x71 - positive response to `RoutineControl`_ service
 - 0x72-0x73 - reserved by ISO 14229-1
 - 0x74 - positive response to `RequestDownload`_ service
 - 0x75 - positive response to `RequestUpload`_ service
 - 0x76 - positive response to `TransferData`_ service
 - 0x77 - positive response to `RequestTransferExit`_ service
 - 0x78 - positive response to `RequestFileTransfer`_ service
 - 0x79-0x7C - reserved by ISO 14229-1
 - 0x7D - positive response to `WriteMemoryByAddress`_ service
 - 0x7E - positive response to `TesterPresent`_ service
 - 0x7F - negative response service identifier
 - 0x80-0x82 - not applicable, reserved by ISO 14229-1
 - 0x83 - reserved by ISO 14229-1
 - 0x84 - `SecuredDataTransmission`_ service request
 - 0x85 - `ControlDTCSetting`_ service request
 - 0x86 - `ResponseOnEvent`_ service request
 - 0x87 - `LinkControl`_ service request
 - 0x88 - reserved by ISO 14229-1
 - 0x89-0xB9 - not applicable, reserved by ISO 14229-1
 - 0xBA-0xBE - system supplier specific service requests
 - 0xBF-0xC2 - not applicable, reserved by ISO 14229-1
 - 0xC3 - reserved by ISO 14229-1
 - 0xC4 - positive response to `SecuredDataTransmission`_ service
 - 0xC5 - positive response to `ControlDTCSetting`_ service
 - 0xC6 - positive response to `ResponseOnEvent`_ service
 - 0xC7 - positive response to `LinkControl`_ service
 - 0xC8 - reserved by ISO 14229-1
 - 0xC9-0xF9 - not applicable, reserved by ISO 14229-1
 - 0xFA-0xFE - positive responses to system supplier specific requests
 - 0xFF - not applicable, reserved by ISO 14229-1


DiagnosticSessionControl
''''''''''''''''''''''''
DiagnosticSessionControl service is used to change diagnostic sessions in the server(s).
In each diagnostic session a different set of diagnostic services (and/or functionalities) is enabled in the server.
Server shall always be in exactly one diagnostic session.


ECUReset
''''''''
ECUReset service is used by the client to request a server reset.


ClearDiagnosticInformation
''''''''''''''''''''''''''
ClearDiagnosticInformation service is used by the client to clear all diagnostic information (DTC and related data)
in one or multiple servers' memory.


ReadDTCInformation
''''''''''''''''''
ReadDTCInformation service allows the client to read from any server or group of servers within a vehicle,
current information about all Diagnostic Trouble Codes. This could be a status of reported Diagnostic Trouble Code (DTC),
number of currently active DTCs or any other information returned by supported ReadDTCInformation SubFunctions.


ReadDataByIdentifier
''''''''''''''''''''
ReadDataByIdentifier service allows the client to request data record values from the server identifier by one or more
DataIdentifiers (DIDs).


ReadMemoryByAddress
'''''''''''''''''''
ReadMemoryByAddress service allows the client to request server's memory data stored under provided memory address.


ReadScalingDataByIdentifier
'''''''''''''''''''''''''''
ReadScalingDataByIdentifier service allows the client to request from the server a scaling data record identified
by a DataIdentifier (DID). The scaling data contains information such as data record type (e.g. ASCII, signed float),
formula and its coefficients used for value calculation, units, etc.


SecurityAccess
''''''''''''''
SecurityAccess service allows the client to unlock functions/services with restricted access.


CommunicationControl
''''''''''''''''''''
CommunicationControl service allows the client to switch on/off the transmission and/or the reception of certain
messages on a server(s).


Authentication
''''''''''''''
Authentication service provides a means for the client to prove its identity, allowing it to access data and/or
diagnostic services, which have restricted access for, for example security, emissions, or safety reasons.


ReadDataByPeriodicIdentifier
''''''''''''''''''''''''''''
ReadDataByPeriodicIdentifier service allows the client to request the periodic transmission of data record values
from the server identified by one or more periodicDataIdentifiers.


DynamicallyDefineDataIdentifier
'''''''''''''''''''''''''''''''
DynamicallyDefineDataIdentifier service allows the client to dynamically define in a server a DataIdentifier (DID)
that can be read via the ReadDataByIdentifier_ service at a later time.


WriteDataByIdentifier
'''''''''''''''''''''
WriteDataByIdentifier service allows the client to write information into the server at an internal location
specified by the provided DataIdentifier (DID).


InputOutputControlByIdentifier
''''''''''''''''''''''''''''''
InputOutputControlByIdentifier service allows the client to substitute a value for an input signal, internal server
function and/or force control to a value for an output (actuator) of an electronic system.


RoutineControl
''''''''''''''
RoutineControl service allows the client to execute a defined sequence of steps to obtain any relevant result.
There is a lot of flexibility with this service, but typical usage may include functionality such as erasing memory,
resetting or learning adaptive data, running a self-test, overriding the normal server control strategy.


RequestDownload
'''''''''''''''
RequestDownload service allows the client to initiate a data transfer from the client to the server (download).


RequestUpload
'''''''''''''
RequestUpload service allows the client to initiate a data transfer from the server to the client (upload).


TransferData
''''''''''''
TransferData service is used by the client to transfer data either from the client to the server (download) or
from the server to the client (upload).


RequestTransferExit
'''''''''''''''''''
RequestTransferExit service is used by the client to terminate a data transfer between the client and server.


RequestFileTransfer
'''''''''''''''''''
RequestFileTransfer service allows the client to initiate a file data transfer either from the server to
the client (upload) or from the server to the client (upload).


WriteMemoryByAddress
''''''''''''''''''''
WriteMemoryByAddress service allows the client to write information into server's memory data under provided
memory address.


TesterPresent
'''''''''''''
TesterPresent service is used by the client to indicate to a server(s) that the client is still connected to a vehicle
and certain diagnostic services and/or communication that have been previously activated are to remain active.


SecuredDataTransmission
'''''''''''''''''''''''
SecuredDataTransmission service is applicable if a client intends to use diagnostic services defined
in this document in a secured mode. It may also be used to transmit external data, which conform to
some other application protocol, in a secured mode between a client and a server. A secured mode in
this context means that the data transmitted is protected by cryptographic methods.


ControlDTCSetting
'''''''''''''''''
ControlDTCSetting service allows the client to stop or resume the updating of DTC status bits in the server(s) memory.


ResponseOnEvent
'''''''''''''''
ResponseOnEvent service allows the client to request from the server to start ot stop transmission of responses on
a specified event.


LinkControl
'''''''''''
LinkControl service allows the client to control the communication between the client and the server(s) in order to
gain bus bandwidth for diagnostic purposes (e.g. programming).


Addressing
``````````
Addressing determines model of UDS communication.

We distinguish following addressing types:
 - Physical_
 - Functional_


Physical
''''''''
Physical addressing is used to send a dedicated message to a certain server (ECU).
When physically addressed messages are sent, the direct (point-to-point) communication between the client and
the server takes place. The server shall respond to physically addressed request unless the request contains
an information that response is not required (further explained in`response behaviour to physically addressed request`_
chapter).

NOTE: You do not need a direct physical connection between the client and the server to have physically addressed
communication as all messages shall be routed to a target of each message.


Response behaviour to physically addressed request
..................................................
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
''''''''''
Functional addressing is used to send messages to multiple servers (ECUs) in the network.
When functionally addressed messages are sent, the one to many communication between the client and
the servers (ECUs) takes place. The server shall only respond to certain requests (further explained in
`response behaviour to functionally addressed request`_ chapter.

NOTE: Some types of buses (e.g. LIN) might also support broadcast communication which is very similar to functionally
addressed. The only difference is that a server response is never expected by the client during broadcast communication.


Response behaviour to functionally addressed request
....................................................
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
TODO


UDS Packet
``````````
UDS packet is also called Network Protocol Data Unit (N_PDU). It is created during segmentation_ of a
`diagnostic message`_. Each `diagnostic message`_ consists of at least one N_PDU. There are some packets (N_PDUs) which
does not carry any `diagnostic message`_ data as they are used to manage the flow of other packets (N_PDUs).

UDS packet (N_PDU) consists of following fields:
 - `Network Address Information`_ (N_AI) - packet addressing
 - `Network Protocol Control Information`_ (N_PCI) - packet type
 - `Network Data Field`_ (N_Data) - packet date


Network Address Information
'''''''''''''''''''''''''''
Network Address Information (N_AI) contains address information which identifies the recipient(s) and the sender
between whom data exchange takes place. It also describes communication model (e.g. whether response is required)
for the message.


Network Protocol Control Information
''''''''''''''''''''''''''''''''''''
Network Protocol Control Information (N_PCI) identifies the type of `UDS packet`_ (Network Protocol Data Unit).
Supported N_PCIs and theirs values interpretation are bus specific.


Network Data Field
''''''''''''''''''
Network Data Field (N_Data) carries `diagnostic message`_ data. It might be an entire `diagnostic message`_ data (if
`diagnostic message`_ fits into one packet) or just a part (a single packet) of it (if `segmentation`_ had to be
used to divide `diagnostic message`_ into smaller parts).

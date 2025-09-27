.. _knowledge-base-service:

Diagnostic Service
==================
Diagnostic services are functions offered by :ref:`Servers (ECUs) <knowledge-base-server>` to
a :ref:`Client <knowledge-base-client>` via the UDS protocol.
Each service is identified by a Service Identifier (SID) value.


.. _knowledge-base-sid:

Service Identifier
------------------
The Service Identifier (SID) is the first byte of the payload (Application Data, A_Data) in each
:ref:`diagnostic message <knowledge-base-diagnostic-message>`.

The SID value determines whether the message is a :ref:`request message <knowledge-base-request-message>`
or a :ref:`diagnostic response <knowledge-base-response-message>`.
It also defines the general purpose and format of the diagnostic message.

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
- 0x32-0x33 - reserved by ISO 14229-1
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
- 0x65-0x66 - reserved by ISO 14229-1
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


Request Service Identifier
``````````````````````````
Request Service Identifier is a subtype of SID. It is the first byte of each request message and identifies
the diagnostic service for which the message is relevant.

.. note:: The 2nd most significant bit (bit 6) of all Request Service Identifiers is 0.


.. _knowledge-base-rsid:

Response Service Identifier
```````````````````````````
Response Service Identifier (RSID) is a subtype of SID. It is the first byte of each response message and identifies
the diagnostic service for which the message is relevant.

.. note:: The 2nd most significant bit (bit 6) of all Response Service Identifiers is 1.


.. _knowledge-base-service-diagnostic-session-control:

DiagnosticSessionControl
------------------------
DiagnosticSessionControl service is used to change diagnostic sessions in the server(s).
In each diagnostic session a different set of diagnostic services (and/or functionalities) is enabled in the server.
Server shall always be in exactly one diagnostic session.

ISO 14229-1 defines the following sessions (values of the *diagnosticSessionType* parameter):

- 0x01 - defaultSession
- 0x02 - programmingSession
- 0x03 - extendedDiagnosticSession
- 0x04 - safetySystemDiagnosticSession


Request Format
``````````````
+----------------------------------------------+-------------+-------------+--------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                    | Present |
+==============================================+=============+=============+================================+=========+
| SID                                          | 8           | 0x10        | DiagnosticSessionControl       | Always  |
+-------------+--------------------------------+-------------+-------------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required          | Always  |
|             |                                |             |             |                                |         |
|             |                                |             |             | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-------------+--------------------------------+---------+
|             | diagnosticSessionType          | 7 (b6 - b0) | 0x00 - 0x7F | Identifies diagnostic session  | Always  |
+-------------+--------------------------------+-------------+-------------+--------------------------------+---------+


Positive Response Format
````````````````````````
+---------------------------------------------------------+-------------+-----------------+-------------------------------------------------------+---------+
| Name                                                    | Bit Length  | Value           | Description                                           | Present |
+=========================================================+=============+=================+=======================================================+=========+
| RSID                                                    | 8           | 0x50            | Positive Response: DiagnosticSessionControl (0x10)    | Always  |
+------------------------+--------------------------------+-------------+-----------------+-------------------------------------------------------+---------+
|       subFunction      | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1       | 0 = response required                                 | Always  |
|                        |                                |             |                 |                                                       |         |
|                        |                                |             |                 | 1 = suppress positive response                        |         |
|                        +--------------------------------+-------------+-----------------+-------------------------------------------------------+---------+
|                        | diagnosticSessionType          | 7 (b6 - b0) | 0x00 - 0x7F     | Identifies diagnostic session                         | Always  |
+------------------------+--------------------------------+-------------+-----------------+-------------------------------------------------------+---------+
| sessionParameterRecord | P2Server_max                   | 16          | 0x0000 - 0xFFFF | Maximum P2 timing used by server in this session      | Always  |
|                        +--------------------------------+-------------+-----------------+-------------------------------------------------------+---------+
|                        | ``P2*Server_max``              | 16          | 0x0000 - 0xFFFF | Maximum ``P2*`` timing used by server in this session | Always  |
+------------------------+--------------------------------+-------------+-----------------+-------------------------------------------------------+---------+

.. note:: :ref:`P2Server_max <knowledge-base-p2-server>` field is provided directly in milliseconds.
  :ref:`P2*Server_max <knowledge-base-p2*-server>` field is encoded in units of 10 ms, so it must be multiplied by 10
  to obtain the value in milliseconds.


.. _knowledge-base-service-ecu-reset:

ECUReset
--------
The ECUReset service is used by the client to request that the server perform a reset.
The server, after receiving this request, performs the specified type of reset.

ISO 14229-1 defines the following reset types (values of the *resetType* parameter):

- 0x01 - hardReset
- 0x02 - keyOffOnReset
- 0x03 - softReset
- 0x04 - enableRapidPowerShutDown
- 0x05 - disableRapidPowerShutDown


Request Format
``````````````
+----------------------------------------------+-------------+-------------+--------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                    | Present |
+==============================================+=============+=============+================================+=========+
| SID                                          | 8           | 0x11        | ECUReset                       | Always  |
+-------------+--------------------------------+-------------+-------------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required          | Always  |
|             |                                |             |             |                                |         |
|             |                                |             |             | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-------------+--------------------------------+---------+
|             | resetType                      | 7 (b6 - b0) | 0x00 - 0x7F | Specifies the reset type       | Always  |
+-------------+--------------------------------+-------------+-------------+--------------------------------+---------+


Positive Response Format
````````````````````````


ISO 14229-1:2020
''''''''''''''''
+----------------------------------------------+-------------+-------------+-------------------------------------------------+----------------------------+
| Name                                         | Bit Length  | Value       | Description                                     | Present                    |
+==============================================+=============+=============+=================================================+============================+
| RSID                                         | 8           | 0x51        | Positive Response: ECUReset (0x11)              | Always                     |
+-------------+--------------------------------+-------------+-------------+-------------------------------------------------+----------------------------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                           | Always                     |
|             |                                |             |             |                                                 |                            |
|             |                                |             |             | 1 = suppress positive response                  |                            |
|             +--------------------------------+-------------+-------------+-------------------------------------------------+----------------------------+
|             | resetType                      | 7 (b6 - b0) | 0x00 - 0x7F | Specifies the reset type                        | Always                     |
+-------------+--------------------------------+-------------+-------------+-------------------------------------------------+----------------------------+
| powerDownTime                                | 8           | 0x00 - 0xFF | 0x00-0xFE: minimum down time required by server | Only when resetType = 0x04 |
|                                              |             |             |                                                 |                            |
|                                              |             |             | 0xFF: failure or time not available             |                            |
+----------------------------------------------+-------------+-------------+-------------------------------------------------+----------------------------+

.. note:: The :code:`powerDownTime` field is only included in the positive response when
  :code:`resetType = 0x04` (*enableRapidPowerShutDown*).
  It defines the minimum time (in seconds) that the server requires to remain powered down before it can be safely
  restarted. A value of :code:`0xFF` indicates that either the time requirement is not available or a failure occurred.


ISO 14229-1:2013
''''''''''''''''
+----------------------------------------------+-------------+-------------+------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                        | Present |
+==============================================+=============+=============+====================================+=========+
| RSID                                         | 8           | 0x51        | Positive Response: ECUReset (0x11) | Always  |
+-------------+--------------------------------+-------------+-------------+------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required              | Always  |
|             |                                |             |             |                                    |         |
|             |                                |             |             | 1 = suppress positive response     |         |
|             +--------------------------------+-------------+-------------+------------------------------------+---------+
|             | resetType                      | 7 (b6 - b0) | 0x00 - 0x7F | Specifies the reset type           | Always  |
+-------------+--------------------------------+-------------+-------------+------------------------------------+---------+


ClearDiagnosticInformation
--------------------------
ClearDiagnosticInformation service is used by the client to clear all diagnostic information (DTC and related data)
in one or multiple servers' memory.


ReadDTCInformation
------------------
ReadDTCInformation service allows the client to read from any server or group of servers within a vehicle,
current information about all Diagnostic Trouble Codes.
This could be a status of reported Diagnostic Trouble Code (DTC), number of currently active DTCs or any other
information returned by supported ReadDTCInformation SubFunctions.


ReadDataByIdentifier
--------------------
ReadDataByIdentifier service allows the client to request data record values from the server identifier by one or more
DataIdentifiers (DIDs).


ReadMemoryByAddress
-------------------
ReadMemoryByAddress service allows the client to request server's memory data stored under provided memory address.


ReadScalingDataByIdentifier
---------------------------
ReadScalingDataByIdentifier service allows the client to request from the server a scaling data record identified
by a DataIdentifier (DID). The scaling data contains information such as data record type (e.g. ASCII, signed float),
formula and its coefficients used for value calculation, units, etc.


SecurityAccess
--------------
SecurityAccess service allows the client to unlock functions/services with restricted access.


CommunicationControl
--------------------
CommunicationControl service allows the client to switch on/off the transmission and/or the reception of certain
messages on a server(s).


Authentication
--------------
Authentication service provides a means for the client to prove its identity, allowing it to access data and/or
diagnostic services, which have restricted access for, for example security, emissions, or safety reasons.


.. _knowledge-base-service-read-data-by-periodic-identifier:

ReadDataByPeriodicIdentifier
----------------------------
ReadDataByPeriodicIdentifier service allows the client to request the periodic transmission of data record values
from the server identified by one or more periodicDataIdentifiers.


DynamicallyDefineDataIdentifier
-------------------------------
DynamicallyDefineDataIdentifier service allows the client to dynamically define in a server a DataIdentifier (DID)
that can be read via the ReadDataByIdentifier_ service at a later time.


WriteDataByIdentifier
---------------------
WriteDataByIdentifier service allows the client to write information into the server at an internal location
specified by the provided DataIdentifier (DID).


InputOutputControlByIdentifier
------------------------------
InputOutputControlByIdentifier service allows the client to substitute a value for an input signal, internal server
function and/or force control to a value for an output (actuator) of an electronic system.


RoutineControl
--------------
RoutineControl service allows the client to execute a defined sequence of steps to obtain any relevant result.
There is a lot of flexibility with this service, but typical usage may include functionality such as erasing memory,
resetting or learning adaptive data, running a self-test, overriding the normal server control strategy.


RequestDownload
---------------
RequestDownload service allows the client to initiate a data transfer from the client to the server (download).


RequestUpload
-------------
RequestUpload service allows the client to initiate a data transfer from the server to the client (upload).


TransferData
------------
TransferData service is used by the client to transfer data either from the client to the server (download) or
from the server to the client (upload).


RequestTransferExit
-------------------
RequestTransferExit service is used by the client to terminate a data transfer between the client and server.


RequestFileTransfer
-------------------
RequestFileTransfer service allows the client to initiate a file data transfer either from the server to
the client (download) or from the server to the client (upload).


WriteMemoryByAddress
--------------------
WriteMemoryByAddress service allows the client to write information into server's memory data under provided
memory address.


.. _knowledge-base-service-tester-present:

TesterPresent
-------------
TesterPresent service is used by the client to indicate to a server(s) that the client is still connected to a vehicle
and certain diagnostic services and/or communication that have been previously activated are to remain active.


SecuredDataTransmission
-----------------------
SecuredDataTransmission service is applicable if a client intends to use diagnostic services defined
in this document in a secured mode. It may also be used to transmit external data, which conform to
some other application protocol, in a secured mode between a client and a server. A secured mode in
this context means that the data transmitted is protected by cryptographic methods.


ControlDTCSetting
-----------------
ControlDTCSetting service allows the client to stop or resume the updating of DTC status bits in the server(s) memory.


.. _knowledge-base-service-response-on-event:

ResponseOnEvent
---------------
ResponseOnEvent service allows the client to request from the server to start or stop transmission of responses on
a specified event.


LinkControl
-----------
LinkControl service allows the client to control the communication between the client and the server(s) to
gain bus bandwidth for diagnostic purposes (e.g. programming).

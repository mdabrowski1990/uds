.. _knowledge-base-service:

Diagnostic Services
===================
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

- **0x00** - not applicable, reserved by ISO 14229-1
- **0x01**-**0x0F** - ISO 15031-5/SAE J1979 specific services
- **0x10** - :ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` service request
- **0x11** - :ref:`ECUReset <knowledge-base-service-ecu-reset>` service request
- **0x12**-**0x13** - reserved by ISO 14229-1
- **0x14** - :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` service request
- **0x15**-**0x18** - reserved by ISO 14229-1
- **0x19** - :ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` service request
- **0x1A**-**0x21** - reserved by ISO 14229-1
- **0x22** - :ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` service request
- **0x23** - :ref:`ReadMemoryByAddress <knowledge-base-service-read-memory-by-address>` service request
- **0x24** - :ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` service request
- **0x25**-**0x26** - reserved by ISO 14229-1
- **0x27** - :ref:`SecurityAccess <knowledge-base-service-security-access>` service request
- **0x28** - :ref:`CommunicationControl <knowledge-base-service-communication-control>` service request
- **0x29** - :ref:`Authentication <knowledge-base-service-authentication>` service request
- **0x2A** - :ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>` service request
- **0x2B** - reserved by ISO 14229-1
- **0x2C** - :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` service request
- **0x2D** - reserved by ISO 14229-1
- **0x2E** - :ref:`WriteDataByIdentifier <knowledge-base-service-write-data-by-identifier>` service request
- **0x2F** - :ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` service request
- **0x30** - reserved by ISO 14229-1
- **0x31** - :ref:`RoutineControl <knowledge-base-service-routine-control>` service request
- **0x32**-**0x33** - reserved by ISO 14229-1
- **0x34** - :ref:`RequestDownload <knowledge-base-service-request-download>` service request
- **0x35** - :ref:`RequestUpload <knowledge-base-service-request-upload>` service request
- **0x36** - :ref:`TransferData <knowledge-base-service-transfer-data>` service request
- **0x37** - :ref:`RequestTransferExit <knowledge-base-service-request-transfer-exit>` service request
- **0x38** - :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` service request
- **0x39**-**0x3C** - reserved by ISO 14229-1
- **0x3D** - :ref:`WriteMemoryByAddress <knowledge-base-service-write-memory-by-address>` service request
- **0x3E** - :ref:`TesterPresent <knowledge-base-service-tester-present>` service request
- **0x3F** - not applicable, reserved by ISO 14229-1
- **0x40** - not applicable, reserved by ISO 14229-1
- **0x41**-**0x4F** - ISO 15031-5/SAE J1979 specific services
- **0x50** - positive response to :ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` service
- **0x51** - positive response to :ref:`ECUReset <knowledge-base-service-ecu-reset>` service
- **0x52**-**0x53** - reserved by ISO 14229-1
- **0x54** - positive response to :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` service
- **0x55**-**0x58** - reserved by ISO 14229-1
- **0x59** - positive response to :ref:`ReadDTCInformation <knowledge-base-service-read-dtc-information>` service
- **0x5A**-**0x61** - reserved by ISO 14229-1
- **0x62** - positive response to :ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` service
- **0x63** - positive response to :ref:`ReadMemoryByAddress <knowledge-base-service-read-memory-by-address>` service
- **0x64** - positive response to :ref:`ReadScalingDataByIdentifier <knowledge-base-service-read-scaling-data-by-identifier>` service
- **0x65**-**0x66** - reserved by ISO 14229-1
- **0x67** - positive response to :ref:`SecurityAccess <knowledge-base-service-security-access>` service
- **0x68** - positive response to :ref:`CommunicationControl <knowledge-base-service-communication-control>` service
- **0x69** - positive response to :ref:`Authentication <knowledge-base-service-authentication>` service
- **0x6A** - positive response to :ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>` service
- **0x6B** - reserved by ISO 14229-1
- **0x6C** - positive response to :ref:`DynamicallyDefineDataIdentifier <knowledge-base-service-dynamically-define-data-identifier>` service
- **0x6D** - reserved by ISO 14229-1
- **0x6E** - positive response to :ref:`WriteDataByIdentifier <knowledge-base-service-write-data-by-identifier>` service
- **0x6F** - positive response to :ref:`InputOutputControlByIdentifier <knowledge-base-service-input-output-control-by-identifier>` service
- **0x70** - reserved by ISO 14229-1
- **0x71** - positive response to :ref:`RoutineControl <knowledge-base-service-routine-control>` service
- **0x72**-**0x73** - reserved by ISO 14229-1
- **0x74** - positive response to :ref:`RequestDownload <knowledge-base-service-request-download>` service
- **0x75** - positive response to :ref:`RequestUpload <knowledge-base-service-request-upload>` service
- **0x76** - positive response to :ref:`TransferData <knowledge-base-service-transfer-data>` service
- **0x77** - positive response to :ref:`RequestTransferExit <knowledge-base-service-request-transfer-exit>` service
- **0x78** - positive response to :ref:`RequestFileTransfer <knowledge-base-service-request-file-transfer>` service
- **0x79**-**0x7C** - reserved by ISO 14229-1
- **0x7D** - positive response to :ref:`WriteMemoryByAddress <knowledge-base-service-write-memory-by-address>` service
- **0x7E** - positive response to :ref:`TesterPresent <knowledge-base-service-tester-present>` service
- **0x7F** - negative response service identifier
- **0x80**-**0x82** - not applicable, reserved by ISO 14229-1
- **0x83** - :ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` service request
  *(withdrawn in ISO 14229-1:2020)*
- **0x84** - :ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>` service request
- **0x85** - :ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` service request
- **0x86** - :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service request
- **0x87** - :ref:`LinkControl <knowledge-base-service-link-control>` service request
- **0x88** - reserved by ISO 14229-1
- **0x89**-**0xB9** - not applicable, reserved by ISO 14229-1
- **0xBA**-**0xBE** - system supplier specific service requests
- **0xBF**-**0xC2** - not applicable, reserved by ISO 14229-1
- **0xC3** - positive response to :ref:`AccessTimingParameter <knowledge-base-service-access-timing-parameter>` service
  *(withdrawn in ISO 14229-1:2020)*
- **0xC4** - positive response to :ref:`SecuredDataTransmission <knowledge-base-service-secured-data-transmission>` service
- **0xC5** - positive response to :ref:`ControlDTCSetting <knowledge-base-service-control-dtc-setting>` service
- **0xC6** - positive response to :ref:`ResponseOnEvent <knowledge-base-service-response-on-event>` service
- **0xC7** - positive response to :ref:`LinkControl <knowledge-base-service-link-control>` service
- **0xC8** - reserved by ISO 14229-1
- **0xC9**-**0xF9** - not applicable, reserved by ISO 14229-1
- **0xFA**-**0xFE** - positive responses to system supplier specific requests
- **0xFF** - not applicable, reserved by ISO 14229-1


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

DiagnosticSessionControl (0x10)
-------------------------------
DiagnosticSessionControl service is used to change diagnostic sessions in the server(s).
In each diagnostic session a different set of diagnostic services (and/or functionalities) is enabled in the server.
Server shall always be in exactly one diagnostic session.


Request Format
``````````````
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x10      | DiagnosticSessionControl                                     | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *diagnosticSessionType*          |   | 7 (b[6-0]) | 0x00-0x7F | Diagnostic Session to enter                                  |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x00: reserved                                               |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x01: defaultSession                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x02: programmingSession                                     |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x03: extendedDiagnosticSession                              |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x04: safetySystemDiagnosticSession                          |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x05–0x3F: reserved                                          |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x40–0x5F: vehicle manufacturer specific                     |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x60–0x7E: system supplier specific                          |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x7F: reserved                                               |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
````````````````````````
:ref:`P2Server_max <knowledge-base-p2-server>` field is provided directly in milliseconds.

:ref:`P2*Server_max <knowledge-base-p2*-server>` field is encoded in units of 10 ms, so it must be multiplied by 10
to obtain the value in milliseconds.

+-------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------------+---------+
| Name                                                        | Bit Length         | Value         | Description                                                     | Present |
+=============================================================+====================+===============+=================================================================+=========+
| *RSID*                                                      | 8                  | 0x50          | DiagnosticSessionControl                                        | Always  |
+--------------------------+----------------------------------+----+---------------+---------------+-----------------------------------------------------------------+---------+
| *SubFunction*            | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])      | 0x0-0x1       | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always  |
|                          +----------------------------------+    +---------------+---------------+-----------------------------------------------------------------+         |
|                          | *diagnosticSessionType*          |    | 7 (b[6-0])    | 0x00-0x7F     | Echo of *diagnosticSessionType* value from the request          |         |
+--------------------------+----------------------------------+----+---------------+---------------+-----------------------------------------------------------------+---------+
| *sessionParameterRecord* | *P2Server_max*                   | 32 | 16 (b[31-16]) | 0x0000-0xFFFF | Maximum P2 value used by the server in this session             | Always  |
|                          +----------------------------------+    +---------------+---------------+-----------------------------------------------------------------+         |
|                          | *P2\*Server_max*                 |    | 16 (b[15-0])  | 0x0000-0xFFFF | Maximum P2\* value used by the server in this session           |         |
+--------------------------+----------------------------------+----+---------------+---------------+-----------------------------------------------------------------+---------+


.. _knowledge-base-service-ecu-reset:

ECUReset (0x11)
---------------
ECUReset service is used by the client to request that the server perform a reset.
The server, after receiving this request, performs the specified type of reset (either before or after transmitting
the positive response).


Request Format
``````````````
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x11      | ECUReset                                                     | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *resetType*                      |   | 7 (b[6-0]) | 0x00-0x7F | Type of reset to perform                                     |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x00: reserved                                               |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x01: hardReset                                              |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x02: keyOffOnReset                                          |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x03: softReset                                              |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x04: enableRapidPowerShutDown                               |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x05: disableRapidPowerShutDown                              |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x06-0x3F: reserved                                          |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x40-0x5F: vehicle manufacturer specific                     |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x60-0x7E: system supplier specific                          |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0x7F: reserved                                               |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
````````````````````````
The *powerDownTime* field defines the minimum time (in seconds) that the server requires to remain powered down before
it can be safely restarted.
A value of :code:`0xFF` indicates that either the time requirement is not available or a failure occurred.

+--------------------------------------------------+----------------+-----------+-----------------------------------------------------------------+-------------------------------------------------------+
| Name                                             | Bit Length     | Value     | Description                                                     | Present                                               |
+==================================================+================+===========+=================================================================+=======================================================+
| *RSID*                                           | 8              | 0x51      | ECUReset                                                        | Always                                                |
+---------------+----------------------------------+---+------------+-----------+-----------------------------------------------------------------+-------------------------------------------------------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                |
|               +----------------------------------+   +------------+-----------+-----------------------------------------------------------------+                                                       |
|               | *resetType*                      |   | 7 (b[6-0]) | 0x00-0x7F | Echo of *resetType* value from the request                      |                                                       |
+---------------+----------------------------------+---+------------+-----------+-----------------------------------------------------------------+-------------------------------------------------------+
| *powerDownTime*                                  | 8              | 0x00-0xFF | Time required by the server to complete the reset sequence      | If *resetType* equals 0x04 (enableRapidPowerShutDown) |
|                                                  |                |           |                                                                 |                                                       |
|                                                  |                |           | 0x00-0xFE: down time in seconds (0-254)                         |                                                       |
|                                                  |                |           |                                                                 |                                                       |
|                                                  |                |           | 0xFF: failure or time unavailable                               |                                                       |
+--------------------------------------------------+----------------+-----------+-----------------------------------------------------------------+-------------------------------------------------------+


.. _knowledge-base-service-clear-diagnostic-information:

ClearDiagnosticInformation (0x14)
---------------------------------
ClearDiagnosticInformation service is used by the client to clear Diagnostic Trouble Codes (DTCs) and related data
stored in one or more server memories.


Request Format
``````````````


ISO 14229-1:2020
''''''''''''''''
The optional *MemorySelection* field is introduced to allow clearing diagnostic information from
a specific DTC memory (e.g. one of the sub-systems).

+-------------------+------------+-------------------+----------------------------------+----------+
| Name              | Bit Length | Value             | Description                      | Present  |
+===================+============+===================+==================================+==========+
| *SID*             | 8          | 0x14              | ClearDiagnosticInformation       | Always   |
+-------------------+------------+-------------------+----------------------------------+----------+
| *groupOfDTC*      | 24         | 0x000000-0xFFFFFF | Group of DTCs to be cleared      | Always   |
|                   |            |                   |                                  |          |
|                   |            |                   | 0xFFFF33: Emissions-system group |          |
|                   |            |                   |                                  |          |
|                   |            |                   | 0xFFFFD0: Safety-system group    |          |
|                   |            |                   |                                  |          |
|                   |            |                   | 0xFFFFFE: VOBD system group      |          |
|                   |            |                   |                                  |          |
|                   |            |                   | 0xFFFFFF: all                    |          |
+-------------------+------------+-------------------+----------------------------------+----------+
| *MemorySelection* | 8          | 0x00-0xFF         | Specifies DTC memory to clear    | Optional |
+-------------------+------------+-------------------+----------------------------------+----------+


ISO 14229-1:2013
''''''''''''''''
+--------------+------------+-------------------+----------------------------------+---------+
| Name         | Bit Length | Value             | Description                      | Present |
+==============+============+===================+==================================+=========+
| *SID*        | 8          | 0x14              | ClearDiagnosticInformation       | Always  |
+--------------+------------+-------------------+----------------------------------+---------+
| *groupOfDTC* | 24         | 0x000000-0xFFFFFF | Group of DTCs to be cleared      | Always  |
|              |            |                   |                                  |         |
|              |            |                   | 0xFFFF33: Emissions-system group |         |
|              |            |                   |                                  |         |
|              |            |                   | 0xFFFFD0: Safety-system group    |         |
|              |            |                   |                                  |         |
|              |            |                   | 0xFFFFFE: VOBD system group      |         |
|              |            |                   |                                  |         |
|              |            |                   | 0xFFFFFF: all                    |         |
+--------------+------------+-------------------+----------------------------------+---------+


Positive Response Format
````````````````````````
+--------+------------+-------+----------------------------+---------+
| Name   | Bit Length | Value | Description                | Present |
+========+============+=======+============================+=========+
| *RSID* | 8          | 0x54  | ClearDiagnosticInformation | Always  |
+--------+------------+-------+----------------------------+---------+


.. _knowledge-base-service-read-dtc-information:

ReadDTCInformation (0x19)
-------------------------
ReadDTCInformation service allows the client to request current
:ref:`Diagnostic Trouble Code (DTC) <knowledge-base-dtc>` information from one or more servers within the vehicle.

ISO 14229-1 defines the following DTC report types (values of the *reportType* parameter):

- 0x01: :ref:`reportNumberOfDTCByStatusMask <knowledge-base-service-read-dtc-information-01>`
- 0x02: :ref:`reportDTCByStatusMask <knowledge-base-service-read-dtc-information-02>`
- 0x03: :ref:`reportDTCSnapshotIdentification <knowledge-base-service-read-dtc-information-03>`
- 0x04: :ref:`reportDTCSnapshotRecordByDTCNumber <knowledge-base-service-read-dtc-information-04>`
- 0x05: :ref:`reportDTCStoredDataByRecordNumber <knowledge-base-service-read-dtc-information-05>`
- 0x06: :ref:`reportDTCExtDataRecordByDTCNumber <knowledge-base-service-read-dtc-information-06>`
- 0x07: :ref:`reportNumberOfDTCBySeverityMaskRecord <knowledge-base-service-read-dtc-information-07>`
- 0x08: :ref:`reportDTCBySeverityMaskRecord <knowledge-base-service-read-dtc-information-08>`
- 0x09: :ref:`reportSeverityInformationOfDTC <knowledge-base-service-read-dtc-information-09>`
- 0x0A: :ref:`reportSupportedDTC <knowledge-base-service-read-dtc-information-0A>`
- 0x0B: :ref:`reportFirstTestFailedDTC <knowledge-base-service-read-dtc-information-0B>`
- 0x0C: :ref:`reportFirstConfirmedDTC <knowledge-base-service-read-dtc-information-0C>`
- 0x0D: :ref:`reportMostRecentTestFailedDTC <knowledge-base-service-read-dtc-information-0D>`
- 0x0E: :ref:`reportMostRecentConfirmedDTC <knowledge-base-service-read-dtc-information-0E>`
- 0x0F: :ref:`reportMirrorMemoryDTCByStatusMask <knowledge-base-service-read-dtc-information-0F>`
  (withdrawn in ISO 14229-1:2020)
- 0x10: :ref:`reportMirrorMemoryDTCExtDataRecordByDTCNumber <knowledge-base-service-read-dtc-information-10>`
  (withdrawn in ISO 14229-1:2020)
- 0x11: :ref:`reportNumberOfMirrorMemoryDTCByStatusMask <knowledge-base-service-read-dtc-information-11>`
  (withdrawn in ISO 14229-1:2020)
- 0x12: :ref:`reportNumberOfEmissionsOBDDTCByStatusMask <knowledge-base-service-read-dtc-information-12>`
  (withdrawn in ISO 14229-1:2020)
- 0x13: :ref:`reportEmissionsOBDDTCByStatusMask <knowledge-base-service-read-dtc-information-13>`
  (withdrawn in ISO 14229-1:2020)
- 0x14: :ref:`reportDTCFaultDetectionCounter <knowledge-base-service-read-dtc-information-14>`
- 0x15: :ref:`reportDTCWithPermanentStatus <knowledge-base-service-read-dtc-information-15>`
- 0x16: :ref:`reportDTCExtDataRecordByRecordNumber <knowledge-base-service-read-dtc-information-16>`
- 0x17: :ref:`reportUserDefMemoryDTCByStatusMask <knowledge-base-service-read-dtc-information-17>`
- 0x18: :ref:`reportUserDefMemoryDTCSnapshotRecordByDTCNumber <knowledge-base-service-read-dtc-information-18>`
- 0x19: :ref:`reportUserDefMemoryDTCExtDataRecordByDTCNumber <knowledge-base-service-read-dtc-information-19>`
- 0x1A: :ref:`reportSupportedDTCExtDataRecord <knowledge-base-service-read-dtc-information-1A>`
  (introduced in ISO 14229-1:2020)
- 0x42: :ref:`reportWWHOBDDTCByMaskRecord <knowledge-base-service-read-dtc-information-42>`
- 0x55: :ref:`reportWWHOBDDTCWithPermanentStatus <knowledge-base-service-read-dtc-information-55>`
- 0x56: :ref:`reportDTCInformationByDTCReadinessGroupIdentifier <knowledge-base-service-read-dtc-information-56>`
  (introduced in ISO 14229-1:2020)


.. _knowledge-base-service-read-dtc-information-01:

reportNumberOfDTCByStatusMask (0x01)
````````````````````````````````````
This sub-function allows the client to request the number of stored :ref:`DTCs <knowledge-base-dtc>`` that match
a specific :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*).
It is typically used as a lightweight mechanism to determine how many DTCs fulfill a given diagnostic condition without
retrieving the DTC values themselves.


Request Format
''''''''''''''
The *DTCStatusMask* parameter specifies which :ref:`DTC Status <knowledge-base-dtc-status>` bits should be used
as a filter when matching :ref:`DTCs <knowledge-base-dtc>`.
A value of 0x00 means that no status bits are selected. Since no DTC can match this by definition, the result will
always be a count of 0.

+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x01      | reportNumberOfDTCByStatusMask                                |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTCs matching                     | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value         | Description                                                     | Present |
+==================================================+================+===============+=================================================================+=========+
| *RSID*                                           | 8              | 0x59          | ReadDTCInformation                                              | Always  |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1       | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always  |
|               +----------------------------------+   +------------+---------------+-----------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x01          | reportNumberOfDTCByStatusMask                                   |         |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *DTCStatusAvailabilityMask*                      | 8              | 0x00-0xFF     | DTC Status bits supported by the server                         | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCFormatIdentifier*                            | 8              | 0x00-0xFF     | DTC Format used by the server                                   | Always  |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x00: SAE J2012-DA DTC Format 00                                |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x01: ISO 14229-1 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x02: SAE J1939-73 DTC Format                                   |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x03: ISO 11992-4 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x04: SAE J2012-DA DTC Format 04                                |         |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCCount*                                       | 16             | 0x0000-0xFFFF | Number of DTCs that match the criteria                          | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-02:

reportDTCByStatusMask (0x02)
````````````````````````````
This sub-function can be used by the client to request a list of all :ref:`DTCs <knowledge-base-dtc>` stored in
the server’s memory that match a specific :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*).
A DTC is included in the response if :code:`DTC Status & DTCStatusMask) != 0`.
This sub-function provides the client with both the DTC values and their corresponding status information for
all DTCs that satisfy the given mask.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x02      | reportDTCByStatusMask                                        |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTCs matching                     | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x02              | reportDTCByStatusMask                                           |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC matches the criteria |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                         |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs matches the criteria  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-03:

reportDTCSnapshotIdentification (0x03)
``````````````````````````````````````
This sub-function can be used by the client to request identification numbers of all stored DTC snapshot records.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+---------+
|               | *reportType*                     |   | 7 (b[6-0]) | 0x03    | reportDTCSnapshotIdentification                              | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| Name                                                                 | Bit Length        | Value             | Description                                                     | Present                                          |
+======================================================================+===================+===================+=================================================================+==================================================+
| *RSID*                                                               | 8                 | 0x59              | ReadDTCInformation                                              | Always                                           |
+-----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| *SubFunction*                     | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                           |
|                                   +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                                  |
|                                   | *reportType*                     |      | 7 (b[6-0]) | 0x03              | reportDTCSnapshotIdentification                                 |                                                  |
+-----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| *DTC and DTCSnapshotRecordNumber* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC Snapshot Record is available |
|                                   +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                                  |
|                                   | *DTCSnapshotRecordNumber*        |      | 8          | 0x00-0xFF         | Number of DTC Snapshot Record reported for DTC#1                |                                                  |
|                                   +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
|                                   | ...                              |      | ...                                                                                                                                                 |
|                                   +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
|                                   | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTC Snapshot Records are available |
|                                   +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                                  |
|                                   | *DTCSnapshotRecordNumber*        |      | 8          | 0x00-0xFF         | Number of DTC Snapshot Record reported for DTC#n                |                                                  |
+-----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-04:

reportDTCSnapshotRecordByDTCNumber (0x04)
`````````````````````````````````````````
This sub-function can be used by the client to request snapshot data for
a specific :ref:`DTC <knowledge-base-dtc>` (*DTC*) and snapshot record number (*DTCSnapshotRecordNumber*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value             | Description                                                  | Present |
+==================================================+================+===================+==============================================================+=========+
| *SID*                                            | 8              | 0x19              | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1           | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 0: response required                                         |         |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-------------------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x04              | reportDTCSnapshotRecordByDTCNumber                           |         |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *DTC*                                            | 24             | 0x000000-0xFFFFFF | DTC number                                                   | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *DTCSnapshotRecordNumber*                        | 8              | 0x00-0xFF         | Number of requested DTC Snapshot Record(s)                   | Always  |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x00: reserved (legislated purposes)                         |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x01-0xFE: specific snapshot record                          |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFF: all snapshot records                                   |         |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                                    |
+========================================================+===================+===================+=================================================================+============================================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                     |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                            |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x04              | reportDTCSnapshotRecordByDTCNumber                              |                                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | Considered DTC                                                  | Always                                                     |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                            |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *DTCSnapshotRecordNumber#1*                            | 8                 | 0x00-0xFF         | Number of DTCSnapshotRecord#1                                   | If at least one DTCSnapshotRecord is available for the DTC |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DIDCount#1*                                           | 8                 | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#1                    |                                                            |
|                                                        |                   |                   | (equals m)                                                      |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_1*                                              | 16                | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshotRecord#1                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_1 data*                                         | multiple of 8     |                   | Data stored under *DID#1_1*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| ...                                                                                                                                                              |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_m*                                              | 16                | 0x0000-0xFFFF     | DID#m that is part of DTCSnapshotRecord#1                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_m data*                                         | multiple of 8     |                   | Data stored under *DID#1_m*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| ...                                                                                                                                                                                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *DTCSnapshotRecordNumber#n*                            | 8                 | 0x00-0xFF         | Number of DTCSnapshotRecord#n                                   | If requested for multiple DTCSnapshotRecords               |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DIDCount#n*                                           | 8                 | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#n                    | AND                                                        |
|                                                        |                   |                   | (equals k)                                                      |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+ at least n DTCSnapshotRecords are available for the DTC    |
| *DID#n_1*                                              | 16                | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshotRecord#n                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#n_1 data*                                         | multiple of 8     |                   | Data stored under *DID#n_1*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| ...                                                                                                                                                              |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#n_k*                                              | 16                | 0x0000-0xFFFF     | DID#k that is part of DTCSnapshotRecord#n                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#n_k data*                                         | multiple of 8     |                   | Data stored under *DID#n_k*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-05:

reportDTCStoredDataByRecordNumber (0x05)
````````````````````````````````````````
This sub-function can be used by the client to request stored data for a specific record (*DTCStoredDataRecordNumber*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x05      | reportDTCStoredDataByRecordNumber                            |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStoredDataRecordNumber*                      | 8              | 0x00-0xFF | Number of requested DTC Stored Data Record(s)                | Always  |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x00: reserved (legislated purposes)                         |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x01–0xFE: specific stored data record                       |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFF: all records                                            |         |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| Name                                                     | Bit Length        | Value             | Description                                                     | Present                                          |
+==========================================================+===================+===================+=================================================================+==================================================+
| *RSID*                                                   | 8                 | 0x59              | ReadDTCInformation                                              | Always                                           |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| *SubFunction*         | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                           |
|                       +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                  |
|                       | *reportType*                     |    | 7 (b[6-0])   | 0x05              | reportDTCStoredDataByRecordNumber                               |                                                  |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| *DTCStoredDataRecordNumber#1*                            | 8                 | 0x00-0xFF         | Number of DTCStoredDataRecord#1                                 | Always                                           |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| *DTC and DTCStatus#1* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC for which DTCStoredDataRecord#1 was reported                | If at least one DTCStoredDataRecord is available |
|                       +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                  |
|                       | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                                  |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DIDCount#1*                                             | 8                 | 0x00-0xFF         | Number of DIDs stored in DTCStoredDataRecord#1                  |                                                  |
|                                                          |                   |                   | (equals m)                                                      |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#1_1*                                                | 16                | 0x0000-0xFFFF     | DID#1 that is part of DTCStoredDataRecord#1                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#1_1 data*                                           | multiple of 8     |                   | Data stored under *DID#1_1*                                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| ...                                                                                                                                                                |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#1_m*                                                | 16                | 0x0000-0xFFFF     | DID#m that is part of *DTCStoredDataRecord#1*                   |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#1_m data*                                           | multiple of 8     |                   | Data stored under *DID#1_m*                                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| ...                                                                                                                                                                                                                   |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+
| *DTCStoredDataRecordNumber#n*                            | 8                 | 0x00-0xFF         | Number of DTCStoredDataRecord#n                                 | If requested for multiple DTCStoredDataRecords   |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DTC and DTCStatus#n* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC for which DTCStoredDataRecord#n was reported                | AND                                              |
|                       +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                  |
|                       | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     | at least n DTCStoredDataRecords are available    |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DIDCount#n*                                             | 8                 | 0x00-0xFF         | Number of DIDs stored in DTCStoredDataRecord#n                  |                                                  |
|                                                          |                   |                   | (equals k)                                                      |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#n_1*                                                | 16                | 0x0000-0xFFFF     | DID#1 that is part of DTCStoredDataRecord#n                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#n_1 data*                                           | multiple of 8     |                   | Data stored under *DID#n_1*                                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| ...                                                                                                                                                                |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#n_k*                                                | 16                | 0x0000-0xFFFF     | DID#n that is part of DTCStoredDataRecord#n                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                  |
| *DID#n_k data*                                           | multiple of 8     |                   | Data stored under *DID#n_k*                                     |                                                  |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-06:

reportDTCExtDataRecordByDTCNumber (0x06)
````````````````````````````````````````
This sub-function can be used by the client to request extended data records for
a specific :ref:`DTC <knowledge-base-dtc>` (*DTC*) and record number (*DTCExtDataRecordNumber*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value             | Description                                                  | Present |
+==================================================+================+===================+==============================================================+=========+
| *SID*                                            | 8              | 0x19              | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1           | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 0: response required                                         |         |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-------------------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x06              | reportDTCExtDataRecordByDTCNumber                            |         |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *DTC*                                            | 24             | 0x000000-0xFFFFFF | DTC for which extended data are requested                    | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *DTCExtDataRecordNumber*                         | 8              | 0x00-0xFF         | Number of requested DTC Extended Data Record(s)              | Always  |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x00: reserved                                               |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x01-0x8F: vehicle manufacturer specific record              |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x90-0x9F: regulated emissions OBD record                    |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xA0-0xEF: regulated record                                  |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xF0-0xFD: reserved                                          |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFE: all regulated emissions OBD records                    |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFF: all extended data records                              |         |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                                   |
+========================================================+===================+===================+=================================================================+===========================================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                                    |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                    |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                           |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x06              | reportDTCExtDataRecordByDTCNumber                               |                                                           |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | Considered DTC                                                  | Always                                                    |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                           |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                                           |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTCExtDataRecordNumber#1*                             | 8                 | 0x00-0xFF         | Number of DTCExtDataRecord#1                                    | If at least one DTCExtDataRecord is available for the DTC |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                           |
| *DTCExtDataRecord#1*                                   | multiple of 8     |                   | Data stored in DTCExtDataRecord#1                               |                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| ...                                                                                                                                                                                                                          |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTCExtDataRecordNumber#n*                             | 8                 | 0x00-0xFF         | Number of DTCExtDataRecord#n                                    | If requested for multiple DTCExtDataRecords               |
|                                                        |                   |                   |                                                                 |                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+ AND                                                       |
| *DTCExtDataRecord#n*                                   | multiple of 8     |                   | Data stored in DTCExtDataRecord#n                               |                                                           |
|                                                        |                   |                   |                                                                 | at least n DTCExtDataRecords are available for the DTC    |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-07:

reportNumberOfDTCBySeverityMaskRecord (0x07)
````````````````````````````````````````````
This sub-function can be used by the client to request the number of :ref:`DTCs <knowledge-base-dtc>` that match
a given :ref:`severity <knowledge-base-dtc-severity>` mask (*DTCSeverityMask*)
and :ref:`status <knowledge-base-dtc-status>`` mask (*DTCStatusMask*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x07      | reportNumberOfDTCBySeverityMaskRecord                        |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCSeverityMask*                                | 8              | 0x00-0xFF | Severity mask to use for DTC matching                        | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTC matching                      | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value         | Description                                                     | Present |
+==================================================+================+===============+=================================================================+=========+
| *RSID*                                           | 8              | 0x59          | ReadDTCInformation                                              | Always  |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1       | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always  |
|               +----------------------------------+   +------------+---------------+-----------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x07          | reportNumberOfDTCBySeverityMaskRecord                           |         |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *DTCStatusAvailabilityMask*                      | 8              | 0x00-0xFF     | DTC Status bits supported by the ECU                            | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCFormatIdentifier*                            | 8              | 0x00-0xFF     | DTC Format used by the server                                   | Always  |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x00: SAE J2012-DA DTC Format 00                                |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x01: ISO 14229-1 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x02: SAE J1939-73 DTC Format                                   |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x03: ISO 11992-4 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x04: SAE J2012-DA DTC Format 04                                |         |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCCount*                                       | 16             | 0x0000-0xFFFF | Number of DTCs that match criteria                              | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-08:

reportDTCBySeverityMaskRecord (0x08)
````````````````````````````````````
This sub-function can be used by the client to request all :ref:`DTCs <knowledge-base-dtc>`` that match
a given :ref:`severity <knowledge-base-dtc-severity>` mask (*DTCSeverityMask*)
and :ref:`status <knowledge-base-dtc-status>`` mask (*DTCStatusMask*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x08      | reportDTCBySeverityMaskRecord                                |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCSeverityMask*                                | 8              | 0x00-0xFF | Severity mask to use for DTC matching                        | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTC matching                      | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+-----------------------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*                                       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *reportType*                     |      | 7 (b[6-0]) | 0x08              | reportDTCBySeverityMaskRecord                                   |                                          |
+-----------------------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                                                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+-----------------------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus* | *DTCSeverity*                    | 48*n | 8          | 0x00-0xFF         | Severity of DTC#1                                               | If at least one DTC matches the criteria |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *DTCFunctionalUnit*              |      | 8          | 0x00-0xFF         | Functional Unit of DTC#1                                        |                                          |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#1                                                           |                                          |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                                                     | ...                              |      | ...                                                                                                                                         |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                                                     | *DTCSeverity*                    |      | 8          | 0x00-0xFF         | Severity of DTC#n                                               | If at least n DTCs matches the criteria  |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *DTCFunctionalUnit*              |      | 8          | 0x00-0xFF         | Functional Unit of DTC#n                                        |                                          |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           |                                          |
|                                                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+-----------------------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-09:

reportSeverityInformationOfDTC (0x09)
`````````````````````````````````````
This sub-function can be used by the client to request severity and functional unit information for
a specific :ref:`DTC <knowledge-base-dtc>` (*DTC*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value             | Description                                                  | Present |
+==================================================+================+===================+==============================================================+=========+
| *SID*                                            | 8              | 0x19              | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1           | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 0: response required                                         |         |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-------------------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x09              | reportSeverityInformationOfDTC                               |         |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *DTC*                                            | 24             | 0x000000-0xFFFFFF | DTC number                                                   | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------+
| Name                                                                                   | Bit Length        | Value             | Description                                                     | Present                      |
+========================================================================================+===================+===================+=================================================================+==============================+
| *RSID*                                                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                       |
+-----------------------------------------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------+
| *SubFunction*                                       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                       |
|                                                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                              |
|                                                     | *reportType*                     |    | 7 (b[6-0])   | 0x09              | reportSeverityInformationOfDTC                                  |                              |
+-----------------------------------------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------+
| *DTCStatusAvailabilityMask*                                                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                       |
+-----------------------------------------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------+
| *DTCSeverity, DTCFunctionalUnit, DTC and DTCStatus* | *DTCSeverity*                    | 48 | 8 (b[47-40)  | 0x00-0xFF         | Severity of the *DTC*                                           | If provided DTC is supported |
|                                                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                              |
|                                                     | *DTCFunctionalUnit*              |    | 8 (b[39-32]) | 0x00-0xFF         | Functional Unit of the *DTC*                                    |                              |
|                                                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                              |
|                                                     | *DTC*                            |    | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC number                                                      |                              |
|                                                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                              |
|                                                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                              |
+-----------------------------------------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------+


.. _knowledge-base-service-read-dtc-information-0A:

reportSupportedDTC (0x0A)
`````````````````````````
This sub-function can be used by the client to request a list of all :ref:`DTCs <knowledge-base-dtc>`
supported by the server.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x0A    | reportSupportedDTC                                           |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                          |
+========================================================+===================+===================+=================================================================+==================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                           |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                           |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                  |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x0A              | reportSupportedDTCs                                             |                                  |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                           |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC is supported |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                  |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+----------------------------------+
|                     | ...                              |      | ...                                                                                                                                 |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+----------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs are supported |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                  |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                  |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+


.. _knowledge-base-service-read-dtc-information-0B:

reportFirstTestFailedDTC (0x0B)
```````````````````````````````
This sub-function can be used by the client to request the first :ref:`DTC <knowledge-base-dtc>` that
failed a test (had **testFailed** :ref:`DTC Status <knowledge-base-dtc-status>` bit set) since
the last :ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x0B    | reportFirstTestFailedDTC                                     |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                    |
+========================================================+===================+===================+=================================================================+============================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                     |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x0B              | reportFirstTestFailedDTC                                        |                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC number                                                      | If testFailed was set for at least one DTC |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0C:

reportFirstConfirmedDTC (0x0C)
``````````````````````````````
This sub-function can be used by the client to request the first confirmed :ref:`DTC <knowledge-base-dtc>`
(had **confirmedDTC** :ref:`DTC Status <knowledge-base-dtc-status>` bit set) since
the last :ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x0C    | reportFirstConfirmedDTC                                      |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                      |
+========================================================+===================+===================+=================================================================+==============================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                       |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                       |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                              |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x0C              | reportFirstConfirmedDTC                                         |                                              |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                       |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC number                                                      | If confirmedDTC was set for at least one DTC |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                              |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                              |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0D:

reportMostRecentTestFailedDTC (0x0D)
````````````````````````````````````
This sub-function can be used by the client to request the most recent :ref:`DTC <knowledge-base-dtc>` that
failed a test (had **testFailed** :ref:`DTC Status <knowledge-base-dtc-status>` bit set) since
the last :ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x0D    | reportMostRecentTestFailedDTC                                |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                    |
+========================================================+===================+===================+=================================================================+============================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                     |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x0D              | reportMostRecentTestFailedDTC                                   |                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC number                                                      | If testFailed was set for at least one DTC |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0E:

reportMostRecentConfirmedDTC (0x0E)
```````````````````````````````````
This sub-function can be used by the client to request the most recent confirmed :ref:`DTC <knowledge-base-dtc>`
(had **confirmedDTC** :ref:`DTC Status <knowledge-base-dtc-status>` bit set) since
the last :ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x0E    | reportMostRecentConfirmedDTC                                 |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                      |
+========================================================+===================+===================+=================================================================+==============================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                       |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                       |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                              |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x0E              | reportMostRecentConfirmedDTC                                    |                                              |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                       |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC number                                                      | If confirmedDTC was set for at least one DTC |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                              |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                              |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0F:

reportMirrorMemoryDTCByStatusMask (0x0F)
````````````````````````````````````````
This sub-function can be used by the client to request all :ref:`DTCs <knowledge-base-dtc>` in the DTC mirror memory
that match a given :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x0F      | reportMirrorMemoryDTCByStatusMask                            |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTC matching                      | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x0F              | reportMirrorMemoryDTCByStatusMask                               |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC matches the criteria |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                         |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs matches the criteria  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-10:

reportMirrorMemoryDTCExtDataRecordByDTCNumber (0x10)
````````````````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*) for
a specific :ref:`DTC <knowledge-base-dtc>` (*DTC*) from the DTC mirror memory.

.. warning:: Withdrawn in ISO 14229-1:2020

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value             | Description                                                  | Present |
+==================================================+================+===================+==============================================================+=========+
| *SID*                                            | 8              | 0x19              | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1           | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 0: response required                                         |         |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-------------------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x10              | reportMirrorMemoryDTCExtDataRecordByDTCNumber                |         |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *DTC*                                            | 24             | 0x000000-0xFFFFFF | DTC for which extended data are requested                    | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *DTCExtDataRecordNumber*                         | 8              | 0x00-0xFF         | Number of requested DTC Extended Data Record(s)              | Always  |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x00: reserved                                               |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x01-0x8F: vehicle manufacturer specific record              |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x90-0x9F: regulated emissions OBD record                    |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xA0-0xEF: regulated record                                  |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xF0-0xFD: reserved                                          |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFE: all regulated emissions OBD records                    |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFF: all extended data records                              |         |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                                   |
+========================================================+===================+===================+=================================================================+===========================================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                                    |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                    |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                           |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x10              | reportMirrorMemoryDTCExtDataRecordByDTCNumber                   |                                                           |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | Considered DTC                                                  | Always                                                    |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                           |
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     |                                                           |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTCExtDataRecordNumber#1*                             | 8                 | 0x00-0xFF         | Number of DTCExtDataRecord#1                                    | If at least one DTCExtDataRecord is available for the DTC |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                           |
| *DTCExtDataRecord#1*                                   | multiple of 8     |                   | Data stored in DTCExtDataRecord#1                               |                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| ...                                                                                                                                                                                                                          |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTCExtDataRecordNumber#n*                             | 8                 | 0x00-0xFF         | Number of DTCExtDataRecord#n                                    | If requested for multiple DTCExtDataRecords               |
|                                                        |                   |                   |                                                                 |                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+ AND                                                       |
| *DTCExtDataRecord#n*                                   | multiple of 8     |                   | Data stored in DTCExtDataRecord#n                               |                                                           |
|                                                        |                   |                   |                                                                 | at least n DTCExtDataRecords are available for the DTC    |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-11:

reportNumberOfMirrorMemoryDTCByStatusMask (0x11)
````````````````````````````````````````````````
This sub-function can be used by the client to request the number of :ref:`DTCs <knowledge-base-dtc>` in
the DTC mirror memory that match a given :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x11      | reportNumberOfMirrorMemoryDTCByStatusMask                    |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTCs matching                     | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value         | Description                                                     | Present |
+==================================================+================+===============+=================================================================+=========+
| *RSID*                                           | 8              | 0x59          | ReadDTCInformation                                              | Always  |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1       | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always  |
|               +----------------------------------+   +------------+---------------+-----------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x11          | reportNumberOfMirrorMemoryDTCByStatusMask                       |         |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *DTCStatusAvailabilityMask*                      | 8              | 0x00-0xFF     | DTC Status bits supported by the server                         | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCFormatIdentifier*                            | 8              | 0x00-0xFF     | DTC Format used by the server                                   | Always  |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x00: SAE J2012-DA DTC Format 00                                |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x01: ISO 14229-1 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x02: SAE J1939-73 DTC Format                                   |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x03: ISO 11992-4 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x04: SAE J2012-DA DTC Format 04                                |         |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCCount*                                       | 16             | 0x0000-0xFFFF | Number of DTCs that match the criteria                          | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-12:

reportNumberOfEmissionsOBDDTCByStatusMask (0x12)
````````````````````````````````````````````````
This sub-function can be used by the client to request the number of emissions-related OBD
:ref:`DTCs <knowledge-base-dtc>` that match a given :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x12      | reportNumberOfEmissionsOBDDTCByStatusMask                    |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTC matching                      | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value         | Description                                                     | Present |
+==================================================+================+===============+=================================================================+=========+
| *RSID*                                           | 8              | 0x59          | ReadDTCInformation                                              | Always  |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1       | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always  |
|               +----------------------------------+   +------------+---------------+-----------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x12          | reportNumberOfEmissionsOBDDTCByStatusMask                       |         |
+---------------+----------------------------------+---+------------+---------------+-----------------------------------------------------------------+---------+
| *DTCStatusAvailabilityMask*                      | 8              | 0x00-0xFF     | DTC Status bits supported by the server                         | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCFormatIdentifier*                            | 8              | 0x00-0xFF     | DTC Format used by the server                                   | Always  |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x00: SAE J2012-DA DTC Format 00                                |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x01: ISO 14229-1 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x02: SAE J1939-73 DTC Format                                   |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x03: ISO 11992-4 DTC Format                                    |         |
|                                                  |                |               |                                                                 |         |
|                                                  |                |               | 0x04: SAE J2012-DA DTC Format 04                                |         |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+
| *DTCCount*                                       | 16             | 0x0000-0xFFFF | Number of DTCs that match the criteria                          | Always  |
+--------------------------------------------------+----------------+---------------+-----------------------------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-13:

reportEmissionsOBDDTCByStatusMask (0x13)
````````````````````````````````````````
This sub-function can be used by the client to request a list of emissions-related OBD :ref:`DTCs <knowledge-base-dtc>`
that match a given :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x13      | reportEmissionsOBDDTCByStatusMask                            |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTCs matching                     | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x13              | reportEmissionsOBDDTCByStatusMask                               |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC matches the criteria |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                         |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs matches the criteria  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-14:

reportDTCFaultDetectionCounter (0x14)
`````````````````````````````````````
This sub-function can be used by the client to request
:ref:`fault detection counters <knowledge-base-dtc-fault-detection-counter>` for :ref:`DTCs <knowledge-base-dtc>`
that have not been reported or confirmed (no :ref:`DTC Status <knowledge-base-dtc-status>` bits set).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x14    | reportDTCFaultDetectionCounter                               |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-----------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+----------------------------------------------------------------------+
| Name                                                                  | Bit Length        | Value             | Description                                                     | Present                                                              |
+=======================================================================+===================+===================+=================================================================+======================================================================+
| *RSID*                                                                | 8                 | 0x59              | ReadDTCInformation                                              | Always                                                               |
+------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------------------------------------------+
| *SubFunction*                      | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                               |
|                                    +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                                                      |
|                                    | *reportType*                     |      | 7 (b[6-0]) | 0x14              | reportDTCFaultDetectionCounter                                  |                                                                      |
+------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------------------------------------------+
| *DTC and DTCFaultDetectionCounter* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC has positive value of *DTCFaultDetectionCounter* |
|                                    +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                                                      |
|                                    | *DTCFaultDetectionCounter*       |      | 8          | 0x00-0xFF         | Value of fault detection counter for DTC#1                      |                                                                      |
|                                    +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+----------------------------------------------------------------------+
|                                    | ...                              |      | ...                                                                                                                                                                     |
|                                    +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+----------------------------------------------------------------------+
|                                    | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs has positive value of *DTCFaultDetectionCounter*  |
|                                    +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                                                      |
|                                    | *DTCFaultDetectionCounter*       |      | 8          | 0x00-0xFF         | Value of fault detection counter for DTC#n                      |                                                                      |
+------------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-15:

reportDTCWithPermanentStatus (0x15)
```````````````````````````````````
This sub-function can be used by the client to request a list of :ref:`DTCs <knowledge-base-dtc>` with permanent status
(once reported, never cleared or healed).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+---------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value   | Description                                                  | Present |
+==================================================+================+=========+==============================================================+=========+
| *SID*                                            | 8              | 0x19    | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1 | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 0: response required                                         |         |
|               |                                  |   |            |         |                                                              |         |
|               |                                  |   |            |         | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+---------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x15    | reportDTCWithPermanentStatus                                 |         |
+---------------+----------------------------------+---+------------+---------+--------------------------------------------------------------+---------+

Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                          |
+========================================================+===================+===================+=================================================================+==================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                           |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                           |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                  |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x15              | reportDTCWithPermanentStatus                                    |                                  |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                           |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC is supported |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                  |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+----------------------------------+
|                     | ...                              |      | ...                                                                                                                                 |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+----------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs are supported |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                  |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                  |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+----------------------------------+


.. _knowledge-base-service-read-dtc-information-16:

reportDTCExtDataRecordByRecordNumber (0x16)
```````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*)
regardless of the DTC number.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x16      | reportDTCExtDataRecordByRecordNumber                         |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCExtDataRecordNumber*                         | 8              | 0x00-0xFF | Number of requested DTC Extended Data Record(s)              | Always  |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x00: reserved                                               |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x01-0x8F: vehicle manufacturer specific record              |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x90-0x9F: regulated emissions OBD record                    |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xA0-0xEF: regulated record                                  |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xF0-0xFD: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFE: all regulated emissions OBD records                    |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFF: all extended data records                              |         |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+
| Name                                                     | Bit Length        | Value             | Description                                                     | Present                                       |
+==========================================================+===================+===================+=================================================================+===============================================+
| *RSID*                                                   | 8                 | 0x59              | ReadDTCInformation                                              | Always                                        |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+
| *SubFunction*         | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                        |
|                       +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                               |
|                       | *reportType*                     |    | 7 (b[6-0])   | 0x16              | reportDTCExtDataRecordByRecordNumber                            |                                               |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+
| *DTCExtDataRecordNumber*                                 | 8                 | 0x00-0xEF         | Identification number of DTCExtDataRecord                       | Always                                        |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+
| *DTC and DTCStatus#1* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTCExtDataRecord is available |
|                       +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                               |
|                       | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Status of DTC#1                                                 |                                               |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+                                               |
| *DTCExtDataRecord#1*                                     | multiple of 8     |                   | Extended Data #1                                                |                                               |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+
| ...                                                                                                                                                                                                                |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+
| *DTC and DTCStatus#n* | *DTC*                            | 32 | 24 (b[31-8]) | 0x00-0xFF         | DTC#n                                                           | If at least n DTCExtDataRecords are available |
|                       +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                               |
|                       | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Status of DTC#n                                                 |                                               |
+-----------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+                                               |
| *DTCExtDataRecord#n*                                     | multiple of 8     |                   | Extended Data #n                                                |                                               |
+----------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-17:

reportUserDefMemoryDTCByStatusMask (0x17)
`````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs that match a given
:ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*) in a selected memory (*MemorySelection*).

*MemorySelection* allows reading DTC related information from a specific DTC memory (e.g. one of the sub-systems).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x17      | reportUserDefMemoryDTCByStatusMask                           |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTCs matching                     | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| *MemorySelection*                                | 8              | 0x00-0xFF | Specifies DTC memory                                         | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x17              | reportUserDefMemoryDTCByStatusMask]                             |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *MemorySelection*                                      | 8                 | 0x00-0xFF         | Echo of *MemorySelection* value from the request                | Always                                   |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC matches the criteria |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                         |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs matches the criteria  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-18:

reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
``````````````````````````````````````````````````````
This sub-function can be used by the client to request snapshot records (*DTCSnapshotRecordNumber*) for
a specific :ref:`DTC <knowledge-base-dtc>` (*DTC*) in a selected memory (*MemorySelection*).

*MemorySelection* allows reading DTC related information from a specific DTC memory (e.g. one of the sub-systems).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value             | Description                                                  | Present |
+==================================================+================+===================+==============================================================+=========+
| *SID*                                            | 8              | 0x19              | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1           | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 0: response required                                         |         |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-------------------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x18              | reportUserDefMemoryDTCSnapshotRecordByDTCNumber              |         |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *DTC*                                            | 24             | 0x000000-0xFFFFFF | DTC number                                                   | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *DTCSnapshotRecordNumber*                        | 8              | 0x00-0xFF         | Number of requested DTC Snapshot Record(s)                   | Always  |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x00: reserved (legislated purposes)                         |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x01-0xFE: specific snapshot record                          |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFF: all snapshot records                                   |         |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *MemorySelection*                                | 8              | 0x00-0xFF         | Specifies DTC memory                                         | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                                    |
+========================================================+===================+===================+=================================================================+============================================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                     |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                            |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x18              | reportUserDefMemoryDTCSnapshotRecordByDTCNumber                 |                                                            |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *MemorySelection*                                      | 8                 | 0x00-0xFF         | Echo of *MemorySelection* value from the request                | Always                                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | Considered DTC                                                  | Always                                                     |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     | Always                                                     |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *DTCSnapshotRecordNumber#1*                            | 8                 | 0x00-0xFF         | Number of DTCSnapshotRecord#1                                   | If at least one DTCSnapshotRecord is available for the DTC |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DIDCount#1*                                           | 8                 | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#1                    |                                                            |
|                                                        |                   |                   | (equals m)                                                      |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_1*                                              | 16                | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshotRecord#1                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_1 data*                                         | multiple of 8     |                   | Data stored under *DID#1_1*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| ...                                                                                                                                                              |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_m*                                              | 16                | 0x0000-0xFFFF     | DID#m that is part of DTCSnapshotRecord#1                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#1_m data*                                         | multiple of 8     |                   | Data stored under *DID#1_m*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| ...                                                                                                                                                                                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+
| *DTCSnapshotRecordNumber#n*                            | 8                 | 0x00-0xFF         | Number of DTCSnapshotRecord#n                                   | If requested for multiple DTCSnapshotRecords               |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DIDCount#n*                                           | 8                 | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#n                    | AND                                                        |
|                                                        |                   |                   | (equals k)                                                      |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+ at least n DTCSnapshotRecords are available for the DTC    |
| *DID#n_1*                                              | 16                | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshotRecord#n                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#n_1 data*                                         | multiple of 8     |                   | Data stored under *DID#n_1*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| ...                                                                                                                                                              |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#n_k*                                              | 16                | 0x0000-0xFFFF     | DID#k that is part of DTCSnapshotRecord#n                       |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                            |
| *DID#n_k data*                                         | multiple of 8     |                   | Data stored under *DID#n_k*                                     |                                                            |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-19:

reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
`````````````````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*) for
a specific :ref:`DTC <knowledge-base-dtc>` (*DTCMaskRecord*) in a selected memory (*MemorySelection*).

*MemorySelection* allows reading DTC related information from a specific DTC memory (e.g. one of the sub-systems).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value             | Description                                                  | Present |
+==================================================+================+===================+==============================================================+=========+
| *SID*                                            | 8              | 0x19              | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1           | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 0: response required                                         |         |
|               |                                  |   |            |                   |                                                              |         |
|               |                                  |   |            |                   | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-------------------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x19              | reportUserDefMemoryDTCExtDataRecordByDTCNumber               |         |
+---------------+----------------------------------+---+------------+-------------------+--------------------------------------------------------------+---------+
| *DTC*                                            | 24             | 0x000000-0xFFFFFF | DTC for which extended data are requested                    | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *DTCExtDataRecordNumber*                         | 8              | 0x00-0xFF         | Number of requested DTC Extended Data Record(s)              | Always  |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x00: reserved                                               |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x01-0x8F: vehicle manufacturer specific record              |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0x90-0x9F: regulated emissions OBD record                    |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xA0-0xEF: regulated record                                  |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xF0-0xFD: reserved                                          |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFE: all regulated emissions OBD records                    |         |
|                                                  |                |                   |                                                              |         |
|                                                  |                |                   | 0xFF: all extended data records                              |         |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+
| *MemorySelection*                                | 8              | 0x00-0xFF         | Specifies DTC memory                                         | Always  |
+--------------------------------------------------+----------------+-------------------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                                   |
+========================================================+===================+===================+=================================================================+===========================================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                                    |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8  | 1 (b[7])     | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                                    |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+                                                           |
|                     | *reportType*                     |    | 7 (b[6-0])   | 0x19              | reportUserDefMemoryDTCExtDataRecordByDTCNumber                  |                                                           |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *MemorySelection*                                      | 8                 | 0x00-0xFF         | Echo of *MemorySelection* value from the request                | Always                                                    |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32 | 24 (b[31-8]) | 0x000000-0xFFFFFF | Considered DTC                                                  | Always                                                    |
|                     +----------------------------------+    +--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
|                     | *DTCStatus*                      |    | 8 (b[7-0])   | 0x00-0xFF         | Current status of the *DTC*                                     | Always                                                    |
+---------------------+----------------------------------+----+--------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTCExtDataRecordNumber#1*                             | 8                 | 0x00-0xFF         | Number of DTCExtDataRecord#1                                    | If at least one DTCExtDataRecord is available for the DTC |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+                                                           |
| *DTCExtDataRecord#1*                                   | multiple of 8     |                   | Data stored in DTCExtDataRecord#1                               |                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| ...                                                                                                                                                                                                                          |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+
| *DTCExtDataRecordNumber#n*                             | 8                 | 0x00-0xFF         | Number of DTCExtDataRecord#n                                    | If requested for multiple DTCExtDataRecords               |
|                                                        |                   |                   |                                                                 |                                                           |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+ AND                                                       |
| *DTCExtDataRecord#n*                                   | multiple of 8     |                   | Data stored in DTCExtDataRecord#n                               |                                                           |
|                                                        |                   |                   |                                                                 | at least n DTCExtDataRecords are available for the DTC    |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+-----------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-1A:

reportSupportedDTCExtDataRecord (0x1A)
``````````````````````````````````````
This sub-function can be used by the client to request the list of :ref:`DTCs <knowledge-base-dtc>` that support
a given extended data record number (*DTCExtDataRecordNumber*).

.. warning:: Introduced in ISO 14229-1:2020


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x1A      | reportSupportedDTCExtDataRecord                              |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *DTCExtDataRecordNumber*                         | 8              | 0x00-0xFD | Number of requested DTC Extended Data Record                 | Always  |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x00: reserved                                               |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x01-0x8F: vehicle manufacturer specific record              |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x90-0x9F: regulated emissions OBD record                    |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xA0-0xEF: regulated record                                  |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xF0-0xFD: reserved                                          |         |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                    |
+========================================================+===================+===================+=================================================================+============================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                     |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                     |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x1A              | reportSupportedDTCExtDataRecord                                 |                                            |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                     |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTCExtDataRecordNumber*                               | 8                 | 0x00-0xFD         | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                     |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC supports ExtDataRecord |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                            |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                           |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs supports ExtDataRecord  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                            |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                            |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+--------------------------------------------+


.. _knowledge-base-service-read-dtc-information-42:

reportWWHOBDDTCByMaskRecord (0x42)
``````````````````````````````````
This sub-function can be used by the client to request WWH-OBD :ref:`DTCs <knowledge-base-dtc-status>` and
their associated :ref:`status <knowledge-base-dtc-status>` and :ref:`severity information <knowledge-base-dtc-severity>`,
filtered by a :ref:`status <knowledge-base-dtc-status>` mask (*DTCStatusMask*) and
a :ref:`severity <knowledge-base-dtc-severity>` mask (*DTCSeverityMaskRecord*).


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x42      | reportWWHOBDDTCByMaskRecord                                  |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *FunctionalGroupIdentifier*                      | 8              | 0x00-0xFF | Functional group to use for DTC matching                     | Always  |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x00-0x32: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x33: emissions-system group                                 |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x34-0xCF: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xD0: safety-system group                                    |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xD1-0xDF: legislative system group                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xE0-0xFD: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFE: VOBD system                                            |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFF: reserved                                               |         |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| *DTCSeverityMaskRecord*                          | 8              | 0x00-0xFF | DTC severity mask to use for DTC matching                    | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| *DTCStatusMask*                                  | 8              | 0x00-0xFF | DTC status mask to use for DTC matching                      | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                                | Bit Length        | Value             | Description                                                     | Present                                  |
+=====================================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                              | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*                    | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                  | *reportType*                     |      | 7 (b[6-0]) | 0x42              | reportWWHOBDDTCByMaskRecord                                     |                                          |
+----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *FunctionalGroupIdentifier*                                         | 8                 | 0x00-0xFF         | Echo of *FunctionalGroupIdentifier* value from the request      | Always                                   |
+---------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                                         | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+---------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCSeverityAvailabilityMask*                                       | 8                 | 0x00-0xFF         | DTC Severity bits supported by the ECU                          | Always                                   |
+---------------------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCFormatIdentifier*                                               | 8                 | 0x00-0xFF         | DTC Format used by the server                                   | Always                                   |
|                                                                     |                   |                   |                                                                 |                                          |
|                                                                     |                   |                   | 0x00: SAE J2012-DA DTC Format 00                                |                                          |
|                                                                     |                   |                   |                                                                 |                                          |
|                                                                     |                   |                   | 0x01: ISO 14229-1 DTC Format                                    |                                          |
|                                                                     |                   |                   |                                                                 |                                          |
|                                                                     |                   |                   | 0x02: SAE J1939-73 DTC Format                                   |                                          |
|                                                                     |                   |                   |                                                                 |                                          |
|                                                                     |                   |                   | 0x03: ISO 11992-4 DTC Format                                    |                                          |
|                                                                     |                   |                   |                                                                 |                                          |
|                                                                     |                   |                   | 0x04: SAE J2012-DA DTC Format 04                                |                                          |
+----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCSeverity, DTC and DTCStatus* | *DTCSeverity*                    | 40*n | 8          | 0x00-0xFF         | Severity of DTC#1                                               | If at least one DTC matches the criteria |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                  | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#1                                                           |                                          |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                  | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                                  | ...                              |      | ...                                                                                                                                         |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                                  | *DTCSeverity*                    |      | 8          | 0x00-0xFF         | Severity of DTC#n                                               | If at least n DTCs matches the criteria  |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                  | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           |                                          |
|                                  +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                                  | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+----------------------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-55:

reportWWHOBDDTCWithPermanentStatus (0x55)
`````````````````````````````````````````
This sub-function can be used by the client to request WWH-OBD :ref:`DTCs <knowledge-base-dtc>` with permanent status.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x55      | reportWWHOBDDTCWithPermanentStatus                           |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *FunctionalGroupIdentifier*                      | 8              | 0x00-0xFF | Functional group to use for DTC matching                     | Always  |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x00-0x32: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x33: emissions-system group                                 |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x34-0xCF: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xD0: safety-system group                                    |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xD1-0xDF: legislative system group                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xE0-0xFD: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFE: VOBD system                                            |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFF: reserved                                               |         |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x55              | reportWWHOBDDTCWithPermanentStatus                              |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *FunctionalGroupIdentifier*                            | 8                 | 0x00-0xFF         | Echo of *FunctionalGroupIdentifier* value from the request      | Always                                   |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCFormatIdentifier*                                  | 8                 | 0x00-0xFF         | DTC Format used by the server                                   | Always                                   |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x00: SAE J2012-DA DTC Format 00                                |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x01: ISO 14229-1 DTC Format                                    |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x02: SAE J1939-73 DTC Format                                   |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x03: ISO 11992-4 DTC Format                                    |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x04: SAE J2012-DA DTC Format 04                                |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC matches the criteria |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                         |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs matches the criteria  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-56:

reportDTCInformationByDTCReadinessGroupIdentifier (0x56)
````````````````````````````````````````````````````````
This sub-function can be used by the client to request OBD :ref:`DTCs <knowledge-base-dtc>` that belong to
a given :ref:`readiness group <knowledge-base-dtc-readiness-group>` (*DTCReadinessGroupIdentifier*).

.. warning:: Introduced in ISO 14229-1:2020

.. note:: `SAE J1979-DA <https://www.sae.org/standards/j1979da_202203-j1979-da-digital-annex-e-e-diagnostic-test-modes>`_
  defines values mapping for *DTCReadinessGroupIdentifier* parameter.


Request Format
''''''''''''''
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| Name                                             | Bit Length     | Value     | Description                                                  | Present |
+==================================================+================+===========+==============================================================+=========+
| *SID*                                            | 8              | 0x19      | ReadDTCInformation                                           | Always  |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 8 | 1 (b[7])   | 0x0-0x1   | Information for the server whether to send positive response | Always  |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 0: response required                                         |         |
|               |                                  |   |            |           |                                                              |         |
|               |                                  |   |            |           | 1: suppress positive response                                |         |
|               +----------------------------------+   +------------+-----------+--------------------------------------------------------------+         |
|               | *reportType*                     |   | 7 (b[6-0]) | 0x56      | reportDTCInformationByDTCReadinessGroupIdentifier            |         |
+---------------+----------------------------------+---+------------+-----------+--------------------------------------------------------------+---------+
| *FunctionalGroupIdentifier*                      | 8              | 0x00-0xFF | Functional group to use for DTC matching                     | Always  |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x00-0x32: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x33: emissions-system group                                 |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0x34-0xCF: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xD0: safety-system group                                    |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xD1-0xDF: legislative system group                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xE0-0xFD: reserved                                          |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFE: VOBD system                                            |         |
|                                                  |                |           |                                                              |         |
|                                                  |                |           | 0xFF: reserved                                               |         |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+
| *DTCReadinessGroupIdentifier*                    | 8              | 0x00-0xFF | Specifies DTC readiness group                                | Always  |
+--------------------------------------------------+----------------+-----------+--------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| Name                                                   | Bit Length        | Value             | Description                                                     | Present                                  |
+========================================================+===================+===================+=================================================================+==========================================+
| *RSID*                                                 | 8                 | 0x59              | ReadDTCInformation                                              | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *SubFunction*       | *suppressPosRspMsgIndicationBit* | 8    | 1 (b[7])   | 0x0-0x1           | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always                                   |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *reportType*                     |      | 7 (b[6-0]) | 0x56              | reportDTCInformationByDTCReadinessGroupIdentifier               |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *FunctionalGroupIdentifier*                            | 8                 | 0x00-0xFF         | Echo of *FunctionalGroupIdentifier* value from the request      | Always                                   |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCStatusAvailabilityMask*                            | 8                 | 0x00-0xFF         | DTC Status bits supported by the ECU                            | Always                                   |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCFormatIdentifier*                                  | 8                 | 0x00-0xFF         | DTC Format used by the server                                   | Always                                   |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x00: SAE J2012-DA DTC Format 00                                |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x01: ISO 14229-1 DTC Format                                    |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x02: SAE J1939-73 DTC Format                                   |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x03: ISO 11992-4 DTC Format                                    |                                          |
|                                                        |                   |                   |                                                                 |                                          |
|                                                        |                   |                   | 0x04: SAE J2012-DA DTC Format 04                                |                                          |
+--------------------------------------------------------+-------------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTCReadinessGroupIdentifier*                          | 8                 | 0x00-0xFF         | Echo of *DTCReadinessGroupIdentifier* value from the request    | Always                                   |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
| *DTC and DTCStatus* | *DTC*                            | 32*n | 24         | 0x000000-0xFFFFFF | DTC#1                                                           | If at least one DTC matches the criteria |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#1                                                 |                                          |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | ...                              |      | ...                                                                                                                                         |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+------------------------------------------+
|                     | *DTC*                            |      | 24         | 0x000000-0xFFFFFF | DTC#n                                                           | If at least n DTCs matches the criteria  |
|                     +----------------------------------+      +------------+-------------------+-----------------------------------------------------------------+                                          |
|                     | *DTCStatus*                      |      | 8          | 0x00-0xFF         | Status of DTC#n                                                 |                                          |
+---------------------+----------------------------------+------+------------+-------------------+-----------------------------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-data-by-identifier:

ReadDataByIdentifier (0x22)
---------------------------
ReadDataByIdentifier service allows the client to request data record values from the server identifier by one or more
:ref:`DataIdentifiers (DIDs) <knowledge-base-did>`.


Request Format
``````````````
Request contains at least one DataIdentifier (*DID*).

+------+------------+---------------+----------------------+----------+
| Name | Bit Length | Value         | Description          | Present  |
+======+============+===============+======================+==========+
| SID  | 8          | 0x22          | ReadDataByIdentifier | Always   |
+------+------------+---------------+----------------------+----------+
|  DID | 16         | 0x0000-0xFFFF | DID#1                | Always   |
|      +------------+---------------+----------------------+----------+
|      | ...                                                          |
|      +------------+---------------+----------------------+----------+
|      | 16         | 0x0000-0xFFFF | DID#n                | Optional |
+------+------------+---------------+----------------------+----------+


Positive Response Format
````````````````````````
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+
| Name       | Bit Length | Value         | Description                                    | Present                                          |
+============+============+===============+================================================+==================================================+
| RSID       | 8          | 0x62          | Positive Response: ReadDataByIdentifier (0x22) | Always                                           |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+
| DID#1      | 16         | 0x0000-0xFFFF | Data Identifier #1                             | Always                                           |
+------------+------------+---------------+------------------------------------------------+                                                  |
| DID#1 data | at least 8 |               | Data stored under DID#1                        |                                                  |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+
| ...                                                                                                                                         |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+
| DID#n      | 16         | 0x0000-0xFFFF | Data Identifier #n                             | If at least n DIDs were requested by the client. |
+------------+------------+---------------+------------------------------------------------+                                                  |
| DID#n data | at least 8 |               | Data stored under DID#n                        |                                                  |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+


.. _knowledge-base-service-read-memory-by-address:

ReadMemoryByAddress (0x23)
--------------------------
ReadMemoryByAddress service allows the client to request server's memory data stored under provided memory address.


Request Format
``````````````
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+
| Name                                                   | Bit Length            | Value   | Description                              | Present |
+========================================================+=======================+=========+==========================================+=========+
| SID                                                    | 8                     | 0x23    | ReadMemoryByAddress                      | Always  |
+----------------------------------+---------------------+-----------------------+---------+------------------------------------------+---------+
| addressAndLengthFormatIdentifier | memorySizeLength    | 4 (b[7-4])            | 0x1-0xF | Number of bytes to use for memorySize    | Always  |
|                                  +---------------------+-----------------------+---------+------------------------------------------+         |
|                                  | memoryAddressLength | 4 (b[3-0])            | 0x1-0xF | Number of bytes to use for memoryAddress |         |
+----------------------------------+---------------------+-----------------------+---------+------------------------------------------+---------+
| memoryAddress                                          | 8*memoryAddressLength |         | Starting address in the server's memory  | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+
| memorySize                                             | 8*memorySizeLength    |         | Number of bytes to read                  | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+


Positive Response Format
````````````````````````
+------+--------------+-------+-----------------------------------------------+---------+
| Name | Bit Length   | Value | Description                                   | Present |
+======+==============+=======+===============================================+=========+
| RSID | 8            | 0x63  | Positive Response: ReadMemoryByAddress (0x23) | Always  |
+------+--------------+-------+-----------------------------------------------+---------+
| data | 8*memorySize |       | Data read from server's memory                | Always  |
+------+--------------+-------+-----------------------------------------------+---------+


.. _knowledge-base-service-read-scaling-data-by-identifier:

ReadScalingDataByIdentifier (0x24)
----------------------------------
ReadScalingDataByIdentifier service allows the client to request the scaling information associated
with a Data Identifier (DID).
Scaling data provides information required to correctly interpret the actual data value, such as:
- data encoding type (e.g. integer, floating-point, ASCII),
- units and formats,
- conversion formulas and coefficients,
- bit mappings, and other interpretation details.


Request Format
``````````````
+------+------------+---------------+-----------------------------+---------+
| Name | Bit Length | Value         | Description                 | Present |
+======+============+===============+=============================+=========+
| SID  | 8          | 0x24          | ReadScalingDataByIdentifier | Always  |
+------+------------+---------------+-----------------------------+---------+
| DID  | 16         | 0x0000-0xFFFF | Data Identifier             | Always  |
+------+------------+---------------+-----------------------------+---------+


Positive Response Format
````````````````````````
Due to the complexity and variability of the *scalingByteExtension*, multiple formats are defined based on the
`scalingByte` value.
Only the format applicable to the returned scalingByte value will be included in the response.

.. warning:: In ISO 14229-1 the coefficients C0..Cm “follow” formulaIdentifier and are part of scalingByteExtension.
  In the translator (due to code design limitations), scalingByteExtension#n contains only formulaIdentifier Data Record.
  Each coefficient is represented as a separate, subsequent Data Record named Ci#n (where i = 0..m), each encoded as:

    Exponent: 4 bits (signed)
    Mantissa: 12 bits (signed)

  Practically, you will see:

    scalingByte#n (type=formula, numberOfBytesOfParameter=k)
    scalingByteExtension#n → formulaIdentifier
    C0#n → Exponent, Mantissa
    C1#n → Exponent, Mantissa

  This layout is equivalent to the ISO definition and is used to simplify conditional rendering and parsing.
  Coefficients are not nested under scalingByteExtension#n in the decoded tree; they follow it as sibling fields.

+----------------------------------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| Name                                                           | Bit Length                                | Value         | Description                                                                                   | Present                                                                 |
+================================================================+===========================================+===============+===============================================================================================+=========================================================================+
| RSID                                                           | 8                                         | 0x64          | Positive Response: ReadScalingDataByIdentifier (0x24)                                         | Always                                                                  |
+----------------------------------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| DID                                                            | 16                                        | 0x0000-0xFFFF | DID                                                                                           | Always                                                                  |
+------------------------+---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByte#1          | type                                  | 4 (b[7-4])                                | 0x0-0xF       | 0x0: unSignedNumeric                                                                          | Always                                                                  |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1: signedNumeric                                                                            |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2: bitMappedReportedWithOutMask                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3: bitMappedReportedWithMask                                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4: BinaryCodedDecimal                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x5: stateEncodedVariable                                                                     |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x6: ASCII                                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x7: signedFloatingPoint                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x8: packet                                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x9: formula                                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0xA: unit/format                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0xB: stateAndConnectionType                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0xC-0xF: reserved                                                                             |                                                                         |
|                        +---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        | numberOfBytesOfParameter              | 4 (b[3-0])                                | 0x0-0xF       | Number of parameter#1's bytes                                                                 |                                                                         |
+------------------------+---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#1 | validityMask                          | 8*scalingByte#1[numberOfBytesOfParameter] |               | Bits supported by the server's application.                                                   | If scalingByte#1[type] equals 0x2 (bitMappedReportedWithOutMask)        |
+------------------------+---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#1 | formulaIdentifier                     | 8                                         | 0x00-0xFF     | 0x00: y = C0 * x + C1                                                                         | If scalingByte#1[type] equals 0x9 (formula)                             |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x01: y = C0 * (x + C1)                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x02: y = C0 / (x + C1) + C2                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x03: y = x / C0 + C1                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x04: y = (x + C0) / C1                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x05: y = (x + C0) / C1 + C2                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x06: y = C0 * x                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x07: y = x / C0                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x08: y = x + C0                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x09: y = x * C0 / C1                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0A-0x7F: ISO/SAE reserved                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x80-0xFF: Vehicle manufacturer specific                                                      |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        | C0#1                   | Exponent     | 4 (b[7-4])                                | 0x0-0xF       | C0#1's parameter exponent value encoded as signed integer value.                              |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | Mantissa     | 12 (b[3-0] + b[7-0])                      | 0x000-0xFFF   | C0#1's parameter mantissa value encoded as signed integer value.                              |                                                                         |
|                        +------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
|                        | ...                                                                                                                                                                                                                                                                         |
|                        +------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
|                        | Cm#1                   | Exponent     | 4 (b[7-4])                                | 0x0-0xF       | Cm#1's parameter exponent value encoded as signed integer value.                              | If scalingByteExtension#1[formulaIdentifier] uses at least m constants. |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | Mantissa     | 12 (b[3-0] + b[7-0])                      | 0x000-0xFFF   | Cm#1's parameter mantissa value encoded as signed integer value.                              |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#1 | unit/format                           | 8                                         | 0x00-0xFF     | 0x00: No unit, no prefix                                                                      | If scalingByte#1[type] equals 0xA (unit/format)                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x01: Meter [m] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x02: Foot [ft] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x03: Inch [in] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x04: Yard [yd] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x05: Mile (English) [mi] - length                                                            |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x06: Gram [g] - mass                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x07: Ton (metric) [t] - mass                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x08: Second [s] - time                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x09: Minute [min] - time                                                                     |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0A: Hour [h] - time                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0B: Day [d] - time                                                                          |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0C: Year [y] - time                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0D: Ampere [A] - current                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0E: Volt [V] - voltage                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0F: Coulomb [C] - electric charge                                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x10: Ohm [Ω] - resistance                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x11: Farad [F] - capacitance                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x12: Henry [H] - inductance                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x13: Siemens [S] - electric conductance                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x14: Weber [Wb] - magnetic flux                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x15: Tesla [T] - magnetic flux density                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x16: Kelvin [K] - thermodynamic temperature                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x17: Celsius [°C] - thermodynamic temperature                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x18: Fahrenheit [°F] - thermodynamic temperature                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x19: Candela [cd] - luminous intensity                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1A: Radian [rad] - plane angle                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1B: Degree [°] - plane angle                                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1C: Hertz [Hz] - frequency                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1D: Joule [J] - energy                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1E: Newton [N] - force                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1F: Kilopond [kp] - force                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x20: Pound force [lbf] - force                                                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x21: Watt [W] - power                                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x22: Horse power (metric) [hk] - power                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x23: Horse power (UK and US) [hp] - power                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x24: Pascal [Pa] - pressure                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x25: Bar [bar] - pressure                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x26: Atmosphere [atm] - pressure                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x27: Pound force per square inch [psi] - pressure                                            |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x28: Becquerel [Bq] - radioactivity                                                          |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x29: Lumen [Lm] - light flux                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2A: Lux [lx] - illuminance                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2B: Litre [l] - volume                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2C: Gallon (British) - volume                                                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2D: Gallon (US liq) - volume                                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2E: Cubic inch [cu in] - volume                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2F: Meter per second [m/s] - speed                                                          |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x30: Kilometer per hour [km/h] - speed                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x31: Mile per hour [mph] - speed                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x32: Revolutions per second [rps] - angular velocity                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x33: Revolutions per minute [rpm] - angular velocity                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x34: Counts                                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x35: Percent [%]                                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x36: Milligram per stroke [mg/stroke] - mass per engine stroke                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x37: Meter per square second [m/s2] - acceleration                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x38: Newton meter [Nm] - moment (e.g. torsion moment)                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x39: Litre per minute [l/min] - flow                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3A: Watt per square meter [W/m2] - intensity                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3B: Bar per second [bar/s] - pressure change                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3C: Radians per second [rad/s] - angular velocity                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3D: Radians per square second [rad/s2] - angular acceleration                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3E: Kilogram per square meter [kg/m2]                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x40: Exa (prefix) [E] - 10 :sup:`18`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x41: Peta (prefix) [P] - 10 :sup:`15`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x42: Tera (prefix) [T] - 10 :sup:`12`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x43: Giga (prefix) [G] - 10 :sup:`9`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x44: Mega (prefix) [M] - 10 :sup:`6`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x45: Kilo (prefix) [k] - 10 :sup:`3`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x46: Hecto (prefix) [h] - 10 :sup:`2`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x47: Deca (prefix) [da] - 10                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x48: Deci (prefix) [d] - 10 :sup:`-1`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x49: Centi (prefix) [c] - 10 :sup:`-2`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4A: Milli (prefix) [m] - 10 :sup:`-3`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4B: Micro (prefix) [μ] - 10 :sup:`-6`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4C: Nano (prefix) [n] - 10 :sup:`-9`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4D: Pico (prefix) [p] - 10 :sup:`-12`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4E: Femto (prefix) [f] - 10 :sup:`-15`                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4F: Atto (prefix) [a] - 10 :sup:`-18`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x50: Year/Month/Day - date                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x51: Day/Month/Year - date                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x52: Month/Day/Year - date                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x53: Week - calendar week                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x54: UTC Hour/Minute/Second - time                                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x55: Hour/Minute/Second - time                                                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x56: Second/Minute/Hour/Day/Month/Year - date and time                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x57: Second/Minute/Hour/Day/Month/Year/Local minute offset/Local hour offset - date and time |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x58: Second/Minute/Hour/Month/Day/Year - date and time                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x59: Second/Minute/Hour/Month/Day/Year/Local minute offset/Local hour offset - date and time |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#1 | stateAndConnectionType | signalAccess | 2 (b[7-6])                                | 0x0-0x3       | 0: Internal signal                                                                            | If scalingByte#1[type] equals 0xB (stateAndConnectionType)              |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Low side switch (2 states)                                                                 |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 2: High side switch (2 states)                                                                |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 3: Low side and high side switch (2 states)                                                   |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | signalType   | 1 (b[5])                                  | 0x0-0x1       | 0: Input signal                                                                               |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Output signal                                                                              |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | signal       | 2 (b[4-3])                                | 0x0-0x3       | 0: Signal at low level (ground)                                                               |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Signal at middle level (between ground and +)                                              |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 2: Signal at high level (+)                                                                   |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 3: Reserved                                                                                   |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | state        | 3 (b[2-0])                                | 0x0-0x7       | 0: Not Active                                                                                 |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Active, function 1                                                                         |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 2: Error detected                                                                             |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 3: Not available                                                                              |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 4: Active, function 2                                                                         |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 5-7: Reserved                                                                                 |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ...                                                                                                                                                                                                                                                                                                  |
+------------------------+---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByte#n          | type                                  | 4 (b[7-4])                                | 0x0-0xF       | 0x0: unSignedNumeric                                                                          | If DID contains at least n parameters                                   |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1: signedNumeric                                                                            |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2: bitMappedReportedWithOutMask                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3: bitMappedReportedWithMask                                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4: BinaryCodedDecimal                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x5: stateEncodedVariable                                                                     |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x6: ASCII                                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x7: signedFloatingPoint                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x8: packet                                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x9: formula                                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0xA: unit/format                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0xB: stateAndConnectionType                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0xC-0xF: reserved                                                                             |                                                                         |
|                        +---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        | numberOfBytesOfParameter              | 4 (b[3-0])                                | 0x0-0xF       | Number of parameter#n's bytes                                                                 |                                                                         |
+------------------------+---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#n | validityMask                          | 8*scalingByte#n[numberOfBytesOfParameter] |               | Bits supported by the server's application.                                                   | If scalingByte#n[type] equals 0x2 (bitMappedReportedWithOutMask)        |
+------------------------+---------------------------------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#n | formulaIdentifier                     | 8                                         | 0x00-0xFF     | 0x00: y = C0 * x + C1                                                                         | If scalingByte#n[type] equals 0x9 (formula)                             |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x01: y = C0 * (x + C1)                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x02: y = C0 / (x + C1) + C2                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x03: y = x / C0 + C1                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x04: y = (x + C0) / C1                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x05: y = (x + C0) / C1 + C2                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x06: y = C0 * x                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x07: y = x / C0                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x08: y = x + C0                                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x09: y = x * C0 / C1                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0A-0x7F: ISO/SAE reserved                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x80-0xFF: Vehicle manufacturer specific                                                      |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        | C0#n                   | Exponent     | 4 (b[7-4])                                | 0x0-0xF       | C0's parameter exponent value encoded as signed value.                                        |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | Mantissa     | 12 (b[3-0] + b[7-0])                      | 0x000-0xFFF   | C0's parameter mantissa value encoded as signed value.                                        |                                                                         |
|                        +------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
|                        | ...                                                                                                                                                                                                                                                                         |
|                        +------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
|                        | Cm#n                   | Exponent     | 4 (b[7-4])                                | 0x0-0xF       | Cm's parameter exponent value encoded as signed value.                                        | If scalingByteExtension#n[formulaIdentifier] uses at least m constants. |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | Mantissa     | 12 (b[3-0] + b[7-0])                      | 0x000-0xFFF   | Cm's parameter mantissa value encoded as signed value.                                        |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#n | unit/format                           | 8                                         | 0x00-0xFF     | 0x00: No unit, no prefix                                                                      | If scalingByte#n[type] equals 0xA (unit/format)                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x01: Meter [m] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x02: Foot [ft] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x03: Inch [in] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x04: Yard [yd] - length                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x05: Mile (English) [mi] - length                                                            |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x06: Gram [g] - mass                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x07: Ton (metric) [t] - mass                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x08: Second [s] - time                                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x09: Minute [min] - time                                                                     |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0A: Hour [h] - time                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0B: Day [d] - time                                                                          |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0C: Year [y] - time                                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0D: Ampere [A] - current                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0E: Volt [V] - voltage                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x0F: Coulomb [C] - electric charge                                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x10: Ohm [Ω] - resistance                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x11: Farad [F] - capacitance                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x12: Henry [H] - inductance                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x13: Siemens [S] - electric conductance                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x14: Weber [Wb] - magnetic flux                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x15: Tesla [T] - magnetic flux density                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x16: Kelvin [K] - thermodynamic temperature                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x17: Celsius [°C] - thermodynamic temperature                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x18: Fahrenheit [°F] - thermodynamic temperature                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x19: Candela [cd] - luminous intensity                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1A: Radian [rad] - plane angle                                                              |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1B: Degree [°] - plane angle                                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1C: Hertz [Hz] - frequency                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1D: Joule [J] - energy                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1E: Newton [N] - force                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x1F: Kilopond [kp] - force                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x20: Pound force [lbf] - force                                                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x21: Watt [W] - power                                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x22: Horse power (metric) [hk] - power                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x23: Horse power (UK and US) [hp] - power                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x24: Pascal [Pa] - pressure                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x25: Bar [bar] - pressure                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x26: Atmosphere [atm] - pressure                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x27: Pound force per square inch [psi] - pressure                                            |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x28: Becquerel [Bq] - radioactivity                                                          |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x29: Lumen [Lm] - light flux                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2A: Lux [lx] - illuminance                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2B: Litre [l] - volume                                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2C: Gallon (British) - volume                                                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2D: Gallon (US liq) - volume                                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2E: Cubic inch [cu in] - volume                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x2F: Meter per second [m/s] - speed                                                          |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x30: Kilometer per hour [km/h] - speed                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x31: Mile per hour [mph] - speed                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x32: Revolutions per second [rps] - angular velocity                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x33: Revolutions per minute [rpm] - angular velocity                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x34: Counts                                                                                  |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x35: Percent [%]                                                                             |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x36: Milligram per stroke [mg/stroke] - mass per engine stroke                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x37: Meter per square second [m/s2] - acceleration                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x38: Newton meter [Nm] - moment (e.g. torsion moment)                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x39: Litre per minute [l/min] - flow                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3A: Watt per square meter [W/m2] - intensity                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3B: Bar per second [bar/s] - pressure change                                                |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3C: Radians per second [rad/s] - angular velocity                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3D: Radians per square second [rad/s2] - angular acceleration                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x3E: Kilogram per square meter [kg/m2]                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x40: Exa (prefix) [E] - 10 :sup:`18`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x41: Peta (prefix) [P] - 10 :sup:`15`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x42: Tera (prefix) [T] - 10 :sup:`12`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x43: Giga (prefix) [G] - 10 :sup:`9`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x44: Mega (prefix) [M] - 10 :sup:`6`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x45: Kilo (prefix) [k] - 10 :sup:`3`                                                         |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x46: Hecto (prefix) [h] - 10 :sup:`2`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x47: Deca (prefix) [da] - 10                                                                 |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x48: Deci (prefix) [d] - 10 :sup:`-1`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x49: Centi (prefix) [c] - 10 :sup:`-2`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4A: Milli (prefix) [m] - 10 :sup:`-3`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4B: Micro (prefix) [μ] - 10 :sup:`-6`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4C: Nano (prefix) [n] - 10 :sup:`-9`                                                        |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4D: Pico (prefix) [p] - 10 :sup:`-12`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4E: Femto (prefix) [f] - 10 :sup:`-15`                                                      |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x4F: Atto (prefix) [a] - 10 :sup:`-18`                                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x50: Year/Month/Day - date                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x51: Day/Month/Year - date                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x52: Month/Day/Year - date                                                                   |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x53: Week - calendar week                                                                    |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x54: UTC Hour/Minute/Second - time                                                           |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x55: Hour/Minute/Second - time                                                               |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x56: Second/Minute/Hour/Day/Month/Year - date and time                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x57: Second/Minute/Hour/Day/Month/Year/Local minute offset/Local hour offset - date and time |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x58: Second/Minute/Hour/Month/Day/Year - date and time                                       |                                                                         |
|                        |                                       |                                           |               |                                                                                               |                                                                         |
|                        |                                       |                                           |               | 0x59: Second/Minute/Hour/Month/Day/Year/Local minute offset/Local hour offset - date and time |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| scalingByteExtension#n | stateAndConnectionType | signalAccess | 2 (b[7-6])                                | 0x0-0x3       | 0: Internal signal                                                                            | If scalingByte#n[type] equals 0xB (stateAndConnectionType)              |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Low side switch (2 states)                                                                 |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 2: High side switch (2 states)                                                                |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 3: Low side and high side switch (2 states)                                                   |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | signalType   | 1 (b[5])                                  | 0x0-0x1       | 0: Input signal                                                                               |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Output signal                                                                              |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | signal       | 2 (b[4-3])                                | 0x0-0x3       | 0: Signal at low level (ground)                                                               |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Signal at middle level (between ground and +)                                              |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 2: Signal at high level (+)                                                                   |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 3: Reserved                                                                                   |                                                                         |
|                        |                        +--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+                                                                         |
|                        |                        | state        | 3 (b[2-0])                                | 0x0-0x7       | 0: Not Active                                                                                 |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 1: Active, function 1                                                                         |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 2: Error detected                                                                             |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 3: Not available                                                                              |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 4: Active, function 2                                                                         |                                                                         |
|                        |                        |              |                                           |               |                                                                                               |                                                                         |
|                        |                        |              |                                           |               | 5-7: Reserved                                                                                 |                                                                         |
+------------------------+------------------------+--------------+-------------------------------------------+---------------+-----------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+

.. note:: Parameter *numberOfBytesOfParameter* shall equal 0 when the *scalingByte* *type* equals
  0x9 [formula] or 0xA [unit/format].


.. _knowledge-base-service-security-access:

SecurityAccess (0x27)
---------------------
SecurityAccess service allows the client to unlock functions/services with restricted access.

Unlocking sequence:

1) The client requests a seed from the server.
2) The server responds with a positive response that includes a randomly generated seed value.
3) Both the client and server compute a key value based on the seed (using a secret algorithm).
4) The client sends the computed key to the server.
5) The server validates the client by comparing the received key with its own calculated key.
   If they match, the client is granted access to the protected functionality for the corresponding security level.


RequestSeed
```````````


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+----------+
| Name                                         | Bit Length | Value     | Description                                                                                            | Present  |
+==============================================+============+===========+========================================================================================================+==========+
| SID                                          | 8          | 0x27      | SecurityAccess                                                                                         | Always   |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+----------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                                                                  | Always   |
|             |                                |            |           |                                                                                                        |          |
|             |                                |            |           | 1 = suppress positive response                                                                         |          |
|             +--------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+          |
|             | securityAccessType             | 7 (b[6-0]) | 0x01-0x7D | 0x01, 0x03, ..., 0x41: request seed for security level defined by the vehicle manufacturer             |          |
|             |                                |            |           |                                                                                                        |          |
|             |                                |            |           | 0x43, 0x45, ..., 0x5D: reserved                                                                        |          |
|             |                                |            |           |                                                                                                        |          |
|             |                                |            |           | 0x5F: request seed for end of life activation of on-board pyrotechnic devices (defined by ISO 26021-2) |          |
|             |                                |            |           |                                                                                                        |          |
|             |                                |            |           | 0x61, 0x63, ..., 0x7D: request seed for security level defined by the system supplier                  |          |
|             |                                |            |           |                                                                                                        |          |
|             |                                |            |           | 0x7F: reserved                                                                                         |          |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+----------+
| securityAccessData                           | 8 or more  |           | Additional vehicle manufacturer specific information about the client (e.g. type of device).           | Optional |
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+----------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                                                            | Present |
+==============================================+============+===========+========================================================================================================+=========+
| RSID                                         | 8          | 0x67      | Positive Response: SecurityAccess (0x27)                                                               | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                                                                  | Always  |
|             |                                |            |           |                                                                                                        |         |
|             |                                |            |           | 1 = suppress positive response                                                                         |         |
|             +--------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+         |
|             | securityAccessType             | 7 (b[6-0]) | 0x01-0x7D | 0x01, 0x03, ..., 0x41: request seed for security level defined by the vehicle manufacturer             |         |
|             |                                |            |           |                                                                                                        |         |
|             |                                |            |           | 0x43, 0x45, ..., 0x5D: reserved                                                                        |         |
|             |                                |            |           |                                                                                                        |         |
|             |                                |            |           | 0x5F: request seed for end of life activation of on-board pyrotechnic devices (defined by ISO 26021-2) |         |
|             |                                |            |           |                                                                                                        |         |
|             |                                |            |           | 0x61, 0x63, ..., 0x7D: request seed for security level defined by the system supplier                  |         |
|             |                                |            |           |                                                                                                        |         |
|             |                                |            |           | 0x7F: reserved                                                                                         |         |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+---------+
| securitySeed                                 | 8 or more  |           | Random seed value generated by the server.                                                             | Always  |
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------------------------------------------+---------+


SendKey
```````


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                                                        | Present |
+==============================================+============+===========+====================================================================================================+=========+
| SID                                          | 8          | 0x27      | SecurityAccess                                                                                     | Always  |
+-------------+--------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                                                              | Always  |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 1 = suppress positive response                                                                     |         |
|             +--------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+         |
|             | securityAccessType             | 7 (b[6-0]) | 0x02-0x7E | 0x00: reserved                                                                                     |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x02, 0x04, ..., 0x42: send key for security level defined by the vehicle manufacturer             |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x44, 0x46, ..., 0x58: reserved                                                                    |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x60: send key for end of life activation of on-board pyrotechnic devices (defined by ISO 26021-2) |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x62, 0x64, ..., 0x7E: send key for security level defined by the system supplier                  |         |
+-------------+--------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+
| securityKey                                  | 8 or more  |           | Security key calculated for the seed value provided earlier by the server.                         | Always  |
+----------------------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                                                        | Present |
+==============================================+============+===========+====================================================================================================+=========+
| RSID                                         | 8          | 0x67      | Positive Response: SecurityAccess (0x27)                                                           | Always  |
+-------------+--------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                                                              | Always  |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 1 = suppress positive response                                                                     |         |
|             +--------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+         |
|             | securityAccessType             | 7 (b[6-0]) | 0x02-0x7E | 0x00: reserved                                                                                     |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x02, 0x04, ..., 0x42: send key for security level defined by the vehicle manufacturer             |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x44, 0x46, ..., 0x58: reserved                                                                    |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x60: send key for end of life activation of on-board pyrotechnic devices (defined by ISO 26021-2) |         |
|             |                                |            |           |                                                                                                    |         |
|             |                                |            |           | 0x62, 0x64, ..., 0x7E: send key for security level defined by the system supplier                  |         |
+-------------+--------------------------------+------------+-----------+----------------------------------------------------------------------------------------------------+---------+


.. _knowledge-base-service-communication-control:

CommunicationControl (0x28)
---------------------------
CommunicationControl service allows the client to switch on/off the transmission and/or the reception of certain
messages on the server(s).


Request Format
``````````````
+----------------------------------------------------+------------+---------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| Name                                               | Bit Length | Value         | Description                                                                 | Present                                                                       |
+====================================================+============+===============+=============================================================================+===============================================================================+
| SID                                                | 8          | 0x28          | CommunicationControl                                                        | Always                                                                        |
+-------------------+--------------------------------+------------+---------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| SubFunction       | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                                                       | Always                                                                        |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 1 = suppress positive response                                              |                                                                               |
|                   +--------------------------------+------------+---------------+-----------------------------------------------------------------------------+                                                                               |
|                   | controlType                    | 7 (b[6-0]) | 0x00-0x7F     | 0x00: enableRxAndTx                                                         |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x01: enableRxAndDisableTx                                                  |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x02: disableRxAndEnableTx                                                  |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x03: disableRxAndTx                                                        |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x04: enableRxAndDisableTxWithEnhancedAddressInformation                    |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x05: enableRxAndTxWithEnhancedAddressInformation                           |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x06-0x3F: reserved                                                         |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x40-0x5F: vehicle manufacturer specific                                    |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x60-0x7E: system supplier specific                                         |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x7F: reserved                                                              |                                                                               |
+-------------------+--------------------------------+------------+---------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| communicationType | messagesType                   | 2 (b[7-6]) | 0x0-0x3       | 0x0: reserved                                                               | Always                                                                        |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x1: normalCommunicationMessages                                            |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x2: networkManagementCommunicationMessages                                 |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x3: networkManagementCommunicationMessages and normalCommunicationMessages |                                                                               |
|                   +--------------------------------+------------+---------------+-----------------------------------------------------------------------------+                                                                               |
|                   | reserved                       | 2 (b[5-4]) | 0x0-0x3       | Unused                                                                      |                                                                               |
|                   +--------------------------------+------------+---------------+-----------------------------------------------------------------------------+                                                                               |
|                   | networks                       | 4 (b[3-0]) | 0x0-0xF       | 0x0: all connected networks                                                 |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0x1-0xE: subnet defined by this subnet number                               |                                                                               |
|                   |                                |            |               |                                                                             |                                                                               |
|                   |                                |            |               | 0xF: network on which this request is received                              |                                                                               |
+-------------------+--------------------------------+------------+---------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| nodeIdentificationNumber                           | 16         | 0x0000-0xFFFF | 0x0000: reserved                                                            | If controlType equals 4 (enableRxAndDisableTxWithEnhancedAddressInformation)  |
|                                                    |            |               |                                                                             | or 5 (enableRxAndTxWithEnhancedAddressInformation)                            |
+----------------------------------------------------+------------+---------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+-----------+----------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                              | Present |
+==============================================+============+===========+==========================================================+=========+
| RSID                                         | 8          | 0x68      | Positive Response: CommunicationControl (0x28)           | Always  |
+-------------+--------------------------------+------------+-----------+----------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                    | Always  |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 1 = suppress positive response                           |         |
|             +--------------------------------+------------+-----------+----------------------------------------------------------+         |
|             | controlType                    | 7 (b[6-0]) | 0x00-0x7F | 0x00: enableRxAndTx                                      |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x01: enableRxAndDisableTx                               |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x02: disableRxAndEnableTx                               |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x03: disableRxAndTx                                     |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x04: enableRxAndDisableTxWithEnhancedAddressInformation |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x05: enableRxAndTxWithEnhancedAddressInformation        |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x06-0x3F: reserved                                      |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x40-0x5F: vehicle manufacturer specific                 |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x60-0x7E: system supplier specific                      |         |
|             |                                |            |           |                                                          |         |
|             |                                |            |           | 0x7F: reserved                                           |         |
+-------------+--------------------------------+------------+-----------+----------------------------------------------------------+---------+


.. _knowledge-base-service-authentication:

Authentication (0x29)
---------------------
Authentication service provides a mechanism for the client to prove its identity, allowing access to data and/or
diagnostic services that have restricted access due to security, emissions, or safety requirements.

.. note:: Service Authentication was introduced in version ISO 14229-1:2020.

ISO 14229-1 defines the following *authenticationTask* sub-function values:

- 0x00: :ref:`deAuthenticate <knowledge-base-service-authentication-00>`
- 0x01: :ref:`verifyCertificateUnidirectional <knowledge-base-service-authentication-01>`
- 0x02: :ref:`verifyCertificateBidirectional <knowledge-base-service-authentication-02>`
- 0x03: :ref:`proofOfOwnership <knowledge-base-service-authentication-03>`
- 0x04: :ref:`transmitCertificate <knowledge-base-service-authentication-04>`
- 0x05: :ref:`requestChallengeForAuthentication <knowledge-base-service-authentication-05>`
- 0x06: :ref:`verifyProofOfOwnershipUnidirectional <knowledge-base-service-authentication-06>`
- 0x07: :ref:`verifyProofOfOwnershipBidirectional <knowledge-base-service-authentication-07>`
- 0x08: :ref:`authenticationConfiguration <knowledge-base-service-authentication-08>`


.. _knowledge-base-service-authentication-00:

deAuthenticate (0x00)
`````````````````````
This sub-function can be used by the client to inform the server that the communication session is being closed and
to exit the authenticated state.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x29    | Authentication                 | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+         |
|             | authenticationTask             | 7 (b[6-0]) | 0x00    | deAuthenticate                 |         |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                        | Present |
+==============================================+============+===========+====================================================================+=========+
| RSID                                         | 8          | 0x69      | Positive Response: Authentication (0x29)                           | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                              | Always  |
|             |                                |            |           |                                                                    |         |
|             |                                |            |           | 1 = suppress positive response                                     |         |
|             +--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
|             | authenticationTask             | 7 (b[6-0]) | 0x00      | deAuthenticate                                                     | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| authenticationReturnParameter                | 8          | 0x00-0xFF | 0x00: RequestAccepted                                              | Always  |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x01: GeneralReject                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x02: AuthenticationConfiguration                                  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x04: AuthenticationConfiguration ACR with symmetric cryptography  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x05-0x0F: reserved                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x10: DeAuthentication successful                                  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x11: CertificateVerified, OwnershipVerificationNecessary          |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x12: OwnershipVerified, AuthenticationComplete                    |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x13: CertificateVerified                                          |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x14-0x9F: reserved                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xA0-0xCF: vehicle manufacturer specific                           |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xD0-0xFE: system supplier specific                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xFF: reserved                                                     |         |
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------+---------+


.. _knowledge-base-service-authentication-01:

verifyCertificateUnidirectional (0x01)
``````````````````````````````````````
This sub-function can be used by the client to initiate its own authentication process using Certificate.


Request Format
''''''''''''''
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| Name                                         | Bit Length                  | Value         | Description                                                | Present                               |
+==============================================+=============================+===============+============================================================+=======================================+
| SID                                          | 8                           | 0x29          | Authentication                                             | Always                                |
+-------------+--------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                    | 0x0-0x1       | 0 = response required                                      | Always                                |
|             |                                |                             |               |                                                            |                                       |
|             |                                |                             |               | 1 = suppress positive response                             |                                       |
|             +--------------------------------+-----------------------------+---------------+------------------------------------------------------------+                                       |
|             | authenticationTask             | 7 (b[6-0])                  | 0x01          | verifyCertificateUnidirectional                            |                                       |
+-------------+--------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| communicationConfiguration                   | 8                           | 0x00-0xFF     | Information about how to proceed with security in further  | Always                                |
|                                              |                             |               | diagnostic communication after the Authentication.         |                                       |
|                                              |                             |               |                                                            |                                       |
|                                              |                             |               | Values meaning is vehicle manufacturer specific.           |                                       |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| lengthOfCertificateClient                    | 16                          | 0x0001-0xFFFF | Byte length of certificateClient Data Record.              | Always                                |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| certificateClient                            | 8*lengthOfCertificateClient |               | The Certificate to verify.                                 | Always                                |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| lengthOfChallengeClient                      | 16                          | 0x0000-0xFFFF | Byte length of challengeClient Data Record.                | Always                                |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+
| challengeClient                              | 8*lengthOfChallengeClient   |               | Challenge generated by the client for the server.          | If lengthOfChallengeClient unequals 0 |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------------------------------------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| Name                                         | Bit Length                         | Value         | Description                                                                    | Present                                        |
+==============================================+====================================+===============+================================================================================+================================================+
| RSID                                         | 8                                  | 0x69          | Positive Response: Authentication (0x29)                                       | Always                                         |
+-------------+--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                           | 0x0-0x1       | 0 = response required                                                          | Always                                         |
|             |                                |                                    |               |                                                                                |                                                |
|             |                                |                                    |               | 1 = suppress positive response                                                 |                                                |
|             +--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
|             | authenticationTask             | 7 (b[6-0])                         | 0x01          | verifyCertificateUnidirectional                                                | Always                                         |
+-------------+--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| authenticationReturnParameter                | 8                                  | 0x00-0xFF     | 0x00: RequestAccepted                                                          | Always                                         |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x01: GeneralReject                                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x02: AuthenticationConfiguration                                              |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography             |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x04: AuthenticationConfiguration ACR with symmetric cryptography              |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x05-0x0F: reserved                                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x10: DeAuthentication successful                                              |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x11: CertificateVerified, OwnershipVerificationNecessary                      |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x12: OwnershipVerified, AuthenticationComplete                                |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x13: CertificateVerified                                                      |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x14-0x9F: reserved                                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0xA0-0xCF: vehicle manufacturer specific                                       |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0xD0-0xFE: system supplier specific                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0xFF: reserved                                                                 |                                                |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfChallengeServer                      | 16                                 | 0x0001-0xFFFF | Byte length of challengeServer Data Record.                                    | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| challengeServer                              | 8*lengthOfChallengeServer          |               | Challenge generated by the server for the client.                              | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfEphemeralPublicKeyServer             | 16                                 | 0x0000-0xFFFF | Byte length of ephemeralPublicKeyServer Data Record.                           | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| ephemeralPublicKeyServer                     | 8*lengthOfEphemeralPublicKeyServer |               | Ephemeral public key generated by the server for Diffie-Hellman key agreement. | If lengthOfEphemeralPublicKeyServer unequals 0 |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+


.. _knowledge-base-service-authentication-02:

verifyCertificateBidirectional (0x02)
`````````````````````````````````````
This sub-function can be used by the client to initiate a mutual (bidirectional) authentication process between
the client and the server using Certificates.


Request Format
''''''''''''''
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| Name                                         | Bit Length                  | Value         | Description                                                | Present |
+==============================================+=============================+===============+============================================================+=========+
| SID                                          | 8                           | 0x29          | Authentication                                             | Always  |
+-------------+--------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                    | 0x0-0x1       | 0 = response required                                      | Always  |
|             |                                |                             |               |                                                            |         |
|             |                                |                             |               | 1 = suppress positive response                             |         |
|             +--------------------------------+-----------------------------+---------------+------------------------------------------------------------+         |
|             | authenticationTask             | 7 (b[6-0])                  | 0x02          | verifyCertificateBidirectional                             |         |
+-------------+--------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| communicationConfiguration                   | 8                           | 0x00-0xFF     | Information about how to proceed with security in further  | Always  |
|                                              |                             |               | diagnostic communication after the Authentication.         |         |
|                                              |                             |               |                                                            |         |
|                                              |                             |               | Values meaning is vehicle manufacturer specific.           |         |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| lengthOfCertificateClient                    | 16                          | 0x0001-0xFFFF | Byte length of certificateClient Data Record.              | Always  |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| certificateClient                            | 8*lengthOfCertificateClient |               | The Certificate to verify.                                 | Always  |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| lengthOfChallengeClient                      | 16                          | 0x0001-0xFFFF | Byte length of challengeClient Data Record.                | Always  |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+
| challengeClient                              | 8*lengthOfChallengeClient   |               | Challenge generated by the client for the server.          | Always  |
+----------------------------------------------+-----------------------------+---------------+------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| Name                                         | Bit Length                         | Value         | Description                                                                    | Present                                        |
+==============================================+====================================+===============+================================================================================+================================================+
| RSID                                         | 8                                  | 0x69          | Positive Response: Authentication (0x29)                                       | Always                                         |
+-------------+--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                           | 0x0-0x1       | 0 = response required                                                          | Always                                         |
|             |                                |                                    |               |                                                                                |                                                |
|             |                                |                                    |               | 1 = suppress positive response                                                 |                                                |
|             +--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
|             | authenticationTask             | 7 (b[6-0])                         | 0x02          | verifyCertificateBidirectional                                                 | Always                                         |
+-------------+--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| authenticationReturnParameter                | 8                                  | 0x00-0xFF     | 0x00: RequestAccepted                                                          | Always                                         |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x01: GeneralReject                                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x02: AuthenticationConfiguration                                              |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography             |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x04: AuthenticationConfiguration ACR with symmetric cryptography              |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x05-0x0F: reserved                                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x10: DeAuthentication successful                                              |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x11: CertificateVerified, OwnershipVerificationNecessary                      |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x12: OwnershipVerified, AuthenticationComplete                                |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x13: CertificateVerified                                                      |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0x14-0x9F: reserved                                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0xA0-0xCF: vehicle manufacturer specific                                       |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0xD0-0xFE: system supplier specific                                            |                                                |
|                                              |                                    |               |                                                                                |                                                |
|                                              |                                    |               | 0xFF: reserved                                                                 |                                                |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfChallengeServer                      | 16                                 | 0x0001-0xFFFF | Byte length of challengeServer Data Record.                                    | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| challengeServer                              | 8*lengthOfChallengeServer          |               | Challenge generated by the server for the client.                              | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfCertificateServer                    | 16                                 | 0x0001-0xFFFF | Byte length of certificateServer Data Record.                                  | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| certificateServer                            | 8*lengthOfCertificateServer        |               | The Certificate to verify.                                                     | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfProofOfOwnershipServer               | 16                                 | 0x0001-0xFFFF | Byte length of proofOfOwnershipServer Data Record.                             | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| proofOfOwnershipServer                       | 8*lengthOfProofOfOwnershipServer   |               | Proof of Ownership to be verified by the client.                               | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfEphemeralPublicKeyServer             | 16                                 | 0x0000-0xFFFF | Byte length of ephemeralPublicKeyServer Data Record.                           | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| ephemeralPublicKeyServer                     | 8*lengthOfEphemeralPublicKeyServer |               | Ephemeral public key generated by the server for Diffie-Hellman key agreement. | If lengthOfEphemeralPublicKeyServer unequals 0 |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+


.. _knowledge-base-service-authentication-03:

proofOfOwnership (0x03)
```````````````````````
This sub-function can be used by the client to verify Proof of Ownership on the client side.


Request Format
''''''''''''''
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| Name                                         | Bit Length                         | Value         | Description                                                                    | Present                                        |
+==============================================+====================================+===============+================================================================================+================================================+
| SID                                          | 8                                  | 0x29          | Authentication                                                                 | Always                                         |
+-------------+--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                           | 0x0-0x1       | 0 = response required                                                          | Always                                         |
|             |                                |                                    |               |                                                                                |                                                |
|             |                                |                                    |               | 1 = suppress positive response                                                 |                                                |
|             +--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+                                                |
|             | authenticationTask             | 7 (b[6-0])                         | 0x03          | proofOfOwnership                                                               |                                                |
+-------------+--------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfProofOfOwnershipClient               | 16                                 | 0x0001-0xFFFF | Byte length of proofOfOwnershipClient Data Record.                             | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| proofOfOwnershipClient                       | 8*lengthOfProofOfOwnershipClient   |               | Client's Proof of Ownership for the challenge value given by the server.       | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| lengthOfEphemeralPublicKeyClient             | 16                                 | 0x0000-0xFFFF | Byte length of ephemeralPublicKeyClient Data Record.                           | Always                                         |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+
| ephemeralPublicKeyClient                     | 8*lengthOfEphemeralPublicKeyClient |               | Ephemeral public key generated by the client for Diffie-Hellman key agreement. | If lengthOfEphemeralPublicKeyClient unequals 0 |
+----------------------------------------------+------------------------------------+---------------+--------------------------------------------------------------------------------+------------------------------------------------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+
| Name                                         | Bit Length               | Value         | Description                                                        | Present                              |
+==============================================+==========================+===============+====================================================================+======================================+
| RSID                                         | 8                        | 0x69          | Positive Response: Authentication (0x29)                           | Always                               |
+-------------+--------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                 | 0x0-0x1       | 0 = response required                                              | Always                               |
|             |                                |                          |               |                                                                    |                                      |
|             |                                |                          |               | 1 = suppress positive response                                     |                                      |
|             +--------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+
|             | authenticationTask             | 7 (b[6-0])               | 0x03          | proofOfOwnership                                                   | Always                               |
+-------------+--------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+
| authenticationReturnParameter                | 8                        | 0x00-0xFF     | 0x00: RequestAccepted                                              | Always                               |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x01: GeneralReject                                                |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x02: AuthenticationConfiguration                                  |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x04: AuthenticationConfiguration ACR with symmetric cryptography  |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x05-0x0F: reserved                                                |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x10: DeAuthentication successful                                  |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x11: CertificateVerified, OwnershipVerificationNecessary          |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x12: OwnershipVerified, AuthenticationComplete                    |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x13: CertificateVerified                                          |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0x14-0x9F: reserved                                                |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0xA0-0xCF: vehicle manufacturer specific                           |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0xD0-0xFE: system supplier specific                                |                                      |
|                                              |                          |               |                                                                    |                                      |
|                                              |                          |               | 0xFF: reserved                                                     |                                      |
+----------------------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+
| lengthOfSessionKeyInfo                       | 16                       | 0x0000-0xFFFF | Byte length of sessionKeyInfo Data Record.                         | Always                               |
+----------------------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+
| sessionKeyInfo                               | 8*lengthOfSessionKeyInfo |               | Session key information (e.g. encrypted session keys).             | If lengthOfSessionKeyInfo unequals 0 |
+----------------------------------------------+--------------------------+---------------+--------------------------------------------------------------------+--------------------------------------+


.. _knowledge-base-service-authentication-04:

transmitCertificate (0x04)
``````````````````````````
This sub-function can be used by the client to transmit its Certificate to the server.


Request Format
''''''''''''''
+----------------------------------------------+---------------------------+---------------+---------------------------------------------------------------+---------+
| Name                                         | Bit Length                | Value         | Description                                                   | Present |
+==============================================+===========================+===============+===============================================================+=========+
| SID                                          | 8                         | 0x29          | Authentication                                                | Always  |
+-------------+--------------------------------+---------------------------+---------------+---------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                  | 0x0-0x1       | 0 = response required                                         | Always  |
|             |                                |                           |               |                                                               |         |
|             |                                |                           |               | 1 = suppress positive response                                |         |
|             +--------------------------------+---------------------------+---------------+---------------------------------------------------------------+         |
|             | authenticationTask             | 7 (b[6-0])                | 0x04          | transmitCertificate                                           |         |
+-------------+--------------------------------+---------------------------+---------------+---------------------------------------------------------------+---------+
| certificateEvaluationId                      | 16                        | 0x0000-0xFFFF | Identifier of evaluation type of the transmitted certificate. | Always  |
+----------------------------------------------+---------------------------+---------------+---------------------------------------------------------------+---------+
| lengthOfCertificateData                      | 16                        | 0x0001-0xFFFF | Byte length of certificateData Data Record.                   | Always  |
+----------------------------------------------+---------------------------+---------------+---------------------------------------------------------------+---------+
| certificateData                              | 8*lengthOfCertificateData |               | The Certificate to verify.                                    | Always  |
+----------------------------------------------+---------------------------+---------------+---------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                        | Present |
+==============================================+============+===========+====================================================================+=========+
| RSID                                         | 8          | 0x69      | Positive Response: Authentication (0x29)                           | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                              | Always  |
|             |                                |            |           |                                                                    |         |
|             |                                |            |           | 1 = suppress positive response                                     |         |
|             +--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
|             | authenticationTask             | 7 (b[6-0]) | 0x04      | transmitCertificate                                                | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| authenticationReturnParameter                | 8          | 0x00-0xFF | 0x00: RequestAccepted                                              | Always  |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x01: GeneralReject                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x02: AuthenticationConfiguration                                  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x04: AuthenticationConfiguration ACR with symmetric cryptography  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x05-0x0F: reserved                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x10: DeAuthentication successful                                  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x11: CertificateVerified, OwnershipVerificationNecessary          |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x12: OwnershipVerified, AuthenticationComplete                    |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x13: CertificateVerified                                          |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x14-0x9F: reserved                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xA0-0xCF: vehicle manufacturer specific                           |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xD0-0xFE: system supplier specific                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xFF: reserved                                                     |         |
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------+---------+


.. _knowledge-base-service-authentication-05:

requestChallengeForAuthentication (0x05)
````````````````````````````````````````
This sub-function can be used by the client to initiate own authentication process by requesting Challenge
from the server.


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-------------------------------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                                               | Present |
+==============================================+============+===========+===========================================================================================+=========+
| SID                                          | 8          | 0x29      | Authentication                                                                            | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                                                     | Always  |
|             |                                |            |           |                                                                                           |         |
|             |                                |            |           | 1 = suppress positive response                                                            |         |
|             +--------------------------------+------------+-----------+-------------------------------------------------------------------------------------------+         |
|             | authenticationTask             | 7 (b[6-0]) | 0x05      | requestChallengeForAuthentication                                                         |         |
+-------------+--------------------------------+------------+-----------+-------------------------------------------------------------------------------------------+---------+
| communicationConfiguration                   | 8          | 0x00-0xFF | Information about how to proceed with security in further                                 | Always  |
|                                              |            |           | diagnostic communication after the Authentication.                                        |         |
|                                              |            |           |                                                                                           |         |
|                                              |            |           | Values meanings are vehicle manufacturer specific.                                        |         |
+----------------------------------------------+------------+-----------+-------------------------------------------------------------------------------------------+---------+
| algorithmIndicator                           | 128        |           | Indicates the algorithm used in the generating and verifying Proof of Ownership.          | Always  |
|                                              |            |           |                                                                                           |         |
|                                              |            |           | This field is a 16 byte value containing the BER encoded OID value of the algorithm used. |         |
|                                              |            |           | The value is left aligned and right padded with zero up to 16 bytes.                      |         |
+----------------------------------------------+------------+-----------+-------------------------------------------------------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| Name                                         | Bit Length                          | Value         | Description                                                                               | Present                                         |
+==============================================+=====================================+===============+===========================================================================================+=================================================+
| RSID                                         | 8                                   | 0x69          | Positive Response: Authentication (0x29)                                                  | Always                                          |
+-------------+--------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                            | 0x0-0x1       | 0 = response required                                                                     | Always                                          |
|             |                                |                                     |               |                                                                                           |                                                 |
|             |                                |                                     |               | 1 = suppress positive response                                                            |                                                 |
|             +--------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
|             | authenticationTask             | 7 (b[6-0])                          | 0x05          | requestChallengeForAuthentication                                                         | Always                                          |
+-------------+--------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| authenticationReturnParameter                | 8                                   | 0x00-0xFF     | 0x00: RequestAccepted                                                                     | Always                                          |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x01: GeneralReject                                                                       |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x02: AuthenticationConfiguration                                                         |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography                        |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x04: AuthenticationConfiguration ACR with symmetric cryptography                         |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x05-0x0F: reserved                                                                       |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x10: DeAuthentication successful                                                         |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x11: CertificateVerified, OwnershipVerificationNecessary                                 |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x12: OwnershipVerified, AuthenticationComplete                                           |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x13: CertificateVerified                                                                 |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0x14-0x9F: reserved                                                                       |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0xA0-0xCF: vehicle manufacturer specific                                                  |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0xD0-0xFE: system supplier specific                                                       |                                                 |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | 0xFF: reserved                                                                            |                                                 |
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| algorithmIndicator                           | 128                                 |               | Indicates the algorithm used in the generating and verifying Proof of Ownership.          | Always                                          |
|                                              |                                     |               |                                                                                           |                                                 |
|                                              |                                     |               | This field is a 16 byte value containing the BER encoded OID value of the algorithm used. |                                                 |
|                                              |                                     |               | The value is left aligned and right padded with zero up to 16 bytes.                      |                                                 |
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| lengthOfChallengeServer                      | 16                                  | 0x0001-0xFFFF | Byte length of challengeServer Data Record.                                               | Always                                          |
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| challengeServer                              | 8*lengthOfChallengeServer           |               | Challenge generated by the server for the client.                                         | Always                                          |
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| lengthOfNeededAdditionalParameter            | 16                                  | 0x0000-0xFFFF | Byte length of neededAdditionalParameter Data Record.                                     | Always                                          |
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+
| neededAdditionalParameter                    | 8*lengthOfNeededAdditionalParameter |               | Indicate what additional parameters, if needed, are expected by the server.               | If lengthOfNeededAdditionalParameter unequals 0 |
+----------------------------------------------+-------------------------------------+---------------+-------------------------------------------------------------------------------------------+-------------------------------------------------+


.. _knowledge-base-service-authentication-06:

verifyProofOfOwnershipUnidirectional (0x06)
```````````````````````````````````````````
This sub-function can be used by the client to verify Proof of Ownership on the client side.


Request Format
''''''''''''''
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| Name                                         | Bit Length                       | Value         | Description                                                                                       | Present                                   |
+==============================================+==================================+===============+===================================================================================================+===========================================+
| SID                                          | 8                                | 0x29          | Authentication                                                                                    | Always                                    |
+-------------+--------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                         | 0x0-0x1       | 0 = response required                                                                             | Always                                    |
|             |                                |                                  |               |                                                                                                   |                                           |
|             |                                |                                  |               | 1 = suppress positive response                                                                    |                                           |
|             +--------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+                                           |
|             | authenticationTask             | 7 (b[6-0])                       | 0x06          | verifyProofOfOwnershipUnidirectional                                                              |                                           |
+-------------+--------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| algorithmIndicator                           | 128                              |               | Indicates the algorithm used in the generating and verifying Proof of Ownership.                  | Always                                    |
|                                              |                                  |               |                                                                                                   |                                           |
|                                              |                                  |               | This field is a 16 byte value containing the BER encoded OID value of the algorithm used.         |                                           |
|                                              |                                  |               | The value is left aligned and right padded with zero up to 16 bytes.                              |                                           |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| lengthOfProofOfOwnershipClient               | 16                               | 0x0001-0xFFFF | Byte length of proofOfOwnershipClient Data Record.                                                | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| proofOfOwnershipClient                       | 8*lengthOfProofOfOwnershipClient |               | Client's Proof of Ownership for the challenge value given by the server.                          | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| lengthOfChallengeClient                      | 16                               | 0x0000-0xFFFF | Byte length of challengeClient Data Record.                                                       | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| challengeClient                              | 8*lengthOfChallengeClient        |               | Challenge generated by the client for the server.                                                 | If lengthOfChallengeClient unequals 0     |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| lengthOfAdditionalParameter                  | 16                               | 0x0000-0xFFFF | Byte length of additionalParameter Data Record.                                                   | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| additionalParameter                          | 8*lengthOfAdditionalParameter    |               | The value of additional parameter that was indicated by the server via neededAdditionalParameter. | If lengthOfAdditionalParameter unequals 0 |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| Name                                         | Bit Length               | Value         | Description                                                                               | Present                              |
+==============================================+==========================+===============+===========================================================================================+======================================+
| RSID                                         | 8                        | 0x69          | Positive Response: Authentication (0x29)                                                  | Always                               |
+-------------+--------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                 | 0x0-0x1       | 0 = response required                                                                     | Always                               |
|             |                                |                          |               |                                                                                           |                                      |
|             |                                |                          |               | 1 = suppress positive response                                                            |                                      |
|             +--------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
|             | authenticationTask             | 7 (b[6-0])               | 0x06          | verifyProofOfOwnershipUnidirectional                                                      | Always                               |
+-------------+--------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| authenticationReturnParameter                | 8                        | 0x00-0xFF     | 0x00: RequestAccepted                                                                     | Always                               |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x01: GeneralReject                                                                       |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x02: AuthenticationConfiguration                                                         |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography                        |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x04: AuthenticationConfiguration ACR with symmetric cryptography                         |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x05-0x0F: reserved                                                                       |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x10: DeAuthentication successful                                                         |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x11: CertificateVerified, OwnershipVerificationNecessary                                 |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x12: OwnershipVerified, AuthenticationComplete                                           |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x13: CertificateVerified                                                                 |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0x14-0x9F: reserved                                                                       |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0xA0-0xCF: vehicle manufacturer specific                                                  |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0xD0-0xFE: system supplier specific                                                       |                                      |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | 0xFF: reserved                                                                            |                                      |
+----------------------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| algorithmIndicator                           | 128                      |               | Indicates the algorithm used in the generating and verifying Proof of Ownership.          | Always                               |
|                                              |                          |               |                                                                                           |                                      |
|                                              |                          |               | This field is a 16 byte value containing the BER encoded OID value of the algorithm used. |                                      |
|                                              |                          |               | The value is left aligned and right padded with zero up to 16 bytes.                      |                                      |
+----------------------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| lengthOfSessionKeyInfo                       | 16                       | 0x0000-0xFFFF | Byte length of sessionKeyInfo Data Record.                                                | Always                               |
+----------------------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| sessionKeyInfo                               | 8*lengthOfSessionKeyInfo |               | Session key information (e.g. encrypted session keys).                                    | If lengthOfSessionKeyInfo unequals 1 |
+----------------------------------------------+--------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+


.. _knowledge-base-service-authentication-07:

verifyProofOfOwnershipBidirectional (0x07)
``````````````````````````````````````````
This sub-function can be used by the client to verify Proof of Ownership on both client's and server's side.


Request Format
''''''''''''''
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| Name                                         | Bit Length                       | Value         | Description                                                                                       | Present                                   |
+==============================================+==================================+===============+===================================================================================================+===========================================+
| SID                                          | 8                                | 0x29          | Authentication                                                                                    | Always                                    |
+-------------+--------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                         | 0x0-0x1       | 0 = response required                                                                             | Always                                    |
|             |                                |                                  |               |                                                                                                   |                                           |
|             |                                |                                  |               | 1 = suppress positive response                                                                    |                                           |
|             +--------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+                                           |
|             | authenticationTask             | 7 (b[6-0])                       | 0x07          | verifyProofOfOwnershipBidirectional                                                               |                                           |
+-------------+--------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| algorithmIndicator                           | 128                              |               | Indicates the algorithm used in the generating and verifying Proof of Ownership.                  | Always                                    |
|                                              |                                  |               |                                                                                                   |                                           |
|                                              |                                  |               | This field is a 16 byte value containing the BER encoded OID value of the algorithm used.         |                                           |
|                                              |                                  |               | The value is left aligned and right padded with zero up to 16 bytes.                              |                                           |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| lengthOfProofOfOwnershipClient               | 16                               | 0x0001-0xFFFF | Byte length of proofOfOwnershipClient Data Record.                                                | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| proofOfOwnershipClient                       | 8*lengthOfProofOfOwnershipClient |               | Client's Proof of Ownership for the challenge value given by the server.                          | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| lengthOfChallengeClient                      | 16                               | 0x0001-0xFFFF | Byte length of challengeClient Data Record.                                                       | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| challengeClient                              | 8*lengthOfChallengeClient        |               | Challenge generated by the client for the server.                                                 | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| lengthOfAdditionalParameter                  | 16                               | 0x0000-0xFFFF | Byte length of additionalParameter Data Record.                                                   | Always                                    |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+
| additionalParameter                          | 8*lengthOfAdditionalParameter    |               | The value of additional parameter that was indicated by the server via neededAdditionalParameter. | If lengthOfAdditionalParameter unequals 0 |
+----------------------------------------------+----------------------------------+---------------+---------------------------------------------------------------------------------------------------+-------------------------------------------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| Name                                         | Bit Length                       | Value         | Description                                                                               | Present                              |
+==============================================+==================================+===============+===========================================================================================+======================================+
| RSID                                         | 8                                | 0x69          | Positive Response: Authentication (0x29)                                                  | Always                               |
+-------------+--------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])                         | 0x0-0x1       | 0 = response required                                                                     | Always                               |
|             |                                |                                  |               |                                                                                           |                                      |
|             |                                |                                  |               | 1 = suppress positive response                                                            |                                      |
|             +--------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
|             | authenticationTask             | 7 (b[6-0])                       | 0x07          | verifyProofOfOwnershipBidirectional                                                       | Always                               |
+-------------+--------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| authenticationReturnParameter                | 8                                | 0x00-0xFF     | 0x00: RequestAccepted                                                                     | Always                               |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x01: GeneralReject                                                                       |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x02: AuthenticationConfiguration                                                         |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography                        |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x04: AuthenticationConfiguration ACR with symmetric cryptography                         |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x05-0x0F: reserved                                                                       |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x10: DeAuthentication successful                                                         |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x11: CertificateVerified, OwnershipVerificationNecessary                                 |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x12: OwnershipVerified, AuthenticationComplete                                           |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x13: CertificateVerified                                                                 |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0x14-0x9F: reserved                                                                       |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0xA0-0xCF: vehicle manufacturer specific                                                  |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0xD0-0xFE: system supplier specific                                                       |                                      |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | 0xFF: reserved                                                                            |                                      |
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| algorithmIndicator                           | 128                              |               | Indicates the algorithm used in the generating and verifying Proof of Ownership.          | Always                               |
|                                              |                                  |               |                                                                                           |                                      |
|                                              |                                  |               | This field is a 16 byte value containing the BER encoded OID value of the algorithm used. |                                      |
|                                              |                                  |               | The value is left aligned and right padded with zero up to 16 bytes.                      |                                      |
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| lengthOfProofOfOwnershipServer               | 16                               | 0x0001-0xFFFF | Byte length of proofOfOwnershipServer Data Record.                                        | Always                               |
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| proofOfOwnershipServer                       | 8*lengthOfProofOfOwnershipServer |               | Proof of Ownership to be verified by the client.                                          | Always                               |
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| lengthOfSessionKeyInfo                       | 16                               | 0x0000-0xFFFF | Byte length of sessionKeyInfo Data Record.                                                | Always                               |
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+
| sessionKeyInfo                               | 8*lengthOfSessionKeyInfo         |               | Session key information (e.g. encrypted session keys).                                    | If lengthOfSessionKeyInfo unequals 1 |
+----------------------------------------------+----------------------------------+---------------+-------------------------------------------------------------------------------------------+--------------------------------------+


.. _knowledge-base-service-authentication-08:

authenticationConfiguration (0x08)
``````````````````````````````````
This sub-function can be used by the client to retrieve information about the current authentication configuration
and status.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x29    | Authentication                 | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+         |
|             | authenticationTask             | 7 (b[6-0]) | 0x08    | authenticationConfiguration    |         |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                                        | Present |
+==============================================+============+===========+====================================================================+=========+
| RSID                                         | 8          | 0x69      | Positive Response: Authentication (0x29)                           | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                              | Always  |
|             |                                |            |           |                                                                    |         |
|             |                                |            |           | 1 = suppress positive response                                     |         |
|             +--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
|             | authenticationTask             | 7 (b[6-0]) | 0x08      | authenticationConfiguration                                        | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------------------------------------------+---------+
| authenticationReturnParameter                | 8          | 0x00-0xFF | 0x00: RequestAccepted                                              | Always  |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x01: GeneralReject                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x02: AuthenticationConfiguration                                  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x03: AuthenticationConfiguration ACR with asymmetric cryptography |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x04: AuthenticationConfiguration ACR with symmetric cryptography  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x05-0x0F: reserved                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x10: DeAuthentication successful                                  |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x11: CertificateVerified, OwnershipVerificationNecessary          |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x12: OwnershipVerified, AuthenticationComplete                    |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x13: CertificateVerified                                          |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0x14-0x9F: reserved                                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xA0-0xCF: vehicle manufacturer specific                           |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xD0-0xFE: system supplier specific                                |         |
|                                              |            |           |                                                                    |         |
|                                              |            |           | 0xFF: reserved                                                     |         |
+----------------------------------------------+------------+-----------+--------------------------------------------------------------------+---------+


.. _knowledge-base-service-read-data-by-periodic-identifier:

ReadDataByPeriodicIdentifier (0x2A)
-----------------------------------
ReadDataByPeriodicIdentifier service allows the client to request periodic transmission of data record values from
the server.
Each periodic data record is identified by *Periodic DID* (the second byte of a DID with a fixed first byte 0xF2).


Request Format
``````````````
+------------------+------------+-----------+-----------------------------------------------+------------------------------------------+
| Name             | Bit Length | Value     | Description                                   | Present                                  |
+==================+============+===========+===============================================+==========================================+
| SID              | 8          | 0x2A      | ReadDataByPeriodicIdentifier                  | Always                                   |
+------------------+------------+-----------+-----------------------------------------------+------------------------------------------+
| transmissionMode | 8          | 0x00-0xFF | 0x00: reserved                                | Always                                   |
|                  |            |           |                                               |                                          |
|                  |            |           | 0x01: sendAtSlowRate                          |                                          |
|                  |            |           |                                               |                                          |
|                  |            |           | 0x02: sendAtMediumRate                        |                                          |
|                  |            |           |                                               |                                          |
|                  |            |           | 0x03: sendAtFastRate                          |                                          |
|                  |            |           |                                               |                                          |
|                  |            |           | 0x04: stopSending                             |                                          |
|                  |            |           |                                               |                                          |
|                  |            |           | 0x05-0xFF: reserved                           |                                          |
+------------------+------------+-----------+-----------------------------------------------+------------------------------------------+
| Periodic DID     | 8          | 0x00-0xFF | Second byte of DID#1 (first byte equals 0xF2) | Mandatory if transmissionMode unequals 4 |
|                  |            |           |                                               |                                          |
|                  |            |           |                                               | Optional if transmissionMode equals 4    |
|                  +------------+-----------+-----------------------------------------------+------------------------------------------+
|                  | ...                                                                                                               |
|                  +------------+-----------+-----------------------------------------------+------------------------------------------+
|                  | 8          | 0x00-0xFF | Second byte of DID#n (first byte equals 0xF2) | Optional                                 |
+------------------+------------+-----------+-----------------------------------------------+------------------------------------------+


Positive Response Format
````````````````````````
This service behaves differently from most diagnostic services because it produces two types of positive responses:

1) Initial confirmation response — sent immediately after the request
2) Ongoing periodic data messages — sent repeatedly according to the requested rate


Initial
'''''''
The first response (sent directly after the request):

+------+------------+-------+--------------------------------------------------------+---------+
| Name | Bit Length | Value | Description                                            | Present |
+======+============+=======+========================================================+=========+
| RSID | 8          | 0x6A  | Positive Response: ReadDataByPeriodicIdentifier (0x2A) | Always  |
+------+------------+-------+--------------------------------------------------------+---------+


Following
'''''''''
The following responses with data for Periodic Data Identifiers. Format according to ISO 14229:

+--------------+------------+-----------+---------------------------------------------+---------+
| Name         | Bit Length | Value     | Description                                 | Present |
+==============+============+===========+=============================================+=========+
| Periodic DID | 8          | 0x00-0xFF | Second byte of DID (first byte equals 0xF2) | Always  |
+--------------+------------+-----------+---------------------------------------------+---------+
| data         | at least 8 |           | Data stored under periodic DID              | Always  |
+--------------+------------+-----------+---------------------------------------------+---------+

.. warning:: The ISO-defined data message format introduces ambiguity because it does not begin with an RSID.
  This makes it impossible to reliably distinguish periodic data messages from other diagnostic messages.
  In my opinion this is a design flaw, and I have submitted feedback to the ISO committee in my country recommending
  that future revisions add an RSID at the start of each periodic data message.

This package uses an **extended, unambiguous** periodic message format that **always includes RSID 0x6A**:

+--------------+------------+-----------+--------------------------------------------------------+---------+
| Name         | Bit Length | Value     | Description                                            | Present |
+==============+============+===========+========================================================+=========+
| RSID         | 8          | 0x6A      | Positive Response: ReadDataByPeriodicIdentifier (0x2A) | Always  |
+--------------+------------+-----------+--------------------------------------------------------+---------+
| Periodic DID | 8          | 0x00-0xFF | Second byte of DID (first byte equals 0xF2)            | Always  |
+--------------+------------+-----------+--------------------------------------------------------+---------+
| data         | at least 8 |           | Data stored under periodic DID                         | Always  |
+--------------+------------+-----------+--------------------------------------------------------+---------+


.. _knowledge-base-service-dynamically-define-data-identifier:

DynamicallyDefineDataIdentifier (0x2C)
--------------------------------------
DynamicallyDefineDataIdentifier service allows the client to define a Data Identifier (DID) dynamically within
the server.
Once defined, the newly created DID can later be read using
:ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` or
:ref:`ReadDataByPeriodicIdentifier <knowledge-base-service-read-data-by-periodic-identifier>` services.

ISO 14229-1 defines the following DID definition types (definitionType parameter values):

- 0x01 – :ref:`defineByIdentifier <knowledge-base-service-dynamically-define-data-identifier-01>`
- 0x02 – :ref:`defineByMemoryAddress <knowledge-base-service-dynamically-define-data-identifier-02>`
- 0x03 – :ref:`clearDynamicallyDefinedDataIdentifier <knowledge-base-service-dynamically-define-data-identifier-03>`


Request Format
``````````````

.. _knowledge-base-service-dynamically-define-data-identifier-01:

defineByIdentifier (0x01)
'''''''''''''''''''''''''
This sub-function allows the client to define a new DID by concatenating data slices taken from existing DIDs.

The request may contain one or more *Data from DID* segments, each consisting of
(*sourceDataIdentifier*, *positionInSourceDataRecord*, *memorySize*).
Each segment selects a portion of an existing DID’s data record:

- *sourceDataIdentifier* identifies the DID whose data is referenced
- *positionInSourceDataRecord* specifies the starting byte position within that DID’s data record
  (index of the first byte = 1)
- *memorySize* defines the number of bytes to extract from that position

+------------------------------------------------+------------+---------------+---------------------------------+----------+
| Name                                           | Bit Length | Value         | Description                     | Present  |
+================================================+============+===============+=================================+==========+
| SID                                            | 8          | 0x2C          | DynamicallyDefineDataIdentifier | Always   |
+---------------+--------------------------------+------------+---------------+---------------------------------+----------+
| SubFunction   | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required           | Always   |
|               |                                |            |               |                                 |          |
|               |                                |            |               | 1 = suppress positive response  |          |
|               +--------------------------------+------------+---------------+---------------------------------+----------+
|               | definitionType                 | 7 (b[6-0]) | 0x01          | defineByIdentifier              | Always   |
+---------------+--------------------------------+------------+---------------+---------------------------------+----------+
| dynamicallyDefinedDataIdentifier               | 16         | 0xF200-0xF3FF | DID to define                   | Always   |
+---------------+--------------------------------+------------+---------------+---------------------------------+----------+
| Data from DID | sourceDataIdentifier           | 16         | 0x0000-0xFFFF | Source DID#1                    | Always   |
|               +--------------------------------+------------+---------------+---------------------------------+          |
|               | positionInSourceDataRecord     | 8          | 0x01-0xFF     | Data position in DID#1          |          |
|               +--------------------------------+------------+---------------+---------------------------------+          |
|               | memorySize                     | 8          | 0x01-0xFF     | Number of bytes from DID#1      |          |
|               +--------------------------------+------------+---------------+---------------------------------+----------+
|               | ...                                                                                                      |
|               +--------------------------------+------------+---------------+---------------------------------+----------+
|               | sourceDataIdentifier           | 16         | 0x0000-0xFFFF | Source DID#n                    | Optional |
|               +--------------------------------+------------+---------------+---------------------------------+          |
|               | positionInSourceDataRecord     | 8          | 0x01-0xFF     | Data position in DID#n          |          |
|               +--------------------------------+------------+---------------+---------------------------------+          |
|               | memorySize                     | 8          | 0x01-0xFF     | Number of bytes from DID#n      |          |
+---------------+--------------------------------+------------+---------------+---------------------------------+----------+


.. _knowledge-base-service-dynamically-define-data-identifier-02:

defineByMemoryAddress (0x02)
''''''''''''''''''''''''''''
This sub-function allows the client to define a new DID by referencing data directly from the server’s memory.

The *addressAndLengthFormatIdentifier* parameter specifies the number of bytes used to encode both
*memoryAddress* and *memorySize* within each memory segment.

The request may include one or more `Data from Memory` segments, with each segments consisting of
(*memoryAddress*, *memorySize*) and selecting a continuous region of memory to be included in the dynamically defined
DID:

- *memoryAddress* specifies the starting address of the memory block
- *memorySize* specifies the number of bytes to include from that address

+-------------------------------------------------------------------+-----------------------+---------------+-------------------------------------------+----------+
| Name                                                              | Bit Length            | Value         | Description                               | Present  |
+===================================================================+=======================+===============+===========================================+==========+
| SID                                                               | 8                     | 0x2C          | DynamicallyDefineDataIdentifier           | Always   |
+----------------------------------+--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
| SubFunction                      | suppressPosRspMsgIndicationBit | 1 (b[7])              | 0x0-0x1       | 0 = response required                     | Always   |
|                                  |                                |                       |               |                                           |          |
|                                  |                                |                       |               | 1 = suppress positive response            |          |
|                                  +--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
|                                  | definitionType                 | 7 (b[6-0])            | 0x02          | defineByMemoryAddress                     | Always   |
+----------------------------------+--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
| dynamicallyDefinedDataIdentifier                                  | 16                    | 0xF200-0xF3FF | DID to define                             | Always   |
+----------------------------------+--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
| addressAndLengthFormatIdentifier | memorySizeLength               | 4 (b[7-4])            | 0x1-0xF       | Number of bytes to use for memorySize     | Always   |
|                                  +--------------------------------+-----------------------+---------------+-------------------------------------------+          |
|                                  | memoryAddressLength            | 4 (b[3-0])            | 0x1-0xF       | Number of bytes to use for memoryAddress  |          |
+----------------------------------+--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
| Data from Memory                 | memoryAddress                  | 8*memoryAddressLength |               | Starting address#1 in the server's memory | Always   |
|                                  +--------------------------------+-----------------------+---------------+-------------------------------------------+          |
|                                  | memorySize                     | 8*memorySizeLength    |               | Number of bytes from address#1            |          |
|                                  +--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
|                                  | ...                                                                                                                           |
|                                  +--------------------------------+-----------------------+---------------+-------------------------------------------+----------+
|                                  | memoryAddress                  | 8*memoryAddressLength |               | Starting address#n in the server's memory | Optional |
|                                  +--------------------------------+-----------------------+---------------+-------------------------------------------+          |
|                                  | memorySize                     | 8*memorySizeLength    |               | Number of bytes from address#n            |          |
+----------------------------------+--------------------------------+-----------------------+---------------+-------------------------------------------+----------+


.. _knowledge-base-service-dynamically-define-data-identifier-03:

clearDynamicallyDefinedDataIdentifier (0x03)
''''''''''''''''''''''''''''''''''''''''''''
This sub-function clears previously defined dynamic DIDs.

If *dynamicallyDefinedDataIdentifier* parameter is present, only the specified dynamic DID is cleared.
If not provided, **all** dynamically defined DIDs stored in the server are cleared.

+----------------------------------------------+------------+---------------+---------------------------------------+----------+
| Name                                         | Bit Length | Value         | Description                           | Present  |
+==============================================+============+===============+=======================================+==========+
| SID                                          | 8          | 0x2C          | DynamicallyDefineDataIdentifier       | Always   |
+-------------+--------------------------------+------------+---------------+---------------------------------------+----------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                 | Always   |
|             |                                |            |               |                                       |          |
|             |                                |            |               | 1 = suppress positive response        |          |
|             +--------------------------------+------------+---------------+---------------------------------------+----------+
|             | definitionType                 | 7 (b[6-0]) | 0x03          | clearDynamicallyDefinedDataIdentifier | Always   |
+-------------+--------------------------------+------------+---------------+---------------------------------------+----------+
| dynamicallyDefinedDataIdentifier             | 16         | 0xF200-0xF3FF | DID to clear                          | Optional |
+----------------------------------------------+------------+---------------+---------------------------------------+----------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+---------------+-----------------------------------------------------------------+----------------------------------------------------------------+
| Name                                         | Bit Length | Value         | Description                                                     | Present                                                        |
+==============================================+============+===============+=================================================================+================================================================+
| RSID                                         | 8          | 0x6C          | Positive Response: DynamicallyDefineDataIdentifier(0x2C)        | Always                                                         |
+-------------+--------------------------------+------------+---------------+-----------------------------------------------------------------+----------------------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                                           | Always                                                         |
|             |                                |            |               |                                                                 |                                                                |
|             |                                |            |               | 1 = suppress positive response                                  |                                                                |
|             +--------------------------------+------------+---------------+-----------------------------------------------------------------+                                                                |
|             | definitionType                 | 7 (b[6-0]) | 0x00-0x7F     | 0x00: reserved                                                  |                                                                |
|             |                                |            |               |                                                                 |                                                                |
|             |                                |            |               | 0x01: defineByIdentifier                                        |                                                                |
|             |                                |            |               |                                                                 |                                                                |
|             |                                |            |               | 0x02: defineByMemoryAddress                                     |                                                                |
|             |                                |            |               |                                                                 |                                                                |
|             |                                |            |               | 0x03: clearDynamicallyDefinedDataIdentifier                     |                                                                |
|             |                                |            |               |                                                                 |                                                                |
|             |                                |            |               | 0x04-0x7F: safetySystemDiagnosticSession                        |                                                                |
+-------------+--------------------------------+------------+---------------+-----------------------------------------------------------------+----------------------------------------------------------------+
| dynamicallyDefinedDataIdentifier             | 16         | 0xF200-0xF3FF | Echo of dynamicallyDefinedDataIdentifier value from the request | If dynamicallyDefinedDataIdentifier was present in the request |
+----------------------------------------------+------------+---------------+-----------------------------------------------------------------+----------------------------------------------------------------+


.. _knowledge-base-service-write-data-by-identifier:

WriteDataByIdentifier (0x2E)
----------------------------
WriteDataByIdentifier service allows the client to write information into the server at an internal location
specified by the provided :ref:`DataIdentifier (DID) <knowledge-base-did>`.


Request Format
``````````````
+----------+------------+---------------+-----------------------+---------+
| Name     | Bit Length | Value         | Description           | Present |
+==========+============+===============+=======================+=========+
| SID      | 8          | 0x2E          | WriteDataByIdentifier | Always  |
+----------+------------+---------------+-----------------------+---------+
| DID      | 16         | 0x0000-0xFFFF | DID to update         | Always  |
+----------+------------+---------------+-----------------------+---------+
| DID data | at least 8 |               | Data to write         | Always  |
+----------+------------+---------------+-----------------------+---------+


Positive Response Format
````````````````````````
+------+------------+---------------+-------------------------------------------------+---------+
| Name | Bit Length | Value         | Description                                     | Present |
+======+============+===============+=================================================+=========+
| RSID | 8          | 0x6E          | Positive Response: WriteDataByIdentifier (0x2E) | Always  |
+------+------------+---------------+-------------------------------------------------+---------+
| DID  | 16         | 0x0000-0xFFFF | DID that was updated                            | Always  |
+------+------------+---------------+-------------------------------------------------+---------+


.. _knowledge-base-service-input-output-control-by-identifier:

InputOutputControlByIdentifier (0x2F)
-------------------------------------
InputOutputControlByIdentifier service allows the client to override an input value, internal server function value,
or force a specific output (actuator) value within the server.


Request Format
``````````````
The *inputOutputControlParameter* determines the type of control to apply:

- **0x00 – returnControlToECU**
  The server restores normal control of all values associated with the DID.

- **0x01 – resetToDefault**
  The server resets the controlled values to their default state.

- **0x02 – freezeCurrentState**
  The server freezes the current values (prevents them from changing).

- **0x03 – shortTermAdjustment**
  The server temporarily applies the value(s) provided by the client.

If the *controlEnableMask* Data Record is present, it specifies which parts of the DID's data are subject to control.
Each bit corresponds to the respective field in the DID structure:

- **1** – take control of this value
- **0** – leave this value under server control

If the *controlState* Data Record is present, it contains the value(s) to be set to the corresponding fields of the DID.

.. note:: The structure and length of *controlState* and *controlEnableMask* follow the structure of the DID’s data.

+-----------------------------+-----------------------------+---------------+--------------------------------------+-----------------------------------------+
| Name                        | Bit Length                  | Value         | Description                          | Present                                 |
+=============================+=============================+===============+======================================+=========================================+
| SID                         | 8                           | 0x2F          | InputOutputControlByIdentifier       | Always                                  |
+-----------------------------+-----------------------------+---------------+--------------------------------------+-----------------------------------------+
| DID                         | 16                          | 0x0000-0xFFFF | DID to control                       | Always                                  |
+-----------------------------+-----------------------------+---------------+--------------------------------------+-----------------------------------------+
| inputOutputControlParameter | 8                           | 0x00-0xFF     | 0x00: returnControlToECU             | Always                                  |
|                             |                             |               |                                      |                                         |
|                             |                             |               | 0x01: resetToDefault                 |                                         |
|                             |                             |               |                                      |                                         |
|                             |                             |               | 0x02: freezeCurrentState             |                                         |
|                             |                             |               |                                      |                                         |
|                             |                             |               | 0x03: shortTermAdjustment            |                                         |
|                             |                             |               |                                      |                                         |
|                             |                             |               | 0x04-0xFF: reserved                  |                                         |
+-----------------------------+-----------------------------+---------------+--------------------------------------+-----------------------------------------+
| controlState                | at least 8                  |               | Values to set in the DID             | If inputOutputControlParameter equals 3 |
+-----------------------------+-----------------------------+---------------+--------------------------------------+-----------------------------------------+
| controlEnableMask           | same as controlOptionRecord |               | Mask of values to control in the DID | Optional if controlState is present     |
+-----------------------------+-----------------------------+---------------+--------------------------------------+-----------------------------------------+


Positive Response Format
````````````````````````
The server responds with the DID and the *inputOutputControlParameter* echoed,
followed by the current values stored under the DID.
The *controlState* in the response is identical to what would be returned by
:ref:`ReadDataByIdentifier <knowledge-base-service-read-data-by-identifier>` service for the same DID.

+-----------------------------+------------+---------------+----------------------------------------------------------+---------+
| Name                        | Bit Length | Value         | Description                                              | Present |
+=============================+============+===============+==========================================================+=========+
| RSID                        | 8          | 0x6F          | Positive Response: InputOutputControlByIdentifier (0x2F) | Always  |
+-----------------------------+------------+---------------+----------------------------------------------------------+---------+
| DID                         | 16         | 0x0000-0xFFFF | DID                                                      | Always  |
+-----------------------------+------------+---------------+----------------------------------------------------------+---------+
| inputOutputControlParameter | 8          | 0x00-0xFF     | 0x00: returnControlToECU                                 | Always  |
|                             |            |               |                                                          |         |
|                             |            |               | 0x01: resetToDefault                                     |         |
|                             |            |               |                                                          |         |
|                             |            |               | 0x02: freezeCurrentState                                 |         |
|                             |            |               |                                                          |         |
|                             |            |               | 0x03: shortTermAdjustment                                |         |
|                             |            |               |                                                          |         |
|                             |            |               | 0x04-0xFF: reserved                                      |         |
+-----------------------------+------------+---------------+----------------------------------------------------------+---------+
| controlState                | at least 8 |               | Currently stored data under the DID                      | Always  |
+-----------------------------+------------+---------------+----------------------------------------------------------+---------+


.. _knowledge-base-service-routine-control:

RoutineControl (0x31)
---------------------
RoutineControl service allows the client to start, stop, or request the results of a routine
identified by a :ref:`RoutineIdentifier (RID) <knowledge-base-rid>`.
A routine is an ECU-implemented function that performs a defined sequence of actions to achieve a specific outcome.

Typical use cases include functions such as memory erasure, resetting or learning adaptive data, initiating
self-tests, or temporarily overriding the normal control strategy of the server.


Request Format
``````````````
+----------------------------------------------+------------+---------------+----------------------------------------+----------------------------------------------------+
| Name                                         | Bit Length | Value         | Description                            | Present                                            |
+==============================================+============+===============+========================================+====================================================+
| SID                                          | 8          | 0x31          | RoutineControl                         | Always                                             |
+-------------+--------------------------------+------------+---------------+----------------------------------------+----------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                  | Always                                             |
|             |                                |            |               |                                        |                                                    |
|             |                                |            |               | 1 = suppress positive response         |                                                    |
|             +--------------------------------+------------+---------------+----------------------------------------+                                                    |
|             | routineControlType             | 7 (b[6-0]) | 0x00-0x7F     | 0x00: reserved                         |                                                    |
|             |                                |            |               |                                        |                                                    |
|             |                                |            |               | 0x01: startRoutine                     |                                                    |
|             |                                |            |               |                                        |                                                    |
|             |                                |            |               | 0x02: stopRoutine                      |                                                    |
|             |                                |            |               |                                        |                                                    |
|             |                                |            |               | 0x03: requestRoutineResults            |                                                    |
|             |                                |            |               |                                        |                                                    |
|             |                                |            |               | 0x04-0x7F: reserved                    |                                                    |
+-------------+--------------------------------+------------+---------------+----------------------------------------+----------------------------------------------------+
| RID                                          | 16         | 0x0000-0xFFFF | Routine Identifier                     | Always                                             |
+----------------------------------------------+------------+---------------+----------------------------------------+----------------------------------------------------+
| routineControlOption                         | at least 8 |               | Additional routine specific parameters | Optional if routineControlType equals 0x01 or 0x02 |
+----------------------------------------------+------------+---------------+----------------------------------------+----------------------------------------------------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+---------------+------------------------------------------+------------------------------------------+
| Name                                         | Bit Length | Value         | Description                              | Present                                  |
+==============================================+============+===============+==========================================+==========================================+
| RSID                                         | 8          | 0x71          | Positive Response: RoutineControl (0x31) | Always                                   |
+-------------+--------------------------------+------------+---------------+------------------------------------------+------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                    | Always                                   |
|             |                                |            |               |                                          |                                          |
|             |                                |            |               | 1 = suppress positive response           |                                          |
|             +--------------------------------+------------+---------------+------------------------------------------+                                          |
|             | routineControlType             | 7 (b[6-0]) | 0x00-0x7F     | 0x00: reserved                           |                                          |
|             |                                |            |               |                                          |                                          |
|             |                                |            |               | 0x01: startRoutine                       |                                          |
|             |                                |            |               |                                          |                                          |
|             |                                |            |               | 0x02: stopRoutine                        |                                          |
|             |                                |            |               |                                          |                                          |
|             |                                |            |               | 0x03: requestRoutineResults              |                                          |
|             |                                |            |               |                                          |                                          |
|             |                                |            |               | 0x04-0x7F: reserved                      |                                          |
+-------------+--------------------------------+------------+---------------+------------------------------------------+------------------------------------------+
| RID                                          | 16         | 0x0000-0xFFFF | Routine Identifier                       | Always                                   |
+----------------------------------------------+------------+---------------+------------------------------------------+------------------------------------------+
| routineStatus                                | at least 8 |               | Routine specific status information      | Mandatory if routineControlType equals 3 |
|                                              |            |               |                                          |                                          |
|                                              |            |               |                                          | Optional otherwise                       |
+----------------------------------------------+------------+---------------+------------------------------------------+------------------------------------------+

.. warning:: ISO 14229-1 distinguishes two optional parameters in the positive response: *routineInfo* and *routineStatus*.
  However, ISO does not define the content, format, or conditions of use for either field for any standardised RID.
  Because both fields are entirely vehicle-manufacturer–specific, this documentation simplifies the model by combining
  them into a single parameter named *routineStatus*.
  This has no functional impact and avoids implying that ISO provides a fixed structure for either field.


.. _knowledge-base-service-request-download:

RequestDownload (0x34)
----------------------
RequestDownload service allows the client to initiate a download sequence, where data is transferred from
the client to the server.

.. note:: Download means that the server is the receiver and the client is the sender.


Request Format
``````````````
+--------------------------------------------------------+-----------------------+---------+-----------------------------------------------------+---------+
| Name                                                   | Bit Length            | Value   | Description                                         | Present |
+========================================================+=======================+=========+=====================================================+=========+
| SID                                                    | 8                     | 0x34    | RequestDownload                                     | Always  |
+----------------------------------+---------------------+-----------------------+---------+-----------------------------------------------------+---------+
| dataFormatIdentifier             | compressionMethod   | 4 (b[7-4])            | 0x0-0xF | 0x0 - no compression                                | Always  |
|                                  |                     |                       |         |                                                     |         |
|                                  |                     |                       |         | 0x1-0xF - vehicle manufacturer specific compression |         |
|                                  +---------------------+-----------------------+---------+-----------------------------------------------------+         |
|                                  | encryptingMethod    | 4 (b[3-0])            | 0x0-0xF | 0x0 - no encryption                                 |         |
|                                  |                     |                       |         |                                                     |         |
|                                  |                     |                       |         | 0x1-0xF - vehicle manufacturer specific encryption  |         |
+----------------------------------+---------------------+-----------------------+---------+-----------------------------------------------------+---------+
| addressAndLengthFormatIdentifier | memorySizeLength    | 4                     | 0x1-0xF | Number of bytes to use for memorySize               | Always  |
|                                  +---------------------+-----------------------+---------+-----------------------------------------------------+         |
|                                  | memoryAddressLength | 4                     | 0x1-0xF | Number of bytes to use for memoryAddress            |         |
+----------------------------------+---------------------+-----------------------+---------+-----------------------------------------------------+---------+
| memoryAddress                                          | 8*memoryAddressLength |         | Starting address in the server’s memory             | Always  |
+--------------------------------------------------------+-----------------------+---------+-----------------------------------------------------+---------+
| memorySize                                             | 8*memorySizeLength    |         | Number of bytes to download                         | Always  |
+--------------------------------------------------------+-----------------------+---------+-----------------------------------------------------+---------+


Positive Response Format
````````````````````````
+------------------------------------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+
| Name                                                       | Bit Length                          | Value   | Description                                                                 | Present |
+============================================================+=====================================+=========+=============================================================================+=========+
| RSID                                                       | 8                                   | 0x74    | Positive Response: RequestDownload (0x34)                                   | Always  |
+------------------------+-----------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+
| lengthFormatIdentifier | maxNumberOfBlockLengthBytesNumber | 4 (b[7-4])                          | 0x1-0xF | Number of bytes to use for maxNumberOfBlockLength                           | Always  |
|                        +-----------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+         |
|                        | reserved                          | 4 (b[3-0])                          | 0x0     | Reserved by ISO 14229 for future definition                                 |         |
+------------------------+-----------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+
| maxNumberOfBlockLength                                     | 8*maxNumberOfBlockLengthBytesNumber |         | Maximal TransferData message length that this server is capable of handling | Always  |
+------------------------------------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+

.. warning:: The *reserved* value shall be equal to 0.

.. note:: The *maxNumberOfBlockLength* value specifies the maximum permitted size of the complete TransferData request
  that the server supports, including *SID* and *blockSequenceCounter* Data Records.


.. _knowledge-base-service-request-upload:

RequestUpload (0x35)
--------------------
RequestUpload service allows the client to initiate an upload sequence, where data is transferred from
the server to the client.

.. note:: Upload means that the server is the sender and the client is the receiver.


Request Format
``````````````
+--------------------------------------------------------+-----------------------+---------+-----------------------------------------------------+---------+
| Name                                                   | Bit Length            | Value   | Description                                         | Present |
+========================================================+=======================+=========+=====================================================+=========+
| SID                                                    | 8                     | 0x35    | RequestUpload                                       | Always  |
+----------------------------------+---------------------+-----------------------+---------+-----------------------------------------------------+---------+
| dataFormatIdentifier             | compressionMethod   | 4 (b[7-4])            | 0x0-0xF | 0x0 - no compression                                | Always  |
|                                  |                     |                       |         |                                                     |         |
|                                  |                     |                       |         | 0x1-0xF - vehicle manufacturer specific compression |         |
|                                  +---------------------+-----------------------+---------+-----------------------------------------------------+         |
|                                  | encryptingMethod    | 4 (b[3-0])            | 0x0-0xF | 0x0 - no encryption                                 |         |
|                                  |                     |                       |         |                                                     |         |
|                                  |                     |                       |         | 0x1-0xF - vehicle manufacturer specific encryption  |         |
+----------------------------------+---------------------+-----------------------+---------+-----------------------------------------------------+---------+
| addressAndLengthFormatIdentifier | memorySizeLength    | 4                     | 0x1-0xF | Number of bytes to use for memorySize               | Always  |
|                                  +---------------------+-----------------------+---------+-----------------------------------------------------+         |
|                                  | memoryAddressLength | 4                     | 0x1-0xF | Number of bytes to use for memoryAddress            |         |
+----------------------------------+---------------------+-----------------------+---------+-----------------------------------------------------+---------+
| memoryAddress                                          | 8*memoryAddressLength |         | Starting address in the server’s memory             | Always  |
+--------------------------------------------------------+-----------------------+---------+-----------------------------------------------------+---------+
| memorySize                                             | 8*memorySizeLength    |         | Number of bytes to upload                           | Always  |
+--------------------------------------------------------+-----------------------+---------+-----------------------------------------------------+---------+


Positive Response Format
````````````````````````
+------------------------------------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+
| Name                                                       | Bit Length                          | Value   | Description                                                                 | Present |
+============================================================+=====================================+=========+=============================================================================+=========+
| RSID                                                       | 8                                   | 0x75    | Positive Response: RequestUpload (0x35)                                     | Always  |
+------------------------+-----------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+
| lengthFormatIdentifier | maxNumberOfBlockLengthBytesNumber | 4 (b[7-4])                          | 0x1-0xF | Number of bytes to use for maxNumberOfBlockLength                           | Always  |
|                        +-----------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+         |
|                        | reserved                          | 4 (b[3-0])                          | 0x0     | Reserved by ISO 14229 for future definition                                 |         |
+------------------------+-----------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+
| maxNumberOfBlockLength                                     | 8*maxNumberOfBlockLengthBytesNumber |         | Maximal TransferData message length that this server is capable of handling | Always  |
+------------------------------------------------------------+-------------------------------------+---------+-----------------------------------------------------------------------------+---------+

.. warning:: The *reserved* value shall be equal to 0.

.. note:: The *maxNumberOfBlockLength* value specifies the maximum permitted size of the complete TransferData response
  that the server supports, including *RSID* and *blockSequenceCounter* Data Records.


.. _knowledge-base-service-transfer-data:

TransferData (0x36)
-------------------
TransferData service is used during both download and upload sequences to transfer blocks of data.

The *blockSequenceCounter* is used by the server to detect message repetition or loss. Its initial value is 1,
and it is incremented with each subsequent message. After reaching 0xFF, it rolls over to 0x00.

Request Format
``````````````
+--------------------------+------------+-----------+-------------------------+------------------------------+
| Name                     | Bit Length | Value     | Description             | Present                      |
+==========================+============+===========+=========================+==============================+
| SID                      | 8          | 0x36      | TransferData            | Always                       |
+--------------------------+------------+-----------+-------------------------+------------------------------+
| blockSequenceCounter     | 8          | 0x00-0xFF | Message counter         | Always                       |
+--------------------------+------------+-----------+-------------------------+------------------------------+
| transferRequestParameter | at least 8 |           | Data sent by the client | If a download is in progress |
+--------------------------+------------+-----------+-------------------------+------------------------------+


Positive Response Format
````````````````````````
+---------------------------+------------+-----------+----------------------------------------+-----------------------------+
| Name                      | Bit Length | Value     | Description                            | Present                     |
+===========================+============+===========+========================================+=============================+
| RSID                      | 8          | 0x76      | Positive Response: TransferData (0x36) | Always                      |
+---------------------------+------------+-----------+----------------------------------------+-----------------------------+
| blockSequenceCounter      | 8          | 0x00-0xFF | Message counter                        | Always                      |
+---------------------------+------------+-----------+----------------------------------------+-----------------------------+
| transferResponseParameter | at least 8 |           | Data sent by the server                | If an upload is in progress |
+---------------------------+------------+-----------+----------------------------------------+-----------------------------+


.. _knowledge-base-service-request-transfer-exit:

RequestTransferExit (0x37)
--------------------------
RequestTransferExit service is used by the client to terminate a data transfer between the client and server.


Request Format
``````````````
+--------------------------+------------+-------+-------------------------------------------------+----------+
| Name                     | Bit Length | Value | Description                                     | Present  |
+==========================+============+=======+=================================================+==========+
| SID                      | 8          | 0x37  | RequestTransferExit                             | Always   |
+--------------------------+------------+-------+-------------------------------------------------+----------+
| transferRequestParameter | at least 8 |       | Additional vehicle manufacturer specific values | Optional |
+--------------------------+------------+-------+-------------------------------------------------+----------+


Positive Response Format
````````````````````````
+---------------------------+------------+-------+-------------------------------------------------+----------+
| Name                      | Bit Length | Value | Description                                     | Present  |
+===========================+============+=======+=================================================+==========+
| RSID                      | 8          | 0x77  | Positive Response: RequestTransferExit (0x37)   | Always   |
+---------------------------+------------+-------+-------------------------------------------------+----------+
| transferResponseParameter | at least 8 |       | Additional vehicle manufacturer specific values | Optional |
+---------------------------+------------+-------+-------------------------------------------------+----------+


.. _knowledge-base-service-request-file-transfer:

RequestFileTransfer (0x38)
--------------------------
RequestFileTransfer service provides an alternative to :ref:`RequestDownload <knowledge-base-service-request-download>`
and :ref:`RequestUpload <knowledge-base-service-request-upload>` services.
Unlike RequestDownload and RequestUpload, which operate on memory addresses,
RequestFileTransfer operates on files identified by their paths and names.

It allows the client to request a range of file-related operations, such as adding, deleting, replacing, reading,
or resuming access to files, as well as retrieving directory information.


Request Format
``````````````
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+
| Name                                     | Bit Length                | Value         | Description                                                            | Present                                |
+==========================================+===========================+===============+========================================================================+========================================+
| SID                                      | 8                         | 0x38          | RequestFileTransfer                                                    | Always                                 |
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+
| modeOfOperation                          | 8                         | 0x00-0xFF     | 0x00: reserved                                                         | Always                                 |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x01: AddFile                                                          |                                        |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x02: DeleteFile                                                       |                                        |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x03: ReplaceFile                                                      |                                        |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x04: ReadFile                                                         |                                        |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x05: ReadDir                                                          |                                        |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x06: ResumeFile                                                       |                                        |
|                                          |                           |               |                                                                        |                                        |
|                                          |                           |               | 0x07-0xFF: reserved                                                    |                                        |
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+
| filePathAndNameLength                    | 16                        | 0x0001-0xFFFF | Number of bytes to use for filePathAndName                             | Always                                 |
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+
| filePathAndName                          | 8*filePathAndNameLength   |               | Path to the file/directory                                             | Always                                 |
+----------------------+-------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+
| dataFormatIdentifier | compressionMethod | 4 (b[7-4])                | 0x0-0xF       | 0x0 - no compression                                                   | If modeOfOperation equals 1, 3, 4 or 6 |
|                      |                   |                           |               |                                                                        |                                        |
|                      |                   |                           |               | 0x1-0xF - vehicle manufacturer specific compression                    |                                        |
|                      +-------------------+---------------------------+---------------+------------------------------------------------------------------------+                                        |
|                      | encryptingMethod  | 4 (b[3-0])                | 0x0-0xF       | 0x0 - no encryption                                                    |                                        |
|                      |                   |                           |               |                                                                        |                                        |
|                      |                   |                           |               | 0x1-0xF - vehicle manufacturer specific encryption                     |                                        |
+----------------------+-------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+
| fileSizeParameterLength                  | 8                         | 0x01-0xFF     | Number of bytes to use for fileSizeUnCompressed and fileSizeCompressed | If modeOfOperation equals 1, 3 or 6    |
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+                                        |
| fileSizeUnCompressed                     | 8*fileSizeParameterLength |               | The size of the uncompressed file in bytes                             |                                        |
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+                                        |
| fileSizeCompressed                       | 8*fileSizeParameterLength |               | The size of the compressed file in bytes                               |                                        |
+------------------------------------------+---------------------------+---------------+------------------------------------------------------------------------+----------------------------------------+

.. warning:: Value 0x06 [ResumeFile] of *modeOfOperation* was introduced in ISO 14229-1:2020 and it was absent in ISO 14229-1:2013.


Positive Response Format
````````````````````````
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| Name                                     | Bit Length                          | Value         | Description                                                                           | Present                                    |
+==========================================+=====================================+===============+=======================================================================================+============================================+
| RSID                                     | 8                                   | 0x78          | Positive Response: RequestFileTransfer (0x38)                                         | Always                                     |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| modeOfOperation                          | 8                                   | 0x00-0xFF     | 0x00: reserved                                                                        | Always                                     |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x01: AddFile                                                                         |                                            |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x02: DeleteFile                                                                      |                                            |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x03: ReplaceFile                                                                     |                                            |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x04: ReadFile                                                                        |                                            |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x05: ReadDir                                                                         |                                            |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x06: ResumeFile                                                                      |                                            |
|                                          |                                     |               |                                                                                       |                                            |
|                                          |                                     |               | 0x07-0xFF: reserved                                                                   |                                            |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| lengthFormatIdentifier                   | 8                                   | 0x01-0xFF     | Number of bytes to use for maxNumberOfBlockLength                                     | If modeOfOperation equals 1, 3, 4, 5 or 6  |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+                                            |
| maxNumberOfBlockLength                   | 8*maxNumberOfBlockLengthBytesNumber |               | Maximal TransferData message length that this server is capable of handling           |                                            |
+----------------------+-------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| dataFormatIdentifier | compressionMethod | 4 (b[7-4])                          | 0x0-0xF       | 0x0 - no compression                                                                  | If modeOfOperation equals 1, 3, 4, 5, or 6 |
|                      |                   |                                     |               |                                                                                       |                                            |
|                      |                   |                                     |               | 0x1-0xF - vehicle manufacturer specific compression                                   |                                            |
|                      +-------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+                                            |
|                      | encryptingMethod  | 4 (b[3-0])                          | 0x0-0xF       | 0x0 - no encryption                                                                   |                                            |
|                      |                   |                                     |               |                                                                                       |                                            |
|                      |                   |                                     |               | 0x1-0xF - vehicle manufacturer specific encryption                                    |                                            |
+----------------------+-------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| fileSizeOrDirInfoParameterLength         | 16                                  | 0x0001-0xFFFF | Number of bytes to use for fileSizeUncompressedOrDirInfoLength and fileSizeCompressed | If modeOfOperation equals 4 or 5           |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| fileSizeUncompressedOrDirInfoLength      | 8*fileSizeOrDirInfoParameterLength  |               | The size of the uncompressed file (or directory) in bytes                             | If modeOfOperation equals 4 or 5           |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| fileSizeCompressed                       | 8*fileSizeOrDirInfoParameterLength  |               | The size of the compressed file in bytes                                              | If modeOfOperation equals 4                |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+
| filePosition                             | 64                                  |               | The byte position to resume downloading after initial download was suspended          | If modeOfOperation equals 6                |
+------------------------------------------+-------------------------------------+---------------+---------------------------------------------------------------------------------------+--------------------------------------------+

.. note:: Parameter *dataFormatIdentifier* shall equal 0x00 [no compression, no encryption] if modeOfOperation equals 0x05 [ReadDir].

.. warning:: Value 0x06 [ResumeFile] of *modeOfOperation* was introduced in ISO 14229-1:2020 and it was absent in ISO 14229-1:2013.


.. _knowledge-base-service-write-memory-by-address:

WriteMemoryByAddress (0x3D)
---------------------------
WriteMemoryByAddress service allows the client to write information into server's memory data under provided
memory address.


Request Format
``````````````
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+
| Name                                                   | Bit Length            | Value   | Description                              | Present |
+========================================================+=======================+=========+==========================================+=========+
| SID                                                    | 8                     | 0x3D    | WriteMemoryByAddress                     | Always  |
+----------------------------------+---------------------+-----------------------+---------+------------------------------------------+---------+
| addressAndLengthFormatIdentifier | memorySizeLength    | 4 (b[7-4])            | 0x1-0xF | Number of bytes to use for memorySize    | Always  |
|                                  +---------------------+-----------------------+---------+------------------------------------------+         |
|                                  | memoryAddressLength | 4 (b[3-0])            | 0x1-0xF | Number of bytes to use for memoryAddress |         |
+----------------------------------+---------------------+-----------------------+---------+------------------------------------------+---------+
| memoryAddress                                          | 8*memoryAddressLength |         | Starting address in the server's memory  | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+
| memorySize                                             | 8*memorySizeLength    |         | Number of bytes to write                 | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+
| data                                                   | 8*memorySize          |         | Data to write to server's memory         | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------+---------+


Positive Response Format
````````````````````````
+--------------------------------------------------------+-----------------------+---------+------------------------------------------------+---------+
| Name                                                   | Bit Length            | Value   | Description                                    | Present |
+========================================================+=======================+=========+================================================+=========+
| RSID                                                   | 8                     | 0x7D    | Positive Response: WriteMemoryByAddress (0x3D) | Always  |
+----------------------------------+---------------------+-----------------------+---------+------------------------------------------------+---------+
| addressAndLengthFormatIdentifier | memorySizeLength    | 4 (b[7-4])            | 0x1-0xF | Number of bytes to use for memorySize          | Always  |
|                                  +---------------------+-----------------------+---------+------------------------------------------------+         |
|                                  | memoryAddressLength | 4 (b[3-0])            | 0x1-0xF | Number of bytes to use for memoryAddress       |         |
+----------------------------------+---------------------+-----------------------+---------+------------------------------------------------+---------+
| memoryAddress                                          | 8*memoryAddressLength |         | Starting address in the server's memory        | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------------+---------+
| memorySize                                             | 8*memorySizeLength    |         | Number of bytes that were written              | Always  |
+--------------------------------------------------------+-----------------------+---------+------------------------------------------------+---------+


.. _knowledge-base-service-tester-present:

TesterPresent (0x3E)
--------------------
TesterPresent service is used by the client to indicate to the server that the diagnostic tester is still
present on the communication bus.
Reception of this service prevents the server’s :ref:`S3Server <knowledge-base-s3-server>` timer from expiring,
thereby extending the active diagnostic session.

.. note:: From the server’s implementation perspective, TesterPresent does not perform any diagnostic action.
   Reception of **any** diagnostic request (TesterPresent or otherwise) resets/extends the S3\ :sub:`Server` timer.


Request Format
``````````````
+----------------------------------------------+------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                    | Present |
+==============================================+============+===========+================================+=========+
| SID                                          | 8          | 0x3E      | TesterPresent                  | Always  |
+-------------+--------------------------------+------------+-----------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required          | Always  |
|             |                                |            |           |                                |         |
|             |                                |            |           | 1 = suppress positive response |         |
|             +--------------------------------+------------+-----------+--------------------------------+         |
|             | zeroSubFunction                | 7 (b[6-0]) | 0x00-0x7F | 0x00: zeroSubFunction          |         |
|             |                                |            |           |                                |         |
|             |                                |            |           | 0x01-0x7F: reserved            |         |
+-------------+--------------------------------+------------+-----------+--------------------------------+---------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| RSID                                         | 8          | 0x7E      | Positive Response: TesterPresent (0x3E) | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+         |
|             | zeroSubFunction                | 7 (b[6-0]) | 0x00-0x7F | 0x00: zeroSubFunction                   |         |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 0x01-0x7F: reserved                     |         |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+


.. _knowledge-base-service-access-timing-parameter:

AccessTimingParameter (0x83)
----------------------------
AccessTimingParameter service is used by the client to read or modify the timing parameters of
the diagnostic communication link.

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
``````````````
+----------------------------------------------+------------+-----------+-------------------------------------------+---------------------------------------+
| Name                                         | Bit Length | Value     | Description                               | Present                               |
+==============================================+============+===========+===========================================+=======================================+
| SID                                          | 8          | 0x83      | AccessTimingParameter                     | Always                                |
+-------------+--------------------------------+------------+-----------+-------------------------------------------+---------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                     | Always                                |
|             |                                |            |           |                                           |                                       |
|             |                                |            |           | 1 = suppress positive response            |                                       |
|             +--------------------------------+------------+-----------+-------------------------------------------+                                       |
|             | timingParameterAccessType      | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                            |                                       |
|             |                                |            |           |                                           |                                       |
|             |                                |            |           | 0x01: readExtendedTimingParameterSet      |                                       |
|             |                                |            |           |                                           |                                       |
|             |                                |            |           | 0x02: setTimingParametersToDefaultValues  |                                       |
|             |                                |            |           |                                           |                                       |
|             |                                |            |           | 0x03: readCurrentlyActiveTimingParameters |                                       |
|             |                                |            |           |                                           |                                       |
|             |                                |            |           | 0x04: setTimingParametersToGivenValues    |                                       |
|             |                                |            |           |                                           |                                       |
|             |                                |            |           | 0x05–0x7F: reserved                       |                                       |
+-------------+--------------------------------+------------+-----------+-------------------------------------------+---------------------------------------+
| TimingParameterRequestRecord                 | at least 8 |           | Values of the timing parameter to set     | If timingParameterAccessType equals 4 |
+----------------------------------------------+------------+-----------+-------------------------------------------+---------------------------------------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+-----------+-------------------------------------------------+--------------------------------------------+
| Name                                         | Bit Length | Value     | Description                                     | Present                                    |
+==============================================+============+===========+=================================================+============================================+
| RSID                                         | 8          | 0xC3      | Positive Response: AccessTimingParameter (0x83) | Always                                     |
+-------------+--------------------------------+------------+-----------+-------------------------------------------------+--------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                           | Always                                     |
|             |                                |            |           |                                                 |                                            |
|             |                                |            |           | 1 = suppress positive response                  |                                            |
|             +--------------------------------+------------+-----------+-------------------------------------------------+                                            |
|             | timingParameterAccessType      | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                                  |                                            |
|             |                                |            |           |                                                 |                                            |
|             |                                |            |           | 0x01: readExtendedTimingParameterSet            |                                            |
|             |                                |            |           |                                                 |                                            |
|             |                                |            |           | 0x02: setTimingParametersToDefaultValues        |                                            |
|             |                                |            |           |                                                 |                                            |
|             |                                |            |           | 0x03: readCurrentlyActiveTimingParameters       |                                            |
|             |                                |            |           |                                                 |                                            |
|             |                                |            |           | 0x04: setTimingParametersToGivenValues          |                                            |
|             |                                |            |           |                                                 |                                            |
|             |                                |            |           | 0x05–0x7F: reserved                             |                                            |
+-------------+--------------------------------+------------+-----------+-------------------------------------------------+--------------------------------------------+
| TimingParameterResponseRecord                | at least 8 |           | Values of the read timing parameter             | If timingParameterAccessType equals 1 or 3 |
+----------------------------------------------+------------+-----------+-------------------------------------------------+--------------------------------------------+


.. _knowledge-base-service-secured-data-transmission:

SecuredDataTransmission (0x84)
------------------------------
SecuredDataTransmission service is applicable if a client intends to use diagnostic services defined
in this document in a secured mode. It may also be used to transmit external data, which conform to
some other application protocol, in a secured mode between a client and a server. A secured mode in
this context means that the data transmitted is protected by cryptographic methods.


Request Format
``````````````


ISO 14229-1:2020
''''''''''''''''
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Name                                                               | Bit Length         | Value         | Description                                              | Present                 |
+====================================================================+====================+===============+==========================================================+=========================+
| SID                                                                | 8                  | 0x84          | SecuredDataTransmission                                  | Always                  |
+--------------------------+-----------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Administrative Parameter | reserved                                | 9 (b[7-0] + b[7])  | 0x000         | Reserved by ISO 14229                                    | Always                  |
|                          +-----------------------------------------+--------------------+---------------+----------------------------------------------------------+                         |
|                          | Signature on the response is requested. | 1 (b[6])           | 0x0-0x1       | 1 = yes                                                  |                         |
|                          |                                         |                    |               |                                                          |                         |
|                          |                                         |                    |               | 0 = no                                                   |                         |
|                          +-----------------------------------------+--------------------+---------------+----------------------------------------------------------+                         |
|                          | Message is signed.                      | 1 (b[5])           | 0x0-0x1       | 1 = yes                                                  |                         |
|                          |                                         |                    |               |                                                          |                         |
|                          |                                         |                    |               | 0 = no                                                   |                         |
|                          +-----------------------------------------+--------------------+---------------+----------------------------------------------------------+                         |
|                          | Message is encrypted.                   | 1 (b[4])           | 0x0-0x1       | 1 = yes                                                  |                         |
|                          |                                         |                    |               |                                                          |                         |
|                          |                                         |                    |               | 0 = no                                                   |                         |
|                          +-----------------------------------------+--------------------+---------------+----------------------------------------------------------+                         |
|                          | A pre-established key is used.          | 1 (b[3])           | 0x0-0x1       | 1 = yes                                                  |                         |
|                          |                                         |                    |               |                                                          |                         |
|                          |                                         |                    |               | 0 = no                                                   |                         |
|                          +-----------------------------------------+--------------------+---------------+----------------------------------------------------------+                         |
|                          | reserved                                | 2 (b[2-1])         | 0x0           | Reserved by ISO 14229                                    |                         |
|                          +-----------------------------------------+--------------------+---------------+----------------------------------------------------------+                         |
|                          | Message is request message.             | 1 (b[0])           | 0x1           | 1 = yes                                                  |                         |
+--------------------------+-----------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Signature/Encryption Calculation                                   | 8                  | 0x00-0xFF     | 0x00-0x7F: vehicle manufacturer specific                 | Always                  |
|                                                                    |                    |               |                                                          |                         |
|                                                                    |                    |               | 0x80-0x8F: system supplier specific                      |                         |
|                                                                    |                    |               |                                                          |                         |
|                                                                    |                    |               | 0x90-0xFF: reserved                                      |                         |
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Signature Length                                                   | 16                 | 0x0000-0xFFFF | Number of bytes to use for Signature/MAC Byte            | Always                  |
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Anti-replay Counter                                                | 16                 | 0x0000-0xFFFF | An incrementing counter to prevent a replay attack.      | Always                  |
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Internal Message Service Request ID                                | 8                  | 0x00-0xFF     | Request SID value (might be encrypted)                   | Always                  |
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Service Specific Parameters                                        | at least 8         |               | The following request message bytes (might be encrypted) | Optional                |
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+
| Signature/MAC                                                      | 8*Signature Length |               | Message signature                                        | If Signature Length > 0 |
+--------------------------------------------------------------------+--------------------+---------------+----------------------------------------------------------+-------------------------+


ISO 14229-1:2013
''''''''''''''''
+---------------------------+------------+-------+---------------------------+---------+
| Name                      | Bit Length | Value | Description               | Present |
+===========================+============+=======+===========================+=========+
| SID                       | 8          | 0x84  | SecuredDataTransmission   | Always  |
+---------------------------+------------+-------+---------------------------+---------+
| securityDataRequestRecord | at least 8 |       | Encrypted request message | Always  |
+---------------------------+------------+-------+---------------------------+---------+


Positive Response Format
````````````````````````


ISO 14229-1:2020
''''''''''''''''
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Name                                                               | Bit Length         | Value         | Description                                               | Present                 |
+====================================================================+====================+===============+===========================================================+=========================+
| RSID                                                               | 8                  | 0xC4          | Positive Response: SecuredDataTransmission (0x84)         | Always                  |
+--------------------------+-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Administrative Parameter | reserved                                | 9 (b[7-0] + b[7])  | 0x000         | Reserved by ISO 14229                                     | Always                  |
|                          +-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+                         |
|                          | Signature on the response is requested. | 1 (b[6])           | 0x0-0x1       | 1 = yes                                                   |                         |
|                          |                                         |                    |               |                                                           |                         |
|                          |                                         |                    |               | 0 = no                                                    |                         |
|                          +-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+                         |
|                          | Message is signed.                      | 1 (b[5])           | 0x0-0x1       | 1 = yes                                                   |                         |
|                          |                                         |                    |               |                                                           |                         |
|                          |                                         |                    |               | 0 = no                                                    |                         |
|                          +-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+                         |
|                          | Message is encrypted.                   | 1 (b[4])           | 0x0-0x1       | 1 = yes                                                   |                         |
|                          |                                         |                    |               |                                                           |                         |
|                          |                                         |                    |               | 0 = no                                                    |                         |
|                          +-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+                         |
|                          | A pre-established key is used.          | 1 (b[3])           | 0x0-0x1       | 1 = yes                                                   |                         |
|                          |                                         |                    |               |                                                           |                         |
|                          |                                         |                    |               | 0 = no                                                    |                         |
|                          +-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+                         |
|                          | reserved                                | 2 (b[2-1])         | 0x0           | Reserved by ISO 14229                                     |                         |
|                          +-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+                         |
|                          | Message is request message.             | 1 (b[0])           | 0x0           | 0 = no                                                    |                         |
+--------------------------+-----------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Signature/Encryption Calculation                                   | 8                  | 0x00-0xFF     | 0x00-0x7F: vehicle manufacturer specific                  | Always                  |
|                                                                    |                    |               |                                                           |                         |
|                                                                    |                    |               | 0x80-0x8F: system supplier specific                       |                         |
|                                                                    |                    |               |                                                           |                         |
|                                                                    |                    |               | 0x90-0xFF: reserved                                       |                         |
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Signature Length                                                   | 16                 | 0x0000-0xFFFF | Number of bytes to use for Signature/MAC Byte             | Always                  |
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Anti-replay Counter                                                | 16                 | 0x0000-0xFFFF | An incrementing counter to prevent a replay attack.       | Always                  |
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Internal Message Service Response ID                               | 8                  | 0x00-0xFF     | Response SID value (might be encrypted)                   | Always                  |
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Response Specific Parameters                                       | at least 8         |               | The following response message bytes (might be encrypted) | Optional                |
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+
| Signature/MAC                                                      | 8*Signature Length |               | Message signature                                         | If Signature Length > 0 |
+--------------------------------------------------------------------+--------------------+---------------+-----------------------------------------------------------+-------------------------+


ISO 14229-1:2013
''''''''''''''''
+----------------------------+------------+-------+---------------------------------------------------+---------+
| Name                       | Bit Length | Value | Description                                       | Present |
+============================+============+=======+===================================================+=========+
| RSID                       | 8          | 0xC4  | Positive Response: SecuredDataTransmission (0x84) | Always  |
+----------------------------+------------+-------+---------------------------------------------------+---------+
| securityDataResponseRecord | at least 8 |       | Encrypted response message                        | Always  |
+----------------------------+------------+-------+---------------------------------------------------+---------+


.. _knowledge-base-service-control-dtc-setting:

ControlDTCSetting (0x85)
------------------------
ControlDTCSetting service allows the client to stop or resume the updating of DTC status bits in the server(s) memory.


Request Format
``````````````
+----------------------------------------------+------------+-----------+-----------------------------------------------------------+----------+
| Name                                         | Bit Length | Value     | Description                                               | Present  |
+==============================================+============+===========+===========================================================+==========+
| SID                                          | 8          | 0x85      | ControlDTCSetting                                         | Always   |
+-------------+--------------------------------+------------+-----------+-----------------------------------------------------------+----------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                                     | Always   |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 1 = suppress positive response                            |          |
|             +--------------------------------+------------+-----------+-----------------------------------------------------------+          |
|             | DTCSettingType                 | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                                            |          |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 0x01: on                                                  |          |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 0x02: off                                                 |          |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 0x03-0x3F: reserved                                       |          |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 0x40-0x5F: vehicle manufacturer specific                  |          |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 0x60-0x7E: system supplier specific                       |          |
|             |                                |            |           |                                                           |          |
|             |                                |            |           | 0x7F: reserved                                            |          |
+-------------+--------------------------------+------------+-----------+-----------------------------------------------------------+----------+
| DTCSettingControlOptionRecord                | at least 8 |           | Additional information (e.g. list of DTCs to be affected) | Optional |
+----------------------------------------------+------------+-----------+-----------------------------------------------------------+----------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+-----------+---------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                 | Present |
+==============================================+============+===========+=============================================+=========+
| RSID                                         | 8          | 0xC5      | Positive Response: ControlDTCSetting (0x85) | Always  |
+-------------+--------------------------------+------------+-----------+---------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                       | Always  |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 1 = suppress positive response              |         |
|             +--------------------------------+------------+-----------+---------------------------------------------+         |
|             | DTCSettingType                 | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                              |         |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 0x01: on                                    |         |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 0x02: off                                   |         |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 0x03-0x3F: reserved                         |         |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 0x40-0x5F: vehicle manufacturer specific    |         |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 0x60-0x7E: system supplier specific         |         |
|             |                                |            |           |                                             |         |
|             |                                |            |           | 0x7F: reserved                              |         |
+-------------+--------------------------------+------------+-----------+---------------------------------------------+---------+


.. _knowledge-base-service-response-on-event:

ResponseOnEvent (0x86)
----------------------
ResponseOnEvent service allows the client to request from the server to start or stop transmission of responses on
a specified event.

.. warning:: In ISO 14229-1 *DTCSnapshotRecordNumber*, *DTCExtDataRecordNumber* and *MemorySelection* "follow"
  *ReadDTCInformation SubFunction* and are part of *eventTypeRecord* (if *event* equals 9).
  In the translator (due to code design limitations), *eventTypeRecord* contains only *DTCStatusMask* and
  *ReadDTCInformation SubFunction* Data Records.
  *DTCSnapshotRecordNumber*, *DTCExtDataRecordNumber* and *MemorySelection* are represented as separate Data Records
  that follows *eventTypeRecord* (for *event* equals 9).


Request Format
``````````````


ISO 14229-1:2020
''''''''''''''''
+-----------------------------------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| Name                                                      | Bit Length           | Value                 | Description                                           | Present                                                |
+===========================================================+======================+=======================+=======================================================+========================================================+
| SID                                                       | 8                    | 0x86                  | ResponseOnEvent                                       | Always                                                 |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| SubFunction              | suppressPosRspMsgIndicationBit | 1 (b[7])             | 0x0-0x1               | 0: response required                                  | Always                                                 |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 1: suppress positive response                         |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | eventType      | storageState  | 1 (b[6])             | 0x0-0x1               | 0x00: doNotStoreEvent                                 |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x01: storeEvent                                      |                                                        |
|                          |                +---------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          |                | event         | 6 (b[5-0])           | 0x00-0x3F             | 0x00: stopResponseOnEvent                             |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x01: onDTCStatusChange                               |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x02: reserved                                        |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x03: onChangeOfDataIdentifier                        |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x04: reportActivatedEvents                           |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x05: startResponseOnEvent                            |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x06: clearResponseOnEvent                            |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x07: onComparisonOfValues                            |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x08: reportMostRecentDtcOnStatusChange               |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x09: reportDTCRecordInformationOnDtcStatusChange     |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x0A-0x3F: reserved                                   |                                                        |
+--------------------------+----------------+---------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| eventWindowTime                                           | 8                    | 0x00-0xFF             | 0x00-0x01: reserved                                   | Always                                                 |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x02: infiniteTimeToResponse                          |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x03: shortEventWindowTime                            |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x04: mediumEventWindowTime                           |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x05: longEventWindowTime                             |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x06: powerWindowTime                                 |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x07: ignitionWindowTime                              |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x08: manufacturerTriggerEventWindowTime              |                                                        |
|                                                           |                      |                       |                                                       |                                                        |
|                                                           |                      |                       | 0x09-0xFF: reserved                                   |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DTCStatusMask                  | 8                    | 0x00-0xFF             | DTC Status bits to trigger event                      | If event equals 1                                      |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID change to trigger event                           | If event equals 3                                      |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID that contains Data Record to compare              | If event equals 7                                      |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | Comparison logic               | 8                    | 0x00-0xFF             | 0x00: reserved                                        |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x01: <                                               |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x02: >                                               |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x03: =                                               |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x04: <>                                              |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x05-0xFF: reserved                                   |                                                        |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | Compare Value                  | 32                   | 0x00000000-0xFFFFFFFF | Constant value to compare                             |                                                        |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | Hysteresis Value               | 8                    | 0x00-0xFF             | 0x00: 0%                                              |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | ...                                                   |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0xFF: 100%                                            |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | Localization   | Compare Sign  | 1 (b[7])             | 0x0-0x1               | 0: Comparison without sign                            |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 1: Comparison with sign                               |                                                        |
|                          |                +---------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          |                | Bits Number   | 5 (b[6-2])           | 0x00-0x1F             | 0x00: 32                                              |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x01: 1                                               |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x02: 2                                               |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | ...                                                   |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x1F: 31                                              |                                                        |
|                          |                +---------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          |                | Bit Offset    | 10 (b[1-0] + b[7-0]) | 0x000-0x3FF           | Value position offset in DID                          |                                                        |
+--------------------------+----------------+---------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | reserved                       | 1                    | 0x0-0x1               | Unused                                                | If event equals 8                                      |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | reportType                     | 7                    | 0x0D-0x0E             | 0x0D: reportMostRecentTestFailedDTC                   |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x0E: reportMostRecentConfirmedDTC                    |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DTCStatusMask                  | 8                    | 0x00-0xFF             | DTC Status bits to trigger event                      | If event equals 9                                      |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | reserved                       | 1                    | 0x0-0x1               | Unused                                                |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+-------------------------------------------------------+                                                        |
|                          | reportType     |               | 8                    | 0x04-0x19             | 0x04: reportDTCSnapshotRecordByDTCNumber              |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x06: reportDTCExtDataRecordByDTCNumber               |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x18: reportUserDefMemoryDTCSnapshotRecordByDTCNumber |                                                        |
|                          |                |               |                      |                       |                                                       |                                                        |
|                          |                |               |                      |                       | 0x19: reportUserDefMemoryDTCExtDataRecordByDTCNumber  |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
|                          | DTCSnapshotRecordNumber        | 8                    | 0x00-0xFF             | 0x00: reserved (legislated purposes)                  | If event equals 9                                      |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x01-0xFE: specific snapshot record                   | and ReadDTCInformation SubFunction equals 0x04 or 0x18 |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0xFF: all snapshot records                            |                                                        |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
|                          | DTCExtDataRecordNumber         | 8                    | 0x00-0xFF             | 0x00: reserved                                        | If event equals 9                                      |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x01-0x8F: vehicle manufacturer specific record       | and ReadDTCInformation SubFunction equals 0x06 or 0x19 |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0x90-0x9F: regulated emissions OBD record             |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0xA0-0xEF: regulated record                           |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0xF0-0xFD: reserved                                   |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0xFE: all regulated emissions OBD records             |                                                        |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       | 0xFF: all extended data records                       |                                                        |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
|                          | MemorySelection                | 8                    | 0x00-0xFF             | Specifies DTC memory                                  | If event equals 9                                      |
|                          |                                |                      |                       |                                                       |                                                        |
|                          |                                |                      |                       |                                                       | and ReadDTCInformation SubFunction equals 0x18 or 0x19 |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
| serviceToRespondToRecord | SID                            | 8                    | 0x00-0xFF             | SID value of Service to respond on Event              | If event equals 1, 3, 7, 8 or 9                        |
|                          +--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+
|                          | Service Specific Parameters    | at least 8           |                       | The following request message bytes                   | Optional if event equals 1, 3, 7, 8 or 9               |
+--------------------------+--------------------------------+----------------------+-----------------------+-------------------------------------------------------+--------------------------------------------------------+


ISO 14229-1:2013
''''''''''''''''
+-----------------------------------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| Name                                                      | Bit Length           | Value                 | Description                              | Present                               |
+===========================================================+======================+=======================+==========================================+=======================================+
| SID                                                       | 8                    | 0x86                  | ResponseOnEvent                          | Always                                |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| SubFunction              | suppressPosRspMsgIndicationBit | 1 (b[7])             | 0x0-0x1               | 0: response required                     | Always                                |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 1: suppress positive response            |                                       |
|                          +----------------+---------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          | eventType      | storageState  | 1 (b[6])             | 0x0-0x1               | 0x00: doNotStoreEvent                    |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x01: storeEvent                         |                                       |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          |                | event         | 6 (b[5-0])           | 0x00-0x3F             | 0x00: stopResponseOnEvent                |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x01: onDTCStatusChange                  |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x02: onTimerInterrupt                   |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x03: onChangeOfDataIdentifier           |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x04: reportActivatedEvents              |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x05: startResponseOnEvent               |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x06: clearResponseOnEvent               |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x07: onComparisonOfValues               |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x08-0x1F: reserved                      |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x20-0x2F: vehicle manufacturer specific |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x30-0x3E: system supplier specific      |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x3F: reserved                           |                                       |
+--------------------------+----------------+---------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| eventWindowTime                                           | 8                    | 0x00-0xFF             | 0x00-0x01: reserved                      | Always                                |
|                                                           |                      |                       |                                          |                                       |
|                                                           |                      |                       | 0x02: infiniteTimeToResponse             |                                       |
|                                                           |                      |                       |                                          |                                       |
|                                                           |                      |                       | 0x03-0x7F: vehicle manufacturer specific |                                       |
|                                                           |                      |                       |                                          |                                       |
|                                                           |                      |                       | 0x80-0xFF: reserved                      |                                       |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| eventTypeRecord          | DTCStatusMask                  | 8                    | 0x00-0xFF             | DTC Status bits to trigger event         | If event equals 1                     |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| eventTypeRecord          | Timer schedule                 | 8                    | 0x00-0xFF             | 0x01: Slow rate                          | If event equals 2                     |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x02: Medium rate                        |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x03: Fast rate                          |                                       |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID change to trigger event              | If event equals 3                     |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID that contains Data Record to compare | If event equals 7                     |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          | Comparison logic               | 8                    | 0x00-0xFF             | 0x00: reserved                           |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x01: <                                  |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x02: >                                  |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x03: =                                  |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x04: <>                                 |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0x05-0xFF: reserved                      |                                       |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          | Compare Value                  | 32                   | 0x00000000-0xFFFFFFFF | Constant value to compare                |                                       |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          | Hysteresis Value               | 8                    | 0x00-0xFF             | 0x00: 0%                                 |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | ...                                      |                                       |
|                          |                                |                      |                       |                                          |                                       |
|                          |                                |                      |                       | 0xFF: 100%                               |                                       |
|                          +----------------+---------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          | Localization   | Compare Sign  | 1 (b[7])             | 0x0-0x1               | 0: Comparison without sign               |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 1: Comparison with sign                  |                                       |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          |                | Bits Number   | 5 (b[6-2])           | 0x00-0x1F             | 0x00: 32                                 |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x01: 1                                  |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x02: 2                                  |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | ...                                      |                                       |
|                          |                |               |                      |                       |                                          |                                       |
|                          |                |               |                      |                       | 0x1F: 31                                 |                                       |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------+                                       |
|                          |                | Bit Offset    | 10 (b[1-0] + b[7-0]) | 0x000-0x3FF           | Value position offset in DID             |                                       |
+--------------------------+----------------+---------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
| serviceToRespondToRecord | SID                            | 8                    | 0x00-0xFF             | SID value of Service to respond on Event | If event equals 1, 2, 3 or 7          |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+
|                          | Service Specific Parameters    | at least 8           |                       | The following request message bytes      | Optional if event equals 1, 2, 3 or 7 |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------+---------------------------------------+


Positive Response Format
````````````````````````


reportActivatedEvents (0x04)
''''''''''''''''''''''''''''
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| Name                                         | Bit Length | Value     | Description                                                         | Present                                           |
+==============================================+============+===========+=====================================================================+===================================================+
| RSID                                         | 8          | 0xC6      | ResponseOnEvent                                                     | Always                                            |
+-------------+--------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0: response required                                                | Always                                            |
|             |                                |            |           |                                                                     |                                                   |
|             |                                |            |           | 1: suppress positive response                                       |                                                   |
|             +--------------+-----------------+------------+-----------+---------------------------------------------------------------------+                                                   |
|             | eventType    | storageState    | 1 (b[6])   | 0x0-0x1   | 0x00: doNotStoreEvent                                               |                                                   |
|             |              |                 |            |           |                                                                     |                                                   |
|             |              |                 |            |           | 0x01: storeEvent                                                    |                                                   |
|             |              +-----------------+------------+-----------+---------------------------------------------------------------------+                                                   |
|             |              | event           | 6 (b[5-0]) | 0x04      | reportActivatedEvents                                               |                                                   |
+-------------+--------------+-----------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| numberOfActivatedEvents                      | 8          | 0x00-0xFF | Number of active events (n)                                         | Always                                            |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| eventTypeOfActiveEvent#1                     | 8          | 0x00-0xFF | The value of eventType sent in the request (event#1)                | If there is at least 1 active event               |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+                                                   |
| eventWindowTime#1                            | 8          | 0x00-0xFF | The value of eventWindowTime sent in the request (event#1)          |                                                   |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| eventTypeRecord#1                            | 8-80       |           | The value of eventTypeRecord sent in the request (event#1)          | If there is at least 1 active event               |
|                                              |            |           |                                                                     |                                                   |
|                                              |            |           |                                                                     | AND the event#1 requires eventTypeRecord          |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| serviceToRespondToRecord#1                   | at least 8 |           | The value of serviceToRespondToRecord sent in the request (event#1) | If there is at least 1 active event               |
|                                              |            |           |                                                                     |                                                   |
|                                              |            |           |                                                                     | AND the event#1 requires serviceToRespondToRecord |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| ...                                                                                                                                                                                             |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| eventTypeOfActiveEvent#n                     | 8          | 0x00-0xFF | The value of eventType sent in the request (event#n)                | If there is at least n active events              |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+                                                   |
| eventWindowTime#n                            | 8          | 0x00-0xFF | The value of eventWindowTime sent in the request (event#n)          |                                                   |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| eventTypeRecord#n                            | 8-80       |           | The value of eventTypeRecord sent in the request (event#n)          | If there is at least n active events              |
|                                              |            |           |                                                                     |                                                   |
|                                              |            |           |                                                                     | AND the event#n requires eventTypeRecord          |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+
| serviceToRespondToRecord#n                   | at least 8 |           | The value of serviceToRespondToRecord sent in the request (event#n) | If there is at least n active events              |
|                                              |            |           |                                                                     |                                                   |
|                                              |            |           |                                                                     | AND the event#n requires serviceToRespondToRecord |
+----------------------------------------------+------------+-----------+---------------------------------------------------------------------+---------------------------------------------------+


other
'''''
Positive response if eventType[event] unequals reportActivatedEvents (0x04).


ISO 14229-1:2020
................
+-----------------------------------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| Name                                                      | Bit Length           | Value                 | Description                                                | Present                                                |
+===========================================================+======================+=======================+============================================================+========================================================+
| RSID                                                      | 8                    | 0xC6                  | ResponseOnEvent                                            | Always                                                 |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| SubFunction              | suppressPosRspMsgIndicationBit | 1 (b[7])             | 0x0-0x1               | 0: response required                                       | Always                                                 |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 1: suppress positive response                              |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | eventType      | storageState  | 1 (b[6])             | 0x0-0x1               | 0x00: doNotStoreEvent                                      |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x01: storeEvent                                           |                                                        |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          |                | event         | 6 (b[5-0])           | 0x00-0x3F             | 0x00: stopResponseOnEvent                                  |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x01: onDTCStatusChange                                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x02: reserved                                             |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x03: onChangeOfDataIdentifier                             |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x05: startResponseOnEvent                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x06: clearResponseOnEvent                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x07: onComparisonOfValues                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x08: reportMostRecentDtcOnStatusChange                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x09: reportDTCRecordInformationOnDtcStatusChange          |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x0A-0x3F: reserved                                        |                                                        |
+--------------------------+----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| numberOfIdentifiedEvents                                  | 8                    | 0x00-0xFF             | Number of identified events during an active event window. | Always                                                 |
+-----------------------------------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventWindowTime                                           | 8                    | 0x00-0xFF             | 0x00-0x01: reserved                                        | Always                                                 |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x02: infiniteTimeToResponse                               |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x03: shortEventWindowTime                                 |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x04: mediumEventWindowTime                                |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x05: longEventWindowTime                                  |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x06: powerWindowTime                                      |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x07: ignitionWindowTime                                   |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x08: manufacturerTriggerEventWindowTime                   |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x09-0xFF: reserved                                        |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DTCStatusMask                  | 8                    | 0x00-0xFF             | DTC Status bits to trigger event                           | If event equals 1                                      |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID change to trigger event                                | If event equals 3                                      |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID that contains Data Record to compare                   | If event equals 7                                      |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Comparison logic               | 8                    | 0x00-0xFF             | 0x00: reserved                                             |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x01: <                                                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x02: >                                                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x03: =                                                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x04: <>                                                   |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x05-0xFF: reserved                                        |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Compare Value                  | 32                   | 0x00000000-0xFFFFFFFF | Constant value to compare                                  |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Hysteresis Value               | 8                    | 0x00-0xFF             | 0x00: 0%                                                   |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | ...                                                        |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xFF: 100%                                                 |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Localization   | Compare Sign  | 1 (b[7])             | 0x0-0x1               | 0: Comparison without sign                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 1: Comparison with sign                                    |                                                        |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          |                | Bits Number   | 5 (b[6-2])           | 0x00-0x1F             | 0x00: 32                                                   |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x01: 1                                                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x02: 2                                                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | ...                                                        |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x1F: 31                                                   |                                                        |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          |                | Bit Offset    | 10 (b[1-0] + b[7-0]) | 0x000-0x3FF           | Value position offset in DID                               |                                                        |
+--------------------------+----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | reserved                       | 1                    | 0x0-0x1               | Unused                                                     | If event equals 8                                      |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | reportType                     | 7                    | 0x0D-0x0E             | 0x0D: reportMostRecentTestFailedDTC                        |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x0E: reportMostRecentConfirmedDTC                         |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DTCStatusMask                  | 8                    | 0x00-0xFF             | DTC Status bits to trigger event                           | If event equals 9                                      |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | reserved                       | 1                    | 0x0-0x1               | Unused                                                     |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | reportType                     | 7                    | 0x04-0x19             | 0x04: reportDTCSnapshotRecordByDTCNumber                   |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x06: reportDTCExtDataRecordByDTCNumber                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x18: reportUserDefMemoryDTCSnapshotRecordByDTCNumber      |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x19: reportUserDefMemoryDTCExtDataRecordByDTCNumber       |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
|                          | DTCSnapshotRecordNumber        | 8                    | 0x00-0xFF             | 0x00: reserved (legislated purposes)                       | If event equals 9                                      |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x01-0xFE: specific snapshot record                        | and ReadDTCInformation SubFunction equals 0x04 or 0x18 |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xFF: all snapshot records                                 |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
|                          | DTCExtDataRecordNumber         | 8                    | 0x00-0xFF             | 0x00: reserved                                             | If event equals 9                                      |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x01-0x8F: vehicle manufacturer specific record            | and ReadDTCInformation SubFunction equals 0x06 or 0x19 |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x90-0x9F: regulated emissions OBD record                  |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xA0-0xEF: regulated record                                |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xF0-0xFD: reserved                                        |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xFE: all regulated emissions OBD records                  |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xFF: all extended data records                            |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
|                          | MemorySelection                | 8                    | 0x00-0xFF             | Specifies DTC memory                                       | If event equals 9                                      |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       |                                                            | and ReadDTCInformation SubFunction equals 0x18 or 0x19 |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| serviceToRespondToRecord | SID                            | 8                    | 0x00-0xFF             | SID value of Service to respond on Event                   | If serviceToRespondToRecord was present in the request |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Service Specific Parameters    | at least 8           |                       | The following request message bytes                        |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+


ISO 14229-1:2013
................
+-----------------------------------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| Name                                                      | Bit Length           | Value                 | Description                                                | Present                                                |
+===========================================================+======================+=======================+============================================================+========================================================+
| RSID                                                      | 8                    | 0xC6                  | ResponseOnEvent                                            | Always                                                 |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| SubFunction              | suppressPosRspMsgIndicationBit | 1 (b[7])             | 0x0-0x1               | 0: response required                                       | Always                                                 |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 1: suppress positive response                              |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | eventType      | storageState  | 1 (b[6])             | 0x0-0x1               | 0x00: doNotStoreEvent                                      |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x01: storeEvent                                           |                                                        |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          |                | event         | 6 (b[5-0])           | 0x00-0x3F             | 0x00: stopResponseOnEvent                                  |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x01: onDTCStatusChange                                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x02: onTimerInterrupt                                     |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x03: onChangeOfDataIdentifier                             |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x05: startResponseOnEvent                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x06: clearResponseOnEvent                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x07: onComparisonOfValues                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x08-0x1F: reserved                                        |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x20-0x2F: vehicle manufacturer specific                   |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x30-0x3E: system supplier specific                        |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x3F: reserved                                             |                                                        |
+--------------------------+----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| numberOfIdentifiedEvents                                  | 8                    | 0x00-0xFF             | Number of identified events during an active event window. | Always                                                 |
+-----------------------------------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventWindowTime                                           | 8                    | 0x00-0xFF             | 0x00-0x01: reserved                                        | Always                                                 |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x02: infiniteTimeToResponse                               |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x03-0x7F: vehicle manufacturer specific                   |                                                        |
|                                                           |                      |                       |                                                            |                                                        |
|                                                           |                      |                       | 0x80-0xFF: reserved                                        |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DTCStatusMask                  | 8                    | 0x00-0xFF             | DTC Status bits to trigger event                           | If event equals 1                                      |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | Timer schedule                 | 8                    | 0x00-0xFF             | 0x01: Slow rate                                            | If event equals 2                                      |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x02: Medium rate                                          |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x03: Fast rate                                            |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID change to trigger event                                | If event equals 3                                      |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| eventTypeRecord          | DID                            | 16                   | 0x0000-0xFFFF         | DID that contains Data Record to compare                   | If event equals 7                                      |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Comparison logic               | 8                    | 0x00-0xFF             | 0x00: reserved                                             |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x01: <                                                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x02: >                                                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x03: =                                                    |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x04: <>                                                   |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0x05-0xFF: reserved                                        |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Compare Value                  | 32                   | 0x00000000-0xFFFFFFFF | Constant value to compare                                  |                                                        |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Hysteresis Value               | 8                    | 0x00-0xFF             | 0x00: 0%                                                   |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | ...                                                        |                                                        |
|                          |                                |                      |                       |                                                            |                                                        |
|                          |                                |                      |                       | 0xFF: 100%                                                 |                                                        |
|                          +----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Localization   | Compare Sign  | 1 (b[7])             | 0x0-0x1               | 0: Comparison without sign                                 |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 1: Comparison with sign                                    |                                                        |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          |                | Bits Number   | 5 (b[6-2])           | 0x00-0x1F             | 0x00: 32                                                   |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x01: 1                                                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x02: 2                                                    |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | ...                                                        |                                                        |
|                          |                |               |                      |                       |                                                            |                                                        |
|                          |                |               |                      |                       | 0x1F: 31                                                   |                                                        |
|                          |                +---------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          |                | Bit Offset    | 10 (b[1-0] + b[7-0]) | 0x000-0x3FF           | Value position offset in DID                               |                                                        |
+--------------------------+----------------+---------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+
| serviceToRespondToRecord | SID                            | 8                    | 0x00-0xFF             | SID value of Service to respond on Event                   | If serviceToRespondToRecord was present in the request |
|                          +--------------------------------+----------------------+-----------------------+------------------------------------------------------------+                                                        |
|                          | Service Specific Parameters    | at least 8           |                       | The following request message bytes                        |                                                        |
+--------------------------+--------------------------------+----------------------+-----------------------+------------------------------------------------------------+--------------------------------------------------------+


.. _knowledge-base-service-link-control:

LinkControl (0x87)
------------------
LinkControl service allows the client to control the communication between the client and the server(s) to
gain bus bandwidth for diagnostic purposes (e.g. programming).


Request Format
``````````````
+--------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------------------------+
| Name                                             | Bit Length | Value             | Description                                     | Present                                                                      |
+==================================================+============+===================+=================================================+==============================================================================+
| *SID*                                            | 8          | 0x87              | LinkControl                                     | Always                                                                       |
+---------------+----------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------------------------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 1 (b[7])   | 0x0-0x1           | 0: response required                            | Always                                                                       |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 1: suppress positive response                   |                                                                              |
|               +----------------------------------+------------+-------------------+-------------------------------------------------+                                                                              |
|               | *linkControlType*                | 7 (b[6-0]) | 0x00-0x7F         | 0x00: reserved                                  |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x01: verifyModeTransitionWithFixedParameter    |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x02: verifyModeTransitionWithSpecificParameter |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x03: transitionMode                            |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x04-0x3F: reserved                             |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x40-0x5F: vehicle manufacturer specific        |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x60-0x7E: system supplier specific             |                                                                              |
|               |                                  |            |                   |                                                 |                                                                              |
|               |                                  |            |                   | 0x7F: reserved                                  |                                                                              |
+---------------+----------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------------------------+
| *linkControlModeIdentifier*                      | 8          | 0x00-0xFF         | 0x00: reserved                                  | If *linkControlType* equals 0x01 (verifyModeTransitionWithFixedParameter)    |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x01: PC9600Baud                                |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x02: PC19200Baud                               |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x03: PC38400Baud                               |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x04: PC57600Baud                               |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x05: PC115200Baud                              |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x06-0x0F: reserved                             |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x10: CAN125000Baud                             |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x11: CAN250000Baud                             |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x12: CAN500000Baud                             |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x13: CAN1000000Baud                            |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x14-0x1F: reserved                             |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x20: ProgrammingSetup                          |                                                                              |
|                                                  |            |                   |                                                 |                                                                              |
|                                                  |            |                   | 0x21-0xFF: reserved                             |                                                                              |
+--------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------------------------+
| *linkRecord*                                     | 24         | 0x000000-0xFFFFFF | Value of a parameter specific for network used  | If *linkControlType* equals 0x02 (verifyModeTransitionWithSpecificParameter) |
+--------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------------------------+


Positive Response Format
````````````````````````
+--------------------------------------------------+------------+-----------+-----------------------------------------------------------------+---------+
| Name                                             | Bit Length | Value     | Description                                                     | Present |
+==================================================+============+===========+=================================================================+=========+
| *RSID*                                           | 8          | 0xC7      | LinkControl                                                     | Always  |
+---------------+----------------------------------+------------+-----------+-----------------------------------------------------------------+---------+
| *SubFunction* | *suppressPosRspMsgIndicationBit* | 1 (b[7])   | 0x0-0x1   | Echo of *suppressPosRspMsgIndicationBit* value from the request | Always  |
|               +----------------------------------+------------+-----------+-----------------------------------------------------------------+         |
|               | *linkControlType*                | 7 (b[6-0]) | 0x00-0x7F | Echo of *linkControlType* value from the request                |         |
+---------------+----------------------------------+------------+-----------+-----------------------------------------------------------------+---------+

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


Request Format
``````````````
+----------------------------------------------+------------+-----------+------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                              | Present |
+==============================================+============+===========+==========================================+=========+
| SID                                          | 8          | 0x10      | DiagnosticSessionControl                 | Always  |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                    | Always  |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 1 = suppress positive response           |         |
|             +--------------------------------+------------+-----------+------------------------------------------+         |
|             | diagnosticSessionType          | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                           |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x01: defaultSession                     |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x02: programmingSession                 |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x03: extendedDiagnosticSession          |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x04: safetySystemDiagnosticSession      |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x05–0x3F: reserved                      |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x40–0x5F: vehicle manufacturer specific |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x60–0x7E: system supplier specific      |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x7F: reserved                           |         |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+


Positive Response Format
````````````````````````
+---------------------------------------------------------+------------+---------------+----------------------------------------------------+---------+
| Name                                                    | Bit Length | Value         | Description                                        | Present |
+=========================================================+============+===============+====================================================+=========+
| RSID                                                    | 8          | 0x50          | Positive Response: DiagnosticSessionControl (0x10) | Always  |
+------------------------+--------------------------------+------------+---------------+----------------------------------------------------+---------+
| SubFunction            | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                              | Always  |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 1 = suppress positive response                     |         |
|                        +--------------------------------+------------+---------------+----------------------------------------------------+         |
|                        | diagnosticSessionType          | 7 (b[6-0]) | 0x00-0x7F     | 0x00: reserved                                     |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x01: defaultSession                               |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x02: programmingSession                           |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x03: extendedDiagnosticSession                    |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x04: safetySystemDiagnosticSession                |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x05–0x3F: reserved                                |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x40–0x5F: vehicle manufacturer specific           |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x60–0x7E: system supplier specific                |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x7F: reserved                                     |         |
+------------------------+--------------------------------+------------+---------------+----------------------------------------------------+---------+
| sessionParameterRecord | P2Server_max                   | 16         | 0x0000-0xFFFF | Maximum P2 timing used by server in this session   | Always  |
|                        +--------------------------------+------------+---------------+----------------------------------------------------+         |
|                        | P2\*Server_max                 | 16         | 0x0000-0xFFFF | Maximum P2* timing used by server in this session  |         |
+------------------------+--------------------------------+------------+---------------+----------------------------------------------------+---------+

.. note:: :ref:`P2Server_max <knowledge-base-p2-server>` field is provided directly in milliseconds.
  :ref:`P2*Server_max <knowledge-base-p2*-server>` field is encoded in units of 10 ms, so it must be multiplied by 10
  to obtain the value in milliseconds.


.. _knowledge-base-service-ecu-reset:

ECUReset
--------
ECUReset service is used by the client to request that the server perform a reset.
The server, after receiving this request, performs the specified type of reset (either before or after transmitting
the positive response).


Request Format
``````````````
+----------------------------------------------+------------+-----------+------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                              | Present |
+==============================================+============+===========+==========================================+=========+
| SID                                          | 8          | 0x11      | ECUReset                                 | Always  |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                    | Always  |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 1 = suppress positive response           |         |
|             +--------------------------------+------------+-----------+------------------------------------------+         |
|             | resetType                      | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                           |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x01: hardReset                          |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x02: keyOffOnReset                      |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x03: softReset                          |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x04: enableRapidPowerShutDown           |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x05: disableRapidPowerShutDown          |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x06-0x3F: reserved                      |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x40-0x5F: vehicle manufacturer specific |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x60-0x7E: system supplier specific      |         |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 0x7F: reserved                           |         |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+


Positive Response Format
````````````````````````
+----------------------------------------------+------------+-----------+------------------------------------------+---------------------+
| Name                                         | Bit Length | Value     | Description                              | Present             |
+==============================================+============+===========+==========================================+=====================+
| RSID                                         | 8          | 0x51      | Positive Response: ECUReset (0x11)       | Always              |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------------------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                    | Always              |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 1 = suppress positive response           |                     |
|             +--------------------------------+------------+-----------+------------------------------------------+                     |
|             | resetType                      | 7 (b[6-0]) | 0x00-0x7F | 0x00: reserved                           |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x01: hardReset                          |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x02: keyOffOnReset                      |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x03: softReset                          |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x04: enableRapidPowerShutDown           |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x05: disableRapidPowerShutDown          |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x06-0x3F: reserved                      |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x40-0x5F: vehicle manufacturer specific |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x60-0x7E: system supplier specific      |                     |
|             |                                |            |           |                                          |                     |
|             |                                |            |           | 0x7F: reserved                           |                     |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------------------+
| powerDownTime                                | 8          | 0x00-0xFF | 0x00-0xFE: down time in seconds          | If resetType = 0x04 |
|                                              |            |           |                                          |                     |
|                                              |            |           | 0xFF: failure or time unavailable        |                     |
+----------------------------------------------+------------+-----------+------------------------------------------+---------------------+

.. note:: The :code:`powerDownTime` field is only included in the positive response when
  :code:`resetType = 0x04` (*enableRapidPowerShutDown*).
  It defines the minimum time (in seconds) that the server requires to remain powered down before it can be safely
  restarted. A value of :code:`0xFF` indicates that either the time requirement is not available or a failure occurred.


.. _knowledge-base-service-clear-diagnostic-information:

ClearDiagnosticInformation
--------------------------
ClearDiagnosticInformation service is used by the client to clear Diagnostic Trouble Codes (DTCs) and related data
stored in one or more server memories.


Request Format
``````````````


ISO 14229-1:2020
''''''''''''''''
+-----------------+------------+-------------------+-------------------------------+----------+
| Name            | Bit Length | Value             | Description                   | Present  |
+=================+============+===================+===============================+==========+
| SID             | 8          | 0x14              | ClearDiagnosticInformation    | Always   |
+-----------------+------------+-------------------+-------------------------------+----------+
| groupOfDTC      | 24         | 0x000000-0xFFFFFF | Group of DTCs to be cleared   | Always   |
+-----------------+------------+-------------------+-------------------------------+----------+
| MemorySelection | 8          | 0x00-0xFF         | Specifies DTC memory to clear | Optional |
+-----------------+------------+-------------------+-------------------------------+----------+

.. note:: In ISO 14229-1:2020 the optional :code:`MemorySelection` field was introduced to allow clearing diagnostic
  information from a specific DTC memory (e.g. one of the sub-systems).


ISO 14229-1:2013
''''''''''''''''
+------------+------------+-------------------+-----------------------------+---------+
| Name       | Bit Length | Value             | Description                 | Present |
+============+============+===================+=============================+=========+
| SID        | 8          | 0x14              | ClearDiagnosticInformation  | Always  |
+------------+------------+-------------------+-----------------------------+---------+
| groupOfDTC | 24         | 0x000000-0xFFFFFF | Group of DTCs to be cleared | Always  |
+------------+------------+-------------------+-----------------------------+---------+


Positive Response Format
````````````````````````
+------+------------+-------+------------------------------------------------------+---------+
| Name | Bit Length | Value | Description                                          | Present |
+======+============+=======+======================================================+=========+
| RSID | 8          | 0x54  | Positive Response: ClearDiagnosticInformation (0x14) | Always  |
+------+------------+-------+------------------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information:

ReadDTCInformation
------------------
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
This sub-function can be used by the client to request the number of stored DTCs that match
a specific status mask (*DTCStatusMask*).
It is typically used as a lightweight way to determine how many DTCs fulfill a given diagnostic condition without
retrieving the DTC values themselves.


Request Format
''''''''''''''
The *DTCStatusMask* parameter specifies which status bits should be used as a filter when matching DTCs.
A value of 0x00 means that no status bits are selected. Since no DTC can match this, the result will always be
a count of 0.

+----------------------------------------------+------------+-----------+------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                              | Present |
+==============================================+============+===========+==========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                       | Always  |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                    | Always  |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 1 = suppress positive response           |         |
|             +--------------------------------+------------+-----------+------------------------------------------+         |
|             | reportType                     | 7 (b[6-0]) | 0x01      | reportNumberOfDTCByStatusMask            |         |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTCs matching | Always  |
+----------------------------------------------+------------+-----------+------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| Name                                         | Bit Length | Value         | Description                                  | Present |
+==============================================+============+===============+==============================================+=========+
| RSID                                         | 8          | 0x59          | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                        | Always  |
|             |                                |            |               |                                              |         |
|             |                                |            |               | 1 = suppress positive response               |         |
|             +--------------------------------+------------+---------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x01          | reportNumberOfDTCByStatusMask                | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8          | 0x00-0xFF     | DTC status bits supported by the server      | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8          | 0x00-0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCCount                                     | 16         | 0x0000-0xFFFF | Number of DTCs that match the criteria       | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-02:

reportDTCByStatusMask (0x02)
````````````````````````````
This sub-function can be used by the client to request a list of all DTCs stored in the server’s memory that match
a specific status mask (*DTCStatusMask*). A DTC is included in the response if :code:`DTC Status & DTCStatusMask) != 0`.
This sub-function provides the client with both the DTC values and their corresponding status information for
all DTCs that satisfy the given mask.


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                              | Present |
+==============================================+============+===========+==========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                       | Always  |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                    | Always  |
|             |                                |            |           |                                          |         |
|             |                                |            |           | 1 = suppress positive response           |         |
|             +--------------------------------+------------+-----------+------------------------------------------+         |
|             | reportType                     | 7 (b[6-0]) | 0x02      | reportDTCByStatusMask                    |         |
+-------------+--------------------------------+------------+-----------+------------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTCs matching | Always  |
+----------------------------------------------+------------+-----------+------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x02              | reportDTCByStatusMask                        | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-03:

reportDTCSnapshotIdentification (0x03)
``````````````````````````````````````
This sub-function can be used by the client to request identification numbers of all stored DTC snapshot records.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+---------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                     | Present |
+==============================================+============+=========+=================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation              | Always  |
+-------------+--------------------------------+------------+---------+---------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required           | Always  |
|             |                                |            |         |                                 |         |
|             |                                |            |         | 1 = suppress positive response  |         |
|             +--------------------------------+------------+---------+---------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x03    | reportDTCSnapshotIdentification | Always  |
+-------------+--------------------------------+------------+---------+---------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-----------------------------------------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| Name                                                            | Bit Length | Value             | Description                                      | Present                                          |
+=================================================================+============+===================+==================================================+==================================================+
| RSID                                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19)     | Always                                           |
+--------------------------------+--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| SubFunction                    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                            | Always                                           |
|                                |                                |            |                   |                                                  |                                                  |
|                                |                                |            |                   | 1 = suppress positive response                   |                                                  |
|                                +--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
|                                | reportType                     | 7 (b[6-0]) | 0x03              | reportDTCSnapshotIdentification                  | Always                                           |
+--------------------------------+--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| DTC and Snapshot Record Number | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                            | If at least one DTC Snapshot Record is available |
|                                +--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
|                                | DTCSnapshotRecordNumber        | 8          | 0x00-0xFF         | Number of DTC Snapshot Record reported for DTC#1 |                                                  |
|                                +--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
|                                | ...                                                                                                                                                                   |
|                                +--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
|                                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                            | If at least n DTC Snapshot Records are available |
|                                +--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
|                                | DTCSnapshotRecordNumber        | 8          | 0x00-0xFF         | Number of DTC Snapshot Record reported for DTC#n |                                                  |
+--------------------------------+--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-04:

reportDTCSnapshotRecordByDTCNumber (0x04)
`````````````````````````````````````````
This sub-function can be used by the client to request snapshot data for a specific DTC (*DTC*)
and snapshot record number (*DTCSnapshotRecordNumber*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-------------------+--------------------------------------+---------+
| Name                                         | Bit Length | Value             | Description                          | Present |
+==============================================+============+===================+======================================+=========+
| SID                                          | 8          | 0x19              | ReadDTCInformation                   | Always  |
+-------------+--------------------------------+------------+-------------------+--------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                | Always  |
|             |                                |            |                   |                                      |         |
|             |                                |            |                   | 1 = suppress positive response       |         |
|             +--------------------------------+------------+-------------------+--------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x04              | reportDTCSnapshotRecordByDTCNumber   | Always  |
+-------------+--------------------------------+------------+-------------------+--------------------------------------+---------+
| DTC                                          | 24         | 0x000000-0xFFFFFF | DTC number                           | Always  |
+----------------------------------------------+------------+-------------------+--------------------------------------+---------+
| DTCSnapshotRecordNumber                      | 8          | 0x00-0xFF         | 0x00: reserved (legislated purposes) | Always  |
|                                              |            |                   |                                      |         |
|                                              |            |                   | 0x01-0xFE: specific snapshot record  |         |
|                                              |            |                   |                                      |         |
|                                              |            |                   | 0xFF: all snapshot records           |         |
+----------------------------------------------+------------+-------------------+--------------------------------------+---------+

.. note:: *DTCSnapshotRecordNumber* (0x01–0xFE) selects a single snapshot record.
  If equal to 0xFF, all available snapshot records for the DTC are returned.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                                    |
+=================================================+============+===================+==============================================+============================================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                                     |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                                     |
|                |                                |            |                   |                                              |                                                            |
|                |                                |            |                   | 1 = suppress positive response               |                                                            |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x04              | reportDTCSnapshotRecordByDTCNumber           | Always                                                     |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | Considered DTC                               | Always                                                     |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
|                | DTCStatus                      | 8          | 0x00-0xFF         | DTC status                                   | Always                                                     |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| DTCSnapshotRecordNumber#1                       | 8          | 0x00-0xFF         | Number of DTCSnapshotRecord#1                | If at least one DTCSnapshotRecord is available for the DTC |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DIDCount#1                                      | 8          | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#1 |                                                            |
|                                                 |            |                   | (equals m)                                   |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#1_1                                         | 16         | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshotRecord#1    |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#1_1 data                                    | 8 or more  |                   | Data stored under DID#1_1                    |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| ...                                                                                                                             |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#1_m                                         | 16         | 0x0000-0xFFFF     | DID#m that is part of DTCSnapshotRecord#1    |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#1_m data                                    | 8 or more  |                   | Data stored under DID#1_m                    |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| ...                                                                                                                                                                                          |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| DTCSnapshotRecordNumber#n                       | 28         | 0x00-0xFF         | Number of DTCSnapshot#n                      | If requested for multiple DTCSnapshot records              |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DIDCount#n                                      | 8          | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#n | AND                                                        |
|                                                 |            |                   | (equals k)                                   |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+ at least n DTCSnapshotRecords are available for the DTC    |
| DID#n_1                                         | 16         | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshot#n          |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#n_1 data                                    | 8 or more  |                   | Data stored under DID#n_1                    |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| ...                                                                                                                             |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#n_k                                         | 16         | 0x0000-0xFFFF     | DID#k that is part of DTCSnapshot#n          |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                            |
| DID#n_k data                                    | 8 or more  |                   | Data stored under DID#n_k                    |                                                            |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-05:

reportDTCStoredDataByRecordNumber (0x05)
````````````````````````````````````````
This sub-function can be used by the client to request stored data for a specific record (*DTCStoredDataRecordNumber*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                            | Present |
+==============================================+============+===========+========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                     | Always  |
+-------------+--------------------------------+------------+-----------+----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                  | Always  |
|             |                                |            |           |                                        |         |
|             |                                |            |           | 1 = suppress positive response         |         |
|             +--------------------------------+------------+-----------+----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x05      | reportDTCStoredDataByRecordNumber      | Always  |
+-------------+--------------------------------+------------+-----------+----------------------------------------+---------+
| DTCStoredDataRecordNumber                    | 8          | 0x00-0xFF | 0x00: reserved (legislated purposes)   | Always  |
|                                              |            |           |                                        |         |
|                                              |            |           | 0x01–0xFE: specific stored data record |         |
|                                              |            |           |                                        |         |
|                                              |            |           | 0xFF: all records                      |         |
+----------------------------------------------+------------+-----------+----------------------------------------+---------+

.. note:: *DTCStoredDataRecordNumber* (0x01–0xFE) selects a single stored data record.
  If equal to 0xFF, all available stored data records for the DTC are returned.


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| Name                                              | Bit Length | Value             | Description                                      | Present                                          |
+===================================================+============+===================+==================================================+==================================================+
| RSID                                              | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19)     | Always                                           |
+------------------+--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| SubFunction      | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                            | Always                                           |
|                  |                                |            |                   |                                                  |                                                  |
|                  |                                |            |                   | 1 = suppress positive response                   |                                                  |
|                  +--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
|                  | reportType                     | 7 (b[6-0]) | 0x05              | reportDTCStoredDataByRecordNumber                | Always                                           |
+------------------+--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| DTCStoredDataRecordNumber#1                       | 8          | 0x00-0xFF         | Number of DTCStoredDataRecord#1                  | Always                                           |
+------------------+--------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| DTC and Status#1 | DTC                            | 24         | 0x000000-0xFFFFFF | DTC for which DTCStoredDataRecord#1 was reported | If at least one DTCStoredDataRecord is available |
|                  +--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
|                  | DTCStatus                      | 8          | 0x00-0xFF         | DTC#1 status                                     |                                                  |
+------------------+--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DIDCount#1                                        | 8          | 0x00-0xFF         | Number of DIDs stored in DTCStoredDataRecord#1   |                                                  |
|                                                   |            |                   | (equals m)                                       |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#1_1                                           | 16         | 0x0000-0xFFFF     | DID#1 that is part of DTCStoredDataRecord#1      |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#1_1 data                                      | 8 or more  |                   | Data stored under DID#1_1                        |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| ...                                                                                                                                   |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#1_m                                           | 16         | 0x0000-0xFFFF     | DID#m that is part of DTCStoredData#1            |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#1_m data                                      | 8 or more  |                   | Data stored under DID#m                          |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| ...                                                                                                                                                                                      |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+
| DTCStoredDataRecordNumber#n                       | 8          | 0x00-0xFF         | Number of DTCStoredDataRecord#n                  | If requested for multiple DTCStoredDataRecords   |
+------------------+--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DTC and Status#n | DTC                            | 24         | 0x000000-0xFFFFFF | DTC for which DTCStoredDataRecord#n was reported | AND                                              |
|                  +--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
|                  | DTCStatus                      | 8          | 0x00-0xFF         | DTC#n status                                     | at least n DTCStoredDataRecords are available    |
+------------------+--------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DIDCount#n                                        | 8          | 0x00-0xFF         | Number of DIDs stored in DTCStoredDataRecord#n   |                                                  |
|                                                   |            |                   | (equals k)                                       |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#n_1                                           | 16         | 0x0000-0xFFFF     | DID#1 that is part of DTCStoredDataRecord#n      |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#n_1 data                                      | 8 or more  |                   | Data stored under DID#n_1                        |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| ...                                                                                                                                   |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#n_k                                           | 16         | 0x0000-0xFFFF     | DID#n that is part of DTCStoredDataRecord#n      |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+                                                  |
| DID#n_k data                                      | 8 or more  |                   | Data stored under DID#n_k                        |                                                  |
+---------------------------------------------------+------------+-------------------+--------------------------------------------------+--------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-06:

reportDTCExtDataRecordByDTCNumber (0x06)
````````````````````````````````````````
This sub-function can be used by the client to request extended data records for a specific DTC (*DTC*)
and record number (*DTCExtDataRecordNumber*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| Name                                         | Bit Length | Value             | Description                                     | Present |
+==============================================+============+===================+=================================================+=========+
| SID                                          | 8          | 0x19              | ReadDTCInformation                              | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                           | Always  |
|             |                                |            |                   |                                                 |         |
|             |                                |            |                   | 1 = suppress positive response                  |         |
|             +--------------------------------+------------+-------------------+-------------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x06              | reportDTCExtDataRecordByDTCNumber               | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTC                                          | 24         | 0x000000-0xFFFFFF | DTC number                                      | Always  |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8          | 0x00-0xFF         | 0x00: reserved                                  | Always  |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x01-0x8F: vehicle manufacturer specific record |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x90-0x9F: regulated emissions OBD record       |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xA0-0xEF: regulated record                     |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xF0-0xFD: reserved                             |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFE: all regulated emissions OBD records       |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFF: all extended data records                 |         |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                                   |
+=================================================+============+===================+==============================================+===========================================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                                    |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                                    |
|                |                                |            |                   |                                              |                                                           |
|                |                                |            |                   | 1 = suppress positive response               |                                                           |
|                +--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x06              | reportDTCExtDataRecordByDTCNumber            | Always                                                    |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | Considered DTC                               | Always                                                    |
|                +--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                | Always                                                    |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
| DTCExtDataRecordNumber#1                        | 8          | 0x00-0xFF         | Number of DTCExtDataRecord#1                 | If at least one DTCExtDataRecord is available for the DTC |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+                                                           |
| DTCExtDataRecord#1                              | at least 8 |                   | Extended Data #1                             |                                                           |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
| ...                                                                                                                                                                                         |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+
| DTCExtDataRecordNumber#n                        | 8          | 0x00-0xFF         | Number of DTCExtDataRecord#n                 | If requested for multiple DTCExtDataRecords               |
|                                                 |            |                   |                                              |                                                           |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+ AND                                                       |
| DTCExtDataRecord#n                              | at least 8 |                   | Extended Data #n                             |                                                           |
|                                                 |            |                   |                                              | at least n DTCExtDataRecords are available for the DTC    |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-07:

reportNumberOfDTCBySeverityMaskRecord (0x07)
````````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs that match a given
severity mask (*DTCSeverityMask*) and status mask (*DTCStatusMask*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x07      | reportNumberOfDTCBySeverityMaskRecord   | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCSeverityMask                              | 8          | 0x00-0xFF | Severity mask to use for DTC matching   | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| Name                                         | Bit Length | Value         | Description                                  | Present |
+==============================================+============+===============+==============================================+=========+
| RSID                                         | 8          | 0x59          | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                        | Always  |
|             |                                |            |               |                                              |         |
|             |                                |            |               | 1 = suppress positive response               |         |
|             +--------------------------------+------------+---------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x07          | reportNumberOfDTCBySeverityMaskRecord        | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8          | 0x00-0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8          | 0x00-0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCCount                                     | 16         | 0x0000-0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-08:

reportDTCBySeverityMaskRecord (0x08)
````````````````````````````````````
This sub-function can be used by the client to request all DTCs that match a given severity mask (*DTCSeverityMask*)
and status mask (*DTCStatusMask*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x08      | reportDTCBySeverityMaskRecord           | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCSeverityMask                              | 8          | 0x00-0xFF | Severity mask to use for DTC matching   | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                                                       | Bit Length | Value             | Description                                  | Present                                  |
+============================================================================+============+===================+==============================================+==========================================+
| RSID                                                                       | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction                               | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                                           |                                |            |                   |                                              |                                          |
|                                           |                                |            |                   | 1 = suppress positive response               |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                           | reportType                     | 7 (b[6-0]) | 0x08              | reportDTCBySeverityMaskRecord                | Always                                   |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                                                  | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Severity, Functional Unit, DTC and Status | DTCSeverity                    | 8          | 0x00-0xFF         | Severity of DTC#1                            | If at least one DTC matches the criteria |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTCFunctionalUnit              | 8          | 0x00-0xFF         | Functional Unit of DTC#1                     |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                           | ...                                                                                                                                                       |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                           | DTCSeverity                    | 8          | 0x00-0xFF         | Severity of DTC#n                            | If at least n DTCs matches the criteria  |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTCFunctionalUnit              | 8          | 0x00-0xFF         | Functional Unit of DTC#n                     |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-09:

reportSeverityInformationOfDTC (0x09)
`````````````````````````````````````
This sub-function can be used by the client to request severity and functional unit information for
a specific DTC (*DTC*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-------------------+--------------------------------+---------+
| Name                                         | Bit Length | Value             | Description                    | Present |
+==============================================+============+===================+================================+=========+
| SID                                          | 8          | 0x19              | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+-------------------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required          | Always  |
|             |                                |            |                   |                                |         |
|             |                                |            |                   | 1 = suppress positive response |         |
|             +--------------------------------+------------+-------------------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x09              | reportSeverityInformationOfDTC | Always  |
+-------------+--------------------------------+------------+-------------------+--------------------------------+---------+
| DTC                                          | 24         | 0x000000-0xFFFFFF | DTC number                     | Always  |
+----------------------------------------------+------------+-------------------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                                                       | Bit Length | Value             | Description                                  | Present                                  |
+============================================================================+============+===================+==============================================+==========================================+
| RSID                                                                       | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction                               | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                                           |                                |            |                   |                                              |                                          |
|                                           |                                |            |                   | 1 = suppress positive response               |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                           | reportType                     | 7 (b[6-0]) | 0x09              | reportSeverityInformationOfDTC               | Always                                   |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                                                  | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Severity, Functional Unit, DTC and Status | DTCSeverity                    | 8          | 0x00-0xFF         | Severity of DTC                              | If at least one DTC matches the criteria |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTCFunctionalUnit              | 8          | 0x00-0xFF         | Functional Unit of DTC                       |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTC                            | 24         | 0x000000-0xFFFFFF | DTC number                                   |                                          |
|                                           +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                           | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                |                                          |
+-------------------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0A:

reportSupportedDTC (0x0A)
`````````````````````````
This sub-function can be used by the client to request a list of all DTCs supported by the server.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x0A    | reportSupportedDTC             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x0A              | reportSupportedDTCs                          | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0B:

reportFirstTestFailedDTC (0x0B)
```````````````````````````````
This sub-function can be used by the client to request the first DTC that failed a test since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x0B    | reportFirstTestFailedDTC       | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+

.. note:: The returned DTC is the first one detected with testFailed status bit (b0) set since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x0B              | reportFirstTestFailedDTC                     | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0C:

reportFirstConfirmedDTC (0x0C)
``````````````````````````````
This sub-function can be used by the client to request the first confirmed DTC since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x0C    | reportFirstConfirmedDTC        | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+

.. note:: The returned DTC is the first one detected with confirmedDTC status bit (b3) set since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x0C              | reportFirstConfirmedDTC                      | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0D:

reportMostRecentTestFailedDTC (0x0D)
````````````````````````````````````
This sub-function can be used by the client to request the most recent DTC that failed a test since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x0D    | reportMostRecentTestFailedDTC  | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+

.. note:: The returned DTC is the most recent one detected with testFailed status bit (b0) set since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x0D              | reportMostRecentTestFailedDTC                | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0E:

reportMostRecentConfirmedDTC (0x0E)
```````````````````````````````````
This sub-function can be used by the client to request the most recent confirmed DTC since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x0E    | reportMostRecentConfirmedDTC   | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+

.. note:: The returned DTC is the most recent one detected with confirmedDTC status bit (b3) set since the last
    :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x0E              | reportMostRecentConfirmedDTC                 | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0F:

reportMirrorMemoryDTCByStatusMask (0x0F)
````````````````````````````````````````
This sub-function can be used by the client to request all DTCs in the DTC mirror memory that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x0F      | reportMirrorMemoryDTCByStatusMask       | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x0F              | reportMirrorMemoryDTCByStatusMask            | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-10:

reportMirrorMemoryDTCExtDataRecordByDTCNumber (0x10)
````````````````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*) for
a specific DTC (*DTC*) from the DTC mirror memory.

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| Name                                         | Bit Length | Value             | Description                                     | Present |
+==============================================+============+===================+=================================================+=========+
| SID                                          | 8          | 0x19              | ReadDTCInformation                              | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                           | Always  |
|             |                                |            |                   |                                                 |         |
|             |                                |            |                   | 1 = suppress positive response                  |         |
|             +--------------------------------+------------+-------------------+-------------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x10              | reportMirrorMemoryDTCExtDataRecordByDTCNumber   | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTC                                          | 24         | 0x000000-0xFFFFFF | DTC number                                      | Always  |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8          | 0x00-0xFF         | 0x00: reserved                                  | Always  |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x01-0x8F: vehicle manufacturer specific record |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x90-0x9F: regulated emissions OBD record       |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xA0-0xEF: regulated record                     |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xF0-0xFD: reserved                             |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFE: all regulated emissions OBD records       |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFF: all extended data records                 |         |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                   | Present                                                   |
+=================================================+============+===================+===============================================+===========================================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19)  | Always                                                    |
+----------------+--------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                         | Always                                                    |
|                |                                |            |                   |                                               |                                                           |
|                |                                |            |                   | 1 = suppress positive response                |                                                           |
|                +--------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x10              | reportMirrorMemoryDTCExtDataRecordByDTCNumber | Always                                                    |
+----------------+--------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | Considered DTC                                | Always                                                    |
|                +--------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                 | Always                                                    |
+----------------+--------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
| DTCExtDataRecordNumber#1                        | 8          | 0x00-0xFF         | Number of DTCExtDataRecord#1                  | If at least one DTCExtDataRecord is available for the DTC |
+-------------------------------------------------+------------+-------------------+-----------------------------------------------+                                                           |
| DTCExtDataRecord#1                              | at least 8 |                   | Extended Data #1                              |                                                           |
+-------------------------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
| ...                                                                                                                                                                                          |
+-------------------------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+
| DTCExtDataRecordNumber#n                        | 8          | 0x00-0xFF         | Number of DTCExtDataRecord#n                  | If requested for multiple DTCExtDataRecords               |
|                                                 |            |                   |                                               |                                                           |
+-------------------------------------------------+------------+-------------------+-----------------------------------------------+ AND                                                       |
| DTCExtDataRecord#n                              | at least 8 |                   | Extended Data #n                              |                                                           |
|                                                 |            |                   |                                               | at least n DTCExtDataRecords are available for the DTC    |
+-------------------------------------------------+------------+-------------------+-----------------------------------------------+-----------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-11:

reportNumberOfMirrorMemoryDTCByStatusMask (0x11)
````````````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs in the DTC mirror memory that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                               | Present |
+==============================================+============+===========+===========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                        | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                     | Always  |
|             |                                |            |           |                                           |         |
|             |                                |            |           | 1 = suppress positive response            |         |
|             +--------------------------------+------------+-----------+-------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x11      | reportNumberOfMirrorMemoryDTCByStatusMask | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching   | Always  |
+----------------------------------------------+------------+-----------+-------------------------------------------+---------+

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| Name                                         | Bit Length | Value         | Description                                  | Present |
+==============================================+============+===============+==============================================+=========+
| RSID                                         | 8          | 0x59          | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                        | Always  |
|             |                                |            |               |                                              |         |
|             |                                |            |               | 1 = suppress positive response               |         |
|             +--------------------------------+------------+---------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x11          | reportNumberOfMirrorMemoryDTCByStatusMask    | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8          | 0x00-0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8          | 0x00-0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCCount                                     | 16         | 0x0000-0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-12:

reportNumberOfEmissionsOBDDTCByStatusMask (0x12)
````````````````````````````````````````````````
This sub-function can be used by the client to request the number of emissions-related OBD DTCs that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                               | Present |
+==============================================+============+===========+===========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                        | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                     | Always  |
|             |                                |            |           |                                           |         |
|             |                                |            |           | 1 = suppress positive response            |         |
|             +--------------------------------+------------+-----------+-------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x12      | reportNumberOfEmissionsOBDDTCByStatusMask | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching   | Always  |
+----------------------------------------------+------------+-----------+-------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| Name                                         | Bit Length | Value         | Description                                  | Present |
+==============================================+============+===============+==============================================+=========+
| RSID                                         | 8          | 0x59          | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1       | 0 = response required                        | Always  |
|             |                                |            |               |                                              |         |
|             |                                |            |               | 1 = suppress positive response               |         |
|             +--------------------------------+------------+---------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x12          | reportNumberOfEmissionsOBDDTCByStatusMask    | Always  |
+-------------+--------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8          | 0x00-0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8          | 0x00-0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |            |               |                                              |         |
|                                              |            |               | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+
| DTCCount                                     | 16         | 0x0000-0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+------------+---------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-13:

reportEmissionsOBDDTCByStatusMask (0x13)
````````````````````````````````````````
This sub-function can be used by the client to request a list of emissions-related OBD DTCs that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x13      | reportEmissionsOBDDTCByStatusMask       | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x13              | reportEmissionsOBDDTCByStatusMask            | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-14:

reportDTCFaultDetectionCounter (0x14)
`````````````````````````````````````
This sub-function can be used by the client to request fault detection counters for DTCs that have not been reported
or confirmed.


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x14    | reportDTCFaultDetectionCounter | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                                              | Bit Length | Value             | Description                                  | Present                                  |
+===================================================================+============+===================+==============================================+==========================================+
| RSID                                                              | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction                      | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                                  |                                |            |                   |                                              |                                          |
|                                  |                                |            |                   | 1 = suppress positive response               |                                          |
|                                  +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                  | reportType                     | 7 (b[6-0]) | 0x14              | reportDTCFaultDetectionCounter               | Always                                   |
+----------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                                         | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Fault Detection Counter  | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                                  +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                  | DTCFaultDetectionCounter       | 8          | 0x01-0xFF         | Value of fault detection counter for DTC#1   |                                          |
|                                  +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                  | ...                                                                                                                                                       |
|                                  +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                                  | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                                  +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                                  | DTCFaultDetectionCounter       | 8          | 0x01-0xFF         | Value of fault detection counter for DTC#n   |                                          |
+----------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-15:

reportDTCWithPermanentStatus (0x15)
```````````````````````````````````
This sub-function can be used by the client to request a list of DTCs with permanent status (once reported,
never cleared by healing).


Request Format
''''''''''''''
+----------------------------------------------+------------+---------+--------------------------------+---------+
| Name                                         | Bit Length | Value   | Description                    | Present |
+==============================================+============+=========+================================+=========+
| SID                                          | 8          | 0x19    | ReadDTCInformation             | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1 | 0 = response required          | Always  |
|             |                                |            |         |                                |         |
|             |                                |            |         | 1 = suppress positive response |         |
|             +--------------------------------+------------+---------+--------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x15    | reportDTCWithPermanentStatus   | Always  |
+-------------+--------------------------------+------------+---------+--------------------------------+---------+

Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x15              | reportDTCWithPermanentStatus                 | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the server      | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-16:

reportDTCExtDataRecordByRecordNumber (0x16)
```````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*)
regardless of the DTC number.


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                     | Present |
+==============================================+============+===========+=================================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                              | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                           | Always  |
|             |                                |            |           |                                                 |         |
|             |                                |            |           | 1 = suppress positive response                  |         |
|             +--------------------------------+------------+-----------+-------------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x16      | reportDTCExtDataRecordByRecordNumber            | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8          | 0x00-0xFF | 0x00: reserved                                  | Always  |
|                                              |            |           |                                                 |         |
|                                              |            |           | 0x01-0x8F: vehicle manufacturer specific record |         |
|                                              |            |           |                                                 |         |
|                                              |            |           | 0x90-0x9F: regulated emissions OBD record       |         |
|                                              |            |           |                                                 |         |
|                                              |            |           | 0xA0-0xEF: regulated record                     |         |
|                                              |            |           |                                                 |         |
|                                              |            |           | 0xF0-0xFD: reserved                             |         |
|                                              |            |           |                                                 |         |
|                                              |            |           | 0xFE: all regulated emissions OBD records       |         |
|                                              |            |           |                                                 |         |
|                                              |            |           | 0xFF: all extended data records                 |         |
+----------------------------------------------+------------+-----------+-------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
| Name                                              | Bit Length | Value             | Description                                  | Present                                       |
+===================================================+============+===================+==============================================+===============================================+
| RSID                                              | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                        |
+------------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
| SubFunction      | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                        |
|                  |                                |            |                   |                                              |                                               |
|                  |                                |            |                   | 1 = suppress positive response               |                                               |
|                  +--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
|                  | reportType                     | 7 (b[6-0]) | 0x16              | reportDTCExtDataRecordByRecordNumber         | Always                                        |
+------------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
| DTCExtDataRecordNumber                            | 8          | 0x00-0xEF         | Identification number of DTCExtDataRecord    | Always                                        |
+------------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
| DTC and Status#1 | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTCExtDataRecord is available |
|                  +--------------------------------+------------+-------------------+----------------------------------------------+                                               |
|                  | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                               |
+------------------+--------------------------------+------------+-------------------+----------------------------------------------+                                               |
| DTCExtDataRecord#1                                | at least 8 |                   | Extended Data #1                             |                                               |
+---------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
| ...                                                                                                                                                                               |
+------------------+--------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+
| DTC and Status#n | DTC                            | 24         | 0x00-0xFF         | DTC#n                                        | If at least n DTCExtDataRecords are available |
|                  +--------------------------------+------------+-------------------+----------------------------------------------+                                               |
|                  | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                               |
+------------------+--------------------------------+------------+-------------------+----------------------------------------------+                                               |
| DTCExtDataRecord#n                                | at least 8 |                   | Extended Data #n                             |                                               |
+---------------------------------------------------+------------+-------------------+----------------------------------------------+-----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-17:

reportUserDefMemoryDTCByStatusMask (0x17)
`````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs that match a given
status mask (*DTCStatusMask*) in a selected memory (*MemorySelection*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x17      | reportUserDefMemoryDTCByStatusMask      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| MemorySelection                              | 8          | 0x00-0xFF | Identifies DTC memory                   | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+

.. note:: :code:`MemorySelection` allows reading DTC related information from a specific DTC memory (e.g. one of
  the sub-systems).


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x17              | reportUserDefMemoryDTCByStatusMask           | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| MemorySelection                                 | 8          | 0x00-0xFF         | Selected memory                              | Always                                   |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-18:

reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
``````````````````````````````````````````````````````
This sub-function can be used by the client to request snapshot records (*DTCSnapshotRecordNumber*) for
a specific DTC (*DTC*) in a selected memory (*MemorySelection*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| Name                                         | Bit Length | Value             | Description                                     | Present |
+==============================================+============+===================+=================================================+=========+
| SID                                          | 8          | 0x19              | ReadDTCInformation                              | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                           | Always  |
|             |                                |            |                   |                                                 |         |
|             |                                |            |                   | 1 = suppress positive response                  |         |
|             +--------------------------------+------------+-------------------+-------------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x18              | reportUserDefMemoryDTCSnapshotRecordByDTCNumber | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTC                                          | 24         | 0x000000-0xFFFFFF | DTC number                                      | Always  |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTCSnapshotRecordNumber                      | 8          | 0x00-0xFF         | 0x00: reserved (legislated purposes)            | Always  |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x01-0xFE: specific snapshot record             |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFF: all snapshot records                      |         |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| MemorySelection                              | 8          | 0x00-0xFF         | Identifies DTC memory                           | Always  |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+

.. note:: :code:`MemorySelection` allows reading DTC related information from a specific DTC memory (e.g. one of
  the sub-systems).


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                     | Present                                                    |
+=================================================+============+===================+=================================================+============================================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19)    | Always                                                     |
+----------------+--------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                           | Always                                                     |
|                |                                |            |                   |                                                 |                                                            |
|                |                                |            |                   | 1 = suppress positive response                  |                                                            |
|                +--------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x18              | reportUserDefMemoryDTCSnapshotRecordByDTCNumber | Always                                                     |
+----------------+--------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| MemorySelection                                 | 8          | 0x00-0xFF         | Selected memory                                 | Always                                                     |
+----------------+--------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | Selected DTC                                    | Always                                                     |
|                +--------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                   | Always                                                     |
+----------------+--------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| DTCSnapshotRecordNumber#1                       | 8          | 0x00-0xFF         | Number of DTCSnapshot#1                         | If at least one DTCSnapshotRecord is available for the DTC |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DIDCount#1                                      | 8          | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#1    |                                                            |
|                                                 |            |                   | (equals m)                                      |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#1_1                                         | 16         | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshotRecord#1       |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#1_1 data                                    | 8 or more  |                   | Data stored under DID#1_1                       |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| ...                                                                                                                                |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#1_m                                         | 16         | 0x0000-0xFFFF     | DID#m that is part of DTCSnapshotRecord#1       |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#1_m data                                    | 8 or more  |                   | Data stored under DID#1_m                       |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| ...                                                                                                                                                                                             |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+
| DTCSnapshotRecordNumber#n                       | 8          | 0x00-0xFF         | Number of DTCSnapshot#n                         | If requested for multiple DTCSnapshot records              |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DIDCount#n                                      | 8          | 0x00-0xFF         | Number of DIDs stored in DTCSnapshotRecord#n    | AND                                                        |
|                                                 |            |                   | (equals k)                                      |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+ at least n DTCSnapshotRecords are available for the DTC    |
| DID#n_1                                         | 16         | 0x0000-0xFFFF     | DID#1 that is part of DTCSnapshot#n             |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#n_1 data                                    | 8 or more  |                   | Data stored under DID#n_1                       |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| ...                                                                                                                                |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#n_k                                         | 16         | 0x0000-0xFFFF     | DID#k that is part of DTCSnapshot#n             |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+                                                            |
| DID#n_k data                                    | 8 or more  |                   | Data stored under DID#n_k                       |                                                            |
+-------------------------------------------------+------------+-------------------+-------------------------------------------------+------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-19:

reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
`````````````````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*) for
a specific DTC (*DTCMaskRecord*) in a selected memory (*MemorySelection*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| Name                                         | Bit Length | Value             | Description                                     | Present |
+==============================================+============+===================+=================================================+=========+
| SID                                          | 8          | 0x19              | ReadDTCInformation                              | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                           | Always  |
|             |                                |            |                   |                                                 |         |
|             |                                |            |                   | 1 = suppress positive response                  |         |
|             +--------------------------------+------------+-------------------+-------------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x19              | reportUserDefMemoryDTCExtDataRecordByDTCNumber  | Always  |
+-------------+--------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTC                                          | 24         | 0x000000-0xFFFFFF | DTC number                                      | Always  |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8          | 0x00-0xFF         | 0x00: reserved                                  | Always  |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x01-0x8F: vehicle manufacturer specific record |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0x90-0x9F: regulated emissions OBD record       |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xA0-0xEF: regulated record                     |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xF0-0xFD: reserved                             |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFE: all regulated emissions OBD records       |         |
|                                              |            |                   |                                                 |         |
|                                              |            |                   | 0xFF: all extended data records                 |         |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+
| MemorySelection                              | 8          | 0x00-0xFF         | Specifies DTC memory                            | Always  |
+----------------------------------------------+------------+-------------------+-------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.

.. note:: :code:`MemorySelection` allows reading DTC related information from a specific DTC memory (e.g. one of
  the sub-systems).


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                    | Present                                       |
+=================================================+============+===================+================================================+===============================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19)   | Always                                        |
+----------------+--------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                          | Always                                        |
|                |                                |            |                   |                                                |                                               |
|                |                                |            |                   | 1 = suppress positive response                 |                                               |
|                +--------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x19              | reportUserDefMemoryDTCExtDataRecordByDTCNumber | Always                                        |
+----------------+--------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| MemorySelection                                 | 8          | 0x00-0xFF         | Selected memory                                | Always                                        |
+----------------+--------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | Considered DTC                                 | Always                                        |
|                +--------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC                                  | Always                                        |
+----------------+--------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| DTCExtDataRecordNumber#1                        | 8          | 0x00-0xFF         | Number of requested DTCExtDataRecord(s)        | If at least one DTCExtDataRecord is available |
+-------------------------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| DTCExtDataRecord#1                              | at least 8 |                   | Extended Data #1                               | If at least one DTCExtDataRecord is available |
+-------------------------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| ...                                                                                                                                                                               |
+-------------------------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+
| DTCExtDataRecord#n                              | at least 8 |                   | Extended Data #n                               | If at least n DTCExtDataRecords are available |
+-------------------------------------------------+------------+-------------------+------------------------------------------------+-----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-1A:

reportSupportedDTCExtDataRecord (0x1A)
``````````````````````````````````````
This sub-function can be used by the client to request the list of DTCs that support a given
extended data record number (*DTCExtDataRecordNumber*).

.. warning:: Introduced in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+---------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                     | Present |
+==============================================+============+===========+=================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation              | Always  |
+-------------+--------------------------------+------------+-----------+---------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required           | Always  |
|             |                                |            |           |                                 |         |
|             |                                |            |           | 1 = suppress positive response  |         |
|             +--------------------------------+------------+-----------+---------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x1A      | reportSupportedDTCExtDataRecord | Always  |
+-------------+--------------------------------+------------+-----------+---------------------------------+---------+
| DTCExtDataRecordNumber                       | 8          | 0x00-0xFD | Extended data record number     | Always  |
+----------------------------------------------+------------+-----------+---------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                                    |
+=================================================+============+===================+==============================================+============================================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                                     |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                                     |
|                |                                |            |                   |                                              |                                                            |
|                |                                |            |                   | 1 = suppress positive response               |                                                            |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x1A              | reportSupportedDTCExtDataRecord              | Always                                                     |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                                     |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| DTCExtDataRecordNumber                          | 8          | 0x01-0xFD         | Identification number of DTCExtDataRecord    | If at least one DTC supports the selected DTCExtDataRecord |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC supports the selected DTCExtDataRecord |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                                            |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                                            |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
|                | ...                                                                                                                                                                         |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs support the selected DTCExtDataRecord   |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                                            |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                                            |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-42:

reportWWHOBDDTCByMaskRecord (0x42)
``````````````````````````````````
This sub-function can be used by the client to request WWH-OBD DTCs and their associated status and
severity information, filtered by a status mask (*DTCStatusMask*) and a severity mask (*DTCSeverityMaskRecord*).


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                             | Present |
+==============================================+============+===========+=========================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                   | Always  |
|             |                                |            |           |                                         |         |
|             |                                |            |           | 1 = suppress positive response          |         |
|             +--------------------------------+------------+-----------+-----------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x42      | reportWWHOBDDTCByMaskRecord             | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------+---------+
| FunctionalGroupIdentifier                    | 8          | 0x00-0xFF | 0x00-0x32: reserved                     | Always  |
|                                              |            |           |                                         |         |
|                                              |            |           | 0x33: emissions-system group            |         |
|                                              |            |           |                                         |         |
|                                              |            |           | 0x34-0xCF: reserved                     |         |
|                                              |            |           |                                         |         |
|                                              |            |           | 0xD0: safety-system group               |         |
|                                              |            |           |                                         |         |
|                                              |            |           | 0xD1-0xDF: legislative system group     |         |
|                                              |            |           |                                         |         |
|                                              |            |           | 0xE0-0xFD: reserved                     |         |
|                                              |            |           |                                         |         |
|                                              |            |           | 0xFE: VOBD system                       |         |
|                                              |            |           |                                         |         |
|                                              |            |           | 0xFF: reserved                          |         |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCSeverityMaskRecord                        | 8          | 0x00-0xFF | Severity mask to use for DTC matching   | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+
| DTCStatusMask                                | 8          | 0x00-0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+------------+-----------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                                          | Bit Length | Value             | Description                                  | Present                                  |
+===============================================================+============+===================+==============================================+==========================================+
| RSID                                                          | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction                  | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                              |                                |            |                   |                                              |                                          |
|                              |                                |            |                   | 1 = suppress positive response               |                                          |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                              | reportType                     | 7 (b[6-0]) | 0x42              | reportWWHOBDDTCByMaskRecord                  | Always                                   |
+------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| FunctionalGroupIdentifier                                     | 8          | 0x00-0xFF         | 0x00-0x32: reserved                          | Always                                   |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0x33: emissions-system group                 |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0x34-0xCF: reserved                          |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0xD0: safety-system group                    |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0xD1-0xDF: legislative system group          |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0xE0-0xFD: reserved                          |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0xFE: VOBD system                            |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0xFF: reserved                               |                                          |
+---------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                                     | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+---------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCSeverityAvailabilityMask                                   | 8          | 0x00-0xFF         | DTC Severity bits supported by the ECU       | Always                                   |
+---------------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCFormatIdentifier                                           | 8          | 0x00-0xFF         | 0x00: SAE J2012-DA DTC Format 00             | Always                                   |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0x01: ISO 14229-1 DTC Format                 |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0x02: SAE J1939-73 DTC Format                |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0x03: ISO 11992-4 DTC Format                 |                                          |
|                                                               |            |                   |                                              |                                          |
|                                                               |            |                   | 0x04: SAE J2012-DA DTC Format 04             |                                          |
+------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Severity, DTC and DTC Status | DTCSeverity                    | 8          | 0x00-0xFF         | Severity of DTC#1                            | If at least one DTC matches the criteria |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                              | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        |                                          |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                              | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                              | ...                                                                                                                                                       |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                              | DTCSeverity                    | 8          | 0x00-0xFF         | Severity of DTC#n                            | If at least n DTCs matches the criteria  |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                              | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        |                                          |
|                              +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                              | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+------------------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-55:

reportWWHOBDDTCWithPermanentStatus (0x55)
`````````````````````````````````````````
This sub-function can be used by the client to request WWH-OBD DTCs with permanent status.


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+-------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                         | Present |
+==============================================+============+===========+=====================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                  | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required               | Always  |
|             |                                |            |           |                                     |         |
|             |                                |            |           | 1 = suppress positive response      |         |
|             +--------------------------------+------------+-----------+-------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x55      | reportWWHOBDDTCWithPermanentStatus  | Always  |
+-------------+--------------------------------+------------+-----------+-------------------------------------+---------+
| FunctionalGroupIdentifier                    | 8          | 0x00-0xFF | 0x00-0x32: reserved                 | Always  |
|                                              |            |           |                                     |         |
|                                              |            |           | 0x33: emissions-system group        |         |
|                                              |            |           |                                     |         |
|                                              |            |           | 0x34-0xCF: reserved                 |         |
|                                              |            |           |                                     |         |
|                                              |            |           | 0xD0: safety-system group           |         |
|                                              |            |           |                                     |         |
|                                              |            |           | 0xD1-0xDF: legislative system group |         |
|                                              |            |           |                                     |         |
|                                              |            |           | 0xE0-0xFD: reserved                 |         |
|                                              |            |           |                                     |         |
|                                              |            |           | 0xFE: VOBD system                   |         |
|                                              |            |           |                                     |         |
|                                              |            |           | 0xFF: reserved                      |         |
+----------------------------------------------+------------+-----------+-------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                                  | Bit Length | Value             | Description                                  | Present                                  |
+=======================================================+============+===================+==============================================+==========================================+
| RSID                                                  | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction          | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                      |                                |            |                   |                                              |                                          |
|                      |                                |            |                   | 1 = suppress positive response               |                                          |
|                      +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                      | reportType                     | 7 (b[6-0]) | 0x55              | reportWWHOBDDTCWithPermanentStatus           | Always                                   |
+----------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| FunctionalGroupIdentifier                             | 8          | 0x00-0xFF         | 0x00-0x32: reserved                          | Always                                   |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0x33: emissions-system group                 |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0x34-0xCF: reserved                          |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0xD0: safety-system group                    |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0xD1-0xDF: legislative system group          |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0xE0-0xFD: reserved                          |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0xFE: VOBD system                            |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0xFF: reserved                               |                                          |
+-------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                             | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+-------------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCFormatIdentifier                                   | 8          | 0x00-0xFF         | 0x00: SAE J2012-DA DTC Format 00             | Always                                   |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0x01: ISO 14229-1 DTC Format                 |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0x02: SAE J1939-73 DTC Format                |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0x03: ISO 11992-4 DTC Format                 |                                          |
|                                                       |            |                   |                                              |                                          |
|                                                       |            |                   | 0x04: SAE J2012-DA DTC Format 04             |                                          |
+----------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status       | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                      +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                      | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                      +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                      | ...                                                                                                                                                       |
|                      +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                      | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                      +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                      | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-56:

reportDTCInformationByDTCReadinessGroupIdentifier (0x56)
````````````````````````````````````````````````````````
This sub-function can be used by the client to request OBD DTCs that belong to a given
readiness group (*DTCReadinessGroupIdentifier*).

.. warning:: Introduced in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+------------+-----------+---------------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                       | Present |
+==============================================+============+===========+===================================================+=========+
| SID                                          | 8          | 0x19      | ReadDTCInformation                                | Always  |
+-------------+--------------------------------+------------+-----------+---------------------------------------------------+---------+
| SubFunction | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1   | 0 = response required                             | Always  |
|             |                                |            |           |                                                   |         |
|             |                                |            |           | 1 = suppress positive response                    |         |
|             +--------------------------------+------------+-----------+---------------------------------------------------+---------+
|             | reportType                     | 7 (b[6-0]) | 0x56      | reportDTCInformationByDTCReadinessGroupIdentifier | Always  |
+-------------+--------------------------------+------------+-----------+---------------------------------------------------+---------+
| FunctionalGroupIdentifier                    | 8          | 0x00-0xFF | 0x00-0x32: reserved                               | Always  |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0x33: emissions-system group                      |         |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0x34-0xCF: reserved                               |         |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0xD0: safety-system group                         |         |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0xD1-0xDF: legislative system group               |         |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0xE0-0xFD: reserved                               |         |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0xFE: VOBD system                                 |         |
|                                              |            |           |                                                   |         |
|                                              |            |           | 0xFF: reserved                                    |         |
+----------------------------------------------+------------+-----------+---------------------------------------------------+---------+
| DTCReadinessGroupIdentifier                  | 8          | 0x00-0xFF | Specifies DTC readiness group                     | Always  |
+----------------------------------------------+------------+-----------+---------------------------------------------------+---------+

.. note:: `SAE J1979-DA <https://www.sae.org/standards/j1979da_202203-j1979-da-digital-annex-e-e-diagnostic-test-modes>`_
  defines values mapping for *DTCReadinessGroupIdentifier* parameter.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length | Value             | Description                                  | Present                                  |
+=================================================+============+===================+==============================================+==========================================+
| RSID                                            | 8          | 0x59              | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| SubFunction    | suppressPosRspMsgIndicationBit | 1 (b[7])   | 0x0-0x1           | 0 = response required                        | Always                                   |
|                |                                |            |                   |                                              |                                          |
|                |                                |            |                   | 1 = suppress positive response               |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b[6-0]) | 0x56              | reportDTCByReadinessGroupIdentifier          | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| FunctionalGroupIdentifier                       | 8          | 0x00-0xFF         | 0x00-0x32: reserved                          | Always                                   |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0x33: emissions-system group                 |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0x34-0xCF: reserved                          |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0xD0: safety-system group                    |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0xD1-0xDF: legislative system group          |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0xE0-0xFD: reserved                          |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0xFE: VOBD system                            |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0xFF: reserved                               |                                          |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8          | 0x00-0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCFormatIdentifier                             | 8          | 0x00-0xFF         | 0x00: SAE J2012-DA DTC Format 00             | Always                                   |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0x01: ISO 14229-1 DTC Format                 |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0x02: SAE J1939-73 DTC Format                |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0x03: ISO 11992-4 DTC Format                 |                                          |
|                                                 |            |                   |                                              |                                          |
|                                                 |            |                   | 0x04: SAE J2012-DA DTC Format 04             |                                          |
+-------------------------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTCReadinessGroupIdentifier                     | 8          | 0x00-0xFF         | Selected readiness group                     | Always                                   |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
| DTC and Status | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#1                              |                                          |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | ...                                                                                                                                                       |
|                +--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+
|                | DTC                            | 24         | 0x000000-0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+------------+-------------------+----------------------------------------------+                                          |
|                | DTCStatus                      | 8          | 0x00-0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+------------+-------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-data-by-identifier:

ReadDataByIdentifier
--------------------
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
| DID#1      | 16         | 0x0000-0xFFFF | DID#1                                          | Always                                           |
+------------+------------+---------------+------------------------------------------------+                                                  |
| DID#1 data | at least 8 |               | Data stored under DID#1                        |                                                  |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+
| ...                                                                                                                                         |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+
| DID#n      | 16         | 0x0000-0xFFFF | DID#n                                          | If at least n DIDs were requested by the client. |
+------------+------------+---------------+------------------------------------------------+                                                  |
| DID#n data | at least 8 |               | Data stored under DID#n                        |                                                  |
+------------+------------+---------------+------------------------------------------------+--------------------------------------------------+


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


.. _knowledge-base-service-dynamically-define-data-identifier:

DynamicallyDefineDataIdentifier
-------------------------------
DynamicallyDefineDataIdentifier service allows the client to dynamically define in a server a DataIdentifier (DID)
that can be read via the ReadDataByIdentifier_ service at a later time.


.. _knowledge-base-service-write-data-by-identifier:

WriteDataByIdentifier
---------------------
WriteDataByIdentifier service allows the client to write information into the server at an internal location
specified by the provided DataIdentifier (DID).


.. _knowledge-base-service-input-output-control-by-identifier:

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

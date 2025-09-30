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
+----------------------------------------------+------------+-----------+-----------------------------------------------+---------+
| Name                                         | Bit Length | Value     | Description                                   | Present |
+==============================================+============+===========+===============================================+=========+
| SID                                          | 8          | 0x10      | DiagnosticSessionControl                      | Always  |
+-------------+--------------------------------+------------+-----------+-----------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)     | 0x0-0x1   | 0 = response required                         | Always  |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 1 = suppress positive response                |         |
|             +--------------------------------+------------+-----------+-----------------------------------------------+         |
|             | diagnosticSessionType          | 7 (b6-b0)  | 0x00-0x7F | 0x00: reserved                                |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x01: defaultSession                          |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x02: programmingSession                      |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x03: extendedDiagnosticSession               |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x04: safetySystemDiagnosticSession           |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x05–0x3F: reserved                           |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x40–0x5F: available for vehicle manufacturer |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0x60–0x7E: available for system supplier      |         |
|             |                                |            |           |                                               |         |
|             |                                |            |           | 0xFF: reserved                                |         |
+-------------+--------------------------------+------------+-----------+-----------------------------------------------+---------+


Positive Response Format
````````````````````````
+---------------------------------------------------------+------------+---------------+----------------------------------------------------+---------+
| Name                                                    | Bit Length | Value         | Description                                        | Present |
+=========================================================+============+===============+====================================================+=========+
| RSID                                                    | 8          | 0x50          | Positive Response: DiagnosticSessionControl (0x10) | Always  |
+------------------------+--------------------------------+------------+---------------+----------------------------------------------------+---------+
| subFunction            | suppressPosRspMsgIndicationBit | 1 (b7)     | 0x0-0x1       | 0 = response required                              | Always  |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 1 = suppress positive response                     |         |
|                        +--------------------------------+------------+---------------+----------------------------------------------------+         |
|                        | diagnosticSessionType          | 7 (b6-b0)  | 0x00-0x7F     | 0x00: reserved                                     |         |
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
|                        |                                |            |               | 0x40–0x5F: available for vehicle manufacturer      |         |
|                        |                                |            |               |                                                    |         |
|                        |                                |            |               | 0x60–0x7E: available for system supplier           |         |
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


.. _knowledge-base-service-clear-diagnostic-information:

ClearDiagnosticInformation
--------------------------
ClearDiagnosticInformation service is used by the client to clear Diagnostic Trouble Codes (DTCs) and related data
stored in one or more server memories.


Request Format
``````````````


ISO 14229-1:2020
''''''''''''''''
+-----------------+------------+---------------------+----------------------------+----------+
| Name            | Bit Length | Value               | Description                | Present  |
+=================+============+=====================+============================+==========+
| SID             | 8          | 0x14                | ClearDiagnosticInformation | Always   |
+-----------------+------------+---------------------+----------------------------+----------+
| groupOfDTC      | 24         | 0x000000 - 0xFFFFFF | DTCs to be cleared         | Always   |
+-----------------+------------+---------------------+----------------------------+----------+
| MemorySelection | 8          | 0x00 - 0xFF         | Identifies DTC memory      | Optional |
+-----------------+------------+---------------------+----------------------------+----------+

.. note:: In ISO 14229-1:2020 the optional :code:`MemorySelection` field was introduced to allow clearing diagnostic
  information from a specific DTC memory (e.g. one of the sub-systems).


ISO 14229-1:2013
''''''''''''''''
+------------+------------+---------------------+----------------------------+---------+
| Name       | Bit Length | Value               | Description                | Present |
+============+============+=====================+============================+=========+
| SID        | 8          | 0x14                | ClearDiagnosticInformation | Always  |
+------------+------------+---------------------+----------------------------+---------+
| groupOfDTC | 24         | 0x000000 - 0xFFFFFF | DTCs to be cleared         | Always  |
+------------+------------+---------------------+----------------------------+---------+


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
ReadDTCInformation service allows the client to request current Diagnostic Trouble Code (DTC) information from
one or more servers within the vehicle.

ISO 14229-1 defines the following DTC report types (values of the *reportType* parameter):

- 0x01 - reportNumberOfDTCByStatusMask
- 0x02 - reportDTCByStatusMask
- 0x03 - reportDTCSnapshotIdentification
- 0x04 - reportDTCSnapshotRecordByDTCNumber
- 0x05 - reportDTCStoredDataByRecordNumber
- 0x06 - reportDTCExtDataRecordByDTCNumber
- 0x07 - reportNumberOfDTCBySeverityMaskRecord
- 0x08 - reportDTCBySeverityMaskRecord
- 0x09 - reportSeverityInformationOfDTC
- 0x0A - reportSupportedDTC
- 0x0D - reportMostRecentTestFailedDTC
- 0x0E - reportMostRecentConfirmedDTC
- 0x0F - reportMirrorMemoryDTCByStatusMask (withdrawn in ISO 14229-1:2020)
- 0x10 - reportMirrorMemoryDTCExtDataRecordByDTCNumber (withdrawn in ISO 14229-1:2020)
- 0x11 - reportNumberOfMirrorMemoryDTCByStatusMask (withdrawn in ISO 14229-1:2020)
- 0x12 - reportNumberOfEmissionsOBDDTCByStatusMask (withdrawn in ISO 14229-1:2020)
- 0x13 - reportEmissionsOBDDTCByStatusMask (withdrawn in ISO 14229-1:2020)
- 0x14 - reportDTCFaultDetectionCounter
- 0x15 - reportDTCWithPermanentStatus
- 0x16 - reportDTCExtDataRecordByRecordNumber
- 0x17 - reportUserDefMemoryDTCByStatusMask
- 0x18 - reportUserDefMemoryDTCSnapshotRecordByDTCNumber
- 0x19 - reportUserDefMemoryDTCExtDataRecordByDTCNumber
- 0x1A - reportSupportedDTCExtDataRecord (introduced in ISO 14229-1:2020)
- 0x42 - reportWWHOBDDTCByMaskRecord
- 0x55 - reportWWHOBDDTCWithPermanentStatus
- 0x56 - reportDTCInformationByDTCReadinessGroupIdentifier (introduced in ISO 14229-1:2020)


.. _knowledge-base-service-read-dtc-information-01:

reportNumberOfDTCByStatusMask (0x01)
````````````````````````````````````
This sub-function can be used by the client to request the number of stored DTCs that match
a specific status mask (*DTCStatusMask*).
It is typically used as a lightweight way to determine how many DTCs fulfill a given diagnostic condition without
retrieving the DTC values themselves.

Request Format
''''''''''''''
The *DTCStatusMask* parameter defines which status bits should be used as a filter when matching DTCs.
A value of 0x00 means that no status bits are selected. Since no DTC can match this, the result will always be
a count of 0.

+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                             | Present |
+==============================================+=============+=============+=========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|             |                                |             |             |                                         |         |
|             |                                |             |             | 1 = suppress positive response          |         |
|             +--------------------------------+-------------+-------------+-----------------------------------------+         |
|             | reportType                     | 7 (b6 - b0) | 0x01        | reportNumberOfDTCByStatusMask           |         |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| Name                                         | Bit Length  | Value           | Description                                  | Present |
+==============================================+=============+=================+==============================================+=========+
| RSID                                         | 8           | 0x59            | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1       | 0 = response required                        | Always  |
|             |                                |             |                 |                                              |         |
|             |                                |             |                 | 1 = suppress positive response               |         |
|             +--------------------------------+-------------+-----------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x01            | reportNumberOfDTCByStatusMask                | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8           | 0x00 - 0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8           | 0x00 - 0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCCount                                     | 16          | 0x0000 - 0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-02:

reportDTCByStatusMask (0x02)
````````````````````````````
This sub-function can be used by the client to request a list of all DTCs stored in the server’s memory that match
a specific status mask (*DTCStatusMask*). A DTC is included in the response if :code:`DTC Status & DTCStatusMask) != 0`.
This sub-function provides the client with both the DTC values and their corresponding status information for
all DTCs that satisfy the given mask.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                             | Present |
+==============================================+=============+=============+=========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|             |                                |             |             |                                         |         |
|             |                                |             |             | 1 = suppress positive response          |         |
|             +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x02        | reportDTCByStatusMask                   | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                  |
+=================================================+=============+=====================+==============================================+==========================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                |                                |             |                     |                                              |                                          |
|                |                                |             |                     | 1 = suppress positive response               |                                          |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x02                | reportDTCByStatusMask                        | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-03:

reportDTCSnapshotIdentification (0x03)
``````````````````````````````````````
This sub-function can be used by the client to request identification of all stored DTC snapshot records.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+---------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                     | Present |
+==============================================+=============+===========+=================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation              | Always  |
+-------------+--------------------------------+-------------+-----------+---------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required           | Always  |
|             |                                |             |           |                                 |         |
|             |                                |             |           | 1 = suppress positive response  |         |
|             +--------------------------------+-------------+-----------+---------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x03      | reportDTCSnapshotIdentification | Always  |
+-------------+--------------------------------+-------------+-----------+---------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+
| Name                                         | Bit Length  | Value               | Description                                      | Present                                         |
+==============================================+=============+=====================+==================================================+=================================================+
| RSID                                         | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19)     | Always                                          |
+-------------+--------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                            | Always                                          |
|             |                                |             |                     |                                                  |                                                 |
|             |                                |             |                     | 1 = suppress positive response                   |                                                 |
|             +--------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+
|             | reportType                     | 7 (b6 - b0) | 0x03                | reportDTCSnapshotIdentification                  | Always                                          |
+-------------+--------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+
| DTCRecord#1                                  | 24          | 0x000000 - 0xFFFFFF | DTC for which DTCSnapshot record #1 was reported | If at least one DTCSnapshot record is available |
+----------------------------------------------+-------------+---------------------+--------------------------------------------------+                                                 |
| DTCSnapshotRecordNumber#1                    | 8           | 0x00 - 0xFF         |                                                  |                                                 |
+----------------------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+
| ...                                                                                                                                                                                   |
+----------------------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+
| DTCRecord#n                                  | 24          | 0x000000 - 0xFFFFFF | DTC for which DTCSnapshot record #n was reported | If at least n DTCSnapshot records are available |
+----------------------------------------------+-------------+---------------------+--------------------------------------------------+                                                 |
| DTCSnapshotRecordNumber#n                    | 8           | 0x00 - 0xFF         | Status of DTC#n                                  |                                                 |
+----------------------------------------------+-------------+---------------------+--------------------------------------------------+-------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-04:

reportDTCSnapshotRecordByDTCNumber (0x04)
`````````````````````````````````````````
This sub-function can be used by the client to request snapshot data for a specific DTC (*DTCMaskRecord*)
and snapshot record number (*DTCSnapshotRecordNumber*).

Request Format
''''''''''''''
+----------------------------------------------+-------------+---------------------+--------------------------------------+---------+
| Name                                         | Bit Length  | Value               | Description                          | Present |
+==============================================+=============+=====================+======================================+=========+
| SID                                          | 8           | 0x19                | ReadDTCInformation                   | Always  |
+-------------+--------------------------------+-------------+---------------------+--------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                | Always  |
|             |                                |             |                     |                                      |         |
|             |                                |             |                     | 1 = suppress positive response       |         |
|             +--------------------------------+-------------+---------------------+--------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x04                | reportDTCSnapshotRecordByDTCNumber   | Always  |
+-------------+--------------------------------+-------------+---------------------+--------------------------------------+---------+
| DTCMaskRecord                                | 24          | 0x000000 - 0xFFFFFF | DTC number                           | Always  |
+----------------------------------------------+-------------+---------------------+--------------------------------------+---------+
| DTCSnapshotRecordNumber                      | 8           | 0x00 - 0xFF         | 0x00: reserved (legislated purposes) | Always  |
|                                              |             |                     |                                      |         |
|                                              |             |                     | 0x01 - 0xFE: select snapshot record  |         |
|                                              |             |                     |                                      |         |
|                                              |             |                     | 0xFF: all snapshot records           |         |
+----------------------------------------------+-------------+---------------------+--------------------------------------+---------+

.. note:: *DTCSnapshotRecordNumber* (0x01–0xFE) selects a single snapshot record.
  If equal to 0xFF, all available snapshot records for the DTC are returned.


Positive Response Format
''''''''''''''''''''''''
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| Name                                                 | Bit Length  | Value               | Description                                              | Present                                                      |
+======================================================+=============+=====================+==========================================================+==============================================================+
| RSID                                                 | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19)             | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
|     subFunction     | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                                    | Always                                                       |
|                     |                                |             |                     |                                                          |                                                              |
|                     |                                |             |                     | 1 = suppress positive response                           |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
|                     | reportType                     | 7 (b6 - b0) | 0x04                | reportDTCSnapshotRecordByDTCNumber                       | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| DTCRecord           | DTC                            | 24          | 0x000000 - 0xFFFFFF | Considered DTC                                           | Always                                                       |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
|                     | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                               | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| DTCSnapshotRecordNumber#1                            | 8           | 0x00 - 0xFF         | Number of DTCSnapshot#1                                  | If at least one DTCSnapshot record is available for the DTC  |
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecordNumberOfIdentifiers#1               | 8           | 0x00 - 0xFF         | Number of Identifiers stored by DTCSnapshot#1 (equals m) |                                                              |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecord#1 | dataIdentifier#1               | 16          | 0x0000 - 0xFFFF     | DID#1 that is part of DTCSnapshot#1                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#1           |             |                     | Data stored under DID#1                                  |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | ...                                                                                                                           |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifier#m               | 16          | 0x0000 - 0xFFFF     | DID#m that is part of DTCSnapshot#1                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#m           |             |                     | Data stored under DID#m                                  |                                                              |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| ...                                                                                                                                                                                                                |
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| DTCSnapshotRecordNumber#n                            | 28          | 0x00 - 0xFF         | Number of DTCSnapshot#n                                  | If requested for multiple DTCSnapshot records                |
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecordNumberOfIdentifiers#n               | 8           | 0x00 - 0xFF         | Number of Identifiers stored by DTCSnapshot#n (equals k) | And at least n DTCSnapshot records are available for the DTC |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecord#n | dataIdentifier#1               | 16          | 0x0000 - 0xFFFF     | DID#1 that is part of DTCSnapshot#n                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#1           | 8 or more   |                     | Data stored under DID#1                                  |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | ...                                                                                                                           |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifier#k               | 16          | 0x0000 - 0xFFFF     | DID#k that is part of DTCSnapshot#n                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#k           | 8 or more   |                     | Data stored under DID#k                                  |                                                              |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-05:

reportDTCStoredDataByRecordNumber (0x05)
````````````````````````````````````````
This sub-function can be used by the client to request stored data for a specific record (*DTCStoredDataRecordNumber*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+--------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                          | Present |
+==============================================+=============+=============+======================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                   | Always  |
+-------------+--------------------------------+-------------+-------------+--------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                | Always  |
|             |                                |             |             |                                      |         |
|             |                                |             |             | 1 = suppress positive response       |         |
|             +--------------------------------+-------------+-------------+--------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x05        | reportDTCStoredDataByRecordNumber    | Always  |
+-------------+--------------------------------+-------------+-------------+--------------------------------------+---------+
| DTCStoredDataRecordNumber                    | 8           | 0x00 - 0xFF | 0x00: reserved (legislated purposes) | Always  |
|                                              |             |             |                                      |         |
|                                              |             |             | 0x01 – 0xFE: select record           |         |
|                                              |             |             |                                      |         |
|                                              |             |             | 0xFF: all records                    |         |
+----------------------------------------------+-------------+-------------+--------------------------------------+---------+

.. note:: *DTCStoredDataRecordNumber* (0x01–0xFE) selects a single stored data record.
  If equal to 0xFF, all available stored data records for the DTC are returned.


Positive Response Format
''''''''''''''''''''''''
+------------------------------------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
| Name                                                       | Bit Length  | Value               | Description                                                | Present                                           |
+============================================================+=============+=====================+============================================================+===================================================+
| RSID                                                       | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19)               | Always                                            |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
| subFunction               | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                                      | Always                                            |
|                           |                                |             |                     |                                                            |                                                   |
|                           |                                |             |                     | 1 = suppress positive response                             |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
|                           | reportType                     | 7 (b6 - b0) | 0x05                | reportDTCStoredDataByRecordNumber                          | Always                                            |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
| DTCStoredDataRecordNumber#1                                | 8           | 0x00 - 0xFF         | Number of DTCStoredData#1 record or echo from the request  | Always                                            |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
| DTCRecord#1               | DTC#1                          | 24          | 0x000000 - 0xFFFFFF | DTC for which first record was reported                    | If at least one DTCStoredData record is available |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | statusOfDTC#1                  | 8           | 0x00 - 0xFF         | DTC#1 status                                               |                                                   |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
| DTCStoredDataRecordNumberOfIdentifiers#1                   | 8           | 0x00 - 0xFF         | Number of Identifiers stored by DTCStoredData#1 (equals m) |                                                   |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
| DTCStoredDataRecord#1#1   | dataIdentifier#1               | 16          | 0x0000 - 0xFFFF     | DID#1 that is part of DTCStoredData#1                      |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | dataIdentifierData#1           |             |                     | Data stored under DID#1                                    |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | ...                                                                                                                             |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | dataIdentifier#m               | 16          | 0x0000 - 0xFFFF     | DID#m that is part of DTCStoredData#1                      |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | dataIdentifierData#m           |             |                     | Data stored under DID#m                                    |                                                   |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
| ...                                                                                                                                                                                                             |
+------------------------------------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+
| DTCStoredDataRecordNumber#n                                | 24          | 0x000000 - 0xFFFFFF | Number of DTCStoredData#n record                           | If at least n DTCStoredData records are available |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
| DTCRecord#n               | DTC#n                          | 24          | 0x000000 - 0xFFFFFF | DTC for which n'th record was reported                     |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | statusOfDTC#n                  | 8           | 0x00 - 0xFF         | DTC#n status                                               |                                                   |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
| DTCSnapshotRecordNumber#n | DTC Status                     | 8           | 0x00 - 0xFF         | Number of Identifiers stored by DTCStoredData#1 (equals k) |                                                   |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
| DTCStoredDataRecord#n     | dataIdentifier#1               | 16          | 0x0000 - 0xFFFF     | DID#1 that is part of DTCStoredData#n                      |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | dataIdentifierData#1           | 8 or more   |                     | Data stored under DID#1                                    |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | ...                                                                                                                             |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | dataIdentifier#k               | 16          | 0x0000 - 0xFFFF     | DID#k that is part of DTCStoredData#n                      |                                                   |
|                           +--------------------------------+-------------+---------------------+------------------------------------------------------------+                                                   |
|                           | dataIdentifierData#k           | 8 or more   |                     | Data stored under DID#k                                    |                                                   |
+---------------------------+--------------------------------+-------------+---------------------+------------------------------------------------------------+---------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-06:

reportDTCExtDataRecordByDTCNumber (0x06)
````````````````````````````````````````
This sub-function can be used by the client to request extended data records for a specific DTC (*DTCMaskRecord*)
and record number (*DTCExtDataRecordNumber*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| Name                                         | Bit Length  | Value               | Description                                              | Present |
+==============================================+=============+=====================+==========================================================+=========+
| SID                                          | 8           | 0x19                | ReadDTCInformation                                       | Always  |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                                    | Always  |
|             |                                |             |                     |                                                          |         |
|             |                                |             |                     | 1 = suppress positive response                           |         |
|             +--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x06                | reportDTCExtDataRecordByDTCNumber                        | Always  |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| DTCMaskRecord                                | 24          | 0x000000 - 0xFFFFFF | DTC number                                               | Always  |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8           | 0x00 - 0xFF         | 0x00: reserved                                           | Always  |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0x01 - 0x8F: select vehicle manufacturer specific record |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0x90 - 0x9F: select regulated emissions OBD record       |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xA0 - 0xEF: select regulated record                     |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xF0 - 0xFD: reserved                                    |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xFE: all regulated emissions OBD records                |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xFF: all extended data records                          |         |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
| Name                                         | Bit Length  | Value               | Description                                  | Present                                                      |
+==============================================+=============+=====================+==============================================+==============================================================+
| RSID                                         | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                                       |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                                       |
|             |                                |             |                     |                                              |                                                              |
|             |                                |             |                     | 1 = suppress positive response               |                                                              |
|             +--------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
|             | reportType                     | 7 (b6 - b0) | 0x06                | reportDTCExtDataRecordByDTCNumber            | Always                                                       |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
| DTCRecord   | DTC                            | 24          | 0x000000 - 0xFFFFFF | Considered DTC                               | Always                                                       |
|             +--------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
|             | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                   | Always                                                       |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
| DTCExtDataRecordNumber#1                     | 8           | 0x00 - 0xFF         | Number of DTCExtDataRecord#1                 | If at least one DTCExtDataRecord is available for the DTC    |
+----------------------------------------------+-------------+---------------------+----------------------------------------------+                                                              |
| DTCExtDataRecord#1                           | at least 8  |                     | Extended Data #1                             |                                                              |
+----------------------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
| ...                                                                                                                                                                                            |
+----------------------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+
| DTCExtDataRecordNumber#n                     | 8           | 0x00 - 0xFF         | Number of DTCExtDataRecord#n                 | If requested for multiple DTCSnapshot records                |
+----------------------------------------------+-------------+---------------------+----------------------------------------------+                                                              |
| DTCExtDataRecord#n                           | at least 8  |                     | Extended Data #n                             | And at least n DTCSnapshot records are available for the DTC |
+----------------------------------------------+-------------+---------------------+----------------------------------------------+--------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-07:

reportNumberOfDTCBySeverityMaskRecord (0x07)
````````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs that match a given
severity mask (*DTCSeverityMask*) and status mask (*DTCStatusMask*).


Request Format
''''''''''''''
+--------------------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                                   | Bit Length  | Value       | Description                             | Present |
+========================================================+=============+=============+=========================================+=========+
| SID                                                    | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-----------------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction           | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|                       |                                |             |             |                                         |         |
|                       |                                |             |             | 1 = suppress positive response          |         |
|                       +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|                       | reportType                     | 7 (b6 - b0) | 0x07        | reportNumberOfDTCBySeverityMaskRecord   | Always  |
+-----------------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCSeverityMaskRecord | DTCSeverityMask                | 8           | 0x00 - 0xFF | Severity mask to use for DTC matching   | Always  |
|                       +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|                       | DTCStatusMask                  | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+-----------------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| Name                                         | Bit Length  | Value           | Description                                  | Present |
+==============================================+=============+=================+==============================================+=========+
| RSID                                         | 8           | 0x59            | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1       | 0 = response required                        | Always  |
|             |                                |             |                 |                                              |         |
|             |                                |             |                 | 1 = suppress positive response               |         |
|             +--------------------------------+-------------+-----------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x07            | reportNumberOfDTCBySeverityMaskRecord        | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8           | 0x00 - 0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8           | 0x00 - 0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCCount                                     | 16          | 0x0000 - 0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-08:

reportDTCBySeverityMaskRecord (0x08)
````````````````````````````````````
This sub-function can be used by the client to request all DTCs that match a given severity mask (*DTCSeverityMask*)
and status mask (*DTCStatusMask*).


Request Format
''''''''''''''
+--------------------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                                   | Bit Length  | Value       | Description                             | Present |
+========================================================+=============+=============+=========================================+=========+
| SID                                                    | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-----------------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction           | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|                       |                                |             |             |                                         |         |
|                       |                                |             |             | 1 = suppress positive response          |         |
|                       +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|                       | reportType                     | 7 (b6 - b0) | 0x08        | reportDTCBySeverityMaskRecord           | Always  |
+-----------------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCSeverityMaskRecord | DTCSeverityMask                | 8           | 0x00 - 0xFF | Severity mask to use for DTC matching   | Always  |
|                       +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|                       | DTCStatusMask                  | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+-----------------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                                    | Bit Length  | Value               | Description                                  | Present                                  |
+=========================================================+=============+=====================+==============================================+==========================================+
| RSID                                                    | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|       subFunction      | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                        |                                |             |                     |                                              |                                          |
|                        |                                |             |                     | 1 = suppress positive response               |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                        | reportType                     | 7 (b6 - b0) | 0x08                | reportDTCBySeverityMaskRecord                | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                               | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndSeverityRecord#1 | DTCSeverity                    | 8           | 0x00 - 0xFF         | Severity of DTC                              | If at least one DTC matches the criteria |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTCFunctionalUnit              | 8           | 0x00 - 0xFF         | Functional Unit of DTC                       |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndSeverityRecord#n | DTCSeverity                    | 8           | 0x00 - 0xFF         | Severity of DTC                              | If at least n DTCs matches the criteria  |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTCFunctionalUnit              | 8           | 0x00 - 0xFF         | Functional Unit of DTC                       |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-09:

reportSeverityInformationOfDTC (0x09)
`````````````````````````````````````
This sub-function can be used by the client to request severity and functional unit information for
a specific DTC (*DTCMaskRecord*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+---------------------+--------------------------------+---------+
| Name                                         | Bit Length  | Value               | Description                    | Present |
+==============================================+=============+=====================+================================+=========+
| SID                                          | 8           | 0x19                | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+---------------------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required          | Always  |
|             |                                |             |                     |                                |         |
|             |                                |             |                     | 1 = suppress positive response |         |
|             +--------------------------------+-------------+---------------------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x09                | reportSeverityInformationOfDTC | Always  |
+-------------+--------------------------------+-------------+---------------------+--------------------------------+---------+
| DTCMaskRecord                                | 24          | 0x000000 - 0xFFFFFF | DTC number                     | Always  |
+----------------------------------------------+-------------+---------------------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                                    | Bit Length  | Value               | Description                                  | Present                                  |
+=========================================================+=============+=====================+==============================================+==========================================+
| RSID                                                    | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| subFunction            | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                        |                                |             |                     |                                              |                                          |
|                        |                                |             |                     | 1 = suppress positive response               |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                        | reportType                     | 7 (b6 - b0) | 0x09                | reportSeverityInformationOfDTC               | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                               | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndSeverityRecord#1 | DTCSeverity                    | 8           | 0x00 - 0xFF         | Severity of DTC                              | If at least one DTC matches the criteria |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTCFunctionalUnit              | 8           | 0x00 - 0xFF         | Functional Unit of DTC                       |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndSeverityRecord#n | DTCSeverity                    | 8           | 0x00 - 0xFF         | Severity of DTC                              | If at least n DTCs matches the criteria  |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTCFunctionalUnit              | 8           | 0x00 - 0xFF         | Functional Unit of DTC                       |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0A:

reportSupportedDTC (0x0A)
`````````````````````````
This sub-function can be used by the client to request a list of all DTCs supported by the server.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x0A      | reportSupportedDTC             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                  |
+=================================================+=============+=====================+==============================================+==========================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                |                                |             |                     |                                              |                                          |
|                |                                |             |                     | 1 = suppress positive response               |                                          |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x0A                | reportSupportedDTCs                          | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0B:

reportFirstTestFailedDTC (0x0B)
```````````````````````````````
This sub-function can be used by the client to request the first DTC that failed a test since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x0B      | reportFirstTestFailedDTC       | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+

.. note:: The returned DTC is the first one detected with testFailed status bit (b0) set since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-----------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                          | Bit Length  | Value               | Description                                  | Present                                  |
+===============================================+=============+=====================+==============================================+==========================================+
| RSID                                          | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|  subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|              |                                |             |                     |                                              |                                          |
|              |                                |             |                     | 1 = suppress positive response               |                                          |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|              | reportType                     | 7 (b6 - b0) | 0x0B                | reportFirstTestFailedDTC                     | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                     | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|              | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0C:

reportFirstConfirmedDTC (0x0C)
``````````````````````````````
This sub-function can be used by the client to request the first confirmed DTC since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x0C      | reportFirstConfirmedDTC        | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+

.. note:: The returned DTC is the first one detected with confirmedDTC status bit (b3) set since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-----------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                          | Bit Length  | Value               | Description                                  | Present                                  |
+===============================================+=============+=====================+==============================================+==========================================+
| RSID                                          | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|  subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|              |                                |             |                     |                                              |                                          |
|              |                                |             |                     | 1 = suppress positive response               |                                          |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|              | reportType                     | 7 (b6 - b0) | 0x0C                | reportFirstConfirmedDTC                      | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                     | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|              | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0D:

reportMostRecentTestFailedDTC (0x0D)
````````````````````````````````````
This sub-function can be used by the client to request the most recent DTC that failed a test since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x0D      | reportMostRecentTestFailedDTC  | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+

.. note:: The returned DTC is the most recent one detected with testFailed status bit (b0) set since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-----------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                          | Bit Length  | Value               | Description                                  | Present                                  |
+===============================================+=============+=====================+==============================================+==========================================+
| RSID                                          | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|  subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|              |                                |             |                     |                                              |                                          |
|              |                                |             |                     | 1 = suppress positive response               |                                          |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|              | reportType                     | 7 (b6 - b0) | 0x0D                | reportMostRecentTestFailedDTC                | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                     | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|              | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0E:

reportMostRecentConfirmedDTC (0x0E)
```````````````````````````````````
This sub-function can be used by the client to request the most recent confirmed DTC since the last
:ref:`Clearing Diagnostic Information <knowledge-base-service-clear-diagnostic-information>`.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x0E      | reportMostRecentConfirmedDTC   | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+

.. note:: The returned DTC is the most recent one detected with confirmedDTC status bit (b3) set since the last
    :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>`.


Positive Response Format
''''''''''''''''''''''''
+-----------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                          | Bit Length  | Value               | Description                                  | Present                                  |
+===============================================+=============+=====================+==============================================+==========================================+
| RSID                                          | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|  subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|              |                                |             |                     |                                              |                                          |
|              |                                |             |                     | 1 = suppress positive response               |                                          |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|              | reportType                     | 7 (b6 - b0) | 0x0E                | reportMostRecentConfirmedDTC                 | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                     | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|              +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|              | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+--------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-0F:

reportMirrorMemoryDTCByStatusMask (0x0F)
````````````````````````````````````````
This sub-function can be used by the client to request all DTCs in the DTC mirror memory that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                             | Present |
+==============================================+=============+=============+=========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|             |                                |             |             |                                         |         |
|             |                                |             |             | 1 = suppress positive response          |         |
|             +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x0F        | reportMirrorMemoryDTCByStatusMask       | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                  |
+=================================================+=============+=====================+==============================================+==========================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                |                                |             |                     |                                              |                                          |
|                |                                |             |                     | 1 = suppress positive response               |                                          |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x0F                | reportMirrorMemoryDTCByStatusMask            | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-10:

reportMirrorMemoryDTCExtDataRecordByDTCNumber (0x10)
````````````````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*) for
a specific DTC (*DTCMaskRecord*) from the DTC mirror memory.

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| Name                                         | Bit Length  | Value               | Description                                              | Present |
+==============================================+=============+=====================+==========================================================+=========+
| SID                                          | 8           | 0x19                | ReadDTCInformation                                       | Always  |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                                    | Always  |
|             |                                |             |                     |                                                          |         |
|             |                                |             |                     | 1 = suppress positive response                           |         |
|             +--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x10                | reportMirrorMemoryDTCExtDataRecordByDTCNumber            | Always  |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| DTCMaskRecord                                | 24          | 0x000000 - 0xFFFFFF | DTC number                                               | Always  |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8           | 0x00 - 0xFF         | 0x00: reserved                                           | Always  |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0x01 - 0x8F: select vehicle manufacturer specific record |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0x90 - 0x9F: select regulated emissions OBD record       |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xA0 - 0xEF: select regulated record                     |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xF0 - 0xFD: reserved                                    |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xFE: all regulated emissions OBD records                |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xFF: all extended data records                          |         |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
| Name                                         | Bit Length  | Value               | Description                                   | Present                                                      |
+==============================================+=============+=====================+===============================================+==============================================================+
| RSID                                         | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19)  | Always                                                       |
+-------------+--------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                         | Always                                                       |
|             |                                |             |                     |                                               |                                                              |
|             |                                |             |                     | 1 = suppress positive response                |                                                              |
|             +--------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
|             | reportType                     | 7 (b6 - b0) | 0x10                | reportMirrorMemoryDTCExtDataRecordByDTCNumber | Always                                                       |
+-------------+--------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
| DTCRecord   | DTC                            | 24          | 0x000000 - 0xFFFFFF | Considered DTC                                | Always                                                       |
|             +--------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
|             | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                    | Always                                                       |
+-------------+--------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
| DTCExtDataRecordNumber#1                     | 8           | 0x00 - 0xFF         | Number of DTCExtDataRecord#1                  | If at least one DTCExtDataRecord is available for the DTC    |
+----------------------------------------------+-------------+---------------------+-----------------------------------------------+                                                              |
| DTCExtDataRecord#1                           | at least 8  |                     | Extended Data #1                              |                                                              |
+----------------------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
| ...                                                                                                                                                                                             |
+----------------------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+
| DTCExtDataRecordNumber#n                     | 8           | 0x00 - 0xFF         | Number of DTCExtDataRecord#n                  | If requested for multiple DTCSnapshot records                |
+----------------------------------------------+-------------+---------------------+-----------------------------------------------+                                                              |
| DTCExtDataRecord#n                           | at least 8  |                     | Extended Data #n                              | And at least n DTCSnapshot records are available for the DTC |
+----------------------------------------------+-------------+---------------------+-----------------------------------------------+--------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-11:

reportNumberOfMirrorMemoryDTCByStatusMask (0x11)
````````````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs in the DTC mirror memory that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-------------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                               | Present |
+==============================================+=============+=============+===========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                        | Always  |
+-------------+--------------------------------+-------------+-------------+-------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                     | Always  |
|             |                                |             |             |                                           |         |
|             |                                |             |             | 1 = suppress positive response            |         |
|             +--------------------------------+-------------+-------------+-------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x11        | reportNumberOfMirrorMemoryDTCByStatusMask | Always  |
+-------------+--------------------------------+-------------+-------------+-------------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching   | Always  |
+----------------------------------------------+-------------+-------------+-------------------------------------------+---------+

.. note:: The DTC mirror memory is an optional error memory that is not affected by
  :ref:`ClearDiagnosticInformation (0x14) <knowledge-base-service-clear-diagnostic-information>` service.


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| Name                                         | Bit Length  | Value           | Description                                  | Present |
+==============================================+=============+=================+==============================================+=========+
| RSID                                         | 8           | 0x59            | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1       | 0 = response required                        | Always  |
|             |                                |             |                 |                                              |         |
|             |                                |             |                 | 1 = suppress positive response               |         |
|             +--------------------------------+-------------+-----------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x11            | reportNumberOfMirrorMemoryDTCByStatusMask    | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8           | 0x00 - 0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8           | 0x00 - 0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCCount                                     | 16          | 0x0000 - 0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-12:

reportNumberOfEmissionsOBDDTCByStatusMask (0x12)
````````````````````````````````````````````````
This sub-function can be used by the client to request the number of emissions-related OBD DTCs that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-------------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                               | Present |
+==============================================+=============+=============+===========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                        | Always  |
+-------------+--------------------------------+-------------+-------------+-------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                     | Always  |
|             |                                |             |             |                                           |         |
|             |                                |             |             | 1 = suppress positive response            |         |
|             +--------------------------------+-------------+-------------+-------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x12        | reportNumberOfEmissionsOBDDTCByStatusMask | Always  |
+-------------+--------------------------------+-------------+-------------+-------------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching   | Always  |
+----------------------------------------------+-------------+-------------+-------------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| Name                                         | Bit Length  | Value           | Description                                  | Present |
+==============================================+=============+=================+==============================================+=========+
| RSID                                         | 8           | 0x59            | Positive Response: ReadDTCInformation (0x19) | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1       | 0 = response required                        | Always  |
|             |                                |             |                 |                                              |         |
|             |                                |             |                 | 1 = suppress positive response               |         |
|             +--------------------------------+-------------+-----------------+----------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x12            | reportNumberOfEmissionsOBDDTCByStatusMask    | Always  |
+-------------+--------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCStatusAvailabilityMask                    | 8           | 0x00 - 0xFF     | DTC Status bits supported by the ECU         | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCFormatIdentifier                          | 8           | 0x00 - 0xFF     | 0x00: SAE J2012-DA DTC Format 00             | Always  |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x01: ISO 14229-1 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x02: SAE J1939-73 DTC Format                |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x03: ISO 11992-4 DTC Format                 |         |
|                                              |             |                 |                                              |         |
|                                              |             |                 | 0x04: SAE J2012-DA DTC Format 04             |         |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+
| DTCCount                                     | 16          | 0x0000 - 0xFFFF | Number of DTCs that match criteria           | Always  |
+----------------------------------------------+-------------+-----------------+----------------------------------------------+---------+


.. _knowledge-base-service-read-dtc-information-13:

reportEmissionsOBDDTCByStatusMask (0x13)
````````````````````````````````````````
This sub-function can be used by the client to request a list of emissions-related OBD DTCs that match
a given status mask (*DTCStatusMask*).

.. warning:: Withdrawn in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                             | Present |
+==============================================+=============+=============+=========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|             |                                |             |             |                                         |         |
|             |                                |             |             | 1 = suppress positive response          |         |
|             +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x13        | reportEmissionsOBDDTCByStatusMask       | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                  |
+=================================================+=============+=====================+==============================================+==========================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                |                                |             |                     |                                              |                                          |
|                |                                |             |                     | 1 = suppress positive response               |                                          |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x13                | reportEmissionsOBDDTCByStatusMask            | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-14:

reportDTCFaultDetectionCounter (0x14)
`````````````````````````````````````
This sub-function can be used by the client to request fault detection counters for DTCs that have not been reported
or confirmed.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x14      | reportDTCFaultDetectionCounter | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                                              | Bit Length  | Value               | Description                                  | Present                                  |
+===================================================================+=============+=====================+==============================================+==========================================+
| RSID                                                              | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| subFunction                      | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                                  |                                |             |                     |                                              |                                          |
|                                  |                                |             |                     | 1 = suppress positive response               |                                          |
|                                  +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                                  | reportType                     | 7 (b6 - b0) | 0x14                | reportDTCFaultDetectionCounter               | Always                                   |
+----------------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                                         | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCFaultDetectionCounterRecord#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                                  +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                                  | DTCFaultDetectionCounter       | 8           | 0x01 - 0xFF         | Value of fault detection counter             |                                          |
+----------------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                                             |
+----------------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCFaultDetectionCounterRecord#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least n DTCs matches the criteria  |
|                                  +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                                  | DTCFaultDetectionCounter       | 8           | 0x01 - 0xFF         | Value of fault detection counter             |                                          |
+----------------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-15:

reportDTCWithPermanentStatus (0x15)
```````````````````````````````````
This sub-function can be used by the client to request a list of DTCs with permanent status (once reported,
never cleared by healing).


Request Format
''''''''''''''
+----------------------------------------------+-------------+-----------+--------------------------------+---------+
| Name                                         | Bit Length  | Value     | Description                    | Present |
+==============================================+=============+===========+================================+=========+
| SID                                          | 8           | 0x19      | ReadDTCInformation             | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1 | 0 = response required          | Always  |
|             |                                |             |           |                                |         |
|             |                                |             |           | 1 = suppress positive response |         |
|             +--------------------------------+-------------+-----------+--------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x15      | reportDTCWithPermanentStatus   | Always  |
+-------------+--------------------------------+-------------+-----------+--------------------------------+---------+

Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                  |
+=================================================+=============+=====================+==============================================+==========================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                |                                |             |                     |                                              |                                          |
|                |                                |             |                     | 1 = suppress positive response               |                                          |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x15                | reportDTCWithPermanentStatus                 | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-16:

reportDTCExtDataRecordByRecordNumber (0x16)
```````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*)
regardless of the DTC number.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+----------------------------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                                              | Present |
+==============================================+=============+=============+==========================================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                                       | Always  |
+-------------+--------------------------------+-------------+-------------+----------------------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                                    | Always  |
|             |                                |             |             |                                                          |         |
|             |                                |             |             | 1 = suppress positive response                           |         |
|             +--------------------------------+-------------+-------------+----------------------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x16        | reportDTCExtDataRecordByRecordNumber                     | Always  |
+-------------+--------------------------------+-------------+-------------+----------------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8           | 0x00 - 0xFF | 0x00: reserved                                           | Always  |
|                                              |             |             |                                                          |         |
|                                              |             |             | 0x01 - 0x8F: select vehicle manufacturer specific record |         |
|                                              |             |             |                                                          |         |
|                                              |             |             | 0x90 - 0x9F: select regulated emissions OBD record       |         |
|                                              |             |             |                                                          |         |
|                                              |             |             | 0xA0 - 0xEF: select regulated record                     |         |
|                                              |             |             |                                                          |         |
|                                              |             |             | 0xF0 - 0xFD: reserved                                    |         |
|                                              |             |             |                                                          |         |
|                                              |             |             | 0xFE: all regulated emissions OBD records                |         |
|                                              |             |             |                                                          |         |
|                                              |             |             | 0xFF: all extended data records                          |         |
+----------------------------------------------+-------------+-------------+----------------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
| Name                                                  | Bit Length  | Value               | Description                                  | Present                                       |
+=======================================================+=============+=====================+==============================================+===============================================+
| RSID                                                  | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
|      subFunction     | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                        |
|                      |                                |             |                     |                                              |                                               |
|                      |                                |             |                     | 1 = suppress positive response               |                                               |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
|                      | reportType                     | 7 (b6 - b0) | 0x16                | reportDTCExtDataRecordByRecordNumber         | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
| DTCExtDataRecordNumber                                | 8           | 0x00 - 0xEF         | Identification number of DTCExtDataRecord    | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
| DTCAndStatusRecord#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTCExtDataRecord is available |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+                                               |
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                   |                                               |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+                                               |
| DTCExtDataRecord#1                                    | at least 8  |                     | Extended Data #1                             |                                               |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
| ...                                                                                                                                                                                      |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+
| DTCAndStatusRecord#n | DTC                            | 24          | 0x00 - 0xFF         | Number of DTCExtDataRecord#n                 | If at least n DTCExtDataRecords are available |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+                                               |
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                   |                                               |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+                                               |
| DTCExtDataRecord#n                                    | at least 8  |                     | Extended Data #n                             |                                               |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+-----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-17:

reportUserDefMemoryDTCByStatusMask (0x17)
`````````````````````````````````````````
This sub-function can be used by the client to request the number of DTCs that match a given
status mask (*DTCStatusMask*) in a selected memory (*MemorySelection*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                             | Present |
+==============================================+=============+=============+=========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|             |                                |             |             |                                         |         |
|             |                                |             |             | 1 = suppress positive response          |         |
|             +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x17        | reportUserDefMemoryDTCByStatusMask      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| MemorySelection                              | 8           | 0x00 - 0xFF | Identifies DTC memory                   | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+

.. note:: :code:`MemorySelection` allows reading DTC related information from a specific DTC memory (e.g. one of
  the sub-systems).


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                  |
+=================================================+=============+=====================+==============================================+==========================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                |                                |             |                     |                                              |                                          |
|                |                                |             |                     | 1 = suppress positive response               |                                          |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x17                | reportUserDefMemoryDTCByStatusMask           | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| MemorySelection                                 | 8           | 0x00 - 0xFF         | Selected memory                              | Always                                   |
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC matches the criteria |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs matches the criteria  |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                          |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-18:

reportUserDefMemoryDTCSnapshotRecordByDTCNumber (0x18)
``````````````````````````````````````````````````````
This sub-function can be used by the client to request snapshot records (*DTCSnapshotRecordNumber*) for
a specific DTC (*DTCMaskRecord*) in a selected memory (*MemorySelection*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+---------------------+-------------------------------------------------+---------+
| Name                                         | Bit Length  | Value               | Description                                     | Present |
+==============================================+=============+=====================+=================================================+=========+
| SID                                          | 8           | 0x19                | ReadDTCInformation                              | Always  |
+-------------+--------------------------------+-------------+---------------------+-------------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                           | Always  |
|             |                                |             |                     |                                                 |         |
|             |                                |             |                     | 1 = suppress positive response                  |         |
|             +--------------------------------+-------------+---------------------+-------------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x18                | reportUserDefMemoryDTCSnapshotRecordByDTCNumber | Always  |
+-------------+--------------------------------+-------------+---------------------+-------------------------------------------------+---------+
| DTCMaskRecord                                | 24          | 0x000000 - 0xFFFFFF | DTC number                                      | Always  |
+----------------------------------------------+-------------+---------------------+-------------------------------------------------+---------+
| DTCSnapshotRecordNumber                      | 8           | 0x00 - 0xFF         | 0x00: reserved (legislated purposes)            | Always  |
|                                              |             |                     |                                                 |         |
|                                              |             |                     | 0x01 - 0xFE: select snapshot record             |         |
|                                              |             |                     |                                                 |         |
|                                              |             |                     | 0xFF: all snapshot records                      |         |
+----------------------------------------------+-------------+---------------------+-------------------------------------------------+---------+
| MemorySelection                              | 8           | 0x00 - 0xFF         | Identifies DTC memory                           | Always  |
+----------------------------------------------+-------------+---------------------+-------------------------------------------------+---------+

.. note:: :code:`MemorySelection` allows reading DTC related information from a specific DTC memory (e.g. one of
  the sub-systems).


Positive Response Format
''''''''''''''''''''''''
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| Name                                                 | Bit Length  | Value               | Description                                              | Present                                                      |
+======================================================+=============+=====================+==========================================================+==============================================================+
| RSID                                                 | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19)             | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
|     subFunction     | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                                    | Always                                                       |
|                     |                                |             |                     |                                                          |                                                              |
|                     |                                |             |                     | 1 = suppress positive response                           |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
|                     | reportType                     | 7 (b6 - b0) | 0x18                | reportUserDefMemoryDTCSnapshotRecordByDTCNumber          | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| MemorySelection                                      | 8           | 0x00 - 0xFF         | Selected memory                                          | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| DTCRecord           | DTC                            | 24          | 0x000000 - 0xFFFFFF | Selected DTC                                             | Always                                                       |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
|                     | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                               | Always                                                       |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| DTCSnapshotRecordNumber#1                            | 8           | 0x00 - 0xFF         | Number of DTCSnapshot#1                                  | If at least one DTCSnapshot record is available for the DTC  |
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecordNumberOfIdentifiers#1               | 8           | 0x00 - 0xFF         | Number of Identifiers stored by DTCSnapshot#1 (equals m) |                                                              |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecord#1 | dataIdentifier#1               | 16          | 0x0000 - 0xFFFF     | DID#1 that is part of DTCSnapshot#1                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#1           |             |                     | Data stored under DID#1                                  |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | ...                                                                                                                           |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifier#m               | 16          | 0x0000 - 0xFFFF     | DID#m that is part of DTCSnapshot#1                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#m           |             |                     | Data stored under DID#m                                  |                                                              |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| ...                                                                                                                                                                                                                |
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+
| DTCSnapshotRecordNumber#n                            | 24          | 0x000000 - 0xFFFFFF | DTC for which DTCSnapshot record #n was reported         | If requested for multiple DTCSnapshot records                |
+------------------------------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecordNumberOfIdentifiers#n               | 8           | 0x00 - 0xFF         | Number of Identifiers stored by DTCSnapshot#1 (equals k) | And at least n DTCSnapshot records are available for the DTC |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
| DTCSnapshotRecord#n | dataIdentifier#1               | 16          | 0x0000 - 0xFFFF     | DID#1 that is part of DTCSnapshot#n                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#1           | 8 or more   |                     | Data stored under DID#1                                  |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | ...                                                                                                                           |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifier#k               | 16          | 0x0000 - 0xFFFF     | DID#k that is part of DTCSnapshot#n                      |                                                              |
|                     +--------------------------------+-------------+---------------------+----------------------------------------------------------+                                                              |
|                     | dataIdentifierData#k           | 8 or more   |                     | Data stored under DID#k                                  |                                                              |
+---------------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+--------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-19:

reportUserDefMemoryDTCExtDataRecordByDTCNumber (0x19)
`````````````````````````````````````````````````````
This sub-function can be used by the client to request extended data records (*DTCExtDataRecordNumber*) for
a specific DTC (*DTCMaskRecord*) in a selected memory (*MemorySelection*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| Name                                         | Bit Length  | Value               | Description                                              | Present |
+==============================================+=============+=====================+==========================================================+=========+
| SID                                          | 8           | 0x19                | ReadDTCInformation                                       | Always  |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                                    | Always  |
|             |                                |             |                     |                                                          |         |
|             |                                |             |                     | 1 = suppress positive response                           |         |
|             +--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x19                | reportUserDefMemoryDTCExtDataRecordByDTCNumber           | Always  |
+-------------+--------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| DTCMaskRecord                                | 24          | 0x000000 - 0xFFFFFF | DTC number                                               | Always  |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| DTCExtDataRecordNumber                       | 8           | 0x00 - 0xFF         | 0x00: reserved                                           | Always  |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0x01 - 0x8F: select vehicle manufacturer specific record |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0x90 - 0x9F: select regulated emissions OBD record       |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xA0 - 0xEF: select regulated record                     |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xF0 - 0xFD: reserved                                    |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xFE: all regulated emissions OBD records                |         |
|                                              |             |                     |                                                          |         |
|                                              |             |                     | 0xFF: all extended data records                          |         |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+
| MemorySelection                              | 8           | 0x00 - 0xFF         | Specifies DTC memory                                     | Always  |
+----------------------------------------------+-------------+---------------------+----------------------------------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* (0x01–0xEF) selects a single extended data record.
  0xFE requests all regulated emissions OBD records.
  0xFF requests all extended data records for the DTC.

.. note:: :code:`MemorySelection` allows reading DTC related information from a specific DTC memory (e.g. one of
  the sub-systems).


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| Name                                                  | Bit Length  | Value               | Description                                    | Present                                       |
+=======================================================+=============+=====================+================================================+===============================================+
| RSID                                                  | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19)   | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
|      subFunction     | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                          | Always                                        |
|                      |                                |             |                     |                                                |                                               |
|                      |                                |             |                     | 1 = suppress positive response                 |                                               |
|                      +--------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
|                      | reportType                     | 7 (b6 - b0) | 0x19                | reportUserDefMemoryDTCExtDataRecordByDTCNumber | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| MemorySelection                                       | 8           | 0x00 - 0xEF         | Selected memory                                | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| DTCAndStatusRecord#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                            | Always                                        |
|                      +--------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | DTC status                                     | Always                                        |
+----------------------+--------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| DTCExtDataRecordNumber#1                              | 8           | 0x00 - 0xFE         |                                                | If at least one DTCExtDataRecord is available |
+-------------------------------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| DTCExtDataRecord#1                                    | at least 8  |                     | Extended Data #1                               | If at least one DTCExtDataRecord is available |
+-------------------------------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| ...                                                                                                                                                                                        |
+-------------------------------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+
| DTCExtDataRecord#n                                    | at least 8  |                     | Extended Data #n                               | If at least n DTCExtDataRecords are available |
+-------------------------------------------------------+-------------+---------------------+------------------------------------------------+-----------------------------------------------+


.. _knowledge-base-service-read-dtc-information-1A:

reportSupportedDTCExtDataRecord (0x1A)
``````````````````````````````````````
This sub-function can be used by the client to request the list of DTCs that support a given
extended data record number (*DTCExtDataRecordNumber*).

.. warning:: Introduced in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+---------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                     | Present |
+==============================================+=============+=============+=================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation              | Always  |
+-------------+--------------------------------+-------------+-------------+---------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required           | Always  |
|             |                                |             |             |                                 |         |
|             |                                |             |             | 1 = suppress positive response  |         |
|             +--------------------------------+-------------+-------------+---------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x1A        | reportSupportedDTCExtDataRecord | Always  |
+-------------+--------------------------------+-------------+-------------+---------------------------------+---------+
| DTCExtDataRecordNumber                       | 8           | 0x00 - 0xFF | Extended data record number     | Always  |
+----------------------------------------------+-------------+-------------+---------------------------------+---------+

.. note:: *DTCExtDataRecordNumber* shall be within 0x01–0xEF range.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
| Name                                            | Bit Length  | Value               | Description                                  | Present                                                    |
+=================================================+=============+=====================+==============================================+============================================================+
| RSID                                            | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                                     |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
|   subFunction  | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                                     |
|                |                                |             |                     |                                              |                                                            |
|                |                                |             |                     | 1 = suppress positive response               |                                                            |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
|                | reportType                     | 7 (b6 - b0) | 0x1A                | reportSupportedDTCExtDataRecord              | Always                                                     |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
| DTCStatusAvailabilityMask                       | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                                     |
+-------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
| DTCExtDataRecordNumber                          | 8           | 0x01 - 0xFD         | Identification number of DTCExtDataRecord    | If at least one DTC supports the selected                  |
|                                                 |             |                     |                                              | DTCExtDataRecord                                           |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
| DTCAndStatus#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#1                                        | If at least one DTC supports the selected DTCExtDataRecord |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#1                              |                                                            |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
| ...                                                                                                                                                                                             |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+
| DTCAndStatus#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC#n                                        | If at least n DTCs support the selected                    |
|                +--------------------------------+-------------+---------------------+----------------------------------------------+ DTCExtDataRecord                                           |
|                | DTC Status                     | 8           | 0x00 - 0xFF         | Status of DTC#n                              |                                                            |
+----------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------------------------+


.. _knowledge-base-service-read-dtc-information-42:

reportWWHOBDDTCByMaskRecord (0x42)
``````````````````````````````````
This sub-function can be used by the client to request WWH-OBD DTCs and their associated status and
severity information, filtered by a status mask (*DTCStatusMask*) and a severity mask (*DTCSeverityMaskRecord*).


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                             | Present |
+==============================================+=============+=============+=========================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                      | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                   | Always  |
|             |                                |             |             |                                         |         |
|             |                                |             |             | 1 = suppress positive response          |         |
|             +--------------------------------+-------------+-------------+-----------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x42        | reportWWHOBDDTCByMaskRecord             | Always  |
+-------------+--------------------------------+-------------+-------------+-----------------------------------------+---------+
| FunctionalGroupIdentifier                    | 8           | 0x00 - 0xFF | 0x00 - 0x32: reserved                   | Always  |
|                                              |             |             |                                         |         |
|                                              |             |             | 0x33: emissions-system group            |         |
|                                              |             |             |                                         |         |
|                                              |             |             | 0x34 - 0xCF: reserved                   |         |
|                                              |             |             |                                         |         |
|                                              |             |             | 0xD0: safety-system group               |         |
|                                              |             |             |                                         |         |
|                                              |             |             | 0xD1 - 0xDF: legislative system group   |         |
|                                              |             |             |                                         |         |
|                                              |             |             | 0xE0 - 0xFD: reserved                   |         |
|                                              |             |             |                                         |         |
|                                              |             |             | 0xFE: VOBD system                       |         |
|                                              |             |             |                                         |         |
|                                              |             |             | 0xFF: reserved                          |         |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCSeverityMaskRecord                        | 8           | 0x00 - 0xFF | Severity mask to use for DTC matching   | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+
| DTCStatusMask                                | 8           | 0x00 - 0xFF | DTC status mask to use for DTC matching | Always  |
+----------------------------------------------+-------------+-------------+-----------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+---------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                                    | Bit Length  | Value               | Description                                  | Present                                  |
+=========================================================+=============+=====================+==============================================+==========================================+
| RSID                                                    | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| subFunction            | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                        |                                |             |                     |                                              |                                          |
|                        |                                |             |                     | 1 = suppress positive response               |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                        | reportType                     | 7 (b6 - b0) | 0x42                | reportWWHOBDDTCByMaskRecord                  | Always                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| FunctionalGroupIdentifier                               | 8           | 0x00 - 0xFF         | 0x00 - 0x32: reserved                        | Always                                   |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0x33: emissions-system group                 |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0x34 - 0xCF: reserved                        |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0xD0: safety-system group                    |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0xD1 - 0xDF: legislative system group        |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0xE0 - 0xFD: reserved                        |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0xFE: VOBD system                            |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0xFF: reserved                               |                                          |
+---------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                               | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+---------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCSeverityAvailabilityMask                             | 8           | 0x00 - 0xFF         | DTC Severity bits supported by the ECU       | Always                                   |
+---------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCFormatIdentifier                                     | 8           | 0x00 - 0xFF         | 0x00: SAE J2012-DA DTC Format 00             | Always                                   |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0x01: ISO 14229-1 DTC Format                 |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0x02: SAE J1939-73 DTC Format                |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0x03: ISO 11992-4 DTC Format                 |                                          |
|                                                         |             |                     |                                              |                                          |
|                                                         |             |                     | 0x04: SAE J2012-DA DTC Format 04             |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndSeverityRecord#1 | DTCSeverity                    | 8           | 0x00 - 0xFF         | Severity of DTC                              | If at least one DTC matches the criteria |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                        | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                        | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                                   |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndSeverityRecord#n | DTCSeverity                    | 8           | 0x00 - 0xFF         | Severity of DTC                              | If at least n DTCs matches the criteria  |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          |                                          |
|                        +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                        | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+------------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-55:

reportWWHOBDDTCWithPermanentStatus (0x55)
`````````````````````````````````````````
This sub-function can be used by the client to request WWH-OBD DTCs with permanent status.


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+---------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                           | Present |
+==============================================+=============+=============+=======================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                    | Always  |
+-------------+--------------------------------+-------------+-------------+---------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                 | Always  |
|             |                                |             |             |                                       |         |
|             |                                |             |             | 1 = suppress positive response        |         |
|             +--------------------------------+-------------+-------------+---------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x55        | reportWWHOBDDTCWithPermanentStatus    | Always  |
+-------------+--------------------------------+-------------+-------------+---------------------------------------+---------+
| FunctionalGroupIdentifier                    | 8           | 0x00 - 0xFF | 0x00 - 0x32: reserved                 | Always  |
|                                              |             |             |                                       |         |
|                                              |             |             | 0x33: emissions-system group          |         |
|                                              |             |             |                                       |         |
|                                              |             |             | 0x34 - 0xCF: reserved                 |         |
|                                              |             |             |                                       |         |
|                                              |             |             | 0xD0: safety-system group             |         |
|                                              |             |             |                                       |         |
|                                              |             |             | 0xD1 - 0xDF: legislative system group |         |
|                                              |             |             |                                       |         |
|                                              |             |             | 0xE0 - 0xFD: reserved                 |         |
|                                              |             |             |                                       |         |
|                                              |             |             | 0xFE: VOBD system                     |         |
|                                              |             |             |                                       |         |
|                                              |             |             | 0xFF: reserved                        |         |
+----------------------------------------------+-------------+-------------+---------------------------------------+---------+


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                                  | Bit Length  | Value               | Description                                  | Present                                  |
+=======================================================+=============+=====================+==============================================+==========================================+
| RSID                                                  | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| subFunction          | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                      |                                |             |                     |                                              |                                          |
|                      |                                |             |                     | 1 = suppress positive response               |                                          |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                      | reportType                     | 7 (b6 - b0) | 0x55                | reportWWHOBDDTCWithPermanentStatus           | Always                                   |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| FunctionalGroupIdentifier                             | 8           | 0x00 - 0xFF         | 0x00 - 0x32: reserved                        | Always                                   |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x33: emissions-system group                 |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x34 - 0xCF: reserved                        |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xD0: safety-system group                    |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xD1 - 0xDF: legislative system group        |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xE0 - 0xFD: reserved                        |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xFE: VOBD system                            |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xFF: reserved                               |                                          |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                             | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCFormatIdentifier                                   | 8           | 0x00 - 0xFF         | 0x00: SAE J2012-DA DTC Format 00             | Always                                   |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x01: ISO 14229-1 DTC Format                 |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x02: SAE J1939-73 DTC Format                |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x03: ISO 11992-4 DTC Format                 |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x04: SAE J2012-DA DTC Format 04             |                                          |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatusRecord#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                                 |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatusRecord#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least n DTCs matches the criteria  |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


.. _knowledge-base-service-read-dtc-information-56:

reportDTCInformationByDTCReadinessGroupIdentifier (0x56)
````````````````````````````````````````````````````````
This sub-function can be used by the client to request OBD DTCs that belong to a given
readiness group (*DTCReadinessGroupIdentifier*).

.. warning:: Introduced in ISO 14229-1:2020


Request Format
''''''''''''''
+----------------------------------------------+-------------+-------------+---------------------------------------------------+---------+
| Name                                         | Bit Length  | Value       | Description                                       | Present |
+==============================================+=============+=============+===================================================+=========+
| SID                                          | 8           | 0x19        | ReadDTCInformation                                | Always  |
+-------------+--------------------------------+-------------+-------------+---------------------------------------------------+---------+
| subFunction | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1   | 0 = response required                             | Always  |
|             |                                |             |             |                                                   |         |
|             |                                |             |             | 1 = suppress positive response                    |         |
|             +--------------------------------+-------------+-------------+---------------------------------------------------+---------+
|             | reportType                     | 7 (b6 - b0) | 0x56        | reportDTCInformationByDTCReadinessGroupIdentifier | Always  |
+-------------+--------------------------------+-------------+-------------+---------------------------------------------------+---------+
| FunctionalGroupIdentifier                    | 8           | 0x00 - 0xFF | 0x00 - 0x32: reserved                             | Always  |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0x33: emissions-system group                      |         |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0x34 - 0xCF: reserved                             |         |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0xD0: safety-system group                         |         |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0xD1 - 0xDF: legislative system group             |         |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0xE0 - 0xFD: reserved                             |         |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0xFE: VOBD system                                 |         |
|                                              |             |             |                                                   |         |
|                                              |             |             | 0xFF: reserved                                    |         |
+----------------------------------------------+-------------+-------------+---------------------------------------------------+---------+
| DTCReadinessGroupIdentifier                  | 8           | 0x00 - 0xFF | Specifies DTC readiness group                     | Always  |
+----------------------------------------------+-------------+-------------+---------------------------------------------------+---------+

.. note:: `SAE J1979-DA <https://www.sae.org/standards/j1979da_202203-j1979-da-digital-annex-e-e-diagnostic-test-modes>`_
  defines values mapping for *DTCReadinessGroupIdentifier* parameter.


Positive Response Format
''''''''''''''''''''''''
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| Name                                                  | Bit Length  | Value               | Description                                  | Present                                  |
+=======================================================+=============+=====================+==============================================+==========================================+
| RSID                                                  | 8           | 0x59                | Positive Response: ReadDTCInformation (0x19) | Always                                   |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| subFunction          | suppressPosRspMsgIndicationBit | 1 (b7)      | 0x0 - 0x1           | 0 = response required                        | Always                                   |
|                      |                                |             |                     |                                              |                                          |
|                      |                                |             |                     | 1 = suppress positive response               |                                          |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
|                      | reportType                     | 7 (b6 - b0) | 0x56                | reportDTCByReadinessGroupIdentifier          | Always                                   |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| FunctionalGroupIdentifier                             | 8           | 0x00 - 0xFF         | 0x00 - 0x32: reserved                        | Always                                   |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x33: emissions-system group                 |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x34 - 0xCF: reserved                        |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xD0: safety-system group                    |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xD1 - 0xDF: legislative system group        |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xE0 - 0xFD: reserved                        |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xFE: VOBD system                            |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0xFF: reserved                               |                                          |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCStatusAvailabilityMask                             | 8           | 0x00 - 0xFF         | DTC Status bits supported by the ECU         | Always                                   |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCFormatIdentifier                                   | 8           | 0x00 - 0xFF         | 0x00: SAE J2012-DA DTC Format 00             | Always                                   |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x01: ISO 14229-1 DTC Format                 |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x02: SAE J1939-73 DTC Format                |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x03: ISO 11992-4 DTC Format                 |                                          |
|                                                       |             |                     |                                              |                                          |
|                                                       |             |                     | 0x04: SAE J2012-DA DTC Format 04             |                                          |
+-------------------------------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCReadinessGroupIdentifier                           | 8           | 0x00 - 0xFF         | Selected readiness group                     | Always                                   |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatusRecord#1 | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least one DTC matches the criteria |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| ...                                                                                                                                                                                 |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+
| DTCAndStatusRecord#n | DTC                            | 24          | 0x000000 - 0xFFFFFF | DTC                                          | If at least n DTCs matches the criteria  |
|                      +--------------------------------+-------------+---------------------+----------------------------------------------+                                          |
|                      | statusOfDTC                    | 8           | 0x00 - 0xFF         | Status of DTC                                |                                          |
+----------------------+--------------------------------+-------------+---------------------+----------------------------------------------+------------------------------------------+


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

.. _knowledge-base-dtc:

Diagnostic Trouble Code (DTC)
=============================
A Diagnostic Trouble Code (DTC) is a standardized identifier representing a specific fault detected by a vehicle’s
electronic control system.
Each DTC corresponds to one distinct diagnostic condition (for example, *“Battery voltage too low”*).

.. seealso::
  - https://www.dtclookup.com/
  - https://obd2pros.com/dtc-codes/
  - https://www.freeautomechanic.com/diagnostictroblecodes.html


DTC Formats
-----------
Historically, DTCs were 2 bytes (16 bits) long.
Modern implementations defined by ISO 14229 (UDS) and SAE J2012 use 3 bytes (24 bits), which is now the standard format
used by all OEMs.

+-------------------+-------------------+
| DTC in UDS Format | DTC in OBD format |
+===================+===================+
| 0x000000          | P0000-00          |
+-------------------+-------------------+
| 0x56789A          | C1678-9A          |
+-------------------+-------------------+
| 0xA5B6C7          | B25B6-C7          |
+-------------------+-------------------+
| 0xFFFFFF          | U3FFF-FF          |
+-------------------+-------------------+


.. _knowledge-base-dtc-obd-format:

OBD
```
The OBD-II format for DTCs is defined in
`SAE J2012 <https://www.sae.org/standards/j2012_202509-diagnostic-trouble-code-definitions>`_.

Example DTC values:

- P0123-45
- U0100-00
- B3FED-CB
- C10F0-FF

In consists of eight characters:

- one letter that identifier the system

  - `P` - Powertrain (bit pattern: 00)
  - `C` - Chassis (bit pattern: 01)
  - `B` - Body (bit pattern: 10)
  - `U` - Network/Communication (bit pattern: 11)

- one numeric digit which informs whether DTC is defined by a standard or vehicle manufacturer

  `0-3` (2 bits)

- one hexadecimal digit which indicates sub-system

  `0-F` (4 bits)

- two hexadecimal digits which identifies the fault

  `00-FF` (8 bits)

- dash: `-`

- two hexadecimal digits which identifies the symptom of the fault

  `00-FF` (8 bits)


.. _knowledge-base-dtc-uds-format:

UDS
```
The UDS representation (defined by ISO 14229-1) encodes the DTC as a 24-bit hexadecimal number.

Example DTC values:

- 0x012345
- 0xDCBA98
- 0xFFFFFF



.. _knowledge-base-dtc-status:

DTC Status
----------
Each DTC has an 8-bit status field that describes the current state of the associated fault and its history.

- *testFailed* (b[0] - LSB) - indicates the result of most recently performed diagnostic test for this DTC

  - 0 - the most recent test passed (no failure detected)
  - 1 - the most recent test failed (a failure detected)

- *testFailedThisOperationCycle* (b[1]) - indicates whether the DTC has reported *testFailed* at any time during
  the current cycle

  - 0 - no failure detected during the current operation cycle
  - 1 - at least one test failed during the current operation cycle

- *pendingDTC* (b[2]) - indicates whether DTC has reported *testFailed* at any time during the current
  or the last completed operation cycle

  - 0 - no check failed during the current or the last completed operation cycle
  - 1 - at least one test failed during the current or the last completed operation cycle

- *confirmedDTC* (b[3]) - indicates whether DTC is desired to be stored in a long-term memory

  - 0 - DTC is not confirmed

    - on :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` call
    - when aging threshold for DTC self-healing procedure is reached

  - 1 - DTC is confirmed

    - set whenever *testFailed*=1

- *testNotCompletedSinceLastClear* (b[4]) - indicates whether the diagnostic test has been completed since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` call

  - 0 - at least one test (either passed or failed) was performed since the last clear
  - 1 - no test was performed since the last clear

- *testFailedSinceLastClear* (b[5]) - indicates whether at least one test failed since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` call

  - 0 - no test failed since the last clear
  - 1 - at least one test failed since the last clear

- *testNotCompletedThisOperationCycle* (b[6]) - indicates whether DTC test was performed this operation cycle

  - 0 - at least one test (either passed or failed) was performed this operation cycle
  - 1 - no test was performed during the current operation cycle

- *warningIndicatorRequested* (b[7] - MSB) - indicates whether a warning indicator associated with DTC shall be
  activated

  - 0 - warning indicator not requested
  - 1 - warning indicator requested

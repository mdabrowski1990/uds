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


DTC Presentation Formats
------------------------
Historically, DTCs were 2 bytes (16 bits) long.
Modern diagnostic protocols defined by ISO 14229 (UDS) and SAE J2012 use 3-byte (24-bit) DTCs,
which are now the industry standard.

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
- U2100-00
- B3FED-CB
- C10F0-FF

It consists of eight characters:

- **one letter** that identifies the system

  - `P` - Powertrain (bit pattern: 00)
  - `C` - Chassis (bit pattern: 01)
  - `B` - Body (bit pattern: 10)
  - `U` - Network/Communication (bit pattern: 11)

- **one numeric digit** which informs whether DTC is defined by a standard or vehicle manufacturer

  `0-3` (2 bits)

- **one hexadecimal digit** which indicates sub-system

  `0-F` (4 bits)

- **two hexadecimal digits** which identify the fault

  `00-FF` (8 bits)

- **dash**

  `-`

- **two hexadecimal digits** which identify the symptom of the fault

  `00-FF` (8 bits)


.. _knowledge-base-dtc-uds-format:

UDS
```
The UDS representation (defined by ISO 14229-1) encodes each DTC as a 24-bit value,
typically represented as a six-digit hexadecimal number.

Example DTC values:

- 0x012345
- 0xDCBA98
- 0xFFFFFF


.. _knowledge-base-dtc-status:

DTC Status
----------
Each DTC has an 8-bit status field that describes the current state of the associated fault and its history.

- **testFailed** (b[0] - LSB) - indicates the result of most recently performed diagnostic test for this DTC

  - 0 - the most recent test passed (no failure detected)
  - 1 - the most recent test failed (a failure detected)

- **testFailedThisOperationCycle** (b[1]) - indicates whether the DTC has reported *testFailed* at any time during
  the current cycle

  - 0 - no failure detected during the current operation cycle
  - 1 - at least one test failed during the current operation cycle

- **pendingDTC** (b[2]) - indicates whether DTC has reported *testFailed* at any time during the current
  or the previous operation cycle

  - 0 - no check failed during the current or the last completed operation cycle
  - 1 - at least one test failed during the current or the last completed operation cycle

- **confirmedDTC** (b[3]) - indicates whether DTC is desired to be stored in a long-term memory

  - 0 - DTC is not confirmed

    - cleared on :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` call
    - cleared when DTC Aging Counter threshold for *self-healing* is reached

  - 1 - DTC is confirmed

    - set whenever *testFailed* is set

- **testNotCompletedSinceLastClear** (b[4]) - indicates whether the DTC test has been completed since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` call

  - 0 - at least one test (either passed or failed) was performed since the last clear
  - 1 - no test was performed since the last clear

- **testFailedSinceLastClear** (b[5]) - indicates whether at least one test failed since the last
  :ref:`ClearDiagnosticInformation <knowledge-base-service-clear-diagnostic-information>` call

  - 0 - no test failed since the last clear
  - 1 - at least one test failed since the last clear

- **testNotCompletedThisOperationCycle** (b[6]) - indicates whether DTC test was performed this operation cycle

  - 0 - at least one test (either passed or failed) was performed this operation cycle
  - 1 - no test was performed during the current operation cycle

- **warningIndicatorRequested** (b[7] - MSB) - indicates whether a warning indicator associated with DTC shall be
  activated

  - 0 - warning indicator not requested
  - 1 - warning indicator requested


.. _knowledge-base-dtc-severity:

DTC Severity
------------
Each DTC may have an associated DTC Severity value, which encodes both its regulatory classification and its severity.
This value is defined by the ECU software or calibration and does not change during vehicle operation.
DTC Severity contains two pieces of information - *GTR DTC class* (bits 0-4) and *severity* (bits 5-7).

- **DTCClass_0** (b[0] - LSB) - indicates whether DTC is unclassified

  - 0 - DTC is classified
  - 1 - DTC is unclassified

- **DTCClass_1** (b[1]) - indicates whether the DTC matches the GTR module B Class A definition

  - 0 - DTC is not Class 1 (GTR module B Class A)
  - 1 - DTC is Class 1 (GTR module B Class A)

- **DTCClass_2** (b[2]) - indicates whether the DTC matches the GTR module B Class B1 definition

  - 0 - DTC is not Class 2 (GTR module B Class B1)
  - 1 - DTC is Class 2 (GTR module B Class B1)

- **DTCClass_3** (b[3]) - indicates whether the DTC matches the GTR module B Class B2 definition

  - 0 - DTC is not Class 3 (GTR module B Class B2)
  - 1 - DTC is Class 3 (GTR module B Class B2)

- **DTCClass_4** (b[4]) - indicates whether the DTC matches the GTR module B Class C definition

  - 0 - DTC is not Class 4 (GTR module B Class C)
  - 1 - DTC is Class 4 (GTR module B Class C)

- **maintenanceOnly** (b[5]) - indicates whether the failure is maintenance only

  - 0 - no maintenanceOnly severity
  - 1 - maintenanceOnly severity

- **checkAtNextHalt** (b[6]) - indicates whether the failure has to be checked at the next halt

  - 0 - no checkAtNextHalt severity
  - 1 - checkAtNextHalt severity

- **checkImmediately** (b[7] - MSB) - indicates whether the failure has to be checked immediately

  - 0 - no checkImmediately severity
  - 1 - checkImmediately severity

.. note:: A valid DTC Severity value shall have exactly two bits set:

  - one GTR class bit (bits 0–4)
  - one severity bit (bits 5–7)


.. _knowledge-base-dtc-fault-detection-counter:

DTC Fault Detection Counter
---------------------------
Each DTC has assigned 8-bit (with a sign) value named DTC Fault Detection Counter.
Each ECU performs self-tests intended to detect whether the failure conditions for its DTCs are currently present.

If a self-test fails, the counter is increased by an implementation-specific amount.
If a self-test passes, the counter is decreased by an implementation-specific amount.

When the counter reaches its maximum value (127), the **testFailed** bit shall be set to 1.
When the counter reaches its minimum value (-128), the **testFailed** bit shall be set to 0.
On start of each operation cycle, DTC Fault Detection Counter is reset to 0.


.. _knowledge-base-dtc-aging-counter:

DTC Aging Counter
-----------------
For each DTC, an Aging Counter is stored. It records the number of vehicle operation cycles since the last occurrence
of the fault.
When the Aging Counter reaches Aging Counter Threshold (usually after 40 operation cycles),
the DTC is considered aged and shall be cleared from memory.
This procedure is often referred to as *self-healing*.


.. _knowledge-base-dtc-functional-unit:

DTC Functional Unit
-------------------
DTC Functional Unit identifies the system or component reporting the fault.
The values meaning is defined by the vehicle manufacturer.


.. _knowledge-base-dtc-functional-group-identifier:

Functional Group Identifier
---------------------------
Functional Group Identifier groups vehicle's systems by their functionalities.

+-----------+--------------------------+
| Value     | Description              |
+===========+==========================+
| 0x00-0x32 | Reserved                 |
+-----------+--------------------------+
| 0x33      | Emissions-system group   |
+-----------+--------------------------+
| 0x34-0xCF | Reserved                 |
+-----------+--------------------------+
| 0xD0      | Safety-system group      |
+-----------+--------------------------+
| 0xD1-0xDF | Legislative system group |
+-----------+--------------------------+
| 0xE0-0xFD | Reserved                 |
+-----------+--------------------------+
| 0xFE      | VOBD system              |
+-----------+--------------------------+
| 0xFF      | Reserved                 |
+-----------+--------------------------+


.. _knowledge-base-dtc-readiness-group:

DTC Readiness Group
-------------------
DTC Readiness Group provides a finer categorization of diagnostic functions within a given
`Functional Group Identifier`_.
The meaning of each readiness group depends entirely on the use-case standard associated with the
`Functional Group Identifier`_.

.. seealso::
  SAE J1979-DA <https://www.sae.org/standards/j1979da_202203-j1979-da-digital-annex-e-e-diagnostic-test-modes>`_

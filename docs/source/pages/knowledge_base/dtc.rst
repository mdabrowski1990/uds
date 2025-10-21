.. _knowledge-base-dtc:

DTC
===
A Diagnostic Trouble Code (DTC) is a standardized identifier representing a specific fault detected by a vehicle’s
electronic control system.
Each DTC corresponds to one distinct diagnostic condition (for example, *“Battery voltage too low”*).

.. seealso::
  https://www.dtclookup.com/
  https://obd2pros.com/dtc-codes/
  https://www.freeautomechanic.com/diagnostictroblecodes.html


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
- one letter (system):
  - `P` - Powertrain (bit pattern: 00)
  - `C` - Chassis (bit pattern: 01)
  - `B` - Body (bit pattern: 10)
  - `U` - Network/Communication (bit pattern: 11)
- one numeric digit: `0-3`
- three hexadecimal digits: `0-F`
- dash: `-`
- two hexadecimal digits: `0-F`


.. _knowledge-base-dtc-uds-format:

UDS
```
The UDS representation (defined by ISO 14229-1) encodes the DTC as a 24-bit hexadecimal number.

Example DTC values:
- 0x012345
- 0xDCBA98
- 0xFFFFFF

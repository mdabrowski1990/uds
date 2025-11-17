.. _knowledge-base-rid:

Routine Identifier (RID)
========================
A Routine Identifier (RID) is a 16-bit identifier used by a diagnostic client to select a specific routine
implemented by the server (ECU). Routines represent executable functions that can be started, stopped, and monitored
for their results or status.

The following UDS services operate on RIDs:

- :ref:`RoutineControl (0x31) <knowledge-base-service-routine-control>`


Defined by ISO 14229-1
----------------------
The same definitions are present in both ISO 14229-1:2020 and ISO 14229-1:2013.

- **0x0000-0x00FF** *[ISOSAEReserved]*:

  Reserved by ISO/SAE for future standardisation.

- **0x0100-0x01FF** *[TachographTestIds]*:

  Assigned for Tachograph-related routines as defined in other legislation/standards.

- **0x0200-0xDFFF** *[VehicleManufacturerSpecific]*:

  Defined by the OEM for vehicle/system specific use.

- **0xE000-0xE1FF** *[OBDTestIds]*:

  Reserved for OBD/EOBD related routines.

- **0xE200** *[Execute SPL]*:

  Execute the previously downloaded Scrapping Program Loader (SPL) and convert it into an executable form.
  See ISO 26021 for detailed definition.

- **0xE201** *[DeployLoopRoutineID]*:

  Perform deployment loop routines for pyrotechnic devices during vehicle scrapping.
  Defined in ISO 26021.

- **0xE202-0xE2FF** *[SafetySystemRoutineIDs]*:

  Routines related to safety system deactivation/deployment as specified in ISO 26021 or OEM definitions.

- **0xE300-0xEFFF** *[ISOSAEReserved]*:

  Reserved by ISO/SAE for future standardisation.

- **0xF000-0xFEFF** *[SystemSupplierSpecific]*:

  Available for system supplier definition.

- **0xFF00** *[eraseMemory]*:

  Routine for erasing ECU memory as part of the reprogramming process.

- **0xFF01** *[checkProgrammingDependencies]*:

  Routine used to verify that all required programming-dependency conditions are satisfied
  as part of the ECU reprogramming process.

- **0xFF02-0xFFFF** *[ISOSAEReserved]*:

  Reserved by ISO/SAE for future standardisation.

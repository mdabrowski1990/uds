.. _knowledge-base-did:

Data Identifier (DID)
=====================
A Data Identifier (DID) is a 16-bit identifier used by a diagnostic client to access specific data stored in
a server (ECU).

The following UDS services operate on DIDs:

- :ref:`ReadDataByIdentifier (0x22) <knowledge-base-service-read-data-by-identifier>`
- :ref:`DynamicallyDefineDataIdentifier (0x2C) <knowledge-base-service-dynamically-define-data-identifier>`
- :ref:`ReadDataByPeriodicIdentifier (0x2A) <knowledge-base-service-read-data-by-periodic-identifier>`
- :ref:`WriteDataByIdentifier (0x2E) <knowledge-base-service-write-data-by-identifier>`
- :ref:`InputOutputControlByIdentifier (0x2F) <knowledge-base-service-input-output-control-by-identifier>`

Each DID points to a data structure of arbitrary length (full-byte-aligned).
The content, byte order, scaling and accessibility depend on the DID definition in the server’s specification.


.. _knowledge-base-did-2020:

Defined by ISO 14229-1:2020
---------------------------
- **0x0000-0x00FF** *[ISOSAEReserved]*:
  Reserved for future definition.

- **0x0100-0xA5FF** *[VehicleManufacturerSpecific]*:
  Defined by the OEM for vehicle/system specific use.

- **0xA600-0xA7FF** *[ReservedForLegislativeUse]*:
  Reserved for future legislation related definitions.

- **0xA800-0xACFF** *[VehicleManufacturerSpecific]*:
  Defined by the OEM for vehicle/system specific use.

- **0xAD00-0xAFFF** *[ReservedForLegislativeUse]*:
  Reserved for future legislation related definitions.

- **0xB000-0xB1FF** *[VehicleManufacturerSpecific]*:
  Defined by the OEM for vehicle/system specific use.

- **0xB200-0xBFFF** *[ReservedForLegislativeUse]*:
  Reserved for future legislation related definitions.

- **0xC000-0xC2FF** *[VehicleManufacturerSpecific]*:
  Defined by the OEM for vehicle/system specific use.

- **0xC300-0xCEFF** *[ReservedForLegislativeUse]*:
  Reserved for future legislation related definitions.

- **0xCF00-0xEFFF** *[VehicleManufacturerSpecific]*:
  Defined by the OEM for vehicle/system specific use.

- **0xF000-0xF00F** *[networkConfigurationDataForTractorTrailerApplicationDataIdentifier]*:
  Remote addresses of all trailer systems.

- **0xF010-0xF0FF** *[vehicleManufacturerSpecific]*:
  Defined by the OEM for vehicle/system specific use.

- **0xF100-0xF17F** *[identificationOptionVehicleManufacturerSpecificDataIdentifier]*:
  Available for vehicle manufacturer server/vehicle Identification related information.

- **0xF180** *[BootSoftwareIdentificationDataIdentifier]*:
  Bootloader Software Identification information.

- **0xF181** *[applicationSoftwareIdentificationDataIdentifier]*:
  Application Software Identification information.

- **0xF182** *[applicationDataIdentificationDataIdentifier]*:
  Application Data Identification information.

- **0xF183** *[bootSoftwareFingerprintDataIdentifier]*:
  Information about the last Bootloader Software update.

- **0xF184** *[applicationSoftwareFingerprintDataIdentifier]*:
  Information about the last Application Software update.

- **0xF185** *[applicationDataFingerprintDataIdentifier]*:
  Information about the last Application Data update.

- **0xF186** *[ActiveDiagnosticSessionDataIdentifier]*:
  Currently active Diagnostic Session.

- **0xF187** *[vehicleManufacturerSparePartNumberDataIdentifier]*:
  Spare Part Number (used by vehicle manufacturer) of the server unit.

- **0xF188** *[vehicleManufacturerECUSoftwareNumberDataIdentifier]*:
  Server's ECU software number used by vehicle manufacturer.

- **0xF189** *[vehicleManufacturerECUSoftwareVersionNumberDataIdentifier]*:
  Server's ECU software version number used by vehicle manufacturer.

- **0xF18A** *[systemSupplierIdentifierDataIdentifier]*:
  Identification of the supplier of the server's system.

- **0xF18B** *[ECUManufacturingDateDataIdentifier]*:
  Server's ECU manufacturing date.

- **0xF18C** *[ECUSerialNumberDataIdentifier]*:
  Server's unique ECU Serial Number.

- **0xF18D** *[supportedFunctionalUnitsDataIdentifier]*:
  Functional units implemented in the server.

- **0xF18E** *[VehicleManufacturerKitAssemblyPartNumberDataIdentifier]*:
  Spare Part Number (used by vehicle manufacturer) of the assembly kit that the server is part of.

- **0xF18F** *[RegulationXSoftwareIdentificationNumbers]*:
  Software Identification numbers required by legislation.

- **0xF190** *[VINDataIdentifier]*:
  VIN Number.

- **0xF191** *[vehicleManufacturerECUHardwareNumberDataIdentifier]*:
  Server's ECU hardware number used by vehicle manufacturer.

- **0xF192** *[systemSupplierECUHardwareNumberDataIdentifier]*:
  Server's ECU hardware number used by system supplier.

- **0xF193** *[systemSupplierECUHardwareVersionNumberDataIdentifier]*:
  Server's ECU hardware version number used by system supplier.

- **0xF194** *[systemSupplierECUSoftwareNumberDataIdentifier]*:
  Server's ECU software number used by system supplier.

- **0xF195** *[systemSupplierECUSoftwareVersionNumberDataIdentifier]*:
  Server's ECU software version number used by system supplier.

- **0xF196** *[exhaustRegulationOrTypeApprovalNumberDataIdentifier]*:
  Exhaust regulation or type approval number (for systems which require type approval).

- **0xF197** *[systemNameOrEngineTypeDataIdentifier]*:
  System name or engine type.

- **0xF198** *[repairShopCodeOrTesterSerialNumberDataIdentifier]*:
  The repair shop code or tester serial number that was used for the most recent server reprogramming.

- **0xF199** *[programmingDateDataIdentifier]*:
  The last date when the server was programmed.

- **0xF19A** *[calibrationRepairShopCodeOrCalibrationEquipmentSerialNumberDataIdentifier]*:
  The repair shop code or tester serial number that was used for the most recent server recalibration.

- **0xF19B** *[calibrationDateDataIdentifier]*:
  The last date when the server was calibrated.

- **0xF19C** *[calibrationEquipmentSoftwareNumberDataIdentifier]*:
  Client's software version that was used for the server calibration.

- **0xF19D** *[ECUInstallationDateDataIdentifier]*:
  The date when the server (ECU) was installed in the vehicle.

- **0xF19E** *[ODXFileDataIdentifier]*:
  Reference to the Open Diagnostic Data Exchange (ODX) file used by the server.

- **0xF19F** *[EntityDataIdentifier]*:
  Entity reference for a Secured Data Transmission.

- **0xF1A0-0xF1EF** *[identificationOptionVehicleManufacturerSpecific]*:
  Available for vehicle manufacturer server/vehicle Identification related information.

- **0xF1F0-0xF1FF** *[identificationOptionSystemSupplierSpecific]*:
  Available for system supplier server/vehicle Identification related information.

- **0xF200-0xF2FF** *[periodicDataIdentifier]*:
  DIDs used for periodic data transmission by ReadDataByPeriodicIdentifier service (SID 0x2A).

- **0xF300-0xF3FF** *[DynamicallyDefinedDataIdentifier]*:
  DIDs that can be dynamically defined by the client using DynamicallyDefineDataIdentifier service (SID 0x2C).

- **0xF400-0xF5FF** *[OBDDataIdentifier]*:
  Regulated emissions related data defined by SAE J1979-DA.

- **0xF600-0xF6FF** *[OBDMonitorDataIdentifier]*:
  OBD/EOBD monitoring values defined by ISO 15031-5.

- **0xF700-0xF7FF** *[OBDDataIdentifier]*:
  Regulated emissions related data defined by SAE J1979-DA.

- **0xF800-0xF8FF** *[OBDInfoTypeDataIdentifier]*:
  OBD/EOBD information-type values defined by ISO 15031-5.

- **0xF900-0xF9FF** *[TachographDataIdentifier]*:
  Tachograph values defined by ISO 16844-7.

- **0xFA00-0xFA0F** *[AirbagDeploymentDataIdentifier]*:
  End of life activation of on-board pyrotechnic devices (airbags) as defined by ISO 26021-2.

- **0xFA10** *[NumberOfEDRDevices]*:
  Number of EDR devices that are capable of reporting EDR data.

- **0xFA11** *[EDRIdentification]*:
  EDR Identification data.

- **0xFA12** *[EDRDeviceAddressInformation]*:
  EDR device address information defined by ISO 26021-2

- **0xFA13-0xFA18** *[EDREntries]*:
  EDR entries (0xFA13 is the earliest).

- **0xFA19-0xFAFF** *[SafetySystemDataIdentifier]*:
  Safety system related information.

- **0xFB00-0xFCFF** *[ReservedForLegislativeUse]*:
  Reserved for future legislation related definitions.

- **0xFD00-0xFEFF** *[SystemSupplierSpecific]*:
  Available for system supplier definition.

- **0xFF00** *[UDSVersionDataIdentifier]*:
  UDS version implemented in the server.

- **0xFF01** *[ReservedForISO15765-5]*:
  Whether the server (ECU) supports CAN Classical, CAN FD or both.

- **0xFF02-0xFFFF** *[ISOSAEReserved]*:
  Reserved for future definition.


.. _knowledge-base-did-2013:

Defined by ISO 14229-1:2013
---------------------------
- **0x0000-0x00FF** *[ISOSAEReserved]*

- **0x0100-0xA5FF** *[VehicleManufacturerSpecific]*

- **0xA600-0xA7FF** *[ReservedForLegislativeUse]*

- **0xA800-0xACFF** *[VehicleManufacturerSpecific]*

- **0xAD00-0xAFFF** *[ReservedForLegislativeUse]*

- **0xB000-0xB1FF** *[VehicleManufacturerSpecific]*

- **0xB200-0xBFFF** *[ReservedForLegislativeUse]*

- **0xC000-0xC2FF** *[VehicleManufacturerSpecific]*

- **0xC300-0xCEFF** *[ReservedForLegislativeUse]*

- **0xCF00-0xEFFF** *[VehicleManufacturerSpecific]*

- **0xF000-0xF00F** *[networkConfigurationDataForTractorTrailerApplicationDataIdentifier]*

- **0xF010-0xF0FF** *[vehicleManufacturerSpecific]*

- **0xF100-0xF17F** *[identificationOptionVehicleManufacturerSpecificDataIdentifier]*

- **0xF180** *[BootSoftwareIdentificationDataIdentifier]*

- **0xF181** *[applicationSoftwareIdentificationDataIdentifier]*

- **0xF182** *[applicationDataIdentificationDataIdentifier]*

- **0xF183** *[bootSoftwareFingerprintDataIdentifier]*

- **0xF184** *[applicationSoftwareFingerprintDataIdentifier]*

- **0xF185** *[applicationDataFingerprintDataIdentifier]*

- **0xF186** *[ActiveDiagnosticSessionDataIdentifier]*

- **0xF187** *[vehicleManufacturerSparePartNumberDataIdentifier]*

- **0xF188** *[vehicleManufacturerECUSoftwareNumberDataIdentifier]*

- **0xF189** *[vehicleManufacturerECUSoftwareVersionNumberDataIdentifier]*

- **0xF18A** *[systemSupplierIdentifierDataIdentifier]*

- **0xF18B** *[ECUManufacturingDateDataIdentifier]*

- **0xF18C** *[ECUSerialNumberDataIdentifier]*

- **0xF18D** *[supportedFunctionalUnitsDataIdentifier]*

- **0xF18E** *[VehicleManufacturerKitAssemblyPartNumberDataIdentifier]*

- **0xF18F** *[ISOSAEReservedStandardized]*

- **0xF190** *[VINDataIdentifier]*

- **0xF191** *[vehicleManufacturerECUHardwareNumberDataIdentifier]*

- **0xF192** *[systemSupplierECUHardwareNumberDataIdentifier]*

- **0xF193** *[systemSupplierECUHardwareVersionNumberDataIdentifier]*

- **0xF194** *[systemSupplierECUSoftwareNumberDataIdentifier]*

- **0xF195** *[systemSupplierECUSoftwareVersionNumberDataIdentifier]*

- **0xF196** *[exhaustRegulationOrTypeApprovalNumberDataIdentifier]*

- **0xF197** *[systemNameOrEngineTypeDataIdentifier]*

- **0xF198** *[repairShopCodeOrTesterSerialNumberDataIdentifier]*

- **0xF199** *[programmingDateDataIdentifier]*

- **0xF19A** *[calibrationRepairShopCodeOrCalibrationEquipmentSerialNumberDataIdentifier]*

- **0xF19B** *[calibrationDateDataIdentifier]*

- **0xF19C** *[calibrationEquipmentSoftwareNumberDataIdentifier]*

- **0xF19D** *[ECUInstallationDateDataIdentifier]*

- **0xF19E** *[ODXFileDataIdentifier]*

- **0xF19F** *[EntityDataIdentifier]*

- **0xF1A0-0xF1EF** *[identificationOptionVehicleManufacturerSpecific]*

- **0xF1F0-0xF1FF** *[identificationOptionSystemSupplierSpecific]*

- **0xF200-0xF2FF** *[periodicDataIdentifier]*

- **0xF300-0xF3FF** *[DynamicallyDefinedDataIdentifier]*

- **0xF400-0xF5FF** *[OBDDataIdentifier]*

- **0xF600-0xF7FF** *[OBDMonitorDataIdentifier]*

- **0xF800-0xF8FF** *[OBDInfoTypeDataIdentifier]*

- **0xF900-0xF9FF** *[TachographDataIdentifier]*

- **0xFA00-0xFA0F** *[AirbagDeploymentDataIdentifier]*

- **0xFA10** *[NumberOfEDRDevices]*

- **0xFA11** *[EDRIdentification]*

- **0xFA12** *[EDRDeviceAddressInformation]*

- **0xFA13-0xFA18** *[EDREntries]*

- **0xFA19-0xFAFF** *[SafetySystemDataIdentifier]*

- **0xFB00-0xFCFF** *[ReservedForLegislativeUse]*

- **0xFD00-0xFEFF** *[SystemSupplierSpecific]*

- **0xFF00** *[UDSVersionDataIdentifier]*

- **0xFF01-0xFFFF** *[ISOSAEReserved]*

""":ref:`DID <knowledge-base-did>` related constants."""

__all__ = [
    "DID_BIT_LENGTH",
    "PERIODIC_DID_BIT_LENGTH", "PERIODIC_DID_OFFSET",
    "DID_MAPPING_2020", "DID_MAPPING_2013",
]

from typing import Dict

DID_BIT_LENGTH = 16
"""Number of bits used for :ref:`DID <knowledge-base-did>`"""

PERIODIC_DID_BIT_LENGTH = 8
"""Number of bits used for `periodicDataIdentifier` in 
:ref:`ReadDataByPeriodicIdentifier service <knowledge-base-service-read-data-by-periodic-identifier>`"""
PERIODIC_DID_OFFSET = 0xF200
"""Offset used by `periodicDataIdentifiers`"""

DID_MAPPING_2020: Dict[int, str] = {
    0xF180: "BootSoftwareIdentificationDataIdentifier",
    0xF181: "applicationSoftwareIdentificationDataIdentifier",
    0xF182: "applicationDataIdentificationDataIdentifier",
    0xF183: "bootSoftwareFingerprintDataIdentifier",
    0xF184: "applicationSoftwareFingerprintDataIdentifier",
    0xF185: "applicationDataFingerprintDataIdentifier",
    0xF186: "ActiveDiagnosticSessionDataIdentifier",
    0xF187: "vehicleManufacturerSparePartNumberDataIdentifier",
    0xF188: "vehicleManufacturerECUSoftwareNumberDataIdentifier",
    0xF189: "vehicleManufacturerECUSoftwareVersionNumberDataIdentifier",
    0xF18A: "systemSupplierIdentifierDataIdentifier",
    0xF18B: "ECUManufacturingDateDataIdentifier",
    0xF18C: "ECUSerialNumberDataIdentifier",
    0xF18D: "supportedFunctionalUnitsDataIdentifier",
    0xF18E: "VehicleManufacturerKitAssemblyPartNumberDataIdentifier",
    0xF18F: "RegulationXSoftwareIdentificationNumbers",
    0xF190: "VINDataIdentifier",
    0xF191: "vehicleManufacturerECUHardwareNumberDataIdentifier",
    0xF192: "systemSupplierECUHardwareNumberDataIdentifier",
    0xF193: "systemSupplierECUHardwareVersionNumberDataIdentifier",
    0xF194: "systemSupplierECUSoftwareNumberDataIdentifier",
    0xF195: "systemSupplierECUSoftwareVersionNumberDataIdentifier",
    0xF196: "exhaustRegulationOrTypeApprovalNumberDataIdentifier",
    0xF197: "systemNameOrEngineTypeDataIdentifier",
    0xF198: "repairShopCodeOrTesterSerialNumberDataIdentifier",
    0xF199: "programmingDateDataIdentifier",
    0xF19A: "calibrationRepairShopCodeOrCalibrationEquipmentSerialNumberDataIdentifier",
    0xF19B: "calibrationDateDataIdentifier",
    0xF19C: "calibrationEquipmentSoftwareNumberDataIdentifier",
    0xF19D: "ECUInstallationDateDataIdentifier",
    0xF19E: "ODXFileDataIdentifier",
    0xF19F: "EntityDataIdentifier",
    0xFA10: "NumberOfEDRDevices",
    0xFA11: "EDRIdentification",
    0xFA12: "EDRDeviceAddressInformation",
    0xFF00: "UDSVersionDataIdentifier",
    0xFF01: "ReservedForISO15765-5",
}
""":ref:`Data Identifiers mapping according to ISO 14229-1:2020 <knowledge-base-did-2020>`."""

DID_MAPPING_2013: Dict[int, str] = {
    0xF180: "BootSoftwareIdentificationDataIdentifier",
    0xF181: "applicationSoftwareIdentificationDataIdentifier",
    0xF182: "applicationDataIdentificationDataIdentifier",
    0xF183: "bootSoftwareFingerprintDataIdentifier",
    0xF184: "applicationSoftwareFingerprintDataIdentifier",
    0xF185: "applicationDataFingerprintDataIdentifier",
    0xF186: "ActiveDiagnosticSessionDataIdentifier",
    0xF187: "vehicleManufacturerSparePartNumberDataIdentifier",
    0xF188: "vehicleManufacturerECUSoftwareNumberDataIdentifier",
    0xF189: "vehicleManufacturerECUSoftwareVersionNumberDataIdentifier",
    0xF18A: "systemSupplierIdentifierDataIdentifier",
    0xF18B: "ECUManufacturingDateDataIdentifier",
    0xF18C: "ECUSerialNumberDataIdentifier",
    0xF18D: "supportedFunctionalUnitsDataIdentifier",
    0xF18E: "VehicleManufacturerKitAssemblyPartNumberDataIdentifier",
    0xF190: "VINDataIdentifier",
    0xF191: "vehicleManufacturerECUHardwareNumberDataIdentifier",
    0xF192: "systemSupplierECUHardwareNumberDataIdentifier",
    0xF193: "systemSupplierECUHardwareVersionNumberDataIdentifier",
    0xF194: "systemSupplierECUSoftwareNumberDataIdentifier",
    0xF195: "systemSupplierECUSoftwareVersionNumberDataIdentifier",
    0xF196: "exhaustRegulationOrTypeApprovalNumberDataIdentifier",
    0xF197: "systemNameOrEngineTypeDataIdentifier",
    0xF198: "repairShopCodeOrTesterSerialNumberDataIdentifier",
    0xF199: "programmingDateDataIdentifier",
    0xF19A: "calibrationRepairShopCodeOrCalibrationEquipmentSerialNumberDataIdentifier",
    0xF19B: "calibrationDateDataIdentifier",
    0xF19C: "calibrationEquipmentSoftwareNumberDataIdentifier",
    0xF19D: "ECUInstallationDateDataIdentifier",
    0xF19E: "ODXFileDataIdentifier",
    0xF19F: "EntityDataIdentifier",
    0xFA10: "NumberOfEDRDevices",
    0xFA11: "EDRIdentification",
    0xFA12: "EDRDeviceAddressInformation",
    0xFF00: "UDSVersionDataIdentifier",
}
""":ref:`Data Identifiers mapping according to ISO 14229-1:2013 <knowledge-base-did-2013>`."""

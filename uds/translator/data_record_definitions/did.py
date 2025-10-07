__all__ = [
    "DID", "DID_2020", "DID_2013",
    "DID_DATA_MAPPING_2020", "DID_DATA_MAPPING_2013", "DEFAULT_DID_DATA",
]

from ..data_record import ConditionalMappingDataRecord, MappingDataRecord, RawDataRecord

DID_MAPPING_2013 = {
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
DID_MAPPING_2020 = {
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

DID_DATA_MAPPING_2013 = {}  # TODO: define
DID_DATA_MAPPING_2020 = {}  # TODO: define

DID_2013 = MappingDataRecord(name="DID",
                             length=16,
                             values_mapping=DID_MAPPING_2013)
OPTIONAL_DID_2013 = MappingDataRecord(name="DID",
                                      length=16,
                                      values_mapping=DID_MAPPING_2013,
                                      min_occurrences=0,
                                      max_occurrences=1)
DID_2020 = MappingDataRecord(name="DID",
                             length=16,
                             values_mapping=DID_MAPPING_2020)
OPTIONAL_DID_2020 = MappingDataRecord(name="DID",
                                      length=16,
                                      values_mapping=DID_MAPPING_2020,
                                      min_occurrences=0,
                                      max_occurrences=1)
DID = DID_2020

DEFAULT_DID_DATA = RawDataRecord(name="DID data",
                                 length=8,
                                 min_occurrences=1,
                                 max_occurrences=None)
DID_DATA_2013 = ConditionalMappingDataRecord(mapping=DID_DATA_MAPPING_2013,
                                             default_message_continuation=[DEFAULT_DID_DATA])
DID_DATA_2020 = ConditionalMappingDataRecord(mapping=DID_DATA_MAPPING_2020,
                                             default_message_continuation=[DEFAULT_DID_DATA])

"""Data Records definitions for Data Identifiers."""

__all__ = [
    "get_did_2013", "get_did_2020",
    "get_did_data_2013",
]

from typing import Tuple

from ..data_record import (
    AbstractDataRecord,
    ConditionalFormulaDataRecord,
    ConditionalMappingDataRecord,
    MappingDataRecord,
    RawDataRecord,
)
from .other import ACTIVE_DIAGNOSTIC_SESSION, RESERVED_BIT

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

DID_DATA_MAPPING_2013 = {
    0xF186: (RESERVED_BIT, ACTIVE_DIAGNOSTIC_SESSION),
}
DID_DATA_MAPPING_2020 = {
    0xF186: DID_DATA_MAPPING_2013[0xF186],
}

def get_did_2013(name: str = "DID", optional: bool = False) -> MappingDataRecord:
    """
    Get DID Data Record compatible with ISO 14229-1:2013 version.

    :param name: Name to assign to the Data Record.
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: Created DID Data Record.
    """
    return MappingDataRecord(name=name,
                             length=16,
                             values_mapping=DID_MAPPING_2013,
                             min_occurrences=0 if optional else 1,
                             max_occurrences=1)

def get_did_2020(name: str = "DID", optional: bool = False) -> MappingDataRecord:
    """
    Get DID Data Record compatible with ISO 14229-1:2020 version.

    :param name: Name to assign to the Data Record.
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: Created DID Data Record.
    """
    return MappingDataRecord(name=name,
                             length=16,
                             values_mapping=DID_MAPPING_2020,
                             min_occurrences=0 if optional else 1,
                             max_occurrences=1)

def get_did_data_2013(name: str = "DID data") -> ConditionalFormulaDataRecord:
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)
    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2013.get(did, None)
        if data_records is None:
            return None
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError("Only fixed length DID data structures are supported right now.")
            total_length += dr.max_occurrences * dr.length
        return RawDataRecord(name=name,
                             children=data_records,
                             length=total_length,
                             min_occurrences=1,
                             max_occurrences=1),
    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])

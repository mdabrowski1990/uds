"""Data Records definitions for Data Identifiers."""

__all__ = [
    "DID_2013", "DID_2020", "OPTIONAL_PERIODIC_DID", "MULTIPLE_DID_2013", "MULTIPLE_DID_2020", "MULTIPLE_PERIODIC_DID",
    "get_did_2013", "get_did_2020", "get_dids_2013", "get_dids_2020",
    "get_did_data_2013", "get_did_data_2020",
    "get_did_records_formula_2013", "get_did_records_formula_2020",
]

from typing import Callable, List, Optional, Tuple, Union

from ..data_record import (
    AbstractDataRecord,
    AliasMessageStructure,
    ConditionalFormulaDataRecord,
    LinearFormulaDataRecord,
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
""":ref:`Data Identifiers mapping according to ISO 14229-1:2013 <knowledge-base-did-2013>`."""

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
""":ref:`Data Identifiers mapping according to ISO 14229-1:2020 <knowledge-base-did-2020>`."""

DID_DATA_MAPPING_2013 = {
    0xF186: (RESERVED_BIT, ACTIVE_DIAGNOSTIC_SESSION),
}
DID_DATA_MAPPING_2020 = {
    0xF186: DID_DATA_MAPPING_2013[0xF186],
}

DID_2013 = MappingDataRecord(name="DID",
                             length=16,
                             values_mapping=DID_MAPPING_2013)
DID_2020 = MappingDataRecord(name="DID",
                             length=16,
                             values_mapping=DID_MAPPING_2020)
OPTIONAL_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                length=8,
                                                offset=0xF200,
                                                factor=1,
                                                min_occurrences=0,
                                                max_occurrences=1)
MULTIPLE_DID_2013 = MappingDataRecord(name="DID",
                                      length=16,
                                      values_mapping=DID_MAPPING_2013,
                                      min_occurrences=1,
                                      max_occurrences=None)
MULTIPLE_DID_2020 = MappingDataRecord(name="DID",
                                      length=16,
                                      values_mapping=DID_MAPPING_2020,
                                      min_occurrences=1,
                                      max_occurrences=None)
MULTIPLE_PERIODIC_DID = LinearFormulaDataRecord(name="Periodic DID",
                                                length=8,
                                                offset=0xF200,
                                                factor=1,
                                                min_occurrences=1,
                                                max_occurrences=None)


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
    """
    Get Conditional Data Record for DID data that is compatible with ISO 14229-1:2013 version.

    :param name: Name for the Data Record that contains whole DID data.

    :return: Conditional Data Record for DID data.
    """
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)

    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2013.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
        return (RawDataRecord(name=name,
                              children=data_records,
                              length=total_length,
                              min_occurrences=1,
                              max_occurrences=1),)
    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])


def get_did_data_2020(name: str = "DID data") -> ConditionalFormulaDataRecord:
    """
    Get Conditional Data Record for DID data that is compatible with ISO 14229-1:2020 version.

    :param name: Name for the Data Record that contains whole DID data.

    :return: Conditional Data Record for DID data.
    """
    default_did_data = RawDataRecord(name=name,
                                     length=8,
                                     min_occurrences=1,
                                     max_occurrences=None)

    def _get_did_data(did: int) -> Tuple[RawDataRecord]:
        data_records = DID_DATA_MAPPING_2020.get(did, None)
        if data_records is None:
            raise ValueError(f"No data structure defined for DID 0x{did:04X}.")
        total_length = 0
        for dr in data_records:
            if not isinstance(dr, AbstractDataRecord) or not dr.fixed_total_length:
                raise ValueError(f"Incorrectly defined data structure for DID 0x{did:04X}. "
                                 f"Only fixed length data records are supported right now.")
            total_length += dr.min_occurrences * dr.length
        return (RawDataRecord(name=name,
                              children=data_records,
                              length=total_length,
                              min_occurrences=1,
                              max_occurrences=1),)
    return ConditionalFormulaDataRecord(formula=_get_did_data,
                                        default_message_continuation=[default_did_data])


def get_dids_2013(did_count: int,
                  record_number: Optional[int],
                  optional: bool = False) -> Tuple[Union[MappingDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get DIDs related Data Records for given record (e.g. Snapshot or Stored Data).

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param did_count: Number of DIDs that are part of the record that contains DIDs.
    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: DIDs related Data Records that are part of the record.
    """
    data_records: List[Union[MappingDataRecord, ConditionalFormulaDataRecord]] = []
    for did_number in range(did_count):
        name = f"DID#{did_number + 1}" if record_number is None else f"DID#{record_number}_{did_number + 1}"
        data_records.append(get_did_2013(name, optional=optional))
        data_records.append(get_did_data_2013(name=f"{name} data"))
    return tuple(data_records)


def get_dids_2020(did_count: int,
                  record_number: Optional[int],
                  optional: bool = False) -> Tuple[Union[MappingDataRecord, ConditionalFormulaDataRecord], ...]:
    """
    Get DIDs related Data Records for given record (e.g. Snapshot or Stored Data).

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param did_count: Number of DIDs that are part of the record that contains DIDs.
    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).
    :param optional: False if the Data Record presence is mandatory, True otherwise.

    :return: DIDs related Data Records that are part of the record.
    """
    data_records: List[Union[MappingDataRecord, ConditionalFormulaDataRecord]] = []
    for did_number in range(did_count):
        name = f"DID#{did_number + 1}" if record_number is None else f"DID#{record_number}_{did_number + 1}"
        data_records.append(get_did_2020(name, optional=optional))
        data_records.append(get_did_data_2020(name=f"{name} data"))
    return tuple(data_records)


def get_did_records_formula_2013(record_number: Optional[int]) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting DID related Data Records.

    .. note:: Supports only ISO 14229-1:2013 DIDs.

    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).

    :return: Formula for given record (e.g. Snapshot or Stored Data).
    """
    return lambda did_count: get_dids_2013(did_count=did_count,
                                           record_number=record_number)


def get_did_records_formula_2020(record_number: Optional[int]) -> Callable[[int], AliasMessageStructure]:
    """
    Get formula that can be used by Conditional Data Record for getting DID related Data Records.

    .. note:: Supports only ISO 14229-1:2020 DIDs.

    :param record_number: Order number of the record that contains DIDs.
        None if this is the only DIDs group (e.g. part of ReadDataByIdentifier).

    :return: Formula for given record (e.g. Snapshot or Stored Data).
    """
    return lambda did_count: get_dids_2020(did_count=did_count,
                                           record_number=record_number)

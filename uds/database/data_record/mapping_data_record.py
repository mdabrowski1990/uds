"""Definition of TextDataRecord which is class for encode and decode values of data records."""

__all__ = ["MappingDataRecord"]

from typing import Dict
from types import MappingProxyType

from .abstract_data_record import AbstractDataRecord, DataRecordPhysicalValueAlias, DecodedDataRecord
from .raw_data_record import RawDataRecord


class MappingDataRecord(RawDataRecord, AbstractDataRecord):
    """Implementation for Text Data Record."""

    def __init__(self, name: str, length: int, mapping: Dict[int, str]) -> None:
        """
        Initialize Text Data Record.

        :param name: Name to assign to this Data Record.
        :param length: Number of bits that this Text Table Data Record is stored over.
        :param mapping: Bidirectional translation between raw value (int) and meaningful value (e.g. float, str).
        """
        super().__init__(name, length)
        self.length = length
        self.mapping = mapping

    @property
    def mapping(self):
        """Get mapping dict."""
        return self.__mapping

    @mapping.setter
    def mapping(self, mapping: Dict[int, str]) -> None:
        """
        Set the mapping.

        :param mapping: dict contains mapping.
        """
        self.__mapping = MappingProxyType(mapping)
        self.__reversed_mapping = MappingProxyType({v: k for k, v in self.__mapping.items()})

    @property
    def reversed_mapping(self):
        """Get reversed mapping dict."""
        return self.__reversed_mapping

    def decode(self, raw_value: int) -> DecodedDataRecord:  # noqa: F841
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        if raw_value in self.mapping:
            physical_value = self.mapping[raw_value]
            return DecodedDataRecord(name=self.name, raw_value=raw_value, physical_value=physical_value)
        return DecodedDataRecord(name=self.name, raw_value=raw_value, physical_value=raw_value)

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        if isinstance(physical_value, int):
            return physical_value
        if isinstance(physical_value, str):
            return self.reversed_mapping[physical_value]
        raise TypeError("physical_value has not expected type.")

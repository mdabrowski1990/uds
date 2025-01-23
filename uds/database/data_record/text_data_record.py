"""Definition of TextDataRecord which is class for encode and decode values of data records."""

__all__ = ["TextDataRecord"]

from typing import Dict, Optional

from .abstract_data_record import AbstractDataRecord, DataRecordPhysicalValueAlias, DecodedDataRecord
from .raw_data_record import RawDataRecord


class TextDataRecord(RawDataRecord, AbstractDataRecord):
    """Implementation for Text Data Record."""

    def __init__(self, name: str, length: int, mapping: Optional[Dict[int, str]] = None) -> None:
        """
        Initialize Text Data Record.

        :param name: Name to assign to this Data Record.

        :raise TypeError: Provided value of name is not str type.
        """
        super().__init__(name, length)
        self.length = length
        self.mapping = mapping

    @property  # noqa: F841
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        return self.__length

    @length.setter
    def length(self, value: str) -> None:
        """
        Set the length.

        :param value: str contains data record text.
        """
        self.__length = len(value.encode('utf-8')) * 8

    @property
    def mapping(self):
        """Get mapping dict."""
        return self.__mapping

    @mapping.setter
    def mapping(self, mapping: dict) -> None:
        """
        Set the mapping.

        :param mapping: dict contains mapping.
        """
        self.__mapping = mapping
        self.__reversed_mapping = {v: k for k, v in self.__mapping.items()}

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
            return DecodedDataRecord(name=self.__name, raw_value=physical_value, physical_value=raw_value)
        return DecodedDataRecord(name=self.__name, raw_value=raw_value, physical_value=raw_value)

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        if isinstance(physical_value, int):
            return physical_value
        if isinstance(physical_value, str):
            if physical_value in self.__reversed_mapping:
                return self.__reversed_mapping[physical_value]
            raise KeyError("physical_value not found in provided mapping.")
        else:
            raise TypeError("physical_value has not expected type.")

"""Definition of TextDataRecord which is class for encode and decode values of data records."""
import copy
from typing import Optional, Tuple, Union, Dict
from uu import decode

from uds.database.abstract_data_record import (AbstractDataRecord, DataRecordType, DataRecordPhysicalValueAlias,
                                               DecodedDataRecord)


class TextDataRecord(AbstractDataRecord):
    """Implementation for Text Data Record."""
    def __init__(self, name: str, length: int, mapping: Dict[int, str] = None) -> None:
        """Initialize Text Data Record.

        :param name: Name to assign to this Data Record.

        :raise TypeError: Provided value of name is not str type.
        """
        super().__init__(name)
        self.length = length
        # self.__reversed_mapping = None ### should it be deleted?
        self.__mapping = mapping

    @property  # noqa: F841
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        return self.__length

    @length.setter
    def length(self, value: str) -> None:
        """Set the length.

        :param value: str contains data record text.
        """
        self.__length = len(value.encode('utf-8')) * 8

    @property  # noqa: F841
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """
        # TODO

    @property  # noqa: F841
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.is_reoccurring`
            equals True.
        """
        # TODO

    @property  # noqa: F841
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.is_reoccurring`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        # TODO

    @property  # noqa: F841
    def contains(self) -> Tuple["AbstractDataRecord", ...]:
        """Get Data Records contained by this Data Record."""
        # TODO

    @property
    def mapping(self):
        """Get mapping dict."""
        return self.__mapping

    @mapping.setter
    def mapping(self, mapping: dict) -> None:
        """Set the mapping.

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
        if self.__reversed_mapping:
            try:
                decoded_value = self.__reversed_mapping[raw_value]
                return DecodedDataRecord(name=self.name, raw_value=decoded_value, physical_value=raw_value)
            except KeyError as error:
                raise KeyError("raw_value not found in provided mapping.") from error
        return DecodedDataRecord(name=self.name, raw_value=raw_value, physical_value=raw_value)

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        if isinstance(physical_value, int):
            return physical_value
        elif isinstance(physical_value, str):
            if self.__mapping:
                try:
                    return self.__mapping[physical_value]
                except KeyError as error:
                    raise KeyError("physical_value not found in provided mapping.") from error
            else:
                raise TypeError("During encoding of str mapping must be provided.")

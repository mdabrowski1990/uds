"""Definition of TextDataRecord which is class for encode and decode values of data records."""
from typing import Optional, Tuple, Union, Dict
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
        self.mapping = mapping

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

    def decode(self, physical_value: Union[int, str]) -> DecodedDataRecord:  # noqa: F841
        """
        Decode physical value for provided raw value.

        :param physical_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        if isinstance(physical_value, int):
            return DecodedDataRecord(name=self.name, raw_value=physical_value, physical_value=physical_value)

        if self.mapping:
            for k, v in self.mapping.items():
                if v == physical_value:
                    return DecodedDataRecord(name=self.name, raw_value=k, physical_value=physical_value)
            raise ValueError("physical_value not found in provided mapping.")
        else:
            raise TypeError("physical_value must be int or mapping must be provided.")

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        if isinstance(physical_value, int):
            return physical_value
        elif isinstance(physical_value, str):
            if self.mapping:
                for k, v in self.mapping.items():
                    if v == physical_value:
                        return k
                raise ValueError("physical_value not found in provided mapping.")
            else:
                raise TypeError("During encoding of str mapping must be provided.")

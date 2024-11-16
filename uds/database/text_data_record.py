"""Definition of TextDataRecord which is class for encode and decode values of data records."""
from typing import Optional, Tuple, Union
from uds.database.abstract_data_record import (AbstractDataRecord, DataRecordType, DataRecordPhysicalValueAlias,
                                               DecodedDataRecord)


class TextDataRecord(AbstractDataRecord):
    """Implementation for Text Data Record."""
    def __init__(self, name: str, text: str) -> None:
        """Initialize Text Data Record.

        :param name: Name to assign to this Data Record.

        :raise TypeError: Provided value of name is not str type.
        """
        super().__init__(name)
        self.length = text

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

    def decode(self, raw_value: Union[int, str]) -> DecodedDataRecord:  # noqa: F841
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """
        if isinstance(raw_value, int):
            return DecodedDataRecord(name=self.name, raw_value=raw_value, physical_value=raw_value)
        elif isinstance(raw_value, str):
            decoded_value = int.from_bytes(raw_value.encode("utf-8"), byteorder="big")
            return DecodedDataRecord(name=self.name, raw_value=decoded_value, physical_value=raw_value)
        else:
            raise TypeError("Raw_value must be int or str.")

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> Union[int, str]:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
        def encode_value(value):
            if isinstance(value, int):
                return value
            elif isinstance(value, str):
                # TODO
            elif isinstance(value, float):
                # TODO

        if isinstance(physical_value, (int, str, float)):
            return encode_value(physical_value)
        elif isinstance(physical_value, tuple):
            if isinstance(physical_value, DecodedDataRecord):
                return tuple(encode_value(elem["raw_value"]) for elem in physical_value)
        else:
            raise TypeError("Raw_value must be int or str.")

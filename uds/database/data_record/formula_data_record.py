"""Definition of FormulaDataRecord."""

from typing import Callable, Optional, Tuple

from .abstract_data_record import AbstractDataRecord, DataRecordPhysicalValueAlias, DecodedDataRecord
from .raw_data_record import RawDataRecord


class CustomFormulaDataRecord(AbstractDataRecord):
    def __init__(
            self,
            name: str,
            length: int,
            encode_function: Callable,
            decode_function: Callable,
            min_value: Optional[float] = None,
            max_value: Optional[float] = None,
            is_reoccurring: bool = False,
            min_occurrences: int = 1,
            max_occurrences: Optional[int] = None,
    ) -> None:
        super().__init__(name)
        self._length = length
        self._encode_function = encode_function
        self._decode_function = decode_function
        self._min_value = min_value
        self._max_value = max_value
        self._is_reoccurring = is_reoccurring
        self._min_occurrences = min_occurrences
        self._max_occurrences = max_occurrences

    @property
    def length(self) -> int:
        return self._length

    @property
    def is_reoccurring(self) -> bool:
        return self._is_reoccurring

    @property
    def min_occurrences(self) -> int:
        return self._min_occurrences

    @property
    def max_occurrences(self) -> Optional[int]:
        return self._max_occurrences

    @property
    def contains(self) -> Tuple["AbstractDataRecord", ...]:
        return ()

    def decode(self, raw_value: int) -> float:
        raw_value = super().decode(raw_value)
        return self._decode_function(raw_value)

    def encode(self, physical_value: float) -> int:
        physical_value = super().encode(physical_value)
        return self._encode_function(physical_value)


class LinearFormulaDataRecord(RawDataRecord):
    def __init__(
            self,
            name: str,
            length: int,
            factor: float,
            offset: float,
            min_value: Optional[float] = None,
            max_value: Optional[float] = None,
            is_reoccurring: bool = False,
            min_occurrences: int = 1,
            max_occurrences: Optional[int] = 1
    ) -> None:
        super().__init__(
            name=name,
        )
        self._length = length
        self._factor = factor
        self._offset = offset
        self._min_value = min_value
        self._max_value = max_value
        self._is_reoccurring = is_reoccurring
        self._min_occurrences = min_occurrences
        self._max_occurrences = max_occurrences

    @property
    def length(self) -> int:
        return self._length

    @property
    def is_reoccurring(self) -> bool:
        return self._is_reoccurring

    @property
    def min_occurrences(self) -> int:
        return self._min_occurrences

    @property
    def max_occurrences(self) -> Optional[int]:
        return self._max_occurrences

    @property
    def contains(self) -> Tuple["AbstractDataRecord", ...]:
        return ()

    def decode(self, raw_value: int) -> DecodedDataRecord:
        decoded_data_record: DecodedDataRecord = super().decode(raw_value)
        physical_value = (decoded_data_record.raw_value / self._factor) + self._offset
        if (self._min_value is not None and physical_value < self._min_value) or \
                (self._max_value is not None and physical_value > self._max_value):
            raise ValueError("Decoded physical value out of expected range.")
        decoded_data_record.physical_value = physical_value
        return decoded_data_record

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:
        physical_value = super().encode(physical_value)
        if (self._min_value is not None and physical_value < self._min_value) or \
                (self._max_value is not None and physical_value > self._max_value):
            raise ValueError("Provided physical value is out of expected range.")
        raw_value = int((physical_value - self._offset) * self._factor)
        return raw_value

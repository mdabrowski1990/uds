"""Definition of FormulaDataRecord."""

from dataclasses import dataclass
from typing import Callable, Optional, Union

from .abstract_data_record import DataRecordPhysicalValueAlias, DecodedDataRecord
from .raw_data_record import RawDataRecord


@dataclass
class FormulaRange:
    min_value: int
    max_value: int

    def __post_init__(self):
        if not isinstance(self.min_value, int) or not isinstance(self.max_value, int):
            raise TypeError("Attributes 'min_value' and 'max_value' must be integers.")
        if self.min_value > self.max_value:
            raise ValueError("Attribute 'min_value' must be less than 'max_value'.")


class CustomFormulaDataRecord(RawDataRecord):
    def __init__(
            self,
            name: str,
            length: int,
            decode_formula: Callable,
            encode_formula: Callable,
            formula_range: Optional[FormulaRange] = None
    ) -> None:
        super().__init__(name=name, length=length)

        if not callable(decode_formula):
            raise TypeError("Provided 'decode_formula' is not callable.")
        if not callable(encode_formula):
            raise TypeError("Provided 'encode_formula' is not callable.")
        if formula_range is not None and not isinstance(formula_range, FormulaRange):
            raise TypeError(
                "Parameter 'formula_range' must be type of 'FormulaRange', "
                f"provided type: '{type(formula_range).__name__}'."
            )
        self.decode_formula = decode_formula
        self.encode_formula = encode_formula
        self.formula_range = formula_range

    def decode(self, raw_value: int) -> Union[int, DecodedDataRecord]:
        decoded_data: DecodedDataRecord = super().decode(raw_value)
        if self.formula_range and self.formula_range.min_value < decoded_data.raw_value < self.formula_range.max_value:
            decoded_data.physical_value = self.decode_formula(decoded_data.raw_value)
        return decoded_data

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:
        encoded_data: int = super().encode(physical_value)
        if self.formula_range and self.formula_range.min_value < encoded_data < self.formula_range.max_value:
            return self.encode_formula(encoded_data)
        return int(encoded_data)


class LinearFormulaDataRecord(RawDataRecord):

    def __init__(
            self,
            name: str,
            length: int,
            factor: float,
            offset: float,
    ) -> None:
        super().__init__(
            name=name,
            length=length,
        )
        self._decode_formula = lambda x: (x / factor) + offset
        self._encode_formula = lambda x: (x - offset) * factor

    def decode(self, raw_value: int) -> Union[int, DecodedDataRecord]:
        decoded_data: DecodedDataRecord = super().decode(raw_value)
        decoded_data.physical_value = self._decode_formula(decoded_data.raw_value)
        return decoded_data

    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:
        encoded_data: int = super().encode(physical_value)
        return int(self._encode_formula(encoded_data))

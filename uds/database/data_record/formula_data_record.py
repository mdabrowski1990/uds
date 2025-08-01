from typing import Callable, Union, Optional

from .abstract_data_record import AbstractDataRecord, SinglePhysicalValueAlias


AliasPhysicalValueEncodingFormula = Union[Callable[[int], int], Callable[[float], int]]
AliasPhysicalValueDecodingFormula = Union[Callable[[int], float], Callable[[int], int]]


class FormulaDataRecord(AbstractDataRecord):

    def __init__(self,
                 name: str,
                 length: int,
                 encoding_formula: AliasPhysicalValueEncodingFormula,
                 decoding_formula: AliasPhysicalValueDecodingFormula,
                 min_occurrences: int,
                 max_occurrences: Optional[int]) -> None:
        ...

    @property
    def encoding_formula(self) -> AliasPhysicalValueEncodingFormula:
        ...

    @property
    def decoding_formula(self) -> AliasPhysicalValueDecodingFormula:
        ...

    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        return self.decoding_formula(raw_value)

    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        return self.encoding_formula(physical_value)


class LinearFormulaDataRecord(FormulaDataRecord):

    def __init__(self,
                 name: str,
                 length: int,
                 factor: Union[float, int],
                 offset: Union[float, int],
                 min_occurrences: int,
                 max_occurrences: Optional[int]) -> None:
        self.decoding_formula = lambda raw_value: factor*raw_value + offset
        self.encoding_formula = lambda physical_value: int(round((physical_value - offset) / factor, 0))

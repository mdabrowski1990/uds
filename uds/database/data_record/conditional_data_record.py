from typing import Dict, Callable, Sequence
from abc import ABC, abstractmethod
from .abstract_data_record import AbstractDataRecord


class AbstractConditionalDataRecord(ABC):
    """
    API definition of conditional Data Records.

    Features:
     - Contains logic with diagnostic message continuation after previous value was revealed.

    Common Use Cases:
     - Selectors of DID structures after DID is provided
     - Selectors of diagnostic request/response continuation after subfunction value is provided
     - Extracting length value for following parameters (e.g. from addressAndLengthFormatIdentifier)
    """

    @abstractmethod
    def get(self, raw_value) -> Sequence[AbstractDataRecord]:
        """
        Get Data Record with diagnostic message continuation.

        :param raw_value: Raw value of the proceeding Data Record.

        :return:
        """



class ConditionalMappingDataRecord:

    def __init__(self, values_mapping: Dict[int, Sequence[AbstractDataRecord]]) -> None:
        self.values_mapping = values_mapping

    def get(self, raw_value) -> Sequence[AbstractDataRecord]:
        return self.values_mapping[raw_value]


class ConditionalFormulaDataRecord:

    def __init__(self, formula: Callable[[int], Sequence[AbstractDataRecord]]) -> None:
        self.formula = formula

    def get(self, raw_value) -> Sequence[AbstractDataRecord]:
        return self.formula(raw_value)

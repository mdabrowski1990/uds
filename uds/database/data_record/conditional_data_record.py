from typing import Dict, Callable, Sequence, Mapping, Optional, Tuple
from abc import ABC, abstractmethod
from .abstract_data_record import AbstractDataRecord
from uds.utilities import InconsistentArgumentsError


class AbstractConditionalDataRecord(ABC):
    """
    API definition of conditional Data Records.

    Features:
     - Conditional Data Records are placeholders that would be replaced with other Data Records the value of
       the previous Data Record is revealed.
     - Contains logic of diagnostic message continuation building.
    """

    AliasMessageContinuation = Sequence[AbstractDataRecord]

    def __init__(self, default_message_continuation: Optional[AliasMessageContinuation] = None) -> None:
        self.default_message_continuation = default_message_continuation

    @property
    def default_message_continuation(self) -> Optional[AliasMessageContinuation]:
        return self.__default_message_continuation

    @default_message_continuation.setter
    def default_message_continuation(self, value: Optional[AliasMessageContinuation]) -> None:
        if value is None:
            self.__default_message_continuation = None
        self.validate_message_continuation(value)
        self.__default_message_continuation = tuple(value)

    @staticmethod
    def validate_message_continuation(value: AliasMessageContinuation) -> None:
        """
        Validate whether the provided value is structure of diagnostic message continuation.

        :param value: Value to check

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: At least one element of the provided sequence is not an instance of AbstractDataRecord class.
        :raise InconsistentArgumentsError: The total length of the Data Records does not add up to full bytes.
        """
        if not isinstance(value, Sequence):
            raise TypeError("Provided value is not a sequence")
        if not all(isinstance(element, AbstractDataRecord) for element in value):
            raise ValueError("At least one element is not an instance of AbstractDataRecord class.")
        total_length = sum([element.length for element in value])
        if total_length % 8 != 0:
            raise InconsistentArgumentsError("The total length of the Data Records does not add up to full bytes.")

    @abstractmethod
    def get(self, raw_value: int) -> AliasMessageContinuation:
        """
        Get Data Record with diagnostic message continuation.

        :param raw_value: Raw value of the proceeding Data Record.

        :return: Following Data Records for the revealed value of the proceeding Data Record.
        """


class ConditionalMappingDataRecord(AbstractConditionalDataRecord):
    """
    Conditional Data Records that uses mapping to select diagnostic message continuation.

    Common Use Cases:
     - DID structure selection after DID value is provided
     - selection of diagnostic message selection after sub-function value is provided
    """

    def __init__(self,
                 raw_values_mapping: Mapping[int, Sequence[AbstractDataRecord]],
                 default_message_continuation: Optional[AbstractConditionalDataRecord.AliasMessageContinuation] = None
                 ) -> None:
        """
        Define logic for this Conditional Data Record.

        :param raw_values_mapping: Mapping from raw values of the proceeding Data Record to structures of
            the diagnostic message continuation.
        """
        self.raw_values_mapping = raw_values_mapping
        super().__init__(default_message_continuation=default_message_continuation)

    @property
    def raw_values_mapping(self) -> Mapping[int, Sequence[AbstractDataRecord]]:
        """Get the mapping with diagnostic message continuation selection."""
        return self.__raw_values_mapping

    @raw_values_mapping.setter
    def raw_values_mapping(self, raw_values_mapping: Mapping[int, Sequence[AbstractDataRecord]]) -> None:
        """
        Set the mapping for diagnostic message continuation selection.

        :param raw_values_mapping: Mapping from raw values of the proceeding Data Record to structures of
            the diagnostic message continuation.

        :raise TypeError: Provided value is not a mapping type.
        :raise ValueError:
        """
        if not isinstance(raw_values_mapping, Mapping):
            raise TypeError("Provided value is not a mapping type.")
        keys = set(raw_values_mapping.keys())

    def get(self, raw_value) -> Sequence[AbstractDataRecord]:
        return self.values_mapping[raw_value]


class ConditionalFormulaDataRecord(AbstractConditionalDataRecord):
    """
    Conditional Data Records that uses formula to generate diagnostic message continuation.

    Common Use Cases:
     - Extracting length value for following parameters (e.g. from addressAndLengthFormatIdentifier)
    """

    def __init__(self,
                 formula: Callable[[int], Sequence[AbstractDataRecord]],
                 default_message_continuation: Optional[AbstractConditionalDataRecord.AliasMessageContinuation] = None
                 ) -> None:
        self.formula = formula
        super().__init__(default_message_continuation=default_message_continuation)

    def get(self, raw_value) -> Sequence[AbstractDataRecord]:
        return self.formula(raw_value)

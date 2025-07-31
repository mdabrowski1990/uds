__all__ = ["DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION",
           "AbstractConditionalDataRecord", "ConditionalMappingDataRecord", "ConditionalFormulaDataRecord"]

from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Callable, Mapping, Optional, Sequence

from uds.utilities import InconsistentArgumentsError

from .abstract_data_record import AbstractDataRecord
from .raw_data_record import RawDataRecord

AliasMessageContinuation = Sequence[AbstractDataRecord]
"""Alias of Diagnostic Message Continuation used by 
:class:`~uds.database.data_record.conditional_data_record.AbstractConditionalDataRecord`"""
DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION: AliasMessageContinuation = [
    RawDataRecord(name="Generic Diagnostic Message Continuation",
                  length=8,
                  min_occurrences=0,
                  max_occurrences=None)
]
"""Generic Diagnostic Message Continuation that can be used when specific information are not available."""


class AbstractConditionalDataRecord(ABC):
    """
    API definition of conditional Data Records.

    Features:
     - Conditional Data Records are placeholders that would be replaced with other Data Records the value of
       the previous Data Record is revealed.
     - Contains logic of diagnostic message continuation building.
    """

    def __init__(self, default_message_continuation: Optional[AliasMessageContinuation]) -> None:
        """
        Initialize the common part for all Conditional Data Records.

        :param default_message_continuation: Value of default message continuation.
            Leave None if you do not wish to use default message continuation.
        """
        self.default_message_continuation = default_message_continuation

    @abstractmethod
    def __getitem__(self, raw_value: int) -> AliasMessageContinuation:
        """
        Get Data Record with diagnostic message continuation.

        :param raw_value: Raw value of the proceeding Data Record.

        :raise KeyError: Provided raw value cannot be handled.

        :return: Following Data Records for the revealed value of the proceeding Data Record.
        """

    @property
    def default_message_continuation(self) -> Optional[AliasMessageContinuation]:
        """
        Get default diagnostic message continuation.

        The default diagnostic message continuation would be used when specific diagnostic message continuation is not
        defined.

        .. note:: None value of default_message_continuation means the default value behavior is turned off.
        """
        return self.__default_message_continuation

    @default_message_continuation.setter
    def default_message_continuation(self, value: Optional[AliasMessageContinuation]) -> None:
        """
        Set default diagnostic message continuation.

        :param value: Value to set.

        :return: Value to be used as default diagnostic message continuation when no specific
        """
        if value is None:
            self.__default_message_continuation = None
        else:
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

    def get_message_continuation(self, raw_value: int) -> AliasMessageContinuation:
        """
        Get Data Record with diagnostic message continuation.

        :param raw_value: Raw value of the proceeding Data Record.

        :raise ValueError: Diagnostic message continuation could not be assessed for the provided raw value.

        :return: Following Data Records for the revealed value of the proceeding Data Record.
        """
        try:
            return self.__getitem__(raw_value)
        except KeyError:
            if self.default_message_continuation is None:
                raise ValueError("No handler for the provided raw value.")
            return self.default_message_continuation


class ConditionalMappingDataRecord(AbstractConditionalDataRecord):
    """
    Conditional Data Records that uses mapping to select diagnostic message continuation.

    Common Use Cases:
     - DID structure selection after DID value is provided
     - selection of diagnostic message selection after sub-function value is provided
    """

    def __init__(self,
                 raw_values_mapping: Mapping[int, Sequence[AbstractDataRecord]],
                 default_message_continuation: Optional[AliasMessageContinuation] = None) -> None:
        """
        Define logic for this Conditional Data Record.

        :param raw_values_mapping: Mapping from raw values of the proceeding Data Record to structures of
            the diagnostic message continuation.
        :param default_message_continuation: Value of default message continuation.
            Leave None if you do not wish to use default message continuation.
        """
        self.raw_values_mapping = raw_values_mapping
        super().__init__(default_message_continuation=default_message_continuation)

    def __getitem__(self, raw_value: int) -> Sequence[AbstractDataRecord]:
        """
        Get diagnostic message continuation for given raw value based on mapping only.

        :param raw_value: Raw value of the proceeding Data Record.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is less than 0.

        :return: Diagnostic message continuation assessed based on mapping only.
        """
        if not isinstance(raw_value, int):
            raise TypeError("Provided value is not int type.")
        if raw_value < 0:
            raise ValueError("Provided value is not a raw value as it is lower than 0.")
        return self.raw_values_mapping[raw_value]

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
        :raise ValueError: Keys in the provided mapping are not raw values only.
        """
        if not isinstance(raw_values_mapping, Mapping):
            raise TypeError("Provided value is not a mapping type.")
        keys = set(raw_values_mapping.keys())
        if not all(isinstance(key, int) and key >= 0 for key in keys):
            raise ValueError("At least one key in the provided mapping is not a raw value.")
        for value in raw_values_mapping.values():
            self.validate_message_continuation(value)
        self.__raw_values_mapping = MappingProxyType(raw_values_mapping)


class ConditionalFormulaDataRecord(AbstractConditionalDataRecord):
    """
    Conditional Data Records that uses formula to generate diagnostic message continuation.

    Common Use Cases:
     - Extracting length value for following parameters (e.g. from addressAndLengthFormatIdentifier)
    """

    def __init__(self,
                 formula: Callable[[int], Sequence[AbstractDataRecord]],
                 default_message_continuation: Optional[AliasMessageContinuation] = None) -> None:
        """
        Define logic for this Conditional Data Record.

        :param formula: Formula used for assessing structure of diagnostic message continuation.
        :param default_message_continuation: Value of default message continuation.
            Leave None if you do not wish to use default message continuation.
        """
        self.formula = formula
        super().__init__(default_message_continuation=default_message_continuation)

    def __getitem__(self, raw_value: int) -> Sequence[AbstractDataRecord]:
        return self.formula(raw_value)

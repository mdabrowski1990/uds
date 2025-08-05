"""Conditional Data Records implementation."""

__all__ = ["DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION", "AliasMessageStructure",
           "AbstractConditionalDataRecord", "ConditionalMappingDataRecord", "ConditionalFormulaDataRecord"]

from abc import ABC, abstractmethod
from inspect import signature
from operator import getitem
from types import MappingProxyType
from typing import Callable, Mapping, Optional, Sequence, Union

from uds.utilities import InconsistentArgumentsError

from .abstract_data_record import AbstractDataRecord
from .raw_data_record import RawDataRecord

AliasMessageStructure = Sequence[Union[AbstractDataRecord, "AbstractConditionalDataRecord"]]
"""Alias of Diagnostic Message Structure used by databases to interpret Diagnostic Messages parameters.

The sequence shall contain `AbstractDataRecord` instances with up to one `AbstractConditionalDataRecord` instance
at the end.
No more than 1 reoccurring Data Record is allowed.
Total length shall always be divisible by 8.
"""
DEFAULT_DIAGNOSTIC_MESSAGE_CONTINUATION: AliasMessageStructure = (
    RawDataRecord(name="Generic Diagnostic Message Continuation",
                  length=8,
                  min_occurrences=0,
                  max_occurrences=None),
)
"""Generic Diagnostic Message Continuation that can be used when specific information are not available."""


class AbstractConditionalDataRecord(ABC):
    """
    API definition of conditional Data Records.

    Features:
     - Conditional Data Records are placeholders that would be replaced with other Data Records the value of
       the previous Data Record is revealed.
     - Contains logic of diagnostic message continuation building.
    """

    def __init__(self, default_message_continuation: Optional[AliasMessageStructure]) -> None:
        """
        Initialize the common part for all Conditional Data Records.

        :param default_message_continuation: Value of default message continuation.
            Leave None if you do not wish to use default message continuation.
        """
        self.default_message_continuation = default_message_continuation

    @abstractmethod
    def __getitem__(self, raw_value: int) -> AliasMessageStructure:
        """
        Get Data Record with diagnostic message continuation.

        :param raw_value: Raw value of the proceeding Data Record.

        :raise KeyError: Provided raw value cannot be handled.

        :return: Following Data Records for the revealed value of the proceeding Data Record.
        """

    @property
    def default_message_continuation(self) -> Optional[AliasMessageStructure]:
        """
        Get default diagnostic message continuation.

        The default diagnostic message continuation would be used when specific diagnostic message continuation is not
        defined.

        .. note:: None value of default_message_continuation means the default value behavior is turned off.
        """
        return self.__default_message_continuation

    @default_message_continuation.setter
    def default_message_continuation(self, value: Optional[AliasMessageStructure]) -> None:
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
    def validate_message_continuation(value: AliasMessageStructure) -> None:
        """
        Validate whether the provided value is structure of diagnostic message continuation.

        :param value: Value to check

        :raise TypeError: Provided value is not a sequence.
        :raise ValueError: Provided sequence does not contain Data Records, or they are incorrectly ordered.
        :raise InconsistentArgumentsError: Contained Data Records cannot be used together.
        """
        if not isinstance(value, Sequence):
            raise TypeError("Provided value is not a sequence")
        names = set()
        min_total_length = 0
        max_total_length = 0
        for i, data_record in enumerate(value):
            if isinstance(data_record, AbstractDataRecord):
                if data_record.name in names:
                    raise InconsistentArgumentsError("Data Records within one message have to have unique names. "
                                                     f"Multiple `{data_record.name}` found.")
                else:
                    names.add(data_record.name)
                if not data_record.fixed_total_length:
                    if i != len(value) - 1:
                        raise ValueError("Data record with varying length can only be placed at the end of "
                                         "the message structure.")
                min_total_length += data_record.length * data_record.min_occurrences
                if data_record.max_occurrences is not None:
                    max_total_length += data_record.length * data_record.max_occurrences
            elif isinstance(data_record, AbstractConditionalDataRecord):
                if i != len(value) - 1:
                    raise ValueError("Conditional Data Record can only be placed at the end of the message structure.")
                if i == 0:
                    raise ValueError("Conditional Data Record cannot be the only part of the message structure.")
            else:
                raise ValueError("Provided sequence contains an element which is not a Data Record.")
        if min_total_length % 8 != 0 or max_total_length % 8:
            raise InconsistentArgumentsError("Total length of diagnostic message continuation must always be divisible "
                                             "by 8.")

    def get_message_continuation(self, raw_value: int) -> AliasMessageStructure:
        """
        Get Data Record with diagnostic message continuation.

        :param raw_value: Raw value of the proceeding Data Record.

        :raise ValueError: Diagnostic message continuation could not be assessed for the provided raw value.

        :return: Following Data Records for the revealed value of the proceeding Data Record.
        """
        try:
            return getitem(self, raw_value)
        except (KeyError, ValueError) as error:
            if self.default_message_continuation is None:
                raise ValueError("No handler for the provided raw value.") from error
            return self.default_message_continuation


class ConditionalMappingDataRecord(AbstractConditionalDataRecord):
    """
    Conditional Data Records that uses mapping to select diagnostic message continuation.

    Common Use Cases:
     - DID structure selection after DID value is provided
     - selection of diagnostic message selection after sub-function value is provided
    """

    def __init__(self,
                 mapping: Mapping[int, AliasMessageStructure],
                 default_message_continuation: Optional[AliasMessageStructure] = None) -> None:
        """
        Define logic for this Conditional Data Record.

        :param mapping: Mapping from raw values of the proceeding Data Record to structures of the diagnostic message
            continuation.
        :param default_message_continuation: Value of default message continuation.
            Leave None if you do not wish to use default message continuation.
        """
        self.mapping = mapping
        super().__init__(default_message_continuation=default_message_continuation)

    def __getitem__(self, raw_value: int) -> AliasMessageStructure:
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
        return self.mapping[raw_value]

    @property
    def mapping(self) -> Mapping[int, AliasMessageStructure]:
        """Get the mapping with diagnostic message continuation selection."""
        return self.__mapping

    @mapping.setter
    def mapping(self, mapping: Mapping[int, AliasMessageStructure]) -> None:
        """
        Set the mapping for diagnostic message continuation selection.

        :param mapping: Mapping from raw values of the proceeding Data Record to structures with the diagnostic message
            continuation.

        :raise TypeError: Provided value is not a Mapping type.
        :raise ValueError: Keys in the provided mapping are not raw values only.
        """
        if not isinstance(mapping, Mapping):
            raise TypeError("Provided value is not a mapping type.")
        keys = set(mapping.keys())
        if not all(isinstance(key, int) and key >= 0 for key in keys):
            raise ValueError("At least one key in the provided mapping is not a raw value.")
        for value in mapping.values():
            self.validate_message_continuation(value)
        self.__mapping = MappingProxyType(mapping)


class ConditionalFormulaDataRecord(AbstractConditionalDataRecord):
    """
    Conditional Data Records that uses formula to generate diagnostic message continuation.

    Common Use Cases:
     - Extracting length value for following parameters (e.g. from addressAndLengthFormatIdentifier)
    """

    def __init__(self,
                 formula: Callable[[int], AliasMessageStructure],
                 default_message_continuation: Optional[AliasMessageStructure] = None) -> None:
        """
        Define logic for this Conditional Data Record.

        :param formula: Formula to use for assessing the structure of a diagnostic message continuation.
        :param default_message_continuation: Value of default message continuation.
            Leave None if you do not wish to use default message continuation.
        """
        self.formula = formula
        super().__init__(default_message_continuation=default_message_continuation)

    def __getitem__(self, raw_value: int) -> AliasMessageStructure:
        """
        Get diagnostic message continuation for given raw value based on formula only.

        :param raw_value: Raw value of the proceeding Data Record.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is less than 0.

        :return: Diagnostic message continuation assessed based on formula only.
        """
        if not isinstance(raw_value, int):
            raise TypeError("Provided value is not int type.")
        if raw_value < 0:
            raise ValueError("Provided value is not a raw value as it is lower than 0.")
        return self.formula(raw_value)

    @property
    def formula(self) -> Callable[[int], AliasMessageStructure]:
        """Get the formula for assessing the structure of diagnostic message continuation."""
        return self.__formula

    @formula.setter
    def formula(self, formula: Callable[[int], AliasMessageStructure]) -> None:
        """
        Set the formula for assessing the structure of diagnostic message continuation.

        :param formula: Formula to use for assessing the structure of a diagnostic message continuation.

        :raise TypeError: Provided value is not callable.
        :raise ValueError: Provided formula's signature or annotation does not match the required format.
        """
        if not callable(formula):
            raise TypeError("Provided value is not callable.")
        formula_signature = signature(formula)
        if len(formula_signature.parameters) != 1:
            raise ValueError("Provided formula does not take exactly one parameter.")
        param_annotation = list(formula_signature.parameters.items())[0][-1].annotation
        if param_annotation != formula_signature.empty and not issubclass(param_annotation, int):
            raise ValueError("Formula's annotation suggests the formula does not take raw value as an argument.")
        self.__formula = formula

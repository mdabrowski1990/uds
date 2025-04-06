"""Definitions of CustomFormulaDataRecord and LinearFormulaDataRecord."""

from dataclasses import dataclass
from typing import Callable, Optional, Union, Tuple

from .abstract_data_record import AbstractDataRecord


@dataclass
class FormulaRange:
    min_value: int
    max_value: int

    def __post_init__(self):
        if not isinstance(self.min_value, int) or not isinstance(self.max_value, int):
            raise TypeError("Attributes 'min_value' and 'max_value' must be integers.")
        if self.min_value > self.max_value:
            raise ValueError("Attribute 'min_value' must be less than 'max_value'.")


class CustomFormulaDataRecord(AbstractDataRecord):
    def __init__(
            self,
            name: str,
            length: int,
            decode_formula: Callable,
            encode_formula: Callable,
            formula_range: Optional[FormulaRange] = None
    ) -> None:
        super().__init__(name=name)

        if not callable(decode_formula):
            raise TypeError("Provided 'decode_formula' is not callable.")
        if not callable(encode_formula):
            raise TypeError("Provided 'encode_formula' is not callable.")
        if formula_range is not None and not isinstance(formula_range, FormulaRange):
            raise TypeError(
                "Parameter 'formula_range' must be type of 'FormulaRange', "
                f"provided type: '{type(formula_range).__name__}'."
            )
        self.length = length
        self.decode_formula = decode_formula
        self.encode_formula = encode_formula
        self.formula_range = formula_range or FormulaRange(min_value=0, max_value=self.max_raw_value)

    # TODO: Should we move the length setter to AbstractDataRecord? Maybe even set values of some other properties?
    @property
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""
        return self.__length

    @length.setter
    def length(self, value: int) -> None:
        """
        Set the length, ensuring it's an integer and within an acceptable range.

        :param value: Number of bits that this Data Record is stored over.

        :raise TypeError: Provided value is not int type.
        :raise ValueError: Provided value is less or equal 0.
        """
        if not isinstance(value, int):
            raise TypeError("Length must be an integer.")
        if value <= 0:
            raise ValueError("Length must be a positive integer.")
        self.__length = value

    @property  # noqa: F841
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """
        return False

    @property  # noqa: F841
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.data_record.raw_data_record.RawDataRecord.is_reoccurring`
            equals True.
        """
        return 1

    @property  # noqa: F841
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.data_record.raw_data_record.RawDataRecord.is_reoccurring`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """
        return 1

    @property  # noqa: F841
    def contains(self) -> Tuple[AbstractDataRecord, ...]:
        """Get Data Records contained by this Data Record."""
        return ()

    def decode(self, raw_value: int) -> Union[int, float]:
        """
        Decode the physical value of the given `raw_value` using the decode formula provided by the user.

        :param raw_value: Raw value to be decoded.

        :return: Physical value decoded with custom decode formula.

        :raises ValueError: Provided `raw_value` is out of range.
        """
        # TODO: Should we implement all the validation, or should we leave it to the user?
        if not self.formula_range.min_value <= raw_value <= self.formula_range.max_value:
            raise ValueError("Provided raw_value parameter is out of range: "
                             f"must be between {self.formula_range.min_value} "
                             f"and {self.formula_range.max_value}, got {raw_value}.")
        return self.decode_formula(raw_value)

    def encode(self, physical_value: Union[int, float]) -> int:
        """
        Encode the raw value of the given `physical_value` using the encode formula provided by the user.

        :param physical_value: Physical value to be encoded.

        :return: Raw value encoded with custom encode formula.

        :raises ValueError: Encoded `raw_value` of provided `physical_value` is out of range.
        """
        raw_value = self.encode_formula(physical_value)
        # TODO: Do I think correctly that FormulaRange should refer only to raw_value?
        if not self.formula_range.min_value <= raw_value <= self.formula_range.max_value:
            raise ValueError("Encoded raw_value is out of configured formula_range: "
                             f"must be between {self.formula_range.min_value} "
                             f"and {self.formula_range.max_value}, got {raw_value}.")
        return raw_value


class LinearFormulaDataRecord(CustomFormulaDataRecord):

    def __init__(
            self,
            name: str,
            length: int,
            factor: float,
            offset: float,
            formula_range: FormulaRange = None,
    ) -> None:
        self._decode_formula = lambda x: (x / factor) + offset
        self._encode_formula = lambda x: (x - offset) * factor
        super().__init__(
            name=name,
            length=length,
            decode_formula=self._decode_formula,
            encode_formula=self._encode_formula,
            formula_range=formula_range
        )

    def decode(self, raw_value: int) -> Union[int, float]:
        """
        Decode the physical value of the given `raw_value` using the linear decode formula.

        :param raw_value: Raw value to be decoded.

        :return: Physical value decoded with linear decode formula.

        :raises TypeError: Provided `raw_value` is not int type.
        :raises ValueError: Provided `raw_value` is out of range.
        """
        if not isinstance(raw_value, int):
            raise TypeError(f"Expected raw_value to be an int type, got '{type(raw_value).__name__}' instead.")
        return super().decode(raw_value)

    def encode(self, physical_value: Union[int, float]) -> int:
        """
        Encode the raw value of the given `physical_value` using the linear encode formula.

        :param physical_value: Physical value to be encoded.

        :return: Raw value encoded with linear encode formula.

        :raises TypeError: Provided `physical_value` is not int type.
        :raises ValueError: Encoded `raw_value` of provided `physical_value` is out of range.
        """
        if not isinstance(physical_value, int):
            raise TypeError(
                f"Expected physical_value to be an int type, got '{type(physical_value).__name__}' instead."
            )
        return super().encode(physical_value)

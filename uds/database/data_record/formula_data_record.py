"""Formula Data Records implementation."""

__all__ = ["CustomFormulaDataRecord", "LinearFormulaDataRecord"]

from typing import Callable, Union, Optional

from .abstract_data_record import AbstractDataRecord, SinglePhysicalValueAlias


AliasPhysicalValueEncodingFormula = Union[Callable[[int], int], Callable[[float], int]]
"""Type alias for encoding formulas that convert physical values to raw values."""
AliasPhysicalValueDecodingFormula = Union[Callable[[int], float], Callable[[int], int]]
"""Type alias for decoding formulas that convert raw values to physical values."""


class CustomFormulaDataRecord(AbstractDataRecord):
    """
    Data Record that uses user defined mathematical formulas for value conversion.

    FormulaDataRecord provides flexible value translation using custom mathematical formulas,
    ideal for complex calculations.

    Features:
     - Custom encoding/decoding formulas: user-defined mathematical transformations
     - Type flexibility: supports both integer and floating-point calculations

    Common Use Cases:
     - Sensor measurements with non-linear conversion formulas
     - Mathematical transformations for proprietary data formats

    .. warning:: The encoding formula must be the mathematical inverse of the decoding formula to ensure proper
        bidirectional conversion.
        Encoding and decoding formulas compatibility is not performed - it is user's responsibility to make sure
        the formulas are working correctly.

    .. seealso:: :class:`~uds.database.data_record.formula_data_record.LinearFormulaDataRecord` for simple linear
        transformations.
    """

    def __init__(self,
                 name: str,
                 length: int,
                 encoding_formula: AliasPhysicalValueEncodingFormula,
                 decoding_formula: AliasPhysicalValueDecodingFormula,
                 min_occurrences: int = 1,
                 max_occurrences: Optional[int] = 1) -> None:
        """
        Configure custom formula Data Record.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param encoding_formula: Convertion function that transforms physical values into raw values.
        :param decoding_formula: Convertion function that transforms raw values into physical values.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        """
        super().__init__(name=name,
                         length=length,
                         children=tuple(),
                         min_occurrences=min_occurrences,
                         max_occurrences=max_occurrences)
        self.encoding_formula = encoding_formula
        self.decoding_formula = decoding_formula

    @property
    def encoding_formula(self) -> AliasPhysicalValueEncodingFormula:
        """Get the encoding formula for converting physical values into raw values."""
        return self.__encoding_formula

    @encoding_formula.setter
    def encoding_formula(self, value: AliasPhysicalValueEncodingFormula) -> None:
        """
        Set the encoding formula that will be used for converting physical values into raw values.

        :param value: Formula to set.

        :raises TypeError: Provided value is not callable.
        """
        if not callable(value):
            raise TypeError("Encoding formula must be callable.")
        self.__encoding_formula = value

    @property
    def decoding_formula(self) -> AliasPhysicalValueDecodingFormula:
        """Get the decoding formula for converting raw values into physical values."""
        return self.__decoding_formula

    @decoding_formula.setter
    def decoding_formula(self, value: AliasPhysicalValueDecodingFormula) -> None:
        """
        Set the decoding formula that will be used for converting raw values into physical values.

        :param value: Formula to set.

        :raises TypeError: Provided value is not callable.
        """
        if not callable(value):
            raise TypeError("Decoding formula must be callable.")
        self.__decoding_formula = value

    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Get physical value representing provided raw value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Physical value for this occurrence that was assessed using decoding formula.
        """
        self._validate_raw_value(raw_value)
        return self.decoding_formula(raw_value)

    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        """
        Get raw value that represents provided physical value.

        :param physical_value: Physical value of this Data Record single occurrence.

        :return: Raw Value for this occurrence that was assessed using encoding formula.
        """
        return self.encoding_formula(physical_value)


class LinearFormulaDataRecord(AbstractDataRecord):
    """
    Data Record for linear mathematical transformations.

    LinearFormulaDataRecord provides simple linear scaling and offset transformations that is the most common type of
    sensor data conversion.

    Features:
     - Linear transformation: [physical value] = [factor] * [raw value] + [offset]
     - Automatic formula generation: encoding/decoding formulas created automatically
     - Integer rounding: encoding results are rounded to nearest integer
     - Type safety: ensures proper numeric types for factor and offset

    Common Use Cases:
     - Temperature sensors (e.g., factor=0.1, offset=-40 for tenths of degrees with -40°C offset)
     - Any sensor with linear calibration curve
     - Scaling from other units (e.g. ECU provides temperature in Fahrenheit, but you prefer them presented in Celsius)
     - Any scaling of linear values
    """

    def __init__(self,
                 name: str,
                 length: int,
                 factor: Union[float, int],
                 offset: Union[float, int],
                 min_occurrences: int = 1,
                 max_occurrences: Optional[int] = 1) -> None:
        """
        Configure Linear Formula Data Record.

        :param name: A name for this Data Record.
        :param length: Number of bits that are used to store a single occurrence of this Data Record.
        :param factor: Multiplication factor for the linear transformation.
        :param offset: Additive offset for the linear transformation.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        """
        self.factor = factor
        self.offset = offset
        super(AbstractDataRecord, self).__init__(name=name,
                                                 length=length,
                                                 children=tuple(),
                                                 min_occurrences=min_occurrences,
                                                 max_occurrences=max_occurrences)

    @property
    def factor(self) -> Union[float, int]:
        """Get the factor value for the linear transformation."""
        return self.__factor

    @factor.setter
    def factor(self, value: Union[float, int]) -> None:
        """
        Set the factor value for the linear transformation.

        :param value: Value to set.

        :raises TypeError: Provided value is not int or float type.
        :raises ValueError: Factor value must be unequal 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Factor value must be int or float type.")
        if value == 0:
            raise ValueError("Factor cannot be equal 0.")
        self.__factor = value

    @property
    def offset(self) -> Union[float, int]:
        """Get the offset value for the linear transformation."""
        return self.__offset

    @offset.setter
    def offset(self, value: Union[float, int]) -> None:
        """
        Set the offset value for the linear transformation.

        :param value: Value to set.

        :raises TypeError: Provided value is not int or float type.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Factor value must be int or float type.")
        self.__offset = value

    @property
    def min_physical_value(self) -> Union[float, int]:
        """Get the minimum physical value."""
        raw_value = self.min_raw_value if self.factor > 0 else self.max_raw_value
        return (raw_value * self.factor) + self.offset

    @property
    def max_physical_value(self) -> Union[float, int]:
        """Get the maximum physical value."""
        raw_value = self.max_raw_value if self.factor > 0 else self.min_raw_value
        return (raw_value * self.factor) + self.offset

    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Get physical value representing provided raw value.

        .. note:: Formula used: [physical value] = [factor] * [raw value] + [offset]

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Physical value for this occurrence that was assessed using linear transformation.
        """
        self._validate_raw_value(raw_value)
        return (raw_value * self.factor) + self.offset

    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        """
        Get raw value that represents provided physical value.

        .. note:: Formula used: [raw value] = ([physical value] - [offset]) / [factor]

        .. warning:: Rounding is used to find raw value that represents the closes physical value to the provided value.

        :param physical_value: Physical value of this Data Record single occurrence.

        :raises TypeError: Provided value is not int or float type.
        :raises ValueError: Provided value is out of range.

        :return: Raw Value for this occurrence that was assessed using linear transformation.
        """
        if not isinstance(physical_value, (int, float)):
            raise TypeError("Physical value must be int or float type.")
        raw_value = int(round((physical_value - self.offset) / self.factor, 0))
        if self.min_raw_value <= raw_value <= self.max_raw_value:
            return raw_value
        raise ValueError("Provided physical value is out of range.")

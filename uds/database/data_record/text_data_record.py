"""Text Data Record implementation."""

__all__ = ["TextDataRecord", "TextEncoding"]

from typing import Callable, Dict, Optional, TypedDict

from uds.utilities import ValidatedEnum

from .abstract_data_record import AbstractDataRecord, MultiplePhysicalValues, SinglePhysicalValueAlias


class TextEncoding(ValidatedEnum):
    """
    Text encoding types supported by TextDataRecord.

    This enum defines the available character encoding schemes for converting between raw integer values and
    their text character representations.
    """

    ASCII: "TextEncoding" = "ascii"  # type: ignore
    """Standard ASCII character encoding.
    
    .. seealso:: https://en.wikipedia.org/wiki/ASCII"""
    BCD: "TextEncoding" = "bcd"  # type: ignore
    """Binary Coded Decimal encoding.
    
    .. seealso:: `https://en.wikipedia.org/wiki/BCD_(character_encoding) 
        <https://en.wikipedia.org/wiki/BCD_(character_encoding)>`_"""


class TextDataRecord(AbstractDataRecord):
    """
    Data Record for encoding and decoding text characters with configurable encoding schemes.

    TextDataRecord provides bidirectional conversion between raw integer values and their text character
    representations using one of the predefined encodings (all supported encodings are defined in
    :class:`~uds.database.data_record.text_data_record.TextEncoding`).

    Common Use Cases:
     - Vehicle identification numbers (VIN) using ASCII encoding
     - Numeric displays and counters using BCD encoding
     - Part numbers and serial numbers in diagnostic data
    """

    def __init__(self,
                 name: str,
                 encoding: TextEncoding,
                 min_occurrences: int = 1,
                 max_occurrences: Optional[int] = None) -> None:
        """
        Configure Text Data Record.

        :param name: A name for this Data Record.
        :param encoding: Text encoding.
        :param min_occurrences: Minimal number of this Data Record occurrences.
        :param max_occurrences: Maximal number of this Data Record occurrences.
            Leave None if there is no limit (infinite number of occurrences).
        """
        self.encoding = encoding
        super().__init__(name=name,
                         length=self.__ENCODINGS[self.encoding]["length"],
                         children=tuple(),
                         min_occurrences=min_occurrences,
                         max_occurrences=max_occurrences)

    @staticmethod
    def __decode_ascii(character: str) -> int:
        """
        Decode ASCII character into byte value.

        :param character: ASCII character.

        :return: Raw value representation of this character in ASCII format.
        """
        if not isinstance(character, str):
            raise TypeError("Provided value is not str type.")
        if not character.isascii():
            raise ValueError("Provided value is non-ASCII character.")
        return ord(character)

    @property
    def encoding(self) -> TextEncoding:
        """Get Text Encoding."""
        return self.__encoding

    @encoding.setter
    def encoding(self, value: TextEncoding) -> None:
        """Set Text Encoding to use."""
        self.__encoding = TextEncoding.validate_member(value)

    @property
    def max_raw_value(self) -> int:
        """Maximum raw (bit) value for this Data Record."""
        if self.encoding == TextEncoding.ASCII:
            return 0x7F
        if self.encoding == TextEncoding.BCD:
            return 9
        raise NotImplementedError(f"Missing implementation for {self.encoding}.")

    def get_physical_values(self, *raw_values: int) -> MultiplePhysicalValues:
        """
        Get physical values representing provided raw values.

        :param raw_values: Raw (bit) values of this Data Record for multiple occurrences.

        :raise RuntimeError: A called was made on a Data Record that is not reoccurring.
        :raise ValueError: No values were provided.

        :return: Text encoded for provided raw values.
        """
        if not self.is_reoccurring:
            raise RuntimeError("This method must be called for reoccurring Data Record only.")
        if len(raw_values) == 0:
            raise ValueError("Raw value for at least one occurrence must be provided.")
        return "".join((self.get_physical_value(raw_value) for raw_value in raw_values))  # type: ignore

    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Get physical value representing provided raw value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: A single encoded text character.
        """
        self._validate_raw_value(raw_value)
        return self.__ENCODINGS[self.encoding]["encode"](raw_value)

    def get_raw_value(self, physical_value: SinglePhysicalValueAlias) -> int:
        """
        Get raw value that represents provided physical value.

        :param physical_value: A single character.

        :return: Raw value decoded from provided character.
        """
        return self.__ENCODINGS[self.encoding]["decode"](physical_value)  # type: ignore

    class _EncodingInfo(TypedDict):
        """Structure of Encoding Information."""

        length: int
        encode: Callable[[int], str]
        decode: Callable[[str], int]

    __ENCODINGS: Dict[TextEncoding, _EncodingInfo] = {
        TextEncoding.ASCII: {
            "length": 8,
            "encode": chr,
            "decode": __decode_ascii,
        },
        TextEncoding.BCD: {
            "length": 4,
            "encode": str,
            "decode": int,
        }
    }

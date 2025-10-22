"""Text Data Record implementation."""

__all__ = ["TextDataRecord", "TextEncoding"]

from typing import Callable, Dict, Optional, TypedDict

from uds.utilities import MAX_DTC_VALUE, ValidatedEnum, int_to_obd_dtc, obd_dtc_to_int

from .abstract_data_record import AbstractDataRecord


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
    """Binary Coded Decimal encoding (only digits 0-9).

    .. seealso:: `https://en.wikipedia.org/wiki/BCD_(character_encoding)
        <https://en.wikipedia.org/wiki/BCD_(character_encoding)>`_"""
    DTC_OBD_FORMAT: "TextEncoding" = "DTC in OBD format"  # type: ignore
    """:ref:`OBD DTC format <knowledge-base-dtc-obd-format>` encoding."""


def decode_ascii(character: str) -> int:
    """
    Decode ASCII character into byte value.

    :param character: ASCII character.

    :raise TypeError: Provided value is not str type.
    :raise ValueError: Provided value is not an ASCII character.

    :return: Raw value representation of this character in ASCII format.
    """
    if not isinstance(character, str):
        raise TypeError("Provided value is not str type.")
    if not character.isascii() or len(character) != 1:
        raise ValueError("Provided value is non-ASCII character.")
    return ord(character)


def decode_bcd(character: str) -> int:
    """
    Decode BCD character into nibble value.

    :param character: BCD character.

    :raise TypeError: Provided value is not str type.
    :raise ValueError: Provided value is not a BCD character.

    :return: Raw value representation of this character in BCD format.
    """
    if not isinstance(character, str):
        raise TypeError("Provided value is not str type.")
    if not character.isdecimal() or len(character) != 1:
        raise ValueError("Provided value is not a BCD character.")
    return int(character)


class TextDataRecord(AbstractDataRecord):
    """
    Data Record for encoding and decoding text characters with configurable encoding schemes.

    TextDataRecord provides bidirectional conversion between raw integer values and their text character
    representations using one of the predefined encodings (all supported encodings are defined in
    :class:`~uds.translator.data_record.text_data_record.TextEncoding`).

    Features:
     - Bidirectional mapping: raw value <-> text
     - Occurrence constraints: multiple occurrences are treated as longer text

    Common Use Cases:
     - Vehicle identification numbers (VIN) using ASCII encoding
     - Numeric displays and counters using BCD encoding
     - Part numbers and serial numbers in diagnostic data
    """

    class _EncodingInfo(TypedDict):
        """Structure of Encoding Information."""

        length: int
        encode: Callable[[int], str]  # noqa: vulture
        decode: Callable[[str], int]

    __ENCODINGS: Dict[TextEncoding, _EncodingInfo] = {
        TextEncoding.ASCII: _EncodingInfo(length=8, encode=chr, decode=decode_ascii),
        TextEncoding.BCD: _EncodingInfo(length=4, encode=str, decode=decode_bcd),
        TextEncoding.DTC_OBD_FORMAT: _EncodingInfo(length=24, encode=int_to_obd_dtc, decode=obd_dtc_to_int)
    }

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
        if self.encoding == TextEncoding.DTC_OBD_FORMAT:
            return MAX_DTC_VALUE
        raise NotImplementedError(f"Missing implementation for {self.encoding!r}.")

    def get_physical_values(self, *raw_values: int) -> str:
        """
        Get physical values representing provided raw values.

        :param raw_values: Raw (bit) values of this Data Record for multiple occurrences.

        :raise RuntimeError: A called was made on a Data Record that is not reoccurring.
        :raise ValueError: No values were provided.

        :return: Text encoded for provided raw values.
        """
        physical_values = super().get_physical_values(*raw_values)
        return "".join(physical_values)  # type: ignore

    def get_physical_value(self, raw_value: int) -> str:
        """
        Get physical value representing provided raw value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: A single encoded text character.
        """
        self._validate_raw_value(raw_value)
        return self.__ENCODINGS[self.encoding]["encode"](raw_value)

    def get_raw_value(self, physical_value: str) -> int:  # type: ignore
        """
        Get raw value that represents provided physical value.

        :param physical_value: A single character.

        :raise TypeError: Provided value is not str type.

        :return: Raw value decoded from provided character.
        """
        if not isinstance(physical_value, str):
            raise TypeError(f"Provided value is not str type. Actual type: {type(physical_value)}.")
        return self.__ENCODINGS[self.encoding]["decode"](physical_value)

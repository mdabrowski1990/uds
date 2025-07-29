"""Text Data Record implementation."""

__all__ = ["TextDataRecord", "TextEncoding"]

from typing import Any, Callable, Dict, Optional, Sequence, TypedDict

from uds.utilities import ValidatedEnum, validate_nibble

from .abstract_data_record import AbstractDataRecord, MultiplePhysicalValues, SinglePhysicalValueAlias


class TextEncoding(ValidatedEnum):
    """Encoding supported by Text Data Records."""

    ASCII: "TextEncoding" = "ascii"  # type: ignore
    BCD: "TextEncoding" = "bcd"  # type: ignore


class TextDataRecord(AbstractDataRecord):
    """Data Record that encodes text values."""

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
        return "".join((self.get_physical_value(raw_value) for raw_value in raw_values))

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
        return self.__ENCODINGS[self.encoding]["decode"](physical_value)


    class _EncodingInfo(TypedDict):
        """Structure of Encoding Information."""

        length: int
        encode: Callable[[int], str]
        decode: Callable[[str], int]

    __ENCODINGS: Dict[TextEncoding, _EncodingInfo] = {
        TextEncoding.ASCII: {
            "length": 8,
            "encode": chr,
            "decode": ord,
        },
        TextEncoding.BCD: {
            "length": 4,
            "encode": str,
            "decode": int,
        }
    }

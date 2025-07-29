"""Text Data Record implementation."""

__all__ = ["TextDataRecord", "TextEncoding"]

from typing import Sequence, Optional, Dict, Any, TypedDict, Callable

from uds.utilities import ValidatedEnum, validate_nibble
from .abstract_data_record import AbstractDataRecord, SinglePhysicalValueAlias


class TextEncoding(ValidatedEnum):
    """Encoding supported by Text Data Records."""

    ASCII = "ascii"
    BCD = "bcd"


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
                         length=self.__ENCODINGS[encoding]["length"],
                         children=tuple(),
                         min_occurrences=min_occurrences,
                         max_occurrences=max_occurrences)

    @staticmethod
    def _encode_bcd(nibble_value: int) -> str:
        validate_nibble(nibble_value)
        if nibble_value > 9:
            raise ValueError
        return str(nibble_value)

    @property
    def encoding(self) -> TextEncoding:
        return self.__encoding

    @encoding.setter
    def encoding(self, value: TextEncoding) -> None:
        self.__encoding = TextEncoding.validate_member(value)

    def get_physical_value(self, raw_value: int) -> SinglePhysicalValueAlias:
        """
        Decode raw value and provide physical value.

        :param raw_value: Raw (bit) value of this Data Record single occurrence.

        :return: Decoded physical (a label) value for this occurrence.
        """
        self._validate_raw_value(raw_value)
        return self.__ENCODINGS[self.encoding]["encode"](raw_value)

    def get_raw_value(self, character: SinglePhysicalValueAlias) -> int:
        if not isinstance(character, str):
            raise TypeError
        if len(character) != 1:
            raise ValueError
        return self.__ENCODINGS[self.encoding]["decode"](character)


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
            "encode": _encode_bcd,
            "decode": lambda char: int(char, 16),
        }
    }

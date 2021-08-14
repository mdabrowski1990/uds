"""Common implementation of UDS PDU (Protocol Data Unit) for all bus types."""

__all__ = ["AbstractPDU", "AbstractPDUType"]

from abc import ABC, abstractmethod

from .addressing import AddressingMemberTyping, AddressingType
from ..utilities import ByteEnum, RawBytes, RawBytesTuple, validate_raw_bytes


class AbstractPDUType(ByteEnum):
    """
    Abstract definition of Protocol Data Unit.

    Enum with PDU types for certain buses (e.g. CAN, LIN, FlexRay) must inherit after this class.
    """


class AbstractPDU(ABC):
    """Abstract definition of Protocol Data Unit that carries part of diagnostic message."""

    def __init__(self, raw_data: RawBytes, addressing: AddressingMemberTyping) -> None:
        """
        Create storage for information about a single UDS PDU.

        :param raw_data: Raw bytes of PDU data.
        :param addressing: Addressing type for which this PDU is relevant.
        """
        self.raw_data = raw_data  # type: ignore
        self.addressing = addressing  # type: ignore

    @property
    def raw_data(self) -> RawBytesTuple:
        """Raw bytes of data that this PDU carries."""
        return self.__raw_data

    @raw_data.setter
    def raw_data(self, value: RawBytes):
        """
        Set value of raw bytes of data.

        :param value: Raw bytes of data to be carries by this PDU.
        """
        validate_raw_bytes(value=value)
        self.__raw_data = tuple(value)

    @property
    def addressing(self) -> AddressingType:
        """Addressing type for which this PDU is relevant."""
        return self.__addressing

    @addressing.setter
    def addressing(self, value: AddressingMemberTyping):
        """
        Set value of addressing type attribute.

        :param value: Value of addressing type to set.
        """
        AddressingType.validate_addressing_type(value=value)
        self.__addressing = AddressingType(value)

    @property  # noqa: F841
    @abstractmethod
    def pdu_type(self) -> AbstractPDUType:
        """Type of this PDU."""

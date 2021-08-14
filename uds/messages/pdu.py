"""Common implementation of UDS PDU (Protocol Data Unit) for all bus types."""

__all__ = ["AbstractPDU"]

from abc import ABC, abstractmethod
from typing import NoReturn

from .addressing import AddressingType
from ..utilities import ByteEnum, RawBytes, RawBytesTuple, validate_raw_bytes


class PDUType(ByteEnum):
    ...


class AbstractPDU(ABC):
    """Abstract definition of Protocol Data Unit that carries part of diagnostic message."""

    def __init__(self, raw_data: RawBytes, addressing: AddressingType) -> None:
        """
        Create storage for information about a single UDS PDU.

        :param raw_data: Raw bytes of PDU data.
        :param addressing: Addressing type for which this PDU is relevant.
        """
        ...

    @property
    def raw_data(self) -> RawBytesTuple:
        ...

    @raw_data.setter
    def raw_data(self, value: RawBytes) -> NoReturn:
        ...

    @property
    def addressing(self) -> AddressingType:
        ...

    @addressing.setter
    def addressing(self, value: AddressingType) -> NoReturn:
        ...

    @property
    @abstractmethod
    def pdu_type(self) -> PDUType:
        ...

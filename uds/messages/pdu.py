"""Common implementation of UDS PDU (Protocol Data Unit) for all bus types."""

__all__ = ["AbstractPDU", "AbstractPDUType"]

from abc import ABC, abstractmethod

from .transmission_attributes import AddressingMemberTyping, AddressingType, \
    TransmissionDirection, DirectionMemberTyping
from ..utilities import ByteEnum, RawBytes, RawBytesTuple, validate_raw_bytes, ReassignmentError


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
        AddressingType.validate_member(value=value)
        self.__addressing = AddressingType(value)

    @property  # noqa: F841
    @abstractmethod
    def pdu_type(self) -> AbstractPDUType:
        """Type of this PDU."""


class AbstractPDURecord(ABC):
    """Abstract definition of Record that stores information about transmitted or received PDU."""

    @abstractmethod
    def __init__(self, frame: object, direction: DirectionMemberTyping) -> None:
        """
        Create record of a PDU that was either received of transmitted to a bus.

        :param frame: Frame that carried this PDU.
        :param direction: Information whether this PDU was transmitted or received.
        """
        self.frame = frame
        self.direction = direction

    @abstractmethod
    def __validate_frame(self, frame: object) -> None:
        """
        Validate value of a frame before attribute assignment.

        :param frame: Frame value to validate.

        :raise TypeError: Frame has other type than expected.
        :raise ValueError: Some values of a frame are not
        """

    @property
    def frame(self) -> object:
        """Frame that carried this PDU."""
        # TODO

    @frame.setter
    def frame(self, value: DirectionMemberTyping):
        """
        Set value of frame attribute.

        :param value:

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        # TODO

    # TODO: other arguments

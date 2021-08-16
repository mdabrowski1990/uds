"""Common implementation of UDS N_PDU (Network Protocol Data Unit) for all bus types."""

__all__ = ["AbstractNPCI", "AbstractNPDU", "AbstractNPDURecord"]

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime

from uds.utilities import ByteEnum, ValidatedEnum, ExtendableEnum, \
    RawByte, RawBytes, RawBytesTuple, validate_raw_bytes, ReassignmentError
from .transmission_attributes import AddressingMemberTyping, AddressingType, \
    TransmissionDirection, DirectionMemberTyping


class AbstractNPCI(ByteEnum, ValidatedEnum, ExtendableEnum):  # pylint: disable=too-many-ancestors
    """
    Abstract definition of Protocol Control Information (N_PCI).

    Enum with N_PCI for certain buses (e.g. CAN, LIN, FlexRay) must inherit after this class.
    There are some differences in available values for each bus (e.g. LIN does not use Flow Control).
    """


class AbstractNPDU(ABC):
    """Abstract definition of N_PDU (Network Protocol Data Unit) that is a packet of diagnostic message."""

    def __init__(self, raw_data: RawBytes, addressing: AddressingMemberTyping) -> None:
        """
        Create storage for information about a single UDS N_PDU.

        :param raw_data: Raw bytes of N_PDU data.
        :param addressing: Addressing type for which this N_PDU is relevant.
        """
        self.raw_data = raw_data  # type: ignore
        self.addressing = addressing  # type: ignore

    @property
    def raw_data(self) -> RawBytesTuple:
        """Raw bytes of data that this N_PDU carries."""
        return self.__raw_data

    @raw_data.setter
    def raw_data(self, value: RawBytes):
        """
        Set value of raw bytes of data.

        :param value: Raw bytes of data to be carries by this N_PDU.
        """
        validate_raw_bytes(value=value)
        self.__raw_data = tuple(value)

    @property
    def addressing(self) -> AddressingType:
        """Addressing type for which this N_PDU is relevant."""
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
    def npci(self) -> AbstractNPCI:
        """N_PCI (type of UDS N_PDU) value of this N_PDU."""


class AbstractNPDURecord(ABC):
    """Abstract definition of Record that stores information about transmitted or received N_PDU."""

    @abstractmethod
    def __init__(self, frame: object, direction: DirectionMemberTyping) -> None:
        """
        Create record of a N_PDU that was either received of transmitted to a bus.

        :param frame: Frame that carried this N_PDU.
        :param direction: Information whether this N_PDU was transmitted or received.
        """
        self.frame = frame
        self.direction = direction  # type: ignore

    @abstractmethod
    def __validate_frame(self, value: Any) -> None:
        """
        Validate value of a frame before attribute assignment.

        :param value: Frame value to validate.

        :raise TypeError: Frame has other type than expected.
        :raise ValueError: Some values of a frame are not
        """

    def __get_raw_pci(self) -> RawByte:
        """
        Get N_PCI (value that describes N_PDU type) of this N_PDU.

        :return: Integer value of N_PCI.
        """
        return (self.raw_data[0] >> 4) & 0xF  # TODO: make sure it is the first nibble of data for all buses

    @property
    def frame(self) -> object:
        """Frame that carried this N_PDU."""
        return self.__frame

    @frame.setter
    def frame(self, value: DirectionMemberTyping):
        """
        Set value of frame attribute.

        :param value: Frame value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_AbstractNPDURecord__frame")
        except AttributeError:
            self.__validate_frame(value=value)
            self.__frame = value
        else:
            raise ReassignmentError("You cannot change value of 'frame' attribute once it is assigned.")

    @property
    def direction(self) -> TransmissionDirection:
        """Information whether this N_PDU was transmitted or received."""
        return self.__direction

    @direction.setter
    def direction(self, value: DirectionMemberTyping):
        """
        Set value of direction attribute.

        :param value: Direction value to set.

        :raise ReassignmentError: There is a call to change the value after the initial assignment (in __init__).
        """
        try:
            self.__getattribute__("_AbstractNPDURecord__direction")
        except AttributeError:
            TransmissionDirection.validate_member(value=value)
            self.__direction = TransmissionDirection(value)
        else:
            raise ReassignmentError("You cannot change value of 'direction' attribute once it is assigned.")

    @property
    @abstractmethod
    def raw_data(self) -> RawBytesTuple:
        """Raw bytes of data that this N_PDU carried."""

    @property   # noqa: F841
    @abstractmethod
    def npci(self) -> AbstractNPCI:
        """N_PCI (type of N_PDU) value carried by this N_PDU."""

    @property
    @abstractmethod
    def addressing(self) -> AddressingType:
        """Addressing type over which this N_PDU was transmitted."""

    @property  # noqa: F841
    @abstractmethod
    def transmission_time(self) -> datetime:
        """Timestamp when this N_PDU was fully transmitted on a bus."""

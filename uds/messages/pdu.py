"""Common implementation of UDS PDU (Protocol Data Unit) for all bus types."""

__all__ = ["AbstractPDU"]

from abc import ABC

from .addressing import AddressingType
from ..utilities import RawBytes, validate_raw_bytes


class AbstractPDU(ABC):
    """Abstract definition of Protocol Data Unit that carries part of diagnostic message."""

    def __init__(self, raw_data: RawBytes, addressing: AddressingType) -> None:
        """
        Create storage for information about a single UDS PDU.

        :param raw_data: Raw bytes of PDU data.
        :param addressing: Addressing type for which this PDU is relevant.
        """
        self.raw_data = raw_data
        self.addressing = addressing

    # TODO: setting restriction
    # def __setattr__(self, key, value):
    #     if key == "raw_data":
    #         try:
    #             self.__getattribute__("raw_data")
    #         except:


    #
    # @property
    # @abstractmethod
    # def raw_data(self) -> RawBytesTuple:
    #     """"""
    #
    # @property
    # @abstractmethod
    # def addressing(self) -> Optional[AddressingType]:
    #     """
    #     Get addressing type over which this PDU was transmitted/received.
    #
    #     :return: Addressing over which the PDU was transmitted/received. None if PDU was not transmitted/received.
    #     """
    #
    # @property  # noqa: F841
    # @abstractmethod
    # def pdu_type(self) -> Enum:
    #     """Getter of this PDU type."""
    #
    # @property
    # @abstractmethod
    # def time_transmitted(self) -> Optional[datetime]:
    #     """
    #     Time when the PDU was published to on a bus.
    #
    #     It is determined by either time when received or transmitted to a bus.
    #
    #     :return: Date and time when the PDU was fully transmitted.
    #     """


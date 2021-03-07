"""Common part (for server and client side) of transport interface."""

__all__ = ["TransportInterface", "UdsSegmentationError"]

from abc import ABC, abstractmethod

from .types import AddressingType, PDU, PDUs, UdsMessage


class UdsSegmentationError(Exception):
    """
    Error related to UDS message segmentation (UDS message -> PDUs) and desegmentation (PDUs -> UDS message).

    Possible causes:
     - Impossible to segment provided message.
     - Provided PDUs are not a complete PDUs set for a single message.
     - Provided PDUs are related to more than one message.
    """


class TransportInterface(ABC):
    """Abstract definition of Transport Interface that is common for the server and the client."""

    @abstractmethod
    def send_pdu(self, pdu: PDU, addressing: AddressingType) -> PDU:
        """
        Transmit a single Protocol Data Unit (PDU).

        :param pdu: Protocol Data Unit to transmit.
        :param addressing: Addressing type to use for the transmission.

        :return: Transmitted PDU updated with data related to its transmission.
        """

    @abstractmethod
    def receive_pdu(self) -> PDU:
        """
        Wait till incoming PDU is received and return it.

        Warning:
            This method might keep the program in the infinite loop if no PDU is ever received.

        :return: The first PDU that to be received after the call of this method.
        """

    @abstractmethod
    def get_received_pdus(self) -> PDUs:
        """
        Get all Protocol Data Units (PDUs) that were silently received by the Transport Interface.

        :return: PDUs that were received since last call of this method.
        """

    @abstractmethod
    def segment_message(self, message: UdsMessage) -> PDUs:  # noqa: F841
        """
        Perform segmentation of UDS message.

        :param message: UDS message to be segmented.

        :return: PDUs that carries the message that was segmented.
        """

    @abstractmethod
    def join_pdus(self, pdus: PDUs) -> UdsMessage:  # noqa: F841
        """
        Connect PDUs to extract message that was carried by them.

        :param pdus: All Protocol Data Units (PDUs) that carries one UDS message.

        :raise UdsSegmentationError: Provided PDUs are not complete set of PDUs for exactly one message.

        :return: UDS message that was carried in provided PDUs.
        """

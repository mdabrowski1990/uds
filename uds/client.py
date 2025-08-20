"""Implementation for UDS Client Simulation."""

__all__ = ["Client"]

from typing import Optional, Tuple

from uds.addressing import AddressingType
from uds.message import UdsMessage, UdsMessageRecord
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import TimeMillisecondsAlias


class Client:
    """Simulator of UDS Client entity."""

    DEFAULT_P2_CLIENT_TIMEOUT: TimeMillisecondsAlias = 50
    """Default value of P2Client timeout."""
    DEFAULT_P6_CLIENT_TIMEOUT: TimeMillisecondsAlias = 50
    """Default value of P6Client timeout."""
    DEFAULT_P2_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 5000
    """Default value of P2*Client timeout."""
    DEFAULT_P6_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 5000
    """Default value of P6*Client timeout."""
    DEFAULT_P3_CLIENT: TimeMillisecondsAlias = DEFAULT_P2_CLIENT_TIMEOUT * 1.5
    """Default value of P3Client_phys and P3Client_func time parameters."""
    DEFAULT_S3_CLIENT: TimeMillisecondsAlias = 2000
    """Default value of S3Client time parameter."""

    def __init__(self,
                 transport_interface: AbstractTransportInterface,
                 p2_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_CLIENT_TIMEOUT,
                 p6_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_CLIENT_TIMEOUT,
                 p2_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_EXT_CLIENT_TIMEOUT,
                 p6_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_EXT_CLIENT_TIMEOUT,
                 p3_client_physical: TimeMillisecondsAlias = DEFAULT_P3_CLIENT,
                 p3_client_functional: TimeMillisecondsAlias = DEFAULT_P3_CLIENT,
                 s3_client: TimeMillisecondsAlias = DEFAULT_S3_CLIENT) -> None:
        """
        Create Client for UDS communication.

        :param transport_interface: Transport Interface object for managing UDS communication.
        :param p2_client_timeout: Timeout value for P2Client parameter.
        :param p6_client_timeout: Timeout value for P6Client parameter.
        :param p2_ext_client_timeout: Timeout value for P2*Client parameter.
        :param p6_ext_client_timeout: Timeout value for P*Client parameter.
        :param p3_client_physical: Value of P3Client_phys time parameter.
        :param p3_client_functional: Value of P3Client_func time parameter.
        :param s3_client: Value of S3Client time parameter.
        """
        raise NotImplementedError

    @property
    def transport_interface(self) -> AbstractTransportInterface:
        """Get Transport Interface used."""
        raise NotImplementedError

    @property
    def p2_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P2Client parameter."""
        raise NotImplementedError

    @p2_client_timeout.setter
    def p2_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """Set timeout value for P2Client parameter."""
        raise NotImplementedError

    @property  # noqa: vulture
    def p2_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P2Client parameter."""
        raise NotImplementedError

    @property
    def p6_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P6Client parameter."""
        raise NotImplementedError

    @p6_client_timeout.setter
    def p6_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """Set timeout value for P6Client parameter."""
        raise NotImplementedError

    @property  # noqa: vulture
    def p6_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P6Client parameter."""
        raise NotImplementedError

    @property
    def p2_ext_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P2*Client parameter."""
        raise NotImplementedError

    @p2_ext_client_timeout.setter
    def p2_ext_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """Set timeout value for P2*Client parameter."""
        raise NotImplementedError

    @property  # noqa: vulture
    def p2_ext_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P2*Client parameter."""
        raise NotImplementedError

    @property
    def p6_ext_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P6*Client parameter."""
        raise NotImplementedError

    @p6_ext_client_timeout.setter
    def p6_ext_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """Set timeout value for P6*Client parameter."""
        raise NotImplementedError

    @property  # noqa: vulture
    def p6_ext_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P6*Client parameter."""
        raise NotImplementedError

    @property
    def p3_client_physical(self) -> TimeMillisecondsAlias:
        """Get value of P3Client_phys parameter."""
        raise NotImplementedError

    @p3_client_physical.setter
    def p3_client_physical(self, value: TimeMillisecondsAlias) -> None:
        """Set value of P3Client_phys parameter."""
        raise NotImplementedError

    @property
    def p3_client_functional(self) -> TimeMillisecondsAlias:
        """Get value of P3Client_func parameter."""
        raise NotImplementedError

    @p3_client_functional.setter
    def p3_client_functional(self, value: TimeMillisecondsAlias) -> None:
        """Set value of P3Client_func parameter."""
        raise NotImplementedError

    @property
    def s3_client(self) -> TimeMillisecondsAlias:
        """Get value of S3Client parameter."""
        raise NotImplementedError

    @s3_client.setter
    def s3_client(self, value: TimeMillisecondsAlias) -> None:
        """Set value of S3Client parameter."""
        raise NotImplementedError

    def start_tester_present(self,
                             addressing_type: AddressingType = AddressingType.FUNCTIONAL,
                             sprmib: bool = True) -> None:  # noqa: vulture
        """
        Start sending Tester Precent cyclically.

        :param addressing_type: Addressing Type to use for cyclical messages.
        :param sprmib: Whether to use Suppress Positive Response Message Indication Bit.
        """
        raise NotImplementedError

    def stop_tester_present(self) -> None:
        """Stop sending Tester Precent cyclically."""
        raise NotImplementedError

    def send_request_receive_responses(self,
                                       request: UdsMessage  # noqa: vulture
                                       ) -> Tuple[UdsMessageRecord, Tuple[UdsMessageRecord, ...]]:
        """
        Send diagnostic request and receive all responses (till the final one).

        :param request: Request message to send.

        :return: Tuple with two elements:

            - record of diagnostic request message that was sent
            - tuple with diagnostic response messages that were received in the response
        """
        raise NotImplementedError

    def get_response(self, timeout: Optional[TimeMillisecondsAlias] = None) -> Optional[UdsMessageRecord]:
        """
        Wait for the first received response message.

        .. note:: This method can be used for fetching responses messages that were not direct responses to
            request messages sent via :meth:`~uds.client.Client.send_request_receive_responses`.

            This includes responses to cyclically sent Tester Present.
            Typically used for fetching following :ref:`Response on Event (RSID 0xC6) <ResponseOnEvent>` responses.

        :param timeout: Maximal time to wait for a response message.
            Leave None to wait forever.

        :return: Record with the first response message received or None if no message was received.
        """
        raise NotImplementedError

    def get_response_no_wait(self) -> Optional[UdsMessageRecord]:
        """
        Get the first received response message, but do not wait for its arrival.

        .. note:: This method can be used for fetching responses messages that were not direct responses to
            request messages sent via :meth:`~uds.client.Client.send_request_receive_responses`.

            This includes responses to cyclically sent Tester Present.
            Typically used for fetching following :ref:`Response on Event (RSID 0xC6) <ResponseOnEvent>` responses.

        :return: Record with the first response message received or None if no message was received.
        """
        raise NotImplementedError

"""Implementation for UDS Client Simulation."""

__all__ = ["Client"]


from typing import Optional

from uds.utilities import TimeMillisecondsAlias
from uds.transport_interface import AbstractTransportInterface


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

    @property
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

    @property
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

    @property
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

    @property
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

    def start_tester_present(self, addressing_type: , sprmib: bool = True) -> None:
        """
        Start sending Tester Precent cyclically.

        :return:
        """
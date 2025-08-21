"""Implementation for UDS Client Simulation."""

__all__ = ["Client"]

from typing import Optional, Tuple

from uds.addressing import AddressingType
from uds.message import UdsMessage, UdsMessageRecord
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import InconsistencyError, ReassignmentError, TimeMillisecondsAlias


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
                 p2_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_EXT_CLIENT_TIMEOUT,
                 p6_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_CLIENT_TIMEOUT,
                 p6_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_EXT_CLIENT_TIMEOUT,
                 p3_client_physical: TimeMillisecondsAlias = DEFAULT_P3_CLIENT,
                 p3_client_functional: TimeMillisecondsAlias = DEFAULT_P3_CLIENT,
                 s3_client: TimeMillisecondsAlias = DEFAULT_S3_CLIENT) -> None:
        """
        Create Client for UDS communication.

        :param transport_interface: Transport Interface object for managing UDS communication.
        :param p2_client_timeout: Timeout value for P2Client parameter.
        :param p2_ext_client_timeout: Timeout value for P2*Client parameter.
        :param p6_client_timeout: Timeout value for P6Client parameter.
        :param p6_ext_client_timeout: Timeout value for P*Client parameter.
        :param p3_client_physical: Value of P3Client_phys time parameter.
        :param p3_client_functional: Value of P3Client_func time parameter.
        :param s3_client: Value of S3Client time parameter.
        """
        self.transport_interface = transport_interface
        self.p2_client_timeout = p2_client_timeout
        self.p2_ext_client_timeout = p2_ext_client_timeout
        self.p6_client_timeout = p6_client_timeout
        self.p6_ext_client_timeout = p6_ext_client_timeout
        self.p3_client_physical = p3_client_physical
        self.p3_client_functional = p3_client_functional
        self.s3_client = s3_client
        self.__p2_client_measured = None
        self.__p2_ext_client_measured = None
        self.__p6_client_measured = None
        self.__p6_ext_client_measured = None

    @property
    def transport_interface(self) -> AbstractTransportInterface:
        """Get Transport Interface used."""
        return self.__transport_interface

    @transport_interface.setter
    def transport_interface(self, value: AbstractTransportInterface) -> None:
        """
        Set Transport Interface for UDS communication.

        :param value: Value to set.

        :raise TypeError: Provided value is not an instance of AbstractTransportInterface class.
        :raise ReassignmentError: An attempt to change the value after object creation.
        """
        if not isinstance(value, AbstractTransportInterface):
            raise TypeError("Provided value is not an instance of AbstractTransportInterface class.")
        if hasattr(self, "_Client__transport_interface"):
            raise ReassignmentError("Value of 'transport_interface' attribute cannot be changed once assigned.")
        self.__transport_interface = value

    @property
    def p2_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P2Client parameter."""
        return self.__p2_client_timeout

    @p2_client_timeout.setter
    def p2_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for P2Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        self.__p2_client_timeout = value

    @property  # noqa: vulture
    def p2_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P2Client parameter."""
        return self.__p2_client_measured

    @property
    def p2_ext_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P2*Client parameter."""
        return self.__p2_ext_client_timeout

    @p2_ext_client_timeout.setter
    def p2_ext_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for P2*Client parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        self.__p2_ext_client_timeout = value

    @property  # noqa: vulture
    def p2_ext_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P2*Client parameter."""
        return self.__p2_ext_client_measured

    @property
    def p6_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P6Client parameter."""
        return self.__p6_client_timeout

    @p6_client_timeout.setter
    def p6_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for P6Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P6Client timeout value must be greater or equal than P2Client.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p2_client_timeout:
            raise InconsistencyError("P6Client timeout value must be greater or equal than P2Client timeout.")
        self.__p6_client_timeout = value

    @property  # noqa: vulture
    def p6_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P6Client parameter."""
        return self.__p6_client_measured

    @property
    def p6_ext_client_timeout(self) -> TimeMillisecondsAlias:
        """Get timeout value for P6*Client parameter."""
        return self.__p6_ext_client_timeout

    @p6_ext_client_timeout.setter
    def p6_ext_client_timeout(self, value: TimeMillisecondsAlias) -> None:
        """
        Set timeout value for P6*Client parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P6*Client timeout value must be greater or equal than P2*Client and P6Client.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p6_client_timeout or value < self.p2_ext_client_timeout:
            raise InconsistencyError("P6*Client timeout value must be greater or equal than "
                                     f"P2*Client timeout ({self.p2_ext_client_timeout} ms) and "
                                     f"P6Client timeout ({self.p6_client_timeout} ms).")
        self.__p6_ext_client_timeout = value

    @property  # noqa: vulture
    def p6_ext_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """Get last measured value of P6*Client parameter."""
        return self.__p6_ext_client_measured

    @property
    def p3_client_physical(self) -> TimeMillisecondsAlias:
        """Get value of P3Client_phys parameter."""
        return self.__p3_client_physical

    @p3_client_physical.setter
    def p3_client_physical(self, value: TimeMillisecondsAlias) -> None:
        """
        Set value of P3Client_phys parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P6*Client timeout value must be greater or equal than P6Client.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p6_client_timeout:
            raise InconsistencyError("P3Client value must be greater or equal than "
                                     f"P6Client timeout ({self.p6_client_timeout} ms).")
        self.__p3_client_physical = value

    @property
    def p3_client_functional(self) -> TimeMillisecondsAlias:
        """Get value of P3Client_func parameter."""
        return self.__p3_client_functional

    @p3_client_functional.setter
    def p3_client_functional(self, value: TimeMillisecondsAlias) -> None:
        """
        Set value of P3Client_func parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P6*Client timeout value must be greater or equal than P6Client.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p6_client_timeout:
            raise InconsistencyError("P3Client value must be greater or equal than "
                                     f"P6Client timeout ({self.p6_client_timeout} ms).")
        self.__p3_client_functional = value

    @property
    def s3_client(self) -> TimeMillisecondsAlias:
        """Get value of S3Client parameter."""
        return self.__s3_client

    @s3_client.setter
    def s3_client(self, value: TimeMillisecondsAlias) -> None:
        """
        Set value of S3Client parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P6*Client timeout value must be greater or equal than P6Client.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p6_client_timeout:
            raise InconsistencyError("S3Client value must be greater or equal than P6Client timeout.")
        self.__s3_client = value

    def _update_p2_client_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of P2Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided value is not int or float type.")
        if value <= 0:
            raise ValueError("P2Client parameter value must be a positive number.")
        self.__p2_client_measured = value

    def _update_p2_ext_client_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of P2*Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided value is not int or float type.")
        if value <= 0:
            raise ValueError("P2*Client parameter value must be a positive number.")
        self.__p2_ext_client_measured = value
        
    def _update_p6_client_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of P6Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided value is not int or float type.")
        if value <= 0:
            raise ValueError("P6Client parameter value must be a positive number.")
        self.__p6_client_measured = value
        
    def _update_p6_ext_client_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of P6*Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided value is not int or float type.")
        if value <= 0:
            raise ValueError("P6*Client parameter value must be a positive number.")
        self.__p6_ext_client_measured = value

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
            Typically used for fetching following
            :ref:`Response on Event (RSID 0xC6) <knowledge-base-service-response-on-event>` responses.

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
            Typically used for fetching following
            :ref:`Response on Event (RSID 0xC6) <knowledge-base-service-response-on-event>` responses.

        :return: Record with the first response message received or None if no message was received.
        """
        raise NotImplementedError

    def clear_response_queue(self) -> None:
        """Clear all response messages that are currently stored in the queue."""
        raise NotImplementedError

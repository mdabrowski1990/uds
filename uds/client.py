"""Implementation for UDS Client Simulation."""

__all__ = ["Client"]

from time import time
from typing import List, Optional, Sequence, Tuple, Union
from warnings import warn

from uds.addressing import AddressingType
from uds.message import NRC, RESPONSE_REQUEST_SID_DIFF, RequestSID, ResponseSID, UdsMessage, UdsMessageRecord
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import InconsistencyError, ReassignmentError, TimeMillisecondsAlias, ValueWarning, bytes_to_hex


class Client:
    """Simulation for UDS Client entity."""

    DEFAULT_P2_CLIENT_TIMEOUT: TimeMillisecondsAlias = 50
    """Default value of P2Client timeout."""
    DEFAULT_P6_CLIENT_TIMEOUT: TimeMillisecondsAlias = 50
    """Default value of P6Client timeout."""
    DEFAULT_P2_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 5000
    """Default value of P2*Client timeout."""
    DEFAULT_P6_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 5000
    """Default value of P6*Client timeout."""
    DEFAULT_S3_CLIENT: TimeMillisecondsAlias = 2000
    """Default value of S3Client time parameter."""

    def __init__(self,
                 transport_interface: AbstractTransportInterface,
                 p2_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_CLIENT_TIMEOUT,
                 p2_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_EXT_CLIENT_TIMEOUT,
                 p6_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_CLIENT_TIMEOUT,
                 p6_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_EXT_CLIENT_TIMEOUT,
                 s3_client: TimeMillisecondsAlias = DEFAULT_S3_CLIENT) -> None:
        """
        Configure Client for UDS communication.

        :param transport_interface: Transport Interface object for managing UDS communication.
        :param p2_client_timeout: Timeout value for P2Client parameter.
        :param p2_ext_client_timeout: Timeout value for P2*Client parameter.
        :param p6_client_timeout: Timeout value for P6Client parameter.
        :param p6_ext_client_timeout: Timeout value for P*Client parameter.
        :param s3_client: Value of S3Client time parameter.
        """
        self.transport_interface = transport_interface
        self.p2_client_timeout = p2_client_timeout
        self.p2_ext_client_timeout = p2_ext_client_timeout
        self.p6_client_timeout = p6_client_timeout
        self.p6_ext_client_timeout = p6_ext_client_timeout
        self.s3_client = s3_client
        self.__p2_client_measured: Optional[TimeMillisecondsAlias] = None
        self.__p2_ext_client_measured: Optional[Tuple[TimeMillisecondsAlias, ...]] = None
        self.__p6_client_measured: Optional[TimeMillisecondsAlias] = None
        self.__p6_ext_client_measured: Optional[TimeMillisecondsAlias] = None

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
        """
        Get last measured value of P2Client parameter.

        :return: The last measured value or None if measurement was not performed.
        """
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
    def p2_ext_client_measured(self) -> Optional[Tuple[TimeMillisecondsAlias, ...]]:
        """
        Get last measured values of P2*Client parameter.

        :return: The last measured values or None if measurement was not performed.
        """
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
        :raise InconsistencyError: P6Client timeout value must be greater or equal than P2Client timeout.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p2_client_timeout:
            raise InconsistencyError("P6Client timeout value must be greater or equal than "
                                     f"P2Client timeout ({self.p2_client_timeout} ms).")
        self.__p6_client_timeout = value

    @property  # noqa: vulture
    def p6_client_measured(self) -> Optional[TimeMillisecondsAlias]:
        """
        Get last measured value of P6Client parameter.

        :return: The last measured value or None if measurement was not performed.
        """
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
        :raise InconsistencyError: P6*Client timeout value must be greater or equal than P2*Client timeout and
            P6Client timeout.
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
        """
        Get last measured value of P6*Client parameter.

        :return: The last measured value or None if measurement was not performed.
        """
        return self.__p6_ext_client_measured

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
        :raise InconsistencyError: S3Client value must be greater or equal than P6Client timeout.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p6_client_timeout:
            raise InconsistencyError("S3Client value must be greater or equal than "
                                     f"P6Client timeout ({self.p6_client_timeout} ms).")
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
        if value > self.p2_client_timeout:
            warn("Measured value of P2Client was greater than P2Client timeout.",
                 category=ValueWarning)
        self.__p2_client_measured = value

    def _update_p2_ext_client_measured(self, *values: TimeMillisecondsAlias) -> None:
        """
        Update measured values of P2*Client parameter.

        :param values: Values to set.

        :raise RuntimeError: At least one P2*Client value must be provided.
        :raise TypeError: One of provided values is not int or float type.
        :raise ValueError: One of provided values is out of range.
        """
        if len(values) == 0:
            raise RuntimeError("At least one P2*Client value must be provided.")
        for value in values:
            if not isinstance(value, (int, float)):
                raise TypeError("One of provided values is not int or float type.")
            if value <= 0:
                raise ValueError("P2*Client parameter value must be a positive number.")
            if value > self.p2_ext_client_timeout:
                warn("Measured value of P2*Client was greater than P2*Client timeout.",
                     category=ValueWarning)
        self.__p2_ext_client_measured = tuple(values)

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
        if value > self.p6_client_timeout:
            warn("Measured value of P6Client was greater than P6Client timeout.",
                 category=ValueWarning)
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
        if value > self.p6_ext_client_timeout:
            warn("Measured value of P6*Client was greater than P6*Client timeout.",
                 category=ValueWarning)
        self.__p6_ext_client_measured = value

    def _update_measured_client_values(self,
                                       request_record: UdsMessageRecord,
                                       response_records: Sequence[UdsMessageRecord]) -> None:
        """
        Update measured timing parameters on Client side (P2Client, P2*Client, P6Client and P6*Client).

        :param request_record: Record of the last transmitted request message.
        :param response_records: Records of received responses to provided message.
        """
        p2_measured = response_records[0].transmission_start - request_record.transmission_end
        self._update_p2_client_measured(p2_measured.total_seconds() * 1000.)
        if len(response_records) > 1:
            p2_ext_measured_list = []
            for i, response_record in enumerate(response_records[1:]):
                _p2_ext_measured = response_record.transmission_end - response_records[i].transmission_end
                p2_ext_measured_list.append(_p2_ext_measured.total_seconds() * 1000.)
            p6_ext_measured = response_records[-1].transmission_end - request_record.transmission_end
            self._update_p2_ext_client_measured(*p2_ext_measured_list)
            self._update_p6_ext_client_measured(p6_ext_measured.total_seconds() * 1000.)
        else:
            p6_measured = response_records[-1].transmission_end - request_record.transmission_end
            self._update_p6_client_measured(p6_measured.total_seconds() * 1000.)

    def _receive_response(self, sid: RequestSID, timeout: TimeMillisecondsAlias) -> Optional[UdsMessageRecord]:
        """
        Received UDS message.

        :param sid: SID of the last sent request message.
        :param timeout: Maximal time (in milliseconds) to wait.

        :return: Record with response message received to the last UDS request message sent.
            None if a timeout was reached.
        """
        time_start_s = time()
        time_remaining_ms = timeout
        while time_remaining_ms > 0:
            try:
                response_record = self.transport_interface.receive_message(timeout=time_remaining_ms)
            except TimeoutError:
                return None
            # positive response message received
            if response_record.payload[0] == sid + RESPONSE_REQUEST_SID_DIFF:
                return response_record
            # negative response message received
            if response_record.payload[0] == ResponseSID.NegativeResponse and response_record.payload[1] == sid:
                return response_record
            # other response message received
            # TODO: add it to response queue when created - https://github.com/mdabrowski1990/uds/issues/63
            time_elapsed_ms = (time() - time_start_s) * 1000.
            time_remaining_ms = timeout - time_elapsed_ms
        return None

    @staticmethod
    def is_response_pending_message(message: Union[UdsMessage, UdsMessageRecord], request_sid: RequestSID) -> bool:
        """
        Check if provided UDS message record contains Negative Response with Response Pending NRC.

        :param message: UDS Message Record to check.
        :param request_sid: Request SID value sent in the proceeding UDS request message.

        :raise TypeError: Provided message value is not an instance of UdsMessageRecord class.

        :return: True if provided UDS message record contains Negative Response with Response Pending NRC,
            False otherwise.
        """
        if not isinstance(message, (UdsMessage, UdsMessageRecord)):
            raise TypeError("Provided message value is not an instance of UdsMessageRecord class.")
        request_sid = RequestSID.validate_member(request_sid)
        if len(message.payload) != 3:
            return False
        return (message.payload[0] == ResponseSID.NegativeResponse
                and message.payload[1] == request_sid
                and message.payload[2] == NRC.RequestCorrectlyReceived_ResponsePending)

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
                                       request: UdsMessage) -> Tuple[UdsMessageRecord, Tuple[UdsMessageRecord, ...]]:
        """
        Send diagnostic request and receive all responses (till the final one).

        :param request: Request message to send.

        :raise TypeError: Provided value is not an instance of UdsMessage class.
        :raise TimeoutError: Response was initiated with Response Pending message, but never finalized.

        :return: Tuple with two elements:

            - record of diagnostic request message that was sent
            - tuple with diagnostic response messages that were received in the response
        """
        if not isinstance(request, UdsMessage):
            raise TypeError("Provided request value is not an instance of UdsMessage class.")
        request_record = self.transport_interface.send_message(request)
        time_last_message = time_request_sent = request_record.transmission_end.timestamp()
        sid = RequestSID(request_record.payload[0])
        response_records: List[UdsMessageRecord] = []
        # get the first response (either final response or negative response with response pending nrc)
        time_elapsed_since_request_ms = (time() - time_request_sent) * 1000.
        time_elapsed_since_last_message_ms = (time() - time_last_message) * 1000.
        final_timeout = self.p6_client_timeout - time_elapsed_since_request_ms
        next_message_timeout = self.p2_client_timeout - time_elapsed_since_last_message_ms
        timeout = min(final_timeout, next_message_timeout)
        response_record = self._receive_response(sid=sid, timeout=timeout)
        if response_record is None:  # timeout achieved - no response
            return request_record, tuple()
        response_records.append(response_record)
        while self.is_response_pending_message(message=response_records[-1], request_sid=sid):
            time_last_message = response_records[-1].transmission_end.timestamp()
            time_elapsed_since_request_ms = (time() - time_request_sent) * 1000.
            time_elapsed_since_last_message_ms = (time() - time_last_message) * 1000.
            final_timeout = self.p6_ext_client_timeout - time_elapsed_since_request_ms
            next_message_timeout = self.p2_ext_client_timeout - time_elapsed_since_last_message_ms
            timeout = min(final_timeout, next_message_timeout)
            response_record = self._receive_response(sid=sid, timeout=timeout)
            if response_record is None:  # timeout achieved - no following response
                raise TimeoutError(f"P2*Client timeout ({self.p2_ext_client_timeout} ms) reached after receiving "
                                   f"{len(response_records)} response pending messages "
                                   f"({bytes_to_hex(response_records[-1].payload)}).")
            response_records.append(response_record)
        self._update_measured_client_values(request_record=request_record, response_records=response_records)
        return request_record, tuple(response_records)

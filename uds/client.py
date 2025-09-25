"""Implementation for :ref:`UDS Client <knowledge-base-client>` Simulation."""

__all__ = ["Client"]

from functools import wraps
from queue import Empty, SimpleQueue
from threading import Event, Thread
from time import perf_counter, time
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union
from warnings import warn

from uds.addressing import AddressingType
from uds.message import NRC, RESPONSE_REQUEST_SID_DIFF, RequestSID, ResponseSID, UdsMessage, UdsMessageRecord
from uds.translator import TESTER_PRESENT
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import (
    InconsistencyError,
    MessageTransmissionNotStartedError,
    ReassignmentError,
    TimeMillisecondsAlias,
    ValueWarning,
    bytes_to_hex,
)


def decorator_block_receiving(method: Callable) -> Callable:  # type: ignore
    """
    Decorate a method that blocks receiving task.

    :param method: Method to decorate.

    :return: Decorated method.
    """
    @wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
        # pylint: disable=protected-access
        self._Client__receiving_break_event.set()
        self._Client__receiving_not_in_progress.wait(timeout=self.p6_ext_client_timeout)
        try:
            return_value = method(self, *args, **kwargs)
        except Exception as error:
            self._Client__receiving_break_event.clear()
            raise error
        self._Client__receiving_break_event.clear()
        return return_value
    return wrapper


class Client:
    """Simulation for UDS Client entity."""

    DEFAULT_P2_CLIENT_TIMEOUT: TimeMillisecondsAlias = 100  # P2Client_max > P2Server_max (default: 50 ms)
    """Default value of :ref:`P2Client <knowledge-base-p2-client>` timeout."""
    DEFAULT_P6_CLIENT_TIMEOUT: TimeMillisecondsAlias = 10000  # P6Client_max > P2Client_max
    """Default value of :ref:`P6Client <knowledge-base-p6-client>` timeout."""
    DEFAULT_P2_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 5050  # P2*Client_max > P2*Server_max (default: 5000 ms)
    """Default value of :ref:`P2*Client <knowledge-base-p2*-client>` timeout."""
    DEFAULT_P6_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 50000  # P6*Client_max > P2*Client_max
    """Default value of :ref:`P6*Client <knowledge-base-p6*-client>` timeout."""
    DEFAULT_S3_CLIENT: TimeMillisecondsAlias = 2000
    """Default value of :ref:`S3Client <knowledge-base-s3-client>` time parameter."""
    DEFAULT_RECEIVING_TASK_CYCLE: TimeMillisecondsAlias = 20
    """Default value of receiving task cycle."""

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
        self.__response_queue: SimpleQueue[UdsMessageRecord] = SimpleQueue()
        self.__receiving_thread: Optional[Thread] = None
        self.__receiving_stop_event: Event = Event()
        self.__receiving_break_event: Event = Event()
        self.__receiving_not_in_progress: Event = Event()
        self.__tester_present_thread: Optional[Thread] = None
        self.__tester_present_stop_event: Event = Event()
        self.__receiving_stop_event.set()
        self.__receiving_break_event.clear()
        self.__receiving_not_in_progress.set()
        self.__tester_present_stop_event.set()

    def __del__(self) -> None:
        """Safely finish all tasks."""
        if self.is_tester_present_sent:
            self.stop_tester_present()
        if self.is_receiving:
            self.stop_receiving()

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
        """Get timeout value for :ref:`P2Client <knowledge-base-p2-client>` parameter."""
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
        """Get timeout value for :ref:`P2*Client <knowledge-base-p2*-client>` parameter."""
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
        """Get timeout value for :ref:`P6Client <knowledge-base-p6-client>` parameter."""
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
        """Get timeout value for :ref:`P6*Client <knowledge-base-p6*-client>` parameter."""
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
        """Get value of :ref:`S3Client <knowledge-base-s3-client>` parameter."""
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
        if value < self.p2_client_timeout:
            raise InconsistencyError("S3Client value must be greater or equal than "
                                     f"P2Client timeout ({self.p2_client_timeout} ms).")
        self.__s3_client = value

    @property
    def is_receiving(self) -> bool:
        """Get flag whether receiving thread is running."""
        return self.__receiving_thread is not None

    @property
    def is_tester_present_sent(self) -> bool:
        """Get flag whether Tester Present thread is running periodic sending."""
        return self.__tester_present_thread is not None

    def _update_p2_client_measured(self, value: TimeMillisecondsAlias) -> None:
        """
        Update measured values of P2Client parameter.

        :param value: Value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
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
        :raise ValueError: Provided time value must be a positive number.
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
        :raise ValueError: Provided time value must be a positive number.
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
        if p2_measured.total_seconds() > 0:
            self._update_p2_client_measured(p2_measured.total_seconds() * 1000.)
        else:
            warn("Measured P2Client value is negative. Check Transport Interface accuracy.",
                 category=RuntimeWarning)
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
            if p6_measured.total_seconds() > 0:
                self._update_p6_client_measured(p6_measured.total_seconds() * 1000.)
            else:
                warn("Measured P6Client value is negative. Check Transport Interface accuracy.",
                     category=RuntimeWarning)

    def _receive_response(self,
                          sid: RequestSID,
                          start_timeout: TimeMillisecondsAlias,
                          end_timeout: TimeMillisecondsAlias) -> Optional[UdsMessageRecord]:
        """
        Receive UDS response message to previously sent request.

        :param sid: SID of the last sent request message.
        :param start_timeout: Maximal time (in milliseconds) to wait.

        :return: Record with response message received to the last UDS request message sent.
            None if a timeout was reached.
        """
        timestamp_start = perf_counter()
        remaining_start_timeout_ms = start_timeout  # either P2Client or P2*Client
        remaining_end_timeout_ms = end_timeout  # either P6Client or P6*Client
        while remaining_start_timeout_ms > 0 and remaining_end_timeout_ms > 0:
            # try to receive a message
            try:
                response_record = self.transport_interface.receive_message(
                    start_timeout=min(remaining_start_timeout_ms, remaining_end_timeout_ms),
                    end_timeout=remaining_end_timeout_ms)
            except MessageTransmissionNotStartedError:
                return None
            # positive response message received
            if response_record.payload[0] == sid + RESPONSE_REQUEST_SID_DIFF:
                return response_record
            # negative response message received
            if response_record.payload[0] == ResponseSID.NegativeResponse and response_record.payload[1] == sid:
                return response_record
            # other response message received
            self.__response_queue.put_nowait(response_record)
            # update time parameters
            time_elapsed_ms = (perf_counter() - timestamp_start) * 1000.
            remaining_start_timeout_ms = start_timeout - time_elapsed_ms
            remaining_end_timeout_ms = end_timeout - time_elapsed_ms
        return None

    def _receive_task(self, cycle: TimeMillisecondsAlias) -> None:
        """
        Schedule reception of a UDS message for a cyclic response collecting.

        :param cycle: Time (in milliseconds) used for this task cycle.
        """
        while not self.__receiving_stop_event.is_set():
            if self.__receiving_break_event.wait(cycle / 1000.):
                continue
            self.__receiving_not_in_progress.clear()
            try:
                response = self.transport_interface.receive_message(start_timeout=cycle,
                                                                    end_timeout=self.p6_ext_client_timeout)
            except TimeoutError:
                pass
            else:
                self.__response_queue.put_nowait(response)
            self.__receiving_not_in_progress.set()

    def _send_tester_present_task(self, tester_present_message: UdsMessage) -> None:
        """
        Schedule a single Tester Present message transmission for a cyclic sending.

        :param tester_present_message: Tester Present message to send.
        """
        period = self.s3_client / 1000.0
        next_call = perf_counter()
        while not self.__tester_present_stop_event.is_set():
            self.transport_interface.send_message(tester_present_message)
            next_call += period
            remaining_wait = next_call - perf_counter()
            if self.__tester_present_stop_event.wait(remaining_wait):
                break

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

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided value is out of range.

        :return: Record with the first response message received or None if no message was received.
        """
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise TypeError("Timeout value must be None, int or float type.")
            if timeout <= 0:
                raise ValueError(f"Provided timeout value is less or equal to 0. Actual value: {timeout}")
        try:
            return self.__response_queue.get(timeout=None if timeout is None else timeout / 1000.)
        except Empty:
            return None

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
        try:
            return self.__response_queue.get_nowait()
        except Empty:
            return None

    def clear_response_queue(self) -> None:
        """Clear all response messages that are currently stored in the queue."""
        for _ in range(self.__response_queue.qsize()):
            self.__response_queue.get_nowait()

    def start_receiving(self, cycle: TimeMillisecondsAlias = DEFAULT_RECEIVING_TASK_CYCLE) -> None:
        """
        Start receiving task in the background.

        All response messages sent to this Client while receiving is active, will be collected and accessible via
        :meth:`~uds.client.Client.get_response` and :meth:`~uds.client.Client.get_response_no_wait` methods.

        .. warning:: Cycle value would be overwritten with default value if request message is sent while receiving.
        """
        if self.is_receiving:
            warn("Receiving is already active.",
                 category=UserWarning)
        else:
            self.__receiving_stop_event.clear()
            self.__receiving_thread = Thread(target=self._receive_task,
                                             kwargs={"cycle": cycle},
                                             daemon=True)
            self.__receiving_thread.start()

    def stop_receiving(self) -> None:
        """Stop receiving task."""
        if self.is_receiving:
            self.__receiving_stop_event.set()
            self.__receiving_thread.join()  # type: ignore
            self.__receiving_thread = None
        else:
            warn("Receiving is already stopped.",
                 category=UserWarning)

    def start_tester_present(self,
                             addressing_type: AddressingType = AddressingType.FUNCTIONAL,
                             sprmib: bool = True) -> None:
        """
        Start sending Tester Present cyclically.

        :param addressing_type: Addressing Type to use for cyclical messages.
        :param sprmib: Whether to use Suppress Positive Response Message Indication Bit.
        """
        if self.is_tester_present_sent:
            warn("Tester Present is already transmitted cyclically.",
                 category=UserWarning)
        else:
            self.__tester_present_stop_event.clear()
            payload = TESTER_PRESENT.encode_request({
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": sprmib,
                    "zeroSubFunction": 0}
            })
            tester_present_message = UdsMessage(payload=payload,
                                                addressing_type=AddressingType.validate_member(addressing_type))
            self.__tester_present_thread = Thread(target=self._send_tester_present_task,
                                                  args=(tester_present_message, ),
                                                  daemon=True)
            self.__tester_present_thread.start()

    def stop_tester_present(self) -> None:
        """Stop sending Tester Present cyclically."""
        if self.is_tester_present_sent:
            self.__tester_present_stop_event.set()
            self.__tester_present_thread.join(timeout=self.s3_client / 1000.)  # type: ignore
            self.__tester_present_thread = None
        else:
            warn("Cyclical sending of Tester Present is already stopped.",
                 category=UserWarning)

    @decorator_block_receiving
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
        time_request_sent = request_record.transmission_end.timestamp()
        sid = RequestSID(request_record.payload[0])
        response_records: List[UdsMessageRecord] = []
        time_elapsed_ms = (time() - time_request_sent) * 1000.
        # get the first response (either final response or negative response with response pending nrc)
        try:
            response_record = self._receive_response(sid=sid,
                                                     start_timeout=self.p2_client_timeout - time_elapsed_ms,
                                                     end_timeout=self.p6_client_timeout - time_elapsed_ms)
        except TimeoutError as exception:
            raise TimeoutError("P6Client timeout reached.") from exception
        if response_record is None:  # timeout achieved - no response
            return request_record, tuple()
        response_records.append(response_record)
        timestamp_p6_ext_timeout = time_request_sent + self.p6_ext_client_timeout / 1000.
        while self.is_response_pending_message(message=response_records[-1], request_sid=sid):
            timestamp_now = time()
            timestamp_p2_ext_timeout = (response_records[-1].transmission_end.timestamp()
                                        + self.p2_ext_client_timeout / 1000.)
            remaining_p2_ext_timeout = (timestamp_p2_ext_timeout - timestamp_now) * 1000.
            remaining_p6_ext_timeout = (timestamp_p6_ext_timeout - timestamp_now) * 1000.
            try:
                response_record = self._receive_response(sid=sid,
                                                         start_timeout=remaining_p2_ext_timeout,
                                                         end_timeout=remaining_p6_ext_timeout)
            except TimeoutError as exception:
                raise TimeoutError("P6*Client timeout reached.") from exception
            if response_record is None:  # timeout achieved - no following response
                raise TimeoutError(f"P2*Client timeout ({self.p2_ext_client_timeout} ms) reached after receiving "
                                   f"{len(response_records)} response pending messages "
                                   f"({bytes_to_hex(response_records[-1].payload)}).")
            response_records.append(response_record)
        self._update_measured_client_values(request_record=request_record, response_records=response_records)
        return request_record, tuple(response_records)

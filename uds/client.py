"""Implementation for :ref:`UDS Client <knowledge-base-client>` Simulation."""

__all__ = ["Client"]

from functools import wraps
from queue import Empty, SimpleQueue
from threading import Event, Lock, Thread
from time import perf_counter, sleep
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union
from warnings import warn

from uds.addressing import AddressingType
from uds.message import NRC, SERVICES_WITH_SUBFUNCTION, RequestSID, ResponseSID, UdsMessage, UdsMessageRecord
from uds.translator import TESTER_PRESENT
from uds.transport_interface import AbstractTransportInterface
from uds.utilities import (
    SPRMIB_MASK,
    InconsistencyError,
    MessageTransmissionNotStartedError,
    ReassignmentError,
    TimeMillisecondsAlias,
    ValueWarning,
)


class Client:
    """Simulation for UDS Client entity."""

    DEFAULT_P2_CLIENT_TIMEOUT: TimeMillisecondsAlias = 100  # P2Client_max > P2Server_max (default: 50 ms)
    """Default value of :ref:`P2Client <knowledge-base-p2-client>` timeout."""
    DEFAULT_P2_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 5050  # P2*Client_max > P2*Server_max (default: 5000 ms)
    """Default value of :ref:`P2*Client <knowledge-base-p2*-client>` timeout."""
    DEFAULT_P3_CLIENT: TimeMillisecondsAlias = DEFAULT_P2_CLIENT_TIMEOUT  # P3Client_Phys, P3Client_Func >= P2Client_max
    """Default value of :ref:`P3Client <knowledge-base-p3-client>` time parameters."""
    DEFAULT_P6_CLIENT_TIMEOUT: TimeMillisecondsAlias = 10000  # P6Client_max > P2Client_max
    """Default value of :ref:`P6Client <knowledge-base-p6-client>` timeout."""
    DEFAULT_P6_EXT_CLIENT_TIMEOUT: TimeMillisecondsAlias = 50000  # P6*Client_max > P2*Client_max
    """Default value of :ref:`P6*Client <knowledge-base-p6*-client>` timeout."""
    DEFAULT_S3_CLIENT: TimeMillisecondsAlias = 2000  # S3Client >= P3Client_Phys, P3Client_Func
    """Default value of :ref:`S3Client <knowledge-base-s3-client>` time parameter."""
    DEFAULT_RECEIVING_TASK_CYCLE: TimeMillisecondsAlias = 20
    """Default value of receiving task cycle."""

    def __init__(self,
                 transport_interface: AbstractTransportInterface,
                 p2_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_CLIENT_TIMEOUT,
                 p2_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P2_EXT_CLIENT_TIMEOUT,
                 p3_client_physical: TimeMillisecondsAlias = DEFAULT_P3_CLIENT,
                 p3_client_functional: TimeMillisecondsAlias = DEFAULT_P3_CLIENT,
                 p6_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_CLIENT_TIMEOUT,
                 p6_ext_client_timeout: TimeMillisecondsAlias = DEFAULT_P6_EXT_CLIENT_TIMEOUT,
                 s3_client: TimeMillisecondsAlias = DEFAULT_S3_CLIENT) -> None:
        """
        Configure Client for UDS communication.

        :param transport_interface: Transport Interface object for managing UDS communication.
        :param p2_client_timeout: Timeout value for P2Client parameter.
        :param p2_ext_client_timeout: Timeout value for P2*Client parameter.
        :param p3_client_physical: Value of P3Client_Phys time parameter.
        :param p3_client_physical: Value of P3Client_Func time parameter.
        :param p6_client_timeout: Timeout value for P6Client parameter.
        :param p6_ext_client_timeout: Timeout value for P*Client parameter.
        :param s3_client: Value of S3Client time parameter.
        """
        # TIMING PARAMETERS
        self.__p2_client_measured: Optional[TimeMillisecondsAlias] = None
        self.__p2_ext_client_measured: Optional[Tuple[TimeMillisecondsAlias, ...]] = None
        self.__p6_client_measured: Optional[TimeMillisecondsAlias] = None
        self.__p6_ext_client_measured: Optional[TimeMillisecondsAlias] = None
        # set default values to avoid errors on values assignment
        self.__p2_client_timeout = self.DEFAULT_P2_CLIENT_TIMEOUT
        self.__p2_ext_client_timeout = self.DEFAULT_P2_EXT_CLIENT_TIMEOUT
        self.__p3_client_physical = self.DEFAULT_P3_CLIENT
        self.__p3_client_functional = self.DEFAULT_P3_CLIENT
        self.__p6_client_timeout = self.DEFAULT_P6_CLIENT_TIMEOUT
        self.__p6_ext_client_timeout = self.DEFAULT_P6_EXT_CLIENT_TIMEOUT
        self.__s3_client = self.DEFAULT_S3_CLIENT
        # values assignment
        self.transport_interface = transport_interface
        self.p2_client_timeout = p2_client_timeout
        self.p2_ext_client_timeout = p2_ext_client_timeout
        self.p3_client_physical = p3_client_physical
        self.p3_client_functional = p3_client_functional
        self.p6_client_timeout = p6_client_timeout
        self.p6_ext_client_timeout = p6_ext_client_timeout
        self.s3_client = s3_client
        # tasks and threads
        self.__tester_present_task_event: Event = Event()
        self.__tester_present_task_event.clear()
        self.__tester_present_thread: Optional[Thread] = None
        self.__background_receiving_task_event: Event = Event()
        self.__background_receiving_task_event.clear()
        self.__break_in_receiving_event: Event = Event()
        self.__break_in_receiving_event.clear()
        self.__background_receiving_thread: Optional[Thread] = None
        self.__receiving_not_in_progress_event: Event = Event()
        self.__receiving_not_in_progress_event.set()
        self.__transmission_not_in_progress_event: Event = Event()
        self.__transmission_not_in_progress_event.set()
        self.__receiving_lock: Lock = Lock()
        self.__transmission_lock: Lock = Lock()
        self.__physical_transmission_lock: Lock = Lock()
        self.__functional_transmission_lock: Lock = Lock()
        # other
        self.__response_queue: SimpleQueue[UdsMessageRecord] = SimpleQueue()
        self.__last_physical_request: Optional[UdsMessageRecord] = None
        self.__last_physical_response: Optional[UdsMessageRecord] = None
        self.__last_functional_request: Optional[UdsMessageRecord] = None
        self.__last_functional_response: Optional[UdsMessageRecord] = None

    def __del__(self) -> None:
        """Safely finish all tasks."""
        if self.is_tester_present_sent:
            self.stop_tester_present()
        if self.is_background_receiving:
            self.stop_background_receiving()

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
        if self.__p2_client_timeout > self.p3_client_physical:
            warn(message="P3Client_Phys had to be updated as its values become less than P2Client timeout.",
                 category=UserWarning)
            self.p3_client_physical = value
        if self.__p2_client_timeout > self.p3_client_functional:
            warn(message="P3Client_Func had to be updated as its values become less than P2Client timeout.",
                 category=UserWarning)
            self.p3_client_functional = value
        if self.__p2_client_timeout > self.p6_client_timeout:
            warn(message="P6Client timeout had to be updated as its values become less than P2Client timeout.",
                 category=UserWarning)
            self.p6_client_timeout = value

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
        if self.__p2_ext_client_timeout > self.p6_ext_client_timeout:
            warn(message="P6*Client timeout had to be updated as its values become less than P2*Client timeout.",
                 category=UserWarning)
            self.p6_ext_client_timeout = value

    @property  # noqa: vulture
    def p2_ext_client_measured(self) -> Optional[Tuple[TimeMillisecondsAlias, ...]]:
        """
        Get last measured values of P2*Client parameter.

        :return: The last measured values or None if measurement was not performed.
        """
        return self.__p2_ext_client_measured

    @property
    def p3_client_physical(self) -> TimeMillisecondsAlias:
        """Get value of :ref:`P3Client_Phys <knowledge-base-p3-client-phys>` parameter."""
        return self.__p3_client_physical

    @p3_client_physical.setter
    def p3_client_physical(self, value: TimeMillisecondsAlias) -> None:
        """
        Set value of P3Client_Phys parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P3Client timeout value must be greater or equal than P2Client timeout.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p2_client_timeout:
            raise InconsistencyError("P3Client timeout value must be greater or equal than "
                                     f"P2Client timeout ({self.p2_client_timeout} ms).")
        self.__p3_client_physical = value
        if self.__p3_client_physical > self.s3_client:
            warn(message="S3Client had to be updated as its values become less than P3Client_Phys.",
                 category=UserWarning)
            self.s3_client = value

    @property
    def p3_client_functional(self) -> TimeMillisecondsAlias:
        """Get value of :ref:`P3Client_Func <knowledge-base-p3-client-func>` parameter."""
        return self.__p3_client_functional

    @p3_client_functional.setter
    def p3_client_functional(self, value: TimeMillisecondsAlias) -> None:
        """
        Set value of P3Client_Func parameter.

        :param value: value to set.

        :raise TypeError: Provided value is not int or float type.
        :raise ValueError: Provided time value must be a positive number.
        :raise InconsistencyError: P3Client timeout value must be greater or equal than P2Client timeout.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Provided time parameter value must be int or float type.")
        if value <= 0:
            raise ValueError("Provided timeout parameter value must be greater than 0.")
        if value < self.p2_client_timeout:
            raise InconsistencyError("P3Client timeout value must be greater or equal than "
                                     f"P2Client timeout ({self.p2_client_timeout} ms).")
        self.__p3_client_functional = value
        if self.__p3_client_functional > self.s3_client:
            warn(message="S3Client had to be updated as its values become less than P3Client_Func.",
                 category=UserWarning)
            self.s3_client = value

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
        if self.__p6_client_timeout > self.p6_ext_client_timeout:
            warn(message="P6*Client timeout had to be updated as its values become less than P6Client timeout.",
                 category=UserWarning)
            self.p6_ext_client_timeout = value

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
        if value < self.p3_client_physical:
            raise InconsistencyError("S3Client value must be greater or equal than "
                                     f"P3Client_Phys ({self.p2_client_timeout} ms).")
        if value < self.p3_client_functional:
            raise InconsistencyError("S3Client value must be greater or equal than "
                                     f"P3Client_Func ({self.p2_client_timeout} ms).")
        self.__s3_client = value

    @property
    def is_background_receiving(self) -> bool:
        """Get flag whether background receiving thread is running."""
        return self.__background_receiving_task_event.is_set()

    @property
    def is_tester_present_sent(self) -> bool:
        """Get flag whether Tester Present thread is running periodic sending."""
        return self.__tester_present_task_event.is_set()

    @property
    def is_ready_for_physical_transmission(self) -> bool:
        """
        Get flag whether Client is ready for physically addressed request message transmission.

        :return: True if no message is currently transmitted or received and the last physically addressed request
            was either received or timed-out (P2, P3 or P6), False otherwise.
        """
        return (self.__transmission_not_in_progress_event.is_set()
                and self.__receiving_not_in_progress_event.is_set()
                and (self.__last_physical_request is None
                     or self.__last_physical_response is not None
                     or perf_counter() > self.__last_physical_request.transmission_end_timestamp
                     + self.p3_client_physical / 1000.))

    @property
    def is_ready_for_functional_transmission(self) -> bool:
        """
        Get flag whether Client is ready for functionally addressed request message transmission.

        :return: True if no message is currently transmitted and
            P3Client_Func timeout was exceeded for the last functionally addressed request.
        """
        return (self.__transmission_not_in_progress_event.is_set()
                and (self.__last_functional_request is None
                     or perf_counter() > self.__last_functional_request.transmission_end_timestamp
                     + self.p3_client_functional / 1000.))

    def __update_p2_client_measured(self, value: TimeMillisecondsAlias) -> None:
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

    def __update_p2_ext_client_measured(self, *values: TimeMillisecondsAlias) -> None:
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

    def __update_p6_client_measured(self, value: TimeMillisecondsAlias) -> None:
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

    def __update_p6_ext_client_measured(self, value: TimeMillisecondsAlias) -> None:
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

    def __receiving_task(self, cycle: TimeMillisecondsAlias) -> None:
        """
        Schedule reception of a UDS message for a cyclic response collecting.

        :param cycle: Time (in milliseconds) used for this task cycle.
        """
        while self.__background_receiving_task_event.is_set():
            sleep(cycle / 1000.)
            if self.__break_in_receiving_event.is_set():
                continue
            try:
                response_record = self._receive_response(start_timeout=cycle,
                                                         end_timeout=self.p6_ext_client_timeout)
            except TimeoutError:
                pass
            else:
                self.__response_queue.put_nowait(response_record)

    def __send_tester_present_task(self, tester_present_request: UdsMessage) -> None:
        """
        Schedule a single Tester Present message transmission for a cyclic sending.

        :param tester_present_request: Tester Present request message to send.
        """
        period_s = self.s3_client / 1000.0
        next_call = perf_counter() + period_s
        sleep(period_s)
        while self.is_tester_present_sent:
            self._send_request(tester_present_request)
            next_call += period_s
            remaining_wait_s = next_call - perf_counter()
            if remaining_wait_s < 0:
                continue
            sleep(remaining_wait_s)

    def _update_measured_client_values(self,
                                       request_record: UdsMessageRecord,
                                       response_records: Sequence[UdsMessageRecord]) -> None:
        """
        Update measured timing parameters on Client side (P2Client, P2*Client, P6Client and P6*Client).

        :param request_record: Record of the last transmitted request message.
        :param response_records: Records of received responses to provided message.
        """
        p2_measured = response_records[0].transmission_start_timestamp - request_record.transmission_end_timestamp
        self.__update_p2_client_measured(round(p2_measured * 1000., 3))
        if len(response_records) > 1:
            p2_ext_measured_list = []
            for i, response_record in enumerate(response_records[1:]):
                _p2_ext_measured = (response_record.transmission_end_timestamp
                                    - response_records[i].transmission_end_timestamp)
                p2_ext_measured_list.append(round(_p2_ext_measured * 1000., 3))
            p6_ext_measured = (response_records[-1].transmission_end_timestamp
                               - request_record.transmission_end_timestamp)
            self.__update_p2_ext_client_measured(*p2_ext_measured_list)
            self.__update_p6_ext_client_measured(round(p6_ext_measured * 1000., 3))
        else:
            p6_measured = response_records[-1].transmission_end_timestamp - request_record.transmission_end_timestamp
            self.__update_p6_client_measured(round(p6_measured * 1000., 3))

    def _send_request(self, request: UdsMessage) -> UdsMessageRecord:
        """
        Send UDS Request Message in a threadsafe way.

        :param request: Request message to send.

        :return: Record of the request message that was sent.
        """
        if request.addressing_type == AddressingType.PHYSICAL:
            addressing_lock = self.__physical_transmission_lock
        elif request.addressing_type == AddressingType.FUNCTIONAL:
            addressing_lock = self.__functional_transmission_lock
        else:
            raise NotImplementedError("Request message with unexpected `addressing_type` attribute value was provided: "
                                      f"{request.addressing_type!r}")
        with addressing_lock:  # avoid queueing two request of the same addressing straight after each other
            self.wait_till_ready_for_transmission(request)
            with self.__transmission_lock:  # avoid two requests being transmitted at the same time
                self.__transmission_not_in_progress_event.clear()
                try:
                    request_record = self.transport_interface.send_message(request)
                finally:
                    self.__transmission_not_in_progress_event.set()
        if request.addressing_type == AddressingType.PHYSICAL:
            self.__last_physical_request = request_record
            self.__last_physical_response = None
        elif request.addressing_type == AddressingType.FUNCTIONAL:
            self.__last_functional_request = request_record
            self.__last_functional_response = None
        return request_record

    def _receive_response(self,
                          start_timeout: TimeMillisecondsAlias,
                          end_timeout: TimeMillisecondsAlias) -> UdsMessageRecord:
        """
        Receive UDS response message to previously sent request.

        :param start_timeout: Maximal time (in milliseconds) to wait for the start of the message reception.
        :param end_timeout: Maximal time (in milliseconds) to wait for the end of the message reception.

        :return: Record with response message received to the last UDS request message sent.
        """
        remaining_start_timeout_ms = start_timeout  # either P2Client or P2*Client
        remaining_end_timeout_ms = end_timeout  # either P6Client or P6*Client
        with self.__receiving_lock:
            self.__receiving_not_in_progress_event.clear()
            try:
                response_record = self.transport_interface.receive_message(
                    start_timeout=min(remaining_start_timeout_ms, remaining_end_timeout_ms),
                    end_timeout=remaining_end_timeout_ms)
            finally:
                self.__receiving_not_in_progress_event.set()
            if self.__last_physical_request is not None and self.__last_physical_response is None:
                sid = RequestSID(self.__last_physical_request.payload[0])
                if (self.is_response_to_request(response_message=response_record,
                                                request_message=self.__last_physical_request)
                        and not self.is_response_pending_message(response_message=response_record,
                                                                 request_sid=sid)):
                    self.__last_physical_response = response_record
            if self.__last_functional_request is not None and self.__last_functional_response is None:
                sid = RequestSID(self.__last_functional_request.payload[0])
                if (self.is_response_to_request(response_message=response_record,
                                                request_message=self.__last_functional_request)
                        and not self.is_response_pending_message(response_message=response_record,
                                                                 request_sid=sid)):
                    self.__last_functional_response = response_record
        return response_record

    def _receive_initial_response(self, request_record: UdsMessageRecord) -> Optional[UdsMessageRecord]:
        """
        Receive the first UDS response to a request message.

        :param request_record: Request message to which response is collected.

        :raise TimeoutError: Either P2Client or P6Client timeout was exceeded.

        :return: Received UDS Response Message.
            None if legitimately (either Functionally addressed request or with SPRMIB set) no response was received.
        """
        sid = RequestSID(request_record.payload[0])
        timestamp_start_timeout = request_record.transmission_end_timestamp + self.p2_client_timeout / 1000.
        timestamp_end_timeout = request_record.transmission_end_timestamp + self.p6_client_timeout / 1000.
        timestamp_now = perf_counter()
        while timestamp_now < timestamp_start_timeout and timestamp_now < timestamp_end_timeout:
            start_timeout_ms = (min(timestamp_start_timeout, timestamp_end_timeout) - timestamp_now) * 1000.
            end_timeout_ms = (timestamp_end_timeout - timestamp_now) * 1000.
            try:
                response_record = self._receive_response(start_timeout=start_timeout_ms,
                                                         end_timeout=end_timeout_ms)
            except MessageTransmissionNotStartedError as exception:
                if request_record.addressing_type == AddressingType.FUNCTIONAL:
                    return None
                if sid in SERVICES_WITH_SUBFUNCTION and request_record.payload[1] & SPRMIB_MASK:
                    return None
                raise TimeoutError("P2Client timeout exceeded.") from exception
            except TimeoutError as exception:
                raise TimeoutError("P6Client timeout exceeded.") from exception
            if self.is_response_to_request(response_message=response_record,
                                           request_message=request_record):
                p2_client = (response_record.transmission_start_timestamp
                             - request_record.transmission_end_timestamp) * 1000.
                if p2_client < self.p2_client_timeout:
                    return response_record
                else:
                    warn(message="Response message was received just after P2Client timeout was exceeded. "
                                  "It was put into response_queue.",
                         category=RuntimeWarning)
                    break
            self.__response_queue.put_nowait(response_record)
        raise TimeoutError("P2Client timeout exceeded.")

    def _receive_following_response(self,
                                    request_record: UdsMessageRecord,
                                    previous_response_record: UdsMessageRecord) -> UdsMessageRecord:
        """
        Receive the following (not the first one) UDS response to a request message.

        :param request_record: Request message to which response is collected.
        :param previous_response_record: Record of the proceeding UDS response.

        :raise TimeoutError: Either P2*Client or P6*Client timeout was exceeded.

        :return: Received UDS Response Message.
        """
        timestamp_start_timeout = (previous_response_record.transmission_end_timestamp
                                   + self.p2_ext_client_timeout / 1000.)
        timestamp_end_timeout = request_record.transmission_end_timestamp + self.p6_ext_client_timeout / 1000.
        timestamp_now = perf_counter()
        while timestamp_now < timestamp_start_timeout and timestamp_now < timestamp_end_timeout:
            start_timeout_ms = (min(timestamp_start_timeout, timestamp_end_timeout) - timestamp_now) * 1000.
            end_timeout_ms = (timestamp_end_timeout - timestamp_now) * 1000.
            try:
                response_record = self._receive_response(start_timeout=start_timeout_ms,
                                                         end_timeout=end_timeout_ms)
            except MessageTransmissionNotStartedError as exception:
                raise TimeoutError("P2*Client timeout exceeded.") from exception
            except TimeoutError as exception:
                raise TimeoutError("P6*Client timeout exceeded.") from exception
            if self.is_response_to_request(response_message=response_record,
                                           request_message=request_record):
                return response_record
            self.__response_queue.put_nowait(response_record)
        raise TimeoutError("P2*Client timeout exceeded.")

    @staticmethod
    def decorator_block_receiving(method: Callable) -> Callable:  # type: ignore
        """
        Decorate a method that blocks receiving task.

        :param method: Method to decorate.

        :return: Decorated method.
        """

        @wraps(method)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
            # pylint: disable=protected-access
            self._Client__break_in_receiving_event.set()
            self._Client__receiving_not_in_progress_event.wait(timeout=self.p6_ext_client_timeout)
            try:
                return_value = method(self, *args, **kwargs)
            finally:
                self._Client__break_in_receiving_event.clear()
            return return_value

        return wrapper

    @staticmethod
    def is_response_pending_message(response_message: Union[UdsMessage, UdsMessageRecord],
                                    request_sid: RequestSID) -> bool:
        """
        Check if provided UDS message is Response Pending Message to a diagnostic service of given SID.

        :param response_message: UDS Message to check.
        :param request_sid: SID value of the proceeding UDS request message.

        :raise TypeError: Provided value is neither instance of UdsMessage nor UdsMessageRecord class.

        :return: True if provided UDS message is a Negative Response Message (with Response Pending NRC)
            to a diagnostic service of given SID,
            False otherwise.
        """
        if not isinstance(response_message, (UdsMessage, UdsMessageRecord)):
            raise TypeError("Provided message value is not an instance of UdsMessageRecord class.")
        request_sid = RequestSID.validate_member(request_sid)
        if len(response_message.payload) != 3:
            return False
        return (response_message.payload[0] == ResponseSID.NegativeResponse
                and response_message.payload[1] == request_sid
                and response_message.payload[2] == NRC.RequestCorrectlyReceived_ResponsePending)

    def is_response_to_request(self,
                               response_message: Union[UdsMessage, UdsMessageRecord],
                               request_message: Union[UdsMessage, UdsMessageRecord]) -> bool:
        """
        Check if provided UDS message is a response message to a diagnostic service of given SID.

        :param response_message: UDS Message to check.
        :param request_message: UDS Request Message.

        :raise TypeError: Provided value is neither instance of UdsMessage nor UdsMessageRecord class.

        :return: True if provided UDS message is a response message to a diagnostic service of given SID,
            False otherwise.
        """
        if not isinstance(response_message, (UdsMessage, UdsMessageRecord)):
            raise TypeError("Provided message value is not an instance of UdsMessageRecord class.")
        if isinstance(request_message, UdsMessageRecord) and isinstance(response_message, UdsMessageRecord):
            if response_message.transmission_start_timestamp < request_message.transmission_end_timestamp:
                return False
        if request_message.addressing_type != response_message.addressing_type:
            rx_physical_params = dict(self.transport_interface.addressing_information.rx_physical_params)
            rx_physical_params.pop("addressing_type")
            rx_functional_params = dict(self.transport_interface.addressing_information.rx_functional_params)
            rx_functional_params.pop("addressing_type")
            if rx_physical_params != rx_functional_params:
                return False
        request_sid = RequestSID.validate_member(request_message.payload[0])
        response_sid = ResponseSID(response_message.payload[0])
        if request_sid.name == response_sid.name:
            return True  # Positive Response
        return (len(response_message.payload) == 3
                and response_sid == ResponseSID.NegativeResponse
                and response_message.payload[1] == request_sid)  # True if Negative Response, False otherwise

    def wait_till_ready_for_physical_transmission(self) -> None:
        """Wait till the client is ready to transmit physically addressed request message."""
        while not self.is_ready_for_physical_transmission:
            self.__transmission_not_in_progress_event.wait()
            self.__receiving_not_in_progress_event.wait()
            if self.__last_physical_request is not None:
                timestamp_now = perf_counter()
                timestamp_p3_timeout = (self.__last_physical_request.transmission_end_timestamp
                                        + self.p3_client_physical / 1000.)
                if timestamp_now < timestamp_p3_timeout:
                    sleep(timestamp_p3_timeout - timestamp_now)

    def wait_till_ready_for_functional_transmission(self) -> None:
        """Wait till the client is ready to transmit functionally addressed request message."""
        while not self.is_ready_for_functional_transmission:
            self.__transmission_not_in_progress_event.wait()
            if self.__last_functional_request is not None:
                timestamp_now = perf_counter()
                timestamp_p3_timeout = (self.__last_functional_request.transmission_end_timestamp
                                        + self.p3_client_functional / 1000.)
                if timestamp_now < timestamp_p3_timeout:
                    sleep(timestamp_p3_timeout - timestamp_now)

    def wait_till_ready_for_transmission(self, request: UdsMessage) -> None:
        """
        Wait till the client is ready for transmitting given request message.

        :param request: Request message to send.
        """
        if request.addressing_type == AddressingType.PHYSICAL:
            return self.wait_till_ready_for_physical_transmission()
        if request.addressing_type == AddressingType.FUNCTIONAL:
            return self.wait_till_ready_for_functional_transmission()
        raise NotImplementedError("Request message with unexpected `addressing_type` attribute value was provided: "
                                  f"{request.addressing_type!r}")

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
        while not self.__response_queue.empty():
            self.__response_queue.get_nowait()

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
            self.__tester_present_task_event.set()
            payload = TESTER_PRESENT.encode_request({
                "SubFunction": {
                    "suppressPosRspMsgIndicationBit": sprmib,
                    "zeroSubFunction": 0x00}
            })
            tester_present_message = UdsMessage(payload=payload,
                                                addressing_type=AddressingType.validate_member(addressing_type))
            self.__tester_present_thread = Thread(target=self.__send_tester_present_task,
                                                  args=(tester_present_message, ),
                                                  daemon=True)
            self.__tester_present_thread.start()

    def stop_tester_present(self) -> None:
        """Stop sending Tester Present cyclically."""
        if self.is_tester_present_sent:
            self.__tester_present_task_event.clear()
            if self.__tester_present_thread is not None:
                self.__tester_present_thread.join(timeout=self.s3_client / 1000.)
            self.__tester_present_thread = None
        else:
            warn("Cyclical sending of Tester Present is already stopped.",
                 category=UserWarning)

    def start_background_receiving(self, cycle: TimeMillisecondsAlias = DEFAULT_RECEIVING_TASK_CYCLE) -> None:
        """
        Start background receiving task.

        ..note:: All response messages sent to this Client while receiving is active,
            will be collected and accessible via :meth:`~uds.client.Client.get_response`
            and :meth:`~uds.client.Client.get_response_no_wait` methods.
        """
        if self.is_background_receiving:
            warn("Background receiving is already active.",
                 category=UserWarning)
        else:
            self.__background_receiving_task_event.set()
            self.__background_receiving_thread = Thread(target=self.__receiving_task,
                                                        kwargs={"cycle": cycle},
                                                        daemon=True)
            self.__background_receiving_thread.start()

    def stop_background_receiving(self) -> None:
        """Stop background receiving task."""
        if self.is_background_receiving:
            self.__background_receiving_task_event.clear()
            if self.__background_receiving_thread is not None:
                self.__background_receiving_thread.join()
            self.__background_receiving_thread = None
        else:
            warn("Receiving is already stopped.",
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
        sid = RequestSID(request.payload[0])
        request_record = self._send_request(request)
        response_records: List[UdsMessageRecord] = []
        initial_response = self._receive_initial_response(request_record)
        if initial_response is None:
            return request_record, tuple()
        response_records.append(initial_response)
        while self.is_response_pending_message(response_message=response_records[-1], request_sid=sid):
            following_response = self._receive_following_response(request_record=request_record,
                                                                  previous_response_record=response_records[-1])
            response_records.append(following_response)
        self._update_measured_client_values(request_record=request_record, response_records=response_records)
        return request_record, tuple(response_records)

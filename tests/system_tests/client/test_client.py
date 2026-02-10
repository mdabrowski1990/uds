__all__ = [
    "AbstractClientTests",
    "AbstractBaseClientFunctionalityTests",
    "AbstractClientTimeoutsTests",
    "AbstractClientErrorGuessing",
]

from abc import ABC, abstractmethod
from time import perf_counter, sleep

import pytest
from tests.system_tests import BaseSystemTests

from uds.addressing import AddressingType, TransmissionDirection
from uds.client import Client
from uds.message import RequestSID, UdsMessage, UdsMessageRecord
from uds.translator import BASE_TRANSLATOR
from uds.transport_interface import AbstractTransportInterface


class AbstractClientTests(BaseSystemTests, ABC):
    """Abstract definition of System tests for UDS Client."""

    transport_interface_1: AbstractTransportInterface
    transport_interface_2: AbstractTransportInterface

    @abstractmethod
    def _define_transport_interfaces(self):
        """
        Define Transport Interfaces used for these tests:
        - transport_interface_1 - Client side Transport Interface
        - transport_interface_2 - Sever side Transport Interface
        """

    @abstractmethod
    def configure_slow_message_reception(self):
        """Change configuration of Transport Interfaces to reach timeouts easily."""

    def setup_method(self):
        """
        Prepare for testing:
        - configue Transport Interfaces
        - define variables used during tests
        """
        self._define_transport_interfaces()
        super().setup_method()

    def teardown_method(self):
        """
        Clean after tests:
        - stop all initiated transmissions
        - kill all started tasks
        - disconnect Transport Interfaces
        """
        super().teardown_method()
        del self.transport_interface_1
        del self.transport_interface_2


class AbstractBaseClientFunctionalityTests(AbstractClientTests, ABC):
    """Common implementation of basic system tests related to Client Functionalities."""

    @pytest.mark.parametrize("addressing_type, sprmib", [
        (AddressingType.PHYSICAL, False),
        (AddressingType.FUNCTIONAL, True),
    ])
    @pytest.mark.parametrize("s3client", [250, 1000])
    def test_cyclic_tester_present(self, s3client, addressing_type, sprmib):
        """
        Check Client for cyclic sending of Tester Present messages.

        Procedure:
        1. Configure Client.
        2. Check that cyclic sending of Tester Present messages is not set in the Client.
        3. Start cyclic sending of Tester Present messages.
        4. Check that cyclic sending of Tester Present messages is set in the Client.
        5. Receive 10 messages on second Transport Interface.
        6. Check that cyclic sending of Tester Present messages is set in the Client.
        7. Stop cyclic sending of Tester Present messages.
        8. Check that cyclic sending of Tester Present messages is not set in the Client.
        9. Check that no more messages are sent by Client.
        10. Validate received messages.
            - Check that each message contains Tester Present request.
            - Check that addressing information of Tester Present packet matches the Client's addressing information.
            - Check that message transmission time is in line with S3Client parameter.
            - Check that direction attribute indicates that message was received.

        :param s3client: Cycle time for Tester Present message sending.
        :param addressing_type: Addressing Type to use for Tester Present messages transmission.
        :param sprmib: Suppress Positive Response Message Indication Bit value to set in Tester Present messages.
        """
        tp_payload = BASE_TRANSLATOR.encode(sid=RequestSID.TesterPresent,
                                            data_records_values={
                                                "SubFunction": {
                                                    "suppressPosRspMsgIndicationBit": sprmib,
                                                    "zeroSubFunction": 0x00
                                                }
                                            })
        addressing_params = dict(self.transport_interface_1.addressing_information.tx_physical_params) \
            if addressing_type == AddressingType.PHYSICAL \
            else dict(self.transport_interface_1.addressing_information.tx_functional_params)
        addressing_params.pop("addressing_type")  # in case Physical and Functional parameters were the same
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=100,
                        p6_client_timeout=200,
                        s3_client=s3client)
        # Check that cyclic sending of Tester Present messages is not set in the Client.
        assert client.is_tester_present_sent is False
        timestamp_start = perf_counter()
        # Start cyclic sending of Tester Present messages.
        client.start_tester_present(addressing_type=addressing_type, sprmib=sprmib)
        # Check that cyclic sending of Tester Present messages is set in the Client.
        assert client.is_tester_present_sent is True
        # Receive 10 messages on second Transport Interface.
        tp_messages_records = []
        for _ in range(10):
            tp_messages_records.append(self.transport_interface_2.receive_message(start_timeout=2 * s3client))
        # Check that cyclic sending of Tester Present messages is set in the Client.
        assert client.is_tester_present_sent is True
        # Stop cyclic sending of Tester Present messages.
        client.stop_tester_present()
        # Check that cyclic sending of Tester Present messages is not set in the Client.
        assert client.is_tester_present_sent is False
        # Check that no more messages are sent by Client.
        with pytest.raises(TimeoutError):
            self.transport_interface_2.receive_message(start_timeout=2 * s3client)
        # Validate received messages.
        for i, tp_message_record in enumerate(tp_messages_records, start=1):
            desired_timestamp = timestamp_start + i * s3client / 1000.
            assert tp_message_record.payload == tp_payload
            assert tp_message_record.direction == TransmissionDirection.RECEIVED
            for attribute_name, attribute_value in addressing_params.items():
                assert getattr(tp_message_record.packets_records[0], attribute_name) == attribute_value
            assert (desired_timestamp - self.TASK_TIMING_TOLERANCE / 1000.
                    <= tp_message_record.transmission_start_timestamp
                    == tp_message_record.transmission_end_timestamp
                    <= desired_timestamp + self.TASK_TIMING_TOLERANCE / 1000.)

    @pytest.mark.parametrize("delay_1, message_1, delay_2, message_2, timeout", [
        (
            50,
            UdsMessage(payload=[0x7E, 0x00], addressing_type=AddressingType.PHYSICAL),
            100,
            UdsMessage(payload=[0x50, 0x03], addressing_type=AddressingType.FUNCTIONAL),
            100
        ),
        (
            0,
            UdsMessage(payload=[0x63] + 1000 * [0x00], addressing_type=AddressingType.PHYSICAL),
            1000,
            UdsMessage(payload=[0x62, *range(256)], addressing_type=AddressingType.PHYSICAL),
            1500
        )
    ])
    def test_background_receiving(self, delay_1, message_1, delay_2, message_2, timeout):
        """
        Check background messages receiving by Client.

        Procedure:
        1. Configure Client.
        2. Check that background receiving is not set in the Client.
        3. Check that there were no requests sent by the Client.
        4. Check that there were no responses received by the Client.
        5. Start background receiving in the Client.
        6. Check that background receiving is set in the Client.
        7. Check that Client has not received any messages yet.
        8. Schedule transmission of two response messages to the Client.
        9. Wait till the two messages are received by the client.
        10. Check that Client has not received more messages.
        11. Check that background receiving is set in the Client.
        12. Stop background receiving in the Client.
        13. Check that background receiving is not set in the Client.
        14. Check that there were no requests sent by the Client.
        12. Validate received messages.
            - Check that received response messages matches the payload of transmitted messages.
            - Check that direction attribute indicates that message was received.
            - Check that the record of the last received message by the Client matches the second received message.

        :param delay_1: Time after which the first response message to be sent.
        :param message_1: The first response message.
        :param delay_2: Time after which the second response message to be sent.
        :param message_2: The second response message.
        :param timeout: Timeout for the second response message reception.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1)
        # Check that background receiving is not set in the Client.
        assert client.is_background_receiving is False
        # Check that there were no requests sent by the Client.
        assert client.last_request_sent is None
        # Check that there were no responses received by the Client.
        assert client.last_response_received is None
        assert client.get_response_no_wait() is None
        # Start background receiving in the Client.
        client.start_background_receiving()
        # Check that background receiving is set in the Client.
        assert client.is_background_receiving is True
        # Check that Client has not received any messages yet.
        assert client.get_response_no_wait() is None
        # Schedule transmission of two response messages to the Client.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=message_1,
                          delay=delay_1)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=message_2,
                          delay=delay_2)
        # Wait till the two messages are received by the client.
        message_record_1 = client.get_response(timeout=delay_2)
        message_record_2 = client.get_response(timeout=timeout)
        # Check that Client has not received more messages.
        assert client.get_response_no_wait() is None
        # Check that background receiving is set in the Client.
        assert client.is_background_receiving is True
        # Stop background receiving in the Client.
        client.stop_background_receiving()
        # Check that background receiving is not set in the Client.
        assert client.is_background_receiving is False
        # Check that there were no requests sent by the Client.
        assert client.last_request_sent is None
        # Validate received messages.
        assert message_record_1.payload == message_1.payload
        assert message_record_1.direction == TransmissionDirection.RECEIVED
        assert message_record_2.payload == message_2.payload
        assert message_record_2.direction == TransmissionDirection.RECEIVED
        assert client.last_response_received is message_record_2

    @pytest.mark.parametrize("request_message", [
        UdsMessage(payload=[0x3E, 0x00],
                   addressing_type=AddressingType.FUNCTIONAL),
        UdsMessage(payload=[0x22, 0x10, 0x00],
                   addressing_type=AddressingType.FUNCTIONAL),
        UdsMessage(payload=[0x10, 0x83],
                   addressing_type=AddressingType.PHYSICAL),
    ])
    @pytest.mark.parametrize("p2_client_timeout", [75, Client.DEFAULT_P2_CLIENT_TIMEOUT])
    def test_send_request_receive_responses__no_response(self, request_message, p2_client_timeout):
        """
        Check Client for sending UDS request and receiving no UDS response.

        Procedure:
        1. Configure Client.
        2. Schedule request message reception by the second Transport Interface.
        3. Check that there were no requests sent by the Client.
        4. Check that there were no responses received by the Client.
        5. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        6. Send UDS request message and receive UDS response by the Client.
        7. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        8. Validate request and response records.
            - Check that request message payload matches the payload of transmitted message.
            - Check that direction attribute of request message indicates that the message was transmitted.
            - Check that addressing type attribute in the message record is correctly set.
            - Check that no response message was received.
            - Check the last request sent by the client.
            - Check the last response received by the client.
        9. Validate timing parameters.
            - Check that waiting for response message lasted P2Client timeout.

        :param request_message: Request message to send by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p3_client_physical=2*p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=1000,
                             end_timeout=None)
        # Check that there were no requests sent by the Client.
        assert client.last_request_sent is None
        # Check that there were no responses received by the Client.
        assert client.last_response_received is None
        assert client.get_response_no_wait() is None
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS response by the Client.
        timestamp_before = perf_counter()
        request_record, response_records = client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Validate request and response records.
        assert isinstance(request_record, UdsMessageRecord)
        assert request_record.direction == TransmissionDirection.TRANSMITTED
        assert request_record.payload == request_message.payload
        assert request_record.addressing_type == request_message.addressing_type
        assert isinstance(response_records, tuple)
        assert len(response_records) == 0
        assert client.last_request_sent is request_record
        assert client.last_response_received is None
        # Validate timing parameters.
        if self.MAKE_TIMING_CHECKS:
            desired_timeout = request_record.transmission_end_timestamp + p2_client_timeout / 1000.
            assert (timestamp_before
                    <= request_record.transmission_start_timestamp
                    <= request_record.transmission_end_timestamp)
            assert (desired_timeout
                    <= timestamp_after
                    <= desired_timeout + self.TASK_TIMING_TOLERANCE / 1000.)

    @pytest.mark.parametrize("request_message, response_message", [
        (UdsMessage(payload=[0x3E, 0x00],
                    addressing_type=AddressingType.FUNCTIONAL),
         UdsMessage(payload=[0x7E, 0x00],
                    addressing_type=AddressingType.FUNCTIONAL)),
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x62, 0x10, 0x00, *range(255)],
                    addressing_type=AddressingType.PHYSICAL)),
        (UdsMessage(payload=[0x2E, 0x23, 0x45, *range(0, 255, 2), *(1, 255, 2)],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x7F, 0x2E, 0x7E],
                    addressing_type=AddressingType.PHYSICAL)),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p6_client_timeout, send_after", [
        (Client.DEFAULT_P2_CLIENT_TIMEOUT, Client.DEFAULT_P6_CLIENT_TIMEOUT, Client.DEFAULT_P2_CLIENT_TIMEOUT - 30),
        (250, 250, 150),
    ])
    def test_send_request_receive_responses__direct(self, request_message, response_message,
                                                    p2_client_timeout, p6_client_timeout, send_after):
        """
        Check Client for sending UDS request and receiving direct UDS response.

        Procedure:
        1. Configure Client.
        2. Schedule response message sending by the second Transport Interface.
        3. Schedule request message reception by the second Transport Interface.
        4. Check that there were no requests sent by the Client.
        5. Check that there were no responses received by the Client.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Send UDS request message and receive UDS response by the Client.
        8. Validate request and response records.
            - Check that messages' payload matches the payload of transmitted messages.
            - Check that direction attribute of request message indicates that the message was transmitted.
            - Check that direction attribute of response message indicates that the message was received.
            - Check that addressing type attribute in the message records is correctly set.
            - Check the last request sent by the client.
            - Check the last response received by the client.
        9. Validate timing parameters.
            - Check that timestamps of record messages matches the transmission schedule.
            - Check that measured P2Client and P6Client attributes were correctly updated in the Client.
            - Check that measured P2*Client and P6*Client attributes were not updated in the Client.

        :param request_message: Request message to send by Client.
        :param response_message: Response message to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param p6_client_timeout: P6Client timeout value to configure in Client.
        :param send_after: Time after which response message would be sent.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p6_client_timeout=p6_client_timeout,
                        p3_client_physical=2*p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout)
        # Schedule response message sending by the second Transport Interface.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_message,
                          delay=send_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=1000,
                             end_timeout=None)
        # Check that there were no requests sent by the Client.
        assert client.last_request_sent is None
        # Check that there were no responses received by the Client.
        assert client.last_response_received is None
        assert client.get_response_no_wait() is None
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS response by the Client.
        timestamp_before = perf_counter()
        request_record, response_records = client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Validate request and response records.
        assert isinstance(request_record, UdsMessageRecord)
        assert request_record.direction == TransmissionDirection.TRANSMITTED
        assert request_record.payload == request_message.payload
        assert request_record.addressing_type == request_message.addressing_type
        assert isinstance(response_records, tuple)
        assert len(response_records) == 1
        response_record = response_records[0]
        assert response_record.direction == TransmissionDirection.RECEIVED
        assert response_record.payload == response_message.payload
        assert response_record.addressing_type == response_message.addressing_type
        assert client.last_request_sent is request_record
        assert client.last_response_received is response_records[-1]
        # Validate timing parameters.
        assert (client.p2_client_measured
                == round((response_record.transmission_start_timestamp
                          - request_record.transmission_end_timestamp) * 1000., 3))
        assert (client.p6_client_measured
                == round((response_record.transmission_end_timestamp
                          - request_record.transmission_end_timestamp) * 1000., 3))
        assert client.p2_ext_client_measured is None
        assert client.p6_ext_client_measured is None
        if self.MAKE_TIMING_CHECKS:
            assert (timestamp_before
                    <= request_record.transmission_start_timestamp
                    <= request_record.transmission_end_timestamp
                    < response_record.transmission_start_timestamp
                    <= response_record.transmission_end_timestamp
                    <= timestamp_after)

    @pytest.mark.parametrize("request_message, response_messages", [
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x62, 0x10, 0x00, *range(255)],
                     addressing_type=AddressingType.PHYSICAL))),
        (UdsMessage(payload=[0x2E, 0x23, 0x45, *range(70)],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x72],
                     addressing_type=AddressingType.PHYSICAL))),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p2_ext_client_timeout, p6_ext_client_timeout, "
                             "start_after, delay, send_last_after", [
        (250, 1000, 2000, 200, 200, 1200),
        (100, 3000, 4000, 50, 1200, 3950),
    ])
    def test_send_request_receive_responses__delayed(self, request_message, response_messages,
                                                     p2_client_timeout, p2_ext_client_timeout, p6_ext_client_timeout,
                                                     start_after, delay, send_last_after):
        """
        Check Client for sending UDS request and receiving delayed UDS response.

        Procedure:
        1. Configure Client.
        2. Schedule response messages sending by the second Transport Interface.
        3. Schedule request message reception by the second Transport Interface.
        4. Check that there were no requests sent by the Client.
        5. Check that there were no responses received by the Client.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Send UDS request message and receive UDS responses by the Client.
        8. Validate request and response records.
            - Check that messages' payload matches the payload of transmitted messages.
            - Check that direction attribute of request message indicates that the message was transmitted.
            - Check that direction attribute of response messages indicates that the messages were received.
            - Check that addressing type attribute in the message records is correctly set.
            - Check the last request sent by the client.
            - Check the last response received by the client.
        9. Validate timing parameters.
            - Check that timestamps of record messages matches the transmission schedule.
            - Check that measured P2Client, P2*Client and P6*Client attributes were correctly updated in the Client.
            - Check that measured P6Client attribute was not updated in the Client.

        :param request_message: Request message to send by Client.
        :param response_messages: Response messages to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param p2_ext_client_timeout: P2*Client timeout value to configure in Client.
        :param p6_ext_client_timeout: P6*Client timeout value to configure in Client.
        :param start_after: Time after which the first Response Pending message would be sent.
        :param delay: Time after which following Response Pending messages are sent.
        :param send_last_after: Time after which the final response message would be sent.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p2_ext_client_timeout=p2_ext_client_timeout,
                        p6_client_timeout=p6_ext_client_timeout,
                        p6_ext_client_timeout=p6_ext_client_timeout,
                        p3_client_physical=2*p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout)
        # Schedule response messages sending by the second Transport Interface.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[0],
                          delay=start_after)
        for i, response_message in enumerate(response_messages[1:-1], start=1):
            self.send_message(transport_interface=self.transport_interface_2,
                              message=response_message,
                              delay=start_after + delay * i)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[-1],
                          delay=send_last_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Check that there were no requests sent by the Client.
        assert client.last_request_sent is None
        # Check that there were no responses received by the Client.
        assert client.last_response_received is None
        assert client.get_response_no_wait() is None
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS responses by the Client.
        timestamp_before = perf_counter()
        request_record, response_records = client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Validate request and response records.
        assert isinstance(request_record, UdsMessageRecord)
        assert request_record.direction == TransmissionDirection.TRANSMITTED
        assert request_record.payload == request_message.payload
        assert request_record.addressing_type == request_message.addressing_type
        assert isinstance(response_records, tuple)
        assert len(response_records) == len(response_messages)
        for i, response_record in enumerate(response_records):
            assert response_record.direction == TransmissionDirection.RECEIVED
            assert response_record.payload == response_messages[i].payload
            assert response_record.addressing_type == response_messages[i].addressing_type
        assert client.last_request_sent is request_record
        assert client.last_response_received is response_records[-1]
        # Validate timing parameters.
        assert (client.p2_client_measured
                == round((response_records[0].transmission_start_timestamp
                          - request_record.transmission_end_timestamp) * 1000., 3))
        assert isinstance(client.p2_ext_client_measured, tuple)
        assert len(client.p2_ext_client_measured) == len(response_records) - 1
        for i, response_record in enumerate(response_records[1:]):
            assert (client.p2_ext_client_measured[i]
                    == round((response_record.transmission_end_timestamp
                              - response_records[i].transmission_end_timestamp) * 1000., 3))
        assert (client.p6_ext_client_measured
                == round((response_records[-1].transmission_end_timestamp
                          - request_record.transmission_end_timestamp) * 1000., 3))
        assert client.p6_client_measured is None
        if self.MAKE_TIMING_CHECKS:
            assert (timestamp_before
                    <= request_record.transmission_start_timestamp
                    <= request_record.transmission_end_timestamp
                    < response_records[0].transmission_start_timestamp
                    <= response_records[0].transmission_end_timestamp
                    < response_records[-1].transmission_start_timestamp
                    <= response_records[-1].transmission_end_timestamp
                    <= timestamp_after)


class AbstractClientTimeoutsTests(AbstractClientTests, ABC):
    """Common implementation of system tests related to timeouts handling by the Client."""

    @pytest.mark.parametrize("request_message, response_message", [
        (UdsMessage(payload=[0x3E, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x7E, 0x00],
                    addressing_type=AddressingType.PHYSICAL)),
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x62, 0x10, 0x00, *range(10)],
                    addressing_type=AddressingType.PHYSICAL)),
        (UdsMessage(payload=[0x2E, 0x23, 0x45, *range(50, 100)],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x7F, 0x2E, 0x78],
                    addressing_type=AddressingType.PHYSICAL)),
    ])
    @pytest.mark.parametrize("p2_client_timeout, send_after", [
        (Client.DEFAULT_P2_CLIENT_TIMEOUT, Client.DEFAULT_P2_CLIENT_TIMEOUT + 30),
        (200, 230),
    ])
    def test_send_request_receive_responses__p2_timeout(self, request_message, response_message,
                                                        p2_client_timeout, send_after):
        """
        Check Client for P2Client timeout reporting.

        Procedure:
        1. Configure Client.
        2. Schedule response message sending by the second Transport Interface just after P2Client timeout is exceeded.
        3. Schedule request message reception by the second Transport Interface.
        4. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        5. Send UDS request message and receive UDS response by the Client.
            Expected: Exception for P2Client timeout raised.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Check that last request sent by the Client is updated.
        8. Check that last response received by the Client remains unassigned.
        9. Validate timing parameters.
            - Check that timeout was raised after P2Client timeout expired.

        :param request_message: Request message to send by Client.
        :param response_message: Response message to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param send_after: Time after which response message would be sent.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p6_client_timeout=2*p2_client_timeout,
                        p3_client_physical=2*p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout)
        # Schedule response message sending by the second Transport Interface just after P2Client timeout is exceeded.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_message,
                          delay=send_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS response by the Client.
        timestamp_before = perf_counter()
        with pytest.raises(TimeoutError, match="P2Client timeout"):
            client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Check that last request sent by the Client is updated.
        assert isinstance(client.last_request_sent, UdsMessageRecord)
        assert client.last_request_sent.payload == request_message.payload
        assert client.last_request_sent.addressing_type == request_message.addressing_type
        # Check that last response received by the Client remains unassigned.
        assert client.last_response_received is None
        # Validate timing parameters.
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (timestamp_after - timestamp_before) * 1000.
            assert (p2_client_timeout
                    <= receiving_time_ms
                    < p2_client_timeout + self.TASK_TIMING_TOLERANCE)
        # wait till message arrives
        sleep(2 * (send_after - p2_client_timeout) / 1000.)

    @pytest.mark.parametrize("request_message, response_message", [
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x62, 0x10, 0x00] + [*range(255)] * 20,
                    addressing_type=AddressingType.PHYSICAL)),
        (UdsMessage(payload=[0x22, *range(255, 100, -1)],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x62] + [*range(255, -1, -1)] * 100,
                    addressing_type=AddressingType.PHYSICAL)),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p6_client_timeout, send_after", [
        (Client.DEFAULT_P2_CLIENT_TIMEOUT, 2*Client.DEFAULT_P2_CLIENT_TIMEOUT, 20),
        (250, 750, 50),
    ])
    def test_send_request_receive_responses__p6_timeout(self, request_message, response_message,
                                                        p2_client_timeout, p6_client_timeout, send_after):
        """
        Check Client for P6Client timeout reporting.

        Procedure:
        1. Configure Client.
        2. Schedule response message sending by the second Transport Interface to exceed P6Client timeout.
        3. Schedule request message reception by the second Transport Interface.
        4. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        5. Send UDS request message and receive UDS response by the Client.
            Expected: Exception for P6Client timeout raised.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Check that last request sent by the Client is updated.
        8. Check that last response received by the Client remains unassigned.
        9. Validate timing parameters.
            - Check that timeout was raised after P6Client timeout expired.

        :param request_message: Request message to send by Client.
        :param response_message: Response message to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param p6_client_timeout: P6Client timeout value to configure in Client.
        :param send_after: Time after which response message would be sent.
        """
        # Configure Client.
        self.configure_slow_message_reception()
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p6_client_timeout=p6_client_timeout,
                        p3_client_physical=p6_client_timeout,
                        p3_client_functional=p6_client_timeout)
        # Schedule response message sending by the second Transport Interface to exceed P6Client timeout.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_message,
                          delay=send_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS response by the Client.
        timestamp_before = perf_counter()
        with pytest.raises(TimeoutError, match="P6Client timeout"):
            client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Check that last request sent by the Client is updated.
        assert isinstance(client.last_request_sent, UdsMessageRecord)
        assert client.last_request_sent.payload == request_message.payload
        assert client.last_request_sent.addressing_type == request_message.addressing_type
        # Check that last response received by the Client remains unassigned.
        assert client.last_response_received is None
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (timestamp_after - timestamp_before) * 1000.
            assert (p6_client_timeout
                    <= receiving_time_ms
                    < p6_client_timeout + send_after + self.TASK_TIMING_TOLERANCE)
        # wait till timeout occurs on server side
        sleep(1)

    @pytest.mark.parametrize("request_message, response_messages", [
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x62, 0x10, 0x00, *range(255)],
                     addressing_type=AddressingType.PHYSICAL))),
        (UdsMessage(payload=[0x2E, 0x23, 0x45, *range(70)],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x72],
                     addressing_type=AddressingType.PHYSICAL))),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p2_ext_client_timeout, p6_ext_client_timeout, "
                             "start_after, delay, send_last_after", [
        (250, 1000, 2000, 200, 200, 1500),
        (100, 1500, 3000, 50, 1750, 2500),
    ])
    def test_send_request_receive_responses__p2_ext_timeout(self, request_message, response_messages,
                                                            p2_client_timeout, p2_ext_client_timeout,
                                                            p6_ext_client_timeout,
                                                            start_after, delay, send_last_after):
        """
        Check Client for P2*Client timeout reporting.

        Procedure:
        1. Configure Client.
        2. Schedule response messages sending by the second Transport Interface with one of the messages scheduled
            after P2*Client timeout expired.
        3. Schedule request message reception by the second Transport Interface.
        4. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        5. Send UDS request message and receive UDS responses by the Client.
            Expected: Exception for P2*Client timeout raised.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Check that last request sent by the Client is updated.
        8. Check that last response received by the Client remains unassigned.
        9. Validate timing parameters.
            - Check that timeout was raised after P2*Client timeout expired.

        :param request_message: Request message to send by Client.
        :param response_messages: Response message to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param p2_ext_client_timeout: P2*Client timeout value to configure in Client.
        :param p6_ext_client_timeout: P6*Client timeout value to configure in Client.
        :param start_after: Time after which the first Response Pending message would be sent.
        :param delay: Time after which following Response Pending messages are sent.
        :param send_last_after: Time after which the final response message would be sent.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p2_ext_client_timeout=p2_ext_client_timeout,
                        p6_client_timeout=2*p2_client_timeout,
                        p6_ext_client_timeout=p6_ext_client_timeout,
                        p3_client_physical=2*p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout)
        # Schedule response messages sending by the second Transport Interface with one of the messages scheduled
        # after P2*Client timeout expired.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[0],
                          delay=start_after)
        for i, response_message in enumerate(response_messages[1:-1], start=1):
            self.send_message(transport_interface=self.transport_interface_2,
                              message=response_message,
                              delay=start_after + delay * i)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[-1],
                          delay=send_last_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS responses by the Client.
        timestamp_before = perf_counter()
        with pytest.raises(TimeoutError, match="P2\*Client timeout"):
            client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Check that last request sent by the Client is updated.
        assert isinstance(client.last_request_sent, UdsMessageRecord)
        assert client.last_request_sent.payload == request_message.payload
        assert client.last_request_sent.addressing_type == request_message.addressing_type
        # Check that last response received by the Client remains unassigned.
        assert client.last_response_received is None
        # Validate timing parameters.
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (timestamp_after - timestamp_before) * 1000.
            assert (start_after + p2_ext_client_timeout
                    <= receiving_time_ms
                    < p6_ext_client_timeout)
        # wait till message arrives
        sleep(2 * p2_ext_client_timeout / 1000.)

    @pytest.mark.parametrize("request_message, response_messages", [
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x62, 0x10, 0x00, *range(255)],
                     addressing_type=AddressingType.PHYSICAL))),
        (UdsMessage(payload=[0x2E, 0x23, 0x45, *range(70)],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x72],
                     addressing_type=AddressingType.PHYSICAL))),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p2_ext_client_timeout, p6_ext_client_timeout, "
                             "start_after, delay, send_last_after", [
        (250, 1500, 2000, 200, 1000, 2100),
        (100, 2000, 3000, 50, 1750, 3100),
    ])
    def test_send_request_receive_responses__p6_ext_timeout(self, request_message, response_messages,
                                                            p2_client_timeout, p2_ext_client_timeout,
                                                            p6_ext_client_timeout,
                                                            start_after, delay, send_last_after):
        """
        Check Client for P6*Client timeout reporting.

        Procedure:
        1. Configure Client.
        2. Schedule response messages sending by the second Transport Interface with the last message scheduled
            after P6*Client timeout expired.
        3. Schedule request message reception by the second Transport Interface.
        4. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        5. Send UDS request message and receive UDS responses by the Client.
            Expected: Exception for P6*Client timeout raised.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Check that last request sent by the Client is updated.
        8. Check that last response received by the Client remains unassigned.
        9. Validate timing parameters.
            - Check that timeout was raised after P6*Client timeout expired.

        :param request_message: Request message to send by Client.
        :param response_messages: Response message to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param p2_ext_client_timeout: P2*Client timeout value to configure in Client.
        :param p6_ext_client_timeout: P6*Client timeout value to configure in Client.
        :param start_after: Time after which the first Response Pending message would be sent.
        :param delay: Time after which following Response Pending messages are sent.
        :param send_last_after: Time after which the final response message would be sent.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p2_ext_client_timeout=p2_ext_client_timeout,
                        p6_client_timeout=2*p2_client_timeout,
                        p6_ext_client_timeout=p6_ext_client_timeout,
                        p3_client_physical=2*p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout)
        # Schedule response messages sending by the second Transport Interface with the last message scheduled
        # after P6*Client timeout expired.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[0],
                          delay=start_after)
        for i, response_message in enumerate(response_messages[1:-1], start=1):
            self.send_message(transport_interface=self.transport_interface_2,
                              message=response_message,
                              delay=start_after + delay * i)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[-1],
                          delay=send_last_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS responses by the Client.
        timestamp_before = perf_counter()
        with pytest.raises(TimeoutError, match="P6\*Client timeout"):
            client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Check that last request sent by the Client is updated.
        assert isinstance(client.last_request_sent, UdsMessageRecord)
        assert client.last_request_sent.payload == request_message.payload
        assert client.last_request_sent.addressing_type == request_message.addressing_type
        # Check that last response received by the Client remains unassigned.
        assert client.last_response_received is None
        # Validate timing parameters.
        if self.MAKE_TIMING_CHECKS:
            receiving_time_ms = (timestamp_after - timestamp_before) * 1000.
            assert (p6_ext_client_timeout
                    <= receiving_time_ms
                    < p6_ext_client_timeout + self.TASK_TIMING_TOLERANCE)
        # wait till message arrives
        sleep(2 * (send_last_after - p6_ext_client_timeout) / 1000.)

    @pytest.mark.parametrize("request_message_1, request_message_2", [
        (UdsMessage(payload=[0x10, 0x83],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x3E, 0x80],
                    addressing_type=AddressingType.PHYSICAL)),
        (UdsMessage(payload=[0x22, 0x10, 0x20],
                    addressing_type=AddressingType.FUNCTIONAL),
         UdsMessage(payload=[0x11, 0x01],
                    addressing_type=AddressingType.FUNCTIONAL)),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p3_client_physical, p3_client_functional", [
        (50, 100, 200),
        (20, 250, 50),
    ])
    def test_send_request_receive_responses__p3_timeout(self, request_message_1, request_message_2,
                                                        p2_client_timeout, p3_client_physical, p3_client_functional):
        """
        Check Client for P3Client timeout.

        Procedure:
        1. Configure Client.
        2. Schedule request message reception by the second Transport Interface.
        3. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        3. Send UDS request message 1 and receive UDS response by the Client.
        4. Schedule request message reception by the second Transport Interface.
        5. Send UDS request message 2 and receive UDS response by the Client.
        6. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        7. Validate request and response records.
            - Check that request messages' payload matches the payload of transmitted messages.
            - Check that direction attribute of request messages indicates that the messages were transmitted.
            - Check that addressing type attribute in the message records are correctly set.
            - Check that no response message was received.
            - Check that last request sent by the Client is the second request message.
            - Check that last response received by the Client remains unassigned.
        7. Validate timing parameters.
            - Time between transmission of request message 1 and request message 2 equals P3Client.

        :param request_message_1: Request message 1 to send by Client.
        :param request_message_2: Request message 2 to send by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param p3_client_physical: P3Client_Phys value to configure in Client.
        :param p3_client_functional: P3Client_Func value to configure in Client.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p3_client_physical=p3_client_physical,
                        p3_client_functional=p3_client_functional)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message 1 and receive UDS response by the Client.
        timestamp_before_1 = perf_counter()
        request_record_1, response_records_1 = client.send_request_receive_responses(request=request_message_1)
        timestamp_after_1 = perf_counter()
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=100,
                             end_timeout=None)
        # Send UDS request message 2 and receive UDS response by the Client.
        timestamp_before_2 = perf_counter()
        request_record_2, response_records_2 = client.send_request_receive_responses(request=request_message_2)
        timestamp_after_2 = perf_counter()
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Validate request and response records.
        assert isinstance(request_record_1, UdsMessageRecord)
        assert request_record_1.direction == TransmissionDirection.TRANSMITTED
        assert request_record_1.payload == request_message_1.payload
        assert request_record_1.addressing_type == request_message_1.addressing_type
        assert isinstance(response_records_1, tuple)
        assert len(response_records_1) == 0
        assert isinstance(request_record_2, UdsMessageRecord)
        assert request_record_2.direction == TransmissionDirection.TRANSMITTED
        assert request_record_2.payload == request_message_2.payload
        assert request_record_2.addressing_type == request_message_2.addressing_type
        assert isinstance(response_records_2, tuple)
        assert len(response_records_2) == 0
        assert client.last_request_sent is request_record_2
        assert client.last_response_received is None
        # Validate timing parameters.
        transmission_diff_ms = (request_record_2.transmission_start_timestamp
                                - request_record_1.transmission_end_timestamp) * 1000.
        p3_client = p3_client_physical \
            if request_message_1.addressing_type == AddressingType.PHYSICAL \
            else p3_client_functional
        assert (p3_client
                <= transmission_diff_ms
                <= p3_client + self.TASK_TIMING_TOLERANCE)


class AbstractClientErrorGuessing(AbstractClientTests, ABC):
    """Common implementation of error-guessing system tests for the Client."""

    @pytest.mark.parametrize("request_message, other_message, response_message", [
        (UdsMessage(payload=[0x3E, 0x00],
                    addressing_type=AddressingType.FUNCTIONAL),
         UdsMessage(payload=[0x54],
                    addressing_type=AddressingType.FUNCTIONAL),
         UdsMessage(payload=[0x7E, 0x00],
                    addressing_type=AddressingType.FUNCTIONAL)),
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x7E, 0x00],
                    addressing_type=AddressingType.FUNCTIONAL),
         UdsMessage(payload=[0x62, *range(255)],
                    addressing_type=AddressingType.PHYSICAL)),
        (UdsMessage(payload=[0x11, 0x01],
                    addressing_type=AddressingType.FUNCTIONAL),
         UdsMessage(payload=[0x2A, *range(100, 200)],
                    addressing_type=AddressingType.PHYSICAL),
         UdsMessage(payload=[0x51, 0x01],
                    addressing_type=AddressingType.FUNCTIONAL)),
    ])
    @pytest.mark.parametrize("p2_client_timeout, send_other_after, send_response_after", [
        (100, 10, 80),
        (250, 50, 150),
    ])
    def test_send_request_receive_responses__other_message(self, request_message, other_message, response_message,
                                                           p2_client_timeout, send_other_after, send_response_after):
        """
        Check Client for sending UDS request and receiving UDS response that is disturbed by other response message.

        Procedure:
        1. Configure Client.
        2. Schedule other response message sending by the second Transport Interface.
        3. Schedule response message sending by the second Transport Interface.
        4. Schedule request message reception by the second Transport Interface.
        5. Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        6. Send UDS request message and receive UDS response by the Client.
        7. Validate request and response records.
            - Check that messages' payload matches the payload of transmitted messages.
            - Check that direction attribute of request message indicates that the message was transmitted.
            - Check that direction attribute of response message indicates that the message was received.
            - Check that addressing type attribute in the message records is correctly set.
            - Check the last request sent by the client.
            - Check the last response received by the client.
        8. Check that other response message is put in background receiving queue.
        9. Validate timing parameters.
            - Check that timestamps of record messages matches the transmission schedule.
            - Check that measured P2Client and P6Client attributes were correctly updated in the Client.
            - Check that measured P2*Client and P6*Client attributes were not updated in the Client.

        :param request_message: Request message to send by Client.
        :param other_message: Other response message to receive by Client.
        :param response_message: Response message (to the request message) to receive by Client.
        :param p2_client_timeout: P2Client timeout value to configure in Client.
        :param send_other_after: Time after which other response message would be sent.
        :param send_response_after: Time after which response message would be sent.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p3_client_functional=2*p2_client_timeout,
                        p3_client_physical=2*p2_client_timeout)
        # Schedule other response message sending by the second Transport Interface.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=other_message,
                          delay=send_other_after)
        # Schedule response message sending by the second Transport Interface.
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_message,
                          delay=send_response_after)
        # Schedule request message reception by the second Transport Interface.
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             start_timeout=1000,
                             end_timeout=None)
        # Check that measured values of P2Client, P2*Client, P6Client and P6*Client are not set in the Client.
        assert client.p2_client_measured is None
        assert client.p2_ext_client_measured is None
        assert client.p6_client_measured is None
        assert client.p6_ext_client_measured is None
        # Send UDS request message and receive UDS response by the Client.
        timestamp_before = perf_counter()
        request_record, response_records = client.send_request_receive_responses(request=request_message)
        timestamp_after = perf_counter()
        # Validate request and response records.
        assert isinstance(request_record, UdsMessageRecord)
        assert request_record.direction == TransmissionDirection.TRANSMITTED
        assert request_record.payload == request_message.payload
        assert request_record.addressing_type == request_message.addressing_type
        assert isinstance(response_records, tuple)
        assert len(response_records) == 1
        response_record = response_records[0]
        assert response_record.direction == TransmissionDirection.RECEIVED
        assert response_record.payload == response_message.payload
        assert response_record.addressing_type == response_message.addressing_type
        assert client.last_request_sent is request_record
        assert client.last_response_received is response_records[-1]
        # Check that other response message is put in background receiving queue.
        other_response_record = client.get_response_no_wait()
        assert isinstance(other_response_record, UdsMessageRecord)
        assert other_response_record.direction == TransmissionDirection.RECEIVED
        assert other_response_record.payload == other_message.payload
        assert other_response_record.addressing_type == other_message.addressing_type
        # Validate timing parameters.
        assert (client.p2_client_measured
                == round((response_record.transmission_start_timestamp
                          - request_record.transmission_end_timestamp) * 1000., 3))
        assert (client.p6_client_measured
                == round((response_record.transmission_end_timestamp
                          - request_record.transmission_end_timestamp) * 1000., 3))
        assert client.p2_ext_client_measured is None
        assert client.p6_ext_client_measured is None
        if self.MAKE_TIMING_CHECKS:
            assert (timestamp_before
                    <= request_record.transmission_start_timestamp
                    <= request_record.transmission_end_timestamp
                    < response_record.transmission_start_timestamp
                    <= response_record.transmission_end_timestamp
                    <= timestamp_after)

    @pytest.mark.parametrize("addressing_type, sprmib, messages, s3_client, delay", [
        (AddressingType.PHYSICAL,
         False,
         [
             UdsMessage(payload=[0x7E, 0x00],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x6A, 0x00, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x7E, 0x00],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x6A, 0x01, *range(60,180)],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x7E, 0x00],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x6A, 0x00, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x7E, 0x00],
                        addressing_type=AddressingType.PHYSICAL),
         ],
         500,
         250),
        (AddressingType.FUNCTIONAL,
         True,
         [
             UdsMessage(payload=[0x7E, 0x00],
                        addressing_type=AddressingType.FUNCTIONAL),
             UdsMessage(payload=[0x6A, 0x00, 0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x6A, 0x01, *range(60, 180)],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x6A, 0x00, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
                        addressing_type=AddressingType.PHYSICAL),
             UdsMessage(payload=[0x7E, 0x80],
                        addressing_type=AddressingType.FUNCTIONAL),
         ],
         1000,
         300),
    ])
    def test_background_receiving_and_tester_present(self, addressing_type, sprmib, messages,
                                                     s3_client, delay):
        """
        Check Client for receiving messages in the background and send Tester Present cyclically at the same time.

        Procedure:
        1. Configure Client.
        2. Schedule response messages sending by the second Transport Interface.
        3. Start background receiving in the Client.
        4. Start cyclic sending of Tester Present messages.
        5. Get records of sent and received messages.
            - Check that record of the last received message is stored in `last_response_received` attribute.
            - Get records of the last sent request message from `last_request_sent` attribute
        6. Stop background receiving in the Client.
        7. Stop cyclic sending of Tester Present messages.
        8. Validate collected messages records.
            - Check that messages timing matches the schedule.
            - Check messages payload and other attributes that were set.

        :param addressing_type: Addressing Type to use for Tester Present messages transmission.
        :param sprmib: Suppress Positive Response Message Indication Bit value to set in Tester Present messages.
        :param messages: Response message to receive by Client.
        :param s3_client: S3Client value to configure in Client.
        :param delay: Time between following response message transmission.
        """
        # Configure Client.
        client = Client(transport_interface=self.transport_interface_1,
                        s3_client=s3_client)
        # Schedule response messages sending by the second Transport Interface.
        for i, message in enumerate(messages, start=1):
            self.send_message(transport_interface=self.transport_interface_2,
                              message=message,
                              delay=i * delay)
        # Start background receiving in the Client.
        client.start_background_receiving()
        # Start cyclic sending of Tester Present messages.
        client.start_tester_present(addressing_type=addressing_type, sprmib=sprmib)
        # Get records of sent and received messages.
        received_records = []
        sent_records = []
        for _ in messages:
            received_records.append(client.get_response(timeout=2 * delay))
            assert client.last_response_received == received_records[-1]
            if client.last_request_sent is not None and client.last_request_sent not in sent_records:
                sent_records.append(client.last_request_sent)
        # Start background receiving in the Client.
        client.stop_tester_present()
        # Stop cyclic sending of Tester Present messages.
        client.stop_background_receiving()
        # Validate collected messages records.
        for i, record in enumerate(sent_records):
            assert isinstance(record, UdsMessageRecord)
            assert record.addressing_type == addressing_type
            assert len(record.payload) == 2
            assert record.payload[0] == 0x3E
            assert record.payload[1] == (0x80 if sprmib else 0x00)
            if i != 0:
                delay_between_tp_ms = (record.transmission_end_timestamp
                                       - sent_records[i-i].transmission_end_timestamp) * 1000.
                assert (s3_client - self.TASK_TIMING_TOLERANCE
                        <= delay_between_tp_ms
                        <= s3_client + self.TASK_TIMING_TOLERANCE)
        assert len(received_records) == len(messages)
        for i, record in enumerate(received_records):
            message = messages[i]
            assert isinstance(record, UdsMessageRecord)
            assert record.addressing_type == message.addressing_type
            assert record.payload == bytes(message.payload)

    def test_background_receiving_and_send_request_receive_responses(self):
        ... #TODO

    def test_tester_present_and_send_request_receive_responses(self):
        ... #TODO


    # # Tester Present
    #
    # @pytest.mark.parametrize("addressing_type, sprmib, s3_client", [
    #     (AddressingType.FUNCTIONAL, True, 1000),
    #     (AddressingType.PHYSICAL, False, 500),
    # ])
    # def test_start_stop_tester_present(self, addressing_type, sprmib, s3_client):
    #     """
    #     Check for starting and stopping cyclical Tester Present sending.
    #
    #     Procedure:
    #     1. Configure Client.
    #     2. Start cyclical Tester Present transmission.
    #     3. Receive 5 Tester Present messages.
    #     4. Stop cyclical Tester Present transmission.
    #     5. Check Tester Present message reception.
    #         Expected: No message received.
    #     6. Validate received Tester Present records.
    #         Expected: Received Tester Present records period and attributes matches preconfigured values.
    #
    #     :param addressing_type: Addressing Type to use for Tester Present transmission.
    #     :param sprmib: Whether Tester Present message have suppressPosRspMsgIndicationBit set.
    #     :param s3_client: S3Client value to configure in Client.
    #     """
    #     client = Client(transport_interface=self.transport_interface_1,
    #                     p6_client_timeout=s3_client,
    #                     s3_client=s3_client)
    #     tester_present_records: List[UdsMessageRecord] = []
    #     client.start_tester_present(addressing_type=addressing_type, sprmib=sprmib)
    #     for i in range(5):
    #         tester_present_records.append(self.transport_interface_2.receive_message(start_timeout=2 * s3_client))
    #     client.stop_tester_present()
    #     with pytest.raises(TimeoutError):
    #         self.transport_interface_2.receive_message(start_timeout=2 * s3_client)
    #     # check sent messages
    #     payload = b"\x3E\x80" if sprmib else b"\x3E\x00"
    #     assert all([tp_record.payload == payload for tp_record in tester_present_records])
    #     rx_physical_params = dict(self.transport_interface_2.addressing_information.rx_physical_params)
    #     rx_functional_params = dict(self.transport_interface_2.addressing_information.rx_functional_params)
    #     rx_physical_params.pop("addressing_type")
    #     rx_functional_params.pop("addressing_type")
    #     if rx_physical_params != rx_functional_params:  # make sure addressing parameters differ
    #         assert all([tp_record.addressing_type == addressing_type for tp_record in tester_present_records])
    #     # performance checks
    #     if self.MAKE_TIMING_CHECKS:
    #         for i, tp_record in enumerate(tester_present_records[1:]):
    #             s3_client_measured = (tp_record.transmission_start_time.timestamp()
    #                                   - tester_present_records[i].transmission_start_time.timestamp())
    #             assert (s3_client - self.TASK_TIMING_TOLERANCE
    #                     <=  s3_client_measured * 1000.
    #                     <= s3_client + self.TASK_TIMING_TOLERANCE)
    #
    # @pytest.mark.parametrize("addressing_type, sprmib, s3_client", [
    #     (AddressingType.FUNCTIONAL, True, 1000),
    #     (AddressingType.PHYSICAL, False, 500),
    # ])
    # def test_restart_tester_present(self, addressing_type, sprmib, s3_client):
    #     """
    #     Check for restarting cyclical Tester Present sending.
    #
    #     Procedure:
    #     1. Configure Client.
    #     2. Start cyclical Tester Present transmission.
    #     3. Receive 1 Tester Present message.
    #     4. Stop cyclical Tester Present transmission.
    #     5. Check Tester Present message reception.
    #         Expected: No message received.
    #     6. Restart cyclical Tester Present transmission.
    #     7. Receive 1 Tester Present message.
    #     8. Check Tester Present message reception.
    #         Expected: No message received.
    #     6. Validate received Tester Present records.
    #         Expected: Received Tester Present records attributes matches preconfigured values.
    #
    #     :param addressing_type: Addressing Type to use for Tester Present transmission.
    #     :param sprmib: Whether Tester Present message have suppressPosRspMsgIndicationBit set.
    #     """
    #     client = Client(transport_interface=self.transport_interface_1,
    #                     p6_client_timeout=s3_client,
    #                     s3_client=s3_client)
    #     client.start_tester_present(addressing_type=addressing_type, sprmib=sprmib)
    #     tester_present_record_1 = self.transport_interface_2.receive_message(start_timeout=2 * s3_client)
    #     client.stop_tester_present()
    #     with pytest.raises(TimeoutError):
    #         self.transport_interface_2.receive_message(start_timeout=2 * s3_client)
    #     client.start_tester_present(addressing_type=addressing_type, sprmib=sprmib)
    #     tester_present_record_2 = self.transport_interface_2.receive_message(start_timeout=2 * s3_client)
    #     client.stop_tester_present()
    #     with pytest.raises(TimeoutError):
    #         self.transport_interface_2.receive_message(start_timeout=2 * s3_client)
    #     # check sent messages
    #     payload = b"\x3E\x80" if sprmib else b"\x3E\x00"
    #     assert tester_present_record_1.payload == tester_present_record_2.payload == payload
    #     assert tester_present_record_1.addressing_type == tester_present_record_2.addressing_type  # do not compare with addressing_type in case the same rx and tx AI parameters
    #
    # # background receiving
    #
    # @pytest.mark.parametrize("message", [
    #     UdsMessage(payload=[0x7E, 0x00], addressing_type=AddressingType.FUNCTIONAL),
    #     UdsMessage(payload=[*range(255)], addressing_type=AddressingType.PHYSICAL),
    # ])
    # @pytest.mark.parametrize("cycle", [10, 500])
    # def test_receive_message_without_request(self, message, cycle):
    #     """
    #     Check for receiving messages in the background.
    #
    #     Procedure:
    #     1. Configure Client.
    #     2. Check that messages stored.
    #         Expected: No message is stored.
    #     3. Start receiving.
    #     4. Check that messages stored.
    #         Expected: No message is stored.
    #     5. Send a message to the client.
    #     6. Wait for message transmission.
    #     7. Stop receiving.
    #     8. Check received messages.
    #         Expected: 1 message stored.
    #
    #     :param message: Message to be received.
    #     :param cycle: Receiving message cycle.
    #     """
    #     client = Client(transport_interface=self.transport_interface_1)
    #     assert client.get_response_no_wait() is None
    #     client.start_background_receiving(cycle=cycle)
    #     assert client.get_response(timeout=1000) is None
    #     self.transport_interface_2.send_message(message)
    #     sleep(1)
    #     client.stop_background_receiving()
    #     record = client.get_response_no_wait()
    #     assert isinstance(record, UdsMessageRecord)
    #     assert record.payload == message.payload
    #     assert record.addressing_type == message.addressing_type
    #     assert record.direction == TransmissionDirection.RECEIVED
    #     assert client.get_response_no_wait() is None
    #
    # @pytest.mark.parametrize("request_message, response_message, other_message", [
    #     (
    #         UdsMessage(payload=[0x19, 0x02, 0xFF],
    #                    addressing_type=AddressingType.FUNCTIONAL),
    #         UdsMessage(payload=[0x59, 0x02, 0xFF],
    #                    addressing_type=AddressingType.FUNCTIONAL),
    #         UdsMessage(payload=[0x7E, 0x00],
    #                    addressing_type=AddressingType.FUNCTIONAL),
    #     ),
    #     (
    #         UdsMessage(payload=[0x22, 0x10, 0x00],
    #                    addressing_type=AddressingType.PHYSICAL),
    #         UdsMessage(payload=[0x62, 0x10, 0x00, *range(255)],
    #                    addressing_type=AddressingType.PHYSICAL),
    #         UdsMessage(payload=[0x7E, 0x00],
    #                    addressing_type=AddressingType.PHYSICAL),
    #     ),
    # ])
    # @pytest.mark.parametrize("send_after, period, pause", [
    #     (450, 10, 2200),
    #     (250, 15, 2000),
    # ])
    # def test_send_request_while_receiving(self, request_message, response_message, other_message,
    #                                       send_after, period, pause):
    #     """
    #     Check for receiving messages in the background.
    #
    #     Procedure:
    #     1. Configure Client.
    #     2. Start receiving.
    #     3. Schedule message to be received by Client (1 answer to the request and 20 other messages).
    #     4. Send message by client and received response.
    #         Expected: Request sent and response received.
    #     5. Wait for all messages delivery.
    #     6. Check sent and received messages.
    #         Expected: All received messages received by Client (both before and after request sending).
    #
    #     :param request_message: Request message to send by Client.
    #     :param response_message: Response message to receive by Client.
    #     :param other_message: Other message to received by Client.
    #     :param send_after: Time in milliseconds to send response after.
    #     :param period: Period used for sending other messages.
    #     """
    #     client = Client(transport_interface=self.transport_interface_1,
    #                     p2_client_timeout=1000)
    #     client.start_background_receiving()
    #     self.send_message(transport_interface=self.transport_interface_2,
    #                       message=response_message,
    #                       delay=send_after)
    #     for i in range(1, 21):
    #         delay = i*period
    #         if i > 2:
    #             delay += pause
    #         self.send_message(transport_interface=self.transport_interface_2,
    #                           message=other_message,
    #                           delay=delay)
    #     request_record, response_records = client.send_request_receive_responses(request=request_message)
    #     sleep(3)  # wait for all messages to be received
    #     client.stop_background_receiving()
    #     # check sent message
    #     assert isinstance(request_record, UdsMessageRecord)
    #     assert request_record.direction == TransmissionDirection.TRANSMITTED
    #     assert request_record.payload == request_message.payload
    #     assert request_record.addressing_type == request_message.addressing_type
    #     # check received response
    #     assert isinstance(response_records, tuple)
    #     assert len(response_records) == 1
    #     response_record = response_records[0]
    #     assert response_record.direction == TransmissionDirection.RECEIVED
    #     assert response_record.payload == response_message.payload
    #     assert response_record.addressing_type == response_message.addressing_type
    #     # check other messages
    #     for _ in range(20):
    #         other_message_record = client.get_response_no_wait()
    #         assert isinstance(other_message_record, UdsMessageRecord)
    #         assert other_message_record.direction == TransmissionDirection.RECEIVED
    #         assert other_message_record.payload == other_message_record.payload
    #         assert other_message_record.addressing_type == other_message_record.addressing_type

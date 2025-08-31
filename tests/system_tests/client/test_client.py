from abc import ABC, abstractmethod
from datetime import datetime
from time import time

import pytest
from tests.system_tests import BaseSystemTests

from uds.addressing import AddressingType, TransmissionDirection
from uds.client import Client
from uds.message import UdsMessage, UdsMessageRecord
from uds.transport_interface import AbstractTransportInterface


class AbstractClientTests(BaseSystemTests, ABC):
    """System tests for UDS Client."""

    transport_interface_1: AbstractTransportInterface
    transport_interface_2: AbstractTransportInterface

    @abstractmethod
    def _define_transport_interfaces(self):
        """
        Define Transport Interfaces used for these tests:
        - transport_interface_1 - Client side Transport Interface
        - transport_interface_2 - Sever side Transport Interface
        """

    def setup_method(self):
        """Prepare Transport Interfaces for testing."""
        self._define_transport_interfaces()
        super().setup_method()

    def teardown_method(self):
        """Finish all tasks that were open during test."""
        del self.transport_interface_1
        del self.transport_interface_2

    # simple: send - receive

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
        (100, 100, 50),
    ])
    def test_send_request_receive_direct_response(self, request_message, response_message,
                                                  p2_client_timeout, p6_client_timeout, send_after):
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p6_client_timeout=p6_client_timeout)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_message,
                          delay=send_after)
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             timeout=1000)
        time_before = time()
        request_record, response_records = client.send_request_receive_responses(request=request_message)
        time_after = time()
        # check sent message
        assert isinstance(request_record, UdsMessageRecord)
        assert request_record.direction == TransmissionDirection.TRANSMITTED
        assert request_record.payload == request_message.payload
        assert request_record.addressing_type == request_message.addressing_type
        # check received response
        assert isinstance(response_records, tuple)
        assert len(response_records) == 1
        response_record = response_records[0]
        assert response_record.direction == TransmissionDirection.RECEIVED
        assert response_record.payload == response_message.payload
        assert response_record.addressing_type == response_message.addressing_type
        # measured time parameters
        assert (client.p2_client_measured
                == (response_record.transmission_start - request_record.transmission_end).total_seconds() * 1000.)
        assert (client.p6_client_measured
                == (response_record.transmission_end - request_record.transmission_end).total_seconds() * 1000.)
        assert client.p2_ext_client_measured is None
        assert client.p6_ext_client_measured is None
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= request_record.transmission_start
                    <= request_record.transmission_end
                    < response_record.transmission_start
                    <= response_record.transmission_end
                    <= datetime.fromtimestamp(time_after + self.TIMESTAMP_TOLERANCE / 1000.))

    @pytest.mark.parametrize("request_message, response_messages", [
        (UdsMessage(payload=[0x22, 0x10, 0x00],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x22, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x62, 0x10, 0x00, *range(255)],
                     addressing_type=AddressingType.PHYSICAL))),
        (UdsMessage(payload=[0x2E, 0x23, 0x45, *range(0, 255, 2), *(1, 255, 2)],
                    addressing_type=AddressingType.PHYSICAL),
         (UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x7F, 0x2E, 0x78],
                     addressing_type=AddressingType.PHYSICAL),
          UdsMessage(payload=[0x6E, 0x23, 0x45],
                     addressing_type=AddressingType.PHYSICAL))),
    ])
    @pytest.mark.parametrize("p2_client_timeout, p6_client_timeout, "
                             "p2_ext_client_timeout, p6_ext_client_timeout, "
                             "start_after, delay, send_after", [
        (Client.DEFAULT_P2_CLIENT_TIMEOUT, Client.DEFAULT_P6_CLIENT_TIMEOUT,
         Client.DEFAULT_P2_EXT_CLIENT_TIMEOUT, Client.DEFAULT_P6_EXT_CLIENT_TIMEOUT,
         20, 1000, 500),
        (100, 100, 1000, 5000,
         50, 750, 80),
    ])
    def test_send_request_receive_delayed_response(self, request_message, response_messages,
                                                   p2_client_timeout, p6_client_timeout,
                                                   p2_ext_client_timeout, p6_ext_client_timeout,
                                                   start_after, delay, send_after):
        client = Client(transport_interface=self.transport_interface_1,
                        p2_client_timeout=p2_client_timeout,
                        p6_client_timeout=p6_client_timeout,
                        p2_ext_client_timeout=p2_ext_client_timeout,
                        p6_ext_client_timeout=p6_ext_client_timeout)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[0],
                          delay=start_after)
        for i, response_message in enumerate(response_messages[1:-1], start=1):
            self.send_message(transport_interface=self.transport_interface_2,
                              message=response_message,
                              delay=start_after + delay * i)
        self.send_message(transport_interface=self.transport_interface_2,
                          message=response_messages[-1],
                          delay=start_after + delay * len(response_messages[1:-1]) + send_after)
        self.receive_message(transport_interface=self.transport_interface_2,
                             delay=0,
                             timeout=10000)
        time_before = time()
        request_record, response_records = client.send_request_receive_responses(request=request_message)
        time_after = time()
        # check sent message
        assert isinstance(request_record, UdsMessageRecord)
        assert request_record.direction == TransmissionDirection.TRANSMITTED
        assert request_record.payload == request_message.payload
        assert request_record.addressing_type == request_message.addressing_type
        # check received response
        assert isinstance(response_records, tuple)
        assert len(response_records) == len(response_messages)
        for i, response_record in enumerate(response_records):
            assert response_record.direction == TransmissionDirection.RECEIVED
            assert response_record.payload == response_messages[i].payload
            assert response_record.addressing_type == response_messages[i].addressing_type
        # measured time parameters
        assert (client.p2_client_measured
                == (response_records[0].transmission_start - request_record.transmission_end).total_seconds() * 1000.)
        assert isinstance(client.p2_ext_client_measured, tuple)
        assert len(client.p2_ext_client_measured) == len(response_records) - 1
        for i, response_record in enumerate(response_records[1:]):
            assert (client.p2_ext_client_measured[i]
                    == (response_record.transmission_end - response_records[i].transmission_end).total_seconds() * 1000.)
        assert (client.p6_ext_client_measured
                == (response_records[-1].transmission_end - request_record.transmission_end).total_seconds() * 1000.)
        assert client.p6_client_measured is None
        # performance checks
        if self.MAKE_TIMING_CHECKS:
            assert (datetime.fromtimestamp(time_before - self.TIMESTAMP_TOLERANCE / 1000.)
                    <= request_record.transmission_start
                    <= request_record.transmission_end
                    < response_records[0].transmission_start
                    <= response_records[0].transmission_end
                    < response_records[-1].transmission_start
                    <= response_records[-1].transmission_end
                    <= datetime.fromtimestamp(time_after + self.TIMESTAMP_TOLERANCE / 1000.))

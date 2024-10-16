"""Abstract definition of system tests cases that are common for CAN bus hardware types."""

from abc import ABC, abstractmethod


class AbstractCanSetup(ABC):
    """Abstract class for setup hardware related tests."""

    TASK_TIMING_TOLERANCE = 30.  # ms
    DELAY_AFTER_RECEIVING_FRAME = 10.  # ms
    DELAY_AFTER_RECEIVING_MESSAGE = 1000.  # ms
    DELAY_BETWEEN_CONSECUTIVE_FRAMES = 50.  # ms

    @abstractmethod
    def setup_class(self):
        """Create bus objects."""
        raise NotImplementedError

    @abstractmethod
    def teardown_class(self):
        """Close bus objects."""
        raise NotImplementedError


class AbstractCanSendPacket(ABC):
    """Abstract class for tests related to sending packets."""

    @abstractmethod
    def test_send_packet(self):
        """Test simple sending of a CAN packet."""

    @abstractmethod
    async def test_async_send_packet(self):
        """Test asynchronous sending of CAN packet."""

    @abstractmethod
    def test_send_packet_on_one_receive_on_other_bus(self):
        """Check for sending and receiving CAN packet using two Transport Interfaces."""

    @abstractmethod
    async def test_async_send_packet_on_one_receive_on_other_bus(self):
        """Check for asynchronous sending and receiving CAN packet using two Transport Interfaces."""


class AbstractCanReceivePacket(ABC):
    """Abstract class for tests related to receiving packets."""

    @abstractmethod
    def test_receive_packet__physical(self):
        """Check for a simple CAN packet (physically addressed) receiving."""

    @abstractmethod
    def test_receive_packet__functional(self):
        """Check for a simple CAN packet (functionally addressed) receiving."""

    @abstractmethod
    async def test_async_receive_packet__physical(self):
        """Check for a simple asynchronous CAN packet (physically addressed) receiving."""

    @abstractmethod
    async def test_async_receive_packet__functional(self):
        """Check for a simple asynchronous CAN packet (functionally addressed) receiving."""


class AbstractCanSendMessage(ABC):
    """Abstract class for tests related to sending a UDS message."""

    @abstractmethod
    def test_send_message__sf(self):
        """Check for a simple synchronous UDS message sending."""

    @abstractmethod
    def test_send_message__multi_packets(self):
        """Check for a synchronous multi packet (FF + CF) UDS message sending."""

    @abstractmethod
    async def test_async_send_message__sf(self):
        """Check for a simple asynchronous UDS message sending."""

    @abstractmethod
    async def test_async_send_message__multi_packets(self):
        """Check for an asynchronous multi packet (FF + CF) UDS message sending."""

    @abstractmethod
    def test_send_message_on_one_receive_on_other_bus(self):
        """Check for sending and receiving UDS message using two Transport Interfaces."""

    @abstractmethod
    async def test_async_send_message_on_one_receive_on_other_bus(self):
        """Check for asynchronous sending and receiving UDS message using two Transport Interfaces."""


class AbstractCanReceiveMessage(ABC):
    """Abstract class for tests related to receiving a UDS message."""

    @abstractmethod
    def test_receive_message__sf(self):
        """Check for receiving of a UDS message (carried by Single Frame packet)."""

    @abstractmethod
    def test_receive_message__multi_packets(self):
        """Check for receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""

    @abstractmethod
    async def test_async_receive_message__sf(self):
        """Check for asynchronous receiving of a UDS message (carried by Single Frame packet)."""

    @abstractmethod
    async def test_async_receive_message__multi_packets(self):
        """Check for asynchronous receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""


class AbstractTimeout(ABC):
    """Abstract class for tests in which timeout is main subject."""

    @abstractmethod
    def test_timeout_then_send_packet(self):
        """Check for sending a CAN packet after a timeout exception during receiving."""

    @abstractmethod
    async def test_async_timeout_then_send_packet(self):
        """Check for asynchronous sending a CAN packet after a timeout exception during asynchronous receiving."""

    @abstractmethod
    def test_send_message__multi_packets__timeout(self):
        """Check for a timeout (N_Bs timeout exceeded) during synchronous multi packet (FF + CF) UDS message sending."""

    @abstractmethod
    async def test_async_send_message__multi_packets__timeout(self):
        """Check for a timeout (N_Bs timeout exceeded) during asynchronous multi packet (FF + CF) UDS message sending."""

    @abstractmethod
    def test_receive_packet__timeout(self):
        """Check for a timeout during packet receiving."""

    @abstractmethod
    async def test_async_receive_packet__timeout(self):
        """Check for a timeout during packet asynchronous receiving."""

    @abstractmethod
    def test_timeout_then_receive_packet(self):
        """Check for receiving a CAN packet after a timeout exception during receiving."""

    @abstractmethod
    async def test_async_timeout_then_receive_packet(self):
        """Check for asynchronous receiving a CAN packet after a timeout exception during receiving."""

    @abstractmethod
    def test_receive_message__sf__timeout(self):
        """Check for a timeout during receiving of a UDS message."""

    @abstractmethod
    async def test_async_receive_message__sf__timeout(self):
        """Check for a timeout during asynchronous receiving of a UDS message."""

    @abstractmethod
    def test_receive_message__multi_packets__timeout(self):
        """Check for a timeout during receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""

    @abstractmethod
    async def test_async_receive_message__multi_packets__timeout(self):
        """Check for a timeout during asynchronous receiving of a UDS message (carried by First Frame and Consecutive Frame packets)."""


class AbstractObserve(ABC):
    """Abstract class for tests related to checking the transmitting a CAN packets."""

    @abstractmethod
    def test_observe_tx_packet(self):
        """Check for transmitting a CAN packet after a sending identical CAN frame."""

    @abstractmethod
    async def test_async_observe_tx_packet(self):
        """ Check for asynchronous transmitting a CAN packet after a sending identical CAN frame."""


class AbstractOverflow(ABC):
    """Abstract class for tests in which handling Overflow is main subject."""

    @abstractmethod
    def test_overflow_during_message_sending(self):
        """Check for handling Overflow status during synchronous multi packet (FF + CF) UDS message sending."""

    @abstractmethod
    async def test_overflow_during_async_message_sending(self):
        """Check for handling Overflow status during asynchronous multi packet (FF + CF) UDS message sending."""

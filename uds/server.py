"""UDS Server side implementation."""


__all__ = ["Server", "ResponseManager"]


class Server:
    """
    Factory of server (ECU) simulators.

    Each server object simulates communication with a single on-board ECU.
    Server is able to automatically respond to received UDS Requests/PDU according to provided set of rules.
    """
    #
    # def __init__(self,
    #              on_request: Optional[Callable] = None,
    #              on_response: Optional[Callable] = None) -> None:
    #     """
    #     Configures communication interfaces and configured events (on_request, on_response) hooks.
    #
    #     :param on_request: Hook to be called on every request message received by the server instance.
    #         IMPORTANT! One parameter 'message'
    #     :param on_response: Hook to be called on every response message transmitted by the server instance.
    #     """
    #     self.on_request = on_request
    #     self.on_response = on_response


class ResponseManager:
    ...

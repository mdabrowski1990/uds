from pytest import fixture

from uds.packet import CanAddressingFormat


@fixture(params=list(CanAddressingFormat))
def example_can_packet_type(request):
    return request.param

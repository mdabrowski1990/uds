from pytest import fixture

from uds.can import CanAddressingFormat, CanPacketType


@fixture(params=list(CanPacketType))
def example_can_packet_type(request):
    return request.param


@fixture(params=list(CanAddressingFormat))
def example_can_addressing_format(request):
    return request.param

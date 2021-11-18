from pytest import fixture

from uds.can import CanAddressingFormat


@fixture(params=list(CanAddressingFormat))
def example_can_addressing_format(request):
    return request.param

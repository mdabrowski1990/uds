from pytest import fixture

from can import Message


@fixture(params=[
    {"arbitration_id": 0x644,
     "is_extended_id": False,
     "channel": 1,
     "dlc": 8,
     "data": [0x05, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE]},
    {"arbitration_id": 0x18DCAB34,
     "is_extended_id": True,
     "channel": "Channel 2",
     "dlc": 0xF,
     "data": [0xD0, 0x10, 0x00, 0xFE, 0xDC, 0xBA, 0x98] + list(range(50, 107)),
     "is_fd": True,
     "bitrate_switch": True},
])
def example_python_can_message(request):
    return Message(**request.param)

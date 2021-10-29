# TODO: docstring

__all__ = ["FirstFrameHandler", "FirstFrameDataLengthHandler"]

from uds.utilities import RawBytes, RawBytesList
from .addressing_format import CanAddressingFormat


class FirstFrameDataLengthHandler:
    # TODO

    @classmethod
    def encode_ff_dl(cls, payload_bytes_number: int, dlc: int) -> RawBytesList:
        ...

    @classmethod
    def decode_ff_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        ...

    @classmethod
    def validate_ff_dl(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> None:
        ...


class FirstFrameHandler:
    # TODO

    @classmethod
    def is_first_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def validate_first_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def generate_can_frame_data(cls) -> RawBytesList:
        ...

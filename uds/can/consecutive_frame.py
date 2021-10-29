from uds.utilities import RawBytes, RawBytesList, Nibble
from .addressing_format import CanAddressingFormat


class SequenceNumberHandler:
    ...

    @staticmethod
    def validate_sn(sequence_number: Nibble) -> None:
        ...

    @classmethod
    def encode_sn(cls, sequence_number: Nibble, dlc: int) -> RawBytesList:
        ...

    @classmethod
    def decode_sn(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> int:
        ...


class ConsecutiveFrameHandler:
    # TODO

    @classmethod
    def is_consecutive_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def validate_consecutive_frame(cls, addressing_format: CanAddressingFormat, raw_frame_data: RawBytes) -> bool:
        ...

    @classmethod
    def generate_can_frame_data(cls) -> RawBytesList:
        ...

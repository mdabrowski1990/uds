"""
Implementation for CAN frame fields that are influenced by UDS.

Handlers for :ref:`CAN Frame <knowledge-base-can-frame>` fields:
 - CAN Identifier
 - DLC
 - Data
"""

__all__ = ["DEFAULT_FILLER_BYTE"]


from uds.utilities import RawByte


DEFAULT_FILLER_BYTE: RawByte = 0xCC
"""Default value of Filler Byte that is specified by ISO 15765-2:2016 (chapter 10.4.2.1).
Filler Byte is used for :ref:`CAN Frame Data Padding <knowledge-base-can-frame-data-padding>`."""


class CanIdHandler:
    ...

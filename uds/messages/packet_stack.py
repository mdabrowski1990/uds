__all__ = ["AbstractPacketStack"]

from abc import ABC, abstractmethod
from asyncio import Queue


class AbstractPacketStack(ABC):
    ...

    # TODO: handlers for Queue.put / Queue.get?

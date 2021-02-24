__all__ = ["AbstractTIServer"]

from abc import ABC, abstractmethod
from typing import Union


class AbstractTIServer(ABC):  # TODO: update according to notes
    """Abstraction of server side implementation of Transport Protocol"""

    def __init__(self,
                 s3_server: Union[int, float],
                 p2_server: Union[int, float],
                 p2ext_server: Union[int, float]) -> None:
        """
        Configures Transport Protocol

        :param s3_server:
        :param p2_server:
        :param p2ext_server:
        """
        # TODO

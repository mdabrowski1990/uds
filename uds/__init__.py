#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package for handling Unified Diagnostic Services (UDS) protocol defined by ISO-14229.

The package is meant to provide tools that enables:
 - monitoring UDS communication
 - simulation of any UDS node (either a client or a server)
 - testing of a device that supports UDS
 - injection of communication faults on any layers 3-7 of UDS OSI Model

The package is created with an idea to support any communication bus:
 - `CAN <https://en.wikipedia.org/wiki/CAN_bus>`_
 - `LIN <https://en.wikipedia.org/wiki/Local_Interconnect_Network>`_
 - `Ethernet <https://en.wikipedia.org/wiki/Ethernet>`_
 - `FlexRay <https://en.wikipedia.org/wiki/FlexRay>`_
 - `K-Line <https://en.wikipedia.org/wiki/K-Line>`_
"""

__all__ = [
    "addressing",
    "can",
    "client",
    "translator",
    "message",
    "packet",
    "segmentation",
    "transport_interface",
    "utilities",
    "__version__",
    "__author__",
    "__maintainer__",
    "__credits__",
    "__email__",
    "__license__",
]

__version__ = "2.0.0"
__author__ = "Maciej Dąbrowski"
__maintainer__ = "Maciej Dąbrowski"
__credits__ = [
    # developers
    "Maciej Dąbrowski (https://www.linkedin.com/in/maciej-dabrowski-test-engineer/)",
    "Przemysław Nieścior (https://www.linkedin.com/in/przemys%C5%82aw-nie%C5%9Bcior-33631021b/)",
    "Igor Jabłoński (https://www.linkedin.com/in/igor-jab%C5%82o%C5%84ski/)"
    # sponsors
    "Merit Automotive (https://merit-automotive.com/)"
]
__email__ = "uds-package-development@googlegroups.com"
__license__ = "MIT"


import importlib
import sys
from typing import Sequence


def __getattr__(name: str) -> object:  # noqa: vulture
    """Lazy imports."""
    if name == name.strip("_") and name in __all__:
        module = importlib.import_module(f"{__name__}.{name}")
        sys.modules[f"{__name__}.{name}"] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> Sequence[str]:  # noqa: vulture
    """All UDS objects."""
    return sorted(__all__)

#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package for handling Unified Diagnostic Services (UDS) protocol defined by ISO-14229.

The package is meant to provide tools to handle Session (5th), Presentation (6th) and Application (7th) layers
of OSI model. Other (bus specific) layers would be supported by extensions (once they are released) to this package
or by the interfaces provided by the user.
"""

__all__ = ["Client", "Server", "ResponseManager"]
__version__ = "0.0"
__author__ = "Maciej Dąbrowski"  # TODO: add other other contributors
# __credits__ = []  TODO: place for sponsors and other stakeholders
__email__ = "maciek_dabrowski@o2.pl"


from .client import Client
from .server import Server, ResponseManager

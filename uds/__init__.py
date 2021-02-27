#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package for handling Unified Diagnostic Services (UDS) protocol defined by ISO-14229.

The package is meant to provide tools to handle following UDS protocol layers (according to OSI model):
 - Session (5th) - specified by ISO 14229-2
 - Presentation (6th) - some part is specified by ISO 27145-2, rest is vehicle manufacturer specific
 - Application (7th) - specified by ISO 14229-1, ISO 14229-3, ISO 14229-4, ISO 14229-5, ISO 14229-6, ISO 14229-7,
        ISO 14229-8, ISO 27145-3 and further standards
Other (bus specific) layers would be supported by extensions (once released) to this package or by custom interfaces
created by users themselves.
"""

# __all__ = []  TODO: update when new feature are added
__version__ = "0.0"
__author__ = "Maciej Dąbrowski"  # TODO: add other other contributors
# __credits__ = []  TODO: place for sponsors and other stakeholders
__email__ = "maciek_dabrowski@o2.pl"

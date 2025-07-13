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

__version__ = "1.1.0"
__author__ = "Maciej Dąbrowski"
__maintainer__ = "Maciej Dąbrowski"
__credits__ = ["Maciej Dąbrowski (https://www.linkedin.com/in/maciej-dabrowski-test-engineer/)",
               "Przemysław Nieścior (https://www.linkedin.com/in/przemys%C5%82aw-nie%C5%9Bcior-33631021b/)",
               "Igor Jabłoński (https://www.linkedin.com/in/igor-jab%C5%82o%C5%84ski/)"
               "Merit Automotive (https://merit-automotive.com/)"]
__email__ = "uds-package-development@googlegroups.com"
__license__ = "MIT"


# import uds.addressing
# import uds.addressing
import uds.database
import uds.message
import uds.packet
import uds.segmentation
import uds.transport_interface

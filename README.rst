*****
UDS
*****

.. image:: https://github.com/mdabrowski1990/uds/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/mdabrowski1990/uds/actions

.. image:: https://travis-ci.com/mdabrowski1990/uds.svg?branch=main
   :target: https://travis-ci.com/mdabrowski1990/uds
   
.. image:: https://coveralls.io/repos/github/mdabrowski1990/uds/badge.svg
   :target: https://coveralls.io/github/mdabrowski1990/uds
   
.. image:: https://readthedocs.org/projects/uds/badge/?version=latest
   :target: https://uds.readthedocs.io/
   :alt: Documentation
   
.. image:: https://bestpractices.coreinfrastructure.org/projects/4703/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/4703
   
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/


Python package for handling `Unified Diagnostic Services`__ (UDS_) protocol defined by ISO 14229.
It supports different communication buses on both sides of communication (client and server).

Current Functionalities
=============
- Diagnostic message support
- Server (on-board ECU) simulation

Planned Functionalities
=============
- Client (diagnostic tester) simulation
- Messaging databases support
- Automatic messaging database import from CANdelaStudio File format (CDD)
- CAN support
- Ethernet support
- LIN support
- FlexRay support
- K-Line support

Documentation
=============
- Package documentation is available on `ReadTheDocs <https://uds.readthedocs.io/en/latest/>`_ and `GitHub Pages <https://mdabrowski1990.github.io/uds/>`_
- UDS protocol:
   - `ISO 14229-1:2020 <https://www.iso.org/standard/72439.html/>`_
   - `ISO 14229-2:2013 <https://www.iso.org/standard/45763.html/>`_
- UDS on CAN:
   - `ISO 14229-3:2012 <https://www.iso.org/standard/55284.html/>`_
   - `ISO 15765-2:2016 <https://www.iso.org/standard/66574.html/>`_
- UDS on LIN:
   - `ISO 14229-7:2015 <https://www.iso.org/standard/61221.html/>`_
   - `ISO 17987-2:2016 <https://www.iso.org/standard/61223.html/>`_
- UDS on Ethernet:
   - `ISO 14229-5:2013 <https://www.iso.org/standard/55287.html/>`_
   - `ISO 13400-2:2019 <https://www.iso.org/standard/74785.html/>`_

.. _UDS: https://en.wikipedia.org/wiki/Unified_Diagnostic_Services
__ UDS_

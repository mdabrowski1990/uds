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

Python package for handling `Unified Diagnostic Services`__ (UDS_) protocol defined by ISO 14229.
It supports different communication buses on both sides of communication (client and server).

Current Functionalities
=============
- Diagnostic message support

Planned Functionalities
=============
- Client (diagnostic tester) simulation
- Server (on-board ECU) simulation
- Messaging databases support
- Automatic messaging database import from Candela File format (CDD)
- CAN support
- Ethernet support
- LIN support
- Flexray support
- K-Line support

Documentation
=============
- Package documentation is available on `ReadTheDocs <https://uds.readthedocs.io/en/latest/>`_ and `GitHub Pages <https://mdabrowski1990.github.io/uds/>`_
- `ISO 14229-1:2020 <https://www.iso.org/standard/72439.html/>`_
- `ISO 14229-2:2013 <https://www.iso.org/standard/45763.html/>`_

.. _UDS: https://en.wikipedia.org/wiki/Unified_Diagnostic_Services
__ UDS_

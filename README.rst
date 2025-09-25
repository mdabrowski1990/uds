***
UDS
***

|CI| |SecurityScan| |BestPractices| |ReadTheDocs| |CodeCoverage|

|LatestVersion| |PythonVersions| |PyPIStatus| |TotalDownloads| |MonthlyDownloads| |Licence|

Python package for working with the `Unified Diagnostic Services`_ (UDS) protocol, as defined in ISO 14229.
It supports different communication buses on both communication sides (client and server).


Documentation
-------------
User documentation is hosted by ReadTheDocs portal and available under the following link: https://uds.readthedocs.io/

Security policy for this package is defined in `SECURITY.md`_ file.

If you want to become a contributor, please read `CONTRIBUTING.md`_ file.


Motivation
----------
Existing Python UDS packages (see `Alternative Options`_) cover parts of the protocol,
but often focus on a single bus, client-only communication, or limited configuration.

This package is designed to:

- support multiple buses (CAN, LIN, Ethernet, K-Line, FlexRay) and multiple bus managers (e.g. `python-can`_)
- handle both client and server roles
- provide detailed control over timing and transmission parameters
- enable use-cases from simple send/receive to simulation, testing, and sniffing/decoding UDS traffic

Development is ongoing, but the architecture is already in place, and several features are implemented.
See the current status at: https://uds.readthedocs.io/en/stable/#features


Alternative Options
```````````````````

python-udsoncan
'''''''''''''''
Link: https://github.com/pylessard/python-udsoncan

- pros:

  - extensive documentation
  - active community and maintenance
  - multiple connection types supported
  - full CAN support; extensible to other buses with custom code
  - configurable CAN transmission parameters via can-isotp
  - multiple diagnostic services implemented
  - error handling for both positive and negative scenarios
  - control over CAN network timings (N_As, N_Ar, N_Bs, N_Br, N_Cs, N_Cr)
  - possibility to inject Transport/Network layer errors

- cons:

  - no full-duplex communication
  - only client-side communication implemented


python-uds
''''''''''
Link: https://github.com/richClubb/python-uds

- pros:

  - CAN and LIN buses are supported

- cons:

  - limited documentation
  - not actively maintained (last release: March 2019)
  - limited interface support (primarily `python-can`_)
  - no full-duplex communication
  - only client-side communication implemented
  - limited configuration of communication parameters
  - no error injection options (e.g. Flow Status manipulation, incorrect sequence handling)


Contact
-------
- e-mail: uds-package-development@googlegroups.com
- group: `UDS package development`_
- discord: `UDS discord server`_


.. _SECURITY.md: https://github.com/mdabrowski1990/uds/blob/main/SECURITY.md

.. _CONTRIBUTING.md: https://github.com/mdabrowski1990/uds/blob/main/CONTRIBUTING.md

.. _UDS package development: https://groups.google.com/g/uds-package-development/about

.. _UDS discord server: https://discord.gg/y3waVmR5PZ

.. _Unified Diagnostic Services: https://en.wikipedia.org/wiki/Unified_Diagnostic_Services

.. _python-can: https://github.com/hardbyte/python-can

.. |CI| image:: https://github.com/mdabrowski1990/uds/actions/workflows/testing.yml/badge.svg?branch=main
   :target: https://github.com/mdabrowski1990/uds/actions/workflows/testing.yml
   :alt: Continuous Integration Status

.. |SecurityScan| image:: https://github.com/mdabrowski1990/uds/actions/workflows/codeql-analysis.yml/badge.svg?branch=main
   :target: https://github.com/mdabrowski1990/uds/actions/workflows/codeql-analysis.yml
   :alt: Security Scan Status

.. |ReadTheDocs| image:: https://readthedocs.org/projects/uds/badge/?version=latest
   :target: https://uds.readthedocs.io/
   :alt: ReadTheDocs Build Status

.. |BestPractices| image:: https://bestpractices.coreinfrastructure.org/projects/4703/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/4703
   :alt: CII Best Practices

.. |CodeCoverage| image:: https://codecov.io/gh/mdabrowski1990/uds/branch/main/graph/badge.svg?token=IL7RYZ5ERC
   :target: https://codecov.io/gh/mdabrowski1990/uds
   :alt: Software Tests Coverage

.. |LatestVersion| image:: https://img.shields.io/pypi/v/py-uds.svg
   :target: https://pypi.python.org/pypi/py-uds
   :alt: The latest Version of UDS package

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/py-uds.svg
   :target: https://pypi.python.org/pypi/py-uds/
   :alt: Supported Python versions

.. |PyPIStatus| image:: https://img.shields.io/pypi/status/py-uds.svg
   :target: https://pypi.python.org/pypi/py-uds/
   :alt: PyPI status

.. |TotalDownloads| image:: https://pepy.tech/badge/py-uds
   :target: https://pepy.tech/project/py-uds
   :alt: Total PyPI downloads

.. |MonthlyDownloads| image:: https://pepy.tech/badge/py-uds/month
   :target: https://pepy.tech/project/py-uds
   :alt: Monthly PyPI downloads

.. |Licence| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/
   :alt: License Type

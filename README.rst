***
UDS
***

|CI| |SecurityScan| |BestPractices| |ReadTheDocs| |CodeCoverage|

|LatestVersion| |PythonVersions| |PyPIStatus| |TotalDownloads| |MonthlyDownloads| |Licence|

Python package for handling `Unified Diagnostic Services`_ (UDS) protocol defined by ISO 14229.
It supports different communication buses on both communication sides (client and server).


Documentation
-------------
User documentation is hosted by ReadTheDocs portal and available under the following link: https://uds.readthedocs.io/

Security policy for this package is defined in `SECURITY.md`_ file.

If you want to become a contributor, please read `CONTRIBUTING.md`_ file.


Why another UDS package?
------------------------
There are a few already existing python packages to handle UDS protocol, so you might wonder why would you consider
using this one?

This package is meant to support **multiple buses** (including CAN, LIN, Ethernet, K-Line, FlexRay) and **multiple
bus managers** (e.g. `python-can`_).
Additionally, it handles both communication nodes (client and server), decoding monitored UDS communication,
and contains detailed configuration to fully control all timing and transmission parameters.

Thanks to all these features, this package can have multiple use-cases, including:

- simple send-receive packets/messages to/from any network
- comprehensive node simulations
- testing of UDS protocol communication implementation - either on client (diagnostic tester / ECU) or server (ECU) side
- sniffing (and decoding) UDS communication

Unfortunately, all previously mentioned plans make the project quite huge.
At the time of writing, the implementation process of these features is still ongoing (and probably the development
would slowly progress over at least a few more years, unless more people get engaged in the project and/or
more sponsors are found).
On the other hand, the architecture to support all these features is already designed and some of them are already
implemented with others defined or planned.

To check the current implementation status, visit:

- https://uds.readthedocs.io/en/stable/#features
- https://uds.readthedocs.io/en/stable/pages/knowledge_base/osi_model.html#uds-functionalities


Alternative options
```````````````````

python-udsoncan
'''''''''''''''
Link: https://github.com/pylessard/python-udsoncan

- pros:

  - comprehensive documentation -
    https://udsoncan.readthedocs.io/en/latest/index.html
  - maintained with active community - https://udsoncan.readthedocs.io/en/latest/udsoncan/questions_answers.html
  - various connection types are supported -
    https://udsoncan.readthedocs.io/en/latest/udsoncan/connection.html#available-connections
  - CAN bus fully supported with possibility to extension for other buses (requires custom code)
  - possibility to configure all transmission parameters for CAN using can-isotp package -
    https://can-isotp.readthedocs.io/en/latest/isotp/implementation.html#
  - handlers for multiple diagnostic services are implemented -
    https://udsoncan.readthedocs.io/en/latest/udsoncan/services.html
  - positive and negatives scenarios are handled - https://udsoncan.readthedocs.io/en/latest/udsoncan/exceptions.html

- cons:

  - does not support simulating negatives scenarios on Transport/Network layer, e.g.

    - cannot force Overflow / Wait value of Flow Status (parameter of Flow Control packet)
    - cannot send CAN packets in wrong order (e.g. incorrect Sequence Numbers order in Consecutive Frames)

  - only Client side communication is implemented - https://udsoncan.readthedocs.io/en/latest/udsoncan/client.html#
  - no control or measurement of CAN timing parameters (N_As, N_Ar, N_Bs, N_Br, N_Cs, N_Cr)


python-uds
''''''''''
Link: https://github.com/richClubb/python-uds

- pros:

  - CAN and LIN buses are supported

- cons:

  - very modest documentation - https://python-uds.readthedocs.io/en/latest/
  - is not maintained with last release in March 2019 - https://pypi.org/project/python-uds/
  - only a few communication interfaces (I have only found examples with python-can) are supported -
    https://python-uds.readthedocs.io/en/latest/interface.html
  - only Client side communication is implemented
  - limited communication parameters configuration - https://python-uds.readthedocs.io/en/latest/configuration.html


Contact
-------
- e-mail: uds-package-development@googlegroups.com
- group: `UDS package development`_
- discord: https://discord.gg/y3waVmR5PZ


.. _SECURITY.md: https://github.com/mdabrowski1990/uds/blob/main/SECURITY.md

.. _CONTRIBUTING.md: https://github.com/mdabrowski1990/uds/blob/main/CONTRIBUTING.md

.. _UDS package development: https://groups.google.com/g/uds-package-development/about

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

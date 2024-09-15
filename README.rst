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
There are a few already existing python packages to handle UDS protocol,
so you might wonder why would you consider using this one?

This package is meant to support **multiple buses** (including CAN, LIN, Ethernet, K-Line, FlexRay) and **multiple
bus managers** (e.g. `python-can`_).
Additionally, it handles both communication nodes (client and server), and contains detailed configuration to fully
control all timing and transmission parameters.

Thanks to all these features, this package can have multiple use-cases, including:

- simple send-receive messages to/from any network
- comprehensive node simulations
- testing of UDS protocol communication implementation

Unfortunately, all previously mentioned plans make the project a huge effort and at the time of writing,
the implementation process of these features is still ongoing (and probably the status will stay the same for at least
a couple more years).
On the other hand, the architecture to support all these features is already designed and some of the features
are already implemented with others defined or planned.

To check the current implementation status, visit:

- https://uds.readthedocs.io/en/stable/#features
- https://uds.readthedocs.io/en/stable/pages/knowledge_base/osi_model.html#uds-functionalities


Alternative options
```````````````````

python-udsoncan
'''''''''''''''
Link: https://github.com/pylessard/python-udsoncan

- pros:
    - comprehensive documentation
    - handlers for multiple diagnostic services is implemented
- cons:
    - only positive use case scenarios (where communication is in line with UDS standard) are supported
    - only CAN bus is supported
    - only Client side communication can be handled
    - limited communication parameters configuration


python-uds
''''''''''
Link: https://github.com/richClubb/python-uds

- pros:
    - CAN and LIN buses are supported
- cons:
    - modest documentation
    - only a few communication interfaces are supported
    - only Client side communication can be handled
    - limited communication parameters configuration


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

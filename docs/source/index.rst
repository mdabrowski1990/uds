Welcome to UDS documentation!
=============================
.. toctree::
    :hidden:

    Home <self>
    pages/installation.rst
    pages/user_guide.rst
    pages/examples.rst
    autoapi/index.rst
    pages/knowledge_base.rst
    pages/contribution.rst


Overview
--------
The purpose of this project is to provide python tool to handle
`Unified Diagnostic Services (UDS) <https://en.wikipedia.org/wiki/Unified_Diagnostic_Services>`_ protocol defined
by ISO-14229. The created package helps to simulate either communication side (client or server), monitoring
and decode diagnostic communication.

The architecture enables to use it with various communication buses (e.g. CAN, LIN).

The most likely use cases of this package are:
 - communication with your vehicle (e.g. reading Diagnostic Trouble Codes)
 - monitoring and decoding UDS communication
 - performing tests against on-board ECU (server)
 - performing tests against OBD Tester (client)


Implementation Status
---------------------
The package is currently in the early development phase, therefore only a few features are currently available.
If you want to speed up the development, please visit :ref:`contribution section <contribution>` to find out
what are your options.


Features
````````
Current implementation status of package features:

+----------------------------------------------+--------------------------------------------+
|                    Feature                   |            Implementation Status           |
+==============================================+============================================+
| UDS Messages and Packets                     | Available since version `0.0.2             |
|                                              | <https://pypi.org/project/py-uds/0.0.2/>`_ |
+----------------------------------------------+--------------------------------------------+
| UDS Packets Reception and Transmission       | Available since version `0.3.0             |
|                                              | <https://pypi.org/project/py-uds/0.3.0/>`_ |
+----------------------------------------------+--------------------------------------------+
| UDS Messages Reception and Transmission      | Available since version `1.0.0             |
|                                              | <https://pypi.org/project/py-uds/1.0.0/>`_ |
+----------------------------------------------+--------------------------------------------+
| Messages Segmentation                        | Available since version `0.2.0             |
|                                              | <https://pypi.org/project/py-uds/0.2.0/>`_ |
+----------------------------------------------+--------------------------------------------+
| UDS Packets Desegmentation                   | Available since version `0.2.0             |
|                                              | <https://pypi.org/project/py-uds/0.2.0/>`_ |
+----------------------------------------------+--------------------------------------------+
| Support for Services with multiple responses | Planned                                    |
+----------------------------------------------+--------------------------------------------+
| Client Simulation                            | Planned                                    |
+----------------------------------------------+--------------------------------------------+
| Server Simulation                            | Planned                                    |
+----------------------------------------------+--------------------------------------------+
| Support for Messages Databases               | Planned                                    |
+----------------------------------------------+--------------------------------------------+


Buses supported
```````````````
Current implementation status of support for communication buses:

+----------+-----------------------+
|    Bus   | Implementation Status |
+==========+=======================+
| CAN      | Full                  |
+----------+-----------------------+
| FlexRay  | Planned               |
+----------+-----------------------+
| Ethernet | Planned               |
+----------+-----------------------+
| K-Line   | Planned               |
+----------+-----------------------+
| LIN      | Planned               |
+----------+-----------------------+


License
-------
The project is licensed under the MIT license - https://github.com/mdabrowski1990/uds/blob/main/LICENSE


Contact
-------
- e-mail: uds-package-development@googlegroups.com
- group: `UDS package development <https://groups.google.com/g/uds-package-development/about>`_
- discord: https://discord.gg/y3waVmR5PZ


.. admonition:: Documentation generated

    |today|

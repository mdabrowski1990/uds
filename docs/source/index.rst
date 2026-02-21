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


.. _implementation-status:

Implementation Status
---------------------
The package is currently in the early development phase, therefore only a few features are currently available.
If you want to speed up the development, please visit :ref:`contribution section <contribution>` to find out
what are your options.


Features
````````
Current implementation status of package features:

+-----------------------------------------+---------------------------------------------------------------------------+
|                 Feature                 |                           Implementation Status                           |
+=========================================+===========================================================================+
| UDS Messages and Packets                | Available since version `0.0.2 <https://pypi.org/project/py-uds/0.0.2/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| Packets Reception and Transmission      | Available since version `0.3.0 <https://pypi.org/project/py-uds/0.3.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| UDS Messages Reception and Transmission | Available since version `1.0.0 <https://pypi.org/project/py-uds/1.0.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| Messages Segmentation                   | Available since version `0.2.0 <https://pypi.org/project/py-uds/0.2.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| Packets Desegmentation                  | Available since version `0.2.0 <https://pypi.org/project/py-uds/0.2.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| Client Simulation                       | Available since version `3.0.0 <https://pypi.org/project/py-uds/3.0.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| Server Simulation                       | Planned                                                                   |
+-----------------------------------------+---------------------------------------------------------------------------+
| UDS Sniffer                             | Planned                                                                   |
+-----------------------------------------+---------------------------------------------------------------------------+
| UDS Messages Translator                 | Available since version `2.0.0 <https://pypi.org/project/py-uds/2.0.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+
| Logger                                  | Available since version `4.0.0 <https://pypi.org/project/py-uds/4.0.0/>`_ |
+-----------------------------------------+---------------------------------------------------------------------------+


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


OSI Model overview
------------------
An overview of features that are required to fully implement UDS protocol is presented in the table below:

+--------------+--------------------------------------+--------------------------------------------+
|   OSI Layer  |            Functionalities           |               Implementation               |
+==============+======================================+============================================+
| Layer 7      | - diagnostic messages support        | - :mod:`uds.message`                       |
| Application  |                                      |                                            |
+--------------+--------------------------------------+--------------------------------------------+
| Layer 6      | - building diagnostic messages       | - :mod:`uds.translator`                    |
| Presentation |                                      |                                            |
|              | - diagnostic messages interpretation |                                            |
+--------------+--------------------------------------+--------------------------------------------+
| Layer 5      | - Client simulation                  | - :mod:`uds.client`                        |
| Session      |                                      |                                            |
|              | - Server simulation                  | *To be provided with Server feature.*      |
|              |                                      |                                            |
|              | - sniffing UDS communication         | *To be provided with Sniffer feature.*     |
+--------------+--------------------------------------+--------------------------------------------+
| Layer 4      | - packet support                     | - :mod:`uds.packet`                        |
| Transport    |                                      |                                            |
|              | - bus specific segmentation          | - :mod:`uds.segmentation`                  |
|              |                                      |                                            |
|              | - bus specific packets transmission  | - :mod:`uds.transport_interface`           |
+--------------+                                      |                                            |
| Layer 3      |                                      | *Network specific:*                        |
| Network      |                                      |                                            |
|              |                                      | - *CAN* - :mod:`uds.can`                   |
|              |                                      |                                            |
|              |                                      | *To be extended for other networks*        |
+--------------+--------------------------------------+--------------------------------------------+
| Layer 2      | - frames transmission                | External python packages for bus handling: |
| Data         |                                      |                                            |
|              | - frames receiving                   | -  CAN:                                    |
+--------------+                                      |                                            |
| Layer 1      |                                      |   - python-can                             |
| Physical     |                                      |                                            |
|              |                                      | *To be extended for other networks*        |
+--------------+--------------------------------------+--------------------------------------------+

where:

- OSI Layer - considered :ref:`OSI Model <knowledge-base-osi-model>` Layer
- Functionalities - functionalities required in the implementation to handle considered UDS OSI layer
- Implementation - UDS package implementation that provides mentioned functionalities


License
-------
The project is licensed under the MIT license - https://github.com/mdabrowski1990/uds/blob/main/LICENSE


Contact
-------
- e-mail: uds-package-development@googlegroups.com
- group: `UDS package development <https://groups.google.com/g/uds-package-development/about>`_
- discord: `UDS Discord <https://discord.gg/y3waVmR5PZ>`_


.. admonition:: Documentation generated

  |today|

Welcome to UDS documentation!
=============================
.. toctree::
   :hidden:

   Home <self>
   pages/installation.rst
   pages/message.rst
   pages/segmentation.rst
   pages/transport.rst
   pages/client_simulation.rst
   pages/server_simulation.rst
   autoapi/index.rst
   pages/knowledge_base.rst
   pages/contribution.rst


Overview
--------
The purpose of this project is to provide python tools for simulation (on both sides - client and server) and
monitoring of diagnostic communication defined by ISO-14229. It can be used with any bus type (e.g. CAN, Ethernet, LIN).

The most likely use cases of this package are:
 - communication with your vehicle (e.g. reading Diagnostic Trouble Codes)
 - monitoring and decoding ongoing UDS communication
 - performing tests against on-board ECU (server)
 - performing tests against OBD Tester (client)


Implementation Status
---------------------
The package is currently in the early development phase.

Features status
'''''''''''''''
Current status of features implementation:

+---------------------------------------+-----------------------+
|                Feature                | Implementation Status |
+=======================================+=======================+
| UDS Packets Reception                 |        Ongoing        |
+---------------------------------------+-----------------------+
| UDS Packets Transmission              |        Planned        |
+---------------------------------------+-----------------------+
| Segmentation                          |        Ongoing        |
+---------------------------------------+-----------------------+
| Periodic and OnEvent Services Support |        Planned        |
+---------------------------------------+-----------------------+
| Client Simulation                     |        Ongoing        |
+---------------------------------------+-----------------------+
| Server Simulation                     |        Planned        |
+---------------------------------------+-----------------------+
| Messaging Databases Support           |        Planned        |
+---------------------------------------+-----------------------+

Bus support status
''''''''''''''''''
Current bus support status:

+----------+-----------------------+
|    Bus   | Implementation Status |
+==========+=======================+
| CAN      | Ongoing               |
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

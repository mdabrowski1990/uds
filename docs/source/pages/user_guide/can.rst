.. _implementation-docan:

Diagnostics over CAN
====================
This part of documentation explains implementation for :ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>`
protocol.

DoCAN implementation is located in :mod:`uds.can` module and divided into smaller modules, each handling one of
the following features:

- `Addressing`_
- `Frame`_
- `Packet`_
- `Segmentation`_
- `Transport Interface`_


.. note:: You might use :ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol separately from UDS.


Addressing
----------
:ref:`CAN Addressing <knowledge-base-can-addressing>` might use one of multiple formats.
This is the reason behind dividing CAN addressing related implementation into multiple modules.
The whole implementation can be found in :mod:`uds.can.addressing` sub-package.


CanAddressingFormat
```````````````````
:class:`~uds.can.addressing.addressing_format.CanAddressingFormat` class is an Enum with all possible
:ref:`CAN Addressing Formats <knowledge-base-can-addressing>` defined.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` - check if provided value is defined as a member of this Enum
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` - validate that provided value is defined as a member of
  this Enum

**Example code:**

  .. code-block::  python

    import uds

    # check if there is member defined for the value
    uds.can.CanAddressingFormat.is_member(uds.can.CanAddressingFormat.NORMAL_ADDRESSING)  # False
    uds.can.CanAddressingFormat.validate_member("Extended Addressing")  # uds.can.CanAddressingFormat.EXTENDED_ADDRESSING
    uds.can.CanAddressingFormat.is_member("Not a CAN Addressing Format")  # False
    uds.can.CanAddressingFormat.validate_member("Not a CAN Addressing Format")  # raises ValueError


AbstractCanAddressingInformation
````````````````````````````````
:class:`~uds.can.addressing.abstract_addressing_information.AbstractCanAddressingInformation` class defines common API
and contains common code for CAN related addressing information storages. It is located in
:mod:`uds.can.addressing.abstract_addressing_information`.

.. warning:: **A user shall not use**
  :class:`~uds.can.addressing.abstract_addressing_information.AbstractCanAddressingInformation`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.


NormalCanAddressingInformation
``````````````````````````````
:class:`~uds.can.addressing.normal_addressing.NormalCanAddressingInformation` class is a storage for
Addressing Information in :ref:`Normal CAN Addressing Format <knowledge-base-can-normal-addressing>`.

*From the user perspective, objects creation and passing them correctly are the only interactions.*
*This is why we only explain how to properly initialize objects of this class.*

In case of :ref:`Normal CAN Addressing Format <knowledge-base-can-normal-addressing>`, each address is fully carried in
CAN Identifier field of :ref:`CAN Frame <knowledge-base-can-frame>`. That is why only "can_id" parameters shall be
passed upon :class:`~uds.can.addressing.normal_addressing.NormalCanAddressingInformation` object creation.

**Example code:**

  .. code-block::  python

    import uds

    # create storage for CAN Addressing Information that use Normal Addressing Format
    ecu_ai = uds.can.addressing.NormalCanAddressingInformation(
        rx_physical_params={"can_id": 0x7E8},
        tx_physical_params={"can_id": 0x7E0},
        rx_functional_params={"can_id": 0x7E8},
        tx_functional_params={"can_id": 0x7DF})


NormalFixedCanAddressingInformation
```````````````````````````````````
:class:`~uds.can.addressing.normal_addressing.NormalFixedCanAddressingInformation` class is a storage for
Addressing Information in :ref:`Normal Fixed CAN Addressing Format <knowledge-base-can-normal-fixed-addressing>`.

*From the user perspective, objects creation and passing them correctly are the only interactions.*
*This is why we only explain how to properly initialize objects of this class.*

In case of :ref:`Normal Fixed CAN Addressing Format <knowledge-base-can-normal-fixed-addressing>` each address is fully
carried in CAN Identifier field of :ref:`CAN Frame <knowledge-base-can-frame>`, but CAN Identifier value contains
**Source Address**, **Target Address** and **priority** parameters.
Upon :class:`~uds.can.addressing.normal_addressing.NormalFixedCanAddressingInformation` object creation,
each address might be defined using either "can_id" parameter, combination of "target_address" and "source_address"
parameters or by providing all these parameters (compatibility cross-check would be performed then).

**Example code:**

  .. code-block::  python

    import uds

    # create storage for CAN Addressing Information that use Normal Fixed Addressing Format
    ecu_ai_1 = uds.can.addressing.NormalFixedCanAddressingInformation(
        rx_physical_params={"can_id": 0x18DAF101},
        tx_physical_params={"can_id": 0x18DA01F1},
        rx_functional_params={"can_id": 0x18DBF101},
        tx_functional_params={"can_id": 0x18DB33F1})
    # define object with the same addresses, but provide parameters differently
    ecu_ai_2 = uds.can.addressing.NormalFixedCanAddressingInformation(
        rx_physical_params={"target_address": 0xF1, "source_address": 0x01},
        tx_physical_params={"target_address": 0x01, "source_address": 0xF1},
        rx_functional_params={"can_id": 0x18DBF101, "target_address": 0xF1, "source_address": 0x01},
        tx_functional_params={"can_id": 0x18DB33F1, "target_address": 0x33, "source_address": 0xF1})
    ecu_ai_1 == ecu_ai_2  # True
    # define object with similar addresses, but using non-default priority value
    ecu_ai_3 = uds.can.addressing.NormalFixedCanAddressingInformation(
        rx_physical_params={"can_id": 0xDAF101},
        tx_physical_params={"can_id": 0xDA01F1, "target_address": 0x01, "source_address": 0xF1},
        rx_functional_params={"can_id": 0x1CDBF101},
        tx_functional_params={"can_id": 0x1CDB33F1, "target_address": 0x33, "source_address": 0xF1})
    ecu_ai_1 == ecu_ai_3  # False

.. warning:: To set CAN Identifier value with priority parameter other than default value (6 - 0b110),
  "can_id" parameter has to be provided.


ExtendedCanAddressingInformation
````````````````````````````````
:class:`~uds.can.addressing.extended_addressing.ExtendedCanAddressingInformation` class is a storage for
Addressing Information in :ref:`Extended CAN Addressing Format <knowledge-base-can-extended-addressing>`.

*From the user perspective, objects creation and passing them correctly are the only interactions.*
*This is why we only explain how to properly initialize objects of this class.*

In case  of :ref:`Extended CAN Addressing Format <knowledge-base-can-extended-addressing>`, each address is carried by
CAN Identifier and first data byte of :ref:`CAN Frame <knowledge-base-can-frame>` (called **Target Address**).
Exactly two parameters "can_id" and "target_address" shall be passed to each address upon
:class:`~uds.can.addressing.extended_addressing.ExtendedCanAddressingInformation` object creation.

**Example code:**

  .. code-block::  python

    import uds

    # create storage for CAN Addressing Information that use Extended Addressing Format
    ecu_ai = uds.can.addressing.ExtendedCanAddressingInformation(
        rx_physical_params={"can_id": 0x701, "target_address": 0x01},
        tx_physical_params={"can_id": 0x702, "target_address": 0xF1},
        rx_functional_params={"can_id": 0x701, "target_address": 0xFF},
        tx_functional_params={"can_id": 0x702, "target_address": 0xF1},


Mixed11BitCanAddressingInformation
``````````````````````````````````
:class:`~uds.can.addressing.mixed_addressing.Mixed11BitCanAddressingInformation` class is a storage for
Addressing Information in
:ref:`Mixed CAN Addressing Format which use Standard CAN ID <knowledge-base-can-mixed-11-bit-addressing>`.

*From the user perspective, objects creation and passing them correctly are the only interactions.*
*This is why we only explain how to properly initialize objects of this class.*

In case of :ref:`Mixed CAN Addressing Format <knowledge-base-can-mixed-addressing>`, each address is carried by
CAN Identifier and first data byte of :ref:`CAN Frame <knowledge-base-can-frame>` (called **Address Extension**).
Exactly two parameters "can_id" and "address_extension" shall be passed to each address upon
:class:`~uds.can.addressing.extended_addressing.ExtendedCanAddressingInformation` object creation.

.. note:: Value of "address_extension" parameter must be the same for transmitting (Tx) and receiving (Rx) addresses.
  It applies to both addresses pairs (for physical and functional communication).

**Example code:**

  .. code-block::  python

    import uds

    # create storage for CAN Addressing Information that use Mixed Addressing Format using standard CAN Identifiers
    ecu_ai = uds.can.addressing.Mixed11BitCanAddressingInformation(
        rx_physical_params={"can_id": 0x701, "address_extension": 0x01},
        tx_physical_params={"can_id": 0x702, "address_extension": 0x01},
        rx_functional_params={"can_id": 0x701, "address_extension": 0xFF},
        tx_functional_params={"can_id": 0x702, "address_extension": 0xFF},


Mixed29BitCanAddressingInformation
``````````````````````````````````
:class:`~uds.can.addressing.mixed_addressing.Mixed29BitCanAddressingInformation` class is a storage for
Addressing Information in
:ref:`Mixed CAN Addressing Format which use Extended CAN ID <knowledge-base-can-mixed-29-bit-addressing>`.

*From the user perspective, objects creation and passing them correctly are the only interactions.*
*This is why we only explain how to properly initialize objects of this class.*

In case of :ref:`Mixed CAN Addressing Format <knowledge-base-can-mixed-addressing>`

Each address in case of :ref:`Mixed CAN Addressing Format <knowledge-base-can-mixed-addressing>`, each address is
carried by CAN Identifier and first data byte of :ref:`CAN Frame <knowledge-base-can-frame>`
(called **Address Extension**).
On top of that, CAN Identifier value contains **Source Address**, **Target Address** and **priority** parameters.
Upon :class:`~uds.can.addressing.mixed_addressing.Mixed29BitCanAddressingInformation` object creation,
each address must contain "address_extension", and "can_id", combination of "target_address" and "source_address"
parameters, or all these parameters (compatibility cross-check would be performed then).

.. note:: Value of "address_extension" parameter must be the same for transmitting (Tx) and receiving (Rx) addresses.
  It applies to both addresses pairs (for physical and functional communication).

**Example code:**

  .. code-block::  python

    import uds

    # create storage for CAN Addressing Information that use Normal Fixed Addressing Format
    ecu_ai_1 = uds.can.addressing.Mixed29BitCanAddressingInformation(
        rx_physical_params={"can_id": 0x18CEF101,
                            "address_extension": 0x2D},
        tx_physical_params={"can_id": 0x18CE01F1,
                            "address_extension": 0x2D},
        rx_functional_params={"can_id": 0x18CDF101,
                              "address_extension": 0x8C},
        tx_functional_params={"can_id": 0x18CD33F1,
                              "address_extension": 0x8C})
    # define object with the same addresses, but provide parameters differently
    ecu_ai_2 = uds.can.addressing.Mixed29BitCanAddressingInformation(
        rx_physical_params={"target_address": 0xF1, "source_address": 0x01,
                            "address_extension": 0x2D},
        tx_physical_params={"target_address": 0x01, "source_address": 0xF1,
                            "address_extension": 0x2D},
        rx_functional_params={"can_id": 0x18CDF101, "target_address": 0xF1, "source_address": 0x01,
                              "address_extension": 0x8C},
        tx_functional_params={"can_id": 0x18CD33F1, "target_address": 0x33, "source_address": 0xF1,
                              "address_extension": 0x8C})
    ecu_ai_1 == ecu_ai_2  # True
    # define object with similar addresses, but using non-default priority value
    ecu_ai_3 = uds.can.addressing.Mixed29BitCanAddressingInformation(
        rx_physical_params={"can_id": 0xCEF101,
                            "address_extension": 0x2D},
        tx_physical_params={"can_id": 0xCE01F1, "target_address": 0x01, "source_address": 0xF1,
                            "address_extension": 0x2D},
        rx_functional_params={"can_id": 0x1CCDF101,
                              "address_extension": 0x8C},
        tx_functional_params={"can_id": 0x1CCD33F1, "target_address": 0x33, "source_address": 0xF1,
                              "address_extension": 0x8C})
    ecu_ai_1 == ecu_ai_3  # False

.. warning:: To set CAN Identifier value with priority parameter other than default value (6 - 0b110),
  "can_id" parameter has to be provided.


CanAddressingInformation
````````````````````````
:class:`~uds.can.addressing.addressing_information.CanAddressingInformation` is factory for
:class:`~uds.can.addressing.abstract_addressing_information.AbstractCanAddressingInformation` subclasses.
You might use it to create Addressing Information object using `addressing_format` argument as
:ref:`CAN Addressing Format <knowledge-base-can-addressing>` selector.

**Example code:**

  .. code-block::  python

    import uds

    # create examples storages for CAN Addressing Information
    ecu_ai = uds.can.addressing.CanAddressingInformation(
        addressing_format=uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
        rx_physical_params={"can_id": 0x7E8},
        tx_physical_params={"can_id": 0x7E0},
        rx_functional_params={"can_id": 0x7E8},
        tx_functional_params={"can_id": 0x7DF})
    ecu_ai_2 = uds.can.CanAddressingInformation(
        addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
        rx_physical_params={"can_id": 0x701, "target_address": 0x01},
        tx_physical_params={"can_id": 0x702, "target_address": 0xF1},
        rx_functional_params={"can_id": 0x701, "target_address": 0xFF},
        tx_functional_params={"can_id": 0x702, "target_address": 0xF1})
    ecu_ai_3 = uds.can.CanAddressingInformation(
        addressing_format=uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING,
        rx_physical_params={"can_id": 0x18CEF101, "address_extension": 0x2D},
        tx_physical_params={"can_id": 0x18CE01F1, "address_extension": 0x2D},
        rx_functional_params={"can_id": 0x18CDF101, "address_extension": 0x8C},
        tx_functional_params={"can_id": 0x18CD33F1, "address_extension": 0x8C})


Frame
-----
There are a few aspects of :ref:`CAN Frames <knowledge-base-can-frame>` management that had to be implemented,
including CAN Identifiers, DLC value and data field length.
The whole implementation can be found in :mod:`uds.can.frame` module.

CanIdHandler
````````````
:class:`~uds.can.frame.CanIdHandler` class was defined as collection of various helper functions for CAN ID management.
There is no need to create an object, as each contained method us in fact "classmethod".

*As a user, you would normally never use* :class:`~uds.can.frame.CanIdHandler` *class directly,*
*therefore we are happy to just inform you about its existence.*


CanDlcHandler
`````````````
:class:`~uds.can.frame.CanDlcHandler` class was defined as collection of various helper functions for DLC field and
data bytes management for CAN bus.
There is no need to create an object, as each contained method us in fact "classmethod".

*As a user, you would normally never use* :class:`~uds.can.frame.CanDlcHandler` *class directly,*
*therefore we are happy to just inform you about its existence.*


Packet
------
Packet implementation for CAN is located in :mod:`uds.can.packet` sub-package. It is divided into following

- :class:`~uds.can.packet.can_packet_type.CanPacketType`
- :class:`~uds.can.packet.abstract_container.AbstractCanPacketContainer`
- :class:`~uds.can.packet.can_packet.CanPacket`
- :class:`~uds.can.packet.can_packet_record.CanPacketRecord`
- :mod:`~uds.can.packet.single_frame`
- :mod:`~uds.can.packet.first_frame`
- :mod:`~uds.can.packet.flow_control`
- :mod:`~uds.can.packet.consecutive_frame`


CanPacketType
`````````````
:class:`~uds.can.packet.can_packet_type.CanPacketType` is an enum with all
:ref:`Network Protocol Control Information (N_PCI) values for Diagnostics over CAN <knowledge-base-can-n-pci>` defined.

Methods:

- :meth:`~uds.can.packet.can_packet_type.CanPacketType.is_initial_packet_type`
- :meth:`~uds.utilities.enums.ExtendableEnum.add_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`


AbstractCanPacketContainer
``````````````````````````
:class:`~uds.can.packet.abstract_container.AbstractCanPacketContainer` class defines attributes of container for
all parameters used by :ref:`CAN Packets <knowledge-base-can-packet>`. It also contains implementation for multiple
parameters extractions. It is a move to avoid repeating similar code in both
:class:`~uds.can.packet.can_packet.CanPacket` and - :class:`~uds.can.packet.can_packet_record.CanPacketRecord` classes.

.. warning:: **A user shall not use**
  `~uds.can.packet.abstract_container.AbstractCanPacketContainer`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.


CanPacket
`````````
:class:`~uds.can.packet.can_packet.CanPacket` class defines a structure for
:ref:`CAN Packets <knowledge-base-can-packet>` information. It is located in :mod:`~uds.can.packet.can_packet`.

Attributes:

- :attr:`~uds.can.packet.can_packet.CanPacket.can_id`
- :attr:`~uds.can.packet.can_packet.CanPacket.raw_frame_data`
- :attr:`~uds.can.packet.can_packet.CanPacket.addressing_format`
- :attr:`~uds.can.packet.can_packet.CanPacket.addressing_type`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.dlc`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.packet_type`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.source_address`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.target_address`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.address_extension`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.payload`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.data_length`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.flow_status`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.block_size`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.st_min`

Methods:

- :meth:`~uds.can.packet.can_packet.CanPacket.set_addressing_information`
- :meth:`~uds.can.packet.can_packet.CanPacket.set_packet_data`
- :meth:`~uds.can.packet.can_packet.CanPacket.__init__`
- :meth:`~uds.can.packet.can_packet.CanPacket.__str__`

**Example code:**

  .. code-block::  python

    import uds

    # create examples CAN Packet objects
    sf = uds.can.CanPacket(addressing_format=uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
                           packet_type=uds.can.CanPacketType.SINGLE_FRAME,
                           addressing_type=uds.addressing.AddressingType.FUNCTIONAL,
                           can_id=0x742,
                           payload=[0x3E, 0x00])
    ff = uds.can.CanPacket(addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                           packet_type=uds.can.CanPacketType.FIRST_FRAME,
                           addressing_type=uds.addressing.AddressingType.PHYSICAL,
                           target_address=0xF1,
                           source_address=0x12,
                           dlc=8,
                           payload=[0x62, 0x12, 0x34, 0x56, 0x78, 0x9A],
                           data_length=123)
    fc = uds.can.CanPacket(addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
                           packet_type=uds.can.CanPacketType.FLOW_CONTROL,
                           addressing_type=uds.addressing.AddressingType.PHYSICAL,
                           can_id=0x615,
                           target_address=0xA2,
                           flow_status=uds.can.CanFlowStatus.Overflow)
    cf = uds.can.CanPacket(addressing_format=uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                           packet_type=uds.can.CanPacketType.CONSECUTIVE_FRAME,
                           addressing_type=uds.addressing.AddressingType.PHYSICAL,
                           target_address=0xF1,
                           source_address=0x3B,
                           address_extension=0x10,
                           payload=b"\xF0\xE1\xD2\xC3\xB4\xA5\x96\x87\x78\x69\x5A\x4B\x3C\x2D\x1E\x0F",
                           sequence_number=1)
    # show content of created packets
    print(sf)
    print(ff)
    print(fc)
    print(cf)

.. note:: Methods :meth:`~uds.can.packet.can_packet.CanPacket.set_addressing_information` and
  :meth:`~uds.can.packet.can_packet.CanPacket.set_packet_data` are providing tools to changing multiple connected
  attributes at the same time, but it is recommended to always create new :class:`~uds.can.packet.can_packet.CanPacket`
  objects instead.


CanPacketRecord
```````````````


Single Frame
````````````


First Frame
```````````


Flow Control
````````````


Consecutive Frame
`````````````````


Segmentation
------------



Transport Interface
-------------------






TODO
====


CAN Transport Interface
-----------------------
The implementation for Transport Interfaces that can be used with CAN bus is located in
:mod:`uds.transport_interface.can_transport_interface` module.


Common
------
Common implementation for all all CAN Transport Interfaces is included in
:class:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface`.

.. warning:: **A user shall not use**
  :class:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.


Configuration
`````````````
CAN bus specific configuration is set upon calling
:meth:`uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.__init__` method.
The following configuration parameters are set then:

- Addressing Information of this CAN node - attribute
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.addressing_information`
- driver for a CAN bus interface - attribute
  :attr:`~uds.transport_interface.abstract_transport_interface.AbstractTransportInterface.bus_manager`
- timing parameters (:ref:`N_Br <knowledge-base-can-n-br>`, :ref:`N_Cs <knowledge-base-can-n-cs>`) - attributes
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_br` and
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_cs`
- communication timeout parameters (:ref:`N_As <knowledge-base-can-n-as>`, :ref:`N_Ar <knowledge-base-can-n-ar>`,
  :ref:`N_Bs <knowledge-base-can-n-bs>`, :ref:`N_Cr <knowledge-base-can-n-cr>`) - attributes
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_as_timeout`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_ar_timeout`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_bs_timeout` and
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.n_cr_timeout`
- UDS message segmentation parameters (:ref:`base DLC of a CAN frame <knowledge-base-can-data-field>`,
  flag whether to use :ref:`data optimization for CAN frame <knowledge-base-can-data-optimization>`,
  and the value to use for :ref:`CAN frame data padding <knowledge-base-can-frame-data-padding>`) - attributes
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.dlc`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.use_data_optimization`,
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.filler_byte`,
- Flow Control generator - attribute
  :attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.flow_control_parameters_generator`

Most of these attributes (all except
:attr:`~uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.addressing_information`)
can be changed after object is created.


Python-CAN
----------
Class :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` contains
the implementation of CAN Transport Interface that uses `python-can <https://python-can.readthedocs.io>`_ package for
receiving and transmitting CAN frames.

.. note:: Right now only half-duplex communication is implemented.

  The matter is further explained in
  :ref:`handling unexpected CAN packets arrivals <knowledge-base-can-unexpected-packet-arrival>` chapter.


Configuration
`````````````
Configuration is set upon calling
:meth:`uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.__init__` method and from
the user perspective it does not provide any additional features to common_ implementation provided by
:meth:`uds.transport_interface.can_transport_interface.common.AbstractCanTransportInterface.__init__`.

**Example code:**

.. code-block::  python

    import uds
    from can import Bus

    # define example python-can bus interface (https://python-can.readthedocs.io/en/stable/bus.html#bus-api)
    python_can_interface = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)

    # define Addressing Information for a CAN Node
    can_node_addressing_information = uds.can.CanAddressingInformation(
        addressing_format=uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
        tx_physical={"can_id": 0x611},
        rx_physical={"can_id": 0x612},
        tx_functional={"can_id": 0x6FF},
        rx_functional={"can_id": 0x6FE})

    # configure CAN Transport Interface for this CAN Node
    can_transport_interface = uds.transport_interface.PyCanTransportInterface(
        can_bus_manager=python_can_interface,
        addressing_information=can_node_addressing_information,
        n_as_timeout=50,
        n_ar_timeout=900,
        n_bs_timeout=50,
        n_br=10,
        n_cs=0,
        n_cr_timeout = 900,
        dlc=0xF,
        use_data_optimization=True,
        filler_byte=0x55,
        flow_control_parameters_generator=uds.can.DefaultFlowControlParametersGenerator(st_min=0,
                                                                                        block_size=5,
                                                                                        wait_count=0,
                                                                                        repeat_wait=False))

    # change CAN Transport Interface configuration
    can_transport_interface.n_as_timeout = uds.transport_interface.PyCanTransportInterface.N_AS_TIMEOUT
    can_transport_interface.n_ar_timeout = uds.transport_interface.PyCanTransportInterface.N_AR_TIMEOUT
    can_transport_interface.n_bs_timeout = uds.transport_interface.PyCanTransportInterface.N_BS_TIMEOUT
    can_transport_interface.n_br = uds.transport_interface.PyCanTransportInterface.DEFAULT_N_BR
    can_transport_interface.n_cs = uds.transport_interface.PyCanTransportInterface.DEFAULT_N_CS
    can_transport_interface.n_cr_timeout = uds.transport_interface.PyCanTransportInterface.N_CR_TIMEOUT
    can_transport_interface.dlc = 8
    can_transport_interface.use_data_optimization = False
    can_transport_interface.filler_byte = 0xAA
    can_transport_interface.flow_control_parameters_generator = uds.can.DefaultFlowControlParametersGenerator(
        st_min=100,
        block_size=15,
        wait_count=1,
        repeat_wait=True)


Synchronous communication
`````````````````````````
.. warning:: Synchronous and asynchronous implementation shall not be mixed, therefore for transmitting and receiving
    UDS Messages and CAN Packets use either:

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_message`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`

    or

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

.. seealso:: :ref:`Examples for python-can Transport Interface <examples-python-can>`

Send Message
''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # send UDS Message and receive UDS message record with historic information about the transmission
    message_record = can_transport_interface.send_message(message)


Receive Message
'''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive an UDS message with timeout set to 1000 ms
    message_record = can_transport_interface.receive_message(timeout=1000)



Send Packet
'''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
method to send CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # segment the message to create a CAN packet
    can_packet = can_transport_interface.segmenter.segmentation(message)[0]

    # send CAN packet and receive CAN packet record with historic information about the transmission and the transmitted CAN packet
    can_packet_record = can_transport_interface.send_packet(can_packet)

Receive Packet
''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`
method to receive CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive a CAN packet with timeout set to 1000 ms
    can_packet_record = can_transport_interface.receive_packet(timeout=1000)


Asynchronous communication
``````````````````````````
.. warning:: Synchronous and asynchronous implementation shall not be mixed, therefore for transmitting and receiving
    UDS Messages and CAN Packets use either:

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.receive_message`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`

    or

    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
    - :meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
    - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

.. seealso:: :ref:`Examples for python-can Transport Interface <examples-python-can>`

.. note:: In all examples, only a coroutine code was presented. If you need a manual how to run an asynchronous code,
    visit https://docs.python.org/3/library/asyncio-runner.html#running-an-asyncio-program.

Send Message
''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_send_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # send UDS Message and receive UDS message record with historic information about the transmission
    message_record = await can_transport_interface.async_send_message(message)

Receive Message
'''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface.async_receive_message`
method to receive UDS messages over CAN.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive an UDS message with timeout set to 1000 ms
    message_record = await can_transport_interface.async_receive_message(timeout=1000)

Send Packet
'''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
method to send CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # define some UDS message to send
    message = uds.message.UdsMessage(addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                     payload=[0x10, 0x03])

    # segment the message to create a CAN packet
    can_packet = can_transport_interface.segmenter.segmentation(message)[0]

    # send CAN packet and receive CAN packet record with historic information about the transmission and the transmitted CAN packet
    can_packet_record = await can_transport_interface.async_send_packet(can_packet)

Receive Packet
''''''''''''''
Once an object of :class:`~uds.transport_interface.can_transport_interface.python_can.PyCanTransportInterface` class
is created, use
:meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`
method to receive CAN packets.

**Example code:**

.. code-block::  python

    # let's assume that we have `can_transport_interface` already configured as presented in configuration example above

    # receive a CAN packet with timeout set to 1000 ms
    can_packet_record = await can_transport_interface.async_receive_packet(timeout=1000)


















CanSegmenter
------------
:class:`~uds.segmentation.can_segmenter.CanSegmenter` handles segmentation process specific for CAN bus.

Following functionalities are provided by :class:`~uds.segmentation.can_segmenter.CanSegmenter`:

- Configuration of the segmenter:

  As a user, you are able to configure :class:`~uds.segmentation.can_segmenter.CanSegmenter` parameters which determines
  the addressing (Addressing Format and Addressing Information of input and output CAN packets) and the content
  (e.g. Filler Byte value and whether to use CAN Frame Data Optimization) of CAN packets.

  **Example code:**

    .. code-block::  python

        import uds

        # define Addressing Information for a CAN Node
        can_node_addressing_information = uds.can.CanAddressingInformation(
            addressing_format=uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
            tx_physical={"can_id": 0x611},
            rx_physical={"can_id": 0x612},
            tx_functional={"can_id": 0x6FF},
            rx_functional={"can_id": 0x6FE})

        # configure CAN Segmenter for this CAN Node
        can_segmenter = uds.segmentation.CanSegmenter(addressing_information=can_node_addressing_information,
                                                      dlc=8,
                                                      use_data_optimization=False,
                                                      filler_byte=0xFF)

        # change CAN Segmenter configuration
        can_segmenter.addressing_information = uds.can.CanAddressingInformation(
            uds.can.CanAddressingFormat.NORMAL_ADDRESSING,
            tx_physical={"can_id": 0x612},
            rx_physical={"can_id": 0x611},
            tx_functional={"can_id": 0x6FE},
            rx_functional={"can_id": 0x6FF})
        can_segmenter.dlc=0xF
        can_segmenter.use_data_optimization = True
        can_segmenter.filler_byte = 0xAA


- Diagnostic message segmentation:

  As a user, you are able to :ref:`segment diagnostic messages <knowledge-base-message-segmentation>`
  (objects of :class:`~uds.message.uds_message.UdsMessage` class) into CAN packets
  (objects for :class:`~uds.can.packet.can_packet.CanPacket` class).

  **Example code:**

    .. code-block::  python

        # let's assume that we have `can_segmenter` already configured as presented in configuration example above

        # define diagnostic message to segment
        uds_message_1 = uds.message.UdsMessage(payload=[0x3E, 0x00],
                                               addressing_type=uds.addressing.AddressingType.FUNCTIONAL)
        uds_message_2 = uds.message.UdsMessage(payload=[0x62, 0x10, 0x00] + [0x20]*100,
                                               addressing_type=uds.addressing.AddressingType.PHYSICAL)

        # use preconfigured segmenter to segment the diagnostic messages
        can_packets_1 = can_segmenter.segmentation(uds_message_1)  # output: Single Frame
        can_packets_2 = can_segmenter.segmentation(uds_message_2)  # output: First Frame with Consecutive Frame(s)

  .. note:: It is impossible to segment functionally addressed diagnostic message into First Frame and Consecutive Frame(s)
      as such result is considered incorrect according to :ref:`UDS ISO Standards <knowledge-base-uds-standards>`.


- CAN packets desegmentation:

  As a user, you are able to :ref:`desegment CAN packets <knowledge-base-packets-desegmentation>`
  (either objects of :class:`~uds.can.packet.can_packet.CanPacket` or
  :class:`~uds.can.packet.can_packet_record.CanPacketRecord` class)
  into diagnostic messages (either objects of :class:`~uds.message.uds_message.UdsMessage` or
  :class:`~uds.message.uds_message.UdsMessageRecord` class).

  **Example code:**

    .. code-block::  python

        # let's assume that we have `can_segmenter` already configured as presented in configuration example above

        # define CAN packets to desegment
        can_packets_1 = [
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.SINGLE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
                                 addressing_type=uds.addressing.AddressingType.FUNCTIONAL,
                                 can_id=0x6A5,
                                 target_address=0x0C,
                                 payload=[0x3E, 0x80])
        ]
        can_packets_2 = [
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.FIRST_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 dlc=8,
                                 data_length=15,
                                 payload=[0x62, 0x10, 0x00] + 3*[0x20]),
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.CONSECUTIVE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 dlc=8,
                                 sequence_number=1,
                                 payload=7*[0x20]),
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.CONSECUTIVE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.addressing.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 sequence_number=1,
                                 payload=2 * [0x20],
                                 filler_byte=0x99)
        ]

        # use preconfigured segmenter to desegment the CAN packets
        uds_message_1 = can_segmenter.desegmentation(can_packets_1)
        uds_message_2 = can_segmenter.desegmentation(can_packets_2)

    .. warning:: Desegmentation performs only sanity check of CAN packets content, therefore some inconsistencies
        with Diagnostic on CAN standard might be silently accepted as long as a message can be unambiguously decoded
        out of provided CAN packets.

    .. note:: Desegmentation can be performed for any CAN packets (not only those targeting this CAN Node) in any format.

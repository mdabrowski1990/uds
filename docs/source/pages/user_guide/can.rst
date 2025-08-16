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
- `Transport`_


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

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`
  this Enum

**Example code:**

  .. code-block::  python

    import uds

    # check if there is member defined for the value
    uds.can.CanAddressingFormat.is_member(uds.can.CanAddressingFormat.NORMAL_ADDRESSING)  # True
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


.. _implementation-can-addressing-information:

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
:class:`~uds.can.frame.CanIdHandler` class was defined as a collection of various helper functions
for CAN ID management.
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


.. _implementation-can-packet:

Packet
------
Packet implementation for CAN is located in :mod:`uds.can.packet` sub-package. It is divided into the following parts:

- `CanPacketType`_
- `AbstractCanPacketContainer`_
- `CanPacket`_
- `CanPacketRecord`_
- `Single Frame`_
- `First Frame`_
- `Consecutive Frame`_
- `Flow Control`_


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
:ref:`CAN Packets <knowledge-base-can-packet>` information. It is located in :mod:`uds.can.packet.can_packet`.

Attributes:

- :attr:`~uds.can.packet.can_packet.CanPacket.can_id`
- :attr:`~uds.can.packet.can_packet.CanPacket.raw_frame_data`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.dlc`
- :attr:`~uds.can.packet.can_packet.CanPacket.addressing_format`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.target_address`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.source_address`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.address_extension`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.packet_type`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.data_length`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.flow_status`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.block_size`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.st_min`
- :attr:`~uds.can.packet.can_packet.CanPacket.addressing_type`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.payload`


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
:class:`~uds.can.packet.can_packet_record.CanPacketRecord` class define a structure for
:ref:`CAN Packet <knowledge-base-can-packet>` records (storage for information about
:ref:`CAN Packets <knowledge-base-can-packet>` that were either transmitted or received).
It is located in :mod:`uds.can.packet.can_packet_record`.

Attributes:

- :attr:`~uds.can.packet.can_packet_record.CanPacketRecord.can_id`
- :attr:`~uds.can.packet.can_packet_record.CanPacketRecord.raw_frame_data`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.dlc`
- :attr:`~uds.can.packet.can_packet_record.CanPacketRecord.addressing_format`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.target_address`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.source_address`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.address_extension`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.packet_type`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.data_length`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.sequence_number`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.flow_status`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.block_size`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.st_min`
- :attr:`~uds.can.packet.can_packet_record.CanPacketRecord.addressing_type`
- :attr:`~uds.can.packet.abstract_container.AbstractCanPacketContainer.payload`

Methods:

- :meth:`~uds.can.packet.can_packet_record.CanPacketRecord._validate_frame`
- :meth:`~uds.can.packet.can_packet_record.CanPacketRecord._validate_attributes`
- :meth:`~uds.can.packet.can_packet_record.CanPacketRecord.__init__`
- :meth:`~uds.can.packet.can_packet_record.CanPacketRecord.__str__`

.. note:: A **user would not create objects of** :class:`~uds.can.packet.can_packet_record.CanPacketRecord` **class**
  in typical situations, but one would probably use them quite often as they are returned by communication layers
  (e.g. :mod:`uds.transport_interface`) of :mod:`uds` package.

.. warning:: All :class:`~uds.can.packet.can_packet_record.CanPacketRecord` **attributes are read only**
  (they are set only once upon an object creation) as they store historic data and history cannot be changed
  (*can't it, right?*).


Single Frame
````````````
:ref:`CAN Single Frame <knowledge-base-can-single-frame>` implementation is located in
:mod:`uds.can.packet.single_frame`.
This code does not have to be called directly by users, as higher layers of this package (e.g.
:class:`~uds.can.packet.abstract_container.AbstractCanPacketContainer`, :class:`~uds.can.packet.can_packet.CanPacket`)
are already integrated with it.

Some user might find these functions useful (e.g. for testing proper error handling of
:ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol):

- :func:`~uds.can.packet.single_frame.is_single_frame`
- :func:`~uds.can.packet.single_frame.validate_single_frame_data`
- :func:`~uds.can.packet.single_frame.create_single_frame_data`
- :func:`~uds.can.packet.single_frame.generate_single_frame_data`
- :func:`~uds.can.packet.single_frame.extract_single_frame_payload`
- :func:`~uds.can.packet.single_frame.extract_sf_dl`
- :func:`~uds.can.packet.single_frame.get_max_sf_dl`
- :func:`~uds.can.packet.single_frame.get_single_frame_min_dlc`


First Frame
```````````
:ref:`CAN First Frame <knowledge-base-can-first-frame>` implementation is located in
:mod:`uds.can.packet.first_frame`.
This code does not have to be called directly by users, as higher layers of this package (e.g.
:class:`~uds.can.packet.abstract_container.AbstractCanPacketContainer`, :class:`~uds.can.packet.can_packet.CanPacket`)
are already integrated with it.

Some user might find these functions useful (e.g. for testing proper error handling of
:ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol):

- :func:`~uds.can.packet.first_frame.is_first_frame`
- :func:`~uds.can.packet.first_frame.validate_first_frame_data`
- :func:`~uds.can.packet.first_frame.create_first_frame_data`
- :func:`~uds.can.packet.first_frame.generate_first_frame_data`
- :func:`~uds.can.packet.first_frame.extract_first_frame_payload`
- :func:`~uds.can.packet.first_frame.extract_ff_dl`
- :func:`~uds.can.packet.first_frame.get_first_frame_payload_size`


Consecutive Frame
`````````````````
:ref:`CAN Consecutive Frame <knowledge-base-can-consecutive-frame>` implementation is located in
:mod:`uds.can.packet.consecutive_frame`.
This code does not have to be called directly by users, as higher layers of this package (e.g.
:class:`~uds.can.packet.abstract_container.AbstractCanPacketContainer`, :class:`~uds.can.packet.can_packet.CanPacket`)
are already integrated with it.

Some user might find these functions useful (e.g. for testing proper error handling of
:ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol):

- :func:`~uds.can.packet.consecutive_frame.is_consecutive_frame`
- :func:`~uds.can.packet.consecutive_frame.validate_consecutive_frame_data`
- :func:`~uds.can.packet.consecutive_frame.create_consecutive_frame_data`
- :func:`~uds.can.packet.consecutive_frame.generate_consecutive_frame_data`
- :func:`~uds.can.packet.consecutive_frame.extract_consecutive_frame_payload`
- :func:`~uds.can.packet.consecutive_frame.get_consecutive_frame_min_dlc`
- :func:`~uds.can.packet.consecutive_frame.get_consecutive_frame_max_payload_size`
- :func:`~uds.can.packet.consecutive_frame.extract_sequence_number`


Flow Control
````````````
:ref:`CAN Flow Control <knowledge-base-can-flow-control>` implementation is located in
:mod:`uds.can.packet.flow_control`.

The key Flow Control related implementation:

- `CanFlowStatus`_
- `CanSTminTranslator`_
- `AbstractFlowControlParametersGenerator`_
- `DefaultFlowControlParametersGenerator`_

Some user might find these functions useful (e.g. for testing proper error handling of
:ref:`Diagnostics over CAN (DoCAN) <knowledge-base-docan>` protocol):

- :func:`~uds.can.packet.flow_control.is_flow_control`
- :func:`~uds.can.packet.flow_control.validate_flow_control_data`
- :func:`~uds.can.packet.flow_control.create_flow_control_data`
- :func:`~uds.can.packet.flow_control.generate_flow_control_data`
- :func:`~uds.can.packet.flow_control.extract_flow_status`
- :func:`~uds.can.packet.flow_control.extract_block_size`
- :func:`~uds.can.packet.flow_control.extract_st_min`
- :func:`~uds.can.packet.flow_control.get_flow_control_min_dlc`


CanFlowStatus
'''''''''''''
:class:`~uds.can.packet.flow_control.CanFlowStatus` class is an Enum with all possible
:ref:`CAN Flow Status <knowledge-base-can-flow-status>` values defined.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`

**Example code:**

  .. code-block::  python

    import uds

    # check if there is member defined for the value
    uds.can.CanFlowStatus.is_member(uds.can.CanFlowStatus.ContinueToSend)  # True
    uds.can.CanFlowStatus.validate_member(3)  # uds.can.CanFlowStatus.Overflow
    uds.can.CanFlowStatus.is_member("Not a CAN Flow Status")  # False
    uds.can.CanFlowStatus.validate_member(0xF)  # raises ValueError


CanSTminTranslator
''''''''''''''''''
:class:`~uds.can.packet.flow_control.CanSTminTranslator` class was defined as a collection of various helper functions
for :ref:`Separation Time Minimum (STmin) <knowledge-base-can-st-min>` management.
There is no need to create an object, as each contained method us in fact "classmethod".

Methods:

- :meth:`~uds.can.packet.flow_control.CanSTminTranslator.decode`
- :meth:`~uds.can.packet.flow_control.CanSTminTranslator.encode`
- :meth:`~uds.can.packet.flow_control.CanSTminTranslator.is_time_value`

**Example code:**

  .. code-block::  python

    import uds

    # check if provided time value [ms] can be encoded as STmin
    uds.can.CanSTminTranslator.is_time_value(0.1)  # True
    uds.can.CanSTminTranslator.is_time_value(127)  # True

    # encode time value [ms] into raw STmin value
    uds.can.CanSTminTranslator.encode(0.1)  # 241
    uds.can.CanSTminTranslator.encode(127)  # 127

    # decode raw STmin value into time value [ms]
    uds.can.CanSTminTranslator.decode(241)  # 0.1 [ms]
    uds.can.CanSTminTranslator.decode(127)  # 127 [ms]


AbstractFlowControlParametersGenerator
''''''''''''''''''''''''''''''''''''''
:class:`~uds.can.packet.flow_control.AbstractFlowControlParametersGenerator` defines abstract API for
Flow Control Generators that are used by CAN Transport Interface
(attribute :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.flow_control_parameters_generator`
of :class:`~uds.can.transport_interface.common.AbstractCanTransportInterface` has to be an object of
:class:`~uds.can.packet.flow_control.AbstractFlowControlParametersGenerator` class)

.. warning:: **A user shall not use**
  :class:`~uds.can.packet.flow_control.AbstractFlowControlParametersGenerator`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.


DefaultFlowControlParametersGenerator
'''''''''''''''''''''''''''''''''''''
:class:`~uds.can.packet.flow_control.DefaultFlowControlParametersGenerator` provides typical concrete implementation
for :class:`~uds.can.packet.flow_control.AbstractFlowControlParametersGenerator`.
It cover all typical use cases.

**Normally users would just create** :class:`~uds.can.packet.flow_control.DefaultFlowControlParametersGenerator`
**objects and pass them to CAN Transport Interface, where all interactions are executed.**
The examples below are provided to visualize how
:class:`~uds.can.packet.flow_control.DefaultFlowControlParametersGenerator` objects are used.

**Example code:**

  .. code-block::  python

    import uds

    # create example flow control parameters generators
    fc_gen_1 = uds.can.DefaultFlowControlParametersGenerator(block_size=2,
                                                             st_min=5,
                                                             wait_count=2,
                                                             repeat_wait=False)
    # create iterators for flow control parameters
    fc_iter_1 = iter(fc_gen_1)
    # generate following flow control parameters (Flow Status, Block Size, STmin)
    next(fc_iter_1)  # (<CanFlowStatus.Wait: 1>, None, None)
    next(fc_iter_1)  # (<CanFlowStatus.Wait: 1>, None, None)
    next(fc_iter_1)  # (<CanFlowStatus.ContinueToSend: 0>, 2, 5)
    next(fc_iter_1)  # (<CanFlowStatus.ContinueToSend: 0>, 2, 5)

    # example 2
    fc_gen_2 = uds.can.DefaultFlowControlParametersGenerator(block_size=13,
                                                             st_min=241,
                                                             wait_count=1,
                                                             repeat_wait=True)
    fc_iter_2 = iter(fc_gen_2)
    next(fc_iter_1)  # (<CanFlowStatus.Wait: 1>, None, None)
    next(fc_iter_1)  # (<CanFlowStatus.ContinueToSend: 0>, 13, 241)
    next(fc_iter_1)  # (<CanFlowStatus.Wait: 1>, None, None)
    next(fc_iter_1)  # (<CanFlowStatus.ContinueToSend: 0>, 13, 241)


Segmentation
------------
:ref:`Segmentation on CAN bus <knowledge-base-can-segmentation>` is fully implemented by `CanSegmenter`_.


CanSegmenter
------------
:class:`~uds.segmentation.can_segmenter.CanSegmenter` handles segmentation process specific for CAN bus.

Following functionalities are provided by :class:`~uds.segmentation.can_segmenter.CanSegmenter`:

- Configuration of the segmenter:

  As a user, you are able to configure :class:`~uds.segmentation.can_segmenter.CanSegmenter` parameters which determines
  the :ref:`addressing <knowledge-base-can-addressing>` and other attributes of
  :ref:`CAN packets <knowledge-base-can-packet>`.

  **Example code:**

    .. code-block::  python

      import uds

      # let's assume that CAN Addressing Information object is already created
      can_node_addressing_information: uds.can.CanAddressingInformation

      # configure example CAN Segmenter for this CAN Node
      can_segmenter = uds.can.CanSegmenter(addressing_information=can_node_addressing_information,
                                           dlc=8,
                                           use_data_optimization=False,
                                           filler_byte=0xFF)

      # change CAN Segmenter configuration
      can_segmenter.dlc=0xF
      can_segmenter.use_data_optimization = True
      can_segmenter.filler_byte = 0xAA

- Diagnostic message segmentation:

  As a user, you are able to :ref:`segment diagnostic messages <knowledge-base-message-segmentation>`
  into :ref:`CAN packets <knowledge-base-can-packet>`.

  **Example code:**

    .. code-block::  python

      import uds

      # let's assume that we have `can_segmenter` already configured
      can_segmenter: uds.can.CanSegmenter

      # define diagnostic message to segment
      uds_message_1 = uds.message.UdsMessage(payload=[0x3E, 0x00],
                                             addressing_type=uds.addressing.AddressingType.FUNCTIONAL)
      uds_message_2 = uds.message.UdsMessage(payload=[0x62, 0x10, 0x00] + [0x20]*100,
                                             addressing_type=uds.addressing.AddressingType.PHYSICAL)

      # use segmenter to segment defined UDS Messages
      can_packets_1 = can_segmenter.segmentation(uds_message_1)  # output: Single Frame
      can_packets_2 = can_segmenter.segmentation(uds_message_2)  # output: First Frame with Consecutive Frame(s)

  .. note:: It is impossible to segment functionally addressed diagnostic message into
    :ref:`First Frame <knowledge-base-can-first-frame>` and
    :ref:`Consecutive Frame(s) <knowledge-base-can-consecutive-frame>`
    as such operation is considered incorrect according to
    :ref:`Diagnostics over CAN <knowledge-base-docan>`.

- CAN packets desegmentation:

  As a user, you are able to :ref:`desegment CAN packets <knowledge-base-packets-desegmentation>`
  into :ref:`diagnostic messages <implementation-diagnostic-message>`.

  **Example code:**

    .. code-block::  python

      import uds

      # let's assume that we have `can_segmenter` already configured
      can_segmenter: uds.can.CanSegmenter

      # define CAN packets to desegment
      can_packets_1 = [
          uds.can.CanPacket(packet_type=uds.can.CanPacketType.SINGLE_FRAME,
                            addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
                            addressing_type=uds.addressing.AddressingType.FUNCTIONAL,
                            can_id=0x6A5,
                            target_address=0x0C,
                            payload=[0x3E, 0x80])
      ]
      can_packets_2 = [
          uds.can.CanPacket(packet_type=uds.can.CanPacketType.FIRST_FRAME,
                            addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                            addressing_type=uds.addressing.AddressingType.PHYSICAL,
                            target_address=0x12,
                            source_address=0xE0,
                            dlc=8,
                            data_length=15,
                            payload=[0x62, 0x10, 0x00] + 3*[0x20]),
          uds.can.CanPacket(packet_type=uds.can.CanPacketType.CONSECUTIVE_FRAME,
                            addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                            addressing_type=uds.addressing.AddressingType.PHYSICAL,
                            target_address=0x12,
                            source_address=0xE0,
                            dlc=8,
                            sequence_number=1,
                            payload=7*[0x20]),
          uds.can.CanPacket(packet_type=uds.can.CanPacketType.CONSECUTIVE_FRAME,
                            addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                            addressing_type=uds.addressing.AddressingType.PHYSICAL,
                            target_address=0x12,
                            source_address=0xE0,
                            sequence_number=1,
                            payload=2 * [0x20],
                            filler_byte=0x99)
      ]

      # use CAN Segmenter to desegment defined CAN packets
      uds_message_1 = can_segmenter.desegmentation(can_packets_1)
      uds_message_2 = can_segmenter.desegmentation(can_packets_2)

      # show content of desegmented messages
      print(uds_message_1)  # UdsMessage(payload=[0x3E, 0x80], addressing_type=Functional)
      print(uds_message_2)  # UdsMessage(payload=[0x62, 0x10, 0x00, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20], addressing_type=Physical)

    .. warning:: Desegmentation performs only sanity check of CAN packets content, therefore some inconsistencies
        with :Ref:`Diagnostic on CAN <knowledge-base-docan>` standard might be silently accepted as long as
        :ref:`a diagnostic message <implementation-diagnostic-message>` can be unambiguously decoded out of provided
        :ref:`CAN packets <knowledge-base-can-packet>`.

    .. note:: Desegmentation can be performed for any CAN packets (not only those targeting this CAN Node)
      using any valid :ref:`CAN Addressing Format <knowledge-base-can-addressing>`.


Transport
---------
:ref:`Diagnostic Messages <implementation-diagnostic-message>` and :ref:`CAN Packets <knowledge-base-can-packet>`
are sent and received by so called Transport Interfaces.
For CAN bus, currently there are following Transport Interfaces defined:

- `AbstractCanTransportInterface`_
- `PyCanTransportInterface`_

.. seealso:: :ref:`Abstract Transport Interface <implementation-abstract-transport-interface>`


AbstractCanTransportInterface
`````````````````````````````
:class:`~uds.can.transport_interface.common.AbstractCanTransportInterface` class defines common part for all CAN related
Transport Interfaces, including all `Diagnostic over CAN <knowledge-base-docan>` related parameters.

Attributes:

- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.N_AS_TIMEOUT`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.N_AR_TIMEOUT`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.N_BS_TIMEOUT`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.N_CR_TIMEOUT`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.DEFAULT_N_BR`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.DEFAULT_N_CS`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.DEFAULT_FLOW_CONTROL_PARAMETERS`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.segmenter`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_as_timeout`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_as_measured`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_ar_timeout`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_ar_measured`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_bs_timeout`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_bs_measured`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_br`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_br_max`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_cs`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_cs_max`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_cr_timeout`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.n_cr_measured`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.dlc`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.use_data_optimization`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.filler_byte`
- :attr:`~uds.can.transport_interface.common.AbstractCanTransportInterface.flow_control_parameters_generator`

Methods:

- :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface._update_n_ar_measured`
- :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface._update_n_as_measured`
- :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface._update_n_bs_measured`
- :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface._update_n_cr_measured`
- :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.clear_measurements`
- :meth:`~uds.can.transport_interface.common.AbstractCanTransportInterface.__init__`

.. warning:: **A user shall not use**
  :class:`~uds.can.transport_interface.common.AbstractCanTransportInterface`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.


.. _implementation-can-python-can-transport-interface:

PyCanTransportInterface
```````````````````````
:class:`~uds.can.transport_interface.python_can.PyCanTransportInterface` class is concrete Transport Interface
implementation that uses `python-can package <https://python-can.readthedocs.io>`_ for CAN bus communication
(sending and receiving :ref:`CAN frames <knowledge-base-can-frame>`).
Implementation is located in :mod:`uds.can.transport_interface.python_can`.

Following functionalities are provided by :class:`~uds.can.transport_interface.python_can.PyCanTransportInterface`:

- Configuration of the transport interface:

  The configuration takes place during :meth:`uds.can.transport_interface.python_can.PyCanTransportInterface.__init__`
  call. From the user perspective it does not provide any additional features to common implementation defined by
  :meth:`uds.can.transport_interface.common.AbstractCanTransportInterface.__init__`.

  **Example code:**

  .. code-block::  python

    import uds
    from can import BusABC

    # let's assume we have python-can bus interface defined
    # More info: https://python-can.readthedocs.io/en/stable/bus.html#bus-api
    python_can_interface: BusABC

    # let's assume that CAN Addressing Information object is already created
    can_node_addressing_information: uds.can.CanAddressingInformation

    # configure example CAN Transport Interface
    can_transport_interface = uds.can.PyCanTransportInterface(
        network_manager=python_can_interface,
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
    can_transport_interface.n_as_timeout = uds.can.PyCanTransportInterface.N_AS_TIMEOUT
    can_transport_interface.n_ar_timeout = uds.can.PyCanTransportInterface.N_AR_TIMEOUT
    can_transport_interface.n_bs_timeout = uds.can.PyCanTransportInterface.N_BS_TIMEOUT
    can_transport_interface.n_br = uds.can.PyCanTransportInterface.DEFAULT_N_BR
    can_transport_interface.n_cs = uds.can.PyCanTransportInterface.DEFAULT_N_CS
    can_transport_interface.n_cr_timeout = uds.can.PyCanTransportInterface.N_CR_TIMEOUT
    can_transport_interface.dlc = 8
    can_transport_interface.use_data_optimization = False
    can_transport_interface.filler_byte = 0xAA
    can_transport_interface.flow_control_parameters_generator = uds.can.DefaultFlowControlParametersGenerator(
        st_min=100,
        block_size=15,
        wait_count=1,
        repeat_wait=True)

- Synchronous communication

  :class:`~uds.can.transport_interface.python_can.PyCanTransportInterface` defines following methods for synchronous
  CAN communication:

  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_message`
  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_message`
  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.send_packet`
  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.receive_packet`

- Asynchronous communication

  :class:`~uds.can.transport_interface.python_can.PyCanTransportInterface` defines following methods for synchronous
  CAN communication:

  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_message`
  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_message`
  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_send_packet`
  - :meth:`~uds.can.transport_interface.python_can.PyCanTransportInterface.async_receive_packet`

.. seealso:: :ref:`Examples for python-can Transport Interface <examples-python-can>`

.. warning:: **Synchronous and asynchronous** implementation **shall not be mixed**.

.. note:: Currently only half-duplex communication is implemented.

  The matter is further explained in
  :ref:`handling unexpected CAN packets arrivals <knowledge-base-can-unexpected-packet-arrival>` chapter.

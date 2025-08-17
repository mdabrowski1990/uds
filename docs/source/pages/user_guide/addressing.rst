.. _implementation-addressing:

Addressing
==========
The :ref:`addressing <knowledge-base-addressing>` related implementation that is common for all networks is located
in :mod:`uds.addressing` sub-package. Each network type has its own specific implementation for addressing information
encoding and extracting from packets.


AddressingType
--------------
:class:`~uds.addressing.addressing_type.AddressingType` class is enum with all possible UDS
:ref:`addressing <knowledge-base-addressing>` types defined in it.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`

**Example code:**

  .. code-block::  python

    import uds

    # check if provided value is AddressingType member
    uds.addressing.AddressingType.is_member(uds.addressing.AddressingType.PHYSICAL)  # True
    uds.addressing.AddressingType.validate_member("Functional")  # uds.addressing.AddressingType.FUNCTIONAL
    uds.addressing.AddressingType.is_member(0)  # False
    uds.addressing.AddressingType.validate_member("not an addressing type")  # raises ValueError


TransmissionDirection
---------------------
:class:`~uds.addressing.transmission_direction.TransmissionDirection` class is enum with all possible communication
directions.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`

**Example code:**

  .. code-block::  python

    import uds

    # check if provided value is TransmissionDirection member
    uds.addressing.TransmissionDirection.is_member(uds.addressing.TransmissionDirection.RECEIVED)  # True
    uds.addressing.TransmissionDirection.validate_member("Tx")  # uds.addressing.TransmissionDirection.TRANSMITTED
    uds.addressing.TransmissionDirection.is_member("not a direction")  # False
    uds.addressing.TransmissionDirection.validate_member("not a direction")  # raises ValueError

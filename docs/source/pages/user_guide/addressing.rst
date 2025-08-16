.. _implementation-addressing:

Addressing
==========
The :ref:`addressing <knowledge-base-addressing>` related implementation that is common for all networks is located
in :mod:`uds.addressing` sub-package. Each network type has its own specific too.

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

    # check if provided value is AddressingType member
    uds.addressing.TransmissionDirection.is_member(uds.addressing.TransmissionDirection.RECEIVED)  # True
    uds.addressing.TransmissionDirection.validate_member("Tx")  # uds.addressing.TransmissionDirection.TRANSMITTED

.. _implementation-addressing:

Addressing
==========
The :ref:`addressing <knowledge-base-addressing>` related implementation common to all networks is located
in the :mod:`uds.addressing` sub-package.
Each network type has its own specific implementation for encoding addressing information and
extracting it from packets.


AddressingType
--------------
:class:`~uds.addressing.addressing_type.AddressingType` is an enum containing all possible UDS
:ref:`addressing <knowledge-base-addressing>` types.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` – check if a value is a valid enum member
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` – validate and convert a value to an enum member

**Example code:**

  .. code-block::  python

    import uds

    # check if provided value is AddressingType member
    uds.addressing.AddressingType.is_member(uds.addressing.AddressingType.PHYSICAL)  # True

    # convert a valid string to enum member
    uds.addressing.AddressingType.validate_member("Functional")  # uds.addressing.AddressingType.FUNCTIONAL

    # check invalid values
    uds.addressing.AddressingType.is_member(0)  # False
    uds.addressing.AddressingType.validate_member("not an addressing type")  # raises ValueError


TransmissionDirection
---------------------
:class:`~uds.addressing.transmission_direction.TransmissionDirection` is an enum containing all possible
communication directions.

Methods:

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` – check if a value is a valid enum member
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` – validate and convert a value to an enum member

**Example code:**

  .. code-block::  python

    import uds

    # check if provided value is TransmissionDirection member
    uds.addressing.TransmissionDirection.is_member(uds.addressing.TransmissionDirection.RECEIVED)  # True

    # convert a valid string to enum member
    uds.addressing.TransmissionDirection.validate_member("Tx")  # uds.addressing.TransmissionDirection.TRANSMITTED

    # check invalid values
    uds.addressing.TransmissionDirection.is_member("not a direction")  # False
    uds.addressing.TransmissionDirection.validate_member("not a direction")  # raises ValueError

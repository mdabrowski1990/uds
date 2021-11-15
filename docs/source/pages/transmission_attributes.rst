Transmission Attributes
=======================
Implementation of attributes that describes UDS communication.
It is located in :mod:`uds.transmission_attributes` sub-package.

We distinguish following transmission attributes:
 - `Transmission Direction`_
 - `Addressing Type`_


Transmission Direction
----------------------
Enum :class:`~uds.transmission_attributes.transmission_direction.TransmissionDirection` was implemented to provide
standard values of communication directions.


Addressing Type
---------------
Enum :class:`~uds.transmission_attributes.addressing.AddressingType` was implemented to define all possible values of
:ref:`addressing <knowledge-base-addressing>` that can be used for UDS communication.

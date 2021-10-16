Transmission Attributes
=======================
Implementation of attributes that describes UDS communication.

We distinguish following transmission attributes:
 - `Transmission Direction`_
 - `Addressing Type`_


Transmission Direction
----------------------
Enum :class:`~uds.transmission_attributes.transmission_direction.TransmissionDirection` was implemented to provide
standard values of communication directions.

Members defined in :class:`~uds.transmission_attributes.transmission_direction.TransmissionDirection` class:
 - :attr:`~uds.transmission_attributes.transmission_direction.TransmissionDirection.RECEIVED` - incoming communication
 - :attr:`~uds.transmission_attributes.transmission_direction.TransmissionDirection.TRANSMITTED` - outcoming communication

Methods implemented in :class:`~uds.transmission_attributes.transmission_direction.TransmissionDirection` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`


Addressing Type
---------------
Enum :class:`~uds.transmission_attributes.addressing.AddressingType` was implemented to define all possible values of
:ref:`addressing <knowledge-base-addressing>` that can be used for UDS communication.

Members defined in :class:`~uds.transmission_attributes.addressing.AddressingType` class:
 - :attr:`~uds.transmission_attributes.addressing.AddressingType.PHYSICAL` - direct one to one communication
   (:ref:`physical addressing <knowledge-base-physical-addressing>`)
 - :attr:`~uds.transmission_attributes.addressing.AddressingType.FUNCTIONAL` - one to many communication
   (:ref:`functional addressing <knowledge-base-functional-addressing>`)

Methods implemented in :class:`~uds.transmission_attributes.addressing.AddressingType` class:
 - :meth:`~uds.utilities.enums.ValidatedEnum.is_member`
 - :meth:`~uds.utilities.enums.ValidatedEnum.validate_member`


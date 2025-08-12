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

- :meth:`~uds.utilities.enums.ValidatedEnum.is_member` - check if provided value is defined as a member of this Enum
- :meth:`~uds.utilities.enums.ValidatedEnum.validate_member` - validate that provided value is defined as a member of
  this Enum


AbstractAddressingInformation
-----------------------------
:class:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation` defines common API and contains
common code for all addressing information storages.
Each concrete addressing information class stores addressing parameters of a single UDS entity for
a specific network type.

Attributes:

- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.rx_physical_params`
  - parameters for :ref:`physically addressed <knowledge-base-physical-addressing>` incoming communication
- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.tx_physical_params`
  - parameters for :ref:`physically addressed <knowledge-base-physical-addressing>` outgoing communication
- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.rx_functional_params`
  - parameters for :ref:`functionally addressed <knowledge-base-functional-addressing>` incoming communication
- :attr:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.tx_functional_params`
  - parameters for :ref:`functionally addressed <knowledge-base-functional-addressing>` outgoing communication

Methods:

- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.validate_addressing_params`
  - validate addressing parameters
- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.is_input_packet`
  - checks whether provided attributes of a frame carries :ref:`addressing information <knowledge-base-n-ai>`
  of an incoming packet for this UDS Entity
- :meth:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation.get_other_end`
  - get addressing information object with addressing parameters for UDS Entity on the other end of the communication
  (client's parameters if this is a server, or server's if this a client)

.. warning:: **A user shall not use**
  :class:`~uds.addressing.abstract_addressing_information.AbstractAddressingInformation`
  **directly** as this is `an abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_.

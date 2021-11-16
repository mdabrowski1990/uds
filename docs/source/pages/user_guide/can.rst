CAN Utilities
=============
Implementation of utilities that are specific for CAN bus is provided in :mod:`uds.can` sub-package.


CAN Frame
---------
Helper classes for following fields of CAN frame are available:
 - `DLC`_
 - `CAN Identifier`_

.. note:: CAN Frame has more fields, but only 3 of them are influenced by UDS protocol (DLC, CAN ID and Data).


DLC
```
Class :class:`~uds.can.can_frame_fields.CanDlcHandler` provides utilities for CAN Data Length Code (DLC) field of
CAN Frame.

Following features are provided by this class:

- Validation of CAN DLC and number of CAN Frame data bytes values.

  Provided by following methods:

  - :meth:`uds.can.can_frame_fields.CanDlcHandler.validate_dlc`
  - :meth:`uds.can.can_frame_fields.CanDlcHandler.validate_data_bytes_number`

  **Example code:**

    .. code-block::  python

        import uds

        # validate whether a value is CAN DLC value
        uds.can.CanDlcHandler.validate_dlc(0x0)
        uds.can.CanDlcHandler.validate_dlc(0x8)
        uds.can.CanDlcHandler.validate_dlc(0xF)

        # validate whether a value is CAN Frame data bytes number
        uds.can.CanDlcHandler.validate_data_bytes_number(1)
        uds.can.CanDlcHandler.validate_data_bytes_number(8)
        uds.can.CanDlcHandler.validate_data_bytes_number(64)

- Checking whether a value is CAN DLC value specific for CAN FD.

  Provided by following method:

  - :meth:`uds.can.can_frame_fields.CanDlcHandler.is_can_fd_specific_dlc`

  **Example code:**

    .. code-block::  python

        import uds

        uds.can.CanDlcHandler.is_can_fd_specific_dlc(0x0)
        uds.can.CanDlcHandler.is_can_fd_specific_dlc(0x8)
        uds.can.CanDlcHandler.is_can_fd_specific_dlc(0xF)

- Decoding DLC value into number of CAN frame data bytes.

  Provided by following method:

  - :meth:`uds.can.can_frame_fields.CanDlcHandler.decode_dlc`

  **Example code:**

    .. code-block::  python

        import uds

        uds.can.CanDlcHandler.decode_dlc(0x0)
        uds.can.CanDlcHandler.decode_dlc(0x8)
        uds.can.CanDlcHandler.decode_dlc(0xF)

- Encoding DLC value from number of CAN frame data bytes.

  Provided by following method:

  - :meth:`uds.can.can_frame_fields.CanDlcHandler.encode_dlc`
  - :meth:`uds.can.can_frame_fields.CanDlcHandler.get_min_dlc`

  **Example code:**

    .. code-block::  python

        import uds

        # get DLC value that carries provided number of data bytes
        uds.can.CanDlcHandler.encode_dlc(0)
        uds.can.CanDlcHandler.encode_dlc(8)
        uds.can.CanDlcHandler.encode_dlc(64)

        # get minimum DLC value that carries at least provided number of data bytes
        uds.can.CanDlcHandler.get_min_dlc(0)
        uds.can.CanDlcHandler.get_min_dlc(8)
        uds.can.CanDlcHandler.get_min_dlc(9)
        uds.can.CanDlcHandler.get_min_dlc(49)
        uds.can.CanDlcHandler.get_min_dlc(63)
        uds.can.CanDlcHandler.get_min_dlc(64)


CAN Identifier
``````````````
Class :class:`~uds.can.can_frame_fields.CanIdHandler` provides utilities for CAN Identifier (CAN ID) field of
CAN Frame.

Following features are provided by this class:

- Checking whether a value is CAN ID.

  Provided by following methods:

  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.validate_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_standard_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_extended_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_compatible_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_normal_11bit_addressed_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_normal_fixed_addressed_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_extended_addressed_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_mixed_11bit_addressed_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.is_mixed_29bit_addressed_can_id`

  **Example code:**

    .. code-block::  python

        import uds

        # check whether a value (0x7FF in example) is CAN ID
        uds.can.CanIdHandler.is_can_id(0x7FF)
        uds.can.CanIdHandler.validate_can_id(0x7FF)  # this one raises exception if value is not a CAN ID

        # check whether a CAN ID value (0x7FF and 0x800 in example) uses Standard (11-bit) CAN ID format
        uds.can.CanIdHandler.is_standard_can_id(0x7FF)
        uds.can.CanIdHandler.is_standard_can_id(0x800)

        # check whether a CAN ID value (0x7FF and 0x800 in example) uses Extended (29-bit) CAN ID format
        uds.can.CanIdHandler.is_extended_can_id(0x7FF)
        uds.can.CanIdHandler.is_extended_can_id(0x800)

        # check whether a CAN ID value is valid for provided CAN Addressing Format
        uds.can.CanIdHandler.is_compatible_can_id(can_id=0x7FF,
                                                  addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                  addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL)
        uds.can.CanIdHandler.is_compatible_can_id(can_id=0x18DB1234,
                                                  addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                                  addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL)
        uds.can.CanIdHandler.is_compatible_can_id(can_id=0x18CEFF00,
                                                  addressing_format=uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                  addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL)

- Decoding CAN Addressing Information from a CAN ID value.

  Provided by following methods:

  - :meth:`uds.can.can_frame_fields.CanIdHandler.decode_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.decode_normal_fixed_addressed_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.decode_mixed_addressed_29bit_can_id`

  **Example code:**

    .. code-block::  python

        import uds

        # decode Addressing Information (Addressing Type, Target Address, Source Address) from a CAN ID value
        uds.can.CanIdHandler.decode_can_id(addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                           can_id=0x7FF)
        uds.can.CanIdHandler.decode_can_id(addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                           can_id=0x18DB1234)
        uds.can.CanIdHandler.decode_can_id(addressing_format=uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                           can_id=0x18CEFF00)

  .. seealso:: `Addressing Information`_ and
      :meth:`uds.can.addressing_information.CanAddressingInformationHandler.decode_ai`

- Encoding CAN Addressing Information into a CAN ID value.

  Provided by following methods:

  - :meth:`uds.can.can_frame_fields.CanIdHandler.encode_normal_fixed_addressed_can_id`
  - :meth:`uds.can.can_frame_fields.CanIdHandler.encode_mixed_addressed_29bit_can_id`

  **Example code:**

    .. code-block::  python

        import uds

        # decode Addressing Information (Addressing Type, Target Address, Source Address) from a CAN ID value
        uds.can.CanIdHandler.decode_can_id(addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                           can_id=0x7FF)
        uds.can.CanIdHandler.decode_can_id(addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                           can_id=0x18DB1234)
        uds.can.CanIdHandler.decode_can_id(addressing_format=uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                           can_id=0x18CEFF00)


Addressing Information
----------------------
Class :class:`~uds.can.addressing_information.CanAddressingInformationHandler` contains CAN specific implementation of
:ref:`Addressing Information (N_AI) <knowledge-base-n-ai>`.

Following features are provided by this class:

- Validation of Addressing Information parameters.

  Provided by following methods:

  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai_normal_11bit`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai_normal_fixed`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai_extended`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai_mixed_11bit`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai_mixed_29bit`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.validate_ai_data_bytes`

  **Example code:**

    .. code-block::  python

        import uds

        # validate data bytes used for Addressing Information carrying
        uds.can.CanAddressingInformationHandler.validate_ai_data_bytes(addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                                       ai_data_bytes=[])
        uds.can.CanAddressingInformationHandler.validate_ai_data_bytes(addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
                                                                       ai_data_bytes=[0x5B])

        # validate all Addressing Information parameters
        uds.can.CanAddressingInformationHandler.validate_ai(addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                            addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                                            can_id=0x740)
        uds.can.CanAddressingInformationHandler.validate_ai(addressing_format=uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING,
                                                            addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL,
                                                            target_address=0x91,
                                                            source_address=0x0C,
                                                            address_extension=0x2E)

- Get number of CAN Frame data bytes used for carrying Addressing Information.

  Provided by following methods:

  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.get_ai_data_bytes_number`

  **Example code:**

    .. code-block::  python

        import uds

        uds.can.CanAddressingInformationHandler.get_ai_data_bytes_number(uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING)
        uds.can.CanAddressingInformationHandler.get_ai_data_bytes_number(uds.can.CanAddressingFormat.EXTENDED_ADDRESSING)
        uds.can.CanAddressingInformationHandler.get_ai_data_bytes_number(uds.can.CanAddressingFormat.MIXED_29BIT_ADDRESSING)

- Decoding Addressing Information parameters from CAN ID and CAN Frame data byte (if used).

  Provided by following methods:

  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.decode_ai`
  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.decode_ai_data_bytes`

  **Example code:**

    .. code-block::  python

        import uds

        TODO

- Encoding Addressing Information parameters into CAN ID and CAN Frame data byte (if used).

  Provided by following methods:

  - :meth:`uds.can.addressing_information.CanAddressingInformationHandler.encode_ai_data_bytes`


CAN Packets
-----------


Single Frame
````````````


First Frame
```````````


Consecutive Frame
`````````````````


Flow Control
````````````

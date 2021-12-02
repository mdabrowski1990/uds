Segmentation
============
Implementation of :ref:`segmentation process <knowledge-base-segmentation>` is located in :mod:`uds.segmentation`
sub-package.


AbstractSegmenter
-----------------
:class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` defines common API and contains common code for all
segmenter classes. Each concrete segmenter class handles segmentation process for a specific bus.

.. warning:: A **user shall not use** :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter` **directly**,
    but one is able (and encouraged) to use :class:`~uds.segmentation.abstract_segmenter.AbstractSegmenter`
    implementation with any of its children classes.


CanSegmenter
------------
:class:`~uds.segmentation.can_segmenter.CanSegmenter` handles segmentation process on CAN bus.

Following functionalities are provided by :class:`~uds.segmentation.can_segmenter.CanSegmenter`:

- Configuration of the segmenter:

  As a user, you are able to configure :class:`~uds.segmentation.can_segmenter.CanSegmenter` parameters which determines
  the format (e.g. Addressing Format), the content (e.g. Filler Byte) of CAN Packets and how they are created
  (e.g. whether to use CAN Frame Data Optimization).

  **Example code:**

    .. code-block::  python

        import uds

        # configure CAN Segmenter
        can_segmenter = uds.segmentation.CanSegmenter(addressing_format=uds.can.CanAddressingFormat.NORMAL_11BIT_ADDRESSING,
                                                      physical_ai={"can_id": 0x601},
                                                      functional_ai={"can_id": 0x6FF},
                                                      dlc=8,
                                                      use_data_optimization=False,
                                                      filler_byte=0xFF)

        # change CAN Segmenter configuration  (note: you cannot change addressing_format, create new segmenter instead)
        can_segmenter.physical_ai = {"can_id": 0x610}
        can_segmenter.functional_ai = {"can_id": 0x7FF}
        can_segmenter.dlc=0xF
        can_segmenter.use_data_optimization = True
        can_segmenter.filler_byte = 0xAA


- Diagnostic message segmentation:

  As a user, you are able to :ref:`segment diagnostic messages <knowledge-base-message-segmentation>`
  (objects of :class:`~uds.message.uds_message.UdsMessage` class) into CAN packets
  (objects for :class:`~uds.packet.can_packet.CanPacket` class).

  **Example code:**

    .. code-block::  python

        # let's assume that we have `can_segmenter` already configured as presented in configuration example above

        # define diagnostic message to segment
        uds_message_1 = uds.message.UdsMessage(payload=[0x3E, 0x00],
                                               addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL)
        uds_message_2 = uds.message.UdsMessage(payload=[0x62, 0x10, 0x00] + [0x20]*100,
                                               addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL)

        # use preconfigured segmenter to segment the diagnostic messages
        can_packets_1 = can_segmenter.segmentation(uds_message_1)  # output: Single Frame
        can_packets_2 = can_segmenter.segmentation(uds_message_2)  # output: First Frame with Consecutive Frame(s)

  .. note:: It is impossible to segment functionally addressed diagnostic message into First Frame and Consecutive Frame(s)
      as such result is considered incorrect according to :ref:`UDS ISO Standards <knowledge-base-uds-standards>`.


- CAN packets desegmentation:

  As a user, you are able to :ref:`desegment CAN packets <knowledge-base-packets-desegmentation>`
  (either objects of :class:`~uds.packet.can_packet.CanPacket` or :class:`~uds.packet.can_packet_record.CanPacketRecord` class)
  into diagnostic messages (either objects of :class:`~uds.message.uds_message.UdsMessage` or
  :class:`~uds.message.uds_message.UdsMessageRecord` class).

  **Example code:**

    .. code-block::  python

        # let's assume that we have `can_segmenter` already configured as presented in configuration example above

        # define CAN packets to desegment
        can_packets_1 = [
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.SINGLE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.EXTENDED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.FUNCTIONAL,
                                 can_id=0x6A5,
                                 target_address=0x0C,
                                 payload=[0x3E, 0x80])
        ]
        can_packets_2 = [
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.FIRST_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 dlc=8,
                                 data_length=15,
                                 payload=[0x62, 0x10, 0x00] + 3*[0x20]),
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.CONSECUTIVE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 dlc=8,
                                 sequence_number=1,
                                 payload=7*[0x20]),
            uds.packet.CanPacket(packet_type=uds.packet.CanPacketType.CONSECUTIVE_FRAME,
                                 addressing_format=uds.can.CanAddressingFormat.NORMAL_FIXED_ADDRESSING,
                                 addressing_type=uds.transmission_attributes.AddressingType.PHYSICAL,
                                 target_address=0x12,
                                 source_address=0xE0,
                                 sequence_number=1,
                                 payload=2 * [0x20],
                                 filler_byte=0x99)
        ]

        # use preconfigured segmenter to desegment the CAN packets
        uds_message_1 = can_segmenter.desegmentation(can_packets_1)
        uds_message_2 = can_segmenter.desegmentation(can_packets_2)

    .. warning:: Desegmentation performs only sanity check of CAN Packets content, therefore some inconsistencies
        with Diagnostic on CAN standard might be silently accepted as long as a message can be unambiguously decoded
        out of provided CAN packets.

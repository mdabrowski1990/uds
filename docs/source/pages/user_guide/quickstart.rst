Quickstart
==========
All steps required to start working with this package:

- `Installation`_
- `Define Addressing Information`_
- `Create Transport Interface`_
- `Send and Receive Packets`_
- `Send and Receive Messages`_

.. seealso:: :ref:`Code Examples <examples>`


Installation
------------

:shell:`pip install -U py-uds`

.. seealso:: :ref:`Installation Guide <installation>`


Define Addressing Information
-----------------------------
This step depends on network type used.

Example for CAN:

  .. code-block::  python

    import uds

    ecu_can_ai = uds.can.addressing.NormalCanAddressingInformation(
        rx_physical_params={"can_id": 0x7E8},
        tx_physical_params={"can_id": 0x7E0},
        rx_functional_params={"can_id": 0x7E8},
        tx_functional_params={"can_id": 0x7DF})

.. seealso:: :ref:`CAN Addressing Information definition <implementation-can-addressing-information>` and
  :ref:`Abstract Addressing Information implementation <implementation-abstract-addressing-information>`


Create Transport Interface
--------------------------
This step depends on network type and network manager used.

Example for CAN and `python-can <https://python-can.readthedocs.io>`_:

  .. code-block::  python

    # we assume steps from previous examples were performed
    from can import Bus

    can_bus = Bus(
        interface="kvaser",
        channel=0,
        receive_own_messages=True,
        bitrate=500_000,
        fd=True,
        data_bitrate=4_000_000)

    ti = uds.can.PyCanTransportInterface(
        network_manager=can_bus,
        addressing_information=ecu_can_ai)

.. seealso:: :ref:`python-can Transport Interface <implementation-can-python-can-transport-interface>` and
  :ref:`Abstract Transport Interface implementation <implementation-abstract-transport-interface>`


Send and Receive Packets
------------------------
This step depends on network type used.

Example for CAN:

  .. code-block::  python

    # we assume steps from previous examples were performed

    # define example packet to send (depends on network type - example for CAN bus)
    sf = uds.can.CanPacket(packet_type=uds.can.CanPacketType.SINGLE_FRAME,
                           payload=[0x3E, 0x00],
                           **ecu_can_ai.tx_functional_params)

    # send defined packet
    sent_packet_record = ti.send_packet(sf)
    # receive message
    received_packet_record = ti.receive_packet(timeout=None)  # no timeout


.. seealso:: :ref:`Packet implementation <implementation-packet>` and
  :ref:`CAN Packet implementation <implementation-can-packet>`


Send and Receive Messages
-------------------------
Example:
  .. code-block::  python

    # we assume Transport Interface is defined

    # define example message to send
    uds_message = uds.message.UdsMessage(payload=[0x10, 0x03],
                                         addressing_type=uds.addressing.AddressingType.PHYSICAL)

    # send defined message
    sent_message_record = ti.send_message(uds_message)
    # receive message
    received_message_record = ti.receive_message(timeout=1000)  # timeout in [ms]


.. seealso:: :ref:`Diagnostic Message implementation <implementation-diagnostic-message>`

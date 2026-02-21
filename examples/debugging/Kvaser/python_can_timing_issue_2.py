"""UDS Issue: https://github.com/mdabrowski1990/uds/issues/228"""

from time import time

from can import BufferedReader, Bus, Message, Notifier

if __name__ == "__main__":
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # connected with bus 1

    buffered_reader = BufferedReader()
    notifier = Notifier(bus=kvaser_interface_1, listeners=[buffered_reader])

    message = Message(data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0], arbitration_id=0x100)

    for _ in range(100):
        time_before_send = time()
        kvaser_interface_1.send(message)
        sent_message = buffered_reader.get_message(timeout=1)
        time_after_send = time()

        print(f"-----------------------------------------------\n"
              f"Result:\n"
              f"Timestamp before send: {time_before_send}\n"
              f"Message timestamp: {sent_message.timestamp}\n"
              f"Current timestamp: {time_after_send}\n"
              f"Message timestamp - Timestamp before send: {sent_message.timestamp - time_before_send:06f} (expected > 0)\n"
              f"Current timestamp - Message timestamp: {time_after_send - sent_message.timestamp:06f} (expected > 0)\n"
              f"Timestamp before send <= Message timestamp <= Current timestamp: {time_before_send <= sent_message.timestamp <= time_after_send} (expected `True`)")

    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()

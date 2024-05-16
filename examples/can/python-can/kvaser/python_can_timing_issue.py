"""UDS Issue: https://github.com/mdabrowski1990/uds/issues/228"""

from threading import Timer
from time import time

from can import BufferedReader, Bus, Message, Notifier

if __name__ == "__main__":
    kvaser_interface_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
    kvaser_interface_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # connected with bus 1

    buffered_reader = BufferedReader()
    notifier = Notifier(bus=kvaser_interface_1, listeners=[buffered_reader])

    message = Message(data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0], arbitration_id=0x100)

    for _ in range(10):
        Timer(interval=0.1, function=kvaser_interface_1.send, args=(message,)).start()

        sent_message = buffered_reader.get_message(timeout=1)
        timestamp_after_send = time()

        print(f"-----------------------------------------------\n"
              f"Result:\n"
              f"Message timestamp: {sent_message.timestamp}\n"
              f"Current timestamp: {timestamp_after_send}\n"
              f"Message timestamp <= Current timestamp: {sent_message.timestamp <= timestamp_after_send} (expected `True`)")

    kvaser_interface_1.shutdown()
    kvaser_interface_2.shutdown()

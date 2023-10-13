from time import time
from threading import Timer
from can import Notifier, BufferedReader, Bus, Message

if __name__ == "__main__":
    kvaser_bus_1 = Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
    kvaser_bus_2 = Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)  # connected with bus 1

    buffered_reader = BufferedReader()
    notifier = Notifier(bus=kvaser_bus_1, listeners=[buffered_reader])

    message = Message(data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0], arbitration_id=0x100)

    for _ in range(10):
        Timer(interval=0.1, function=kvaser_bus_1.send, args=(message, )).start()

        sent_message = buffered_reader.get_message(timeout=1)
        timestamp_after_send = time()

        print([sent_message.timestamp, timestamp_after_send, sent_message.timestamp <= timestamp_after_send])

    kvaser_bus_1.shutdown()
    kvaser_bus_2.shutdown()

import can

bus1 = can.Bus(interface="kvaser", channel=0, fd=True, receive_own_messages=True)
bus2 = can.Bus(interface="kvaser", channel=1, fd=True, receive_own_messages=True)
listener1 = can.BufferedReader()
listener2 = can.BufferedReader()
notifier1 = can.Notifier(bus=bus1, listeners=[listener1])
notifier2 = can.Notifier(bus=bus2, listeners=[listener2])


msg1 = can.Message(arbitration_id=0x123456,
                   dlc=64,
                   is_fd=True,
                   data=8*[0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])
msg2 = can.Message(arbitration_id=0x7FF,
                   dlc=8,
                   data=[0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF][::-1])

print("#MSG 1 sent to bus1")
bus1.send(msg=msg1)

print("#MSG 2 sent to bus1")
bus1.send(msg=msg2)

print("#MSG 2 sent to bus2")
bus2.send(msg=msg1)

print(listener1.get_message())
print(listener2.get_message())
print(listener1.get_message())
print(listener2.get_message())
print(listener1.get_message())
print(listener2.get_message())
print(listener1.get_message())
print(listener2.get_message())


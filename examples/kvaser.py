import can

bus1 = can.Bus(interface="kvaser", channel=0, fd=True)
bus2 = can.Bus(interface="kvaser", channel=1, fd=True)
listener = can.BufferedReader()
notifier = can.Notifier(bus=bus1, listeners=[listener])


msg1 = can.Message(arbitration_id=0x123456,
                   dlc=64,
                   is_fd=True,
                   data=8*[0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])
msg2 = can.Message(arbitration_id=0x7FF,
                   dlc=8,
                   data=[0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF][::-1])

bus1.send(msg=msg1)
bus1.send(msg=msg1)
bus2.send(msg=msg2)

print(listener.get_message())
print(listener.get_message())

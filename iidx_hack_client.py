import socket, time, inputs

## Client runs on the Linux VM and sends controller inputs to the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.2.2", 44717))

## send some data to indicate we've connected
                 # status      1-7 and start e1 and e2     turntable axis float
s.send(bytearray([0b00000001, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
print("Successfully established connection to server.")

a = 0

print("Awaiting controller connection...")

inputs.get_gamepad()

s.send(bytearray([0b00000010]))

while True:
    events = inputs.get_gamepad()
    
    for event in events:
        if 'eventType' == 'BUTTON':
            if control == '1':
                if value:
                    s.send(bytearray([0b11000001]))
                else:
                    s.send(bytearray([0b11100001]))
            if control == '2':
                if value:
                    s.send(bytearray([0b11000010]))
                else:
                    s.send(bytearray([0b11100010]))
            if control == '3':
                if value:
                    s.send(bytearray([0b11000011]))
                else:
                    s.send(bytearray([0b11100011]))
            if control == '4':
                if value:
                    s.send(bytearray([0b11000100]))
                else:
                    s.send(bytearray([0b11100100]))
            if control == '5':
                if value:
                    s.send(bytearray([0b11000101]))
                else:
                    s.send(bytearray([0b11100101]))
            if control == '6':
                if value:
                    s.send(bytearray([0b11000110]))
                else:
                    s.send(bytearray([0b11100110]))
            if control == '7':
                if value:
                    s.send(bytearray([0b11000111]))
                else:
                    s.send(bytearray([0b11100111]))
            if control == 'E1':
                if value:
                    s.send(bytearray([0b11001000]))
                else:
                    s.send(bytearray([0b11101000]))
            if control == 'E2':
                if value:
                    s.send(bytearray([0b11001001]))
                else:
                    s.send(bytearray([0b11101001]))

    time.sleep(0.01)
    pass
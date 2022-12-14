import socket, time, inputs

## Client runs on the Linux VM and sends controller inputs to the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.2.2", 44717))

## send some data to indicate we've connected
                 # status      1-7 and start e1 and e2     turntable axis float
s.send(bytearray([0b00000001, 0b00000000]))
print("Successfully established connection to server.")

a = 0

print("Awaiting controller connection...")

inputs.get_gamepad()

s.send(bytearray([0b00000010, 0b00000000]))

# codes
KEY1 = 'BTN_TRIGGER'
KEY2 = 'BTN_THUMB'
KEY3 = 'BTN_THUMB2'
KEY4 = 'BTN_TOP'
KEY5 = 'BTN_TOP2'
KEY6 = 'BTN_PINKIE'
KEY7 = 'BTN_BASE'
E1 = 'BTN_BASE3'
E2 = 'BTN_BASE4'


while True:
    events = inputs.get_gamepad()
    
    for event in events:
        if event.code == KEY1:
            if event.state:
                s.send(bytearray([0b11000001, 0b00000000]))
            else:
                s.send(bytearray([0b11100001, 0b00000000]))
        if event.code == KEY2:
            if event.state:
                s.send(bytearray([0b11000010, 0b00000000]))
            else:
                s.send(bytearray([0b11100010, 0b00000000]))
        if event.code == KEY3:
            if event.state:
                s.send(bytearray([0b11000011, 0b00000000]))
            else:
                s.send(bytearray([0b11100011, 0b00000000]))
        if event.code == KEY4:
            if event.state:
                s.send(bytearray([0b11000100, 0b00000000]))
            else:
                s.send(bytearray([0b11100100, 0b00000000]))
        if event.code == KEY5:
            if event.state:
                s.send(bytearray([0b11000101, 0b00000000]))
            else:
                s.send(bytearray([0b11100101, 0b00000000]))
        if event.code == KEY6:
            if event.state:
                s.send(bytearray([0b11000110, 0b00000000]))
            else:
                s.send(bytearray([0b11100110, 0b00000000]))
        if event.code == KEY7:
            if event.state:
                s.send(bytearray([0b11000111, 0b00000000]))
            else:
                s.send(bytearray([0b11100111, 0b00000000]))
        if event.code == E1:
            if event.state:
                s.send(bytearray([0b11001000, 0b00000000]))
            else:
                s.send(bytearray([0b11101000, 0b00000000]))
        if event.code == E2:
            if event.state:
                s.send(bytearray([0b11001001, 0b00000000]))
            else:
                s.send(bytearray([0b11101001, 0b00000000]))
        if event.code == 'ABS_X':
            s.send(bytearray([0b11110000, event.state + 127]))

    #time.sleep(0.01)
    pass
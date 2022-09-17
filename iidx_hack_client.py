import socket, time

## Client runs on the Linux VM and sends controller inputs to the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.2.2", 44717))

## send some data to indicate we've connected
                 # status      1-7 and start e1 and e2     turntable axis float
s.send(bytearray([0b00000001, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))

while True:
    ## nothing yet i just want to test the connection
    time.sleep(10); 
    s.send(bytearray([0b11111111, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
    pass
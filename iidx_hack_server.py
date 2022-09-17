import socketserver

## Server runs on the host Windows machine and creates a virtual gamepad

class IIDXHackTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(49)
            if self.data[0] == 0b00000001:
                print("[status] a connection has been successfully established")
            if self.data[0] == 0b11111111:
                print("[status] recieved 128 (you are either doing this on purpose or have encountered an error)")
        pass

with socketserver.TCPServer(('127.0.0.1', 44717), IIDXHackTCPHandler) as server:
    print("[status] setting up server...")
    server.serve_forever()
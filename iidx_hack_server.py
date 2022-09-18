import socketserver, vgamepad

## Server runs on the host Windows machine and creates a virtual gamepad

class IIDXHackTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.gamepad = None
        
        self.data = self.request.recv(64)
        self.dataindex = 0
        self.curmessage = []
        while True:

            for msgbyte in self.data:
                if len(self.curmessage) < 2:
                    self.curmessage.append(msgbyte)
                
                if len(self.curmessage) == 2:
                    self.readMessage(self.curmessage)
                    self.curmessage = []
                self.dataindex += 1

            if self.dataindex == len(self.data):
                self.data = self.request.recv(64)
                self.dataindex = 0            
    
    def readMessage(self, message):
        if message[0] == 0b00000001: #connection state change
            print("[status] a connection has been successfully established")
        if message[0] == 0b00000010: #controller connected
            print("[status] controller connected")
            self.gamepad = vgamepad.VDS4Gamepad()
                                
            self.gamepad.update()
        if message[0] == 0b00000011: #disconnected
            self.gamepad = None
        if message[0] == 0b11111111:
            print("[status] recieved 128 (you are either doing this on purpose or have encountered an error)")
        # i dont understand bytes so i will just hardcore this for now. i'm sorry. it works.
        ## PRESS EVENTS
        if message[0] == 0b11000001: # press key 1
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
        if message[0] == 0b11000010: # press key 2
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
        if message[0] == 0b11000011: # press key 3
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE)
        if message[0] == 0b11000100: # press key 4
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        if message[0] == 0b11000101: # press key 5
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
        if message[0] == 0b11000110: # press key 6
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
        if message[0] == 0b11000111: # press key 7
            ## vgamepad doesn't seem to have a way to press Button 7, at least not in a way
            ## that the HTML5 Gamepad API will see, which bothers me. I could use the left
            ## trigger, but using an axis for a key input seems to cause major problems in
            ## beatoraja so I'm opting to use the left thumbstick button instead.
            ## I hope this doesn't cause problems with Infinitas lmao but I believe you
            ## can set your keybindings in that game so hopefully it wouldn't be a problem.
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT)
        if message[0] == 0b11001000: # e1
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHARE)
        if message[0] == 0b11001001: # e2
            self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
        ## UNPRESS EVENTS
        if message[0] == 0b11100001: # press key 1
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
        if message[0] == 0b11100010: # press key 2
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
        if message[0] == 0b11100011: # press key 3
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE)
        if message[0] == 0b11100100: # press key 4
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        if message[0] == 0b11100101: # press key 5
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
        if message[0] == 0b11100110: # press key 6
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
        if message[0] == 0b11100111: # press key 7
            ## see the equivalent comment in the press section
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT)
        if message[0] == 0b11101000: # e1
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHARE)
        if message[0] == 0b11101001: # e2
            self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
        ## Turntable
        if message[0] == 0b11110000: # turntable axis in the next 4 bytes
            ## raw value is -127 to 127, it seems; on the client end I add
            ## 127 to the value so it's within the range of 0-254 so i can just
            ## send the raw int as a byte.  
            self.gamepad.left_joystick(message[1], 128)
        if not self.gamepad == None:
            self.gamepad.update()
        pass

with socketserver.TCPServer(('127.0.0.1', 44717), IIDXHackTCPHandler) as server:
    print("[status] setting up server...")
    server.serve_forever()
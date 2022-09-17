import socketserver, vgamepad

## Server runs on the host Windows machine and creates a virtual gamepad

class IIDXHackTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.gamepad = None
        while True:
            self.data = self.request.recv(49)
            if self.data[0] == 0b00000001: #connection state change
                print("[status] a connection has been successfully established")
            if self.data[0] == 0b00000010: #controller connected
                print("[status] controller connected")
                self.gamepad = vgamepad.VDS4Gamepad()
                                    
                self.gamepad.update()
            if self.data[0] == 0b00000011: #disconnected
                self.gamepad = None
            if self.data[0] == 0b11111111:
                print("[status] recieved 128 (you are either doing this on purpose or have encountered an error)")
            # i dont understand bytes so i will just hardcore this for now. i'm sorry. it works.
            ## PRESS EVENTS
            if self.data[0] == 0b11000001: # press key 1
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
            if self.data[0] == 0b11000010: # press key 2
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            if self.data[0] == 0b11000011: # press key 3
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE)
            if self.data[0] == 0b11000100: # press key 4
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
            if self.data[0] == 0b11000101: # press key 5
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
            if self.data[0] == 0b11000110: # press key 6
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
            if self.data[0] == 0b11000111: # press key 7
                ## assigned to what is button 10 in the HTML5 gamepad api; I cannot seem to activate
                ## button 6, what it should be, with vgamepad
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT)
            if self.data[0] == 0b11001000: # e1
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHARE)
            if self.data[0] == 0b11001001: # e2
                self.gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
            ## UNPRESS EVENTS
            if self.data[0] == 0b11100001: # press key 1
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
            if self.data[0] == 0b11100010: # press key 2
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            if self.data[0] == 0b11100011: # press key 3
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE)
            if self.data[0] == 0b11100100: # press key 4
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
            if self.data[0] == 0b11100101: # press key 5
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
            if self.data[0] == 0b11100110: # press key 6
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
            if self.data[0] == 0b11100111: # press key 7
                ## assigned to what is button 10 in the HTML5 gamepad api; I cannot seem to activate
                ## button 6, what it should be, with vgamepad
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT)
            if self.data[0] == 0b11101000: # e1
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_SHARE)
            if self.data[0] == 0b11101001: # e2
                self.gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
            ## Turntable
            if self.data[0] == 0b11110000: # turntable axis in the next 4 bytes
                ## raw value is -127 to 127, it seems; on the client end I add
                ## 127 to the value so it's within the range of 0-254 so i can just
                ## send the raw int as a byte.  
                self.gamepad.left_joystick(self.data[1], 128)
            if not self.gamepad == None:
                self.gamepad.update()
        pass

with socketserver.TCPServer(('127.0.0.1', 44717), IIDXHackTCPHandler) as server:
    print("[status] setting up server...")
    server.serve_forever()
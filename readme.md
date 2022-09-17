# IIDX Con Hack
## What this is, and why I need to use it
This is a program I'm writing/have written in order to get my official Konami IIDX Entry Model
controller to actually frickin work on my PC. For some reason, the controller is completely unresponsive if I plug it into my PC directly,
but works completely fine inside a virtual machine, so this program provides:

- A server run on a host Windows machine that acts as a virtual DirectInput controller via ViGEmBus,
- A client run on a guest Linux VM that takes the controller inputs and transmits them to the server across the local network

I initially attempted to use Steam Link for this purpose but the problem there is that requires a GUI (extra processing overhead)
and also, more importantly, seemed to lock the controller's polling rate to somewhere between 50 and 60 Hz, which is absolutely
abysmal. This program attempts to act as a better solution because there is very few things out there that seem to do what I need
them to do; I don't even know what to *look* for when it comes to trying to find a controller-over-network solution. The closest
I managed to find was NetInput, but that's Windows only and I don't want to have to set up a Windows VM personally because I'm
trying to limit how much resources are dedicated to the VM since I, frankly, shouldn't have to be using one in the first place,
but here we are I suppose.

This program was made to do an extremely specific thing and nothing else so I forgive you if you question why I even needed this
in the first place. It could theoretically be expanded upon to be a general controller-over-network app, but for the time being
I have no need for that; feel free to screw around with the code yourself if you want to expand upon it but I will likely
be keeping the scope here somewhat limited for the sake of simplicity.

## Dependencies
Linux/Client end:
- `Gamepad` library

Windows/Server end:
- `ViGEmBus`
- `vgamepad` library

## Usage
No usage instructions yet as the program hasn't actually been written yet. 
# IIDX Con Hack
Provides a simple client/server program to send inputs from an official
Konami IIDX Entry Model controller over a network connection from a guest
virtual machine back to the host,  intended for if you're stuck in a bizarre
situation like I was when this controller refused to work normally but ended up
working fine in a VM.


## IMPORTANT

**This workaround does not fully support use with *IIDX INFINITAS*, and may never.** Due to limitations with the library I'm using for this hack, it seems that there is no way to get the game to read analog turntable input from this hack (it only looks at axis 1, which is what the dpad is assigned to and there is seemingly no way to use it as a regular analog axis as far as I can tell.) So, currently, only the buttons are usable there - I may get around to implementing digital turntable logic in order to at least partially support Infinitas but at the moment this workaround is only suitable for use with beatoraja.

## Requirements
* Host side:
  * Python 3
  * [ViGEmBus](https://github.com/ViGEm/ViGEmBus)
  * [vgamepad Python library](https://pypi.org/project/vgamepad/)
* Guest side:
  * Python 3
  * [inputs Python library](https://pypi.org/project/inputs/)

## Usage insutrctions
This assumes you already have a virtual machine environment set up and have Python installed 
on both your host and guest; I won't go into detail here about how to set those up for the
sake of simplicity (and the VM setup will likely slightly differ depending on what OS
you want to use for it).

### Host side
1. Install [the latest release of ViGEmBus](https://github.com/ViGEm/ViGEmBus/releases/latest);
   this is required to actually create the virtual gamepad on the host end.
2. Install the vgamepad library with `pip`: 
   ```
   pip install vgamepad
   ```
3. Clone the repository:
   ```
   git clone https://github.com/Tiyenti/iidx-con-hack.git
   ```
4. When required, open a terminal in the directory you downloaded the repository to and run the
   server with Python. 
   ```
   python iidx_hack_server.py
   ```

### Guest side
1. If using VirtualBox for your VM, make sure that your network adapter type is set to **NAT**.
   This seems to be required; the client code connets to `10.0.2.2` which allows a NAT-type adapter to access the host machine's `127.0.0.1`, what the server runs on. If you are using
   a different virtual machine platform, I am sure that a similar setting exists but I cannot
   speak from experience. Look up the relevant information to your VM platform.
2. Install the inputs library with `pip`: 
   ```
   pip install inputs
   ```
3. Clone the repository:
   ```
   git clone https://github.com/Tiyenti/iidx-con-hack.git
   ```
4. When required, open a terminal in the directory you downloaded the repository to and run the
   client with Python. 
   ```
   python iidx_hack_client.py
   ```
5. After starting the client, press a button on the controller after seeing `Awaiting controller input...` to detect the controller.

Once both the guest side and host side setup is done, you should now successfully have a working
IIDX controller.

## Implementation notes
* The **server** is run on the Windows host, and recieves the inputs sent from
  the **client**, which runs on the guest VM. The server is hosted on localhost
  on port `44717`.
* The virtual controller on the Windows side is created as a virtual DualShock 4 controller. At the time of making this hack I assumed that Infinitas wouldn't support xinput devices, although I now know I'm mistaken there. This is just the design decision that I initially went with and it'd take too much effort to change. (It doesn't work with Infinitas properly anyway, though, as mentioned above.)
* There is no specific polling rate set, the client (that processes the inputs) will just
  send messages of 2 bytes each to the server whenever it detects an input. In theory, this should poll
  at roughly the same rate the controller normally polls at. My testing appeared to show at least 200Hz,
  probably closer to 220Hz, which I tested with a modified version of this code that instead created an XInput device and used [XInputTest](https://github.com/chrizonix/XInputTest) to
  determine the rate.
* Raw turntable input is seemingly in the range of -127 to 127 on the guest side in my tests and is converted to a 0 to 254 range by the client before being sent to the server. This *might* cause problems as vgamepad's DS4 API represents analog inputs in a 0 to 255 range, but hopefully it's not too noticeable.
* The buttons are bound to the following bindings in the HTML5 gamepad API, according to [gamepad-tester.com](https://gamepad-tester.com/):
  * IIDX: Gamepad API (DS4 Button)
  * Key 1: Button 0 (Cross)
  * Key 2: Button 1 (Circle)
  * Key 3: Button 2 (Square)
  * Key 4: Button 3 (Triangle)
  * Key 5: Button 4 (L1 / Left Shoulder)
  * Key 6: Button 5 (R1 / Right Shoulder)
  * Key 7: Button 10 (L3 / Left Stick Click) - *Chosen as vgamepad doesn't seem to have a way to trigger button 6, at least in DS4 mode; I can use the left trigger axis instead, but using an analog axis for the keys causes severe issues in beatoraja, such as resulting in keys being unable to be held down*
  * E1/Start: Button 8 (Options)
  * E2/Select: Button 9 (Share)
  * Turntable: Axis 0 (Left Sick Horizontal)

## wait hold on what is this actually for why do you need this
*This is mostly contextual information given the hyper specific niche this
fills; you can skip this section if you already know why you're here.*

The context for this is somewhat complex but the gist of it is that the
controller seems to not  like my PC for whatever reason, being completely
unreponsive if plugged in normally, but somehow, it manages to work
perfectly fine if passed into a guest virtual machine. Which is absolutely
bizarre, but alright, fine. If that's the way things are, then sure. I can
work with that. I just need a way to get those inputs *out* of the VM and
back into my host machine as a controller I can use for any game I want.

Initially I tried using the Steam Link Linux client combined with GlosSI for this,
but this wasn't ideal. For one thing, it needed a GUI, so that would be adding extra
processing overhead, but the more important reason is that the polling rate was
absolutely *horrible* - it seems to be limited to around 60Hz, which is maybe fine
for simple games but for a rhythm game like IIDX/BMS with a heavy focus on consistent
timing? Hell no. That's not gonna work at all.

So... in the absense of any other working solution that I could find to send controller
inputs over a network connection - the only way I could concievably achieve the task I
wanted - I suddenly remembered that, oh yeah, I know how to code. So I just did it myself.
I hope it isn't broken.
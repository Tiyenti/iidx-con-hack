# IIDX Con Hack
Provides a simple client/server program to send inputs from an official
Konami IIDX Entry Model controller over a network connection from a guest
virtual machine back to the host,  intended for if you're stuck in a bizarre
situation like I was when this controller refused to work normally but ended up
working fine in a VM.

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

## Potential issues
I have not thouroughly tested this yet, so there may be some problems.

* It has so far been tested on a Windows 10 Home host with an Ubuntu virtual machine,
  using the workaround to play *beatoraja*. This appears to work alright.
* **One potential issue:** One time during my initial hour or so of testing this, I had a
  problem where a key got stuck being held down. This however has so far only happened once.
  At this time I am not sure if this was due to the controller itself, or something to do
  with my code (perhaps an input release event was not sent properly, or was dropped due to being
  recieved at the same time as another event, and I so far am only checking 1 byte of data
  at a time, potentially casuing problems).
* I will most likely be using this solution for my beatmania sessions for the forseeable
  future so if any issues become apparent I will definitely become aware of them lmao

## Implementation notes
* The **server** is run on the Windows host, and recieves the inputs sent from
  the **client**, which runs on the guest VM. The server is hosted on localhost
  on port `44717`.
* The virtual controller on the Windows side is created as a virtual DS4 controller;
  I chose this as I believe this means it's using DirectInput, which as far as I
  am aware is the only controller API that the official *beatmania IIDX INFINITAS*
  client supports. I have not actually tested this with *INFINITAS* yet however as
  I am too lazy to and don't want to spend the money on it right now.
* There is no specific polling rate set, the client (that processes the inputs) will just
  send 1 (button) or 2 (turntable) bytes to the server whenever it detects an input. In theory, this should poll
  at the same rate the controller normally polls at. My testing appeared to show at least 200Hz,
  probably closer to 220Hz, which I tested with a modified version of this code that instead created an XInput device and used [XInputTest](https://github.com/chrizonix/XInputTest) to
  determine the rate.
* Raw turntable input is seemingly in the range of -127 to 127 on the guest side in my tests and is converted to a 0 to 254 range by the client before being sent to the server. This *might* cause problems as vgamepad represents analog inputs in a 0 to 255 range, but hopefully it's not too noticeable.
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
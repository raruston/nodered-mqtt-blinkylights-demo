# Node-RED, MQTT and Pimoroni UnicornHAT Demo

This repository contains the various components needed to set up a simple 
control mechanism for a UnicornHAT sitting on a Raspberry Pi. It uses Node-RED 
to provide a direct control mechanism via Inject nodes, an API, and a simple web
UI. MQTT is used as an interface between Node-RED and the Python code which 
actually controls the UnicornHAT via the provided Python API.

It would be possible to drive the UnicornHAT directly from Node-RED, and using 
MQTT is more flexible and simplifies some of the control. For example, it would
be trivial to have the Unicorn HAT mounted on a different Pi, or have several
Pis all with their own UnicornHATs all bowing down to a single Node-RED 
controller. 

**Note:** This should run on any Raspberry Pi 2 B or Pi B+, but it has only been
tested on the Pi 2.

### Pre-requisites
To use this code, you should already have followed the relevant instructions for
installing the following:

* Unicorn HAT - https://github.com/pimoroni/unicorn-hat
* Node.js and Node-RED - http://nodered.org/docs/hardware/raspberrypi.html
* Mosquitto MQTT Broker - http://mosquitto.org/download/
* Python Client for MQTT (paho-mqtt 1.1) https://pypi.python.org/pypi/paho-mqtt

### Installing

Simply copy the files provided to an appropriate location on your Pi
For access to the Web UI, the user used to start Node-RED must have permission
to read the files in the webui folder.

The flows folder contains Node-RED flows exported to JSON which need to be 
imported to Node-RED. Once imported, the webui flows need to be modified so the 
file node points to the correct location based on where you put the files.

### Running

1. Ensure Node-RED and MQTT are running
2. Start the Python control 
```bash
sudo python uhcontrol.py
```
3. Use the inject nodes from the directcontrol flows to test everything works.
4. The webui can be accessed at http://hostname:noderedpport/lights


### How it works

**uhcontrol**
Starting at the lowest level, the uhcontrol.py script is a long running script
which subscribes to the "pi/uhcontrol" topic, and waits for messages. The only
way to terminate the script is to break out using CTRL-C (or kill if running in
the background) or by publishing a specific message to the topic - more on that 
shortly. The script connects to a local MQTT broker by default, but there is
no reason this couldn't point to a remote broker.

Once a message is received from the broker, the script parses it, and based on 
the content triggers an action. The script expects the message payload to be a 
simple JSON object containing an 'opcode'. **Note** that there is little to no 
error checking or validation going on, this is just a demo/plaything after all.

The script then uses the UnicornHAT Python API to do different stuff depending 
on the opcode. This ranges from the simple, such as setting all the LEDs to the 
same colour, to the more complicated such as simulating the starting lights of 
an F1 race, and causing the the UH to pulse.

The 'pulse' action is a little different from the others, and worth explaining
further. The uhcontrol script is single threaded with the exception of the 
pulse action. This means that when a message is received via MQTT, the main 
thread parses it, performs the action, and then goes back to waiting for the
next message. The pulse action requires a constant loop to make the UH pulse, 
and if you do that on the main thread it would never be in a position to check
for the message.

The solution was to offload the pulse code to a new thread, and to provide 
'start' and 'stop' opcodes to control it. This is fine except that there is no 
protection against running multiple, conflicting, actions at once. If you inject
multiple actions while pulse is running, the behaviour is 'undefined'.

**MQTT*
Not a lot to say here - I just used the default install of Mosquitto and it just
worked

**Node-RED**
The flows here are quite simple and should be pretty self explanatory. 

The directcontrol flows just send a pre-defined JSON string to the MQTT node 
which publishes it to the "pi/uhcontrol" topic. 

The api flows provide HTTP endpoints for the api and map the api request to the 
opcode object required by the uhcontrol script, and then publishes it to MQTT.

Finally, the webui flows provide the Web UI HTML and CSS which exploits the 
API and lets you turn the UH on and off.

Simples.

# Thanks and Acknowledgements

The code for generating the pulse effect comes from **@sandyjmacdonald** and is based
on his post here: http://sandyjmacdonald.github.io/2014/12/29/controlling-the-pimoroni-unicorn-hat-with-the-skywriter/

Thanks to:
* The team at @pimoroni (for a cool piece of kit, and the useful example
code which served as the basis for the controller).

* The @raspberry_pi foundation for the Pi itself.

* @monkeymademe for demoing the UnicornHAT at @raspijamberlin and inspiring me to get one and have a play.






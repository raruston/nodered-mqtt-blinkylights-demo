# Node-RED, MQTT and Pimoroni UnicornHAT Demo

This repository contains the various components needed to set up a simple 
control mechanism for a UnicornHAT sitting on a Raspberry Pi. It uses Node-RED 
to provide a direct control mechanism via Inject nodes, an API, and a simple web
UI. MQTT is used as an interface between Node-RED and the Python code which 
actually controls the UnicornHAT via the provided Python API.

It would be possible to drive the UnicornHAT directly from Node-RED, and that
actually seemed more complicated than having a single backend script to 
interface with the UnicornHAT, and controlling that via MQTT.

**Note:** This should run on any Raspberry Pi 2 B or Pi B+, but it has only been
tested on the Pi 2.

### Pre-requisites
To use this code, you should already have followed the relevant instructions for
installing the following:

Unicorn HAT - https://github.com/pimoroni/unicorn-hat
Node.js and Node-RED - http://nodered.org/docs/hardware/raspberrypi.html
Mosquitto MQTT Broker - http://mosquitto.org/download/


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


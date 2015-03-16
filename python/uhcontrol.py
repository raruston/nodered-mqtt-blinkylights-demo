import paho.mqtt.client as mqtt
import unicornhat as UH
import time, colorsys, thread
import simplejson as json
import random
import numpy as np
from time import sleep
import sys

working = False
contWorking = False

# Set the UH to full white
def uh_setFullColour(r, g, b, brightness = 0.2):
    UH.off()
    UH.brightness(brightness)
    for y in range(8):
        for x in range(8):
            UH.set_pixel(x,y,r,g,b)
    UH.show()
   
# F1 Style Start
def uh_f1start(b = 0.2):
    UH.off()
    UH.brightness(b)
    UH.rotation(180)
    for x in range(2):
        for y in range(8):
            UH.set_pixel(x,y,255,0,0)
    UH.show()
    sleep(1)
    for x in range(2,4):
        for y in range(8):
            UH.set_pixel(x,y,255,0,0)
    UH.show()
    sleep(1)
    for x in range(4,6):
        for y in range(8):
            UH.set_pixel(x,y,255,0,0)
    UH.show()
    sleep(1)
    for x in range(6,8):
        for y in range(8):
            UH.set_pixel(x,y,255,0,0)
    UH.show()
    delayswitch =  random.random()
    delay = random.random()
    if delayswitch > 0.66:
        sleep(6 + delay)
    elif delayswitch > 0.33:
        sleep(5 + delay)
    else:
        sleep(4 + delay)
    UH.off()

def make_gaussian(fwhm, x0, y0):
    x = np.arange(0, 8, 1, float)
    y = x[:, np.newaxis]
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

def uh_pulse():	
    UH.off()
    global working
    working = True
    global contWorking
    contWorking = True
    while contWorking == True:
        x0, y0 = 3.5, 3.5
        for z in range(1, 5)[::-1] + range(1, 10):
            fwhm = 5/z
            gauss = make_gaussian(fwhm, x0, y0)
            for y in range(8):
                for x in range(8):
                    h = 0.8
                    s = 0.8
                    v = gauss[x,y]
                    rgb = colorsys.hsv_to_rgb(h, s, v)
                    r = int(rgb[0] * 255.0)
                    g = int(rgb[1] * 255.0)
                    b = int(rgb[2] * 255.0)
                    UH.set_pixel(x, y, r, g, b)
            UH.show()
            time.sleep(0.025)
	UH.off()
    working = False
    
# Handle command
def handleRequest(req):
    #print ("OpCode: " + req['opcode'])
    if (req['opcode'] == '0'):
        UH.off()
    elif (req['opcode'] == '1'):
        uh_setFullColour(255,255,255)
    elif (req['opcode'] == '2'):
        uh_setFullColour(255,0,0)
    elif (req['opcode'] == '3'):
        uh_setFullColour(255,153,0)
    elif (req['opcode'] == '4'):
        uh_setFullColour(0,255,0)
    elif (req['opcode'] == '40'):
        try:
            thread.start_new_thread(uh_pulse, ())   
        except:
            print "Error: unable to start thread"        
    elif (req['opcode'] == '41'):
        global contWorking
        contWorking = False	
    elif (req['opcode'] == '50'):	
        uh_f1start()
    elif (req['opcode'] == '99'):
        UH.off()
        print ("Exit request received")
        sys.exit(0) 
        
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("pi/uhcontrol")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print("Request received: " + str(msg.payload))
    req = json.loads(msg.payload)
    handleRequest(req)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

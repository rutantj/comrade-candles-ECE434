#!/usr/bin/python3
import time
import math
import Adafruit_BBIO.GPIO as GPIO
from flask import Flask, render_template, request

#GPIO Button Setup
colorButton = "P8_15"
flashButton = "P8_10"
GPIO.setup(colorButton, GPIO.IN) 
GPIO.setup(flashButton, GPIO.IN) 

LEDlength = 60
r=1
g=1
b=1
current = -1
amp = 12
f = 5
shift = 3
phase = 0 
currFlash = 0
flashSpeeds = [0, 0.1, 0.25, 0.5, 1]
flashLength = len(flashSpeeds)
flashDelay = 0

colors = [[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1], [1,1,1], [0,0,0]]
length = len(colors)

# Open a file
fo = open("/dev/rpmsg_pru30", "wb", 0)


def changeColor(colorButton):
    global current
    global length
    current += 1 
    current %= length
    color = colors[current]
    r = color[0]
    g = color[1]
    b = color[2]
    time.sleep(0.01) #debounce delay
    for i in range(0, LEDlength):
        fo.write(b"%d %d %d %d\n" % (i, r, g, b))
    fo.write(b"-1 0 0 0\n");    # Send colors to LEDs

def changeFlash(flashButton):
    global currFlash
    global flashLength
    global flashDelay
    currFlash += 1
    currFlash %= flashLength
    flashDelay = flashSpeeds[currFlash]
    print("FlashDelay: ", flashDelay)

GPIO.add_event_detect(colorButton, GPIO.FALLING, callback=changeColor)
GPIO.add_event_detect(flashButton, GPIO.FALLING, callback=changeFlash)

for i in range(0, LEDlength):
    fo.write(b"%d %d %d %d\n" % (i, r, g, b))
fo.write(b"-1 0 0 0\n");    # Send colors to LEDs


#online stuff ##################################################################################################

app = Flask(__name__)
@app.route("/")
def index():
	templateData = {
              'title' : 'Comrade Candle control!',
        }
	return render_template('remoteVirtual.html', **templateData)
	
@app.route("/<red>/<green>/<blue>/<browserAction>")
def action(red, green, blue, browserAction):
	#if (browserAction == "yes")
	#   Send same url with browserAction changed to "no" to other bone.
	r = int(red)
	g = int(green)
	b = int(blue)
	
	templateData = {
	}
	return render_template('remoteVirtual.html', **templateData)
	

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)

#end of online stuff ##################################################################################################

# steady state code
while True:
    if current==length-1:
        for i in range(0, LEDlength):
            r = (amp * (math.sin(2*math.pi*f*(i-phase-0*shift)/LEDlength) + 1)) + 1;
            g = (amp * (math.sin(2*math.pi*f*(i-phase-1*shift)/LEDlength) + 1)) + 1;
            b = (amp * (math.sin(2*math.pi*f*(i-phase-2*shift)/LEDlength) + 1)) + 1;
            fo.write(b"%d %d %d %d\n" % (i, r, g, b))
        fo.write(b"-1 0 0 0\n");
        phase=phase+1+(flashDelay*5)
        time.sleep(0.05)
    else:
        color = colors[current]
        r = color[0]
        g = color[1]
        b = color[2]
        for i in range(0, LEDlength):
            fo.write(b"%d %d %d %d\n" % (i, r, g, b))
        fo.write(b"-1 0 0 0\n");
    
    if flashDelay != 0:
        time.sleep(flashDelay)
        for i in range(0, LEDlength):
            fo.write(b"%d %d %d %d\n" % (i, 0, 0, 0))
        fo.write(b"-1 0 0 0\n");
        time.sleep(flashDelay)
    
# Close opened file
fo.close()
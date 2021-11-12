#!/usr/bin/python3
import time
import math
import Adafruit_BBIO.GPIO as GPIO

colorButton = "P8_15"
GPIO.setup(colorButton, GPIO.IN) 
LEDlength = 60
r=1
g=1
b=1
current = -1;
amp = 12
f = 5
shift = 3
phase = 0

colors = [[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1], [1,1,1], [0,0,0]]
print(type(colors))
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

GPIO.add_event_detect(colorButton, GPIO.FALLING, callback=changeColor)

for i in range(0, LEDlength):
    fo.write(b"%d %d %d %d\n" % (i, r, g, b))
fo.write(b"-1 0 0 0\n");    # Send colors to LEDs

while True:
    while current==length-1:
            for i in range(0, LEDlength):
                r = (amp * (math.sin(2*math.pi*f*(i-phase-0*shift)/LEDlength) + 1)) + 1;
                g = (amp * (math.sin(2*math.pi*f*(i-phase-1*shift)/LEDlength) + 1)) + 1;
                b = (amp * (math.sin(2*math.pi*f*(i-phase-2*shift)/LEDlength) + 1)) + 1;
                fo.write(b"%d %d %d %d\n" % (i, r, g, b))
                # print("0 0 127 %d" % (i))
            fo.write(b"-1 0 0 0\n");
            phase = phase + 1
            time.sleep(0.05)

# Close opened file
fo.close()
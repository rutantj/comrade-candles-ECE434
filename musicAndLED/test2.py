#!/usr/bin/python3
import time
import math
import Adafruit_BBIO.GPIO as GPIO
import sys
import os

#GPIO Button Setup
colorButton = "P8_8"
flashButton = "P8_9"
pauseAndPlayButton = "P8_10"
skipButton = "P8_15"
GPIO.setup(colorButton, GPIO.IN)
GPIO.setup(flashButton, GPIO.IN)
GPIO.setup(pauseAndPlayButton, GPIO.IN)
GPIO.setup(skipButton, GPIO.IN)

audiofiles = ['DLF11.mp3', 'Leave The Broom Where It Is.mp3', 'Take A Breath.mp3', 'DLF4.mp3' 'Put On Your Shades.mp3', 'You Should Go.mp3']
musicIndex = 0

LEDlength = 60
print(sys.argv)
r=int(sys.argv[1])
g=int(sys.argv[2])
b=int(sys.argv[3])
current = 0
amp = 12
f = 5
shift = 3
phase = 0 
currFlash = 0
flashSpeeds = [float(sys.argv[4]),0, 0.1, 0.25, 0.5, 1]
flashLength = len(flashSpeeds)
flashDelay = float(sys.argv[4])

colors = [[int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])],[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1], [1,1,1], [0,0,0]]
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
    time.sleep(0.05) #debounce delay
    for i in range(0, LEDlength):
        fo.write(b"%d %d %d %d\n" % (i, r, g, b))
    fo.write(b"-1 0 0 0\n");    # Send colors to LEDs
    os.system("wget --spider --server-response vandensp.pagekite.me/"+str(r)+"/"+str(g)+"/"+str(b)+"/"+str(flashDelay)+"/"+str(musicIndex)+"/te")

def changeFlash(flashButton):
    global currFlash
    global flashLength
    global flashDelay
    currFlash += 1
    currFlash %= flashLength
    flashDelay = flashSpeeds[currFlash]
    print("FlashDelay: ", flashDelay)
    os.system("wget --spider --server-response vandensp.pagekite.me/"+str(r)+"/"+str(g)+"/"+str(b)+"/"+str(flashDelay)+"/"+str(musicIndex)+"/t")

def pauseOrPlay(pauseAndPlayButton):
    #os.system("python pagekite.py 8081 vandensp.pagekite.me")
    time.sleep(0.05)

def skipSong(skipButton):
    global musicIndex
    musicIndex += 1
    os.system("wget --spider --server-response vandensp.pagekite.me/"+str(r)+"/"+str(g)+"/"+str(b)+"/"+str(flashDelay)+"/"+str(musicIndex)+"/false")
    time.sleep(0.05)
    
	
GPIO.add_event_detect(pauseAndPlayButton, GPIO.FALLING, callback=pauseOrPlay)
GPIO.add_event_detect(skipButton, GPIO.FALLING, callback=skipSong)	
GPIO.add_event_detect(colorButton, GPIO.FALLING, callback=changeColor)
GPIO.add_event_detect(flashButton, GPIO.FALLING, callback=changeFlash)

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
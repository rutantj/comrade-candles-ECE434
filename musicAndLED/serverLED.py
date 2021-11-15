#!/usr/bin/python3
import time
import math
import Adafruit_BBIO.GPIO as GPIO
from flask import Flask, render_template, request
import os

#GPIO Setup
pauseAndPlayButton = "P8_10"
skipButton = "P8_15"
GPIO.setup(pauseAndPlayButton, GPIO.IN)
GPIO.setup(skipButton, GPIO.IN)
pauseAndPlayButtonVal = False
skipButtonVal = False

#online stuff ##################################################################################################

app = Flask(__name__)
@app.route("/")
def index():
	templateData = {
              'title' : 'Comrade Candle control!',
        }
	return render_template('remoteVirtual.html', **templateData)
	
@app.route("/<red>/<green>/<blue>/<flash>")
def action(red, green, blue, flash):
	#   Send same url with browserAction changed to "no" to other bone.
	os.system("pkill -9 -f ./test.py")
	os.system("pkill -f mplayer")
	os.system("./test.py "+red+" "+green+" "+blue+" "+flash+" &")
	os.system("mplayer -ao alsa:device=sysdefault=AT2020USB ../mp3folder/'Leave The Broom Where It Is.mp3'")
	templateData={
	}
	return render_template('remoteVirtual.html', **templateData)
	
def pauseOrPlay(pauseAndPlayButton):
	pauseAndPlayButtonVal = True

def skipSong(skipButton):
	skipButtonVal = true
    
#GPIO.add_event_detect(pauseAndPlayButton, GPIO.FALLING, callback=pauseOrPlay)
#GPIO.add_event_detect(skipButton, GPIO.FALLING, callback=skipSong)	
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8081, debug=True)
#end of online stuff ##################################################################################################

while(1):
	if (pauseAndPlayButtonVal):
		print("ppDetected")
		pauseAndPlayButtonVal = False
		time.sleep(0.5) #debounce delay
		
	if (skipButtonVal):
		print("skip button detected")
		skipButtonVal = False
		time.sleep(0.5)

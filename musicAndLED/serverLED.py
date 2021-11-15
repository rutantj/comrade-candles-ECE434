#!/usr/bin/python3
import time
import math
import Adafruit_BBIO.GPIO as GPIO
from flask import Flask, render_template, request
import os

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
	
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8081, debug=True)
#end of online stuff ##################################################################################################
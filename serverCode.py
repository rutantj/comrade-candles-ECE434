#!/usr/bin/env python3
# From: https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
'''
	Raspberry Pi GPIO Status and Control
'''
#Import PyBBIO library:
import Adafruit_BBIO.GPIO as GPIO
from flask import Flask, render_template, request
# Write an 8x8 Red/Green LED matrix
# https://www.adafruit.com/product/902
import smbus
import time

# matrix setup
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

delay = 1; # Delay between images in s

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
board = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]
#clear board
bus.write_i2c_block_data(matrix, 0, board)
#set cursor position
pos = [0,0]
maxY = 8
maxX = 8
maxX -= 1
maxY -= 1

list = [0,1,2,3]
ledRedSts = 2

#online stuff
app = Flask(__name__)
@app.route("/")
def index():
	templateData = {
              'title' : 'GPIO output Status!',
        }
	return render_template('remoteVirtual.html', **templateData)
	
@app.route("/<action>/<green>/<blue>/")
def action(action, green, blue):
	if ((action == "left") & (pos[0]>0)):
		pos[0]-=1
	elif ((action == "up") & (pos[1]>0)):
		pos[1]-=1
	elif ((action == "right") & (pos[0]<maxX)):
		pos[0]+=1
	elif ((action == "down") & (pos[1]<maxY)):
		pos[1]+=1
	elif ((action == "clear")):
		for i in range(15):
			board[i] = 0
	board[2*pos[0]] = board[2*pos[0]] | (1<<pos[1])
	bus.write_i2c_block_data(matrix, 0, board)
	
	templateData = {
	}
	return render_template('remoteVirtual.html', **templateData)
	

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)

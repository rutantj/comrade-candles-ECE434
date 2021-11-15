#!/usr/bin/env python3
import Adafruit_BBIO.UART as UART
import time
import serial
import smbus
import gpiod
import sys

UART.setup("UART1")
CONSUMER='getset'
CHIP='1'
chip = gpiod.Chip(CHIP)
getoffsets=[17]

getlines = chip.get_lines(getoffsets)
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

ser = serial.Serial(port = "/dev/ttyO1", baudrate=19200)
ser.close()
ser.open()
while ser.isOpen():
    #print(".")
    #for i in range(0,15):
    ser_data = ser.read(1)
    print(ord(ser_data))
        #data_array[i] = ser_data
        
        #if(i == 15):
        #    dataCheck = hammingWeight(data_array)
    
#while ser.isOpen():
    
    #ev_lines = getlines.event_wait(sec=1)
    #if ev_lines:
    #    for line in ev_lines:
    #        event = line.event_read()
    #        event_handle(event)
    

#def event_handle(event):
#    print(ser.read())
#    ser.flush()
  
    
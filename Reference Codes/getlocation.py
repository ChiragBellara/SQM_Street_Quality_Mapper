from datetime import datetime
import serial
import time
import string
import re
import os
from pynmea import nmea
import RPi.GPIO as gpio

#providing sudo permissions to the serial port
os.system("sudo chmod 777 /dev/ttyAMA0")

port = "/dev/ttyAMA0"# the serial port to which the pi is connected.

#function to get the location
def getloc():
    #create a serial object
    
    ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    
    while True:
        data = ser.readline().decode('utf-8')
        if data[0:6] == '$GPGGA':  #reading the GPGGA part of the NMEA sentence
            lat, long, timestamp = data_l(data)
            return(lat, long, timestamp) 
        
def data_l(data):
    msg = nmea.GPGGA()
    msg.parse(data)
    timestamp = str(datetime.now())
    latval = str(float(msg.latitude)/100) if re.search('[0-9]+\.[0-9]+',msg.latitude)!=None else ""
    longval = str(float(msg.longitude)/100) if re.search('[0-9]+\.[0-9]+',msg.longitude)!=None else ""

    return(latval,longval, timestamp)

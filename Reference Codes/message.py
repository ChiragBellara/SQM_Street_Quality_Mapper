import RPi.GPIO as GPIO
import serial
import time,sys

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)


ser.write("AT+CMGF = 1\r")
print("Text mode enabled.")
time.sleep(3)
ser.write('AT+CMGS="8879354575"\r')
message = "Gaurav Sahu Zindabad"
print("Sending Message")
time.sleep(3)
ser.write(message+chr(26))
time.sleep(3)
print("Message sent")

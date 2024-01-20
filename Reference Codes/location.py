import RPi.GPIO as GPIO
import serial
import time,sys

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
'''
print(ser.write("AT\r"))
recv = ser.read(10)
print(recv)
print("AT Okay")

print(ser.write(b'AT+SAPBR=3,1,"Contype","GPRS"\r'))
recv = ser.read(10)
print(recv)
print("Location 1")

print(ser.write('AT+SAPBR=3,1,"APN","imis/internet"\r'))
recv = ser.read(10)
print(recv)
print("Location 2")

print(ser.write("AT+SAPBR=1,1\r"))
recv = ser.read(10)
print(recv)
print("Location 2")

print(ser.write("AT+SAPBR=2,1\r"))
recv = ser.read(10)
print(recv)
'''
print(ser.write("AT+CIPGSMLOC=1,1\r"))
recv = ser.read(10)
print(recv)

answer = sendATcommand("AT+CGPS=1,2","OK",1000)
print(answer)
print(sendATcommand("AT+CGPSINFO","+CGPSINFO:",1000))

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.framerate = 20
camera.start_preview()
camera.start_recording('/home/pi/video1.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview()

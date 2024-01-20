from picamera import PiCamera,Color
import time
from time import sleep

camera = PiCamera()
camera.start_preview()
#camera.image_effect = 'sketch'
#camera.annotate_text = " Hello world "
#camera.awb_mode = 'sunlight'
sleep(5)
end_time = time.time()
camera.capture('/home/pi/Desktop/sunlight.jpg')
start_time = time.time()
#camera.exposure_mode = 'beach'
sleep(5)
camera.capture('/home/pi/Desktop/beach.jpg')
print(start_time - end_time)
camera.stop_preview()
camera.close

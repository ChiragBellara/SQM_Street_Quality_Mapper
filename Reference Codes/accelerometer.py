import smbus
from time import sleep, strftime, time
from mpu6050 import mpu6050
import math
import atexit
from os import path
from json import dumps, loads

sensor1 = mpu6050(0x68)
sensor2 = mpu6050(0x69)
count=0


#Automated Counting here
def read_counter():
    return loads(open("counter.json", "r").read()) + 1 if path.exists("counter.json") else 0

def write_counter():
    with open("counter.json", "w") as f:
        f.write(dumps(counter))
        
#note if you want to delete counter i.e to start with 0 again delete counter.json and all the files produced

counter = read_counter()          #counter for file
atexit.register(write_counter)    #storing records


with open("/home/pi/Reference Codes/(automated)Accelerometer-Data-{}.csv".format(counter), "a") as log:
    while count<=300:        
        accelerometer_data1 = sensor1.get_accel_data()
        accelerometer_data2 = sensor2.get_accel_data()
        (avg_x, avg_y, avg_z)=((accelerometer_data1['x']+(accelerometer_data2['x'])/2), ((accelerometer_data1['y']+accelerometer_data2['y'])/2), ((accelerometer_data1['z']+accelerometer_data2['z'])/2))
        print(str(avg_x)+'\t'+str(avg_y)+'\t'+str(avg_z))
        log.write(str(avg_x)+','+str(avg_y)+','+str(avg_z)+'\n')
        #accelerometer_z=accelerometer_data['z']
        #gyro_data = sensor.get_gyro_data()
        count += 1
       # print(str(accelerometer_data) + "\t\t\t" + str(gyro_data))
    log.close()


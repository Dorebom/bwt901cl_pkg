from src.bwt901cl import BWT901CL

import subprocess
import time

subprocess.call("sudo chmod 777 /dev/ttyUSB0", shell=True)

nodes = BWT901CL("/dev/ttyUSB0")


angle, angular_velocity, accel, temp, magnetic = nodes.getData()

while(True):
    print("th:", angle)
    print("d_th: ", angular_velocity)
    print("d_x: ", accel)
    print("mag: ", magnetic)
    print("tmp: ", temp)
    time.sleep(1)


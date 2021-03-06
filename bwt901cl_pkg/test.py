from src.bwt901cl import BWT901CL

nodes = BWT901CL("/dev/ttyUSB0")


angle, angular_velocity, accel, temp, magnetic = nodes.getData()
print("angle: ", angle)
print("angle_v:", angular_velocity)
print("magnetic:", magnetic)
print("temperature: ", temp)



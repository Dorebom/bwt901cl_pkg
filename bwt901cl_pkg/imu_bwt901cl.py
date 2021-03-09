import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Temperature, MagneticField
from geometry_msgs.msg import Vector3
import subprocess

from .src.bwt901cl import BWT901CL

class Imu901cl(Node):
    def __init__(self, time_interval=1.0):
        super().__init__('imu_bwt901cl')
        self.pub_imu = self.create_publisher(Imu, '/sensor/bwt901cl/Imu', 10)
        self.pub_mag = self.create_publisher(MagneticField, '/sensor/bwt901cl/MagneticField', 10)
        self.pub_tmp = self.create_publisher(Temperature, '/sensor/bwt901cl/Temperature', 10)
        self.pub_ang = self.create_publisher(Vector3, '/sensor/bwt901cl/Angle', 10)
        self.tmr = self.create_timer(time_interval, self.timer_callback)
        subprocess.call("sudo chmod 777 /dev/ttyUSB0", shell=True)
        self.imu_sensor =  BWT901CL("/dev/ttyUSB0")

    def timer_callback(self):
        msg_imu = Imu()
        msg_mag = MagneticField()
        msg_tmp = Temperature()
        msg_ang = Vector3()

        angle, angular_velocity, accel, temp, magnetic, quaternion, time = self.imu_sensor.getData()

        msg_tmp.temperature = temp
        self.pub_tmp.publish(msg_tmp)

        msg_mag.magnetic_field.x = float(magnetic[0])
        msg_mag.magnetic_field.y = float(magnetic[1])
        msg_mag.magnetic_field.z = float(magnetic[2])
        self.pub_mag.publish(msg_mag)

        msg_imu.orientation.x = quaternion[0]
        msg_imu.orientation.y = quaternion[1]
        msg_imu.orientation.z = quaternion[2]
        msg_imu.orientation.w = quaternion[3]
        msg_imu.angular_velocity.x = angular_velocity[0]
        msg_imu.angular_velocity.y = angular_velocity[1]
        msg_imu.angular_velocity.z = angular_velocity[2]
        msg_imu.linear_acceleration.x = accel[0]
        msg_imu.linear_acceleration.y = accel[1]
        msg_imu.linear_acceleration.z = accel[2]
        self.pub_imu.publish(msg_imu)

        msg_ang.x = angle[0]
        msg_ang.y = angle[1]
        msg_ang.z = angle[2]
        self.pub_ang.publish(msg_ang)

        #print("Time:", time)
        #print("th:", angle)
        #print("d_th: ", angular_velocity)
        #print("d_x: ", accel)
        #print("mag: ", magnetic)
        #print("tmp: ", temp)
        #print(quaternion)

def main(args=None):    
    print('Hi from bwt901cl_pkg.')

    rclpy.init(args=args)
    node_imu_bwt901cl = Imu901cl(time_interval=0.1)
    rclpy.spin(node_imu_bwt901cl)

    node_imu_bwt901cl.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

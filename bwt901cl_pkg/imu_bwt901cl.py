import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Temperature, MagneticField

from src.bwt901cl import BWT901CL

class Imu901cl(Node):
    def __init__(self):
        super().__init__('imu_bwt901cl')
        self.pub_imu = self.create_publisher(Imu, '/sensor/bwt901cl/imu', 10)
        self.pub_mag = self.create_publisher(MagneticField, '/sensor/bwt901cl/MagneticField', 10)
        self.pub_tmp = self.create_publisher(Temperature, '/sensor/bwt901cl/Temperature', 10)
        self.tmr = self.create_timer(1.0, self.timer_callback)
        self.imu_sensor =  BWT901CL("/dev/ttyUSB0")

    def timer_callback(self):
        msg_imu = Imu
        msg_mag = MagneticField
        msg_tmp = Temperature

        angle, angular_velocity, accel, temp, magnetic = self.imu_sensor.getData()
        msg_imu.angular_velocity = angular_velocity
        print(angle) 

def main(args=None):    
    print('Hi from bwt901cl_pkg.')

    rclpy.init(args=args)
    node_imu_bwt901cl = Imu901cl()
    rclpy.spin(node_imu_bwt901cl)

    node_imu_bwt901cl.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

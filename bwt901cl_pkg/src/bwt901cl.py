from serial import Serial
from time import sleep

class BWT901CL(Serial):
    def __init__(self, Port):
        self.myserial = super().__init__(Port, baudrate = 115200, timeout = 1)

        self.angular_velocity_x = 0.0
        self.angular_velocity_y = 0.0
        self.angular_velocity_z = 0.0
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0
        self.Temp = 0.0
        self.magnetic_x = 0.0
        self.magnetic_y = 0.0
        self.magnetic_z = 0.0
        self.quaternion_x = 0.0
        self.quaternion_y = 0.0
        self.quaternion_z = 0.0
        self.quaternion_w = 1.0
        self.YY = 0
        self.MM = 0
        self.DD = 0
        self.hh = 0
        self.mm = 0
        self.ss = 0
        self.ms = 0
        self.D0 = 0
        self.D1 = 0
        self.D2 = 0
        self.D3 = 0

        while True:
            data = super(BWT901CL, self).read(size=1)
            if data == b'\x55':
                data = super(BWT901CL, self).read(size=10)
                print("success!")
                print(bytes(data))
                break
            print("trying", data)
        #print(super(BWT901CL, self).isOpen())
        self._readData()

    def _readData(self):
        try:
            for i in range(6):
                data = super(BWT901CL, self).read(size=11)

                if not len(data) == 11:
                    print('byte error:', len(data))
                    break
                if not data[0] == 0x55:
                    print('UART sync error:', bytes(data))
                    break
               #Time
                if data[1] == 0x50:
                    self.YY = data[2]
                    self.MM = data[3]
                    self.DD = data[4]
                    self.hh = data[5]
                    self.mm = data[6]
                    self.ss = data[7]
                    self.ms = int.from_bytes(data[8:10], byteorder='little')

                #Acceleration
                elif data[1] == 0x51:
                    self.accel_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768.0*16.0*9.8
                    self.accel_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768.0*16.0*9.8
                    self.accel_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768.0*16.0*9.8
                    self.Temp = int.from_bytes(data[8:10], byteorder='little', signed=True)/340.0+36.25

                #Angular velocity
                elif data[1] == 0x52:
                    self.angular_velocity_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768*2000.0
                    self.angular_velocity_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768*2000.0
                    self.angular_velocity_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768*2000.0
                    self.Temp = int.from_bytes(data[8:10], byteorder='little')/340.0+36.25

                #Angle
                elif data[1] == 0x53:
                    self.angle_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768*180
                    self.angle_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768*180
                    self.angle_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768*180

                #Magnetic
                elif data[1] == 0x54:
                    self.magnetic_x = int.from_bytes(data[2:4], byteorder='little', signed=True)
                    self.magnetic_y = int.from_bytes(data[4:6], byteorder='little', signed=True)
                    self.magnetic_z = int.from_bytes(data[6:8], byteorder='little', signed=True)

                #Quatrernion
                elif data[1] == 0x59:
                    self.quaternion_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768
                    self.quaternion_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768
                    self.quaternion_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768
                    self.quaternion_w = int.from_bytes(data[8:10], byteorder='little', signed=True)/32768

                #Data output port status
                elif data[1] == 0x55:
                    self.D0 = int.from_bytes(data[2:4], byteorder='little',signed=True)
                    self.D1 = int.from_bytes(data[4:6], byteorder='little',signed=True)
                    self.D2 = int.from_bytes(data[6:8], byteorder='little',signed=True)
                    self.D3 = int.from_bytes(data[8:10], byteorder='little',signed=True)

        except KeyboardInterrupt:
            super(BWT901CL, self).close()

    def getAngle(self):
        self._readData()
        return (self.angle_x, self.angle_y, self.angle_z)

    def getAnglurVelocity(self):
        self._readData()
        return (self.angular_velocity_x, self.angular_velocity_y, self.angular_velocity_z)

    def getAccel(self):
        self._readData()
        return (self.accel_x, self.accel_y, self.accel_z)

    def getTemperature(self):
        return self.Temp

    def getData(self):
        super(BWT901CL, self).reset_input_buffer()
        is_not_sync = True
        while is_not_sync:
            data = super(BWT901CL, self).read(size=1)
            if data == b'\x55':
                data = super(BWT901CL, self).read(size=10)
                is_not_sync = False
                break

        self._readData()
        return  (self.angle_x, self.angle_y, self.angle_z), \
                (self.angular_velocity_x, self.angular_velocity_y, self.angular_velocity_z), \
                (self.accel_x, self.accel_y, self.accel_z), \
                self.Temp, \
                (self.magnetic_x, self.magnetic_y, self.magnetic_z), \
                (self.quaternion_x, self.quaternion_y, self.quaternion_z, self.quaternion_w), \
                (self.MM, self.DD, self.hh, self.mm, self.ss, self.ms)

if __name__ == "__main__":

    jy_sensor =  BWT901CL("/dev/ttyUSB0")
    #sleep(1)
    #jy_sensor.wake_up()
    while True:
        #print('Angle: ', jy_sensor.getAngle())
        #print('Anglular velocity: ', jy_sensor.getAnglurVelocity())
        sleep(0.5)
        jy_sensor.getData()
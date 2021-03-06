from serial import Serial

class BWT901CL(Serial):
    def __init__(self, Port):
        self.myserial = super().__init__(Port, baudrate = 115200, timeout = 1)
        while True:
            data = super(BWT901CL, self).read(size=1)
            if data == b'\x55':
                print("success!")
                super(BWT901CL, self).read(size=10)
                break
            print("trying", data)

    def _readData(self):
        try:
            for i in range(6):
                data = super(BWT901CL, self).read(size=11)

                if not len(data) == 11:
                    print('byte error:', len(data))

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
                if data[1] == 0x51:
                    self.accel_x = int.from_bytes(data[2:4], byteorder='little')/32768.0*16
                    self.accel_y = int.from_bytes(data[4:6], byteorder='little')/32768.0*16
                    self.accel_z = int.from_bytes(data[6:8], byteorder='little')/32768.0*16
                    self.Temp = int.from_bytes(data[8:10], byteorder='little')/340.0+36.25

                #Angular velocity
                elif data[1] == 0x52:
                    self.angular_velocity_x = int.from_bytes(data[2:4], byteorder='little')/32768*2000
                    self.angular_velocity_y = int.from_bytes(data[4:6], byteorder='little')/32768*2000
                    self.angular_velocity_z = int.from_bytes(data[6:8], byteorder='little')/32768*2000
                    self.Temp = int.from_bytes(data[8:10], byteorder='little')/340.0+36.25

                #Angle
                elif data[1] == 0x53:
                    self.angle_x = int.from_bytes(data[2:4], byteorder='little')/32768*180
                    self.angle_y = int.from_bytes(data[4:6], byteorder='little')/32768*180
                    self.angle_z = int.from_bytes(data[6:8], byteorder='little')/32768*180

                #Magnetic
                elif data[1] == 0x54:
                    self.magnetic_x = int.from_bytes(data[2:4], byteorder='little')
                    self.magnetic_y = int.from_bytes(data[4:6], byteorder='little')
                    self.magnetic_z = int.from_bytes(data[6:8], byteorder='little')

                #Data output port status
                elif data[1] == 0x55:
                    self.D0 = int.from_bytes(data[2:4], byteorder='little')
                    self.D1 = int.from_bytes(data[4:6], byteorder='little')
                    self.D2 = int.from_bytes(data[6:8], byteorder='little')
                    self.D3 = int.from_bytes(data[8:10], byteorder='little')

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
        self._readData()
        return (self.angle_x, self.angle_y, self.angle_z), \
               (self.angular_velocity_x, self.angular_velocity_y, self.angular_velocity_z), \
               (self.accel_x, self.accel_y, self.accel_z), \
               self.Temp, \
               (self.magnetic_x, self.magnetic_y, self.magnetic_z)


if __name__ == "__main__":

    jy_sensor =  BWT901CL("/dev/ttyUSB0")
    while True:
        print('Angle: ', jy_sensor.getAngle())
        print('Anglular velocity: ', jy_sensor.getAnglurVelocity())
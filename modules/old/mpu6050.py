# dummy for errorchecking reason outside of py
# DON'T COPY TO PY
class dummyData:
    def __init__(self):
        self.x = 1.256
        self.y = 2.789
        self.z = 3.556

class mpu6050:

    ACCEL_SCALE_MODIFIER_4G = 8192.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    ACCEL_RANGE_4G = 0x08
    GYRO_RANGE_500DEG = 0x08


    def __init__(self, id):
        self.id = id

    def get_accel_data(self):
        return dummyData()

    def get_gyro_data(self):
        return dummyData()

    def get_temp(self):
        return 26

    def set_accel_range(self, accel_range):
        return

    def set_gyro_range(self, gyro_range):
        return
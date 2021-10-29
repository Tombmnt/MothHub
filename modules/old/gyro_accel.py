#apt install python3-smbus
#pip install mpu6050_raspberrypi

from mpu6050 import mpu6050
import timeUtil, printHelper

class DataAccel:
    def __init__(self, time, date, x, y, z):
        self.time = time #UTC en nmea
        self.date = date
        self.x = x
        self.y = y
        self.z = z

class DataGyro:
    def __init__(self, time, date, pitch, yaw, roll):
        self.time = time #UTC en nmea
        self.date = date
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

class DataTemperature:
    def __init__(self, time, date, temp):
        self.time = time
        self.date = date
        self.temp = temp

class GyroAccel:
    def __init__(self):
        self.accelero = mpu6050(0x68)
        self.accelero.set_accel_range(mpu6050.ACCEL_RANGE_4G)
        self.accelero.set_gyro_range(mpu6050.GYRO_RANGE_500DEG)

        self.calibration = self.calibrate()

    def calibrate(self, threshold=50, n_samples=100):
        """
        Get calibration date for the sensor, by repeatedly measuring
        while the sensor is stable. The resulting calibration
        dictionary contains offsets for this sensor in its
        current position.
        """
        printHelper.infoMPU6050("calibrating, the device must be level and stable.")
        while True:
            v1 = self.getRawAccelData(True, n_samples)
            v2 = self.getRawAccelData(True, n_samples)
            # Check all consecutive measurements are within
            # the threshold. We use abs() so all calculated 
            # differences are positive.
            if all(abs(v1[key] - v2[key]) < threshold for key in v1.keys()):
                printHelper.infoMPU6050("calibrated.")
                return v1  # Calibrated.

    def getRawAccelData(self, calib=False, n_samples=10):
        data = {}

        for s in range(n_samples):
            accel_data = self.accelero.get_accel_data()

            for i in range({"x", "y", "z"}):
                data[i] += accel_data[i]

        for key in data.keys():
            data[key] /= n_samples
            if not calib:
                data[key] -= self.calibration[key]

        return data

    def getAccelData(self):
        accel_data = self.getRawAccelData()
        angVelX = (accel_data["x"] / mpu6050.ACCEL_SCALE_MODIFIER_4G) #TODO: needs math formula
        angVelY = (accel_data["y"] / mpu6050.ACCEL_SCALE_MODIFIER_4G) #idem
        angVelZ = (accel_data["z"] / mpu6050.ACCEL_SCALE_MODIFIER_4G) #idem 2
        #angX = 
        #angY = 
        #angZ =        
        return DataAccel(timeUtil.getTimeNowAsNMEA(), timeUtil.getDateNowAsNMEA(), angVelX, angVelY, angVelZ)
    
    def getGyroData(self):
        gyro_data = self.accelero.get_gyro_data()
        angVelX = (gyro_data.x / mpu6050.GYRO_SCALE_MODIFIER_500DEG) #TODO: needs math formula
        angVelY = (gyro_data.y / mpu6050.GYRO_SCALE_MODIFIER_500DEG) #idem
        angVelZ = (gyro_data.z / mpu6050.GYRO_SCALE_MODIFIER_500DEG) #idem 2
        #angX = 
        #angY = 
        #angZ = 
        return DataGyro(timeUtil.getTimeNowAsNMEA(), timeUtil.getDateNowAsNMEA(), angVelX, angVelY, angVelZ)

    def getTemperatureData(self):
        temp = self.accelero.get_temp()
        return DataTemperature(timeUtil.getTimeNowAsNMEA(), timeUtil.getDateNowAsNMEA(), temp)


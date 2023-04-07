import threading

from rcpy import mpu9250
from time import sleep

# imu = mpu9250.IMU(enable_dmp=True,
#                   dmp_sample_rate=4,
#                   enable_magnetometer=True,
#                   enable_fusion=True)

# mpu9250.read_accel_data()
# mpu9250.read_gyro_data()
# mpu9250.read_mag_data()

"""
accel: 3-axis accelerations (m/s 2)
gyro: 3-axis angular velocities (degree/s)
mag: 3D magnetic field vector in (μT)
quat: orientation quaternion
tb: pitch/roll/yaw X/Y/Z angles (radians)
head: heading from magnetometer (radians)
"""

# while True:
#     data = imu.read()
#     sleep(0.00001)
#     data['gyro'] = mpu9250.read_gyro_data()
#     data['accel'] = mpu9250.read_accel_data()
#     data['mag'] = mpu9250.read_mag_data()
#     print(data)


class IMUThread(threading.Thread):
    def __init__(self):
        self.imu = mpu9250.IMU(enable_dmp=True,
                          dmp_sample_rate=4,
                          enable_magnetometer=True,
                          enable_fusion=True)
        self._stop = False

    def start(self):
        while True:
            data = self.imu.read()
            sleep(0.00001)
            data['gyro'] = mpu9250.read_gyro_data()
            data['accel'] = mpu9250.read_accel_data()
            data['mag'] = mpu9250.read_mag_data()
            print(data)
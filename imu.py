from rcpy import mpu9250
from time import sleep
import warnings

warnings.filterwarnings('ignore')

"""
accel: 3-axis accelerations (m/s 2)
gyro: 3-axis angular velocities (degree/s)
mag: 3D magnetic field vector in (μT)
quat: orientation quaternion
tb: pitch/roll/yaw X/Y/Z angles (radians)
head: heading from magnetometer (radians)
"""


class IMUT:
    def __init__(self, stop_flag):
        super().__init__(stop_flag)
        self.imu = mpu9250.IMU(enable_dmp=True,
                               dmp_sample_rate=4,
                               enable_magnetometer=True,
                               enable_fusion=True)

    def run(self):
        while True:
            data = self.imu.read()
            sleep(0.0001)
            data['gyro'] = mpu9250.read_gyro_data()
            data['accel'] = mpu9250.read_accel_data()
            data['mag'] = mpu9250.read_mag_data()
            #print(data)


def main():
    imu= IMU()
    imu.run()


if __name__ == "__main__":
    main()
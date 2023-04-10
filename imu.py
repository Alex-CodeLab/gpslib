from rcpy import mpu9250
from time import sleep
from config import TTY, BAUDRATE, IPADDRESS
import json
import warnings
import zmq

warnings.filterwarnings('ignore')

"""
accel: 3-axis accelerations (m/s 2)
gyro: 3-axis angular velocities (degree/s)
mag: 3D magnetic field vector in (μT)
quat: orientation quaternion
tb: pitch/roll/yaw X/Y/Z angles (radians)
head: heading from magnetometer (radians)
"""


class IMU:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect(f"tcp://{IPADDRESS}")
        self._imu = mpu9250.IMU(enable_dmp=True,
                               dmp_sample_rate=4,
                               enable_magnetometer=True,
                               enable_fusion=True)

    def run(self):
        while True:
            data = self._imu.read()
            sleep(0.001)
            data['gyro'] = mpu9250.read_gyro_data()
            data['accel'] = mpu9250.read_accel_data()
            data['mag'] = mpu9250.read_mag_data()
            self.socket.send_multipart([b'', json.dumps(data).encode('utf-8')])


def main():
    imu= IMU()
    imu.run()


if __name__ == "__main__":
    main()
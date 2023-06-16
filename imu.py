#!/home/debain/gpslib/env/bin/python
import json
import os
import sys
import warnings
from time import sleep
import zmq
warnings.filterwarnings("ignore")
from rcpy import mpu9250
from config import IPADDRESS, PORT


"""
    accel: 3-axis accelerations (m/s 2)
    gyro: 3-axis angular velocities (degree/s)
    mag: 3D magnetic field vector in (μT)
    quat: orientation quaternion
    tb: pitch/roll/yaw X/Y/Z angles (radians)
    head: heading from magnetometer (radians)
"""


class IMU:
    """
    Represents an Inertial Measurement Unit (IMU) object that reads data from an MPU9250 sensor and publishes it over a ZeroMQ socket.

    Attributes:
        socket (zmq.Socket): ZeroMQ socket for publishing IMU data.

    """
    def __init__(self):
        """ Initializes the IMU object by setting up the ZeroMQ socket and MPU9250 sensor.
        """
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect(f"tcp://{IPADDRESS}:{PORT}")
        try:
            self._imu = mpu9250.IMU(enable_dmp=True,
                                    dmp_sample_rate=4,
                                    enable_magnetometer=True,
                                    enable_fusion=True)
        except Exception as e:
            print('check calibration', e)
            exit()

    def run(self):
        """
        Continuously reads data from the MPU9250 sensor and publishes it over the ZeroMQ socket.

        This method runs an infinite loop that reads data from the MPU9250 sensor. The sensor data, including gyroscope,
        accelerometer, and magnetometer readings, is published over the ZeroMQ socket as a JSON-encoded message.
        """
        while True:
            try:
                data = self._imu.read()
            except KeyboardInterrupt:
                try:
                    sys.exit(130)
                except SystemExit:
                    os._exit(130)

            sleep(0.01)
            data['gyro'] = mpu9250.read_gyro_data()
            data['accel'] = mpu9250.read_accel_data()
            data['mag'] = mpu9250.read_mag_data()
            self.socket.send_multipart([b'', json.dumps(data).encode('utf-8')])


def main():
    imu = IMU()
    imu.run()


if __name__ == "__main__":
    main()

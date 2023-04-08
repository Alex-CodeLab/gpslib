import signal
import threading
from time import sleep

from gps import GPSThread
from imu import IMUThread
from zeromq import ZMQThread
import queue


class SignalHandler:
    def __init__(self):
        self.flag = False

    def __call__(self, sig, frame):
        self.flag = True


def main():
    # handle termination
    stop_flag = threading.Event()
    handler = SignalHandler()
    signal.signal(signal.SIGINT, handler)
    stop_flag.handler = handler

    # initialize threads
    gps_thread = GPSThread(queue=queue.Queue(), stop_flag=stop_flag)
    imu_thread = IMUThread(stop_flag)
    zmq_thread = ZMQThread(stop_flag)

    gps_thread.start()
    imu_thread.start()
    zmq_thread.start()

    while not stop_flag.is_set() and not handler.flag:
        sleep(1)

    stop_flag.set()

    gps_thread.join()
    imu_thread.join()
    zmq_thread.join()


if __name__ == "__main__":
    main()

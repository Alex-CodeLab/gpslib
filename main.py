from gps import GPSThread
import threading
# from multiprocessing import Queue, Process
import queue


class Program:
    def __init__(self):
        # Create the queue and the threads
        self.queue = queue.Queue()
        self.gps_thread = GPSThread(self.queue)
        # self.imu_thread = IMUThread(self.queue)
        self.input_thread.daemon = True
        # self.imu_thread.daemon = True


    def start(self):
        self.gps_thread.start()
        # self.imu_thread.start()
        # self.zmq_thread.start()

        self.gps_thread.join()


def main():
    # Create the program instance and start it
    program = Program()
    program.start()


if __name__ == "__main__":
    main()

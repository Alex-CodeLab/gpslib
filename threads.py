import threading
import signal
import multiprocessing


class Threads(multiprocessing.Process):

    def __init__(self, stop_flag):
        super().__init__()
        self.stop_flag = stop_flag
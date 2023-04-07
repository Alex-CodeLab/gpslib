import threading
import signal


class Threads(threading.Thread):

    def __init__(self, stop_flag):
        super().__init__()
        self.stop_flag = stop_flag
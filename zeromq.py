import zmq
from config import IPADDRESS
import queue
import time

from threads import Threads


class ZMQThread(Threads):

    def __init__(self, q):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://{IPADDRESS}")
        self.q = q


    def start(self):
        while True:
            try:
                item = self.q.get(block=False)
                print(f"Got item: {item}")
                self.q.task_done()
            except queue.Empty:
                print("Queue is empty")
                time.sleep(1)
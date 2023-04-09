import zmq
from config import IPADDRESS
import queue as queue_
import time

from threads import Threads


class ZMQThread(Threads):

    def __init__(self, queue, stop_flag):
        super().__init__(stop_flag)
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://{IPADDRESS}")
        self.q = queue


    def run(self):
        while not self.stop_flag.is_set() and not self.stop_flag.handler.flag:
            # try:
                item = self.q.get(block=False)
                print(f"Got item: {item}")
                self.q.task_done()
            # except queue_.Empty:
            #     print("Queue is empty")
            #     time.sleep(1)

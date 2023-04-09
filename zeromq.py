import zmq
from config import IPADDRESS
import asyncio


class ZeroPubSub:

    def __init__(self, publish_address, subscribe_address):
        self.context = zmq.Context()
        self.publish_socket = self.context.socket(zmq.PUB)
        self.publish_socket.bind(publish_address)
        self.subscribe_socket = self.context.socket(zmq.SUB)
        self.subscribe_socket.bind(subscribe_address)
        self.subscribe_socket.setsockopt(zmq.SUBSCRIBE, b"")


    async def start(self):
        while True:
            message = await self.subscribe_socket.recv()
            await self.publish_socket.send(message)


if __name__ == "__main__":
    pubsub = ZeroPubSub("tcp://*:5555", "inproc://messages")
    asyncio.run(pubsub.start())
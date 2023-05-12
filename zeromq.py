#!/home/debain/gpslib/env/bin/python
import zmq
import zmq.asyncio
from config import IPADDRESS
import asyncio
import websockets
from config import TTY, BAUDRATE, IPADDRESS, PORT


async def handler(websocket, path):
    await websocket.send('test reply')


class ZeroPubSub:

    def __init__(self, subscribe_address):
        self.context = zmq.asyncio.Context()
        self.subscribe_socket = self.context.socket(zmq.SUB)
        self.subscribe_socket.bind(subscribe_address)
        self.subscribe_socket.setsockopt(zmq.SUBSCRIBE, b"")

    async def start(self):
        while True:
            message = await self.subscribe_socket.recv()
            print(message)
            await self.websocketserver.send(message)


if __name__ == "__main__":
    pubsub = ZeroPubSub(f"tcp://{IPADDRESS}:{PORT}")
    asyncio.run(pubsub.start())
    start_server = websockets.serve(handler, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

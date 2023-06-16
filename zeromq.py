#!/home/debain/gpslib/env/bin/python
import asyncio

import websockets
import zmq
import zmq.asyncio

from config import IPADDRESS, PORT


async def handler(websocket):
    await websocket.send('test reply')


class ZeroPubSub:

    def __init__(self, subscribe_address):
        self.context = zmq.asyncio.Context()
        self.subscribe_socket = self.context.socket(zmq.SUB)
        self.subscribe_socket.bind(subscribe_address)
        self.subscribe_socket.setsockopt(zmq.SUBSCRIBE, b"")

    async def start(self):
        while True:
            with await self.subscribe_socket.recv() as message:
                print(message)
                # await self.websocketserver.send(message)


if __name__ == "__main__":
    pubsub = ZeroPubSub(f"tcp://{IPADDRESS}:{PORT}")
    asyncio.run(pubsub.start())
    start_server = websockets.serve(handler, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

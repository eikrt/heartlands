import asyncio
import websockets
import json
import pickle
from generator import generator
HOST = 'localhost'
PORT = 5000
def read_world(filename):
    print(f'Loading world from {filename}')
    with open (filename, "rb") as inp:
        world = pickle.load(inp)
    return world
world = read_world('dat/world.dat')


async def map(websocket):
    async for message in websocket:
        data = json.loads(message)
        await websocket.send(json.dumps(world.return_map(int(data['x']),int(data['y']))))

async def main():
    async with websockets.serve(map, HOST,PORT):
        print(f'Running websocket server in host {HOST} port {PORT}')
        await asyncio.Future()  # run forever

asyncio.run(main())


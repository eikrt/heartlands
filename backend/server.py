# server file is responsible for serving world via socket connection

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

# legacy for downloading map by tiles, not chunks
#async def map(websocket):
#    async for message in websocket:
#        data = json.loads(message)
#        await websocket.send(json.dumps(world.return_map(int(data['x']),int(data['y']))))

# load world by chunk

async def map(websocket):
    async for message in websocket:
        data = json.loads(message)
        if data['header'] == 'metadata':
            await websocket.send(json.dumps(world.return_metadata()))
        elif data['header'] == 'chunks':
            await websocket.send(json.dumps(world.return_chunk(int(data['x']),int(data['y']))))
        elif data['header'] == None:
            await websocket.send(json.dumps({'header': 'header invalid or None'}))

async def main():
    async with websockets.serve(map, HOST,PORT):
        print(f'Running websocket server in host {HOST} port {PORT}')
        await asyncio.Future()  # run forever

asyncio.run(main())


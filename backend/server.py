import asyncio
import websockets
import json
from generator import generator
def get_world():
    gen = generator.Generator(256,256)
    gen.generate(100)
    return gen.get_world()

world = get_world()


async def map(websocket):
    async for message in websocket:
        print(message)
        data = json.loads(message)

        await websocket.send(json.dumps(world.return_map(int(data['x']),int(data['y']))))

async def main():
    async with websockets.serve(map, "localhost",5000):
        await asyncio.Future()  # run forever

asyncio.run(main())


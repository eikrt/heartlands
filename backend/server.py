import socketio
import eventlet
from environs import Env
from generator import generator
def get_world():
    gen = generator.Generator(256,256)
    gen.generate(100)
    return gen.get_world()
world = get_world()
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

env = Env()
env.read_env()
@sio.on('map')
def handle(sid, data):
    sio.emit("map", world.return_map(data['x'],data['y']))
def run():
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from environs import Env
from generator import generator
from waitress import serve
def get_world():
    gen = generator.Generator(256,256)
    gen.generate(100)
    return gen.get_world()

env = Env()
env.read_env()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
socketio = SocketIO(app, host='0.0.0.0', cors_allowed_origins="*")
world = get_world()
@app.route('/')
def root():
    return ""
@app.route('/map/<ret_x>/<ret_y>')
def heightmap(ret_x, ret_y):
    return world.return_map(ret_x, ret_y)
@socketio.on('map')
def handle(data):
    emit("map", world.return_map(data['x'],data['y']))
def run():
    #if not env('debug') == 'False':
    #    app.run(host='0.0.0.0', debug=env('debug'),port=env('PORT'))
    #else:
   # serve(app, host='0.0.0.0', port=env('PORT'))
    port = env('PORT')
    print(f'Listening on port: {port}' ) 
    socketio.run(app)

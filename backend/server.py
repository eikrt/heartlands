from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from environs import Env
from generator import generator

def get_world():
    gen = generator.Generator(64,64)
    gen.generate(100)
    return gen.get_world()

env = Env()
env.read_env()
app = Flask(__name__)
CORS(app)
api = Api(app)
world = get_world()
@app.route('/')
def root():
    return ""
@app.route('/map')
def heightmap():
    return world.return_map()

def run():
    app.run(host='0.0.0.0', debug=env('debug'),port=env('PORT'))


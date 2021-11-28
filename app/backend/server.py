from flask import Flask
from flask_restful import Resource, Api, reqparse
from environs import Env
from ..generator import generator

def get_world():
    gen = generator.Generator(64,64)
    gen.generate(100)
    return gen.get_world()

env = Env()
env.read_env()
app = Flask(__name__)
api = Api(app)
world = get_world()
@app.route('/')
def hello():
    return "hello"
@app.route('/map')
def heightmap():
    return world.return_map()

def run():
    app.run(debug=env('debug'),port=env('PORT'))


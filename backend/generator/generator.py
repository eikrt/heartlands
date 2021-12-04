from perlin_noise import PerlinNoise
import random
from scipy.spatial import Voronoi, voronoi_plot_2d

CHUNK_SIZE = 16
BIOMES = [
         

            {'name': 'glacier', 'height':4, 'start_y': 0, 'end_y': 2, 'tile_types': ['ice']},
            {'name': 'tundra', 'height':3, 'start_y': 2, 'end_y': 4, 'tile_types': ['permafrost']},
            {'name': 'taiga', 'height':3, 'start_y': 4, 'end_y': 6, 'tile_types': ['grass']},
            {'name': 'forest' , 'height':1, 'start_y': 6, 'end_y': 8, 'tile_types': ['grass']},
            {'name': 'grasslands', 'height':1, 'start_y': 8, 'end_y': 10, 'tile_types': ['grass']},
            {'name': 'mountains', 'height':8, 'start_y': 10, 'end_y': 12, 'tile_types': ['stone']},
            {'name': 'mediterraean', 'height':4, 'start_y': 12, 'end_y': 14, 'tile_types': ['grass']},
            {'name': 'ocean', 'height':-1, 'start_y': 12, 'end_y': 14, 'tile_types': ['sand']},
            {'name': 'archipelago', 'height':2, 'start_y': 12, 'end_y': 14, 'tile_types': ['sand']},
            {'name': 'savannah', 'height':2, 'start_y': 14, 'end_y': 16, 'tile_types': ['grass']},
            {'name': 'desert', 'height':1, 'start_y': 16, 'end_y': 18, 'tile_types': ['sand']},
            {'name': 'rock desert', 'height':3, 'start_y': 18, 'end_y': 20, 'tile_types': ['stone']},
            {'name': 'red desert', 'height':1, 'start_y': 20, 'end_y': 22, 'tile_types': ['sand']},
            {'name': 'rainforest','height':1, 'start_y': 22, 'end_y': 24, 'tile_types': ['grass']},
        ]
class Tile:
    def __init__(self,tile_type, x,y,h, chunk_x, chunk_y):
        self.x = x
        self.y = y
        self.h = h
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.tile_type = tile_type
class Chunk:
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome

class World:
    def __init__(self,map, w, h, sealevel, name):
        self.map = map
        self.w = w
        self.h = h
        self.ret_size= 128
        self.name = name
        self.sealevel = sealevel
    def return_map(self, ret_x, ret_y):
        dict = {}
        index = 0
        dict['tiles'] = []
        for i in range(int(ret_x), int(ret_x) + self.ret_size):
            for j in range(int(ret_y), int(ret_y) + self.ret_size):
                if i >= 0 and j >= 0 and i < self.w*CHUNK_SIZE-2 and j < self.h*CHUNK_SIZE-2:
                    print(len(self.map[i]) )
                    height = self.map[i][j].h
                    tile_type = self.map[i][j].tile_type
                else:
                    height = -1
                    tile_type = 'grass'
                dict['tiles'].append({f'tile_{index}':{'props':[{'x': f'{i}'}, {'y': f'{j}'}, {'h': f'{height}'}, {'type': f'{tile_type}'}]}})
                dict['metadata'] = {'sealevel': self.sealevel, 'width': self.w, 'height': self.h, 'name': self.name}

                index += 1
        return dict
class Generator:
    def __init__(self):
        self.world = None
    def generate(self, seed, w, h, sealevel, name):
        noise = PerlinNoise()
        noise1 = PerlinNoise(octaves=3,seed=seed)
        map = [[] for x in range((h)*CHUNK_SIZE)]
        # create height map
        chunk_x = 0
        chunk_y = 0
        chunks = []
        for i in range(w):
            crow = []
            for j in range(h):
                biome = BIOMES[random.randint(0,len((BIOMES))-1)]
                crow.append(Chunk(i,j,biome))
                for k in range(CHUNK_SIZE):

                    row = []
                    for x in range(CHUNK_SIZE):
                        noise_val = noise1([k/(w*CHUNK_SIZE), x/(h*CHUNK_SIZE)]) * biome['height']
                        tile_type = 'water' if -noise_val < sealevel else biome['tile_types'][0]
                        row.append(Tile(tile_type, k, x, -noise_val, i,j  ))
                    map[k+i*CHUNK_SIZE].extend(row)
            chunks.append(crow)
        self.world = World(map, w, h, sealevel, name)
    def get_world(self):
        return self.world

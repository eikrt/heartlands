from perlin_noise import PerlinNoise
import random
from datetime import datetime
CHUNK_BUFFER = 4
BORDER_FREQ = 4
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
    def __init__(self,map, w, h, sealevel, chunk_size, name):
        self.map = map
        self.w = w
        self.h = h
        self.ret_size= 128
        self.name = name
        self.chunk_size = chunk_size
        self.sealevel = sealevel
    def return_map(self, ret_x, ret_y):
        dict = {}
        index = 0
        dict['tiles'] = []
        for i in range(int(ret_x), int(ret_x) + self.ret_size):
            for j in range(int(ret_y), int(ret_y) + self.ret_size):
                if i >= 0 and j >= 0 and i < self.w*self.chunk_size-2 and j < self.h*self.chunk_size-2:
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


    def generate(self, seed,  w, h, chunk_size, sealevel, name):
        start_time = datetime.now()
        biome_num = 10*2
        biome_variation = 1
        biomes = [
    
            {'name': 'glacier', 'height':2, 'start_y': 0, 'end_y': h/biome_num, 'tile_types': ['ice']},
            {'name': 'tundra', 'height':1, 'start_y': 1*h/biome_num, 'end_y': 2*h/biome_num, 'tile_types': ['permafrost']},
            {'name': 'taiga', 'height':2, 'start_y': 2*h/biome_num, 'end_y': 3*h/biome_num, 'tile_types': ['grass']},
            {'name': 'forest' , 'height':1, 'start_y': 3*h/biome_num, 'end_y': 4*h/biome_num, 'tile_types': ['grass']},
            {'name': 'grasslands', 'height':1, 'start_y': 4*h/biome_num, 'end_y':5* h/biome_num, 'tile_types': ['grass']},
            {'name': 'mountains', 'height':4, 'start_y': 5*h/biome_num, 'end_y': 6*h/biome_num, 'tile_types': ['mountain_land']},
            {'name': 'mediterraean', 'height':2, 'start_y': 6/h/biome_num, 'end_y':7* h/biome_num, 'tile_types': ['coarse_land']},

            {'name': 'savannah', 'height':1, 'start_y': 9*h/biome_num, 'end_y': 10*h/biome_num, 'tile_types': ['savannah_land']},
            {'name': 'desert', 'height':1, 'start_y': 10*h/biome_num, 'end_y': 11*h/biome_num, 'tile_types': ['sand']},
            {'name': 'red desert', 'height':1, 'start_y': 12*h/biome_num, 'end_y': 13*h/biome_num, 'tile_types': ['red_sand']},
            {'name': 'rainforest','height':1, 'start_y': 13*h/biome_num, 'end_y': 14*h/biome_num, 'tile_types': ['grass']},
        ]
        global_biomes = [
                
                {'name': 'ocean', 'height':-4, 'tile_types': ['sand']},
                {'name': 'archipelago', 'height':-2, 'tile_types': ['grass']},
            ]
        ocean_frequency = 128
        archipelago_frequency = 256
        noise = PerlinNoise()
        noise1 = PerlinNoise(octaves=3,seed=seed)
        map = [[] for x in range((h)*chunk_size)]
        # create height map
        chunk_x = 0
        chunk_y = 0
        chunks = []
        print('Creating tiles...')
        for i in range(w):
            crow = []
            for j in range(h):
                biome = biomes[4]
                for b in biomes:
                    biome_i = j # choose biome from list, create symmetrical world by biomes
                    biome_i_with_variation = biome_i + random.randint(-biome_variation, biome_variation)
                    #biome_i_with_variation = j
                    if biome_i >= h/2:
                        biome_i_with_variation = h/2 + h/2-biome_i_with_variation

                    if biome_i_with_variation >= b['start_y'] and biome_i_with_variation <= b['end_y']:
                        biome = b
                        break
                crow.append(Chunk(i,j,biome))
                for k in range(chunk_size):

                    row = []
                    for x in range(chunk_size):
                        a_x = (i*chunk_size)+k # actual tile coords
                        a_y = (j*chunk_size)+x
                        noise_val = noise1([(a_x)/(w*chunk_size), (a_y)/(h*chunk_size)]) * biome['height']
                        tile_type = biome['tile_types'][0]
                        row.append(Tile(tile_type, k, x, -noise_val, i,j  ))
                    map[k+i*chunk_size].extend(row)
            chunks.append(crow)
        print('Applying water and biome gradient...')            
        for i in range(w):
            for j in range(h):
                for k in range(chunk_size):
                    for x in range(chunk_size):

                        biome = chunks[i][j].biome
                        a_x = (i*chunk_size)+k # actual tile coords
                        a_y = (j*chunk_size)+x

                        noise_val = noise1([(a_x)/(w*chunk_size), (a_y)/(h*chunk_size)]) * biome['height']
                        
                        tile_type = 'water' if -noise_val < sealevel else biome['tile_types'][0]
                        tile_type = map[a_x][a_y].tile_type
                        if k < CHUNK_BUFFER:
                            if random.randint(0,BORDER_FREQ) == 1 and i > 0:
                                tile_type = chunks[i-1][j].biome['tile_types'][0]
                                map[a_x][a_y].h /= chunks[i-1][j].biome['height']
                                
                        if k > chunk_size - CHUNK_BUFFER:
                            if random.randint(0,BORDER_FREQ) == 1 and i < w-1:
                                tile_type = chunks[i+1][j].biome['tile_types'][0]
                                map[a_x][a_y].h /= chunks[i+1][j].biome['height']

                        if x < CHUNK_BUFFER:
                            if random.randint(0,BORDER_FREQ) == 1 and j > 0:
                                tile_type = chunks[i][j-1].biome['tile_types'][0]
                                map[a_x][a_y].h /= chunks[i][j-1].biome['height']
                        if x > chunk_size - CHUNK_BUFFER:
                            if random.randint(0,BORDER_FREQ) == 1 and j < h-1:
                                tile_type = chunks[i][j+1].biome['tile_types'][0]
                                map[a_x][a_y].h /= chunks[i][j+1].biome['height']
                        map[a_x][a_y].tile_type = tile_type
        
        self.world = World(map, w, h, sealevel, chunk_size, name)
        print(f'Generated world {name} in time {datetime.now() - start_time}')
    def get_world(self):
        return self.world

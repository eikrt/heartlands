# this file is responsible for holding Generator, Tile, Chunk and World classes. World is the interface from where socket server gets the desired
# chunks of world
# Generator class generates the world
import noise
import math
import random
from datetime import datetime

BIOMES = [

    {'name': 'glacier', 'height':1, 'temperature': 5, 'temperature_margin': 5, 'tile_types': ['ice']},
    {'name': 'tundra', 'height':1, 'temperature': 10,  'temperature_margin': 5,'tile_types': ['permafrost']},
    {'name': 'taiga', 'height':1, 'temperature': 15, 'temperature_margin': 5,'tile_types': ['grass']},
    {'name': 'forest' , 'height':1, 'temperature': 20, 'temperature_margin': 5,'tile_types': ['grass']},
    {'name': 'grasslands', 'height':1, 'temperature': 25, 'temperature_margin': 5, 'tile_types': ['grass']},
    {'name': 'mediterraean', 'height':1, 'temperature': 25, 'temperature_margin': 5,'tile_types': ['coarse_land']},

    {'name': 'savannah', 'height':1, 'temperature': 30, 'temperature_margin': 5,'tile_types': ['savannah_land']},
    {'name': 'desert', 'height':1, 'temperature': 35, 'temperature_margin': 5,'tile_types': ['sand']},
    {'name': 'red desert', 'height':1, 'temperature': 40 , 'temperature_margin': 5, 'tile_types': ['red_sand']},
    {'name': 'rainforest','height':1, 'temperature': 45, 'temperature_margin': 5, 'tile_types': ['grass']},
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
    def __init__(self,map, w, h, sealevel, chunk_size, name):
        self.map = map
        self.w = w
        self.h = h
        self.ret_w = 512
        self.ret_h = 256
        self.name = name
        self.chunk_size = chunk_size
        self.sealevel = sealevel
    def return_map(self, ret_x, ret_y): # return a piece of world, size specified by ret_w and ret_h, location by parameters
        dict = {}
        index = 0
        dict['tiles'] = []
        for i in range(int(ret_x), int(ret_x) + self.ret_w):
            for j in range(int(ret_y), int(ret_y) + self.ret_h):
                if i >= 0 and j >= 0 and i < self.w*self.chunk_size and j < self.h*self.chunk_size:
                    height = self.map[i][j].h
                    tile_type = self.map[i][j].tile_type
                else:
                    height = -1
                    tile_type = 'void'
                dict['tiles'].append({f'tile_{index}':{'props':[{'x': f'{i}'}, {'y': f'{j}'}, {'h': f'{height}'}, {'type': f'{tile_type}'}]}})
                dict['metadata'] = {'sealevel': self.sealevel, 'width': self.w, 'height': self.h, 'name': self.name}

                index += 1
        return dict
class Generator:
    def __init__(self):
        self.world = None


    def generate(self, seed,  w, h, chunk_size, sealevel, name): # generate world from layers of perlin noise
        start_time = datetime.now()

        map = [[] for x in range((h)*chunk_size)]
        # create height ma3
        chunk_x = 0
        chunk_y = 0
        chunks = []
        chunk_buffer = chunk_size / random.randint(5,6)
        
        # height map 
        hmap_octaves = 3 # perlin parameter
        hmap_persistence = 1 # perlin parameter
        hmap_lacunarity = 16 # perlin parameter
        hmap_fraq = 8 # fraction to scale the noise pattern. For example 2 scales the noise patter to a larger one
        hmap_flatten = 8 # value to divide perlin output
        hmap_base = 0.1 # add base to noise
        # large scale terrain changes
        sea_octaves = 16 
        sea_persistence = -0.5
        sea_lacunarity = 2
        sea_fraq = 4

        # biome variety
        biome_octaves = 8
        biome_persistence = 1
        biome_lacunarity = 2
        biome_fraq = 16
        
        # mountains 
        mountain_octaves = 8
        mountain_persistence = 1
        mountain_lacunarity = 2
        mountain_fraq = 8
        mountain_base = 0
        mountain_flatten = 1
        mountain_threshold = 0.15 # accept only values below or over this value
        mountain_acceleration = 8 # multiply output with this value

        # river areas 
        riverarea_octaves = 16
        riverarea_persistence = -0.4
        riverarea_lacunarity = 3
        riverarea_fraq = 2
        riverarea_flatten = 1
        riverarea_threshold = 0.15
        riverarea_base = 0.0
        riverarea_acceleration = 2
        # rivers 
        river_octaves = 3
        river_persistence = 2
        river_lacunarity = 2
        river_fraq =0.2
        river_flatten = 1
        river_threshold = 0.0
        river_base = 0.05
        river_acceleration = 1

        # apply layers
        apply_seas = True
        apply_heightmap = True
        apply_mountains = True
        apply_rivers = False 
        apply_water = True
        print('Creating tiles and BIOMES...')

        for i in range(w):
            crow = []
            print((f'{(i/w)*100}%'))
            for j in range(h):
                crow.append(Chunk(i,j,'land'))
                for k in range(chunk_size):

                    row = []
                    for x in range(chunk_size):

                        a_x = (i*chunk_size)+k # actual tile coords
                        a_y = (j*chunk_size)+x
                        dist_from_equator = math.dist([a_y], [(h*chunk_size)/2])
                        if dist_from_equator == 0:
                            dist_from_equator = 0.1
                        if a_y != 0:
                            rel = ( 1- (dist_from_equator /  ((h*chunk_size)/2)))
                        else:
                            rel = 0
                        biome_val = noise.pnoise2(a_x/(w*biome_fraq),
                                                    a_y/(h*biome_fraq),
                                                    octaves=biome_octaves,
                                                    persistence=biome_persistence,
                                                    lacunarity=biome_lacunarity,
                                                    repeatx=w*chunk_size,
                                                    repeaty=h*chunk_size,
                                                    base=0)
                        biome_val += rel

                        temp = int(biome_val * 40)
                        biome = BIOMES[0]
                        for b in BIOMES:
                            if temp > b['temperature'] - b['temperature_margin'] and temp < b['temperature'] + b['temperature_margin']:
                                biome = b
                                break

                        height_val = 0
                        tile_type = biome['tile_types'][0]
                        row.append(Tile(tile_type, k, x, height_val, i,j  ))
                    map[k+i*chunk_size].extend(row)
            chunks.append(crow)

        if apply_seas:

            print("Applying seas...")
            for i in range(w*chunk_size):

                print((f'{(i/(w*chunk_size))*100}%'))
                for j in range(h*chunk_size):

                    noise_val = noise.pnoise2(i/(w*sea_fraq),
                                                j/(h*sea_fraq),
                                                octaves=sea_octaves,
                                                persistence=sea_persistence,
                                                lacunarity=sea_lacunarity,
                                                repeatx=w*chunk_size,
                                                repeaty=h*chunk_size,
                                                base=seed) * biome['height']
                    map[i][j].h = noise_val

        if apply_heightmap:

            print("Applying height variety and water")
            for i in range(w*chunk_size):

                print((f'{(i/(w*chunk_size))*100}%'))
                for j in range(h*chunk_size):
                    
                    height_val = noise.pnoise2(i/(w*chunk_size*hmap_fraq),
                                                    j /(h*chunk_size *hmap_fraq),
                                                    octaves=hmap_octaves,
                                                    persistence=hmap_persistence,
                                                    lacunarity=hmap_lacunarity,
                                                    repeatx=w*chunk_size,
                                                    repeaty=h*chunk_size,
                                                    base=seed) / hmap_flatten + hmap_base
                    map[i][j].h += height_val

        if apply_mountains:

            print("Applying mountains...")
            for i in range(w*chunk_size):

                print((f'{(i/(w*chunk_size))*100}%'))
                for j in range(h*chunk_size):
                    
                    height_val = noise.pnoise2(i/(w*chunk_size*mountain_fraq),
                                                    j /(h*chunk_size *mountain_fraq),
                                                    octaves=mountain_octaves,
                                                    persistence=mountain_persistence,
                                                    lacunarity=mountain_lacunarity,
                                                    repeatx=w*chunk_size,
                                                    repeaty=h*chunk_size,
                                                    base=seed) / mountain_flatten + mountain_base
                    if height_val > mountain_threshold:
                        map[i][j].h = height_val * mountain_acceleration

        if apply_rivers:

            print("Applying rivers...")
            for i in range(w*chunk_size):

                print((f'{(i/(w*chunk_size))*100}%'))
                for j in range(h*chunk_size):
                    

                    riverarea_val = noise.pnoise2(i/(w*chunk_size*riverarea_fraq),
                                                    j /(h*chunk_size *riverarea_fraq),
                                                    octaves=riverarea_octaves,
                                                    persistence=riverarea_persistence,
                                                    lacunarity=riverarea_lacunarity,
                                                    repeatx=w*chunk_size,
                                                    repeaty=h*chunk_size,
                                                    base=seed) / riverarea_flatten + riverarea_base
                    height_val = noise.pnoise2(i/(w*chunk_size*river_fraq),
                                                    j /(h*chunk_size *river_fraq),
                                                    octaves=river_octaves,
                                                    persistence=river_persistence,
                                                    lacunarity=river_lacunarity,
                                                    repeatx=w*chunk_size,
                                                    repeaty=h*chunk_size,
                                                    base=seed) / river_flatten + river_base
                    if riverarea_val > riverarea_threshold:
                        if height_val < river_threshold:
                            if map[i][j].h > sealevel:
                                map[i][j].h = -abs(height_val * river_acceleration)

        if apply_water:
            print("Applying water...")
            for i in range(w*chunk_size):
                for j in range(h*chunk_size):
                    if map[i][j].h < sealevel:
                        map[i][j].h = -map[i][j].h
                        map[i][j].tile_type="water"

        self.world = World(map, w, h, sealevel, chunk_size, name)
        print(f'Generated world {name} in time {datetime.now() - start_time}')
    def get_world(self):
        return self.world

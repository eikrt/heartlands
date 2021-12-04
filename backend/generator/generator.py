from perlin_noise import PerlinNoise
class Tile:
    def __init__(self,x,y,h):
        self.x = x
        self.y = y
        self.h = h
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
                if i > 0 and j > 0 and i < self.w-2 and j < self.h-2:
                    height = self.map[i][j].h
                else:
                    height = -1
                dict['tiles'].append({f'tile_{index}':{'props':[{'x': f'{i}'}, {'y': f'{j}'}, {'h': f'{height}'}]}})
                dict['metadata'] = {'sealevel': self.sealevel, 'width': self.w, 'height': self.h, 'name': self.name}
                index += 1
        return dict
class Generator:
    def __init__(self):
        self.world = None
    def generate(self, seed, w, h, sealevel, name):
        noise = PerlinNoise()
        noise1 = PerlinNoise(octaves=3,seed=seed)
        map = []
        for i in range(w):
            row = []
            for j in range(h):
                noise_val = noise1([i/w, j/h])

                row.append(Tile(i, j, -noise_val))
            map.append(row)
        self.world = World(map, w, h, sealevel, name)
    def get_world(self):
        return self.world

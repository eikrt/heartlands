from perlin_noise import PerlinNoise
class Tile:
    def __init__(self,x,y,h):
        self.x = x
        self.y = y
        self.h = h
class World:
    def __init__(self,map, w, h):
        self.map = map
        self.w = w
        self.h = h
        self.ret_size= 64
    def return_map(self, ret_x, ret_y):
        dict = {}
        index = 0
        for i in range(int(ret_x), int(ret_x) + self.ret_size):
            for j in range(int(ret_y), int(ret_y) + self.ret_size):
                if i > 0 and j > 0 and i < self.w-2 and j < self.h-2:
                    height = self.map[i][j].h
                else:
                    height = -1
                dict[f'tile_{index}'] = {'props':[{'x': f'{i}'}, {'y': f'{j}'}, {'h': f'{height}'}]}
                index += 1
        return dict
class Generator:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.world = None
    def generate(self, seed):
        noise = PerlinNoise()
        noise1 = PerlinNoise(octaves=3,seed=seed)
        map = []
        for i in range(self.w):
            row = []
            for j in range(self.h):
                noise_val = noise1([i/self.w, j/self.h])

                row.append(Tile(i, j, -noise_val))
            map.append(row)
        self.world = World(map, self.w, self.h)
    def get_world(self):
        return self.world

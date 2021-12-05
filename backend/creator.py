import pickle
import sys
from generator import generator
seed = 100
width = 32
height = 32
sealevel = 1
chunk_size = 16
FILENAME = 'dat/world.dat'

def write(world, filename):
    with open(filename, "wb") as outp:
        pickle.dump(world, outp, pickle.HIGHEST_PROTOCOL)
def create():
    print(f'Writing world with seed {seed}...')
    gen = generator.Generator()
    gen.generate(seed, width, height, chunk_size, sealevel, 'Land Of Green')
    print(f'Writing to file {FILENAME}')
    write(gen.get_world(), FILENAME)
if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Provide all arguments")
        exit()
    seed = int(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    chunk_size = int(sys.argv[4])
    sealevel = float(sys.argv[5])
    create()



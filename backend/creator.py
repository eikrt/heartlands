import pickle
from generator import generator
SEED = 100
FILENAME = 'dat/world.dat'
def write(world, filename):
    with open(filename, "wb") as outp:
        pickle.dump(world, outp, pickle.HIGHEST_PROTOCOL)
def create():
    print(f'Writing world with seed {SEED}...')
    gen = generator.Generator(256,256)
    gen.generate(SEED)
    print(f'Writing to file {FILENAME}')
    write(gen.get_world(), FILENAME)



create()

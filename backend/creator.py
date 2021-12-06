# creator file is responsible for file io, name generating, taking parameters and creating a world generation call from them

import pickle
import sys
import os
import string
import subprocess
import random
from generator import generator

# some default values
seed = 100
width = 32
height = 32
sealevel = 1
chunk_size = 16 # world is divided into chunks

FILENAME = 'dat/world.dat'

def write(world, filename): # write world to disc
    with open(filename, "wb") as outp:
        pickle.dump(world, outp, pickle.HIGHEST_PROTOCOL)
def generate_world_name(): # take random word from dict, reverse it and change its first and last letter and random letter
    lower_upper_alphabet = string.ascii_letters
    random_letter1 = random.choice(lower_upper_alphabet)
    random_letter2 = random.choice(lower_upper_alphabet)
    random_letter3 = random.choice(lower_upper_alphabet)
    words = subprocess.check_output('cat /usr/share/dict/american-english', shell=True).decode('utf-8')#os.system('cat /usr/share/dict/american-english'))
    word_list = words.split('\n')
    name = word_list[random.randint(0,len(word_list)-1)]
    name = name[::-1].lower()
    name = name.replace(name[0], random_letter1)
    name = name.replace(name[-1], random_letter2)
    name = name.replace(name[random.randint(0,len(name)-1)], random_letter3)
    name = name.capitalize()
    return name 
    
def create():
    print(f'Writing world with seed {seed}...')
    gen = generator.Generator()
    gen.generate(seed, width, height, chunk_size, sealevel, generate_world_name())
    print(f'Writing to file {FILENAME}')
    write(gen.get_world(), FILENAME)

if __name__ == '__main__': # arguments: seed, width in chunks, height in chunks, chunk size in tiles, sealevel (preferably -1...1)
    if len(sys.argv) < 6:
        print("Provide all arguments")
        exit()
    seed = int(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    chunk_size = int(sys.argv[4])
    sealevel = float(sys.argv[5])
    create()



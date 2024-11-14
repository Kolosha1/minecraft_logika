import os 
from ursina import load_texture 

block_textures = []

DEFAULT_BLOCK=3
MAP_SIZE = 40
TREE_DENSITY=100
BASE_DIR = os.getcwd()
BLOCK_DIR = os.path.join(BASE_DIR, 'assets/blocks')

file_list = os.listdir(BLOCK_DIR)

for image in file_list:
    texture = load_texture('assets/blocks' + os.sep + image)
    block_textures.append(texture)
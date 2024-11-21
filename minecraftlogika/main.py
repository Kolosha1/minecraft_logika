from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()
from settings import *
from models import *
import pickle

class GameController:
    def __init__(self):


        sky = Sky(texture='sky_sunset')
        sun = DirectionalLight(shadows=True)
        sun.look_at(Vec3(1,-1,1 ))
        scene.blocks={}
        scene.trees={}
        self.map = Map()
        self.map.generate()

        self.player = Player(self.map)
    def save(self):
        game_data = {
            "player_pos":( self.player.x,self.player.y,self.player.z),
            "blocks":[],
            "trees": [],
        }

        for block_pos, block_id  in scene.blocks.items():
            game_data["blocks"].append((block_pos,block_id.id))

        for tree_pos, tree  in scene.trees.items():
            game_data["trees"].append((tree_pos,tree))

        with open("save.dat","wb") as file:
            pickle.dump(game_data,file)

        print_on_screen("Гру збережено", position=(-0.8,0.45),origin=(-.5,.5),scale=1,duration=1)
        
    def clear_map(self):
        for block in scene.blocks.values():
            destroy(block)
        for tree in scene.trees.values():
            destroy(tree)   
        scene.blocks.clear()
        scene.trees.clear()

    def load(self):
        with open('save.dat', "rb") as file:
            game_data = pickle.load(file)
            self.clear_map()
            for block_pos, block_id in game_data["blocks"]:
                Block(block_pos,block_id)
            for tree_pos, tree in game_data["trees"]:
                Tree(tree_pos)

            self.player.position = game_data["player_pos"]
            print_on_screen("Збереження завантажено", position=(-0.8,0.45),origin=(-.5,.5),scale=1,duration=1)

game = GameController()
def input(key):
    if key == 'k':
        game.save()
    if key == 'l':
        game.load()

window.fullscreen = True
app.run()
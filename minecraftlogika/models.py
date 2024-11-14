from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from settings import*

from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
from perlin_noise import PerlinNoise
from numpy import floor
import pickle   
class Tree(Button):
    def __init__(self, pos,  **kwargs):
        super().__init__(parent=scene,
                         color = color.color(0,0, random.uniform(0.9, 1)),
                         highlight_color=color.gray,
                         model='assets\\minecraft tree\\scene.gltf',
                         position=pos,
                         scale=5,
                         collider='box',
                         origin_y=.5,
                         shader=basic_lighting_shader,
                         **kwargs)

class Block(Button):
    current=DEFAULT_BLOCK

    def __init__(self, pos, texture_id=3,parent=scene, **kwargs):
        super().__init__(parent=parent,
                         color= color.color(0,0,random.uniform(0.9,1)),
                         model='cube',
                         texture=block_textures[texture_id],
                         position=pos,
                         scale = 1,
                         collider='box',
                         origin_y=-0.5,
                         shader=basic_lighting_shader,
                         **kwargs)
        scene.blocks[(self.x,self.y,self.z)] = texture_id
        

class Map(Entity):
    def __init__(self, **kwargs):
         super().__init__(model=None,collider=None, **kwargs)
         self.blocks={}
         self.ground = Entity(model='plane',position=(MAP_SIZE//2,MAP_SIZE//2),collider='box', scale=MAP_SIZE, texture=block_textures[DEFAULT_BLOCK], texture_scale=(4,4))
         self.ground.y=-3
         self.noise = PerlinNoise(octaves=2,seed=6666)
         self.bg_music = Audio(sound_file_name='assets\\audio\\crafting_game_music.mp3', autoplay=True,loop=True,volume=0.2)



    def generate(self):
        for x in range(MAP_SIZE):
            for z in range(MAP_SIZE):
                y = floor(self.noise([x/24,z/24])*6)
                cube = Block((x,y,z),DEFAULT_BLOCK,self)

                rand_num = random.randint(1,TREE_DENSITY)
                if rand_num == 75:
                    Tree((x,y+1,z))

class Player(FirstPersonController):
    def __init__(self,map, **kwargs):
        super().__init__(**kwargs)
        self.map = map
        self.build_sound = Audio(sound_file_name='assets\\audio\\wood01.ogg', autoplay=False)
        self.destroy_sound = Audio(sound_file_name='assets\\audio\\gravel.ogg', autoplay=False)
        self.creative_mode = False
        self.held_block = Entity(model='cube', texture=block_textures[Block.current],
                                 parent=camera.ui,position=(0.6,-0.42),
                                 rotation=Vec3(30,-30,10),
                                 shader=basic_lighting_shader,
                                 scale = 0.2,
                                 )           

    def input(self,key):
        super().input(key)

        if key == "left mouse down" and mouse.hovered_entity and mouse.hovered_entity!=self.map.ground:
            self.destroy_sound.play()
            destroy(mouse.hovered_entity)

        if key == "right mouse down" and mouse.hovered_entity:
            hit_info=raycast(camera.world_position,camera.forward,distance=15)
            if hit_info.hit and isinstance(hit_info.entity,Block):
                Block(hit_info.entity.position + hit_info.normal, Block.current)

            
        if key == "scroll up":
            Block.current +=1
            if Block.current >= len(block_textures):
                Block.current = 0

        if key == "scroll down":
            Block.current -=1
            if Block.current <0:
                Block.current = len(block_textures) - 1

        if key == "c":
            self.creative_mode= not self.creative_mode
            if self.creative_mode:
                print_on_screen("Режим створення увімкнено", position=(-0.8, 0.45), origin=(-.5,.5), scale=1, duration=1)
            else:
                print_on_screen("Режим створення вимкнено", position=(-0.8, 0.42), origin=(-.5,.5), scale=1, duration=1)
    
    def update(self):
        super().update()
    
        if self.creative_mode:
            self.gravity=0
            self.grounded=True
        else:
            self.gravity=1

        if held_keys['control']and self.creative_mode:
            self.y-=self.speed * time.dt
        
        if not self.creative_mode and self.y<-10:
            self.y = 10
            self.x = MAP_SIZE//2
            self.z = MAP_SIZE//2

        # if not self.creative_mode:
        #     if self.x > MAP_SIZE:
        #         self.x = MAP_SIZE
        #     if self.z > MAP_SIZE:
        #         self.z = MAP_SIZE

        #     if self.x < 0:
        #         self.x = 0
        #     if self.z< 0:
        #         self.z = 0
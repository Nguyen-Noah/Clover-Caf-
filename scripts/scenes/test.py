import imgui, json
from engine.ecs.scene import Scene
from engine.ecs.entity import Entity
from engine.misc.camera import Camera
from engine.tile.tilemap import Tilemap
from ..constants.window import Screen
from engine.components.transform import Transform
from engine.components.sprite_renderer import SpriteRenderer
from engine.components.sprite import Sprite
from engine.components.spritesheet import Spritesheet
from engine.primitives.vec2 import vec2

from engine.utils.io import read_json, write_json

class TestScene(Scene):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.load_resources()

        self.sprites = self.e['Assets'].get_spritesheet('veggies.png')

        """ self.entity1 = Entity(name=f'Turnip Seeds', 
                              transform=Transform(vec2(430, 170), vec2(100, 100)),
                              z_index=3
                              )
        self.entity1.add_component(SpriteRenderer(sprite=self.sprites.get_sprite(0)))
        self.add_entity_to_scene(self.entity1)

        entity2 = Entity(name=f'Onion', 
                         transform=Transform(vec2(400, 200), vec2(100, 200)),
                         z_index=1
                         )
        entity2.add_component(SpriteRenderer(sprite=self.sprites.get_sprite(5)))
        self.add_entity_to_scene(entity2) """

        #self.save_exit()
        self.load('level.json')

        self.active_entity = self.entities[0]

        self.camera = Camera(Screen.RESOLUTION)

    def load_resources(self):
        self.e['Assets'].get_shader('vsDefault.glsl', 'default.glsl')
        self.e['Assets'].add_spritesheet('veggies.png', 
                            Spritesheet(self.e['Assets'].get_texture('veggies.png'),
                                        16, 16, 8, 0))

    def imgui(self):
        pass
        """ imgui.begin('Test window')
        imgui.text('Some random text')
        imgui.end() """

    def update(self, dt):
        self.camera.update()
        for entity in self.entities:
            entity.update(dt)

        self.renderer.render()

    def render(self):
        pass
        #self.tilemap.render()
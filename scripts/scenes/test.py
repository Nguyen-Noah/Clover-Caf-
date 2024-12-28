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

class TestScene(Scene):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.load_resources()

        self.sprites = self.e['Assets'].get_spritesheet('veggies.png')


        self.test_entity = Entity('test')
        self.add_entity_to_scene(self.test_entity)
        
        entity1 = Entity(name=f'Obj (x, y)', transform=Transform(vec2(32, 16), vec2(100, 100)))
        entity1.add_component(SpriteRenderer(sprite=self.sprites.get_sprite(0)))
        self.add_entity_to_scene(entity1)

        entity2 = Entity(name=f'Obj (x, y)', transform=Transform(vec2(800, 56), vec2(100, 100)))
        entity2.add_component(SpriteRenderer(sprite=self.sprites.get_sprite(5)))
        self.add_entity_to_scene(entity2)


        self.camera = Camera(Screen.RESOLUTION)
        #self.tilemap = Tilemap(self, 'test', scale_ratio=Screen.SCALE_RATIO)
        
    def load_resources(self):
        self.e['Assets'].get_shader('vsDefault.glsl', 'default.glsl')
        self.e['Assets'].add_spritesheet('veggies.png', 
                            Spritesheet(self.e['Assets'].get_texture('veggies.png'),
                                        16, 16, 8, 0))

    def update(self, dt):
        self.camera.update()
        for entity in self.entities:
            entity.update(dt)

        self.renderer.render()

    def render(self):
        pass
        #self.tilemap.render()
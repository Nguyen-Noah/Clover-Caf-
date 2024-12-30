from ..ecs.entity import Entity
from ..components.transform import Transform
from ..components.sprite_renderer import SpriteRenderer
from ..primitives.vec2 import vec2

class Prefabs:
    def generate_sprite_object(sprite, size_x, size_y):
        block = Entity(name='Sprite_Object_Gen', 
                       transform=Transform(vec2(), vec2(size_x, size_y)),
                       z_index=0)
        renderer = SpriteRenderer(sprite=sprite)
        block.add_component(renderer)

        return block
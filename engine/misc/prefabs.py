from ..ecs.entity import Entity
from ..components.transform import Transform
from ..components.sprite_renderer import SpriteRenderer
from ..primitives.vec2 import vec2

class Prefabs:
    @staticmethod
    def generate_sprite_object(e, sprite, size_x, size_y):
        block = e['Game'].current_scene.create_entity(name='Sprite_Object_Gen')
        block.transform.scale.x = size_x
        block.transform.scale.y = size_y
        renderer = SpriteRenderer(sprite=sprite)
        block.add_component(renderer)
        return block
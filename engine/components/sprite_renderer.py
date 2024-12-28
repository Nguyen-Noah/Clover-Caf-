from ..ecs.component import Component
from ..primitives.vec2 import vec2

class SpriteRenderer(Component):
    def __init__(self, color=(1, 1, 1, 1), sprite=None):
        super().__init__()
        self.color = color
        self.sprite = sprite

    def get_texture(self):
        return self.sprite.texture
    
    def get_tex_coords(self):
        return self.sprite.tex_coords
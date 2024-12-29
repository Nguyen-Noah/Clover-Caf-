from ..ecs.component import Component
from ..components.transform import Transform
from ..primitives.vec2 import vec2

class SpriteRenderer(Component):
    def __init__(self, color=(1, 1, 1, 1), sprite=None):
        super().__init__()
        self._color = color
        self._sprite = sprite

        self.last_transform = None
        self.dirty = True

    def start(self):
        self.last_transform = self.entity.transform.copy()

    def get_texture(self):
        return self.sprite.texture
    
    def get_tex_coords(self):
        return self.sprite.tex_coords
    
    def is_dirty(self):
        return self.dirty
    
    def clean(self):
        self.dirty = False
    
    @property
    def sprite(self):
        return self._sprite

    def set_sprite(self, new_sprite):
        self._sprite = new_sprite
        self.dirty = True

    @property
    def color(self):
        return self._color

    def set_color(self, new_color):
        if not self.color.equals(new_color):
            self._color = new_color
            self.dirty = True

    def update(self, dt):
        # check if the transform has changed
        if not self.last_transform.equals(self.entity.transform):
            self.entity.transform.copy(self.last_transform)
            self.dirty = True
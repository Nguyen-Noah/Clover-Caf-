from .component import Component
from .component_deserializer import register_component
from engine.components.sprite import Sprite
from engine.primitives.vec4 import vec4

@register_component
class SpriteRenderer(Component):
    def __init__(self, color=None, sprite=None):
        super().__init__()
        self.color = color if color is not None else vec4(1, 1, 1, 1)
        self.sprite = sprite

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

    def set_sprite(self, new_sprite):
        self.sprite = new_sprite
        self.dirty = True

    def set_color(self, new_color):
        if self.color != new_color:
            self.color = new_color
            self.dirty = True

    def editor_update(self, dt):
        if not self.last_transform.equals(self.entity.transform):
            self.entity.transform.copy(self.last_transform)
            self.dirty = True

    def update(self, dt):
        # check if the transform has changed
        if not self.last_transform.equals(self.entity.transform):
            self.entity.transform.copy(self.last_transform)
            self.dirty = True

    def serialize(self):
        data = super().serialize()
        data.update({
            "color": self.color.serialize(),
            "sprite": self.sprite.serialize()
        })
        return data
    
    @classmethod
    def deserialize(cls, data):
        return cls(color=vec4.deserialize(data['color']), sprite=Sprite.deserialize(data['sprite']))
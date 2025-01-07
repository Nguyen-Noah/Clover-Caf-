import imgui
from .component import Component
from ..components.transform import Transform
from ..components.sprite import Sprite
from ..primitives.vec4 import vec4

class SpriteRenderer(Component):
    def __init__(self, color=vec4(1, 1, 1, 1), sprite=None):
        super().__init__()
        self.color = color
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
    
    def imgui(self):
        changed, im_vec = imgui.color_edit4('Color Picker', *self.color,
                              imgui.COLOR_EDIT_NO_INPUTS | 
                              imgui.COLOR_EDIT_ALPHA_BAR)
        if changed:
            self.set_color(vec4(*im_vec))

    def set_sprite(self, new_sprite):
        self.sprite = new_sprite
        self.dirty = True

    def set_color(self, new_color):
        # if new_color.x == 1:
        #      print(f'old {self.color}; new {new_color}; diff {self.color != new_color}')
        if self.color != new_color:
            self.color = new_color
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
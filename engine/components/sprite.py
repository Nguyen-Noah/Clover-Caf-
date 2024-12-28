from ..primitives.vec2 import vec2

class Sprite:
    def __init__(self, texture, tex_coords=[
            vec2(1, 1),
            vec2(1, 0),
            vec2(0, 0),
            vec2(0, 1),
        ]):
        self.texture = texture
        self.tex_coords = tex_coords
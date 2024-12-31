from ..primitives.vec2 import vec2
from ..rendering.texture import Texture

class Sprite:
    def __init__(self, texture, width, height, tex_coords=[
            vec2(1, 1),
            vec2(1, 0),
            vec2(0, 0),
            vec2(0, 1),
        ]):
        self.texture = texture
        self.width = width
        self.height = height
        self.tex_coords = tex_coords

    def get_tex_id(self):
        return -1 if self.texture is None else self.texture.get_id()

    def serialize(self):
        return {
            "texture": self.texture.serialize() if self.texture else None,
            "width": self.width,
            "height": self.height,
            "tex_coords": [coord.serialize() for coord in self.tex_coords]
        }
    
    @classmethod
    def deserialize(cls, data):
        texture_data = data['texture']
        texture = Texture.deserialize(texture_data) if texture_data else None

        tex_coords_data = data.get("tex_coords", [])
        tex_coords = [vec2.deserialize(coord) for coord in tex_coords_data]

        return cls(texture=texture, width=data.get("width"), height=data.get("height"), tex_coords=tex_coords)
from ..primitives.vec2 import vec2
from ..assets.texture import Texture

class Sprite:
    def __init__(self, texture, tex_coords=[
            vec2(1, 1),
            vec2(1, 0),
            vec2(0, 0),
            vec2(0, 1),
        ]):
        self.texture = texture
        self.tex_coords = tex_coords

    # ADD TEXTURE SERAILIATION
    def serialize(self):
        return {
            "texture": self.texture.serialize() if self.texture else None,
            "tex_coords": [coord.serialize() for coord in self.tex_coords]
        }
    
    @classmethod
    def deserialize(cls, data):
        texture_data = data['texture']
        texture = Texture.deserialize(texture_data) if texture_data else None

        tex_coords_data = data.get("tex_coords", [])
        tex_coords = [vec2.deserialize(coord) for coord in tex_coords_data]

        return cls(texture=texture, tex_coords=tex_coords)
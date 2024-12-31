import moderngl
from ..utils.elements import Element
from ..utils.assets import load_texture

class Texture(Element):
    def __init__(self, path="Generated", width=None, height=None):
        super().__init__()
        self.path = path
        if path is not "Generated":
            self.load_texture(self.path)
        if width is not None and height is not None:
            self.texture = self.e['Game'].ctx.texture((width, height), 3)
            self.texture.repeat_x = True
            self.texture.repeat_y = True
            self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

    def load_texture(self, path):
        self.texture = load_texture(path, self.e['Game'].ctx)
        self.width = self.texture.width
        self.height = self.texture.height
        self.size = self.texture.size

    def get_id(self):
        return self.texture.glo

    def serialize(self):
        return {
            "path": self.path,
            "width": self.width,
            "height": self.height
        }
    
    @classmethod
    def deserialize(cls, data):
        texture = cls(data['path'])
        return texture
    